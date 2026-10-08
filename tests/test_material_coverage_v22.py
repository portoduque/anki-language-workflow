"""v2.2 material coverage, retired Production, live/APKG parity and clip QA."""
from __future__ import annotations

import json
import struct
import sys
import wave
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "anki-language" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from build_apkg import build, clean  # noqa: E402
from card_contract import card_source_footer  # noqa: E402
from deliver_live import note_fields, reject_cross_generation_duplicates  # noqa: E402
from ankiconnect_client import AnkiConnectError  # noqa: E402
from audio_clip import inspect_clip_edges  # noqa: E402
from validate_plan import validate_plan  # noqa: E402


def make_plan(cards: list[dict], units: list[dict] | None = None, *,
              version: str = "2.2") -> dict:
    plan = {
        "version": version, "target_language": {"name": "French", "code": "fr"},
        "base_language": {"name": "English", "code": "en"}, "deck_name": "French",
        "cards": cards,
    }
    if units is not None:
        plan["source_units"] = units
    return plan


def r(cid: str = "read1", target: str = "C'est gentil !") -> dict:
    return {"id": cid, "skill": "reading", "target_text": target,
            "base_text": "That's kind!"}


def problems(plan: dict, tmp_path: Path) -> list[str]:
    return validate_plan(plan, tmp_path / "plan.json", check_media=False)


def test_current_contract_requires_every_input_text_unit(tmp_path: Path) -> None:
    p = make_plan([r()])
    assert any("nonempty source_units" in e for e in problems(p, tmp_path))
    p["source_units"] = [{"id": "a", "text": "C'est gentil !", "card_ids": ["read1"]}]
    assert problems(p, tmp_path) == []


def test_absent_or_unlinked_phrase_fails(tmp_path: Path) -> None:
    p = make_plan([r()], [
        {"id": "one", "text": "C'est gentil !", "card_ids": ["read1"]},
        {"id": "two", "text": "Le cours commence.", "card_ids": ["no-such-card"]},
    ])
    assert any("does not exist" in e for e in problems(p, tmp_path))


def test_user_words_and_sentences_share_fast_card_without_loss(tmp_path: Path) -> None:
    source = "Ah merci. C'est gentil ! Bon, le cours commence. Au revoir !"
    word = "étudiante"
    p = make_plan([r()], [
        {"id": "sentence", "text": source, "card_ids": ["read1"]},
        {"id": "word", "text": word, "card_ids": ["read1"]},
    ])
    assert problems(p, tmp_path) == []
    footer = card_source_footer(p, p["cards"][0])
    assert source in footer and word in footer
    assert note_fields(p, p["cards"][0])["Source"] == clean(footer)
    assert source not in note_fields(p, p["cards"][0])["Target"]


def test_source_file_independently_detects_missing_phrase(tmp_path: Path) -> None:
    original = tmp_path / "source.txt"
    original.write_text("Bonjour !\nBonsoir !\n", encoding="utf-8")
    p = make_plan([r(target="Bonjour !")],
                  [{"id": "one", "text": "Bonjour !", "card_ids": ["read1"]}])
    p["source_text_file"] = "source.txt"
    assert any("missing=" in e and "bonsoir" in e for e in problems(p, tmp_path))
    p["source_units"].append({"id": "two", "text": "Bonsoir !", "card_ids": ["read1"]})
    assert problems(p, tmp_path) == []


def test_four_skills_and_retired_production_regression(tmp_path: Path) -> None:
    cards = [
        r(),
        {"id": "write", "skill": "writing", "target_text": "Je vais à l'école.",
         "writing_answer": "à l'école", "prompt": "Type the phrase meaning to school."},
        {"id": "pronounce", "skill": "pronunciation", "target_text": "rue",
         "prompt": "Pronounce this word.", "mode": "standard"},
    ]
    units = [
        {"id": "a", "text": "C'est gentil !", "card_ids": ["read1"]},
        {"id": "b", "text": "Je vais à l'école.", "card_ids": ["write"]},
        {"id": "c", "text": "rue", "card_ids": ["pronounce"]},
    ]
    p = make_plan(cards, units)
    assert problems(p, tmp_path) == []
    p["cards"].append({"id": "prod", "skill": "production", "target_text": "Bonjour",
                       "prompt": "Say hello"})
    p["source_units"].append({"id": "d", "text": "Bonjour", "card_ids": ["prod"]})
    assert any("Production is retired" in e for e in problems(p, tmp_path))
    legacy = make_plan([{"id": "old", "skill": "production", "target_text": "Bonjour",
                         "prompt": "Say hello"}], version="2.0")
    assert problems(legacy, tmp_path) == []


def test_apkg_and_live_render_full_source_on_back(tmp_path: Path) -> None:
    p = make_plan([r()], [{
        "id": "utterance", "text": "Ah merci. C'est gentil ! Bon, le cours commence.",
        "card_ids": ["read1"],
    }])
    filepath = tmp_path / "plan.json"
    filepath.write_text(json.dumps(p, ensure_ascii=False), encoding="utf-8")
    result = build(filepath, tmp_path / "French.apkg")
    assert result["cards_total"] == 1
    import zipfile
    import sqlite3
    with zipfile.ZipFile(tmp_path / "French.apkg") as archive:
        with archive.open("collection.anki2") as src:
            db = tmp_path / "collection.anki2"
            db.write_bytes(src.read())
    con = sqlite3.connect(db)
    try:
        raw = con.execute("SELECT flds FROM notes").fetchone()[0]
        assert "Ah merci. C'est gentil" in raw
        assert "le cours commence" in raw
    finally:
        con.close()
    assert "Ah merci. C'est gentil" in note_fields(p, p["cards"][0])["Source"]


class DuplicateClient:
    def __init__(self, target: str, same_tag: str | None = None):
        self.target = target
        self.same_tag = same_tag
    def invoke(self, action: str, params: dict | None = None):
        if action == "findNotes":
            return [1234]
        if action == "notesInfo":
            return [{
                "noteId": 1234, "fields": {
                    "Context": {"value": "French — Reading"},
                    "Target": {"value": self.target},
                }, "tags": [self.same_tag] if self.same_tag else [],
            }]
        raise AssertionError(action)


def test_live_preflight_blocks_second_generation_duplicate_before_writing(tmp_path: Path) -> None:
    p = make_plan([r()], [{"id": "a", "text": "C'est gentil !", "card_ids": ["read1"]}])
    with pytest.raises(AnkiConnectError, match="already reviews"):
        reject_cross_generation_duplicates(DuplicateClient("C'est gentil !"), p)


def test_audio_edges_detect_loud_cuts_without_flagging_padded_audio(tmp_path: Path) -> None:
    path = tmp_path / "clip.wav"
    def write(samples: list[int]) -> None:
        with wave.open(str(path), "wb") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(16000)
            w.writeframes(struct.pack("<" + "h" * len(samples), *samples))
    loud = [12000 if i % 2 else -12000 for i in range(16000)]
    write(loud)
    assert "start" in inspect_clip_edges(path) and "end" in inspect_clip_edges(path)
    write([0] * 4000 + loud[4000:12000] + [0] * 4000)
    assert inspect_clip_edges(path) == []


def test_legacy_source_footer_is_unchanged() -> None:
    p = {"version": "2.1", "source_units": [{"id": "a", "text": "EXTRA",
                                              "card_ids": ["old"]}]}
    assert card_source_footer(p, {"id": "old", "source": "page 12"}) == "page 12"

def test_reading_two_forms_requires_clear_comparison_cue(tmp_path: Path) -> None:
    p = make_plan([r(target="Enchanté / Enchantée")],
                  [{"id": "two-forms", "text": "Enchanté / Enchantée",
                    "card_ids": ["read1"]}])
    assert any("Reading comparison/contrast fronts require" in e
               for e in problems(p, tmp_path))
    p["cards"][0]["prompt"] = "Which form is used by a female speaker?"
    assert problems(p, tmp_path) == []
