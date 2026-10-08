#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from deliver import deliver
from media_enrich import enrich_plan
from validate_plan import load_plan, vocabulary_coverage
from validate_lesson import load_analysis


def main() -> int:
    parser = argparse.ArgumentParser(description="End-to-end media enrichment, validation, and delivery pipeline.")
    parser.add_argument("plan", type=Path)
    parser.add_argument("--resolved-plan", type=Path)
    parser.add_argument("--media-dir", type=Path)
    parser.add_argument("--delivery", choices=["apkg", "live", "both"])
    parser.add_argument("--output", type=Path, help="APKG output for apkg/both modes.")
    parser.add_argument("--endpoint", help="AnkiConnect endpoint for live/both modes.")
    args = parser.parse_args()

    resolved = args.resolved_plan or args.plan.with_name(args.plan.stem + ".resolved.json")
    try:
        enrichment = enrich_plan(args.plan, resolved, args.media_dir)
        delivery = deliver(resolved, args.delivery, args.output, args.endpoint)
    except Exception as exc:
        print(f"ERROR: {exc}")
        return 1

    current = load_plan(resolved)
    lesson_summary = None
    if current.get("version") == "2.7":
        analysis_path = (args.plan.resolve().parent / current["lesson_analysis_file"]).resolve()
        analysis = load_analysis(analysis_path)
        lesson_summary = {
            "source_units_analyzed": len(analysis["source_assessments"]),
            "knowledge_points": len(analysis["learning_points"]),
            "priority_knowledge": sum(p["priority"] == "high" for p in analysis["learning_points"]),
            "teacher_candidates_considered": sum(c["origin"] == "teacher" for p in analysis["learning_points"] for c in p["candidates"]),
            "author_cards_selected": sum(c.get("origin") == "teacher" for c in current["cards"]),
            "cards_by_skill": {skill: sum(c["skill"] == skill for c in current["cards"]) for skill in ("reading", "listening", "pronunciation", "writing")},
        }

    print(json.dumps({
        "status": "ok",
        "resolved_plan": str(resolved.resolve()),
        "enrichment": enrichment,
        "delivery": delivery,
        "teacher_analysis_summary": lesson_summary,
        "vocabulary_coverage": vocabulary_coverage(load_plan(resolved)) if load_plan(resolved).get("version") in {"2.5", "2.6", "2.7"} else None,
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
