from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "anki-language" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from audit_live import REQUIRED_ACTIONS, audit_live, normalize_fields, summarize_reviews  # noqa: E402


class FakeClient:
    def __init__(self) -> None:
        self.calls: list[tuple[str, dict | None]] = []

    def verify_actions(self, required: set[str]) -> dict:
        assert required == REQUIRED_ACTIONS
        return {"api_version": 6, "actions": sorted(required)}

    def invoke(self, action: str, params: dict | None = None):
        self.calls.append((action, params))
        if action == "findCards":
            return [102, 101]
        if action == "cardsInfo":
            return [
                {
                    "cardId": 102,
                    "note": 202,
                    "deckName": "Japanese::01 Reading",
                    "modelName": "Anki Language v3 — Reading",
                    "interval": 12,
                    "factor": 2500,
                    "fields": {
                        "Target": {"value": "分かる"},
                        "Base": {"value": "entender"},
                        "Source": {"value": "https://youtu.be/example?t=95"},
                    },
                },
                {
                    "cardId": 101,
                    "note": 201,
                    "deckName": "Japanese::03 Production",
                    "modelName": "Anki Language v3 — Production",
                    "interval": 3,
                    "factor": 2400,
                    "fields": {
                        "Target": {"value": "分かる"},
                        "Base": {"value": "entender"},
                    },
                },
            ]
        if action == "getReviewsOfCards":
            return {
                "102": [
                    {"id": 1001, "ease": 3},
                    {"id": 1002, "ease": 1},
                ],
                "101": [
                    {"id": 1003, "ease": 1},
                    {"id": 1004, "ease": 1},
                    {"id": 1005, "ease": 3},
                ],
            }
        if action == "areSuspended":
            return [False, True]
        raise AssertionError(f"Unexpected action: {action}")


def test_summarize_reviews_uses_anki_rating_semantics() -> None:
    summary = summarize_reviews([
        {"id": 10, "ease": 1},
        {"id": 11, "ease": 2},
        {"id": 12, "ease": 3},
        {"id": 13, "ease": 4},
        {"id": 14, "ease": 1},
    ])
    assert summary["reviews_total"] == 5
    assert summary["ratings"] == {
        "again": 2,
        "hard": 1,
        "good": 1,
        "easy": 1,
        "other": 0,
    }
    assert summary["again_rate"] == 0.4
    assert summary["last_review_id"] == 14


def test_normalize_fields_extracts_anki_values() -> None:
    assert normalize_fields({
        "Target": {"value": "bonjour", "order": 0},
        "Base": "hello",
    }) == {"Target": "bonjour", "Base": "hello"}


def test_audit_is_read_only_and_orders_repeat_failures_first() -> None:
    client = FakeClient()
    report = audit_live(client=client, limit=100, batch_size=100)

    assert report["status"] == "ok"
    assert report["mode"] == "read-only-audit"
    assert report["query"] == "tag:anki-language"
    assert report["total_found"] == 2
    assert report["cards_analyzed"] == 2
    assert report["truncated"] is False

    # Card 101 has more Again reviews, so it is surfaced first for inspection.
    assert [card["card_id"] for card in report["cards"]] == [101, 102]
    assert report["cards"][0]["ratings"]["again"] == 2
    assert report["cards"][0]["suspended"] is True
    assert report["cards"][1]["fields"]["Source"].endswith("?t=95")

    called = [action for action, _ in client.calls]
    assert called == ["findCards", "cardsInfo", "getReviewsOfCards", "areSuspended"]
    assert not {
        "updateNoteFields",
        "deleteNotes",
        "suspend",
        "setDueDate",
        "forgetCards",
        "relearnCards",
        "answerCards",
        "gradeNow",
    }.intersection(called)


def test_audit_limit_reports_truncation() -> None:
    client = FakeClient()
    report = audit_live(client=client, limit=1, batch_size=1)
    assert report["total_found"] == 2
    assert report["cards_analyzed"] == 1
    assert report["truncated"] is True
