"""v2.5: teacher-created chunks, vocabulary use, and unchanged media/Anki export."""
from __future__ import annotations

import json
import math
import sqlite3
import struct
import sys
import wave
import zipfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "anki-language" / "scripts"))

import media_enrich  # noqa: E402
from build_apkg import build, make_model  # noqa: E402
from card_contract import card_notes_with_examples, card_source_footer  # noqa: E402
from deliver_live import note_fields  # noqa: E402
from media_enrich import enrich_plan  # noqa: E402
from validate_plan import validate_plan, vocabulary_coverage, load_plan  # noqa: E402


def sample() -> dict:
    return {
        "version": "2.5",
        "target_language": {"name": "French", "code": "fr"},
        "base_language": {"name": "English", "code": "en"},
        "deck_name": "French",
        "audio_settings": {"voice": "fr_FR-siwis-medium", "length_scale": 0.93,
                           "include_source_audio": False},
        "source_units": [
            {"id": "first", "text": "Vous pouvez me suivre, c'est à deux minutes d'ici.",
             "card_ids": ["follow", "campus"]},
            {"id": "second", "text": "Je travaille ici à l'université.",
             "card_ids": ["campus"]},
        ],
        "cards": [
            {"id": "follow", "skill": "reading", "origin": "source",
             "target_text": "Vous pouvez me suivre", "base_text": "You can follow me."},
            {"id": "campus", "skill": "reading", "origin": "teacher",
             "target_text": "L'université est à deux minutes d'ici.",
             "base_text": "The university is two minutes from here.",
             "focus": "à deux minutes d'ici",
             "teaching_examples": [
                 {"text": "Je travaille ici. C'est à deux minutes d'ici.",
                  "base_text": "I work here. It's two minutes from here."},
             ]},
        ],
    }


def issues(data: dict, tmp_path: Path, check_media: bool = False) -> list[str]:
    return validate_plan(data, tmp_path / "cards.json", check_media=check_media)


def test_teacher_created_and_source_chunks_are_distinguished(tmp_path: Path) -> None:
    data = sample()
    assert issues(data, tmp_path) == []
    audit = vocabulary_coverage(data)
    assert audit["source_words"] > 8
    assert audit["covered_words"] == audit["source_words"]
    assert audit["missing_words"] == []
    notes = card_notes_with_examples(data, data["cards"][1])
    assert "Professor · chunk criado" in notes
    assert "Professor · exemplo criado: Je travaille ici." in notes
    assert "não é citação da fonte" in notes
    assert "Professor · exemplo criado" not in card_notes_with_examples(data, data["cards"][0])
    assert "Vous pouvez me suivre" in card_source_footer(data, data["cards"][0])
    assert "Je travaille ici à l'université." in card_source_footer(data, data["cards"][1])


def test_original_word_use_is_distinct_from_copied_source_footer(tmp_path: Path) -> None:
    data = sample()
    data["cards"][1]["teaching_examples"] = []
    errs = issues(data, tmp_path)
    assert any("vocabulary coverage incomplete" in e for e in errs)
    audit = vocabulary_coverage(data)
    assert "travaille" in audit["missing_words"]
    assert "c'est" in audit["missing_words"]
    assert "Je travaille ici" in card_source_footer(data, data["cards"][1])


def test_origin_is_required_and_quotations_are_verified(tmp_path: Path) -> None:
    data = sample()
    del data["cards"][0]["origin"]
    assert any(".origin is required" in e for e in issues(data, tmp_path))
    data["cards"][0]["origin"] = "source"
    data["cards"][0]["target_text"] = "Vous me pouvez suivre"
    assert any("origin=source" in e for e in issues(data, tmp_path))


def test_teacher_cannot_claim_verbatim_source_or_omit_meaning(tmp_path: Path) -> None:
    data = sample()
    data["cards"][1]["source_excerpt"] = "L'université est à deux minutes d'ici."
    assert any("cannot claim an exact source_excerpt" in e for e in issues(data, tmp_path))
    del data["cards"][1]["source_excerpt"]
    data["cards"][1]["base_text"] = ""
    assert any("base_text required" in e for e in issues(data, tmp_path))


def test_example_must_be_distinct_from_target(tmp_path: Path) -> None:
    data = sample()
    data["cards"][1]["teaching_examples"][0]["text"] = data["cards"][1]["target_text"]
    assert any("must differ from the target" in e for e in issues(data, tmp_path))


def test_full_card_and_live_export_show_generated_examples(tmp_path: Path, monkeypatch) -> None:
    calls: list[str] = []
    def fake_piper(text: str, language: str, output: Path, voice: str | None,
                   voice_dir: Path, length_scale: float | None = None):
        calls.append(text)
        freq = 170 + sum(map(ord, text)) % 500
        samples = [int(3500 * math.sin(2 * math.pi * freq * i / 16000))
                   for i in range(16000)]
        output.parent.mkdir(parents=True, exist_ok=True)
        with wave.open(str(output), "wb") as audio:
            audio.setnchannels(1)
            audio.setsampwidth(2)
            audio.setframerate(16000)
            audio.writeframes(struct.pack("<" + "h" * len(samples), *samples))
        return voice or "fr_FR-siwis-medium", {}
    monkeypatch.setattr(media_enrich, "synthesize_piper", fake_piper)
    original = tmp_path / "plan.json"
    original.write_text(json.dumps(sample(), ensure_ascii=False), encoding="utf-8")
    resolved = tmp_path / "resolved.json"
    stats = enrich_plan(original, resolved)
    data = load_plan(resolved)
    assert stats["audio_generated"] == 2
    assert len(calls) == 2  # focused targets only, not full source utterances
    assert not any(unit.get("audio") for unit in data["source_units"])
    assert issues(data, tmp_path, check_media=True) == []
    package = tmp_path / "test.apkg"
    result = build(resolved, package)
    assert result["cards_total"] == 2
    assert result["media_total"] == 2
    with zipfile.ZipFile(package) as archive:
        database = tmp_path / "collection.anki2"
        database.write_bytes(archive.read("collection.anki2"))
    with sqlite3.connect(database) as connection:
        raw_notes = [row[0] for row in connection.execute("SELECT flds FROM notes")]
    assert any("Professor · chunk criado" in raw for raw in raw_notes)
    assert any("Je travaille ici." in raw for raw in raw_notes)
    card = data["cards"][1]
    fields = note_fields(data, card)
    assert "Professor · chunk criado" in fields["Notes"]
    assert "Professor · exemplo criado" in fields["Notes"]
    assert "Je travaille ici à l'université." in fields["Source"]
    assert make_model("reading", "2.5").name == make_model("reading", "2.4").name


def test_legacy_v24_not_subject_to_new_coverage_rules(tmp_path: Path) -> None:
    legacy = sample()
    legacy["version"] = "2.4"
    for card in legacy["cards"]:
        card.pop("origin", None)
        card.pop("teaching_examples", None)
    assert issues(legacy, tmp_path) == []
    assert card_notes_with_examples(legacy, legacy["cards"][1]) == ""
