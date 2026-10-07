#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def tokens(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9.+:-]+", text.casefold()))


def score(query: str, keywords: list[str]) -> int:
    q = query.casefold()
    q_tokens = tokens(q)
    total = 0
    for keyword in keywords:
        k = keyword.casefold()
        if k in q:
            total += 8 + len(tokens(k))
        overlap = len(q_tokens & tokens(k))
        total += overlap
    return total


def main() -> int:
    parser = argparse.ArgumentParser(description="Route an Anki technical question to local reference files.")
    parser.add_argument("query", help="Technical Anki need, e.g. 'FSRS desired retention' or 'APKG audio media'.")
    parser.add_argument("--limit", type=int, default=4)
    args = parser.parse_args()

    skill_dir = Path(__file__).resolve().parents[1]
    route_path = skill_dir / "references" / "anki" / "ROUTING.json"
    data = json.loads(route_path.read_text(encoding="utf-8"))

    ranked = []
    for topic in data["topics"]:
        value = score(args.query, topic["keywords"] + [topic["id"]])
        if value:
            path = skill_dir / topic["file"]
            ranked.append({
                "topic": topic["id"],
                "file": str(path),
                "score": value,
            })

    ranked.sort(key=lambda item: (-item["score"], item["topic"]))
    ranked = ranked[: max(1, args.limit)]

    result = {
        "query": args.query,
        "references": ranked,
        "fallback_index": str(skill_dir / data["fallback"]["file"]),
        "official_live_index": data["fallback"]["live_index"],
        "policy": (
            "Read only the top matching local references first. "
            "Use the official live index for current/version-sensitive details or gaps."
        ),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
