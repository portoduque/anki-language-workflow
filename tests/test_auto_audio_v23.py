"""v2.3: automatic local speech + full-source on-demand replay, no extra cards."""
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
from card_contract import card_source_audio_paths  # noqa: E402
from deliver_live import build_note, expected_persisted_fields  # noqa: E402
from media_enrich import enrich_plan  # noqa: E402
from validate_plan import load_plan, validate_plan  # noqa: E402


def plan() -> dict:
    return {
        "version": "2.3", "target_language": {"name": "French", "code": "fr"},
        "base_language": {"name": "English", "code": "en"}, "deck_name": "French",
        "source_units": [
            {"id": "u1", "text": "Ah merci. C'est gentil ! Le cours commence.",
             "card_ids": ["reading", "writing"]},
            {"id": "u2", "text": "Vous pouvez me suivre.", "card_ids": ["listen", "pronounce"]},
            {"id": "u3", "text": "C'est gentil !", "card_ids": ["reading"]},
        ],
        "cards": [
            {"id": "reading", "skill": "reading", "target_text": "C'est gentil !",
             "base_text": "That's kind."},
            {"id": "writing", "skill": "writing", "target_text": "Le cours commence.",
             "writing_answer": "commence", "prompt": "Complete the verb."},
            {"id": "listen", "skill": "listening", "target_text": "Vous pouvez me suivre."},
            {"id": "pronounce", "skill": "pronunciation", "mode": "standard",
             "prompt": "Pronounce this sentence.", "target_text": "Vous pouvez me suivre."},
        ],
    }


def fake_piper(calls: list[str]):
    def synth(text: str, language: str, output: Path, voice: str | None, voice_dir: Path):
        calls.append(text)
        assert language == "fr"
        output.parent.mkdir(parents=True, exist_ok=True)
        samples = [int(4000 * math.sin(2 * math.pi * 180 * i / 16000))
                   for i in range(16000)]
        with wave.open(str(output), "wb") as handle:
            handle.setnchannels(1)
            handle.setsampwidth(2)
            handle.setframerate(16000)
            handle.writeframes(struct.pack("<" + "h" * len(samples), *samples))
        return "fr_FR-test-medium", {"license": {"name": "test license"}}
    return synth


def test_automatically_enriches_every_skill_and_full_source(tmp_path: Path, monkeypatch) -> None:
    calls: list[str] = []
    monkeypatch.setattr(media_enrich, "synthesize_piper", fake_piper(calls))
    src = tmp_path / "plan.json"
    src.write_text(json.dumps(plan(), ensure_ascii=False), encoding="utf-8")
    resolved = tmp_path / "resolved.json"
    report = enrich_plan(src, resolved)
    result = load_plan(resolved)
    assert report["audio_generated"] == 4  # 3 source texts + distinct Writing target
    assert len(calls) == 4
    assert all(c["audio"] for c in result["cards"])
    assert all(unit["audio"] for unit in result["source_units"])
    assert all(unit["media_validation"]["audio"]["sha256"] for unit in result["source_units"])
    assert result["cards"][0]["audio"] == result["source_units"][2]["audio"]
    assert result["cards"][2]["audio"] == result["cards"][3]["audio"]
    assert len(card_source_audio_paths(result, result["cards"][0])) == 1
    assert validate_plan(result, resolved, check_media=True) == []

    out = tmp_path / "French.apkg"
    report = build(resolved, out)
    assert report["cards_total"] == 4
    assert report["media_total"] == 4
    with zipfile.ZipFile(out) as package:
        db = tmp_path / "contents.anki2"
        db.write_bytes(package.read("collection.anki2"))
        assert len(json.loads(package.read("media"))) == 4
    con = sqlite3.connect(db)
    try:
        models = json.loads(con.execute("SELECT models FROM col").fetchone()[0])
        assert len(models) == 4
        assert all("v7" in m["name"] for m in models.values())
        assert all(m["flds"][-1]["name"] == "SourceAudio" for m in models.values())
        assert all("hint:SourceAudio" in m["tmpls"][0]["afmt"] for m in models.values())
        fields = [row[0].split("\x1f") for row in con.execute("SELECT flds FROM notes")]
        assert any("sound:" in f[-1] for f in fields)
    finally:
        con.close()

    note, media = build_note(result, result["cards"][0], resolved.parent)
    persisted = expected_persisted_fields(note)
    assert "sound:" in persisted["BackAudio"]
    assert "sound:" in persisted["SourceAudio"]
    assert len(media) == 2


def test_missing_tts_fails_before_export_no_silent_apkg(tmp_path: Path, monkeypatch) -> None:
    src = tmp_path / "plan.json"
    src.write_text(json.dumps(plan(), ensure_ascii=False), encoding="utf-8")
    def fail(*_args, **_kwargs):
        raise RuntimeError("no compatible voice installed")
    monkeypatch.setattr(media_enrich, "synthesize_piper", fail)
    with pytest.raises(RuntimeError, match="mandatory source audio.*no compatible voice"):
        enrich_plan(src, tmp_path / "resolved.json")
    assert not (tmp_path / "resolved.json").exists()
    assert any("source_units" in e and "audio" in e
               for e in validate_plan(plan(), src, check_media=True))


def test_previous_plan_version_does_not_require_or_add_audio(tmp_path: Path) -> None:
    old = plan()
    old["version"] = "2.2"
    src = tmp_path / "legacy.json"
    src.write_text(json.dumps(old, ensure_ascii=False), encoding="utf-8")
    assert validate_plan(old, src, check_media=True) == [
        e for e in validate_plan(old, src, check_media=True)
        if "source_units" not in e and "v2.3" not in e
    ]
    assert make_model("reading").name.startswith("Anki Language v5")
    assert make_model("pronunciation").name.startswith("Anki Language v6")
    assert "SourceAudio" not in [x["name"] for x in make_model("reading").fields]


def test_contrast_spoken_without_literal_slash() -> None:
    assert media_enrich.tts_spoken_target("Enchanté / Enchantée") == "Enchanté. Enchantée"
