from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "anki-language"
REF = SKILL / "references" / "anki-connect"
FINDER = SKILL / "scripts" / "find_ankiconnect_reference.py"


def route(query: str) -> dict:
    result = subprocess.run(
        [sys.executable, str(FINDER), query],
        cwd=ROOT,
        check=False,
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    return json.loads(result.stdout)


def test_action_catalog_is_complete_snapshot() -> None:
    catalog = json.loads((REF / "ACTION_CATALOG.json").read_text(encoding="utf-8"))
    assert catalog["api_version"] == 6
    assert catalog["action_count"] == 114
    assert len(catalog["actions"]) == 114
    names = {action["name"] for action in catalog["actions"]}
    for required in (
        "addNote",
        "addNotes",
        "storeMediaFile",
        "createModel",
        "modelTemplates",
        "findNotes",
        "cardsInfo",
        "requestPermission",
        "apiReflect",
        "multi",
        "sync",
        "exportPackage",
        "importPackage",
    ):
        assert required in names


def test_all_action_categories_are_represented() -> None:
    catalog = json.loads((REF / "ACTION_CATALOG.json").read_text(encoding="utf-8"))
    categories = {action["category"] for action in catalog["actions"]}
    assert categories == {
        "Card",
        "Deck",
        "Graphical",
        "Media",
        "Miscellaneous",
        "Model",
        "Note",
        "Statistic",
    }


def test_exact_addnote_routes_to_note_reference() -> None:
    data = route("addNote")
    assert any(action["name"] == "addNote" for action in data["matched_actions"])
    assert any(item["file"].endswith("05-note-actions.md") for item in data["references"])


def test_media_goal_routes_to_media_reference() -> None:
    data = route("storeMediaFile audio base64 url")
    assert any(action["name"] == "storeMediaFile" for action in data["matched_actions"])
    assert any(item["file"].endswith("07-media-actions.md") for item in data["references"])


def test_model_goal_routes_to_model_reference() -> None:
    data = route("createModel templates css fields")
    assert any(action["name"] == "createModel" for action in data["matched_actions"])
    assert any(item["file"].endswith("06-model-actions.md") for item in data["references"])


def test_security_config_reference_documents_safe_defaults() -> None:
    config = (REF / "01-installation-configuration.md").read_text(encoding="utf-8")
    protocol = (REF / "02-protocol-auth-security.md").read_text(encoding="utf-8")
    assert "2055492159" in config
    assert "127.0.0.1" in config
    assert "8765" in config
    assert "apiKey" in config
    assert "webCorsOriginList" in config
    assert "Never recommend this" in config or "Never recommend" in protocol
    assert "apiReflect" in protocol


def test_source_map_preserves_upstream_lineage() -> None:
    sources = (REF / "SOURCES.md").read_text(encoding="utf-8")
    assert "https://ankiweb.net/shared/info/2055492159" in sources
    assert "https://github.com/FooSoft/anki-connect" in sources
    assert "https://git.sr.ht/~foosoft/anki-connect" in sources
    assert "https://github.com/ankiultimate/anki-connect" in sources


def test_request_examples_cover_core_live_workflow() -> None:
    examples = (REF / "13-request-examples.md").read_text(encoding="utf-8")
    for action in (
        "version",
        "apiReflect",
        "createDeck",
        "createModel",
        "canAddNotesWithErrorDetail",
        "addNote",
        "storeMediaFile",
        "findNotes",
        "updateNoteFields",
        "guiBrowse",
        "multi",
        "exportPackage",
        "importPackage",
    ):
        assert action in examples


def test_skill_routes_live_collection_work_to_ankiconnect_library() -> None:
    skill = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    assert "## AnkiConnect live-integration reference" in skill
    assert "find_ankiconnect_reference.py" in skill
    assert "Never invent plausible AnkiConnect actions" in skill
    assert "versionapiReflect" in skill


def test_general_anki_router_can_escalate_to_ankiconnect() -> None:
    general = SKILL / "scripts" / "find_anki_reference.py"
    result = subprocess.run(
        [sys.executable, str(general), "AnkiConnect addNote live collection"],
        cwd=ROOT,
        check=False,
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    data = json.loads(result.stdout)
    assert any(item["file"].endswith("references/anki-connect/INDEX.md") for item in data["references"])
