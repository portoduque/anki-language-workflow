from __future__ import annotations

import hashlib
import re
from typing import Any

SKILL_META = {
    "reading": ("01 Reading", "Reading"),
    "listening": ("02 Listening", "Listening"),
    "production": ("03 Production", "Production"),
    "pronunciation": ("04 Pronunciation & Sounds", "Pronunciation & Sounds"),
    "writing": ("05 Writing", "Writing"),
}

SUPPORTED_MODES_BY_SKILL = {
    "reading": frozenset({"standard"}),
    "listening": frozenset({"standard"}),
    "production": frozenset({"standard"}),
    "writing": frozenset({"standard"}),
    "pronunciation": frozenset({
        "standard",
        "minimal-pair",
        "sound-discrimination",
        "spelling-sound",
        "audio-to-spelling",
    }),
}

AUDIO_FRONT_MODES = frozenset({"minimal-pair", "sound-discrimination", "audio-to-spelling"})
WRITTEN_FRONT_PRONUNCIATION_MODES = frozenset({"standard", "spelling-sound"})
AUDIO_REQUIRED_PRONUNCIATION_MODES = frozenset({
    "minimal-pair",
    "sound-discrimination",
    "spelling-sound",
    "audio-to-spelling",
})

WORKFLOW_TAG = "anki-language"


def normalize_mode(card: dict[str, Any]) -> str:
    return str(card.get("mode", "standard")).strip().lower()


def pronunciation_front_cue(card: dict[str, Any]) -> str:
    """Show the written target only when the task is to pronounce its spelling."""
    if card.get("skill") != "pronunciation":
        return ""
    if normalize_mode(card) in WRITTEN_FRONT_PRONUNCIATION_MODES:
        return str(card.get("target_text", "")).strip()
    return ""


def writing_parts(card: dict[str, Any]) -> tuple[str, str, str]:
    """Split one unique complete word/chunk out of a short source sentence.

    Keeps writing cards on the existing 1-note/1-card architecture. The AI
    selects the meaningful chunk; code only validates its exact boundaries.
    """
    target = str(card.get("target_text", ""))
    answer = str(card.get("writing_answer", ""))
    if not answer or not answer.strip() or answer != answer.strip():
        raise ValueError("writing_answer must be a nonempty single-line word/chunk without outer whitespace.")
    if any(ch in answer for ch in ("\\n", "\\r", "<", ">")):
        raise ValueError("writing_answer must be plain text on one line.")
    if not target.strip() or any(ch in target for ch in ("\\n", "\\r")):
        raise ValueError("Writing target_text must be a short, single-line sentence.")
    if target.count(answer) != 1:
        raise ValueError("writing_answer must occur exactly once in target_text.")
    before, after = target.split(answer, 1)
    if not (before.strip() or after.strip()):
        raise ValueError("Writing must test a part of the sentence, not the whole sentence.")
    if (before and re.match(r"\\w", before[-1], re.UNICODE)) or (after and re.match(r"\\w", after[0], re.UNICODE)):
        raise ValueError("writing_answer must align to word boundaries, not cut through a word.")
    return before, answer, after


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
