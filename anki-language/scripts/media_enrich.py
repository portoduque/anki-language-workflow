#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import json
import os
import re
import subprocess
import sys
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

from PIL import Image

from media_validate import MediaValidationError, validate_media_file

USER_AGENT = "anki-language-workflow/1.0 (https://github.com/portoduque/anki-language-workflow)"
DEFAULT_IMAGE_LICENSES = ["cc0", "pdm"]


def safe_id(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "-", value).strip("-")
    return cleaned[:80] or "card"


def http_json(url: str, headers: dict[str, str] | None = None) -> dict[str, Any]:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, **(headers or {})})
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.load(response)


def download_bytes(url: str, max_bytes: int = 25 * 1024 * 1024) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=45) as response:
        chunks: list[bytes] = []
        total = 0
        while True:
            chunk = response.read(1024 * 1024)
            if not chunk:
                break
            total += len(chunk)
            if total > max_bytes:
                raise ValueError(f"Remote media exceeds {max_bytes} bytes: {url}")
            chunks.append(chunk)
        return b"".join(chunks)


def piper_voice(target_code: str, requested: str | None = None) -> tuple[str, dict[str, Any]]:
    try:
        from piper.download_voices import get_voices
    except ImportError as exc:
        raise RuntimeError(
            "Automatic TTS requires Piper. Install: python -m pip install -r requirements-media.txt"
        ) from exc

    voices = get_voices()
    if requested:
        if requested not in voices:
            raise RuntimeError(f"Requested Piper voice is unavailable: {requested}")
        return requested, voices[requested]

    normalized = target_code.replace("-", "_")
    prefixes = [normalized + "-"]
    if "_" in normalized:
        prefixes.append(normalized.split("_", 1)[0] + "_")
    else:
        prefixes.append(normalized + "_")

    candidates = [name for name in voices if any(name.startswith(prefix) for prefix in prefixes)]
    if not candidates:
        raise RuntimeError(f"No Piper voice found for target language code: {target_code}")

    quality_rank = {"medium": 0, "high": 1, "low": 2, "x_low": 3}
    candidates.sort(key=lambda name: (quality_rank.get(name.rsplit("-", 1)[-1], 9), name))
    selected = candidates[0]
    return selected, voices[selected]


def synthesize_piper(text: str, target_code: str, output: Path, voice: str | None, voice_dir: Path) -> tuple[str, dict[str, Any]]:
    try:
        from piper.download_voices import download_voice
    except ImportError as exc:
        raise RuntimeError(
            "Automatic TTS requires Piper. Install: python -m pip install -r requirements-media.txt"
        ) from exc

    selected, metadata = piper_voice(target_code, voice)
    voice_dir.mkdir(parents=True, exist_ok=True)
    download_voice(selected, voice_dir)
    output.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        sys.executable, "-m", "piper",
        "--data-dir", str(voice_dir),
        "-m", selected,
        "-f", str(output),
        "--", text,
    ]
    completed = subprocess.run(cmd, check=False, text=True, capture_output=True)
    if completed.returncode != 0:
        raise RuntimeError(f"Piper failed for {selected}: {completed.stderr.strip() or completed.stdout.strip()}")
    return selected, metadata


def normalize_image(raw_path: Path, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(raw_path) as image:
        image.load()
        if image.mode not in {"RGB", "RGBA"}:
            image = image.convert("RGB")
        image.thumbnail((1600, 1600))
        image.save(output_path, format="WEBP", quality=86, method=6)


def openverse_candidates(query: str, licenses: list[str]) -> list[dict[str, Any]]:
    params = urllib.parse.urlencode({
        "q": query,
        "license": ",".join(licenses),
        "mature": "false",
        "filter_dead": "true",
        "page_size": "10",
    })
    headers: dict[str, str] = {}
    token = os.getenv("OPENVERSE_API_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    data = http_json(f"https://api.openverse.org/v1/images/?{params}", headers)
    allowed = {item.casefold() for item in licenses}
    results = []
    for item in data.get("results", []):
        license_name = str(item.get("license", "")).casefold()
        if license_name not in allowed:
            continue
        url = item.get("url") or item.get("thumbnail")
        if not url:
            continue
        results.append({
            "url": url,
            "title": item.get("title") or "",
            "license": item.get("license") or "",
            "license_url": item.get("license_url") or "",
            "creator": item.get("creator") or "",
            "attribution": item.get("attribution") or "",
            "source_url": item.get("foreign_landing_url") or item.get("detail_url") or "",
            "provider": f"openverse:{item.get('source') or item.get('provider') or 'unknown'}",
        })
    return results


def strip_html(value: str) -> str:
    return re.sub(r"<[^>]+>", "", html.unescape(value or "")).strip()


def wikimedia_candidates(query: str, licenses: list[str]) -> list[dict[str, Any]]:
    params = {
        "action": "query",
        "format": "json",
        "formatversion": "2",
        "generator": "search",
        "gsrsearch": query,
        "gsrnamespace": "6",
        "gsrlimit": "10",
        "prop": "imageinfo",
        "iiprop": "url|extmetadata|mime|mediatype|size",
    }
    data = http_json("https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(params))
    wanted = {x.casefold() for x in licenses}
    results = []
    for page in data.get("query", {}).get("pages", []):
        info = (page.get("imageinfo") or [{}])[0]
        meta = info.get("extmetadata") or {}
        short = strip_html((meta.get("LicenseShortName") or {}).get("value", "")).casefold()
        license_key = "cc0" if "cc0" in short else "pdm" if ("public domain" in short or "pdm" in short) else ""
        if license_key not in wanted:
            continue
        url = info.get("url")
        if not url:
            continue
        results.append({
            "url": url,
            "title": page.get("title", ""),
            "license": strip_html((meta.get("LicenseShortName") or {}).get("value", "")),
            "license_url": strip_html((meta.get("LicenseUrl") or {}).get("value", "")),
            "creator": strip_html((meta.get("Artist") or {}).get("value", "")),
            "attribution": strip_html((meta.get("Credit") or {}).get("value", "")) or strip_html((meta.get("Artist") or {}).get("value", "")),
            "source_url": info.get("descriptionurl") or "",
            "provider": "wikimedia-commons",
        })
    return results


def fetch_image(query: str, provider: str, licenses: list[str], output: Path) -> dict[str, Any]:
    providers = [provider] if provider != "auto" else ["openverse", "wikimedia"]
    failures: list[str] = []
    for current in providers:
        try:
            candidates = openverse_candidates(query, licenses) if current == "openverse" else wikimedia_candidates(query, licenses)
        except Exception as exc:
            failures.append(f"{current}: search failed: {exc}")
            continue
        for index, candidate in enumerate(candidates):
            raw = output.with_suffix(f".candidate-{index}")
            try:
                raw.write_bytes(download_bytes(str(candidate["url"])))
                normalize_image(raw, output)
                validation = validate_media_file(output, "image")
                candidate["validation"] = validation
                return candidate
            except Exception as exc:
                failures.append(f"{current} candidate {index}: {exc}")
            finally:
                raw.unlink(missing_ok=True)
    raise RuntimeError("No functional licensed image candidate found. " + " | ".join(failures[-8:]))


def resolve_path(plan_dir: Path, raw: str) -> Path:
    path = Path(raw)
    return path.resolve() if path.is_absolute() else (plan_dir / path).resolve()


def relative_to_plan(path: Path, plan_dir: Path) -> str:
    try:
        return str(path.resolve().relative_to(plan_dir.resolve()))
    except ValueError:
        return str(path.resolve())


def enrich_plan(plan_path: Path, output_path: Path, media_dir: Path | None = None) -> dict[str, Any]:
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    plan_dir = plan_path.resolve().parent
    media_root = (media_dir or (plan_dir / "media")).resolve()
    voice_dir = media_root / ".piper-voices"
    media_root.mkdir(parents=True, exist_ok=True)
    counts = {"audio_generated": 0, "images_downloaded": 0, "media_validated": 0}

    for card in plan.get("cards", []):
        card_validation = dict(card.get("media_validation") or {})

        if card.get("audio"):
            path = resolve_path(plan_dir, str(card["audio"]))
            card_validation["audio"] = validate_media_file(path, "audio")
            counts["media_validated"] += 1
        elif card.get("audio_request"):
            request = card["audio_request"]
            provider = request.get("provider", "auto")
            if provider not in {"auto", "piper"}:
                raise RuntimeError(f"Unsupported audio provider: {provider}")
            output = media_root / f"{safe_id(str(card['id']))}-audio.wav"
            selected, metadata = synthesize_piper(
                str(request["text"]),
                str(plan["target_language"]["code"]),
                output,
                request.get("voice"),
                voice_dir,
            )
            validation = validate_media_file(output, "audio")
            card["audio"] = relative_to_plan(output, plan_dir)
            license_meta = metadata.get("license") if isinstance(metadata, dict) else None
            if isinstance(license_meta, dict):
                license_text = str(license_meta.get("name") or license_meta.get("url") or "")
            else:
                license_text = str(license_meta or "")
            card["audio_provenance"] = {
                "kind": "tts",
                "provider": f"piper:{selected}",
                "source_url": "https://github.com/OHF-Voice/piper1-gpl",
                **({"license": license_text} if license_text else {}),
            }
            card_validation["audio"] = validation
            counts["audio_generated"] += 1
            counts["media_validated"] += 1

        if card.get("image"):
            path = resolve_path(plan_dir, str(card["image"]))
            card_validation["image"] = validate_media_file(path, "image")
            counts["media_validated"] += 1
        elif card.get("image_request"):
            request = card["image_request"]
            licenses = [str(x).casefold() for x in (request.get("licenses") or DEFAULT_IMAGE_LICENSES)]
            output = media_root / f"{safe_id(str(card['id']))}-image.webp"
            result = fetch_image(
                str(request["query"]),
                str(request.get("provider", "auto")),
                licenses,
                output,
            )
            card["image"] = relative_to_plan(output, plan_dir)
            card["image_provenance"] = {
                "kind": "licensed",
                "provider": str(result["provider"]),
                "source_url": str(result.get("source_url") or ""),
                "license": str(result.get("license") or ""),
                **({"license_url": str(result.get("license_url"))} if result.get("license_url") else {}),
                **({"attribution": str(result.get("attribution"))} if result.get("attribution") else {}),
            }
            card_validation["image"] = result["validation"]
            counts["images_downloaded"] += 1
            counts["media_validated"] += 1

        if card_validation:
            card["media_validation"] = card_validation

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"status": "ok", "output": str(output_path.resolve()), **counts}


def main() -> int:
    parser = argparse.ArgumentParser(description="Resolve automatic audio/image requests and validate every media file.")
    parser.add_argument("plan", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--media-dir", type=Path)
    args = parser.parse_args()
    output = args.output or args.plan.with_name(args.plan.stem + ".resolved.json")
    try:
        report = enrich_plan(args.plan, output, args.media_dir)
    except (OSError, ValueError, RuntimeError, MediaValidationError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}")
        return 1
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
