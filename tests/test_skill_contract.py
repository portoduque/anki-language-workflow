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
