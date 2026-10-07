from __future__ import annotations

import hashlib
from typing import Any

SKILL_META = {
    "reading": ("01 Reading", "Reading"),
    "listening": ("02 Listening", "Listening"),
    "production": ("03 Production", "Production"),
    "pronunciation": ("04 Pronunciation & Sounds", "Pronunciation & Sounds"),
}

SUPPORTED_MODES_BY_SKILL = {
    "reading": frozenset({"standard"}),
    "listening": frozenset({"standard"}),
    "production": frozenset({"standard"}),
    "pronunciation": frozenset({
        "standard",
        "minimal-pair",
        "sound-discrimination",
        "spelling-sound",
        "audio-to-spelling",
    }),
}

AUDIO_FRONT_MODES = frozenset({"minimal-pair", "sound-discrimination", "audio-to-spelling"})
AUDIO_REQUIRED_PRONUNCIATION_MODES = frozenset({
    "minimal-pair",
    "sound-discrimination",
    "spelling-sound",
    "audio-to-spelling",
})

WORKFLOW_TAG = "anki-language"


def normalize_mode(card: dict[str, Any]) -> str:
    return str(card.get("mode", "standard")).strip().lower()


def full_deck_name(deck_name: str, skill: str) -> str:
    return f"{deck_name}::{SKILL_META[skill][0]}"


def legacy_workflow_tag(card_id: str) -> str:
    digest = hashlib.sha256(card_id.encode("utf-8")).hexdigest()[:20]
    return f"anki_language_id_{digest}"


def workflow_tag(deck_name: str, target_code: str, skill: str, card_id: str) -> str:
    identity = "\x1f".join([
        deck_name.strip(),
        target_code.strip().casefold(),
        skill.strip().casefold(),
        card_id.strip(),
    ])
    digest = hashlib.sha256(identity.encode("utf-8")).hexdigest()[:24]
    return f"anki_language_key_{digest}"


def workflow_system_tags(deck_name: str, target_code: str, skill: str, card_id: str) -> list[str]:
    return [WORKFLOW_TAG, workflow_tag(deck_name, target_code, skill, card_id)]
