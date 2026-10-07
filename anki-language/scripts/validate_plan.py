#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

AUDIO_FRONT_MODES = {"minimal-pair", "sound-discrimination", "audio-to-spelling"}


def load_plan(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError("Plan root must be a JSON object.")
    return data


def schema_errors(plan: dict[str, Any]) -> list[str]:
    schema_path = Path(__file__).resolve().parents[1] / "schemas" / "card-plan.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    errors: list[str] = []
    for error in sorted(validator.iter_errors(plan), key=lambda item: list(item.absolute_path)):
        path = "$"
        for part in error.absolute_path:
            path += f"[{part}]" if isinstance(part, int) else f".{part}"
        errors.append(f"{path}: {error.message}")
    return errors


def validate_plan(plan: dict[str, Any], plan_path: Path, check_media: bool = True) -> list[str]:
    errors = schema_errors(plan)
    if errors:
        return errors

    support = plan["support_language"]
    support_name = str(support["name"]).strip().lower()
    support_code = str(support["code"]).strip().lower()
    is_english = support_name == "english" or support_code == "en" or support_code.startswith("en-")
    if not is_english and not bool(plan.get("support_language_override")):
        errors.append(
            "Support language must be English unless support_language_override=true "
            "because the user explicitly requested another support language."
        )

    seen_ids: set[str] = set()
    media_by_basename: dict[str, Path] = {}
    plan_dir = plan_path.resolve().parent

    for index, card in enumerate(plan["cards"]):
        prefix = f"cards[{index}]"
        card_id = str(card["id"]).strip()
        if card_id in seen_ids:
            errors.append(f"Duplicate card id: {card_id}")
        else:
            seen_ids.add(card_id)

        skill = card["skill"]
        if skill == "production" and not str(card.get("prompt", "")).strip():
            errors.append(f"{prefix}.prompt is required for production cards.")
        if skill == "listening" and not str(card.get("audio", "")).strip():
            errors.append(f"{prefix}.audio is required for listening cards.")

        mode = str(card.get("mode", "standard")).strip().lower()
        if skill == "pronunciation" and mode in AUDIO_FRONT_MODES and not str(card.get("audio", "")).strip():
            errors.append(f"{prefix}.audio is required for pronunciation mode '{mode}'.")

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
            if check_media and not media_path.is_file():
                errors.append(f"Missing {media_key} file for {prefix}: {media_path}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an anki-language card plan.")
    parser.add_argument("plan", type=Path)
    parser.add_argument("--allow-missing-media", action="store_true", help="Validate structure without requiring referenced media files to exist.")
    args = parser.parse_args()
    try:
        plan = load_plan(args.plan)
        errors = validate_plan(plan, args.plan, check_media=not args.allow_missing_media)
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