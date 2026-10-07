"""Functional coverage for one-gap, short typed Writing cards.

Uses Anki's native {{type:WritingAnswer}} only; no external editor/add-on.
"""
from __future__ import annotations

import json
import sqlite3
import sys
import zipfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "anki-language" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from build_apkg import CSS, FIELDS, build, fields_for_skill, make_model  # noqa: E402
from card_contract import SKILL_META, writing_parts  # noqa: E402
from deliver_live import build_note, ensure_models, note_fields  # noqa: E402
from validate_plan import validate_plan  # noqa: E402


def card(**changes: object) -> dict:
    item = {
        "id": "write-01",
        "skill": "writing",
        "target_text": "Je vais à l'école.",
        "writing_answer": "à l'école",
        "prompt": "Complete com a expressão que significa 'para a escola'.",
        "base_text": "Eu vou à escola.",
    }
    item.update(changes)
    return item


def plan(cards: list[dict] | None = None) -> dict:
    return {
        "version": "2.0",
        "target_language": {"name": "French", "code": "fr"},
        "base_language": {"name": "Portuguese", "code": "pt-BR"},
        "deck_name": "French",
        "cards": cards if cards is not None else [card()],
    }


def test_writing_native_typing_template_is_single_gap_and_keeps_answer_hidden() -> None:
    assert SKILL_META["writing"] == ("05 Writing", "Writing")
    model = make_model("writing")
    front = model.templates[0]["qfmt"]
    back = model.templates[0]["afmt"]

    assert model.name == "Anki Language v5 — Writing"
    assert [x["name"] for x in model.fields] == [
        *[x["name"] for x in FIELDS],
        "WritingBefore", "WritingAfter", "WritingAnswer",
    ]
    assert 'class="anki-card skill-writing"' in front
    assert "Write the missing part" in front
    assert "{{WritingBefore}}" in front and "{{WritingAfter}}" in front
    assert front.count("{{type:WritingAnswer}}") == 1
    assert "{{WritingAnswer}}" not in front.replace("{{type:WritingAnswer}}", "")
    assert "{{Target}}" not in front
    assert "{{FrontAudio}}" not in front
    assert "{{Source}}" not in front
    assert "{{FrontSide}}" in back
    assert '<hr id="answer">' in back
    assert "{{Target}}" in back
    assert "{{WritingAnswer}}" in back
    assert "{{Source}}" in back
    assert ".skill-writing" in CSS
    assert ".nightMode .skill-writing" in CSS
    assert "#typeans" in CSS
    assert 'dir="auto"' in front
    assert "@media (max-width: 480px)" in CSS
    assert "<script" not in (front + back).lower()
    assert "https://" not in (front + back).lower()


def test_writing_parts_allow_meaningful_chunks_in_unspaced_scripts() -> None:
    assert writing_parts(card(
        target_text="私は学校に行きます。",
        writing_answer="学校",
    )) == ("私は", "学校", "に行きます。")
    assert writing_parts(card(
        target_text="我喜欢学习中文。",
        writing_answer="中文",
    )) == ("我喜欢学习", "中文", "。")


def test_writing_parts_preserve_unicode_accents_quotes_and_word_boundaries() -> None:
    assert writing_parts(card()) == ("Je vais ", "à l'école", ".")
    assert writing_parts(card(
        target_text="Nous sommes déjà arrivés.",
        writing_answer="déjà",
    )) == ("Nous sommes ", "déjà", " arrivés.")
    assert writing_parts(card(
        target_text="C'est à l'école qu'on apprend.",
        writing_answer="à l'école",
    )) == ("C'est ", "à l'école", " qu'on apprend.")


@pytest.mark.parametrize("target,answer,issue", [
    ("Je vais à l'école.", "demain", "exactly once"),
    ("Je vais à l'école.", "Je vais à l'école.", "part of the sentence"),
    ("Elle mange et mange encore.", "mange", "exactly once"),
    ("Nous sommes ici.", "omm", "word boundaries"),
    ("Je vais à l'école.", " école", "outer whitespace"),
    ("Je vais à l'école.", "", "non-empty"),
    ("Je vais à l'école.", "à\nl'école", "plain text"),
    ("Je vais à l'école.", "<b>école</b>", "plain text"),
])
def test_writing_rejects_bad_or_unanswerable_gaps(
    target: str, answer: str, issue: str, tmp_path: Path
) -> None:
    bad = card(target_text=target, writing_answer=answer)
    issues = validate_plan(plan([bad]), tmp_path / "plan.json", check_media=False)
    assert any(issue in x for x in issues), issues


def test_writing_requires_prompt_and_rejects_typed_field_for_other_skills(tmp_path: Path) -> None:
    errors = validate_plan(plan([card(prompt=" ")]), tmp_path / "plan.json", check_media=False)
    assert any("prompt is required for Writing" in x for x in errors)

    wrong = card(skill="reading")
    errors = validate_plan(plan([wrong]), tmp_path / "plan.json", check_media=False)
    assert any("writing_answer is only supported" in x for x in errors)


def test_writing_keeps_one_card_and_separate_skill_tag_from_production(tmp_path: Path) -> None:
    content = plan([card(), {
        "id": "production-01",
        "skill": "production",
        "target_text": "Je vais à l'école.",
        "prompt": "Diga que você está indo à escola.",
    }])
    input_path = tmp_path / "plan.json"
    input_path.write_text(json.dumps(content, ensure_ascii=False), encoding="utf-8")
    assert validate_plan(content, input_path, check_media=True) == []

    output = tmp_path / "French.apkg"
    report = build(input_path, output)
    assert report["cards_total"] == 2
    assert report["cards_by_skill"]["writing"] == 1
    assert output.is_file()

    with zipfile.ZipFile(output) as archive:
        name = "collection.anki21" if "collection.anki21" in archive.namelist() else "collection.anki2"
        database = tmp_path / name
        database.write_bytes(archive.read(name))
    with sqlite3.connect(database) as conn:
        notes = conn.execute("SELECT flds,tags FROM notes").fetchall()
        decks = conn.execute("SELECT count(*) FROM cards").fetchone()[0]
        models = json.loads(conn.execute("SELECT models FROM col").fetchone()[0])
        deck_data = json.loads(conn.execute("SELECT decks FROM col").fetchone()[0])
    assert decks == 2
    model_names = {item["name"] for item in models.values()}
    assert "Anki Language v5 — Writing" in model_names
    assert "Anki Language v5 — Production" in model_names
    assert "French::05 Writing" in {item["name"] for item in deck_data.values()}
    writing = next((fields.split("\x1f"), tags) for fields, tags in notes if "anki-language" in tags and fields.split("\x1f")[-1] == "à l'école")
    assert writing[0][-3:] == ["Je vais ", ".", "à l'école"]


def test_live_note_fields_and_model_match_apkg_contract(tmp_path: Path) -> None:
    item = card()
    assert note_fields(plan(), item)["WritingBefore"] == "Je vais "
    note, media = build_note(plan(), item, tmp_path)
    assert media == {}
    assert note["deckName"] == "French::05 Writing"
    assert note["modelName"] == "Anki Language v5 — Writing"
    assert note["fields"]["WritingAnswer"] == "à l'école"
    assert note["fields"]["WritingAfter"] == "."
    assert note["fields"]["FrontAudio"] == ""
    assert note["fields"]["BackAudio"] == ""


class ModelClient:
    def __init__(self) -> None:
        self.models: dict[str, dict] = {}

    def invoke(self, action: str, params: dict | None = None):
        params = params or {}
        if action == "modelNames":
            return list(self.models)
        if action == "createModel":
            self.models[params["modelName"]] = {
                "fields": list(params["inOrderFields"]),
                "templates": {
                    i["Name"]: {"Front": i["Front"], "Back": i["Back"]}
                    for i in params["cardTemplates"]
                },
                "css": params["css"],
            }
            return {"id": len(self.models)}
        if action == "modelFieldNames":
            return self.models[params["modelName"]]["fields"]
        if action == "modelTemplates":
            return self.models[params["modelName"]]["templates"]
        if action == "modelStyling":
            return {"css": self.models[params["modelName"]]["css"]}
        raise AssertionError(f"unexpected action {action}")


def test_writing_live_creation_and_drift_preflight() -> None:
    client = ModelClient()
    ensure_models(client, {"writing"})
    assert list(client.models) == ["Anki Language v5 — Writing"]
    assert client.models["Anki Language v5 — Writing"]["fields"] == [x["name"] for x in fields_for_skill("writing")]
    ensure_models(client, {"writing"})
    client.models["Anki Language v5 — Writing"]["css"] += " /* custom */"
    with pytest.raises(Exception, match="CSS drift"):
        ensure_models(client, {"writing"})
