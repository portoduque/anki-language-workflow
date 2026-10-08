"""New v2.1 cards omit Production; audio inventory guards full source coverage."""
from __future__ import annotations

import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "anki-language" / "scripts"))
from validate_plan import validate_plan  # noqa: E402


def plan(cards: list[dict], *, version: str = "2.1", inventory: dict | None = None) -> dict:
    result = {
        "version": version,
        "target_language": {"name": "French", "code": "fr"},
        "base_language": {"name": "English", "code": "en"},
        "deck_name": "French",
        "cards": cards,
    }
    if inventory is not None:
        result["source_inventory"] = inventory
    return result


def check(tmp_path: Path, cards: list[dict], *, version: str = "2.1",
          inventory: dict | None = None) -> list[str]:
    return validate_plan(plan(cards, version=version, inventory=inventory),
                         tmp_path / "plan.json", check_media=False)


def touch_sources(tmp_path: Path, *filenames: str) -> Path:
    folder = tmp_path / "input_audio"
    folder.mkdir()
    for index, name in enumerate(filenames):
        p = folder / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(f"recording {index}".encode())
    return folder


def item(key: str, file: str, *, cards: list[str] | None = None,
         reason: str = "") -> dict:
    return (
        {"id": key, "file": file, "status": "selected", "card_ids": cards}
        if cards is not None else
        {"id": key, "file": file, "status": "skipped", "reason": reason}
    )


def reading(card_id: str, focus: str, source_id: str) -> dict:
    return {"id": card_id, "skill": "reading", "target_text": focus,
            "base_text": "Meaning", "source_item_id": source_id}


def test_production_rejected_in_new_plan_but_legacy_is_compatible(tmp_path: Path) -> None:
    old_card = {"id": "old", "skill": "production",
                "target_text": "Bonjour !", "prompt": "Say hello"}
    assert any("Production is retired" in e for e in check(tmp_path, [old_card]))
    assert check(tmp_path, [old_card], version="2.0") == []


def test_all_original_audio_files_must_be_accounted_for(tmp_path: Path) -> None:
    touch_sources(tmp_path, "audio_1.mp3", "audio_2.mp3", "audio_3.mp3")
    inventory = {"audio_root": "input_audio", "items": [
        item("01", "audio_1.mp3", cards=["read1"]),
        item("02", "audio_2.mp3", reason="Duplicate easy greeting."),
    ]}
    errs = check(tmp_path, [reading("read1", "Vous pouvez me suivre.", "01")],
                 inventory=inventory)
    assert any("Source audio files omitted" in e and "audio_3.mp3" in e for e in errs)
    inventory["items"].append(item("03", "audio_3.mp3", reason="Already mastered."))
    assert check(tmp_path, [reading("read1", "Vous pouvez me suivre.", "01")],
                 inventory=inventory) == []


def test_long_sentence_may_yield_multiple_different_short_cards(tmp_path: Path) -> None:
    touch_sources(tmp_path, "long.wav")
    inv = {"audio_root": "input_audio", "items": [
        item("long", "long.wav", cards=["a", "b"]),
    ]}
    cards = [reading("a", "Vous pouvez me suivre", "long"),
             reading("b", "C'est à deux minutes d'ici", "long")]
    assert check(tmp_path, cards, inventory=inv) == []


def test_skipped_audio_requires_meaningful_reason_and_no_cards(tmp_path: Path) -> None:
    touch_sources(tmp_path, "a.mp3", "b.mp3")
    inv = {"audio_root": "input_audio", "items": [
        item("a", "a.mp3", cards=["one"]),
        item("b", "b.mp3", reason=""),
    ]}
    errs = check(tmp_path, [reading("one", "Bonjour", "a")], inventory=inv)
    assert any("needs a reason" in e for e in errs)


def test_selected_audio_requires_bidirectional_card_links(tmp_path: Path) -> None:
    touch_sources(tmp_path, "lesson.mp3")
    inv = {"audio_root": "input_audio", "items": [
        item("a", "lesson.mp3", cards=["first"]),
    ]}
    errors = check(tmp_path, [reading("first", "Bonjour", "wrong")], inventory=inv)
    assert any("must set source_item_id" in e for e in errors)
    assert any("must reference a declared source_item_id" in e for e in errors)


def test_inventory_scans_zip_and_rejects_missing_original(tmp_path: Path) -> None:
    archive = tmp_path / "materials.zip"
    with zipfile.ZipFile(archive, "w") as z:
        z.writestr("audios/audio_1.mp3", b"alpha")
        z.writestr("audios/audio_2.mp3", b"beta")
        z.writestr("Screenshot.png", b"image")
    inv = {"audio_root": "materials.zip", "items": [
        item("one", "audios/audio_1.mp3", cards=["one"]),
    ]}
    errors = check(tmp_path, [reading("one", "Je suis étudiante.", "one")],
                   inventory=inv)
    assert any("audio_2.mp3" in e for e in errors)
    inv["items"].append(item("two", "audios/audio_2.mp3", reason="Already known."))
    assert check(tmp_path, [reading("one", "Je suis étudiante.", "one")],
                 inventory=inv) == []


def test_duplicate_file_rows_fail_without_forcing_extra_cards(tmp_path: Path) -> None:
    touch_sources(tmp_path, "a.mp3")
    inv = {"audio_root": "input_audio", "items": [
        item("one", "a.mp3", cards=["one"]),
        item("two", "a.mp3", reason="Same file repeated in inventory."),
    ]}
    assert any("listed more than once" in e for e in
               check(tmp_path, [reading("one", "Bonsoir", "one")], inventory=inv))


def test_no_inventory_permitted_for_text_only_material(tmp_path: Path) -> None:
    assert check(tmp_path, [{"id": "text1", "skill": "reading",
                             "target_text": "Bonsoir.", "base_text": "Good evening."}]) == []

def test_source_audio_requires_inventory_even_when_author_omits_manifest(tmp_path: Path) -> None:
    card = {"id": "clip", "skill": "listening", "target_text": "Bonjour.",
            "audio_clip": {"source": "a.mp3"}}
    assert any("source_inventory is required" in e for e in check(tmp_path, [card]))
    tts = {"id": "tts", "skill": "listening", "target_text": "Bonjour.",
           "audio_request": {"mode": "tts", "text": "Bonjour."}}
    assert check(tmp_path, [tts]) == []
