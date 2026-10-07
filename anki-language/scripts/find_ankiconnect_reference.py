#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def normalize(text: str) -> str:
    return text.casefold().strip()


def tokens(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9_.:+-]+", normalize(text)))


def topic_score(query: str, topic: dict) -> int:
    q = normalize(query)
    q_tokens = tokens(q)
    total = 0
    for item in [topic["id"], *topic.get("keywords", [])]:
        k = normalize(str(item))
        if k in q:
            total += 10 + len(tokens(k))
        total += len(q_tokens & tokens(k))
    return total


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Route an AnkiConnect goal/action to the smallest useful local references."
    )
    parser.add_argument("query")
    parser.add_argument("--limit", type=int, default=4)
    args = parser.parse_args()

    skill_dir = Path(__file__).resolve().parents[1]
    ref_dir = skill_dir / "references" / "anki-connect"
    routing = json.loads((ref_dir / "ROUTING.json").read_text(encoding="utf-8"))
    catalog = json.loads((ref_dir / "ACTION_CATALOG.json").read_text(encoding="utf-8"))

    q = normalize(args.query)
    q_tokens = tokens(q)

    exact_actions = []
    fuzzy_actions = []
    for action in catalog.get("actions", []):
        name = action["name"]
        n = normalize(name)
        if n == q or n in q_tokens or n in q:
            exact_actions.append(action)
            continue

        action_text = " ".join([
            name,
            action.get("category", ""),
            action.get("description", ""),
            action.get("source_signature", ""),
            " ".join(action.get("parameters", []) or []),
            action.get("risk", ""),
        ])
        overlap = len(q_tokens & tokens(action_text))
        if overlap:
            fuzzy_actions.append((overlap, action))

    fuzzy_actions.sort(key=lambda pair: (-pair[0], pair[1]["name"]))
    matched_actions = exact_actions + [a for _, a in fuzzy_actions[:8]]
    seen = set()
    matched_actions = [
        a for a in matched_actions
        if not (a["name"] in seen or seen.add(a["name"]))
    ][:8]

    ranked = []
    for topic in routing["topics"]:
        score = topic_score(args.query, topic)
        if score:
            ranked.append({
                "topic": topic["id"],
                "file": str(skill_dir / topic["file"]),
                "score": score,
            })
    ranked.sort(key=lambda item: (-item["score"], item["topic"]))
    ranked = ranked[:max(1, args.limit)]

    category_to_file = {
        "Card": "03-card-actions.md",
        "Deck": "04-deck-actions.md",
        "Note": "05-note-actions.md",
        "Model": "06-model-actions.md",
        "Media": "07-media-actions.md",
        "Graphical": "08-gui-actions.md",
        "Miscellaneous": "09-misc-actions.md",
        "Statistic": "10-statistic-actions.md",
    }
    for action in matched_actions:
        filename = category_to_file.get(action.get("category"))
        if filename:
            candidate = str(ref_dir / filename)
            if all(r["file"] != candidate for r in ranked):
                ranked.append({
                    "topic": f"action:{action['name']}",
                    "file": candidate,
                    "score": 100 if action in exact_actions else 50,
                })

    ranked.sort(key=lambda item: (-item["score"], item["topic"]))
    ranked = ranked[:max(1, args.limit)]

    result = {
        "query": args.query,
        "matched_actions": matched_actions,
        "references": ranked,
        "catalog": str(ref_dir / "ACTION_CATALOG.json"),
        "config_reference": str(ref_dir / "CONFIG_REFERENCE.json"),
        "coverage": str(ref_dir / "COVERAGE.md"),
        "sources": str(ref_dir / "SOURCES.md"),
        "policy": (
            "Read only the returned local references first. "
            "For uncertain/version-sensitive actions, verify the user's live instance with "
            "version/apiReflect and consult the current upstream sources."
        ),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
