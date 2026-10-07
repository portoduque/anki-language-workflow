#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import zipfile
from pathlib import Path


def validate_apkg(path: Path, expected_media: set[str] | None = None) -> tuple[list[str], dict]:
    errors: list[str] = []
    summary: dict = {"path": str(path.resolve())}

    if not path.is_file():
        return [f"APKG not found: {path}"], summary
    if not zipfile.is_zipfile(path):
        return [f"Not a valid ZIP/APKG file: {path}"], summary

    with zipfile.ZipFile(path, "r") as archive:
        names = set(archive.namelist())
        collection_files = sorted(name for name in names if name.startswith("collection.anki"))
        if not collection_files:
            errors.append("Missing Anki collection database inside APKG.")
        if "media" not in names:
            errors.append("Missing media manifest inside APKG.")
            media_map = {}
        else:
            try:
                media_map = json.loads(archive.read("media").decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                errors.append(f"Invalid media manifest: {exc}")
                media_map = {}

        media_names = list(media_map.values()) if isinstance(media_map, dict) else []
        if len(media_names) != len(set(media_names)):
            errors.append("Duplicate media filenames found in APKG manifest.")

        missing_payloads = [
            payload_name for payload_name in (media_map.keys() if isinstance(media_map, dict) else [])
            if payload_name not in names
        ]
        if missing_payloads:
            errors.append(f"Media manifest references missing ZIP entries: {missing_payloads}")

        if expected_media is not None:
            packaged = set(media_names)
            missing_expected = sorted(expected_media - packaged)
            if missing_expected:
                errors.append(f"Expected media missing from APKG: {missing_expected}")

        summary.update({
            "collection_files": collection_files,
            "media_total": len(media_names),
            "zip_entries": len(names),
        })

    return errors, summary


def expected_media_from_plan(plan_path: Path) -> set[str]:
    data = json.loads(plan_path.read_text(encoding="utf-8"))
    expected: set[str] = set()
    for card in data.get("cards", []):
        for key in ("audio", "image"):
            raw = card.get(key)
            if raw:
                expected.add(Path(raw).name)
    return expected


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a generated Anki APKG.")
    parser.add_argument("apkg", type=Path)
    parser.add_argument("--plan", type=Path, help="Optional card plan to verify expected media.")
    args = parser.parse_args()

    try:
        expected = expected_media_from_plan(args.plan) if args.plan else None
        errors, summary = validate_apkg(args.apkg, expected)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}")
        return 2

    if errors:
        print("APKG validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
