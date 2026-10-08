"""Small synthetic regressions distilled from a user-exported French deck.

No private source sentences, imported deck, or user media are committed here.
"""
from __future__ import annotations

import json
import sqlite3
import sys
import wave
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "anki-language" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from build_apkg import FIELDS, build, make_model, model_version  # noqa: E402
from card_contract import pronunciation_front_cue  # noqa: E402
from deliver_live import build_note, model_payload  # noqa: E402
from validate_plan import normalized_utterance, validate_plan  # noqa: E402


def base_plan(cards: list[dict]) -> dict:
    return {
        "version": "2.0",
        "target_language": {"name": "French", "code": "fr"},
        "base_language": {"name": "Portuguese", "code": "pt-BR"},
        "deck_name": "French Test",
        "cards": cards,
    }


def make_wav(path: Path) -> None:
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(16000)
        w.writeframes(b"\x00\x00" * 3200)


def test_written_pronunciation_target_has_a_front_cue_but_audio_identification_does_not() -> None:
    phrase = "Vous pouvez me suivre."
    standard = {"skill": "pronunciation", "mode": "standard", "target_text": phrase}
    spelling = {"skill": "pronunciation", "mode": "spelling-sound", "target_text": phrase}
    heard = {"skill": "pronunciation", "mode": "sound-discrimination", "target_text": phrase}
    minimal = {"skill": "pronunciation", "mode": "minimal-pair", "target_text": phrase}
    to_spelling = {"skill": "pronunciation", "mode": "audio-to-spelling", "target_text": phrase}

    assert pronunciation_front_cue(standard) == phrase
    assert pronunciation_front_cue(spelling) == phrase
    assert all(not pronunciation_front_cue(card) for card in (heard, minimal, to_spelling))
    assert model_version("pronunciation") == 6
    assert all(model_version(skill) == 5 for skill in ("reading", "listening", "production"))
    template = make_model("pronunciation").templates[0]
    assert "{{#FrontCue}}" in template["qfmt"]
    assert "{{FrontCue}}" in template["qfmt"]
    assert "{{Target}}" not in template["qfmt"]
    assert "{{#FrontAudio}}" in template["qfmt"]
    assert make_model("pronunciation").name == "Anki Language v6 — Pronunciation & Sounds"
    assert len(make_model("pronunciation").fields) == len(FIELDS) + 1


def test_live_note_uses_same_pronunciation_cue_and_answer_side_audio(tmp_path: Path) -> None:
    audio = tmp_path / "spoken.wav"
    make_wav(audio)
    plan = base_plan([])
    standard = {
        "id": "say-natural",
        "skill": "pronunciation",
        "target_text": "Je suis prêt.",
        "prompt": "Diga esta expressão em voz alta.",
        "audio": audio.name,
    }
    note, _ = build_note(plan, standard, tmp_path)
    assert note["modelName"] == "Anki Language v6 — Pronunciation & Sounds"
    assert note["fields"]["FrontCue"] == "Je suis prêt."
    assert note["fields"]["FrontAudio"] == ""
    assert note["audio"][0]["fields"] == ["BackAudio"]
    assert model_payload("pronunciation")["inOrderFields"][-1] == "FrontCue"

    audio_id = {**standard, "mode": "sound-discrimination"}
    other, _ = build_note(plan, audio_id, tmp_path)
    assert other["fields"]["FrontCue"] == ""
    assert other["audio"][0]["fields"] == ["FrontAudio"]


def test_apkg_stores_front_cue_for_read_aloud_without_changing_v5_other_models(tmp_path: Path) -> None:
    plan = base_plan([
        {
            "id": "read-aloud",
            "skill": "pronunciation",
            "target_text": "Ça va.",
            "prompt": "Pronuncie em francês.",
        },
        {
            "id": "reading",
            "skill": "reading",
            "target_text": "Bonjour !",
            "base_text": "Olá!",
        },
    ])
    path = tmp_path / "plan.json"
    path.write_text(json.dumps(plan, ensure_ascii=False), encoding="utf-8")
    output = tmp_path / "sample.apkg"
    report = build(path, output)
    assert report["cards_total"] == 2
    assert output.is_file()

    with zipfile.ZipFile(output) as archive:
        # genanki currently exports collection.anki2; newer Anki exports may
        # use collection.anki21. Exercise the actual archive layout.
        db_name = "collection.anki21" if "collection.anki21" in archive.namelist() else "collection.anki2"
        db_path = tmp_path / db_name
        db_path.write_bytes(archive.read(db_name))
    with sqlite3.connect(db_path) as conn:
        rows = conn.execute("SELECT flds FROM notes").fetchall()
    by_target = {row[0].split("\x1f")[3]: row[0].split("\x1f") for row in rows}
    assert by_target["Ça va."][-1] == "Ça va."
    assert len(by_target["Bonjour !"]) == len(FIELDS)


def test_audio_reused_for_two_different_targets_needs_verified_transcript(tmp_path: Path) -> None:
    cards = [
        {"id": "listen", "skill": "listening", "target_text": "Je suis Suisse.", "audio": "clip.wav"},
        {
            "id": "say",
            "skill": "pronunciation",
            "target_text": "J'habite en France.",
            "prompt": "Pronuncie a frase.",
            "audio": "clip.wav",
        },
    ]
    errors = validate_plan(base_plan(cards), tmp_path / "plan.json", check_media=False)
    assert sum("audio_transcript is required" in error for error in errors) == 2

    transcript = "Je suis Suisse, mais j'habite en France."
    for card in cards:
        card["audio_transcript"] = transcript
    # The entire original clip is not appropriate for a shorter Listening /
    # read-aloud target merely because the words appear inside the transcript.
    issues = validate_plan(base_plan(cards), tmp_path / "plan.json", check_media=False)
    assert sum("audio_transcript must match target_text exactly" in issue for issue in issues) == 2


def test_audio_transcript_mismatch_and_conflicting_declarations_fail(tmp_path: Path) -> None:
    cards = [
        {
            "id": "listen",
            "skill": "listening",
            "target_text": "Je suis Suisse.",
            "audio": "clip.wav",
            "audio_transcript": "Nous sommes arrivés.",
        },
        {
            "id": "listen2",
            "skill": "listening",
            "target_text": "Vous êtes prêts.",
            "audio": "clip.wav",
            "audio_transcript": "Vous êtes prêts.",
        },
    ]
    errors = validate_plan(base_plan(cards), tmp_path / "plan.json", check_media=False)
    assert any("does not contain the target wording" in error for error in errors)
    assert any("inconsistent transcripts" in error for error in errors)


def test_punctuation_variations_do_not_break_verified_audio_alignment() -> None:
    assert normalized_utterance("J’habite en France !") == normalized_utterance("J'habite en France.")
    assert normalized_utterance("  À  deux minutes  ") == "à deux minutes"
