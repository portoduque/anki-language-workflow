from __future__ import annotations

import json
import shutil
import subprocess
import sys
import wave
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "anki-language" / "scripts"
sys.path.insert(0, str(SCRIPTS))

import audio_clip as clip_module  # noqa: E402
from audio_clip import locate_exact_phrase  # noqa: E402
from media_enrich import enrich_plan  # noqa: E402
from media_validate import validate_media_file  # noqa: E402
from validate_plan import validate_plan  # noqa: E402


def make_wav(path: Path, seconds: int = 7) -> None:
    with wave.open(str(path), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(16000)
        wav.writeframes(b"\0\0" * (16000 * seconds))


def plan_for(cards: list[dict]) -> dict:
    return {
        "version": "2.0",
        "target_language": {"name": "French", "code": "fr"},
        "base_language": {"name": "Portuguese", "code": "pt-BR"},
        "deck_name": "French",
        "cards": cards,
    }


def target_card(**fields) -> dict:
    return {
        "id": "listen-one",
        "skill": "listening",
        "target_text": "Vous pouvez me suivre.",
        **fields,
    }


def test_exact_alignment_handles_apostrophe_case_and_punctuation() -> None:
    words = [
        (" Bienvenue,", 0.1, 0.7),
        (" J’", 1.1, 1.25),
        ("habite", 1.25, 1.8),
        (" en", 1.8, 2.0),
        (" France!", 2.0, 2.6),
        (" Au", 3.3, 3.5),
        (" revoir.", 3.5, 4.0),
    ]
    assert locate_exact_phrase("J'habite en FRANCE.", words) == (1.1, 2.6)


def test_alignment_does_not_guess_repeated_or_missing_phrases() -> None:
    words = [
        (" Vous", 0.3, 0.5), (" pouvez", 0.5, 0.9),
        (" me", 0.9, 1.0), (" suivre", 1.0, 1.6),
        (" Vous", 4.3, 4.5), (" pouvez", 4.5, 4.9),
        (" me", 4.9, 5.0), (" suivre", 5.0, 5.6),
    ]
    with pytest.raises(ValueError, match="multiple times"):
        locate_exact_phrase("Vous pouvez me suivre.", words)
    with pytest.raises(ValueError, match="not found exactly"):
        locate_exact_phrase("Bonjour mon ami.", words)
    with pytest.raises(ValueError, match="single word"):
        locate_exact_phrase("suivre", words)


def test_clip_request_validates_schema_conflicts_and_unresolved_state(tmp_path: Path) -> None:
    source = tmp_path / "lesson.wav"
    make_wav(source)
    card = target_card(audio_clip={"source": source.name, "start_seconds": 1.0, "end_seconds": 2.0})
    plan = plan_for([card])
    path = tmp_path / "plan.json"
    assert validate_plan(plan, path, check_media=False) == []
    errors = validate_plan(plan, path, check_media=True)
    assert any("must be resolved" in error for error in errors)

    partial = target_card(audio_clip={"source": source.name, "start_seconds": 1.0})
    assert any("end_seconds" in e for e in validate_plan(plan_for([partial]), path, check_media=False))

    competing = target_card(audio="lesson.wav", audio_clip={"source": source.name})
    errors = validate_plan(plan_for([competing]), path, check_media=False)
    assert any("choose only one audio source" in e for e in errors)


@pytest.mark.skipif(shutil.which("ffmpeg") is None, reason="FFmpeg not installed in CI")
def test_verified_timestamp_clip_is_short_and_validated_before_apkg(tmp_path: Path) -> None:
    source = tmp_path / "dialogue.wav"
    make_wav(source, seconds=9)
    initial_hash = validate_media_file(source, "audio")["sha256"]
    plan = plan_for([
        target_card(audio_clip={"source": source.name, "start_seconds": 2.0, "end_seconds": 3.0}),
        {
            "id": "production-one",
            "skill": "production",
            "target_text": "J'habite en France.",
            "prompt": "Diga onde você mora.",
            "audio_clip": {"source": source.name, "start_seconds": 4.0, "end_seconds": 5.2},
        },
    ])
    input_path = tmp_path / "plan.json"
    resolved_path = tmp_path / "resolved.json"
    input_path.write_text(json.dumps(plan), encoding="utf-8")

    result = enrich_plan(input_path, resolved_path)
    assert result["audio_clipped"] == 2
    assert result["audio_aligned"] == 0

    resolved = json.loads(resolved_path.read_text(encoding="utf-8"))
    for card in resolved["cards"]:
        assert "audio_clip" not in card
        assert card["audio"].endswith("-clip.wav")
        clip_path = tmp_path / card["audio"]
        assert clip_path.is_file() and clip_path != source
        duration = validate_media_file(clip_path, "audio")["duration_seconds"]
        assert 0.8 < duration < 2.0
        assert card["media_validation"]["audio"]["sha256"] == validate_media_file(clip_path, "audio")["sha256"]
        assert card["audio_provenance"]["alignment"] == "verified-timestamps"
        assert card["audio_provenance"]["source_path"] == source.name

    assert validate_plan(resolved, resolved_path, check_media=True) == []
    assert validate_media_file(source, "audio")["sha256"] == initial_hash

    # The normal APKG builder is part of the same delivery pipeline.
    output = tmp_path / "French.apkg"
    built = subprocess.run(
        [sys.executable, str(SCRIPTS / "build.py"), str(resolved_path), "--output", str(output)],
        text=True, capture_output=True, check=False,
    )
    assert built.returncode == 0, built.stdout + built.stderr
    deep = subprocess.run(
        [sys.executable, str(SCRIPTS / "validate_apkg.py"), str(output), "--plan", str(resolved_path)],
        text=True, capture_output=True, check=False,
    )
    assert deep.returncode == 0, deep.stdout + deep.stderr


@pytest.mark.skipif(shutil.which("ffmpeg") is None, reason="FFmpeg not installed in CI")
def test_auto_alignment_is_cached_per_source_and_uses_focused_clips(tmp_path: Path, monkeypatch) -> None:
    source = tmp_path / "dialogue.wav"
    make_wav(source, seconds=9)
    calls: list[tuple[Path, str]] = []
    def fake_transcribe(path: Path, language: str) -> list[tuple[str, float, float]]:
        calls.append((path, language))
        return [
            (" Vous", 1.0, 1.3), (" pouvez", 1.3, 1.7), (" me", 1.7, 1.9),
            (" suivre.", 1.9, 2.3), (" Je", 4.0, 4.2), (" suis", 4.2, 4.6),
            (" prêt.", 4.6, 5.2),
        ]
    monkeypatch.setattr(clip_module, "transcribe_words", fake_transcribe)

    plan = plan_for([
        target_card(audio_clip={"source": source.name}),
        {
            "id": "listen-two", "skill": "listening", "target_text": "Je suis prêt.",
            "audio_clip": {"source": source.name},
        },
    ])
    original = tmp_path / "original.json"
    resolved = tmp_path / "resolved.json"
    original.write_text(json.dumps(plan), encoding="utf-8")
    result = enrich_plan(original, resolved)

    assert result["audio_clipped"] == 2
    assert result["audio_aligned"] == 2
    assert calls == [(source, "fr")]
    done = json.loads(resolved.read_text(encoding="utf-8"))
    assert done["cards"][0]["audio"] != done["cards"][1]["audio"]
    assert all(c["audio_provenance"]["alignment"] == "asr-exact" for c in done["cards"])
    assert validate_plan(done, resolved, check_media=True) == []


@pytest.mark.skipif(shutil.which("ffmpeg") is None, reason="FFmpeg not installed in CI")
def test_clip_fails_closed_on_invalid_bounds_and_ambiguous_auto_match(tmp_path: Path, monkeypatch) -> None:
    source = tmp_path / "dialogue.wav"
    make_wav(source, seconds=5)
    plan = plan_for([target_card(audio_clip={"source": source.name, "start_seconds": 3.0, "end_seconds": 8.0})])
    input_path = tmp_path / "original.json"
    resolved = tmp_path / "resolved.json"
    input_path.write_text(json.dumps(plan), encoding="utf-8")
    with pytest.raises(RuntimeError, match="outside"):
        enrich_plan(input_path, resolved)
    assert not resolved.exists()

    monkeypatch.setattr(
        clip_module, "transcribe_words",
        lambda _p, _l: [
            (" Vous", 0.3, 0.5), (" pouvez", 0.5, 0.8), (" me", 0.8, 1.0), (" suivre", 1.0, 1.5),
            (" Vous", 2.3, 2.5), (" pouvez", 2.5, 2.8), (" me", 2.8, 3.0), (" suivre", 3.0, 3.5),
        ],
    )
    plan["cards"][0]["audio_clip"] = {"source": source.name}
    input_path.write_text(json.dumps(plan), encoding="utf-8")
    with pytest.raises(RuntimeError, match="multiple times"):
        enrich_plan(input_path, resolved)
    assert not resolved.exists()


def test_missing_ffmpeg_reports_actionable_error(tmp_path: Path, monkeypatch) -> None:
    source = tmp_path / "dialogue.wav"
    make_wav(source)
    monkeypatch.setattr(clip_module.shutil, "which", lambda _bin: None)
    with pytest.raises(RuntimeError, match="FFmpeg"):
        clip_module.clip_audio(
            source, tmp_path / "clip.wav", target_text="Je suis prêt.",
            language="fr", start_seconds=1, end_seconds=2, word_cache={},
        )


def test_optional_alignment_dependency_failure_is_actionable(tmp_path: Path, monkeypatch) -> None:
    source = tmp_path / "dialogue.wav"
    make_wav(source)
    monkeypatch.setattr(clip_module, "transcribe_words", lambda _p, _l: (_ for _ in ()).throw(RuntimeError("Install: python -m pip install -r requirements-alignment.txt")))
    with pytest.raises(RuntimeError, match="requirements-alignment"):
        clip_module.clip_audio(
            source, tmp_path / "clip.wav", target_text="Vous pouvez me suivre.",
            language="fr", start_seconds=None, end_seconds=None, word_cache={},
        )
