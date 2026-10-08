from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "anki-language"
EXAMPLE = SKILL / "examples" / "card-plan.example.json"
LEGACY_EXAMPLE = SKILL / "examples" / "card-plan.legacy.example.json"

sys.path.insert(0, str(SKILL / "scripts"))
from build_apkg import CSS, FIELDS, MODEL_VERSION, card_context, make_model  # noqa: E402
from card_contract import WORKFLOW_TAG, workflow_tag  # noqa: E402


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, *args], cwd=ROOT, check=False, text=True, capture_output=True)


def test_example_plan_validates() -> None:
    result = run(str(SKILL / "scripts" / "validate_plan.py"), str(EXAMPLE), "--allow-missing-media")
    assert result.returncode == 0, result.stdout + result.stderr


def test_one_command_pipeline_builds_and_deep_validates(tmp_path: Path) -> None:
    output = tmp_path / "French.apkg"
    build = run(str(SKILL / "scripts" / "build.py"), str(LEGACY_EXAMPLE), "--output", str(output))
    assert build.returncode == 0, build.stdout + build.stderr
    assert output.is_file()

    report = json.loads(Path(str(output) + ".report.json").read_text(encoding="utf-8"))
    assert report["cards_total"] == 3
    assert report["target_language"]["name"] == "French"
    assert report["base_language"]["name"] == "English"

    validate = run(str(SKILL / "scripts" / "validate_apkg.py"), str(output), "--plan", str(LEGACY_EXAMPLE))
    assert validate.returncode == 0, validate.stdout + validate.stderr
    summary = json.loads(validate.stdout)
    assert summary["card_count"] == 3
    assert summary["note_count"] == 3
    assert "French::01 Reading" in summary["deck_names"]
    assert "French::05 Writing" in summary["deck_names"]
    assert WORKFLOW_TAG in summary["all_tags"]
    assert workflow_tag("French", "fr", "reading", "fr-reading-001") in summary["all_tags"]


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
                "audio_transcript": "Je suis ici.",
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


def test_structured_language_fields_are_in_current_models() -> None:
    field_names = [field["name"] for field in FIELDS]
    assert "Reading" in field_names
    assert "Variant" in field_names
    assert "Grammar" in field_names

    model = make_model("reading")
    assert model.name == "Anki Language v5 — Reading"
    back = model.templates[0]["afmt"]
    assert "{{#Reading}}" in back and "{{Reading}}" in back
    assert "{{#Variant}}" in back and "{{Variant}}" in back
    assert "{{#Grammar}}" in back and "{{Grammar}}" in back


def test_v5_templates_are_portable_for_night_mode_rtl_and_long_cards() -> None:
    assert MODEL_VERSION == 5
    assert ".card.nightMode" in CSS
    assert "@media (max-width: 480px)" in CSS
    assert "overflow-wrap: anywhere" in CSS

    reading = make_model("reading")
    front = reading.templates[0]["qfmt"]
    back = reading.templates[0]["afmt"]

    assert 'dir="auto"' in front
    assert 'dir="auto"' in back
    assert '<hr id="answer">' in back
    assert reading.name == "Anki Language v5 — Reading"


def test_older_note_types_are_not_mutated_in_place() -> None:
    # v5 is a new generated model family. Existing v3/v4 cards remain untouched
    # unless a separate explicit migration is requested.
    current = make_model("reading").name
    assert current != "Anki Language v3 — Reading"
    assert current != "Anki Language v4 — Reading"


def test_v5_ui_has_shared_hierarchy_and_skill_specific_identity() -> None:
    expected = {
        "reading": ("skill-reading", "Reading", "Read"),
        "listening": ("skill-listening", "Listening", "Listen"),
        "production": ("skill-production", "Production", "Produce"),
        "pronunciation": ("skill-pronunciation", "Pronunciation & Sounds", "Pronounce / identify"),
    }

    for skill, (skill_class, skill_label, stage_label) in expected.items():
        model = make_model(skill)
        front = model.templates[0]["qfmt"]
        back = model.templates[0]["afmt"]

        assert f'class="anki-card {skill_class}"' in front
        assert skill_label in front
        assert stage_label in front
        assert f'class="answer-shell {skill_class}"' in back
        assert '<div class="answer-chip">Answer</div>' in back
        assert "{{TargetLanguage}}" in front
        assert "{{Source}}" not in front
        assert "{{Source}}" in back

    assert "--surface:" in CSS
    assert "--accent:" in CSS
    assert ".skill-reading" in CSS
    assert ".skill-listening" in CSS
    assert ".skill-production" in CSS
    assert ".skill-pronunciation" in CSS
    assert ".answer-primary" in CSS
    assert ".hint-card" in CSS
    assert ".audio-stage" in CSS


def test_generated_templates_require_no_javascript_or_remote_assets() -> None:
    for skill in ("reading", "listening", "production", "pronunciation"):
        model = make_model(skill)
        rendered = "\n".join([
            CSS,
            model.templates[0]["qfmt"],
            model.templates[0]["afmt"],
        ]).lower()

        assert "<script" not in rendered
        assert "javascript:" not in rendered
        assert "http://" not in rendered
        assert "https://" not in rendered
        assert "<iframe" not in rendered


def test_source_metadata_stays_off_the_front() -> None:
    for skill in ("reading", "listening", "production", "pronunciation"):
        model = make_model(skill)
        assert "{{Source}}" not in model.templates[0]["qfmt"]
        assert "{{Source}}" in model.templates[0]["afmt"]


def test_plan_rejects_unknown_or_cross_skill_modes(tmp_path: Path) -> None:
    base_plan = {
        "version": "2.0",
        "target_language": {"name": "French", "code": "fr"},
        "base_language": {"name": "English", "code": "en"},
        "deck_name": "French",
    }

    typo = {
        **base_plan,
        "cards": [{
            "id": "bad-mode-1",
            "skill": "pronunciation",
            "mode": "sound-discriminaton",
            "prompt": "Which sound?",
            "target_text": "u",
        }],
    }
    typo_path = tmp_path / "typo.json"
    typo_path.write_text(json.dumps(typo), encoding="utf-8")
    result = run(str(SKILL / "scripts" / "validate_plan.py"), str(typo_path))
    assert result.returncode == 1
    assert "sound-discriminaton" in result.stdout

    wrong_skill = {
        **base_plan,
        "cards": [{
            "id": "bad-mode-2",
            "skill": "reading",
            "mode": "minimal-pair",
            "target_text": "dessert",
        }],
    }
    wrong_skill_path = tmp_path / "wrong-skill.json"
    wrong_skill_path.write_text(json.dumps(wrong_skill), encoding="utf-8")
    result = run(str(SKILL / "scripts" / "validate_plan.py"), str(wrong_skill_path))
    assert result.returncode == 1
    assert "not supported for skill 'reading'" in result.stdout


def test_spelling_sound_requires_audio_after_enrichment(tmp_path: Path) -> None:
    plan = {
        "version": "2.0",
        "target_language": {"name": "French", "code": "fr"},
        "base_language": {"name": "English", "code": "en"},
        "deck_name": "French",
        "cards": [{
            "id": "spell-sound-1",
            "skill": "pronunciation",
            "mode": "spelling-sound",
            "prompt": "Pronounce: eaux",
            "target_text": "eaux",
        }],
    }
    path = tmp_path / "spell-sound.json"
    path.write_text(json.dumps(plan), encoding="utf-8")
    result = run(str(SKILL / "scripts" / "validate_plan.py"), str(path))
    assert result.returncode == 1
    assert "audio is required for pronunciation mode 'spelling-sound'" in result.stdout


def test_plan_rejects_whitespace_only_required_identifiers(tmp_path: Path) -> None:
    plan = {
        "version": "2.0",
        "target_language": {"name": "French", "code": "fr"},
        "base_language": {"name": "English", "code": "en"},
        "deck_name": "   ",
        "cards": [{
            "id": "   ",
            "skill": "reading",
            "target_text": "   ",
        }],
    }
    path = tmp_path / "whitespace.json"
    path.write_text(json.dumps(plan), encoding="utf-8")
    result = run(str(SKILL / "scripts" / "validate_plan.py"), str(path))
    assert result.returncode == 1
    assert "does not match" in result.stdout
