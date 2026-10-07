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


def test_openai_metadata_mentions_skill() -> None:
    data = yaml.safe_load((SKILL / "agents" / "openai.yaml").read_text(encoding="utf-8"))
    assert "$anki-language" in data["interface"]["default_prompt"]
    assert data["policy"]["allow_implicit_invocation"] is True


def test_antigravity_workflow_is_thin_delegate() -> None:
    workflow = (SKILL / "assets" / "antigravity-workflow.md").read_text(encoding="utf-8")
    assert "use the installed `anki-language` skill as the source of truth" in workflow
    assert "/anki-language" in workflow