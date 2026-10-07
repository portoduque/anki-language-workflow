"""Regression tests for fast, distinct cards and correctly aligned audio."""
from __future__ import annotations

import json
import sys
import wave
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "anki-language" / "scripts"))

from media_enrich import enrich_plan  # noqa: E402
from validate_plan import validate_plan  # noqa: E402


def card(card_id: str, *, skill: str = "reading", target: str = "finir par", **fields: object) -> dict:
    return {"id": card_id, "skill": skill, "target_text": target, **fields}


def plan(cards: list[dict]) -> dict:
    return {
        "version": "2.0",
        "target_language": {"name": "French", "code": "fr"},
        "base_language": {"name": "English", "code": "en"},
        "deck_name": "French",
        "cards": cards,
    }


def problems(cards: list[dict], tmp_path: Path) -> list[str]:
    return validate_plan(plan(cards), tmp_path / "cards.json", check_media=False)


def test_same_reading_front_cannot_be_made_distinct_by_ids_tags_sources(tmp_path: Path) -> None:
    issues = problems([
        card("one", base_text="to end up", source="page 1"),
        card("two", base_text="to end up", tags=["new"], source="page 2"),
    ], tmp_path)
    assert any("duplicate retrieval task" in issue for issue in issues)


def test_conflicting_back_with_identical_reading_front_is_not_answerable(tmp_path: Path) -> None:
    issues = problems([
        card("one", base_text="sense A"),
        card("two", base_text="sense B"),
    ], tmp_path)
    assert any("duplicate retrieval task" in issue for issue in issues)


def test_cross_skill_retrieval_is_allowed_and_different_production_cues_are_distinct(tmp_path: Path) -> None:
    items = [
        card("read", base_text="to end up"),
        card("produce", skill="production", prompt="Say 'to end up'."),
        card("produce2", skill="production", prompt="Finish: J'ai ___ attendre."),
    ]
    assert problems(items, tmp_path) == []


def test_same_writing_gap_with_new_id_is_duplicate(tmp_path: Path) -> None:
    details = {
        "target_text": "Je vais à l'école.",
        "writing_answer": "à l'école",
        "prompt": "Type the expression meaning 'to school'.",
    }
    items = [
        {"id": "write1", "skill": "writing", **details},
        {"id": "write2", "skill": "writing", **details, "notes": "more details"},
    ]
    assert any("duplicate retrieval task" in issue for issue in problems(items, tmp_path))


def test_verified_audio_transcript_uses_word_boundaries_not_partial_substrings(tmp_path: Path) -> None:
    bad = card("bad", target="the cat", audio="source.wav", audio_transcript="the caterpillar")
    assert any("does not contain the target wording" in s for s in problems([bad], tmp_path))
    good = card("good", target="the cat", audio="source.wav", audio_transcript="I saw the cat.")
    assert problems([good], tmp_path) == []


def test_tts_cannot_read_a_different_sentence_than_the_card(tmp_path: Path) -> None:
    wrong = card("wrong", skill="listening", target="Bonjour", audio_request={
        "mode": "tts", "provider": "piper", "text": "Bonsoir",
    })
    assert any("audio_request.text must match target_text" in s for s in problems([wrong], tmp_path))
    right = card("right", skill="listening", target="Bonjour !", audio_request={
        "mode": "tts", "provider": "piper", "text": "bonjour",
    })
    assert problems([right], tmp_path) == []


def test_invalid_plan_fails_before_starting_media_enrichment(tmp_path: Path) -> None:
    source = tmp_path / "plan.json"
    source.write_text(json.dumps(plan([
        card("a"),
        card("b", source="elsewhere"),
    ])), encoding="utf-8")
    with pytest.raises(ValueError, match="duplicate retrieval task"):
        enrich_plan(source, tmp_path / "resolved.json")
    assert not (tmp_path / "media").exists()


def test_sanitized_card_ids_cannot_overwrite_one_anothers_generated_audio(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    import media_enrich

    def fake_tts(text: str, target_code: str, output: Path, voice: object, voice_dir: Path):
        output.parent.mkdir(parents=True, exist_ok=True)
        with wave.open(str(output), "wb") as handle:
            handle.setnchannels(1)
            handle.setsampwidth(2)
            handle.setframerate(16000)
            handle.writeframes(b"\\x00\\x00" * 1600)
        return "test-voice", {}

    monkeypatch.setattr(media_enrich, "synthesize_piper", fake_tts)
    source = tmp_path / "plan.json"
    source.write_text(json.dumps(plan([
        card("a/b", target="Bonjour", audio_request={"mode": "tts", "text": "Bonjour"}),
        card("a-b", target="Bonsoir", audio_request={"mode": "tts", "text": "Bonsoir"}),
    ])), encoding="utf-8")
    output = tmp_path / "resolved.json"
    enrich_plan(source, output)
    resolved = json.loads(output.read_text(encoding="utf-8"))
    names = [item["audio"] for item in resolved["cards"]]
    assert len(set(names)) == 2
    assert all((tmp_path / name).is_file() for name in names)
