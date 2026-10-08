"""v2.6 teacher-first retrieval, source coverage, audio identity, safe live media."""
from __future__ import annotations

import base64
import copy
import hashlib
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
from card_contract import card_source_footer  # noqa: E402
from deliver_live import build_note, upload_media_base64  # noqa: E402
from media_enrich import enrich_plan  # noqa: E402
from validate_plan import validate_plan, vocabulary_coverage, load_plan, vocabulary_match  # noqa: E402


def lesson() -> dict:
    return {
        "version": "2.6", "deck_name": "French",
        "target_language": {"name": "French", "code": "fr"},
        "base_language": {"name": "English", "code": "en"},
        "audio_settings": {"voice": "fr_FR-siwis-medium",
                           "length_scale": 0.93,
                           "include_source_audio": False},
        "teacher_analysis": {
            "summary": "Teach useful direction requests and campus location frames without copying entire dialogue turns.",
            "priority_vocabulary": ["suivre", "minutes", "université", "travaille"],
            "discarded_candidates": [
                {"text": "Bonjour ! Vous pouvez me suivre, c'est à deux minutes d'ici.",
                 "reason": "Contains two independent tasks; splitting into natural short chunks is faster."}
            ],
        },
        "source_units": [
            {"id": "u1", "text": "Bonjour ! Vous pouvez me suivre, c'est à deux minutes d'ici.",
             "card_ids": ["follow", "campus"]},
            {"id": "u2", "text": "Je travaille ici à l'université.",
             "card_ids": ["campus"]},
            {"id": "u3", "text": "Merci beaucoup !",
             "card_ids": ["follow"]},
        ],
        "cards": [
            {"id": "follow", "skill": "reading", "origin": "source",
             "target_text": "Vous pouvez me suivre",
             "base_text": "You can follow me.",
             "learning_goal": "Recognize pouvoir + infinitive as a polite request",
             "selection_reason": "Practical reusable request, distinct from the whole direction turn."},
            {"id": "campus", "skill": "reading", "origin": "teacher",
             "target_text": "L'université est à deux minutes d'ici.",
             "base_text": "The university is two minutes away.",
             "learning_goal": "Indicate nearby distance in a new context",
             "selection_reason": "Combines language from two original sources in a natural standalone frame.",
             "teaching_examples": [
                 {"text": "Je travaille ici. C'est à deux minutes d'ici.",
                  "base_text": "I work here. It is two minutes away."}
             ]},
        ],
    }


def validate(plan: dict, tmp_path: Path, check_media: bool = False) -> list[str]:
    return validate_plan(plan, tmp_path / "plan.json", check_media=check_media)


def test_vocab_boundary_understands_french_apostrophes_without_partial_words() -> None:
    assert vocabulary_match("Je travaille à l'université.", "université")
    assert vocabulary_match("Je travaille à l’université.", "université")
    assert vocabulary_match("C'est à deux minutes d'ici.", "d'ici")
    assert not vocabulary_match("I can't", "can")
    assert not vocabulary_match("sociales", "social")


def test_teacher_first_short_retrieval_and_context_only_words(tmp_path: Path) -> None:
    p = lesson()
    assert validate(p, tmp_path) == []
    report = vocabulary_coverage(p)
    assert report["priority_vocabulary"] == 4
    assert report["priority_covered"] == 4
    assert "bonjour" in report["context_only_words"]
    assert "merci" in report["context_only_words"]
    assert "Bonjour !" in card_source_footer(p, p["cards"][0])
    assert "Merci beaucoup !" in card_source_footer(p, p["cards"][0])
    assert "Je travaille ici" in card_source_footer(p, p["cards"][1])


def test_not_force_teacher_cards_when_sources_are_short(tmp_path: Path) -> None:
    p = lesson()
    p["source_units"] = [
        {"id": "u1", "text": "Vous pouvez me suivre.", "card_ids": ["follow"]},
        {"id": "u2", "text": "C'est à deux minutes d'ici.", "card_ids": ["campus"]},
    ]
    p["cards"][1]["origin"] = "source"
    p["cards"][1]["target_text"] = "C'est à deux minutes d'ici."
    p["cards"][1]["teaching_examples"] = [{"text": "Je travaille ici à l'université."}]
    assert validate(p, tmp_path)  # Priority words must be source-grounded
    p["teacher_analysis"]["priority_vocabulary"] = ["suivre", "minutes"]
    assert validate(p, tmp_path) == []


def test_reject_1_to_1_copied_long_source_turns(tmp_path: Path) -> None:
    p = lesson()
    turns = [
        "Bonjour excusez moi comment je fais pour arriver à la faculté de sciences humaines et sociales en ce moment près de la bibliothèque centrale de l université",
        "Merci beaucoup vous êtes étudiant aussi et vous travaillez ici depuis longtemps dans cette université",
        "Non moi je travaille ici au département d histoire et je suis étudiante en sociologie",
        "Aujourd hui c est mon premier jour à l université et je parle assez bien le français",
    ]
    p["source_units"] = [
        {"id": f"s{i}", "text": text, "card_ids": [f"c{i}"]}
        for i, text in enumerate(turns)
    ]
    p["cards"] = [
        {"id": f"c{i}", "skill": "reading", "origin": "source",
         "target_text": text, "base_text": "A complete spoken turn.",
         "learning_goal": f"Memorize full unchunked utterance number {i}",
         "selection_reason": f"Directly repeat the entire original phrase {i} without chunking."}
        for i, text in enumerate(turns)
    ]
    p["teacher_analysis"]["priority_vocabulary"] = ["bonjour"]
    p["teacher_analysis"]["discarded_candidates"] = [
        {"text": "Au revoir", "reason": "Does not teach an independent reusable pattern."}
    ]
    errs = validate(p, tmp_path)
    assert any("source-copy shortcut" in item for item in errs)
    assert any("too long for a fast Reading" in item for item in errs)


def test_priority_vocabulary_and_selection_rationale_enforced(tmp_path: Path) -> None:
    p = lesson()
    del p["cards"][0]["learning_goal"]
    p["teacher_analysis"]["priority_vocabulary"] += ["étudiante"]
    errs = validate(p, tmp_path)
    assert any("requires learning_goal" in e for e in errs)
    assert any("not present in source" in e for e in errs)
    p = lesson()
    p["teacher_analysis"]["priority_vocabulary"] = ["bonjour"]
    assert any("missing from targets and examples" in e for e in validate(p, tmp_path))


def test_context_is_not_passed_off_as_active_vocabulary(tmp_path: Path) -> None:
    p = lesson()
    p["teacher_analysis"]["priority_vocabulary"].append("bonjour")
    assert any("Source footers" in e for e in validate(p, tmp_path))
    p["cards"][0]["teaching_examples"] = [
        {"text": "Bonjour ! Vous pouvez me suivre.", "base_text": "Hello! You can follow me."}
    ]
    assert validate(p, tmp_path) == []


def fake_speech_factory(calls: list[str]):
    def fake(text: str, language: str, output: Path, voice: str | None,
             voice_dir: Path, length_scale: float | None = None):
        calls.append(text)
        frequency = 170 + len(calls) * 60 + sum(map(ord, text)) % 170
        signal = [int(4000 * math.sin(2 * math.pi * frequency * i / 16000))
                  for i in range(16000)]
        output.parent.mkdir(parents=True, exist_ok=True)
        with wave.open(str(output), "wb") as handle:
            handle.setnchannels(1); handle.setsampwidth(2); handle.setframerate(16000)
            handle.writeframes(struct.pack("<" + "h" * len(signal), *signal))
        return voice or "fr_FR-siwis-medium", {}
    return fake


def test_v26_audio_by_actual_content_and_apkg_retains_short_targets(
    tmp_path: Path, monkeypatch
) -> None:
    calls: list[str] = []
    monkeypatch.setattr(media_enrich, "synthesize_piper", fake_speech_factory(calls))
    input_path = tmp_path / "plan.json"
    input_path.write_text(json.dumps(lesson(), ensure_ascii=False), encoding="utf-8")
    first = tmp_path / "first.json"
    second = tmp_path / "second.json"
    first_counts = enrich_plan(input_path, first)
    second_counts = enrich_plan(input_path, second)
    a, b = load_plan(first), load_plan(second)
    assert first_counts["audio_generated"] == 2
    assert second_counts["audio_generated"] == 2
    assert len(calls) == 4
    assert all(card["audio"].startswith("media/anki-audio-") for card in a["cards"])
    assert a["cards"][0]["audio"] != b["cards"][0]["audio"]
    assert all((tmp_path / card["audio"]).exists() for card in a["cards"] + b["cards"])
    assert all("bonjour" not in call.casefold() for call in calls)
    assert validate(a, tmp_path, True) == []
    package = tmp_path / "french.apkg"
    result = build(first, package)
    assert result["cards_total"] == 2
    assert result["media_total"] == 2
    with zipfile.ZipFile(package) as archive:
        sqlite = tmp_path / "collection.anki2"
        sqlite.write_bytes(archive.read("collection.anki2"))
    with sqlite3.connect(sqlite) as con:
        assert con.execute("SELECT count(*) FROM notes").fetchone()[0] == 2
    note, _ = build_note(a, a["cards"][1], tmp_path)
    assert "[sound:anki-audio-" in note["fields"]["BackAudio"] or note.get("audio")


def make_wav(path: Path) -> None:
    with wave.open(str(path), "wb") as wavefile:
        wavefile.setnchannels(1); wavefile.setsampwidth(2); wavefile.setframerate(16000)
        wavefile.writeframes(b"\x00\x00" * 16000)


class FakeAnki:
    def __init__(self):
        self.remote: dict[str, bytes] = {}
        self.writes: list[str] = []
    def invoke(self, name: str, params: dict):
        if name == "retrieveMediaFile":
            data = self.remote.get(params["filename"])
            return base64.b64encode(data).decode() if data is not None else False
        if name == "storeMediaFile":
            assert params["deleteExisting"] is False
            assert "path" not in params
            filename = params["filename"]
            assert filename not in self.remote
            self.remote[filename] = base64.b64decode(params["data"])
            self.writes.append(filename)
            return filename
        raise AssertionError(name)


def test_live_media_collision_preserves_old_and_updates_links(tmp_path: Path) -> None:
    wav = tmp_path / "anki-tts-shared.wav"
    make_wav(wav)
    original = b"prior speech from another voice"
    client = FakeAnki()
    client.remote[wav.name] = original
    note = {
        "fields": {"BackAudio": "", "SourceAudio": ""},
        "audio": [
            {"path": str(wav), "filename": wav.name, "fields": ["BackAudio"]},
            {"path": str(wav), "filename": wav.name, "fields": ["SourceAudio"]},
        ],
    }
    report = upload_media_base64(client, [note])
    new_name = f"anki-tts-shared-{hashlib.sha256(wav.read_bytes()).hexdigest()[:24]}.wav"
    assert client.remote[wav.name] == original
    assert client.remote[new_name] == wav.read_bytes()
    assert new_name in report and wav.name not in report
    assert note["fields"]["BackAudio"] == f"[sound:{new_name}]"
    assert note["fields"]["SourceAudio"] == f"[sound:{new_name}]"
    assert client.writes == [new_name]
    repeat = {"fields": {"BackAudio": ""},
              "audio": [{"path": str(wav), "filename": wav.name, "fields": ["BackAudio"]}]}
    again = upload_media_base64(client, [repeat])
    assert list(again) == [new_name]
    assert client.writes == [new_name]
    assert client.remote[wav.name] == original


def test_older_v25_word_gate_stays_strict(tmp_path: Path) -> None:
    p = lesson()
    p["version"] = "2.5"
    p.pop("teacher_analysis")
    for c in p["cards"]:
        c.pop("learning_goal")
        c.pop("selection_reason")
    errs = validate(p, tmp_path)
    assert any("vocabulary coverage incomplete" in e for e in errs)
