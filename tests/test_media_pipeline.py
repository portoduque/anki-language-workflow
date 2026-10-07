from __future__ import annotations

import base64
import json
import sys
import wave
from pathlib import Path

import pytest
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "anki-language"
sys.path.insert(0, str(SKILL / "scripts"))

from deliver_live import verify_uploaded_media  # noqa: E402
from media_enrich import enrich_plan  # noqa: E402
from media_validate import MediaValidationError, validate_media_file  # noqa: E402
from validate_plan import load_plan, validate_plan  # noqa: E402


def write_wav(path: Path) -> None:
    with wave.open(str(path), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(16000)
        wav.writeframes(b"\x00\x00" * 3200)


def write_png(path: Path) -> None:
    Image.new("RGB", (64, 64), (240, 240, 240)).save(path, "PNG")


def test_audio_and_image_validation_are_real_decodes(tmp_path: Path) -> None:
    audio = tmp_path / "ok.wav"
    image = tmp_path / "ok.png"
    write_wav(audio)
    write_png(image)

    audio_result = validate_media_file(audio, "audio")
    image_result = validate_media_file(image, "image")

    assert audio_result["status"] == "valid"
    assert audio_result["duration_seconds"] > 0
    assert len(audio_result["sha256"]) == 64
    assert image_result["status"] == "valid"
    assert image_result["width"] == 64
    assert image_result["height"] == 64


def test_invalid_media_is_rejected_before_build_or_upload(tmp_path: Path) -> None:
    bad_audio = tmp_path / "bad.mp3"
    bad_image = tmp_path / "bad.png"
    bad_audio.write_bytes(b"not-an-audio-file" * 20)
    bad_image.write_bytes(b"not-an-image-file" * 20)

    with pytest.raises(MediaValidationError):
        validate_media_file(bad_audio, "audio")
    with pytest.raises(MediaValidationError):
        validate_media_file(bad_image, "image")


def test_enricher_validates_existing_media_and_records_hashes(tmp_path: Path) -> None:
    audio = tmp_path / "phrase.wav"
    image = tmp_path / "thing.png"
    write_wav(audio)
    write_png(image)

    plan = {
        "version": "2.0",
        "target_language": {"name": "French", "code": "fr"},
        "base_language": {"name": "English", "code": "en"},
        "deck_name": "French",
        "cards": [{
            "id": "card-1",
            "skill": "production",
            "prompt": "Say it.",
            "target_text": "Bonjour",
            "audio": "phrase.wav",
            "image": "thing.png",
        }],
    }
    plan_path = tmp_path / "plan.json"
    resolved = tmp_path / "resolved.json"
    plan_path.write_text(json.dumps(plan), encoding="utf-8")

    report = enrich_plan(plan_path, resolved)
    data = json.loads(resolved.read_text(encoding="utf-8"))
    validation = data["cards"][0]["media_validation"]

    assert report["media_validated"] == 2
    assert validation["audio"]["status"] == "valid"
    assert validation["image"]["status"] == "valid"
    assert len(validation["audio"]["sha256"]) == 64
    assert len(validation["image"]["sha256"]) == 64

    errors = validate_plan(load_plan(resolved), resolved, check_media=True)
    assert errors == []


def test_plan_rejects_media_changed_after_recorded_validation(tmp_path: Path) -> None:
    audio = tmp_path / "phrase.wav"
    write_wav(audio)
    plan = {
        "version": "2.0",
        "target_language": {"name": "French", "code": "fr"},
        "base_language": {"name": "English", "code": "en"},
        "deck_name": "French",
        "cards": [{
            "id": "listen-1",
            "skill": "listening",
            "target_text": "Bonjour",
            "audio": "phrase.wav",
        }],
    }
    source = tmp_path / "plan.json"
    resolved = tmp_path / "resolved.json"
    source.write_text(json.dumps(plan), encoding="utf-8")
    enrich_plan(source, resolved)

    write_wav(audio)
    with audio.open("ab") as handle:
        handle.write(b"changed")

    errors = validate_plan(load_plan(resolved), resolved, check_media=True)
    assert any("changed after validation" in error for error in errors)


class FakeClient:
    def __init__(self, payload: bytes):
        self.payload = payload

    def invoke(self, action, params=None):
        assert action == "retrieveMediaFile"
        return base64.b64encode(self.payload).decode("ascii")


def test_live_media_verification_compares_uploaded_bytes(tmp_path: Path) -> None:
    audio = tmp_path / "phrase.wav"
    write_wav(audio)
    result = verify_uploaded_media(FakeClient(audio.read_bytes()), audio)
    assert result["verified"] is True
    assert result["bytes"] == audio.stat().st_size


def test_live_media_verification_rejects_remote_mismatch(tmp_path: Path) -> None:
    audio = tmp_path / "phrase.wav"
    write_wav(audio)
    with pytest.raises(Exception, match="hash mismatch"):
        verify_uploaded_media(FakeClient(b"different"), audio)
