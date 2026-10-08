"""Regression coverage for source fidelity, skill-specific audio, and duplicate bytes."""
from __future__ import annotations

import sys
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "anki-language" / "scripts"))

from validate_plan import validate_plan  # noqa: E402


def plan(cards: list[dict]) -> dict:
    return {
        "version": "2.0",
        "target_language": {"name": "French", "code": "fr"},
        "base_language": {"name": "English", "code": "en"},
        "deck_name": "French",
        "cards": cards,
    }


def issues(tmp_path: Path, cards: list[dict], *, media: bool = False) -> list[str]:
    return validate_plan(plan(cards), tmp_path / "plan.json", check_media=media)


def example(card_id: str, skill: str, target: str, **extra: object) -> dict:
    return {"id": card_id, "skill": skill, "target_text": target, **extra}


def test_source_excerpt_catches_changed_wording_from_screenshot(tmp_path: Path) -> None:
    wrong = example(
        "quote", "listening", "Eh ben ! Mais vous parlez très bien le français !",
        audio="original.mp3",
        source_excerpt="Ah super ! Mais vous parlez très bien le français !",
    )
    assert any("source_excerpt does not contain the target wording" in e
               for e in issues(tmp_path, [wrong]))


def test_source_excerpt_allows_exact_source_chunk_with_normalized_punctuation(tmp_path: Path) -> None:
    right = example(
        "chunk", "production", "C'est gentil !",
        prompt="Thank someone kindly.",
        source_excerpt="Ah merci. C’est gentil ! Bon, le cours commence.",
    )
    assert issues(tmp_path, [right]) == []


def test_original_recording_must_declare_actual_transcript(tmp_path: Path) -> None:
    raw = example("a", "production", "C'est gentil !", prompt="Say 'that's kind'.",
                  audio="dialogue.mp3", audio_provenance={"kind": "user-supplied"})
    assert any("audio_transcript is required for original source audio" in e
               for e in issues(tmp_path, [raw]))
    raw["audio_transcript"] = "Ah merci. C'est gentil ! Bon, le cours commence."
    assert any("audio_transcript must match target_text exactly" in e
               for e in issues(tmp_path, [raw]))
    raw["audio_transcript"] = "C'est gentil !"
    assert issues(tmp_path, [raw]) == []


def test_listening_long_transcript_is_not_valid_for_short_target(tmp_path: Path) -> None:
    card = example("a", "listening", "le cours commence", audio="dialogue.mp3",
                   audio_transcript="Ah merci. C'est gentil. Bon, le cours commence.")
    assert any("audio_transcript must match target_text exactly" in e
               for e in issues(tmp_path, [card]))


def test_reading_with_broader_audio_context_is_compatible(tmp_path: Path) -> None:
    card = example("read", "reading", "C'est gentil !", audio="dialogue.mp3",
                   audio_transcript="Ah merci. C'est gentil !")
    assert issues(tmp_path, [card]) == []


def test_byte_identical_audio_with_different_names_and_answers_fails(tmp_path: Path) -> None:
    a, b = tmp_path / "audio_2.wav", tmp_path / "audio_3.wav"
    with wave.open(str(a), "wb") as handle:
        handle.setnchannels(1)
        handle.setsampwidth(2)
        handle.setframerate(16000)
        handle.writeframes(b"\\x00\\x00" * 16000)
    b.write_bytes(a.read_bytes())
    cards = [
        example("a", "listening", "Bonjour.", audio=a.name, audio_transcript="Bonjour."),
        example("b", "listening", "Bonsoir.", audio=b.name, audio_transcript="Bonsoir."),
    ]
    assert any("Identical audio bytes" in e for e in issues(tmp_path, cards, media=True))


def test_same_audio_can_support_same_target_in_two_distinct_skills(tmp_path: Path) -> None:
    cards = [
        example("listen", "listening", "Bonjour.", audio="one.mp3", audio_transcript="Bonjour."),
        example("say", "production", "Bonjour.", prompt="Greet someone.",
                audio="one.mp3", audio_transcript="Bonjour."),
    ]
    assert issues(tmp_path, cards) == []
