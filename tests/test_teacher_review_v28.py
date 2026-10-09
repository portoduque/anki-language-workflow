"""v2.8: independent opportunity review and matched APKG/resolved media export."""
from __future__ import annotations

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

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "anki-language"
sys.path.insert(0, str(SKILL / "scripts"))

import media_enrich  # noqa: E402
from build_apkg import build  # noqa: E402
from media_enrich import enrich_plan  # noqa: E402
from validate_apkg import validate_apkg, media_hashes_from_plan  # noqa: E402
from validate_lesson import validate_analysis, validate_against_plan  # noqa: E402
from validate_plan import validate_plan, load_plan  # noqa: E402


def sample(tmp_path: Path):
    plan = json.loads((SKILL / "examples/card-plan.example.json").read_text(encoding="utf-8"))
    analysis = json.loads((SKILL / "examples/lesson-analysis.example.json").read_text(encoding="utf-8"))
    (tmp_path / "lesson-analysis.example.json").write_text(json.dumps(analysis, ensure_ascii=False), encoding="utf-8")
    plan_path = tmp_path / "plan.json"
    plan_path.write_text(json.dumps(plan, ensure_ascii=False), encoding="utf-8")
    return plan, analysis, plan_path


def test_v28_example_records_real_selection_competition(tmp_path: Path) -> None:
    plan, analysis, path = sample(tmp_path)
    assert analysis["version"] == "1.1" and plan["version"] == "2.8"
    assert validate_analysis(analysis) == []
    assert validate_against_plan(analysis, plan) == []
    assert validate_plan(plan, path, check_media=False) == []
    assert len(analysis["review"]["tradeoffs"]) == 2
    assert any(c["decision"] == "reject" for p in analysis["learning_points"] for c in p["candidates"])


def test_v28_requires_review_but_v27_stays_compatible(tmp_path: Path) -> None:
    plan, analysis, path = sample(tmp_path)
    analysis["version"] = "1.0"
    (tmp_path / "lesson-analysis.example.json").write_text(json.dumps(analysis, ensure_ascii=False))
    assert any("version 1.1" in e for e in validate_plan(plan, path, check_media=False))
    plan["version"] = "2.7"
    assert validate_plan(plan, path, check_media=False) == []


def test_invented_or_omitted_opportunities_are_rejected(tmp_path: Path) -> None:
    _, analysis, _ = sample(tmp_path)
    analysis["source_assessments"][0]["examined_expressions"][0]["text"] = "a fake French phrase"
    assert any("absent from the original" in e for e in validate_analysis(analysis))
    _, analysis, _ = sample(tmp_path)
    analysis["source_assessments"][0]["examined_expressions"] = []
    assert any("examined_expressions" in e for e in validate_analysis(analysis))


def test_competitive_review_rejects_fake_or_missing_comparisons(tmp_path: Path) -> None:
    _, analysis, _ = sample(tmp_path)
    analysis["review"]["tradeoffs"][0]["alternative_candidate_id"] = "follow-original"
    assert any("actually rejected" in e or "rejected or example" in e for e in validate_analysis(analysis))
    _, analysis, _ = sample(tmp_path)
    analysis["review"]["tradeoffs"][0]["alternative_candidate_id"] = "nonexistent"
    assert any("rejected or example-only" in e for e in validate_analysis(analysis))
    _, analysis, _ = sample(tmp_path)
    analysis["review"]["tradeoffs"].pop()
    # A single comparison suffices in this tiny 2-source teaching example.
    assert validate_analysis(analysis) == []


def test_substantial_lesson_cannot_approve_every_candidate(tmp_path: Path) -> None:
    _, analysis, _ = sample(tmp_path)
    # Eight original entries and two high points require independent
    # competitive decisions and explicit exclusion from SRS.
    for i in range(3, 9):
        analysis["source_assessments"].append({
            "source_unit_id": f"extra-{i}",
            "text": f"Bonjour {i}. Je travaille ici dans une université.",
            "observations": ["Common campus conversation."],
            "disposition": "context",
            "reason": "Already covered by the main teaching points.",
            "examined_expressions": [
                {"text": "Bonjour", "decision": "context",
                 "reason": "Duplicate greeting should not trigger a further card."},
            ],
        })
    assert validate_analysis(analysis) == []
    analysis["review"]["tradeoffs"] = [analysis["review"]["tradeoffs"][0]]
    assert any("two distinct" in e for e in validate_analysis(analysis))
    analysis["review"]["tradeoffs"] = [
        {"learning_point_id": "follow", "selected_candidate_id": "follow-original",
         "alternative_candidate_id": "follow-teacher",
         "reason": "One variation is not worth additional study."},
        {"learning_point_id": "distance", "selected_candidate_id": "distance-teacher",
         "alternative_candidate_id": "distance-original",
         "reason": "The created example offers more transfer."},
    ]
    for unit in analysis["source_assessments"]:
        unit["examined_expressions"] = [
            {**item, "decision": "practice", "learning_point_id": "follow"}
            for item in unit["examined_expressions"]
        ]
    assert any("context-only expressions" in e for e in validate_analysis(analysis))


def fake_piper(text: str, language: str, output: Path, voice: str | None,
               voice_dir: Path, length_scale: float | None = None):
    output.parent.mkdir(parents=True, exist_ok=True)
    frequency = 220 + sum(map(ord, text)) % 370
    signal = [int(3500 * math.sin(2 * math.pi * frequency * i / 16000))
              for i in range(16000)]
    with wave.open(str(output), "wb") as audio:
        audio.setnchannels(1)
        audio.setsampwidth(2)
        audio.setframerate(16000)
        audio.writeframes(struct.pack("<" + "h" * len(signal), *signal))
    return voice or "fr_FR-siwis-medium", {}


def test_export_hashes_package_bytes_and_delivers_matching_plan(tmp_path: Path, monkeypatch) -> None:
    _, _, original = sample(tmp_path)
    monkeypatch.setattr(media_enrich, "synthesize_piper", fake_piper)
    resolved = tmp_path / "plan.resolved.json"
    enrich_plan(original, resolved)
    plan = load_plan(resolved)
    assert validate_plan(plan, resolved, check_media=True) == []
    package = tmp_path / "French.apkg"
    report = build(resolved, package)
    snapshot = tmp_path / "French.resolved.json"
    assert snapshot.is_file()
    assert snapshot.read_bytes() == resolved.read_bytes()
    assert report["media_hash_verified"] is True
    assert report["resolved_plan_sha256"] == hashlib.sha256(snapshot.read_bytes()).hexdigest()
    assert report["apkg_sha256"] == hashlib.sha256(package.read_bytes()).hexdigest()
    expected = media_hashes_from_plan(plan)
    assert report["media_sha256"] == expected
    errors, summary = validate_apkg(package, expected_media_hashes=expected,
                                    expected_card_count=2)
    assert errors == []
    assert summary["note_count"] == 2
    assert json.loads((tmp_path / "French.apkg.report.json").read_text())["media_hash_verified"]


def test_corrupted_zip_audio_is_rejected_even_when_filename_matches(
    tmp_path: Path, monkeypatch
) -> None:
    _, _, original = sample(tmp_path)
    monkeypatch.setattr(media_enrich, "synthesize_piper", fake_piper)
    resolved = tmp_path / "plan.resolved.json"
    enrich_plan(original, resolved)
    plan = load_plan(resolved)
    good = tmp_path / "French.apkg"
    build(resolved, good)
    corrupt = tmp_path / "corrupt.apkg"
    with zipfile.ZipFile(good) as src, zipfile.ZipFile(corrupt, "w") as dst:
        media = json.loads(src.read("media"))
        changed = next(iter(media))
        for member in src.infolist():
            payload = src.read(member.filename)
            if member.filename == changed:
                payload = b"wrong media bytes"
            dst.writestr(member, payload)
    errors, _ = validate_apkg(corrupt, expected_media_hashes=media_hashes_from_plan(plan))
    assert any("content differs" in e for e in errors)
