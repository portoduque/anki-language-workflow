from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "anki-language"
EXAMPLE = SKILL / "examples" / "card-plan.example.json"


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *args],
        cwd=ROOT,
        check=False,
        text=True,
        capture_output=True,
    )


def test_example_plan_validates_without_media() -> None:
    result = run(
        str(SKILL / "scripts" / "validate_plan.py"),
        str(EXAMPLE),
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_example_builds_and_validates(tmp_path: Path) -> None:
    output = tmp_path / "French.apkg"

    build = run(
        str(SKILL / "scripts" / "build_apkg.py"),
        str(EXAMPLE),
        str(output),
    )
    assert build.returncode == 0, build.stdout + build.stderr
    assert output.is_file()

    validate = run(
        str(SKILL / "scripts" / "validate_apkg.py"),
        str(output),
        "--plan",
        str(EXAMPLE),
    )
    assert validate.returncode == 0, validate.stdout + validate.stderr

    report_path = Path(str(output) + ".report.json")
    report = json.loads(report_path.read_text(encoding="utf-8"))
    assert report["cards_total"] == 3
    assert report["cards_by_skill"]["reading"] == 1
    assert report["cards_by_skill"]["production"] == 2
