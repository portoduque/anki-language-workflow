"""v2.4 regression: focused TTS, optional source audio, Piper and Flatpak media."""
from __future__ import annotations

import base64
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
from card_contract import card_source_audio_paths  # noqa: E402
from deliver_live import build_note, upload_media_base64  # noqa: E402
from media_enrich import enrich_plan  # noqa: E402
from validate_plan import load_plan, validate_plan  # noqa: E402


def new_plan(source_audio: bool = False) -> dict:
    return {
        "version": "2.4", "deck_name": "French",
        "target_language": {"name": "French", "code": "fr"},
        "base_language": {"name": "English", "code": "en"},
        "audio_settings": {"voice": "fr_FR-siwis-medium", "length_scale": 0.93,
                           "include_source_audio": source_audio},
        "source_units": [
            {"id": "u1", "text": "Bonjour ! Vous pouvez me suivre, c'est à deux minutes d'ici.",
             "card_ids": ["c1", "c2"]},
        ],
        "cards": [
            {"id": "c1", "skill": "reading", "target_text": "Vous pouvez me suivre",
             "base_text": "You can follow me."},
            {"id": "c2", "skill": "listening", "target_text": "C'est à deux minutes d'ici.",
             "base_text": "It's two minutes away."},
        ],
    }


def fake_piper(calls: list[tuple[str, str | None, float | None]]):
    def synth(text: str, language: str, output: Path, voice: str | None,
              voice_dir: Path, length_scale: float | None = None):
        calls.append((text, voice, length_scale))
        freq = 180 + sum(map(ord, text)) % 450
        samples = [int(4000 * math.sin(2 * math.pi * freq * i / 16000))
                   for i in range(16000)]
        output.parent.mkdir(parents=True, exist_ok=True)
        with wave.open(str(output), "wb") as wav:
            wav.setnchannels(1)
            wav.setsampwidth(2)
            wav.setframerate(16000)
            wav.writeframes(struct.pack("<" + "h" * len(samples), *samples))
        return voice or "fr_FR-siwis-medium", {}
    return synth


def run_tts(tmp_path: Path, monkeypatch, source_audio: bool):
    calls: list[tuple[str, str | None, float | None]] = []
    monkeypatch.setattr(media_enrich, "synthesize_piper", fake_piper(calls))
    p = new_plan(source_audio)
    file = tmp_path / "plan.json"
    resolved = tmp_path / "resolved.json"
    file.write_text(json.dumps(p, ensure_ascii=False), encoding="utf-8")
    result = enrich_plan(file, resolved)
    return calls, result, load_plan(resolved), resolved


def test_focused_audio_without_context_by_default(tmp_path: Path, monkeypatch) -> None:
    calls, report, p, resolved = run_tts(tmp_path, monkeypatch, False)
    assert report["audio_generated"] == 2
    assert report["source_audio_generated"] == 0
    assert len(calls) == 2
    assert {text for text, _, _ in calls} == {
        "Vous pouvez me suivre", "C'est à deux minutes d'ici."
    }
    assert all(v == "fr_FR-siwis-medium" and rate == 0.93 for _, v, rate in calls)
    assert not p["source_units"][0].get("audio")
    assert not card_source_audio_paths(p, p["cards"][0])
    assert all(card["audio"] and card["media_validation"]["audio"]["sha256"]
               for card in p["cards"])
    assert validate_plan(p, resolved, check_media=True) == []
    output = tmp_path / "cards.apkg"
    result = build(resolved, output)
    assert result["cards_total"] == 2
    assert result["media_total"] == 2
    with zipfile.ZipFile(output) as archive:
        sqlite = tmp_path / "collection.anki2"
        sqlite.write_bytes(archive.read("collection.anki2"))
    with sqlite3.connect(sqlite) as con:
        modelset = json.loads(con.execute("SELECT models FROM col").fetchone()[0])
        assert all(m["flds"][-1]["name"] == "SourceAudio" for m in modelset.values())
        assert all(row[0].split("\x1f")[-1] == "" for row in con.execute("SELECT flds FROM notes"))


def test_context_audio_is_explicit_opt_in(tmp_path: Path, monkeypatch) -> None:
    calls, report, p, resolved = run_tts(tmp_path, monkeypatch, True)
    assert len(calls) == 3
    assert report["source_audio_generated"] == 1
    assert p["source_units"][0]["audio"]
    assert card_source_audio_paths(p, p["cards"][0])
    assert validate_plan(p, resolved, check_media=True) == []


def test_context_missing_blocks_delivery_when_opted_in(tmp_path: Path) -> None:
    p = new_plan(True)
    errs = validate_plan(p, tmp_path / "plan.json", check_media=True)
    assert any("source_units[0].audio" in error for error in errs)
    p["audio_settings"]["include_source_audio"] = False
    errs = validate_plan(p, tmp_path / "plan.json", check_media=True)
    assert not any("source_units[0].audio" in error for error in errs)


def test_production_retirement_and_voice_locale(tmp_path: Path) -> None:
    p = new_plan()
    p["cards"][0]["skill"] = "production"
    assert any("Production is retired" in x for x in
               validate_plan(p, tmp_path / "plan.json", check_media=False))
    p["cards"][0]["skill"] = "reading"
    p["audio_settings"]["voice"] = "en_US-lessac-medium"
    assert any("voice must match" in x for x in
               validate_plan(p, tmp_path / "plan.json", check_media=False))


class FakeFlatpakClient:
    def __init__(self):
        self.stored: dict[str, bytes] = {}
        self.actions: list[str] = []
    def invoke(self, action: str, params: dict):
        self.actions.append(action)
        if action == "retrieveMediaFile":
            content = self.stored.get(params["filename"])
            return base64.b64encode(content).decode("ascii") if content else False
        if action == "storeMediaFile":
            assert "path" not in params
            data = base64.b64decode(params["data"])
            self.stored[params["filename"]] = data
            return params["filename"]
        raise AssertionError(action)


def test_flatpak_media_sent_before_note_create_without_paths(tmp_path: Path) -> None:
    file = tmp_path / "short.wav"
    with wave.open(str(file), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(16000)
        w.writeframes(b"\x00\x00" * 16000)
    p = new_plan()
    p["cards"][0]["audio"] = file.name
    note, media = build_note(p, p["cards"][0], tmp_path)
    assert media
    c = FakeFlatpakClient()
    result = upload_media_base64(c, [note])
    assert file.name in result
    assert result[file.name]["sha256"] == hashlib.sha256(file.read_bytes()).hexdigest()
    assert "audio" not in note and "picture" not in note
    assert f"[sound:{file.name}]" in note["fields"]["BackAudio"]
    assert "storeMediaFile" in c.actions
    again = upload_media_base64(c, [{
        "fields": {"BackAudio": ""},
        "audio": [{"path": str(file), "filename": file.name, "fields": ["BackAudio"]}]
    }])
    assert again[file.name]["verified"]
    assert c.actions.count("storeMediaFile") == 1


def test_piper_command_speed_and_offline_model(tmp_path: Path, monkeypatch) -> None:
    from media_enrich import synthesize_piper
    model = tmp_path / "fr_FR-siwis-medium.onnx"
    config = tmp_path / "fr_FR-siwis-medium.onnx.json"
    model.write_bytes(b"fake")
    config.write_text("{}", encoding="utf-8")
    calls = []
    def fake_run(cmd, **kwargs):
        calls.append(cmd)
        class Done:
            returncode = 0
            stderr = ""
            stdout = ""
        return Done()
    monkeypatch.setattr(media_enrich.subprocess, "run", fake_run)
    output = tmp_path / "test.wav"
    selected, _ = synthesize_piper(
        "Bonjour.", "fr", output, "fr_FR-siwis-medium", tmp_path,
        length_scale=0.93,
    )
    assert selected == "fr_FR-siwis-medium"
    assert not any("piper.download_voices" in c for c in calls)
    assert "--length-scale" in calls[0]
    assert calls[0][calls[0].index("--length-scale") + 1] == "0.93"


def test_legacy_23_source_audio_behavior_and_model() -> None:
    p = new_plan()
    p["version"] = "2.3"
    p["audio_settings"] = {}
    p["source_units"][0]["audio"] = "old.wav"
    assert card_source_audio_paths(p, p["cards"][0]) == ["old.wav"]
    assert make_model("reading", "2.3").name == make_model("reading", "2.4").name
