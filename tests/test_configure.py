from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIGURE = ROOT / "anki-language" / "scripts" / "configure.py"


def test_configure_persists_arbitrary_target_and_base_languages(tmp_path: Path) -> None:
    output = tmp_path / "anki-language.config.json"
    result = subprocess.run(
        [
            sys.executable, str(CONFIGURE),
            "--target-name", "Japanese", "--target-code", "ja",
            "--base-name", "Portuguese", "--base-code", "pt-BR",
            "--output", str(output),
        ],
        cwd=ROOT, check=False, text=True, capture_output=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    data = json.loads(output.read_text(encoding="utf-8"))
    assert data["target_language"]["name"] == "Japanese"
    assert data["base_language"]["name"] == "Portuguese"