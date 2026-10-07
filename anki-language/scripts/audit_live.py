#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
from collections import Counter
from pathlib import Path
from typing import Any, Iterable

from ankiconnect_client import AnkiConnectClient, AnkiConnectError

REQUIRED_ACTIONS = {
    "version",
    "apiReflect",
    "findCards",
    "cardsInfo",
    "getReviewsOfCards",
    "areSuspended",
}


def chunked(items: list[int], size: int) -> Iterable[list[int]]:
    for start in range(0, len(items), size):
        yield items[start:start + size]


def normalize_fields(raw: Any) -> dict[str, str]:
    if not isinstance(raw, dict):
        return {}
    result: dict[str, str] = {}
    for name, value in raw.items():
        if isinstance(value, dict):
            result[str(name)] = str(value.get("value", ""))
        else:
            result[str(name)] = str(value)
    return result


def summarize_reviews(reviews: list[dict[str, Any]] | None) -> dict[str, Any]:
    rows = reviews or []
    counts: Counter[int] = Counter()
    review_ids: list[int] = []

    for row in rows:
        try:
            ease = int(row.get("ease", 0))
        except (TypeError, ValueError):
            ease = 0
        counts[ease] += 1
        try:
            review_ids.append(int(row.get("id")))
        except (TypeError, ValueError):
            pass

    total = len(rows)
    known = sum(counts.get(value, 0) for value in (1, 2, 3, 4))
    again = counts.get(1, 0)
    return {
        "reviews_total": total,
        "ratings": {
            "again": again,
            "hard": counts.get(2, 0),
            "good": counts.get(3, 0),
            "easy": counts.get(4, 0),
            "other": total - known,
        },
        "again_rate": round(again / total, 4) if total else 0.0,
        "last_review_id": max(review_ids) if review_ids else None,
    }


def _review_rows(review_map: Any, card_id: int) -> list[dict[str, Any]]:
    if not isinstance(review_map, dict):
        return []
    rows = review_map.get(str(card_id), review_map.get(card_id, []))
    return rows if isinstance(rows, list) else []


def audit_live(
    query: str = "tag:anki-language",
    *,
    endpoint: str = "http://127.0.0.1:8765",
    api_key: str | None = None,
    limit: int = 1000,
    batch_size: int = 100,
    client: AnkiConnectClient | None = None,
) -> dict[str, Any]:
    if limit < 1:
        raise ValueError("limit must be >= 1")
    if batch_size < 1:
        raise ValueError("batch_size must be >= 1")

    client = client or AnkiConnectClient(endpoint, api_key)
    capabilities = client.verify_actions(REQUIRED_ACTIONS)

    found_raw = client.invoke("findCards", {"query": query}) or []
    found: list[int] = []
    seen: set[int] = set()
    for raw in found_raw:
        try:
            card_id = int(raw.get("cardId") if isinstance(raw, dict) else raw)
        except (TypeError, ValueError):
            continue
        if card_id not in seen:
            seen.add(card_id)
            found.append(card_id)

    total_found = len(found)
    selected = found[:limit]
    rows: list[dict[str, Any]] = []

    for batch in chunked(selected, batch_size):
        info_rows = client.invoke(
            "cardsInfo",
            {"cards": batch, "retrieved_info_mode": "COMPACT"},
        ) or []
        review_map = client.invoke("getReviewsOfCards", {"cards": batch}) or {}
        suspended_flags = client.invoke("areSuspended", {"cards": batch}) or []

        suspended_by_id = {
            card_id: bool(suspended_flags[index])
            for index, card_id in enumerate(batch)
            if index < len(suspended_flags)
        }

        info_by_id: dict[int, dict[str, Any]] = {}
        for info in info_rows:
            if not isinstance(info, dict):
                continue
            try:
                card_id = int(info.get("cardId"))
            except (TypeError, ValueError):
                continue
            info_by_id[card_id] = info

        for card_id in batch:
            info = info_by_id.get(card_id, {})
            review_summary = summarize_reviews(_review_rows(review_map, card_id))
            rows.append({
                "card_id": card_id,
                "note_id": info.get("note"),
                "deck_name": info.get("deckName"),
                "model_name": info.get("modelName"),
                "interval": info.get("interval"),
                "ease": info.get("factor", info.get("ease")),
                "suspended": suspended_by_id.get(card_id, False),
                "fields": normalize_fields(info.get("fields")),
                **review_summary,
            })

    rows.sort(
        key=lambda item: (
            -int(item["ratings"]["again"]),
            -int(item["reviews_total"]),
            int(item["card_id"]),
        )
    )

    return {
        "status": "ok",
        "mode": "read-only-audit",
        "query": query,
        "total_found": total_found,
        "cards_analyzed": len(rows),
        "truncated": total_found > len(selected),
        "limit": limit,
        "capabilities": capabilities,
        "cards": rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Read-only AnkiConnect audit of card fields and review history."
    )
    parser.add_argument(
        "--query",
        default="tag:anki-language",
        help="Anki search query. Defaults to cards created by this workflow.",
    )
    parser.add_argument("--endpoint", default=os.getenv("ANKICONNECT_URL", "http://127.0.0.1:8765"))
    parser.add_argument("--api-key-env", default="ANKICONNECT_API_KEY")
    parser.add_argument("--limit", type=int, default=1000)
    parser.add_argument("--batch-size", type=int, default=100)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    api_key = os.getenv(args.api_key_env) or None
    try:
        report = audit_live(
            args.query,
            endpoint=args.endpoint,
            api_key=api_key,
            limit=args.limit,
            batch_size=args.batch_size,
        )
    except (AnkiConnectError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}")
        return 1

    rendered = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
