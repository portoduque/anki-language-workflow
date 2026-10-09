"""v2.7 regressions: autonomous professor pre-card stage, linked candidates, audio."""
from __future__ import annotations

import copy
import json
import math
import sqlite3
import struct
import sys
import wave
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "anki-language"
sys.path.insert(0, str(SKILL / "scripts"))

import media_enrich  # noqa: E402
from build_apkg import build  # noqa: E402
from media_enrich import enrich_plan  # noqa: E402
from validate_lesson import load_analysis, validate_analysis, validate_against_plan  # noqa: E402
from validate_plan import load_plan, validate_plan  # noqa: E402


def examples(tmp_path: Path) -> tuple[dict, dict, Path]:
    source = SKILL / "examples"
    plan = json.loads((source / "card-plan.example.json").read_text(encoding="utf-8"))
    analysis = json.loads((source / "lesson-analysis.example.json").read_text(encoding="utf-8"))
    # Exercise the historical v2.7 contract independently of the current
    # v2.8 example's mandatory opportunity/tradeoff review.
    plan["version"] = "2.7"
    analysis["version"] = "1.0"
    analysis.pop("review", None)
    for item in analysis["source_assessments"]:
        item.pop("examined_expressions", None)
    analysis_path = tmp_path / "lesson-analysis.example.json"
    analysis_path.write_text(json.dumps(analysis, ensure_ascii=False), encoding="utf-8")
    return plan, analysis, tmp_path / "card-plan.json"


def issues(plan: dict, path: Path) -> list[str]:
    return validate_plan(plan, path, check_media=False)


def test_pre_card_analysis_and_example_valid(tmp_path: Path) -> None:
    plan, analysis, path = examples(tmp_path)
    assert validate_analysis(analysis) == []
    assert validate_against_plan(analysis, plan) == []
    assert issues(plan, path) == []
    assert len(analysis["source_assessments"]) == len(plan["source_units"])
    assert sum(c["origin"] == "teacher" and c["decision"] == "card"
               for lp in analysis["learning_points"] for c in lp["candidates"]) == 1


def test_high_priority_vocabulary_must_be_actively_used(tmp_path: Path) -> None:
    plan, analysis, path = examples(tmp_path)
    point = analysis["learning_points"][1]
    point["focus_vocabulary"] = ["travaille"]
    # The source is grounded, but its word appears only in a Back example,
    # which counts as active contextual teaching.
    assert validate_against_plan(analysis, plan) == []
    plan["cards"][1]["teaching_examples"] = []
    errors = validate_against_plan(analysis, plan)
    assert any("not actively taught" in error for error in errors)


def test_important_vocabulary_must_come_from_originals(tmp_path: Path) -> None:
    plan, analysis, path = examples(tmp_path)
    analysis["learning_points"][0]["focus_vocabulary"].append("inconnu")
    assert any("must occur in linked original sources" in e for e in validate_analysis(analysis))


def test_teach_source_requires_knowledge_point(tmp_path: Path) -> None:
    plan, analysis, path = examples(tmp_path)
    analysis["source_assessments"][1]["disposition"] = "teach"
    analysis["learning_points"][1]["source_unit_ids"] = ["phrase-01"]
    assert any("marked teach" in e for e in validate_analysis(analysis))


def test_cannot_deliver_without_pre_card_artifact(tmp_path: Path) -> None:
    plan, _, path = examples(tmp_path)
    plan.pop("lesson_analysis_file")
    assert any("requires lesson_analysis_file" in issue for issue in issues(plan, path))
    plan["lesson_analysis_file"] = "../outside.json"
    assert any("Invalid lesson_analysis_file" in issue for issue in issues(plan, path))


def test_analysis_covers_every_original_exactly(tmp_path: Path) -> None:
    plan, analysis, path = examples(tmp_path)
    analysis["source_assessments"][1]["text"] += " More."
    assert any("do not match" in error for error in validate_against_plan(analysis, plan))
    analysis["source_assessments"][1]["text"] = plan["source_units"][1]["text"]
    analysis["source_assessments"].pop()
    assert any("unknown original source" in error for error in validate_against_plan(analysis, plan))


def test_priority_and_decisions_cannot_be_retroactively_changed(tmp_path: Path) -> None:
    plan, analysis, path = examples(tmp_path)
    plan["cards"][1]["target_text"] = "Le cours commence."
    assert any("differs from approved candidate" in e for e in validate_against_plan(analysis, plan))
    plan, analysis, path = examples(tmp_path)
    plan["cards"][1]["candidate_id"] = "distance-original"
    assert any("not approved as a card" in e for e in validate_against_plan(analysis, plan))
    plan, analysis, path = examples(tmp_path)
    analysis["learning_points"][1]["candidates"][0]["decision"] = "reject"
    assert any("High-priority knowledge" in e for e in validate_against_plan(analysis, plan))
    plan, analysis, path = examples(tmp_path)
    analysis["learning_points"][1]["candidates"][0]["decision"] = "reject"
    analysis["learning_points"][1]["candidates"][1]["decision"] = "reject"
    assert any("High-priority knowledge" in e for e in validate_analysis(analysis))


def test_nothing_forces_authored_card_when_original_chunk_is_better(tmp_path: Path) -> None:
    plan, analysis, path = examples(tmp_path)
    distance = analysis["learning_points"][1]
    distance["candidates"][0]["decision"] = "reject"
    distance["candidates"][1]["decision"] = "card"
    distance["teacher_option"] = "unnecessary"
    distance["teacher_reason"] = "Source sentence already conveys the frame naturally; an adapted card is redundant."
    # Reprioritize the original lesson objective to distance only; the word
    # université remains preserved as context, not falsely marked active.
    distance["focus_vocabulary"] = ["à deux minutes d'ici"]
    plan["cards"][1]["origin"] = "source"
    plan["cards"][1]["target_text"] = "c'est à deux minutes d'ici."
    plan["cards"][1]["candidate_id"] = "distance-original"
    (tmp_path / "lesson-analysis.example.json").write_text(
        json.dumps(analysis, ensure_ascii=False), encoding="utf-8"
    )
    assert issues(plan, path) == []


def test_four_skill_review_and_candidate_provenance_required(tmp_path: Path) -> None:
    plan, analysis, path = examples(tmp_path)
    analysis["skill_review"].pop("listening")
    assert any("listening" in error for error in validate_analysis(analysis))
    plan, analysis, path = examples(tmp_path)
    analysis["learning_points"][0]["teacher_option"] = "explored"
    analysis["learning_points"][0]["candidates"] = [
        c for c in analysis["learning_points"][0]["candidates"]
        if c["origin"] != "teacher"
    ]
    assert any("teacher-origin candidate" in e for e in validate_analysis(analysis))


def test_independently_justified_second_card_on_high_priority_is_allowed(tmp_path: Path) -> None:
    plan, analysis, path = examples(tmp_path)
    additional = {
        "id": "follow-new", "skill": "listening", "origin": "teacher",
        "target_text": "Vous pouvez me suivre à l'université.",
        "base_text": "You can follow me to the university.",
        "learning_goal": "Recognize this invitation by ear without text",
        "selection_reason": "Independent listening comprehension bottleneck, not another Reading copy.",
        "learning_point_id": "follow", "candidate_id": "follow-teacher",
    }
    analysis["learning_points"][0]["candidates"][1]["decision"] = "card"
    plan["cards"].append(additional)
    plan["source_units"][0]["card_ids"].append("follow-new")
    (tmp_path / "lesson-analysis.example.json").write_text(json.dumps(analysis, ensure_ascii=False))
    assert issues(plan, path) == []


def fake_voice(text: str, language: str, output: Path, voice: str | None,
               voice_dir: Path, length_scale: float | None = None):
    output.parent.mkdir(parents=True, exist_ok=True)
    frequency = 200 + (sum(map(ord, text)) % 350)
    signal = [int(4000 * math.sin(2 * math.pi * frequency * i / 16000))
              for i in range(16000)]
    with wave.open(str(output), "wb") as audio:
        audio.setnchannels(1)
        audio.setsampwidth(2)
        audio.setframerate(16000)
        audio.writeframes(struct.pack("<" + "h" * len(signal), *signal))
    return voice or "fr_FR-siwis-medium", {}


def test_full_pipeline_still_exports_short_card_audio(tmp_path: Path, monkeypatch) -> None:
    plan, analysis, path = examples(tmp_path)
    monkeypatch.setattr(media_enrich, "synthesize_piper", fake_voice)
    path.write_text(json.dumps(plan, ensure_ascii=False), encoding="utf-8")
    resolved = tmp_path / "card-plan.resolved.json"
    stats = enrich_plan(path, resolved)
    assert stats["audio_generated"] == 2
    done = load_plan(resolved)
    assert validate_plan(done, resolved, check_media=True) == []
    assert all("anki-audio-" in c["audio"] for c in done["cards"])
    assert all(not u.get("audio") for u in done["source_units"])
    apkg = tmp_path / "French.apkg"
    result = build(resolved, apkg)
    assert result["cards_total"] == 2
    assert result["media_total"] == 2
    with zipfile.ZipFile(apkg) as archive:
        dest = tmp_path / "collection.anki2"
        dest.write_bytes(archive.read("collection.anki2"))
        media = json.loads(archive.read("media"))
        assert len(media) == 2
    with sqlite3.connect(dest) as con:
        assert con.execute("SELECT count(*) FROM notes").fetchone()[0] == 2


def test_legacy_26_unmodified(tmp_path: Path) -> None:
    plan, analysis, path = examples(tmp_path)
    plan["version"] = "2.6"
    plan.pop("lesson_analysis_file")
    for card in plan["cards"]:
        card.pop("learning_point_id")
        card.pop("candidate_id")
    plan["teacher_analysis"] = {
        "summary": "Teach polite directions and distance phrases as efficient reusable chunks.",
        "priority_vocabulary": ["suivre", "minutes", "université"],
        "discarded_candidates": [{"text": "Merci beaucoup!",
                                  "reason": "Already a very easy expression."}],
    }
    assert validate_plan(plan, path, check_media=False) == []
