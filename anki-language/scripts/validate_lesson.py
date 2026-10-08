#!/usr/bin/env python3
"""Independent pre-card teacher audit. Run this before authoring card-plan.json.

Structural checks can verify a selection trail, but cannot determine if a
French sentence is idiomatic or prove when a human/AI made a decision.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


SCHEMA_PATH = Path(__file__).resolve().parents[1] / "schemas" / "lesson-analysis.schema.json"


def load_analysis(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Lesson analysis must be a JSON object.")
    return data


def matches(text: str, term: str) -> bool:
    """Orthographic whole-form match, allowing elided French clitics."""
    import re
    import unicodedata

    haystack = unicodedata.normalize("NFKC", text).casefold().replace("’", "'")
    needle = unicodedata.normalize("NFKC", term).casefold().replace("’", "'").strip()
    return bool(needle and re.search(
        r"(?<!\w)" + re.escape(needle) + r"(?![\w'])", haystack
    ))


def validate_analysis(data: dict[str, Any]) -> list[str]:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    failures = sorted(Draft202012Validator(schema).iter_errors(data),
                      key=lambda error: str(error.absolute_path))
    if failures:
        return ["Lesson " + ".".join(map(str, error.absolute_path)) + ": " + error.message
                for error in failures]
    errors: list[str] = []
    sources: set[str] = set()
    for index, item in enumerate(data["source_assessments"]):
        sid = item["source_unit_id"]
        if sid in sources:
            errors.append(f"source_assessments[{index}]: duplicate source_unit_id {sid!r}.")
        sources.add(sid)

    ids: set[str] = set()
    taught_sources: set[str] = set()
    selected = 0
    for index, point in enumerate(data["learning_points"]):
        pid = point["id"]
        if pid in ids:
            errors.append(f"learning_points[{index}]: duplicate knowledge id {pid!r}.")
        ids.add(pid)
        for sid in point["source_unit_ids"]:
            if sid not in sources:
                errors.append(f"learning_points[{index}]: unknown original source {sid!r}.")
        if point["priority"] != "context":
            taught_sources.update(point["source_unit_ids"])
        original_text = " ".join(
            u["text"] for u in data["source_assessments"]
            if u["source_unit_id"] in point["source_unit_ids"]
        )
        for term in point["focus_vocabulary"]:
            if not matches(original_text, term):
                errors.append(
                    f"Knowledge {pid!r}: focus vocabulary {term!r} must occur in linked original sources."
                )
        seen_candidates: set[str] = set()
        seen_text: set[str] = set()
        teacher_found = False
        chosen = 0
        for j, candidate in enumerate(point["candidates"]):
            cid = candidate["id"]
            if cid in seen_candidates:
                errors.append(f"learning_points[{index}].candidates[{j}]: duplicate candidate id {cid!r}.")
            seen_candidates.add(cid)
            norm = candidate["text"].strip().casefold()
            if norm in seen_text:
                errors.append(f"learning_points[{index}].candidates[{j}]: repeated wording; compare distinct alternatives.")
            seen_text.add(norm)
            if candidate["origin"] == "teacher":
                teacher_found = True
            if candidate["decision"] == "card":
                chosen += 1
                selected += 1
            if candidate["origin"] == "source" and not any(
                matches(item["text"], candidate["text"])
                for item in data["source_assessments"]
                if item["source_unit_id"] in point["source_unit_ids"]
            ):
                errors.append(f"learning_points[{index}].candidates[{j}]: source excerpt not present in linked originals.")
        if point["priority"] == "high" and chosen == 0:
            errors.append(f"High-priority knowledge {pid!r} requires a selected card candidate.")
        if point["priority"] == "context" and chosen:
            errors.append(f"Context-only knowledge {pid!r} should not request a card; change its priority with rationale.")
        if point["teacher_option"] == "explored" and not teacher_found:
            errors.append(f"Knowledge {pid!r} says teacher alternatives were explored but has no teacher-origin candidate.")
    for item in data["source_assessments"]:
        if item["disposition"] == "teach" and item["source_unit_id"] not in taught_sources:
            errors.append(
                f"Original source {item['source_unit_id']!r} was marked teach but has "
                "no high/medium learning point; analyze it before selecting cards."
            )
    if not selected:
        errors.append("Lesson analysis must select at least one meaningful card candidate.")
    return errors


def validate_against_plan(
    data: dict[str, Any], plan: dict[str, Any]
) -> list[str]:
    """Bind independently prepared analysis to the final selected cards."""
    errors = validate_analysis(data)
    if errors:
        return errors
    if data["target_language"].casefold() != str(plan["target_language"]["code"]).casefold():
        errors.append("lesson_analysis target_language does not match the card plan.")
    if data["base_language"].casefold() != str(plan["base_language"]["code"]).casefold():
        errors.append("lesson_analysis base_language does not match the card plan.")

    expected = {unit["id"]: unit["text"] for unit in plan.get("source_units", [])}
    observed = {unit["source_unit_id"]: unit["text"] for unit in data["source_assessments"]}
    if expected != observed:
        errors.append("lesson_analysis source units do not match plan source_units exactly (IDs and original text).")

    lookup = {(point["id"], candidate["id"]): (point, candidate)
              for point in data["learning_points"] for candidate in point["candidates"]}
    referenced: set[tuple[str, str]] = set()
    card_map = {str(card["id"]): card for card in plan["cards"]}
    for idx, card in enumerate(plan["cards"]):
        key = (card.get("learning_point_id"), card.get("candidate_id"))
        if key not in lookup:
            errors.append(f"cards[{idx}] must reference a candidate from the approved lesson analysis.")
            continue
        point, candidate = lookup[key]
        if candidate["decision"] != "card":
            errors.append(f"cards[{idx}] uses an analysis candidate not approved as a card.")
        if candidate["origin"] != card.get("origin"):
            errors.append(f"cards[{idx}] origin differs from teacher analysis.")
        if candidate["text"].strip() != str(card["target_text"]).strip():
            errors.append(f"cards[{idx}] target_text differs from approved candidate wording.")
        if key in referenced:
            errors.append(f"cards[{idx}] reuses a candidate already used for another card.")
        referenced.add(key)
        linked_sources = {unit["id"] for unit in plan["source_units"]
                          if str(card["id"]) in unit.get("card_ids", [])}
        if not linked_sources.intersection(point["source_unit_ids"]):
            errors.append(f"cards[{idx}] has no original source link for its learning point.")
    for key, (point, candidate) in lookup.items():
        if candidate["decision"] == "card" and key not in referenced:
            errors.append(f"Approved lesson candidate {key!r} was omitted from the final plan.")
    for point in data["learning_points"]:
        linked = [card for card in plan["cards"]
                  if card.get("learning_point_id") == point["id"]]
        if point["priority"] in {"high", "medium"} and linked:
            active = [str(card["target_text"]) for card in linked]
            active += [str(example["text"]) for card in linked
                       for example in card.get("teaching_examples", [])]
            for term in point["focus_vocabulary"]:
                if not any(matches(text, term) for text in active):
                    errors.append(
                        f"Knowledge {point['id']!r}: priority vocabulary {term!r} "
                        "is not actively taught in targets or teacher examples."
                    )
        if point["priority"] != "high":
            continue
        if not linked:
            errors.append(f"High-priority knowledge {point['id']!r} was not practiced.")
        if len(linked) > 1:
            goals = {str(card.get("learning_goal", "")).strip().casefold() for card in linked}
            if len(goals) != len(linked):
                errors.append(f"Knowledge {point['id']!r}: sibling cards need distinct learning goals.")
    # A teaching example is optional, never a pretext for forced extra reviews.
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate pre-card language teaching analysis.")
    parser.add_argument("analysis", type=Path)
    args = parser.parse_args()
    try:
        data = load_analysis(args.analysis)
        errors = validate_analysis(data)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}")
        return 2
    if errors:
        print("Lesson analysis invalid:")
        for error in errors:
            print(f"- {error}")
        return 1
    chosen = sum(c["decision"] == "card"
                 for point in data["learning_points"] for c in point["candidates"])
    print(f"Lesson analysis valid: {len(data['source_assessments'])} sources; "
          f"{len(data['learning_points'])} knowledge points; {chosen} selected card candidates.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
