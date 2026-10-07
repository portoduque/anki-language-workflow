#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import json
import re
from pathlib import Path

REQUIRED_MODULES = {"genanki": "genanki", "jsonschema": "jsonschema", "yaml": "PyYAML"}


def check_dependencies() -> list[str]:
    return [package for module, package in REQUIRED_MODULES.items() if importlib.util.find_spec(module) is None]


def default_output(plan: dict, plan_path: Path) -> Path:
    raw = str(plan.get("deck_name") or "language").strip()
    safe = re.sub(r"[^A-Za-z0-9._-]+", "-", raw).strip("-") or "language"
    return plan_path.resolve().parent / f"{safe}.apkg"


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a plan, build its APKG, then deeply validate the package.")
    parser.add_argument("plan", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--config", type=Path, help="Explicit workspace language configuration. Auto-discovered when omitted.")
    args = parser.parse_args()

    missing = check_dependencies()
    if missing:
        requirements = Path(__file__).resolve().parents[1] / "requirements.txt"
        print("ERROR: missing Python dependencies: " + ", ".join(sorted(missing)))
        print(f"Install them with: python -m pip install -r {requirements}")
        return 2

    from build_apkg import build
    from validate_apkg import expectations_from_plan, validate_apkg
    from validate_plan import load_plan, validate_plan

    try:
        plan = load_plan(args.plan)
        errors = validate_plan(plan, args.plan, check_media=True, config_path=args.config)
        if errors:
            print("Plan validation failed:")
            for error in errors:
                print(f"- {error}")
            return 1

        output = args.output or default_output(plan, args.plan)
        report = build(args.plan, output)
        expected_media, expected_count, expected_decks, expected_tags = expectations_from_plan(args.plan)
        package_errors, package_summary = validate_apkg(
            output,
            expected_media=expected_media,
            expected_card_count=expected_count,
            expected_decks=expected_decks,
            expected_tags=expected_tags,
        )
        if package_errors:
            print("APKG validation failed:")
            for error in package_errors:
                print(f"- {error}")
            return 1

        print(json.dumps({
            "status": "ok",
            "output": str(output.resolve()),
            "report": report,
            "validation": package_summary,
        }, ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())