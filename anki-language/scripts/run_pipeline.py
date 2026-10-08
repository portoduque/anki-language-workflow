#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from deliver import deliver
from media_enrich import enrich_plan
from validate_plan import load_plan, vocabulary_coverage


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

    print(json.dumps({
        "status": "ok",
        "resolved_plan": str(resolved.resolve()),
        "enrichment": enrichment,
        "delivery": delivery,
        "vocabulary_coverage": vocabulary_coverage(load_plan(resolved)) if load_plan(resolved).get("version") in {"2.5", "2.6"} else None,
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
