from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "anki-language"
ANKI_REF = SKILL / "references" / "anki"
ROUTING = ANKI_REF / "ROUTING.json"
FINDER = SKILL / "scripts" / "find_anki_reference.py"


def run_query(query: str) -> dict:
    result = subprocess.run(
        [sys.executable, str(FINDER), query],
        cwd=ROOT,
        check=False,
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    return json.loads(result.stdout)


def test_all_routed_reference_files_exist() -> None:
    data = json.loads(ROUTING.read_text(encoding="utf-8"))
    assert data["fallback"]["live_index"] == "https://docs.ankiweb.net/llms.txt"
    for topic in data["topics"]:
        path = SKILL / topic["file"]
        assert path.is_file(), topic


def test_reference_index_covers_major_anki_topics() -> None:
    index = (ANKI_REF / "INDEX.md").read_text(encoding="utf-8").lower()
    required = (
        "note types",
        "templates",
        "cloze",
        "image occlusion",
        "media",
        "fsrs",
        "import",
        "sync",
        "add-ons",
        "automation",
        "mobile",
        "troubleshooting",
    )
    for phrase in required:
        assert phrase in index


def test_router_finds_fsrs_reference() -> None:
    data = run_query("FSRS desired retention scheduling")
    files = [item["file"] for item in data["references"]]
    assert any(path.endswith("07-scheduling-fsrs-study-options.md") for path in files)


def test_router_finds_apkg_and_media_references() -> None:
    data = run_query("APKG audio media import package")
    files = [item["file"] for item in data["references"]]
    assert any(path.endswith("08-import-export-packages.md") for path in files)
    assert any(path.endswith("05-media-audio-images-tts.md") for path in files)


def test_router_finds_automation_reference() -> None:
    data = run_query("AnkiConnect automation API")
    files = [item["file"] for item in data["references"]]
    assert any(path.endswith("12-automation-development-apis.md") for path in files)


def test_sources_points_to_official_live_docs_index() -> None:
    sources = (ANKI_REF / "SOURCES.md").read_text(encoding="utf-8")
    assert "https://docs.ankiweb.net/llms.txt" in sources
    assert "https://docs.ankiweb.net/manual/deck-options" in sources
    assert "https://docs.ankiweb.net/manual/importing/text-files" in sources
    assert "https://docs.ankiweb.net/addons/intro" in sources


def test_skill_routes_technical_anki_questions_selectively() -> None:
    skill = (SKILL / "SKILL.md").read_text(encoding="utf-8").lower()
    assert "anki technical reference routing" in skill
    assert "find_anki_reference.py" in skill
    assert "do **not** preload the full anki library" in skill
    assert "docs.ankiweb.net/llms.txt" in skill


def test_native_binary_grading_and_break_recovery_are_documented() -> None:
    scheduling = (ANKI_REF / "07-scheduling-fsrs-study-options.md").read_text(encoding="utf-8")
    addons = (ANKI_REF / "11-useful-addons.md").read_text(encoding="utf-8")

    assert "### Optional two-button grading" in scheduling
    assert "only **Again** and **Good**" in scheduling
    assert "does **not** require a Pass/Fail add-on" in scheduling
    assert "## Returning after a break" in scheduling
    assert "resume where they left off" in scheduling
    assert "### Pass/Fail / two-button grading add-ons" in addons
    assert "Do not install a Pass/Fail add-on merely to obtain binary grading" in addons
