#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
from pathlib import Path
from typing import Any

from ankiconnect_client import AnkiConnectClient, AnkiConnectError
from build_apkg import CSS, card_context, clean, fields_for_skill, make_model, normalize_tags
from card_contract import (
    AUDIO_FRONT_MODES,
    SKILL_META,
    full_deck_name,
    legacy_workflow_tag,
    normalize_mode,
    pronunciation_front_cue,
    workflow_system_tags,
    workflow_tag,
    writing_parts,
    card_source_footer,
)
from media_validate import MediaValidationError, sha256_file, validate_media_file
from validate_plan import load_plan, validate_plan, normalized_utterance


REQUIRED_ACTIONS = {
    "version", "apiReflect", "deckNames", "createDeck", "modelNames",
    "modelFieldNames", "modelTemplates", "modelStyling", "createModel",
    "findNotes", "canAddNotesWithErrorDetail", "addNotes", "notesInfo",
    "retrieveMediaFile",
}


def media_path(plan_dir: Path, raw: str | None) -> Path | None:
    if not raw:
        return None
    path = Path(raw)
    return path.resolve() if path.is_absolute() else (plan_dir / path).resolve()


def model_payload(skill: str) -> dict[str, Any]:
    model = make_model(skill)
    template = model.templates[0]
    return {
        "modelName": model.name,
        "inOrderFields": [field["name"] for field in fields_for_skill(skill)],
        "css": model.css,
        "isCloze": False,
        "cardTemplates": [{
            "Name": template["name"],
            "Front": template["qfmt"],
            "Back": template["afmt"],
        }],
    }


def normalize_markup(value: Any) -> str:
    return str(value or "").replace("\r\n", "\n").strip()


def normalize_template_map(raw: Any) -> dict[str, dict[str, str]]:
    if not isinstance(raw, dict):
        return {}
    result: dict[str, dict[str, str]] = {}
    for name, template in raw.items():
        if not isinstance(template, dict):
            continue
        result[str(name)] = {
            "Front": normalize_markup(template.get("Front", template.get("qfmt", ""))),
            "Back": normalize_markup(template.get("Back", template.get("afmt", ""))),
        }
    return result


def expected_template_map(skill: str) -> dict[str, dict[str, str]]:
    template = make_model(skill).templates[0]
    return {
        str(template["name"]): {
            "Front": normalize_markup(template["qfmt"]),
            "Back": normalize_markup(template["afmt"]),
        }
    }


def ensure_models(client: AnkiConnectClient, skills: set[str]) -> None:
    existing = set(client.invoke("modelNames") or [])
    for skill in sorted(skills):
        expected_fields = [field["name"] for field in fields_for_skill(skill)]
        model = make_model(skill)
        if model.name not in existing:
            client.invoke("createModel", model_payload(skill))
            existing.add(model.name)

        actual_fields = client.invoke("modelFieldNames", {"modelName": model.name})
        if list(actual_fields or []) != expected_fields:
            raise AnkiConnectError(
                f"Existing model '{model.name}' has incompatible fields. "
                f"Expected {expected_fields}, got {actual_fields}."
            )

        actual_templates = normalize_template_map(
            client.invoke("modelTemplates", {"modelName": model.name})
        )
        expected_templates = expected_template_map(skill)
        if actual_templates != expected_templates:
            raise AnkiConnectError(
                f"Existing model '{model.name}' has template drift. "
                "The workflow will not overwrite user/customized templates automatically."
            )

        styling = client.invoke("modelStyling", {"modelName": model.name})
        actual_css = (
            styling.get("css", styling.get("CSS", ""))
            if isinstance(styling, dict)
            else styling
        )
        if normalize_markup(actual_css) != normalize_markup(model.css):
            raise AnkiConnectError(
                f"Existing model '{model.name}' has CSS drift. "
                "The workflow will not overwrite user/customized styling automatically."
            )


def ensure_decks(client: AnkiConnectClient, plan: dict[str, Any]) -> None:
    existing = set(client.invoke("deckNames") or [])
    parent = str(plan["deck_name"])
    needed = {parent}
    for card in plan["cards"]:
        needed.add(f"{parent}::{SKILL_META[card['skill']][0]}")
    for deck in sorted(needed):
        if deck not in existing:
            client.invoke("createDeck", {"deck": deck})


def note_fields(plan: dict[str, Any], card: dict[str, Any]) -> dict[str, str]:
    skill = card["skill"]
    fields = {
        "Context": clean(card_context(str(plan["target_language"]["name"]), skill)),
        "Prompt": clean(card.get("prompt", "")),
        "TargetLanguage": clean(plan["target_language"]["name"]),
        "Target": clean(card.get("target_text", "")),
        "BaseLanguage": clean(plan["base_language"]["name"]),
        "Base": clean(card.get("base_text", "")),
        "Focus": clean(card.get("focus", "")),
        "Hint": clean(card.get("hint", "")),
        "Notes": clean(card.get("notes", "")),
        "IPA": clean(card.get("ipa", "")),
        "Reading": clean(card.get("reading", "")),
        "Variant": clean(card.get("variant", "")),
        "Grammar": clean(card.get("grammar", "")),
        "FrontAudio": "",
        "BackAudio": "",
        "Image": "",
        "Source": clean(card_source_footer(plan, card)),
    }
    if skill == "pronunciation":
        fields["FrontCue"] = clean(pronunciation_front_cue(card))
    if skill == "writing":
        before, answer, after = writing_parts(card)
        fields["WritingBefore"] = clean(before)
        fields["WritingAfter"] = clean(after)
        fields["WritingAnswer"] = clean(answer)
    return fields


def build_note(plan: dict[str, Any], card: dict[str, Any], plan_dir: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    skill = card["skill"]
    model = make_model(skill)
    fields = note_fields(plan, card)
    note: dict[str, Any] = {
        "deckName": full_deck_name(str(plan["deck_name"]), skill),
        "modelName": model.name,
        "fields": fields,
        "options": {"allowDuplicate": True},
        "tags": normalize_tags([
            *(card.get("tags") or []),
            *workflow_system_tags(
                str(plan["deck_name"]),
                str(plan["target_language"]["code"]),
                skill,
                str(card["id"]),
            ),
        ]),
    }

    media: dict[str, Path] = {}
    audio = media_path(plan_dir, card.get("audio"))
    image = media_path(plan_dir, card.get("image"))
    mode = normalize_mode(card)
    audio_on_front = skill == "listening" or (skill == "pronunciation" and mode in AUDIO_FRONT_MODES)

    if audio is not None:
        validate_media_file(audio, "audio")
        field = "FrontAudio" if audio_on_front else "BackAudio"
        note["audio"] = [{"path": str(audio), "filename": audio.name, "fields": [field]}]
        media[f"audio:{field}"] = audio
    if image is not None:
        validate_media_file(image, "image")
        note["picture"] = [{"path": str(image), "filename": image.name, "fields": ["Image"]}]
        media["image:Image"] = image

    return note, media


def field_value(note_info: dict[str, Any], field: str) -> str:
    raw = (note_info.get("fields") or {}).get(field, "")
    if isinstance(raw, dict):
        return str(raw.get("value", ""))
    return str(raw)


def expected_persisted_fields(note: dict[str, Any]) -> dict[str, str]:
    fields = dict(note["fields"])
    for item in note.get("audio", []):
        filename = str(item["filename"])
        for field in item.get("fields", []):
            fields[str(field)] = fields.get(str(field), "") + f"[sound:{filename}]"
    for item in note.get("picture", []):
        filename = str(item["filename"])
        for field in item.get("fields", []):
            fields[str(field)] = fields.get(str(field), "") + f'<img src="{filename}">'
    return fields


def quote_anki_search(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def note_content_mismatches(
    note_info: dict[str, Any],
    expected_note: dict[str, Any],
    *,
    allow_legacy_model: bool,
) -> list[str]:
    mismatches: list[str] = []
    actual_model = str(note_info.get("modelName") or "")
    expected_model = str(expected_note["modelName"])
    if allow_legacy_model:
        if actual_model and not actual_model.startswith("Anki Language v"):
            mismatches.append(f"modelName={actual_model!r}")
    elif actual_model != expected_model:
        mismatches.append(f"modelName={actual_model!r} expected={expected_model!r}")

    for field, expected in expected_persisted_fields(expected_note).items():
        actual = field_value(note_info, field)
        if actual != expected:
            mismatches.append(f"{field}: actual={actual!r} expected={expected!r}")
    return mismatches


def find_existing_card(
    client: AnkiConnectClient,
    plan: dict[str, Any],
    card: dict[str, Any],
    expected_note: dict[str, Any],
) -> tuple[int, str] | None:
    scoped_tag = workflow_tag(
        str(plan["deck_name"]),
        str(plan["target_language"]["code"]),
        str(card["skill"]),
        str(card["id"]),
    )
    existing = client.invoke("findNotes", {"query": f"tag:{scoped_tag}"}) or []
    identity_kind = "scoped"

    if not existing:
        legacy_tag = legacy_workflow_tag(str(card["id"]))
        deck = full_deck_name(str(plan["deck_name"]), str(card["skill"]))
        query = f"tag:{legacy_tag} deck:{quote_anki_search(deck)}"
        existing = client.invoke("findNotes", {"query": query}) or []
        identity_kind = "legacy"

    if not existing:
        return None
    if len(existing) != 1:
        raise AnkiConnectError(
            f"Card {card['id']!r} matched {len(existing)} existing notes via "
            f"{identity_kind} workflow identity; refusing ambiguous live delivery."
        )

    note_id = int(existing[0])
    infos = client.invoke("notesInfo", {"notes": [note_id]}) or []
    if len(infos) != 1:
        raise AnkiConnectError(
            f"Existing note {note_id} for card {card['id']!r} could not be inspected reliably."
        )

    mismatches = note_content_mismatches(
        infos[0],
        expected_note,
        allow_legacy_model=identity_kind == "legacy",
    )
    if identity_kind == "scoped":
        actual_tags = {str(tag) for tag in (infos[0].get("tags") or [])}
        required_tags = set(workflow_system_tags(
            str(plan["deck_name"]),
            str(plan["target_language"]["code"]),
            str(card["skill"]),
            str(card["id"]),
        ))
        missing_tags = sorted(required_tags - actual_tags)
        if missing_tags:
            mismatches.append(f"missing system tags={missing_tags!r}")

    if mismatches:
        raise AnkiConnectError(
            f"Existing workflow note drift for card {card['id']!r}: "
            + "; ".join(mismatches[:6])
            + ". The workflow will not silently overwrite or skip changed content."
        )
    return note_id, identity_kind


def verify_uploaded_media(client: AnkiConnectClient, path: Path) -> dict[str, Any]:
    encoded = client.invoke("retrieveMediaFile", {"filename": path.name})
    if not encoded:
        raise AnkiConnectError(f"Uploaded media cannot be retrieved from Anki: {path.name}")
    try:
        remote = base64.b64decode(encoded)
    except Exception as exc:
        raise AnkiConnectError(f"Anki returned invalid base64 for {path.name}: {exc}") from exc
    local_hash = sha256_file(path)
    remote_hash = hashlib.sha256(remote).hexdigest()
    if remote_hash != local_hash:
        raise AnkiConnectError(
            f"Uploaded media hash mismatch for {path.name}: local={local_hash} remote={remote_hash}"
        )
    return {"filename": path.name, "sha256": local_hash, "bytes": len(remote), "verified": True}



def reject_cross_generation_duplicates(client: AnkiConnectClient, plan: dict[str, Any]) -> None:
    """Read-only: block redundant new note identities before any live writes."""
    if plan.get("version") != "2.2":
        return
    existing = client.invoke("findNotes", {"query": "tag:anki-language"}) or []
    if not existing:
        return
    prospective = {
        (card["skill"], normalized_utterance(str(card["target_text"]))): card
        for card in plan["cards"]
    }
    for start in range(0, len(existing), 100):
        infos = client.invoke("notesInfo", {"notes": existing[start:start + 100]}) or []
        for info in infos:
            fields = info.get("fields") or {}
            context = field_value(info, "Context")
            target = normalized_utterance(field_value(info, "Target"))
            if not target or not context or not context.startswith(str(plan["target_language"]["name"]) + " — "):
                continue
            skill_label = context.split(" — ", 1)[-1]
            matches = [s for s, (_, label) in SKILL_META.items() if label == skill_label]
            if not matches:
                continue
            card = prospective.get((matches[0], target))
            if card is None:
                continue
            same_identity = workflow_tag(
                str(plan["deck_name"]), str(plan["target_language"]["code"]),
                card["skill"], str(card["id"])
            )
            if same_identity in set(info.get("tags") or []):
                continue
            raise AnkiConnectError(
                f"Existing Anki note {info.get('noteId', '?')} already reviews "
                f"{card['skill']} target {card['target_text']!r} under a different identity. "
                "No new cards were created. Review the old/new notes and choose "
                "which to keep; never auto-delete or silently duplicate them."
            )

def deliver_live(
    plan_path: Path,
    endpoint: str = "http://127.0.0.1:8765",
    api_key: str | None = None,
) -> dict[str, Any]:
    plan = load_plan(plan_path)
    errors = validate_plan(plan, plan_path, check_media=True)
    if errors:
        raise ValueError("Plan validation failed before live delivery:\n- " + "\n- ".join(errors))

    client = AnkiConnectClient(endpoint, api_key)
    capabilities = client.verify_actions(REQUIRED_ACTIONS)
    reject_cross_generation_duplicates(client, plan)
    ensure_decks(client, plan)
    ensure_models(client, {card["skill"] for card in plan["cards"]})

    plan_dir = plan_path.resolve().parent
    pending_notes: list[dict[str, Any]] = []
    pending_cards: list[dict[str, Any]] = []
    pending_media: list[dict[str, Path]] = []
    skipped_existing: list[str] = []
    legacy_existing_verified: list[str] = []

    for card in plan["cards"]:
        note, media = build_note(plan, card, plan_dir)
        existing = find_existing_card(client, plan, card, note)
        if existing is not None:
            _, identity_kind = existing
            skipped_existing.append(str(card["id"]))
            if identity_kind == "legacy":
                legacy_existing_verified.append(str(card["id"]))
            continue
        pending_notes.append(note)
        pending_cards.append(card)
        pending_media.append(media)

    if not pending_notes:
        return {
            "status": "ok",
            "mode": "live",
            "created": 0,
            "skipped_existing": skipped_existing,
            "legacy_existing_verified": legacy_existing_verified,
            "capabilities": capabilities,
            "media_verified": [],
        }

    preflight = client.invoke("canAddNotesWithErrorDetail", {"notes": pending_notes})
    problems = []
    for index, result in enumerate(preflight or []):
        if not result.get("canAdd", False):
            problems.append({"card": pending_cards[index]["id"], "error": result.get("error")})
    if problems:
        raise AnkiConnectError(f"AnkiConnect preflight rejected notes: {problems}")

    note_ids = client.invoke("addNotes", {"notes": pending_notes})
    if not isinstance(note_ids, list) or len(note_ids) != len(pending_notes) or any(x is None for x in note_ids):
        raise AnkiConnectError(f"Unexpected addNotes result: {note_ids}")

    info = client.invoke("notesInfo", {"notes": note_ids})
    by_id = {int(item["noteId"]): item for item in (info or []) if item.get("noteId") is not None}
    media_verified: dict[str, dict[str, Any]] = {}

    for note_id, card, media in zip(note_ids, pending_cards, pending_media):
        note_info = by_id.get(int(note_id))
        if note_info is None:
            raise AnkiConnectError(f"Created note {note_id} was not returned by notesInfo.")
        for descriptor, path in media.items():
            _, field = descriptor.split(":", 1)
            if path.name not in field_value(note_info, field):
                raise AnkiConnectError(
                    f"Created note {note_id} field {field} does not reference uploaded media {path.name}."
                )
            if path.name not in media_verified:
                media_verified[path.name] = verify_uploaded_media(client, path)

    report = {
        "status": "ok",
        "mode": "live",
        "created": len(note_ids),
        "note_ids": note_ids,
        "skipped_existing": skipped_existing,
        "legacy_existing_verified": legacy_existing_verified,
        "capabilities": capabilities,
        "media_verified": sorted(media_verified.values(), key=lambda item: item["filename"]),
    }
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Deliver a fully resolved card plan directly into a running Anki via AnkiConnect.")
    parser.add_argument("plan", type=Path)
    parser.add_argument("--endpoint", default=os.getenv("ANKICONNECT_URL", "http://127.0.0.1:8765"))
    parser.add_argument("--api-key-env", default="ANKICONNECT_API_KEY")
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    api_key = os.getenv(args.api_key_env) or None
    try:
        report = deliver_live(args.plan, args.endpoint, api_key)
    except (OSError, ValueError, MediaValidationError, AnkiConnectError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}")
        return 1
    if args.report:
        args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
