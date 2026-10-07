from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "anki-language"
EXAMPLE = SKILL / "examples" / "card-plan.example.json"

sys.path.insert(0, str(SKILL / "scripts"))
from build_apkg import CSS, FIELDS, MODEL_VERSION, card_context, make_model  # noqa: E402


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, *args], cwd=ROOT, check=False, text=True, capture_output=True)


def test_example_plan_validates() -> None:
    result = run(str(SKILL / "scripts" / "validate_plan.py"), str(EXAMPLE))
    assert result.returncode == 0, result.stdout + result.stderr


def test_one_command_pipeline_builds_and_deep_validates(tmp_path: Path) -> None:
    output = tmp_path / "French.apkg"
    build = run(str(SKILL / "scripts" / "build.py"), str(EXAMPLE), "--output", str(output))
    assert build.returncode == 0, build.stdout + build.stderr
    assert output.is_file()

    report = json.loads(Path(str(output) + ".report.json").read_text(encoding="utf-8"))
    assert report["cards_total"] == 3
    assert report["target_language"]["name"] == "French"
    assert report["base_language"]["name"] == "English"

    validate = run(str(SKILL / "scripts" / "validate_apkg.py"), str(output), "--plan", str(EXAMPLE))
    assert validate.returncode == 0, validate.stdout + validate.stderr
    summary = json.loads(validate.stdout)
    assert summary["card_count"] == 3
    assert summary["note_count"] == 3
    assert "French::01 Reading" in summary["deck_names"]
    assert "French::03 Production" in summary["deck_names"]


def test_non_english_base_language_builds(tmp_path: Path) -> None:
    plan = {
        "version": "2.0",
        "target_language": {"name": "Japanese", "code": "ja"},
        "base_language": {"name": "Portuguese", "code": "pt-BR"},
        "deck_name": "Japanese",
        "cards": [
            {
                "id": "ja-reading-1",
                "skill": "reading",
                "target_text": "猫",
                "base_text": "gato",
                "reading": "ねこ",
                "variant": "ネコ",
                "grammar": "noun",
                "tags": ["vocabulary"],
            }
        ],
    }
    plan_path = tmp_path / "plan.json"
    plan_path.write_text(json.dumps(plan, ensure_ascii=False), encoding="utf-8")
    output = tmp_path / "Japanese.apkg"
    result = run(str(SKILL / "scripts" / "build.py"), str(plan_path), "--output", str(output))
    assert result.returncode == 0, result.stdout + result.stderr
    report = json.loads(Path(str(output) + ".report.json").read_text(encoding="utf-8"))
    assert report["base_language"]["name"] == "Portuguese"


def test_listening_media_is_packaged(tmp_path: Path) -> None:
    import wave

    audio = tmp_path / "phrase.wav"
    with wave.open(str(audio), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(16000)
        wav.writeframes(b"\x00\x00" * 1600)
    plan = {
        "version": "2.0",
        "target_language": {"name": "French", "code": "fr"},
        "base_language": {"name": "Spanish", "code": "es"},
        "deck_name": "French",
        "cards": [
            {
                "id": "listen-1",
                "skill": "listening",
                "target_text": "Je suis ici.",
                "base_text": "Estoy aquí.",
                "audio": "phrase.wav",
                "audio_provenance": {"kind": "user-supplied"},
                "tags": ["listening"],
            }
        ],
    }
    plan_path = tmp_path / "plan.json"
    plan_path.write_text(json.dumps(plan, ensure_ascii=False), encoding="utf-8")
    output = tmp_path / "French.apkg"
    build = run(str(SKILL / "scripts" / "build.py"), str(plan_path), "--output", str(output))
    assert build.returncode == 0, build.stdout + build.stderr
    validate = run(str(SKILL / "scripts" / "validate_apkg.py"), str(output), "--plan", str(plan_path))
    assert validate.returncode == 0, validate.stdout + validate.stderr
    summary = json.loads(validate.stdout)
    assert summary["media_total"] == 1
    assert "French::02 Listening" in summary["deck_names"]


def test_pronunciation_front_does_not_render_target_directly() -> None:
    front = make_model("pronunciation").templates[0]["qfmt"]
    assert "{{Target}}" not in front
    assert "{{FrontAudio}}" in front


def test_card_template_has_dynamic_language_labels() -> None:
    back = make_model("reading").templates[0]["afmt"]
    assert "{{TargetLanguage}}" in back
    assert "{{BaseLanguage}}" in back
    assert ">English<" not in back

def test_workspace_config_rejects_mismatched_plan_languages(tmp_path: Path) -> None:
    config = {
        "version": "1.0",
        "target_language": {"name": "Japanese", "code": "ja"},
        "base_language": {"name": "Portuguese", "code": "pt-BR"},
    }
    (tmp_path / "anki-language.config.json").write_text(
        json.dumps(config, ensure_ascii=False), encoding="utf-8"
    )
    plan = {
        "version": "2.0",
        "target_language": {"name": "French", "code": "fr"},
        "base_language": {"name": "English", "code": "en"},
        "deck_name": "French",
        "cards": [
            {
                "id": "read-1",
                "skill": "reading",
                "target_text": "bonjour",
                "base_text": "hello",
            }
        ],
    }
    plan_path = tmp_path / "plan.json"
    plan_path.write_text(json.dumps(plan), encoding="utf-8")
    result = run(str(SKILL / "scripts" / "validate_plan.py"), str(plan_path))
    assert result.returncode == 1
    assert "does not match workspace configuration" in result.stdout


def test_front_context_identifies_target_language_and_skill() -> None:
    assert card_context("French", "listening") == "French — Listening"
    assert card_context("Japanese", "production") == "Japanese — Production"


def test_structured_language_fields_are_in_v3_models() -> None:
    field_names = [field["name"] for field in FIELDS]
    assert "Reading" in field_names
    assert "Variant" in field_names
    assert "Grammar" in field_names

    model = make_model("reading")
    assert model.name == "Anki Language v4 — Reading"
    back = model.templates[0]["afmt"]
    assert "{{#Reading}}" in back and "{{Reading}}" in back
    assert "{{#Variant}}" in back and "{{Variant}}" in back
    assert "{{#Grammar}}" in back and "{{Grammar}}" in back


def test_v4_templates_are_portable_for_night_mode_rtl_and_long_cards() -> None:
    assert MODEL_VERSION == 4
    assert ".card.nightMode" in CSS
    assert "@media (max-width: 480px)" in CSS
    assert "overflow-wrap: anywhere" in CSS

    reading = make_model("reading")
    front = reading.templates[0]["qfmt"]
    back = reading.templates[0]["afmt"]

    assert 'dir="auto"' in front
    assert 'dir="auto"' in back
    assert '<hr id="answer">' in back
    assert reading.name == "Anki Language v4 — Reading"


def test_legacy_v3_audit_compatibility_is_not_removed() -> None:
    # v4 is a new generated model family; audit_live remains model-agnostic and
    # existing v3 cards are intentionally not migrated in place.
    assert make_model("reading").name != "Anki Language v3 — Reading"
