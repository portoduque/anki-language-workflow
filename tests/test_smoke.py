from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "anki-language"
EXAMPLE = SKILL / "examples" / "card-plan.example.json"

sys.path.insert(0, str(SKILL / "scripts"))
from build_apkg import make_model  # noqa: E402


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *args],
        cwd=ROOT,
        check=False,
        text=True,
        capture_output=True,
    )


def test_example_plan_validates() -> None:
    result = run(str(SKILL / "scripts" / "validate_plan.py"), str(EXAMPLE))
    assert result.returncode == 0, result.stdout + result.stderr


def test_one_command_pipeline_builds_and_deep_validates(tmp_path: Path) -> None:
    output = tmp_path / "French.apkg"
    build = run(
        str(SKILL / "scripts" / "build.py"),
        str(EXAMPLE),
        "--output",
        str(output),
    )
    assert build.returncode == 0, build.stdout + build.stderr
    assert output.is_file()

    report = json.loads(Path(str(output) + ".report.json").read_text(encoding="utf-8"))
    assert report["cards_total"] == 3
    assert report["cards_by_skill"]["reading"] == 1
    assert report["cards_by_skill"]["production"] == 2

    validate = run(
        str(SKILL / "scripts" / "validate_apkg.py"),
        str(output),
        "--plan",
        str(EXAMPLE),
    )
    assert validate.returncode == 0, validate.stdout + validate.stderr
    summary = json.loads(validate.stdout)
    assert summary["card_count"] == 3
    assert summary["note_count"] == 3
    assert "French::01 Reading" in summary["deck_names"]
    assert "French::03 Production" in summary["deck_names"]


def test_listening_media_is_packaged(tmp_path: Path) -> None:
    audio = tmp_path / "phrase.mp3"
    audio.write_bytes(b"test-audio-payload")
    plan = {
        "version": "1.0",
        "target_language": {"name": "French", "code": "fr"},
        "support_language": {"name": "English", "code": "en"},
        "deck_name": "French",
        "cards": [
            {
                "id": "listen-1",
                "skill": "listening",
                "target_text": "Je suis ici.",
                "support_text": "I am here.",
                "audio": "phrase.mp3",
                "audio_provenance": {"kind": "user-supplied"},
                "tags": ["listening"],
            }
        ],
    }
    plan_path = tmp_path / "plan.json"
    plan_path.write_text(json.dumps(plan), encoding="utf-8")
    output = tmp_path / "French.apkg"

    build = run(
        str(SKILL / "scripts" / "build.py"),
        str(plan_path),
        "--output",
        str(output),
    )
    assert build.returncode == 0, build.stdout + build.stderr

    validate = run(
        str(SKILL / "scripts" / "validate_apkg.py"),
        str(output),
        "--plan",
        str(plan_path),
    )
    assert validate.returncode == 0, validate.stdout + validate.stderr
    summary = json.loads(validate.stdout)
    assert summary["media_total"] == 1
    assert "French::02 Listening" in summary["deck_names"]


def test_pronunciation_front_does_not_render_target_directly() -> None:
    front = make_model("pronunciation").templates[0]["qfmt"]
    assert "{{Target}}" not in front
    assert "{{FrontAudio}}" in front