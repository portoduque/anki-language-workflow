#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import unicodedata
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from card_contract import AUDIO_REQUIRED_PRONUNCIATION_MODES, SUPPORTED_MODES_BY_SKILL, normalize_mode, writing_parts
from media_validate import MediaValidationError, validate_media_file

CONFIG_FILENAME = "anki-language.config.json"


def load_json_object(path: Path, label: str) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{label} root must be a JSON object.")
    return data


def load_plan(path: Path) -> dict[str, Any]:
    return load_json_object(path, "Plan")


def schema_errors(data: dict[str, Any], schema_name: str, label: str) -> list[str]:
    schema_path = Path(__file__).resolve().parents[1] / "schemas" / schema_name
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    errors: list[str] = []
    for error in sorted(validator.iter_errors(data), key=lambda item: list(item.absolute_path)):
        path = "$"
        for part in error.absolute_path:
            path += f"[{part}]" if isinstance(part, int) else f".{part}"
        errors.append(f"{label} {path}: {error.message}")
    return errors


def discover_config(plan_path: Path, explicit: Path | None = None) -> Path | None:
    if explicit is not None:
        return explicit.resolve()
    candidates = [Path.cwd() / CONFIG_FILENAME, plan_path.resolve().parent / CONFIG_FILENAME]
    seen: set[Path] = set()
    for candidate in candidates:
        resolved = candidate.resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        if resolved.is_file():
            return resolved
    return None


def validate_language_config(plan: dict[str, Any], config_path: Path) -> list[str]:
    try:
        config = load_json_object(config_path, "Configuration")
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        return [f"Invalid workspace configuration: {exc}"]
    errors = schema_errors(config, "config.schema.json", "Config")
    if errors:
        return errors
    for key in ("target_language", "base_language"):
        plan_lang = plan[key]
        config_lang = config[key]
        if str(plan_lang["code"]).casefold() != str(config_lang["code"]).casefold() or str(plan_lang["name"]).casefold() != str(config_lang["name"]).casefold():
            errors.append(
                f"Plan {key} ({plan_lang['name']} / {plan_lang['code']}) does not match "
                f"workspace configuration ({config_lang['name']} / {config_lang['code']})."
            )
    return errors


def normalized_utterance(value: str) -> str:
    """Compare transcript/target wording without punctuation or whitespace noise."""
    folded = unicodedata.normalize("NFKC", value).casefold()
    return " ".join(re.findall(r"[^\W_]+", folded, flags=re.UNICODE))


def retrieval_signature(card: dict[str, Any]) -> tuple[str, ...]:
    """Catch identical review tasks regardless of ids, tags, notes, or source.

    Intentionally do not compare across skills: recognition, listening, and
    production can be independent retrieval operations. This is not an AI
    similarity score and must not discard legitimate semantic variations.
    """
    skill = str(card["skill"])
    mode = normalize_mode(card)
    def norm(key: str) -> str:
        return " ".join(unicodedata.normalize("NFKC", str(card.get(key, ""))).casefold().split())

    signature = [skill, mode, norm("target_text"), norm("prompt")]
    if skill == "writing":
        signature.append(norm("writing_answer"))
    elif skill == "production":
        signature.extend([norm("hint"), norm("image")])
    elif skill in {"listening", "pronunciation"}:
        clip = card.get("audio_clip")
        signature.extend([
            norm("audio"),
            json.dumps(clip, sort_keys=True, ensure_ascii=False) if clip else "",
            json.dumps(card.get("audio_request"), sort_keys=True, ensure_ascii=False)
            if card.get("audio_request") else "",
        ])
    return tuple(signature)


def validate_plan(
    plan: dict[str, Any],
    plan_path: Path,
    check_media: bool = True,
    config_path: Path | None = None,
) -> list[str]:
    errors = schema_errors(plan, "card-plan.schema.json", "Plan")
    if errors:
        return errors

    resolved_config = discover_config(plan_path, config_path)
    if resolved_config is not None:
        errors.extend(validate_language_config(plan, resolved_config))

    seen_ids: set[str] = set()
    seen_retrievals: dict[tuple[str, ...], tuple[int, str]] = {}
    media_by_basename: dict[str, Path] = {}
    audio_uses: dict[Path, list[tuple[int, str, str]]] = {}
    plan_dir = plan_path.resolve().parent

    for index, card in enumerate(plan["cards"]):
        prefix = f"cards[{index}]"
        card_id = str(card["id"]).strip()
        if card_id in seen_ids:
            errors.append(f"Duplicate card id: {card_id}")
        else:
            seen_ids.add(card_id)

        signature = retrieval_signature(card)
        previous = seen_retrievals.get(signature)
        if previous is not None:
            previous_index, previous_id = previous
            errors.append(
                f"{prefix}: duplicate retrieval task of cards[{previous_index}] "
                f"(id={previous_id!r}); differing ids, tags, notes, or sources "
                "do not make a new learning target."
            )
        else:
            seen_retrievals[signature] = (index, card_id)

        skill = card["skill"]
        mode = normalize_mode(card)
        allowed_modes = SUPPORTED_MODES_BY_SKILL[skill]
        if mode not in allowed_modes:
            errors.append(
                f"{prefix}.mode '{mode}' is not supported for skill '{skill}'. "
                f"Allowed: {sorted(allowed_modes)}"
            )
        if skill == "production" and not str(card.get("prompt", "")).strip():
            errors.append(f"{prefix}.prompt is required for production cards.")
        if skill == "writing":
            if not str(card.get("prompt", "")).strip():
                errors.append(f"{prefix}.prompt is required for Writing to constrain the typed answer.")
            try:
                writing_parts(card)
            except ValueError as exc:
                errors.append(f"{prefix}.writing_answer: {exc}")
        elif card.get("writing_answer") is not None:
            errors.append(f"{prefix}.writing_answer is only supported for Writing cards.")
        request = card.get("audio_request")
        if request and (mode == "standard" or (skill == "pronunciation" and mode == "spelling-sound")):
            requested_text = normalized_utterance(str(request["text"]))
            target_text = normalized_utterance(str(card["target_text"]))
            if requested_text != target_text:
                errors.append(
                    f"{prefix}.audio_request.text must match target_text for this mode; "
                    "TTS must not teach different spoken words than the card answer."
                )
        clip = card.get("audio_clip")
        audio_sources = [key for key in ("audio", "audio_clip", "audio_request") if card.get(key)]
        if len(audio_sources) > 1:
            errors.append(
                f"{prefix}: choose only one audio source: audio, audio_clip, or audio_request."
            )
        if card.get("image") and card.get("image_request"):
            errors.append(f"{prefix}: choose only one image source: image or image_request.")
        if clip and check_media:
            errors.append(f"{prefix}.audio_clip must be resolved before delivery.")
        if skill == "listening" and not str(card.get("audio", "")).strip():
            if check_media or not (card.get("audio_request") or clip):
                errors.append(f"{prefix}.audio is required for listening cards after media enrichment.")
        if skill == "pronunciation" and not str(card.get("prompt", "")).strip():
            errors.append(f"{prefix}.prompt is required for pronunciation cards so the builder never invents a base-language instruction.")
        if skill == "pronunciation" and mode in AUDIO_REQUIRED_PRONUNCIATION_MODES and not str(card.get("audio", "")).strip():
            if check_media or not (card.get("audio_request") or clip):
                errors.append(f"{prefix}.audio is required for pronunciation mode '{mode}' after media enrichment.")

        raw_audio = card.get("audio")
        if raw_audio:
            path = Path(str(raw_audio))
            resolved_audio = (path if path.is_absolute() else plan_dir / path).resolve()
            target = normalized_utterance(str(card.get("target_text", "")))
            transcript = normalized_utterance(str(card.get("audio_transcript", "")))
            audio_uses.setdefault(resolved_audio, []).append((index, target, transcript))
            if transcript and target and f" {target} " not in f" {transcript} ":
                errors.append(
                    f"{prefix}.audio_transcript does not contain the target wording; "
                    "use a matching clip, adjust the target, or omit the audio."
                )

        for media_key in ("audio", "image"):
            raw = card.get(media_key)
            if not raw:
                continue
            media_path = Path(str(raw))
            if not media_path.is_absolute():
                media_path = (plan_dir / media_path).resolve()
            basename = media_path.name
            previous = media_by_basename.get(basename)
            if previous is not None and previous != media_path:
                errors.append(f"Media basename collision for '{basename}': '{previous}' and '{media_path}'.")
            else:
                media_by_basename[basename] = media_path
            if check_media:
                if not media_path.is_file():
                    errors.append(f"Missing {media_key} file for {prefix}: {media_path}")
                    continue
                try:
                    current = validate_media_file(media_path, media_key)
                except MediaValidationError as exc:
                    errors.append(f"Invalid {media_key} for {prefix}: {exc}")
                    continue
                recorded = (card.get("media_validation") or {}).get(media_key)
                if recorded and recorded.get("sha256") and recorded["sha256"] != current["sha256"]:
                    errors.append(
                        f"{prefix}.{media_key} changed after validation: "
                        f"recorded sha256={recorded['sha256']} current sha256={current['sha256']}"
                    )

    for path, uses in audio_uses.items():
        if len({target for _, target, _ in uses}) <= 1:
            continue
        transcripts = {transcript for _, _, transcript in uses if transcript}
        for index, _, transcript in uses:
            if not transcript:
                errors.append(
                    f"cards[{index}].audio_transcript is required because audio "
                    f"'{path.name}' is reused for different target texts. "
                    "Verify the recording transcript before reusing it."
                )
        if len(transcripts) > 1:
            errors.append(
                f"Audio '{path.name}' has inconsistent transcripts across reused cards."
            )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an anki-language card plan.")
    parser.add_argument("plan", type=Path)
    parser.add_argument("--config", type=Path, help="Explicit workspace language configuration. Auto-discovered when omitted.")
    parser.add_argument("--allow-missing-media", action="store_true", help="Validate structure without requiring referenced media files to exist.")
    args = parser.parse_args()
    try:
        plan = load_plan(args.plan)
        errors = validate_plan(plan, args.plan, check_media=not args.allow_missing_media, config_path=args.config)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"ERROR: {exc}")
        return 2
    if errors:
        print("Plan validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"Plan valid: {len(plan['cards'])} card(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())