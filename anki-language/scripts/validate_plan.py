#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

VALID_SKILLS = {"reading", "listening", "production", "pronunciation"}
AUDIO_FRONT_MODES = {"minimal-pair", "sound-discrimination", "audio-to-spelling"}


def load_plan(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError("Plan root must be a JSON object.")
    return data


def validate_plan(plan: dict[str, Any], plan_path: Path, check_media: bool = True) -> list[str]:
    errors: list[str] = []

    for key in ("version", "target_language", "support_language", "deck_name", "cards"):
        if key not in plan:
            errors.append(f"Missing required field: {key}")

    if plan.get("version") != "1.0":
        errors.append("version must be '1.0'.")

    for language_key in ("target_language", "support_language"):
        value = plan.get(language_key)
        if not isinstance(value, dict):
            errors.append(f"{language_key} must be an object.")
            continue
        if not str(value.get("name", "")).strip():
            errors.append(f"{language_key}.name is required.")
        if len(str(value.get("code", "")).strip()) < 2:
            errors.append(f"{language_key}.code must contain a language code.")

    support = plan.get("support_language") or {}
    support_name = str(support.get("name", "")).strip().lower()
    support_code = str(support.get("code", "")).strip().lower()
    is_english = support_name == "english" or support_code == "en" or support_code.startswith("en-")
    if not is_english and not bool(plan.get("support_language_override")):
        errors.append(
            "Support language must be English unless support_language_override=true "
            "because the user explicitly requested another support language."
        )

    if not str(plan.get("deck_name", "")).strip():
        errors.append("deck_name must be a non-empty string.")

    cards = plan.get("cards")
    if not isinstance(cards, list):
        errors.append("cards must be an array.")
        return errors

    seen_ids: set[str] = set()
    media_by_basename: dict[str, Path] = {}
    plan_dir = plan_path.resolve().parent

    for index, card in enumerate(cards):
        prefix = f"cards[{index}]"
        if not isinstance(card, dict):
            errors.append(f"{prefix} must be an object.")
            continue

        card_id = str(card.get("id", "")).strip()
        if not card_id:
            errors.append(f"{prefix}.id is required.")
        elif card_id in seen_ids:
            errors.append(f"Duplicate card id: {card_id}")
        else:
            seen_ids.add(card_id)

        skill = card.get("skill")
        if skill not in VALID_SKILLS:
            errors.append(f"{prefix}.skill must be one of {sorted(VALID_SKILLS)}.")

        if not str(card.get("target_text", "")).strip():
            errors.append(f"{prefix}.target_text is required.")

        if skill == "production" and not str(card.get("prompt", "")).strip():
            errors.append(f"{prefix}.prompt is required for production cards.")

        if skill == "listening" and not str(card.get("audio", "")).strip():
            errors.append(f"{prefix}.audio is required for listening cards.")

        mode = str(card.get("mode", "standard")).strip().lower()
        if skill == "pronunciation" and mode in AUDIO_FRONT_MODES and not str(card.get("audio", "")).strip():
            errors.append(f"{prefix}.audio is required for pronunciation mode '{mode}'.")

        tags = card.get("tags", [])
        if tags is not None and (not isinstance(tags, list) or any(not str(t).strip() for t in tags)):
            errors.append(f"{prefix}.tags must be an array of non-empty strings.")

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
                errors.append(
                    f"Media basename collision for '{basename}': '{previous}' and '{media_path}'."
                )
            else:
                media_by_basename[basename] = media_path
            if check_media and not media_path.is_file():
                errors.append(f"Missing {media_key} file for {prefix}: {media_path}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an anki-language card plan.")
    parser.add_argument("plan", type=Path)
    parser.add_argument(
        "--allow-missing-media",
        action="store_true",
        help="Validate structure without requiring referenced media files to exist.",
    )
    args = parser.parse_args()

    try:
        plan = load_plan(args.plan)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"ERROR: {exc}")
        return 2

    errors = validate_plan(plan, args.plan, check_media=not args.allow_missing_media)
    if errors:
        print("Plan validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Plan valid: {len(plan.get('cards', []))} card(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
