from __future__ import annotations

import base64
import json
import sys
import wave
from pathlib import Path

import pytest
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "anki-language"
sys.path.insert(0, str(SKILL / "scripts"))

import deliver_live as live_module  # noqa: E402
import media_enrich as enrich_module  # noqa: E402
from deliver_live import verify_uploaded_media  # noqa: E402
from media_enrich import enrich_plan  # noqa: E402
from media_validate import MediaValidationError, validate_media_file  # noqa: E402
from validate_plan import load_plan, validate_plan  # noqa: E402


def write_wav(path: Path) -> None:
    with wave.open(str(path), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(16000)
        wav.writeframes(b"\x00\x00" * 3200)


def write_png(path: Path) -> None:
    Image.new("RGB", (64, 64), (240, 240, 240)).save(path, "PNG")


def test_audio_and_image_validation_are_real_decodes(tmp_path: Path) -> None:
    audio = tmp_path / "ok.wav"
    image = tmp_path / "ok.png"
    write_wav(audio)
    write_png(image)

    audio_result = validate_media_file(audio, "audio")
    image_result = validate_media_file(image, "image")

    assert audio_result["status"] == "valid"
    assert audio_result["duration_seconds"] > 0
    assert len(audio_result["sha256"]) == 64
    assert image_result["status"] == "valid"
    assert image_result["width"] == 64
    assert image_result["height"] == 64


def test_invalid_media_is_rejected_before_build_or_upload(tmp_path: Path) -> None:
    bad_audio = tmp_path / "bad.mp3"
    bad_image = tmp_path / "bad.png"
    bad_audio.write_bytes(b"not-an-audio-file" * 20)
    bad_image.write_bytes(b"not-an-image-file" * 20)

    with pytest.raises(MediaValidationError):
        validate_media_file(bad_audio, "audio")
    with pytest.raises(MediaValidationError):
        validate_media_file(bad_image, "image")


def test_enricher_validates_existing_media_and_records_hashes(tmp_path: Path) -> None:
    audio = tmp_path / "phrase.wav"
    image = tmp_path / "thing.png"
    write_wav(audio)
    write_png(image)

    plan = {
        "version": "2.0",
        "target_language": {"name": "French", "code": "fr"},
        "base_language": {"name": "English", "code": "en"},
        "deck_name": "French",
        "cards": [{
            "id": "card-1",
            "skill": "production",
            "prompt": "Say it.",
            "target_text": "Bonjour",
            "audio": "phrase.wav",
            "image": "thing.png",
        }],
    }
    plan_path = tmp_path / "plan.json"
    resolved = tmp_path / "resolved.json"
    plan_path.write_text(json.dumps(plan), encoding="utf-8")

    report = enrich_plan(plan_path, resolved)
    data = json.loads(resolved.read_text(encoding="utf-8"))
    validation = data["cards"][0]["media_validation"]

    assert report["media_validated"] == 2
    assert validation["audio"]["status"] == "valid"
    assert validation["image"]["status"] == "valid"
    assert len(validation["audio"]["sha256"]) == 64
    assert len(validation["image"]["sha256"]) == 64

    errors = validate_plan(load_plan(resolved), resolved, check_media=True)
    assert errors == []


def test_plan_rejects_media_changed_after_recorded_validation(tmp_path: Path) -> None:
    audio = tmp_path / "phrase.wav"
    write_wav(audio)
    plan = {
        "version": "2.0",
        "target_language": {"name": "French", "code": "fr"},
        "base_language": {"name": "English", "code": "en"},
        "deck_name": "French",
        "cards": [{
            "id": "listen-1",
            "skill": "listening",
            "target_text": "Bonjour",
            "audio": "phrase.wav",
        }],
    }
    source = tmp_path / "plan.json"
    resolved = tmp_path / "resolved.json"
    source.write_text(json.dumps(plan), encoding="utf-8")
    enrich_plan(source, resolved)

    write_wav(audio)
    with audio.open("ab") as handle:
        handle.write(b"changed")

    errors = validate_plan(load_plan(resolved), resolved, check_media=True)
    assert any("changed after validation" in error for error in errors)


class FakeClient:
    def __init__(self, payload: bytes):
        self.payload = payload

    def invoke(self, action, params=None):
        assert action == "retrieveMediaFile"
        return base64.b64encode(self.payload).decode("ascii")


def test_live_media_verification_compares_uploaded_bytes(tmp_path: Path) -> None:
    audio = tmp_path / "phrase.wav"
    write_wav(audio)
    result = verify_uploaded_media(FakeClient(audio.read_bytes()), audio)
    assert result["verified"] is True
    assert result["bytes"] == audio.stat().st_size


def test_live_media_verification_rejects_remote_mismatch(tmp_path: Path) -> None:
    audio = tmp_path / "phrase.wav"
    write_wav(audio)
    with pytest.raises(Exception, match="hash mismatch"):
        verify_uploaded_media(FakeClient(b"different"), audio)


def test_unresolved_listening_audio_request_is_plannable_but_not_deliverable(tmp_path: Path) -> None:
    plan = {
        "version": "2.0",
        "target_language": {"name": "French", "code": "fr"},
        "base_language": {"name": "English", "code": "en"},
        "deck_name": "French",
        "cards": [{
            "id": "listen-auto",
            "skill": "listening",
            "target_text": "Bonjour",
            "audio_request": {"mode": "auto", "text": "Bonjour", "provider": "piper"},
        }],
    }
    path = tmp_path / "plan.json"
    path.write_text(json.dumps(plan), encoding="utf-8")
    assert validate_plan(load_plan(path), path, check_media=False) == []
    errors = validate_plan(load_plan(path), path, check_media=True)
    assert any("after media enrichment" in error for error in errors)


def test_optional_image_failure_is_recorded_and_skipped(tmp_path: Path, monkeypatch) -> None:
    plan = {
        "version": "2.0",
        "target_language": {"name": "French", "code": "fr"},
        "base_language": {"name": "English", "code": "en"},
        "deck_name": "French",
        "cards": [{
            "id": "read-image",
            "skill": "reading",
            "target_text": "écureuil",
            "image_request": {"mode": "auto", "query": "squirrel", "provider": "openverse"},
        }],
    }
    source = tmp_path / "plan.json"
    resolved = tmp_path / "resolved.json"
    source.write_text(json.dumps(plan, ensure_ascii=False), encoding="utf-8")

    def fail(*args, **kwargs):
        raise RuntimeError("provider unavailable")

    monkeypatch.setattr(enrich_module, "fetch_image", fail)
    report = enrich_plan(source, resolved)
    data = json.loads(resolved.read_text(encoding="utf-8"))

    assert report["media_skipped"] == 1
    assert "image" not in data["cards"][0]
    assert data["cards"][0]["media_issues"][0]["kind"] == "image"


class LiveFakeClient:
    def __init__(self):
        self.models = {}
        self.notes = {}
        self.media = {}
        self.next_id = 1000

    def verify_actions(self, required):
        return {"api_version": 6, "actions": sorted(required)}

    def invoke(self, action, params=None):
        params = params or {}
        if action == "deckNames":
            return []
        if action == "createDeck":
            return 1
        if action == "modelNames":
            return list(self.models)
        if action == "createModel":
            self.models[params["modelName"]] = {
                "fields": list(params["inOrderFields"]),
                "templates": {
                    item["Name"]: {"Front": item["Front"], "Back": item["Back"]}
                    for item in params["cardTemplates"]
                },
                "css": params.get("css", ""),
            }
            return {"id": 1}
        if action == "modelFieldNames":
            return self.models[params["modelName"]]["fields"]
        if action == "modelTemplates":
            return self.models[params["modelName"]]["templates"]
        if action == "modelStyling":
            return {"css": self.models[params["modelName"]]["css"]}
        if action == "findNotes":
            query = str(params.get("query", ""))
            tag = ""
            deck = None
            for part in query.split():
                if part.startswith("tag:"):
                    tag = part[4:]
            marker = 'deck:"'
            if marker in query:
                deck = query.split(marker, 1)[1].split('"', 1)[0]
            return [
                note_id
                for note_id, note in self.notes.items()
                if (not tag or tag in note.get("tags", []))
                and (deck is None or note.get("deckName") == deck)
            ]
        if action == "canAddNotesWithErrorDetail":
            return [{"canAdd": True, "error": None} for _ in params["notes"]]
        if action == "addNotes":
            ids = []
            for note in params["notes"]:
                note_id = self.next_id
                self.next_id += 1
                fields = {name: {"value": value} for name, value in note["fields"].items()}
                for media_key, markup in (("audio", "[sound:{name}]"), ("picture", '<img src="{name}">')):
                    for item in note.get(media_key, []):
                        path = Path(item["path"])
                        self.media[item["filename"]] = path.read_bytes()
                        for field in item["fields"]:
                            fields[field]["value"] += markup.format(name=item["filename"])
                self.notes[note_id] = {
                    "noteId": note_id,
                    "modelName": note["modelName"],
                    "deckName": note["deckName"],
                    "tags": list(note.get("tags", [])),
                    "fields": fields,
                }
                ids.append(note_id)
            return ids
        if action == "notesInfo":
            return [self.notes[note_id] for note_id in params["notes"]]
        if action == "retrieveMediaFile":
            return base64.b64encode(self.media[params["filename"]]).decode("ascii")
        raise AssertionError(f"Unexpected action: {action}")


def test_live_delivery_prevalidates_and_postvalidates_media(tmp_path: Path, monkeypatch) -> None:
    audio = tmp_path / "phrase.wav"
    image = tmp_path / "thing.png"
    write_wav(audio)
    write_png(image)

    plan = {
        "version": "2.0",
        "target_language": {"name": "French", "code": "fr"},
        "base_language": {"name": "English", "code": "en"},
        "deck_name": "French",
        "delivery": {"mode": "live"},
        "cards": [{
            "id": "live-1",
            "skill": "production",
            "prompt": "Say hello.",
            "target_text": "Bonjour",
            "reading": "bon-ZHOOR",
            "variant": "bonjour",
            "grammar": "greeting / interjection",
            "audio": "phrase.wav",
            "image": "thing.png",
        }],
    }
    source = tmp_path / "plan.json"
    resolved = tmp_path / "resolved.json"
    source.write_text(json.dumps(plan), encoding="utf-8")
    enrich_plan(source, resolved)

    fake = LiveFakeClient()
    monkeypatch.setattr(live_module, "AnkiConnectClient", lambda endpoint, api_key: fake)
    report = live_module.deliver_live(resolved)

    assert report["created"] == 1
    assert len(report["media_verified"]) == 2
    assert all(item["verified"] is True for item in report["media_verified"])

    note = fake.notes[report["note_ids"][0]]
    assert note["fields"]["Reading"]["value"] == "bon-ZHOOR"
    assert note["fields"]["Variant"]["value"] == "bonjour"
    assert note["fields"]["Grammar"]["value"] == "greeting / interjection"


def write_simple_live_plan(path: Path, *, deck: str = "French", target: str = "Bonjour") -> None:
    plan = {
        "version": "2.0",
        "target_language": {"name": "French", "code": "fr"},
        "base_language": {"name": "English", "code": "en"},
        "deck_name": deck,
        "delivery": {"mode": "live"},
        "cards": [{
            "id": "stable-card-1",
            "skill": "production",
            "prompt": "Say hello.",
            "target_text": target,
        }],
    }
    path.write_text(json.dumps(plan), encoding="utf-8")


def test_live_delivery_is_idempotent_only_after_content_verification(tmp_path: Path, monkeypatch) -> None:
    source = tmp_path / "plan.json"
    write_simple_live_plan(source)

    fake = LiveFakeClient()
    monkeypatch.setattr(live_module, "AnkiConnectClient", lambda endpoint, api_key: fake)

    first = live_module.deliver_live(source)
    second = live_module.deliver_live(source)

    assert first["created"] == 1
    assert second["created"] == 0
    assert second["skipped_existing"] == ["stable-card-1"]
    assert len(fake.notes) == 1


def test_live_delivery_rejects_existing_card_drift(tmp_path: Path, monkeypatch) -> None:
    source = tmp_path / "plan.json"
    write_simple_live_plan(source)

    fake = LiveFakeClient()
    monkeypatch.setattr(live_module, "AnkiConnectClient", lambda endpoint, api_key: fake)
    live_module.deliver_live(source)

    write_simple_live_plan(source, target="Salut")
    with pytest.raises(Exception, match="Existing workflow note drift"):
        live_module.deliver_live(source)

    assert len(fake.notes) == 1


def test_live_identity_is_scoped_by_deck_and_language(tmp_path: Path, monkeypatch) -> None:
    first_path = tmp_path / "general.json"
    second_path = tmp_path / "work.json"
    write_simple_live_plan(first_path, deck="French")
    write_simple_live_plan(second_path, deck="French Work")

    fake = LiveFakeClient()
    monkeypatch.setattr(live_module, "AnkiConnectClient", lambda endpoint, api_key: fake)

    first = live_module.deliver_live(first_path)
    second = live_module.deliver_live(second_path)

    assert first["created"] == 1
    assert second["created"] == 1
    assert len(fake.notes) == 2


def test_live_delivery_detects_current_model_css_drift(tmp_path: Path, monkeypatch) -> None:
    source = tmp_path / "plan.json"
    write_simple_live_plan(source)

    fake = LiveFakeClient()
    monkeypatch.setattr(live_module, "AnkiConnectClient", lambda endpoint, api_key: fake)
    live_module.deliver_live(source)

    model_name = "Anki Language v4 — Production"
    fake.models[model_name]["css"] += "\n.card { border: 1px solid red; }"

    with pytest.raises(Exception, match="CSS drift"):
        live_module.deliver_live(source)


def test_live_delivery_recognizes_legacy_identity_without_migrating_it(tmp_path: Path, monkeypatch) -> None:
    source = tmp_path / "plan.json"
    write_simple_live_plan(source)
    plan = json.loads(source.read_text(encoding="utf-8"))
    card = plan["cards"][0]

    fake = LiveFakeClient()
    expected_note, _ = live_module.build_note(plan, card, tmp_path)
    fields = {
        name: {"value": value}
        for name, value in live_module.expected_persisted_fields(expected_note).items()
    }
    fake.notes[900] = {
        "noteId": 900,
        "modelName": "Anki Language v3 — Production",
        "deckName": expected_note["deckName"],
        "tags": ["anki-language", live_module.legacy_workflow_tag(card["id"])],
        "fields": fields,
    }

    monkeypatch.setattr(live_module, "AnkiConnectClient", lambda endpoint, api_key: fake)
    report = live_module.deliver_live(source)

    assert report["created"] == 0
    assert report["skipped_existing"] == ["stable-card-1"]
    assert report["legacy_existing_verified"] == ["stable-card-1"]
    assert len(fake.notes) == 1
