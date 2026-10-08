#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
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

from audio_clip import clip_audio
from card_contract import AUDIO_REQUIRED_PRONUNCIATION_MODES, normalize_mode
from media_validate import MediaValidationError, validate_media_file
from validate_plan import validate_plan

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


def piper_voice(
    target_code: str, requested: str | None = None, voice_dir: Path | None = None
) -> tuple[str, dict[str, Any]]:
    """Resolve modern/legacy Piper voices, including offline downloaded voices."""
    normalized = target_code.replace("-", "_")
    installed = {
        f.stem: {} for f in (voice_dir.glob("*.onnx") if voice_dir and voice_dir.is_dir() else [])
        if f.with_suffix(".onnx.json").is_file()
    }
    if requested and requested in installed:
        if not (requested.startswith(normalized + "-") or (
            len(normalized) == 2 and requested.startswith(normalized + "_")
        )):
            raise RuntimeError(f"Piper voice {requested!r} is not for target language {target_code}.")
        return requested, installed[requested]
    voices: dict[str, dict[str, Any]] = {}
    try:
        from piper.download_voices import get_voices
        try:
            voices = get_voices()
        except TypeError:
            voices = get_voices(voice_dir or Path.cwd())
    except (ImportError, OSError, ValueError, RuntimeError):
        # Some distributions do not export get_voices. The supported CLI
        # prints one voice ID per line (avoid unstable private Python APIs).
        result = subprocess.run(
            [sys.executable, "-m", "piper.download_voices"],
            capture_output=True, text=True, check=False, timeout=30,
        )
        if result.returncode == 0:
            voices = {name.strip(): {} for name in result.stdout.splitlines()
                      if re.match(r"^[a-z]{2,3}_[A-Z]{2}-[\\w-]+$", name.strip())}
    voices = {**voices, **installed}
    if requested:
        if not (requested.startswith(normalized + "-") or (
            len(normalized) == 2 and requested.startswith(normalized + "_")
        )):
            raise RuntimeError(f"Piper voice {requested!r} is not for target language {target_code}.")
        # The download tool validates available remote voices; permit a
        # custom explicitly selected model even with an offline catalog.
        return requested, voices.get(requested, {})

    prefixes = [normalized + "-"]
    if "_" not in normalized:
        prefixes.append(normalized + "_")
    candidates = [name for name in voices if any(name.startswith(p) for p in prefixes)]
    if not candidates:
        raise RuntimeError(
            f"No Piper voice found for {target_code}. Install a voice or set audio_settings.voice."
        )
    preferred = {"fr": "fr_FR-siwis-medium", "fr_FR": "fr_FR-siwis-medium"}
    favorite = preferred.get(normalized)
    if favorite in candidates:
        return favorite, voices[favorite]
    rank = {"medium": 0, "high": 1, "low": 2, "x_low": 3}
    candidates.sort(key=lambda n: (rank.get(n.rsplit("-", 1)[-1], 9), n))
    return candidates[0], voices[candidates[0]]


def synthesize_piper(
    text: str, target_code: str, output: Path, voice: str | None,
    voice_dir: Path, length_scale: float | None = None,
) -> tuple[str, dict[str, Any]]:
    selected, metadata = piper_voice(target_code, voice, voice_dir)
    voice_dir.mkdir(parents=True, exist_ok=True)
    model = voice_dir / f"{selected}.onnx"
    config = voice_dir / f"{selected}.onnx.json"
    if not (model.is_file() and config.is_file()):
        # Keep compatibility with Piper 1.8+ and its supported CLI downloader.
        command = [
            sys.executable, "-m", "piper.download_voices",
            "--data-dir", str(voice_dir), selected,
        ]
        downloaded = subprocess.run(command, capture_output=True, text=True,
                                    check=False, timeout=240)
        if downloaded.returncode != 0 or not (model.is_file() and config.is_file()):
            raise RuntimeError(
                f"Could not download Piper voice {selected}: "
                f"{downloaded.stderr.strip() or downloaded.stdout.strip()}"
            )
    output.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        sys.executable, "-m", "piper",
        "--data-dir", str(voice_dir), "-m", selected,
        "-f", str(output), "--sentence-silence", "0",
    ]
    if length_scale is not None:
        cmd += ["--length-scale", str(length_scale)]
    cmd += ["--", text]
    completed = subprocess.run(cmd, check=False, text=True, capture_output=True,
                               timeout=240)
    if completed.returncode != 0:
        raise RuntimeError(
            f"Piper failed for {selected}: {completed.stderr.strip() or completed.stdout.strip()}"
        )
    return selected, metadata

def tts_spoken_target(target: str) -> str:
    """Speak written contrasts as distinct forms, never synthesize 'slash'."""
    return re.sub(r"\s+[/×]\s+", ". ", target.strip())


def cached_piper_tts(
    text: str,
    language: str,
    requested_voice: str | None,
    media_root: Path,
    voice_dir: Path,
    cache: dict[tuple[str, str, str, str], tuple[Path, str, dict[str, Any], dict[str, Any]]],
    length_scale: float | None = None,
) -> tuple[Path, str, dict[str, Any], dict[str, Any], bool]:
    key = (language, requested_voice or "", text, str(length_scale))
    if key in cache:
        return (*cache[key], False)
    fingerprint = hashlib.sha256(
        json.dumps(key, ensure_ascii=False).encode("utf-8")
    ).hexdigest()[:20]
    output = media_root / f"anki-tts-{fingerprint}.wav"
    if length_scale is None:
        selected, metadata = synthesize_piper(text, language, output, requested_voice, voice_dir)
    else:
        selected, metadata = synthesize_piper(
            text, language, output, requested_voice, voice_dir, length_scale=length_scale
        )
    validation = validate_media_file(output, "audio")
    cache[key] = (output, selected, metadata, validation)
    return output, selected, metadata, validation, True


def piper_source_metadata(selected: str, metadata: dict[str, Any]) -> dict[str, Any]:
    license_meta = metadata.get("license") if isinstance(metadata, dict) else None
    if isinstance(license_meta, dict):
        license_text = str(license_meta.get("name") or license_meta.get("url") or "")
    else:
        license_text = str(license_meta or "")
    return {
        "kind": "tts", "provider": f"piper:{selected}",
        "source_url": "https://github.com/OHF-Voice/piper1-gpl",
        **({"license": license_text} if license_text else {}),
    }


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
    # Fail before any download, TTS generation, or clipping on malformed or
    # duplicate review tasks. The final delivery still validates actual media.
    errors = validate_plan(plan, plan_path, check_media=False)
    if errors:
        raise ValueError("Invalid card plan before enrichment:\n- " + "\n- ".join(errors))
    plan_dir = plan_path.resolve().parent
    media_root = (media_dir or (plan_dir / "media")).resolve()
    voice_dir = media_root / ".piper-voices"
    media_root.mkdir(parents=True, exist_ok=True)
    counts = {"audio_generated": 0, "audio_clipped": 0, "audio_aligned": 0, "images_downloaded": 0, "media_validated": 0, "media_skipped": 0}
    word_cache: dict[tuple[Path, str], list[tuple[str, float, float]]] = {}
    tts_cache: dict[tuple[str, str, str, str], tuple[Path, str, dict[str, Any], dict[str, Any]]] = {}
    is_auto_audio = plan.get("version") in {"2.3", "2.4"}
    chunk_first = plan.get("version") == "2.4"
    options = plan.get("audio_settings") or {}
    voice = options.get("voice") if chunk_first else None
    length_scale = float(options.get("length_scale", 0.93)) if chunk_first else None
    include_source = not chunk_first or bool(options.get("include_source_audio", False))
    counts["audio_warnings"] = []
    counts["source_audio_generated"] = 0

    if is_auto_audio and not chunk_first:
        # Legacy v2.3 synthesizes original context first, unchanged.
        for unit in plan.get("source_units", []):
            if unit.get("audio"):
                original = resolve_path(plan_dir, str(unit["audio"]))
                unit.setdefault("media_validation", {})["audio"] = validate_media_file(original, "audio")
                counts["media_validated"] += 1
                continue
            try:
                output, selected, metadata, validation, created = cached_piper_tts(
                    str(unit["text"]), str(plan["target_language"]["code"]), None,
                    media_root, voice_dir, tts_cache,
                )
            except Exception as exc:
                raise RuntimeError(
                    f"Could not generate mandatory source audio for {unit['id']}: {exc}"
                ) from exc
            unit["audio"] = relative_to_plan(output, plan_dir)
            unit["audio_provenance"] = piper_source_metadata(selected, metadata)
            unit["media_validation"] = {"audio": validation}
            counts["audio_generated"] += int(created)
            counts["media_validated"] += 1

    for card in plan.get("cards", []):
        card_validation = dict(card.get("media_validation") or {})
        media_issues = list(card.get("media_issues") or [])

        selected_audio = [name for name in ("audio", "audio_clip", "audio_request") if card.get(name)]
        if len(selected_audio) > 1:
            raise ValueError(
                f"Card {card['id']} has conflicting audio sources: {selected_audio}. "
                "Choose audio, audio_clip, or audio_request."
            )
        if is_auto_audio and not selected_audio:
            card["audio_request"] = {
                "mode": "auto", "provider": "piper",
                "text": tts_spoken_target(str(card["target_text"])),
                **({"voice": voice} if voice else {}),
                "required": True,
            }

        if card.get("audio_clip"):
            request = card["audio_clip"]
            source = resolve_path(plan_dir, str(request["source"]))
            identity = "\x1f".join([
                str(card["id"]), str(source), str(card["target_text"]),
                str(request.get("start_seconds", "")), str(request.get("end_seconds", "")),
            ])
            digest = hashlib.sha256(identity.encode("utf-8")).hexdigest()[:12]
            output = media_root / f"{safe_id(str(card['id']))[:55]}-{digest}-clip.wav"
            if output.resolve() == source.resolve():
                raise ValueError(f"Clip destination would overwrite its source: {source}")
            try:
                result = clip_audio(
                    source,
                    output,
                    target_text=str(card["target_text"]),
                    language=str(plan["target_language"]["code"]),
                    start_seconds=request.get("start_seconds"),
                    end_seconds=request.get("end_seconds"),
                    word_cache=word_cache,
                    strict_boundaries=plan.get("version") in {"2.2", "2.3", "2.4"},
                )
            except Exception as exc:
                raise RuntimeError(
                    f"Could not align/clip original audio for card {card['id']}: {exc}"
                ) from exc
            card["audio"] = relative_to_plan(output, plan_dir)
            # The resolved recording is the clipped target, not the original
            # long source. Do not retain the pre-clip transcript as if it were
            # the transcript of this new audio file.
            card["audio_transcript"] = str(card["target_text"])
            card["audio_provenance"] = {
                "kind": "user-supplied",
                "provider": "ffmpeg-clip",
                "source_path": relative_to_plan(source, plan_dir),
                "start_seconds": result["start_seconds"],
                "end_seconds": result["end_seconds"],
                "alignment": result["alignment"],
            }
            card.pop("audio_clip")
            card_validation["audio"] = result["validation"]
            counts["audio_clipped"] += 1
            if result["alignment"] == "asr-exact":
                counts["audio_aligned"] += 1
            counts["media_validated"] += 1
        elif card.get("audio"):
            path = resolve_path(plan_dir, str(card["audio"]))
            card_validation["audio"] = validate_media_file(path, "audio")
            counts["media_validated"] += 1
        elif card.get("audio_request"):
            request = card["audio_request"]
            provider = request.get("provider", "auto")
            mode = normalize_mode(card)
            audio_required = bool(request.get("required")) or card.get("skill") == "listening" or (
                card.get("skill") == "pronunciation" and mode in AUDIO_REQUIRED_PRONUNCIATION_MODES
            )
            try:
                if provider not in {"auto", "piper"}:
                    raise RuntimeError(f"Unsupported audio provider: {provider}")
                if is_auto_audio:
                    output, selected, metadata, validation, created = cached_piper_tts(
                        str(request["text"]), str(plan["target_language"]["code"]),
                        request.get("voice") or voice, media_root, voice_dir, tts_cache,
                        length_scale=length_scale,
                    )
                else:
                    identity = json.dumps(
                        {"id": card["id"], "request": request}, sort_keys=True, ensure_ascii=False
                    )
                    digest = hashlib.sha256(identity.encode("utf-8")).hexdigest()[:12]
                    output = media_root / f"{safe_id(str(card['id']))[:55]}-{digest}-audio.wav"
                    selected, metadata = synthesize_piper(
                        str(request["text"]),
                        str(plan["target_language"]["code"]), output,
                        request.get("voice"), voice_dir,
                    )
                    validation = validate_media_file(output, "audio")
                    created = True
                card["audio"] = relative_to_plan(output, plan_dir)
                card["audio_transcript"] = str(request["text"])
                card.pop("audio_request", None)  # resolved plan has one audio source
                card["audio_provenance"] = piper_source_metadata(selected, metadata)
                card_validation["audio"] = validation
                counts["audio_generated"] += int(created)
                counts["media_validated"] += 1
                if chunk_first:
                    seconds = float(validation.get("duration_seconds") or 0)
                    words = max(1, len(str(request["text"]).split()))
                    if seconds > 0.85 * words + 1.15:
                        counts["audio_warnings"].append({
                            "card": str(card["id"]), "seconds": seconds,
                            "words": words, "reason": "Lengthy for a focused chunk; listen and consider another Piper voice."
                        })
            except Exception as exc:
                if audio_required:
                    raise RuntimeError(f"Required audio could not be generated for card {card['id']}: {exc}") from exc
                media_issues.append({"kind": "audio", "provider": str(provider), "error": str(exc)})
                counts["media_skipped"] += 1

        if card.get("image"):
            path = resolve_path(plan_dir, str(card["image"]))
            card_validation["image"] = validate_media_file(path, "image")
            counts["media_validated"] += 1
        elif card.get("image_request"):
            request = card["image_request"]
            licenses = [str(x).casefold() for x in (request.get("licenses") or DEFAULT_IMAGE_LICENSES)]
            provider = str(request.get("provider", "auto"))
            try:
                identity = json.dumps(
                    {"id": card["id"], "request": request}, sort_keys=True, ensure_ascii=False
                )
                digest = hashlib.sha256(identity.encode("utf-8")).hexdigest()[:12]
                output = media_root / f"{safe_id(str(card['id']))[:55]}-{digest}-image.webp"
                result = fetch_image(
                    str(request["query"]),
                    provider,
                    licenses,
                    output,
                )
                card["image"] = relative_to_plan(output, plan_dir)
                card.pop("image_request", None)  # resolved plan has one image source
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
            except Exception as exc:
                if bool(request.get("required")):
                    raise RuntimeError(f"Required image could not be resolved for card {card['id']}: {exc}") from exc
                media_issues.append({"kind": "image", "provider": provider, "error": str(exc)})
                counts["media_skipped"] += 1

        if card_validation:
            card["media_validation"] = card_validation
        if media_issues:
            card["media_issues"] = media_issues

    if chunk_first and include_source:
        # Context is opt-in. Target clips have already been chosen/synthesized.
        for unit in plan.get("source_units", []):
            if unit.get("audio"):
                existing = resolve_path(plan_dir, str(unit["audio"]))
                unit.setdefault("media_validation", {})["audio"] = validate_media_file(existing, "audio")
                continue
            try:
                output, selected, metadata, validation, created = cached_piper_tts(
                    str(unit["text"]), str(plan["target_language"]["code"]),
                    voice, media_root, voice_dir, tts_cache, length_scale=length_scale,
                )
            except Exception as exc:
                raise RuntimeError(
                    f"Could not generate optional requested source audio for {unit['id']}: {exc}"
                ) from exc
            unit["audio"] = relative_to_plan(output, plan_dir)
            unit["audio_provenance"] = piper_source_metadata(selected, metadata)
            unit["media_validation"] = {"audio": validation}
            counts["audio_generated"] += int(created)
            counts["source_audio_generated"] += int(created)
            counts["media_validated"] += 1

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
