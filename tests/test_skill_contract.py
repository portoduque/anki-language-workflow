from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "anki-language"


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, *args], cwd=ROOT, check=False, text=True, capture_output=True)


def test_portable_skill_validates() -> None:
    result = run(str(SKILL / "scripts" / "validate_skill.py"), str(SKILL))
    assert result.returncode == 0, result.stdout + result.stderr


def test_skill_requires_first_run_target_and_base_languages() -> None:
    text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    assert "Mandatory first-run language setup" in text
    assert "Target language" in text
    assert "Base language" in text
    assert "do not use a default" in text.lower()
    assert "anki-language.config.json" in text


def test_openai_metadata_mentions_skill_and_first_run() -> None:
    data = yaml.safe_load((SKILL / "agents" / "openai.yaml").read_text(encoding="utf-8"))
    assert "$anki-language" in data["interface"]["default_prompt"]
    assert "target language" in data["interface"]["default_prompt"].lower()
    assert "base language" in data["interface"]["default_prompt"].lower()
    assert data["policy"]["allow_implicit_invocation"] is True


def test_antigravity_workflow_delegates_and_has_first_run_handshake() -> None:
    workflow = (SKILL / "assets" / "antigravity-workflow.md").read_text(encoding="utf-8")
    assert "use the installed `anki-language` skill as the source of truth" in workflow
    assert "target language" in workflow.lower()
    assert "base language" in workflow.lower()


def test_readme_documents_all_install_surfaces() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for command in ("python install.py codex", "python install.py claude", "python install.py antigravity", "python install.py generic"):
        assert command in readme
    assert "README maintenance rule" in readme

def test_skill_exposes_non_negotiable_card_rules() -> None:
    text = (SKILL / "SKILL.md").read_text(encoding="utf-8").lower()
    required = (
        "minimum useful number of cards",
        "one primary retrieval target",
        "self-orienting",
        "blind/ambiguous cloze is forbidden",
        "do not create automatic reverse cards",
        "do not generate every card type",
        "sentence mining is selective",
        "audio and images are optional",
        "keep answers concise",
        "ask the user instead of guessing",
    )
    for phrase in required:
        assert phrase in text


def test_readme_contains_official_card_creation_rules() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "## Official card-creation rules" in readme
    assert "useful, distinct, clear, atomic, fast" in readme


def test_skill_allows_selective_multi_card_reuse_without_volume_inflation() -> None:
    text = (SKILL / "SKILL.md").read_text(encoding="utf-8").lower()
    assert "same sentence, word, expression, audio, image, or passage may produce multiple cards" in text
    assert "incremental learning value" in text
    assert "future review cost" in text
    assert "optimize memory efficiency, not volume" in text


def test_readme_documents_anki_reference_library() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "## Complete Anki technical reference library" in readme
    assert "find_anki_reference.py" in readme
    assert "https://docs.ankiweb.net/llms.txt" in readme


def test_readme_documents_ankiconnect_reference_library() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "## Complete AnkiConnect reference library" in readme
    assert "find_ankiconnect_reference.py" in readme
    assert "114 baseline/common documented actions" in readme.lower()
    assert "118 cataloged entries total" in readme.lower()
    assert "version" in readme and "apiReflect" in readme


def test_skill_requires_validated_automatic_media_pipeline() -> None:
    skill = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    assert "## Automatic media and delivery" in skill
    assert "audio_request" in skill
    assert "image_request" in skill
    assert "run_pipeline.py" in skill
    assert "Never bypass this gate" in skill
    assert "retrieveMediaFile" in skill
    assert "SHA-256" in skill


def test_readme_documents_media_generation_and_delivery_modes() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "## Automatic audio, images, and delivery" in readme
    assert "Piper" in readme
    assert "Openverse" in readme
    assert "Wikimedia Commons" in readme
    assert "--delivery live" in readme
    assert "--delivery both" in readme
    assert "retrieveMediaFile" in readme
    assert "--skip-media-deps" in readme


def test_antigravity_workflow_never_bypasses_media_validation() -> None:
    workflow = (SKILL / "assets" / "antigravity-workflow.md").read_text(encoding="utf-8")
    assert "every audio/image is decoded and hashed before packaging/upload" in workflow
    assert "Never bypass media validation" in workflow


def test_fluent_forever_refinements_are_explicit_and_selective() -> None:
    card_rules = (SKILL / "references" / "card-selection.md").read_text(encoding="utf-8").lower()
    pedagogy = (SKILL / "references" / "pedagogy.md").read_text(encoding="utf-8").lower()
    skill = (SKILL / "SKILL.md").read_text(encoding="utf-8").lower()

    assert "same speaker/voice" in card_rules
    assert "fade out spelling/sound scaffolding" in card_rules
    assert "semantic success over exact example reproduction" in card_rules
    assert "target-language definition" in card_rules
    assert "same speaker/voice" in skill
    assert "spelling/spelling-sound cards are scaffolding" in skill
    assert "semantically correct alternative examples" in skill
    assert "monolinguality is not a goal by itself" in pedagogy


def test_fluent_forever_research_note_records_rejections() -> None:
    note = (SKILL / "references" / "research" / "fluent-forever-gallery.md").read_text(encoding="utf-8").lower()
    assert "rigid “no translation on cards”" in note
    assert "an image for almost every sentence" in note
    assert "fixed phase progression" in note
    assert "old anki scheduling settings" in note
    assert "100–300" in note


def test_readme_documents_research_derived_refinements() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "## Research-derived refinements" in readme
    assert "fluent-forever-gallery.md" in readme
    assert "Minimal-pair isolation" in readme
    assert "Spelling fade-out" in readme
    assert "Semantic success over verbatim recall" in readme
