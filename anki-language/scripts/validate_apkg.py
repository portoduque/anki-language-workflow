#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import sqlite3
import tempfile
import zipfile
from pathlib import Path

from card_contract import SKILL_META, WORKFLOW_TAG, workflow_tag


def inspect_collection(archive: zipfile.ZipFile, collection_name: str) -> tuple[list[str], dict]:
    errors: list[str] = []
    with tempfile.TemporaryDirectory(prefix="anki-language-") as tmp:
        extracted = Path(archive.extract(collection_name, path=tmp))
        connection = None
        try:
            connection = sqlite3.connect(extracted)
            note_count = int(connection.execute("SELECT COUNT(*) FROM notes").fetchone()[0])
            card_count = int(connection.execute("SELECT COUNT(*) FROM cards").fetchone()[0])
            tag_rows = connection.execute("SELECT tags FROM notes").fetchall()
            all_tags = sorted({
                tag
                for row in tag_rows
                for tag in str(row[0] or "").split()
                if tag
            })
            row = connection.execute("SELECT decks FROM col LIMIT 1").fetchone()
            decks = json.loads(row[0] if row else "{}")
            deck_names = sorted(
                value.get("name", "")
                for value in decks.values()
                if isinstance(value, dict) and value.get("name")
            )
        except (sqlite3.DatabaseError, json.JSONDecodeError, TypeError) as exc:
            errors.append(f"Invalid Anki collection database: {exc}")
            return errors, {}
        finally:
            if connection is not None:
                connection.close()
    return errors, {
        "note_count": note_count,
        "card_count": card_count,
        "deck_names": deck_names,
        "all_tags": all_tags,
    }


def validate_apkg(
    path: Path,
    expected_media: set[str] | None = None,
    expected_card_count: int | None = None,
    expected_decks: set[str] | None = None,
    expected_tags: set[str] | None = None,
    expected_media_hashes: dict[str, str] | None = None,
) -> tuple[list[str], dict]:
    errors: list[str] = []
    summary: dict = {"path": str(path.resolve())}
    if not path.is_file():
        return [f"APKG not found: {path}"], summary
    if not zipfile.is_zipfile(path):
        return [f"Not a valid ZIP/APKG file: {path}"], summary

    with zipfile.ZipFile(path, "r") as archive:
        names = set(archive.namelist())
        collection_files = sorted(name for name in names if name.startswith("collection.anki"))
        collection_summary = {}
        if not collection_files:
            errors.append("Missing Anki collection database inside APKG.")
        else:
            collection_errors, collection_summary = inspect_collection(archive, collection_files[0])
            errors.extend(collection_errors)

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
            payload_name
            for payload_name in (media_map.keys() if isinstance(media_map, dict) else [])
            if payload_name not in names
        ]
        if missing_payloads:
            errors.append(f"Media manifest references missing ZIP entries: {missing_payloads}")

        if expected_media is not None:
            missing_expected = sorted(expected_media - set(media_names))
            if missing_expected:
                errors.append(f"Expected media missing from APKG: {missing_expected}")
        if expected_media_hashes is not None:
            if set(expected_media_hashes) != set(media_names):
                errors.append(
                    "APKG media manifest differs from resolved plan: "
                    f"missing={sorted(set(expected_media_hashes) - set(media_names))}, "
                    f"unexpected={sorted(set(media_names) - set(expected_media_hashes))}."
                )
            for index, name in media_map.items():
                if name not in expected_media_hashes or index not in names:
                    continue
                expected = expected_media_hashes[name]
                actual = hashlib.sha256(archive.read(index)).hexdigest()
                if actual != expected:
                    errors.append(f"APKG media content differs from resolved plan: {name}.")


        if expected_card_count is not None and collection_summary:
            if collection_summary.get("card_count") != expected_card_count:
                errors.append(
                    f"APKG card count mismatch: expected {expected_card_count}, "
                    f"got {collection_summary.get('card_count')}."
                )
            if collection_summary.get("note_count") != expected_card_count:
                errors.append(
                    f"APKG note count mismatch: expected {expected_card_count}, "
                    f"got {collection_summary.get('note_count')}."
                )

        if expected_decks is not None and collection_summary:
            actual_decks = set(collection_summary.get("deck_names", []))
            missing_decks = sorted(expected_decks - actual_decks)
            if missing_decks:
                errors.append(f"Expected decks missing from APKG: {missing_decks}")

        if expected_tags is not None and collection_summary:
            actual_tags = set(collection_summary.get("all_tags", []))
            missing_tags = sorted(expected_tags - actual_tags)
            if missing_tags:
                errors.append(f"Expected workflow tags missing from APKG: {missing_tags}")

        summary.update({
            "collection_files": collection_files,
            "media_total": len(media_names),
            "zip_entries": len(names),
            **collection_summary,
        })

    return errors, summary



def media_hashes_from_plan(plan: dict) -> dict[str, str]:
    """Media identities in the resolved plan, prior to packaging."""
    output: dict[str, str] = {}
    for card in plan["cards"]:
        for key in ("audio", "image"):
            raw = card.get(key)
            if not raw:
                continue
            fingerprint = ((card.get("media_validation") or {}).get(key) or {}).get("sha256")
            if not fingerprint:
                raise ValueError(f"Resolved card {card['id']} lacks {key} sha256.")
            name = Path(raw).name
            if name in output and output[name] != fingerprint:
                raise ValueError(f"Media filename collision in plan: {name}.")
            output[name] = fingerprint
    if plan.get("audio_settings", {}).get("include_source_audio", False):
        for unit in plan.get("source_units", []):
            if not unit.get("audio") or not unit.get("card_ids"):
                continue
            name = Path(unit["audio"]).name
            fingerprint = ((unit.get("media_validation") or {}).get("audio") or {}).get("sha256")
            if not fingerprint:
                raise ValueError(f"Source audio {unit['id']} lacks checksum.")
            if name in output and output[name] != fingerprint:
                raise ValueError(f"Source audio filename collision: {name}.")
            output[name] = fingerprint
    return output


def expectations_from_plan(plan_path: Path) -> tuple[set[str], int, set[str], set[str]]:
    data = json.loads(plan_path.read_text(encoding="utf-8"))
    expected_media: set[str] = set()
    expected_decks: set[str] = set()
    expected_tags: set[str] = {WORKFLOW_TAG}
    deck_name = str(data.get("deck_name", "")).strip()
    target_code = str((data.get("target_language") or {}).get("code", "")).strip()
    cards = data.get("cards", [])
    for card in cards:
        for key in ("audio", "image"):
            raw = card.get(key)
            if raw:
                expected_media.add(Path(raw).name)
        skill_meta = SKILL_META.get(card.get("skill"))
        if deck_name and skill_meta:
            expected_decks.add(f"{deck_name}::{skill_meta[0]}")
        if deck_name and target_code and card.get("id") is not None:
            expected_tags.add(workflow_tag(deck_name, target_code, str(card["skill"]), str(card["id"])))
    return expected_media, len(cards), expected_decks, expected_tags


def main() -> int:
    parser = argparse.ArgumentParser(description="Deeply validate a generated Anki APKG.")
    parser.add_argument("apkg", type=Path)
    parser.add_argument("--plan", type=Path, help="Optional card plan for expected media/count/decks.")
    args = parser.parse_args()
    try:
        if args.plan:
            expected_media, expected_count, expected_decks, expected_tags = expectations_from_plan(args.plan)
        else:
            expected_media = expected_count = expected_decks = expected_tags = None
        errors, summary = validate_apkg(
            args.apkg,
            expected_media=expected_media,
            expected_card_count=expected_count,
            expected_decks=expected_decks,
            expected_tags=expected_tags,
            expected_media_hashes=media_hashes_from_plan(
                json.loads(args.plan.read_text(encoding="utf-8"))
            ) if args.plan and json.loads(args.plan.read_text(encoding="utf-8")).get("version") == "2.8" else None,
        )
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