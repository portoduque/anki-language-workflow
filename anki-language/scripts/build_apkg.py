#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import html
import json
from collections import Counter
from pathlib import Path
from typing import Any

import genanki

from validate_plan import load_plan, validate_plan

SKILL_META = {
    "reading": ("01 Reading", "Reading"),
    "listening": ("02 Listening", "Listening"),
    "production": ("03 Production", "Production"),
    "pronunciation": ("04 Pronunciation & Sounds", "Pronunciation & Sounds"),
}

AUDIO_FRONT_MODES = {"minimal-pair", "sound-discrimination", "audio-to-spelling"}

FIELDS = [
    {"name": "Context"},
    {"name": "Prompt"},
    {"name": "Target"},
    {"name": "Support"},
    {"name": "Focus"},
    {"name": "Hint"},
    {"name": "Notes"},
    {"name": "IPA"},
    {"name": "FrontAudio"},
    {"name": "BackAudio"},
    {"name": "Image"},
    {"name": "Source"},
]

CSS = """
.card {
  font-family: Arial, sans-serif;
  font-size: 21px;
  text-align: left;
  color: #222;
  background: #fff;
  max-width: 760px;
  margin: 0 auto;
  line-height: 1.45;
}
.context { font-size: 13px; opacity: .65; margin-bottom: 14px; text-transform: uppercase; letter-spacing: .08em; }
.prompt { margin: 10px 0 18px; }
.target { font-size: 27px; font-weight: 600; margin: 12px 0; }
.support, .focus, .hint, .notes, .ipa, .source { margin-top: 10px; }
.label { font-size: 12px; opacity: .55; text-transform: uppercase; letter-spacing: .06em; }
img { max-width: 100%; max-height: 360px; object-fit: contain; }
hr { margin: 20px 0; }
"""


def stable_id(seed: str) -> int:
    digest = hashlib.sha256(seed.encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "big") & 0x7FFFFFFFFFFFFFFF


def clean(value: Any) -> str:
    if value is None:
        return ""
    return html.escape(str(value), quote=False).replace("\n", "<br>")


def media_path(plan_dir: Path, raw: str | None) -> Path | None:
    if not raw:
        return None
    path = Path(raw)
    if not path.is_absolute():
        path = (plan_dir / path).resolve()
    return path


def sound_ref(path: Path | None) -> str:
    return f"[sound:{path.name}]" if path else ""


def image_ref(path: Path | None) -> str:
    return f'<img src="{html.escape(path.name, quote=True)}">' if path else ""


def make_model(skill: str) -> genanki.Model:
    model_id = stable_id(f"anki-language:model:{skill}")
    common_back = """
{{FrontSide}}
<hr>
{{#Target}}<div class="label">Target</div><div class="target">{{Target}}</div>{{/Target}}
{{#Support}}<div class="label">English</div><div class="support">{{Support}}</div>{{/Support}}
{{#Focus}}<div class="label">Focus</div><div class="focus">{{Focus}}</div>{{/Focus}}
{{#IPA}}<div class="label">IPA</div><div class="ipa">{{IPA}}</div>{{/IPA}}
{{#BackAudio}}<div class="back-audio">{{BackAudio}}</div>{{/BackAudio}}
{{#Image}}<div class="image">{{Image}}</div>{{/Image}}
{{#Notes}}<div class="label">Notes</div><div class="notes">{{Notes}}</div>{{/Notes}}
{{#Source}}<div class="label">Source</div><div class="source">{{Source}}</div>{{/Source}}
"""

    if skill == "reading":
        front = """
<div class="context">{{Context}}</div>
<div class="target">{{Target}}</div>
{{#Prompt}}<div class="prompt">{{Prompt}}</div>{{/Prompt}}
{{#FrontAudio}}<div>{{FrontAudio}}</div>{{/FrontAudio}}
"""
    elif skill == "listening":
        front = """
<div class="context">{{Context}}</div>
{{#Prompt}}<div class="prompt">{{Prompt}}</div>{{/Prompt}}
<div>{{FrontAudio}}</div>
"""
    elif skill == "production":
        front = """
<div class="context">{{Context}}</div>
<div class="prompt">{{Prompt}}</div>
{{#Hint}}<div class="label">Hint</div><div class="hint">{{Hint}}</div>{{/Hint}}
{{#Image}}<div class="image">{{Image}}</div>{{/Image}}
"""
        common_back = common_back.replace('{{#Image}}<div class="image">{{Image}}</div>{{/Image}}', "")
    else:
        # Do not render Target directly on the pronunciation front. For
        # sound-discrimination/minimal-pair cards that would reveal the answer.
        # Standard pronunciation cards put the written target inside Prompt.
        front = """
<div class="context">{{Context}}</div>
{{#Prompt}}<div class="prompt">{{Prompt}}</div>{{/Prompt}}
{{#Hint}}<div class="label">Hint</div><div class="hint">{{Hint}}</div>{{/Hint}}
{{#FrontAudio}}<div>{{FrontAudio}}</div>{{/FrontAudio}}
"""

    return genanki.Model(
        model_id,
        f"Anki Language — {SKILL_META[skill][1]}",
        fields=FIELDS,
        templates=[{"name": "Card 1", "qfmt": front, "afmt": common_back}],
        css=CSS,
    )


def normalize_tags(tags: list[Any] | None) -> list[str]:
    if not tags:
        return []
    result = []
    for tag in tags:
        normalized = str(tag).strip().replace(" ", "_")
        if normalized:
            result.append(normalized)
    return sorted(set(result))


def build(plan_path: Path, output_path: Path) -> dict[str, Any]:
    plan = load_plan(plan_path)
    errors = validate_plan(plan, plan_path, check_media=True)
    if errors:
        raise ValueError("Plan validation failed:\n- " + "\n- ".join(errors))

    cards = plan.get("cards", [])
    if not cards:
        raise ValueError("No cards were selected. Refusing to create an empty APKG.")

    plan_dir = plan_path.resolve().parent
    deck_name = str(plan["deck_name"]).strip()
    models = {skill: make_model(skill) for skill in SKILL_META}
    decks: dict[str, genanki.Deck] = {}
    media_files: dict[str, Path] = {}
    counts: Counter[str] = Counter()

    for card in cards:
        skill = card["skill"]
        subdeck, context = SKILL_META[skill]
        full_deck_name = f"{deck_name}::{subdeck}"
        if skill not in decks:
            decks[skill] = genanki.Deck(
                stable_id(f"anki-language:deck:{deck_name}:{skill}"),
                full_deck_name,
            )

        audio = media_path(plan_dir, card.get("audio"))
        image = media_path(plan_dir, card.get("image"))
        if audio:
            media_files[audio.name] = audio
        if image:
            media_files[image.name] = image

        mode = str(card.get("mode", "standard")).strip().lower()
        audio_on_front = skill == "listening" or (
            skill == "pronunciation" and mode in AUDIO_FRONT_MODES
        )

        prompt = str(card.get("prompt", "")).strip()
        if skill == "listening" and not prompt:
            prompt = "What did you hear and understand?"
        if skill == "pronunciation" and not prompt:
            if audio_on_front:
                prompt = "Which sound or word did you hear?"
            else:
                prompt = f"Pronounce this aloud: {card['target_text']}"

        fields = [
            clean(context),
            clean(prompt),
            clean(card.get("target_text", "")),
            clean(card.get("support_text", "")),
            clean(card.get("focus", "")),
            clean(card.get("hint", "")),
            clean(card.get("notes", "")),
            clean(card.get("ipa", "")),
            sound_ref(audio) if audio_on_front else "",
            sound_ref(audio) if audio and not audio_on_front else "",
            image_ref(image),
            clean(card.get("source", "")),
        ]

        guid = genanki.guid_for(
            deck_name,
            str(card["id"]),
            skill,
            str(card.get("target_text", "")),
        )
        note = genanki.Note(
            model=models[skill],
            fields=fields,
            tags=normalize_tags(card.get("tags")),
            guid=guid,
        )
        decks[skill].add_note(note)
        counts[skill] += 1

    package = genanki.Package(list(decks.values()))
    package.media_files = [str(path) for path in sorted(media_files.values(), key=lambda p: p.name)]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    package.write_to_file(str(output_path))

    report = {
        "version": plan.get("version"),
        "target_language": plan.get("target_language"),
        "support_language": plan.get("support_language"),
        "deck_name": deck_name,
        "cards_total": len(cards),
        "cards_by_skill": dict(sorted(counts.items())),
        "media_total": len(media_files),
        "skipped_total": len(plan.get("skipped", [])),
        "output": str(output_path.resolve()),
    }
    report_path = Path(str(output_path) + ".report.json")
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Build an Anki APKG from a validated card plan.")
    parser.add_argument("plan", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    try:
        report = build(args.plan, args.output)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}")
        return 1

    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
