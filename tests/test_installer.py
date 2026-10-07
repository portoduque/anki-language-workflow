from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INSTALLER = ROOT / "anki-language" / "scripts" / "install_skill.py"
ROOT_INSTALLER = ROOT / "install.py"


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, *args], cwd=ROOT, check=False, text=True, capture_output=True)


def test_codex_project_install(tmp_path: Path) -> None:
    result = run(str(INSTALLER), "codex", "--scope", "project", "--project", str(tmp_path))
    assert result.returncode == 0, result.stdout + result.stderr
    assert (tmp_path / ".agents" / "skills" / "anki-language" / "SKILL.md").is_file()


def test_claude_project_install(tmp_path: Path) -> None:
    result = run(str(INSTALLER), "claude", "--scope", "project", "--project", str(tmp_path))
    assert result.returncode == 0, result.stdout + result.stderr
    assert (tmp_path / ".claude" / "skills" / "anki-language" / "SKILL.md").is_file()


def test_antigravity_project_install_adds_slash_workflow(tmp_path: Path) -> None:
    result = run(str(INSTALLER), "antigravity", "--scope", "project", "--project", str(tmp_path))
    assert result.returncode == 0, result.stdout + result.stderr
    assert (tmp_path / ".agents" / "skills" / "anki-language" / "SKILL.md").is_file()
    workflow = tmp_path / ".agents" / "workflows" / "anki-language.md"
    assert workflow.is_file()


def test_generic_install_to_custom_skill_directory(tmp_path: Path) -> None:
    target = tmp_path / "custom-ai" / "skills" / "anki-language"
    result = run(str(INSTALLER), "generic", "--dest", str(target))
    assert result.returncode == 0, result.stdout + result.stderr
    assert (target / "SKILL.md").is_file()
    assert (target / "scripts" / "build.py").is_file()


def test_root_one_command_installer_can_install_generic_without_reinstalling_deps(tmp_path: Path) -> None:
    target = tmp_path / "one-command" / "anki-language"
    result = run(str(ROOT_INSTALLER), "generic", "--dest", str(target), "--skip-deps")
    assert result.returncode == 0, result.stdout + result.stderr
    assert (target / "SKILL.md").is_file()