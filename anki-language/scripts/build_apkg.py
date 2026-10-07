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

from card_contract import AUDIO_FRONT_MODES, SKILL_META, normalize_mode, workflow_system_tags
from validate_plan import load_plan, validate_plan

MODEL_VERSION = 4

FIELDS = [
    {"name": "Context"},
    {"name": "Prompt"},
    {"name": "TargetLanguage"},
    {"name": "Target"},
    {"name": "BaseLanguage"},
    {"name": "Base"},
    {"name": "Focus"},
    {"name": "Hint"},
    {"name": "Notes"},
    {"name": "IPA"},
    {"name": "Reading"},
    {"name": "Variant"},
    {"name": "Grammar"},
    {"name": "FrontAudio"},
    {"name": "BackAudio"},
    {"name": "Image"},
    {"name": "Source"},
]

CSS = """
.card {
  box-sizing: border-box;
  font-family: Arial, sans-serif;
  font-size: 21px;
  text-align: start;
  color: #222;
  background: #fff;
  max-width: 760px;
  margin: 0 auto;
  padding: 24px 18px;
  line-height: 1.45;
  overflow-wrap: anywhere;
}
.context { font-size: 13px; opacity: .65; margin-bottom: 14px; text-transform: uppercase; letter-spacing: .08em; }
.prompt { margin: 10px 0 18px; }
.target { font-size: 27px; font-weight: 600; margin: 12px 0; }
.support, .focus, .hint, .notes, .ipa, .reading, .variant, .grammar, .source { margin-top: 10px; }
.label { font-size: 12px; opacity: .55; text-transform: uppercase; letter-spacing: .06em; }
img { display: block; max-width: 100%; max-height: 360px; object-fit: contain; margin: 12px auto 0; }
hr { margin: 20px 0; border: 0; border-top: 1px solid #d8d8d8; }

.card.nightMode {
  color: #f2f3f5;
  background: #1f2125;
}
.nightMode .label,
.nightMode .context,
.nightMode .source {
  color: #b5bac1;
}
.nightMode hr {
  border-top-color: #454a50;
}

@media (max-width: 480px) {
  .card {
    font-size: 20px;
    padding: 18px 12px;
  }
  .target {
    font-size: 25px;
  }
}
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
    model_id = stable_id(f"anki-language:model:v{MODEL_VERSION}:{skill}")
    common_back = """
{{FrontSide}}
<hr id="answer">
{{#Target}}<div class="label">{{TargetLanguage}}</div><div class="target" dir="auto">{{Target}}</div>{{/Target}}
{{#Base}}<div class="label">{{BaseLanguage}}</div><div class="support" dir="auto">{{Base}}</div>{{/Base}}
{{#Focus}}<div class="label">Focus</div><div class="focus" dir="auto">{{Focus}}</div>{{/Focus}}
{{#IPA}}<div class="label">IPA</div><div class="ipa" dir="auto">{{IPA}}</div>{{/IPA}}
{{#Reading}}<div class="label">Reading</div><div class="reading" dir="auto">{{Reading}}</div>{{/Reading}}
{{#Variant}}<div class="label">Variant</div><div class="variant" dir="auto">{{Variant}}</div>{{/Variant}}
{{#Grammar}}<div class="label">Grammar</div><div class="grammar" dir="auto">{{Grammar}}</div>{{/Grammar}}
{{#BackAudio}}<div class="back-audio">{{BackAudio}}</div>{{/BackAudio}}
{{#Image}}<div class="image">{{Image}}</div>{{/Image}}
{{#Notes}}<div class="label">Notes</div><div class="notes" dir="auto">{{Notes}}</div>{{/Notes}}
{{#Source}}<div class="label">Source</div><div class="source" dir="auto">{{Source}}</div>{{/Source}}
"""

    if skill == "reading":
        front = """
<div class="context" dir="auto">{{Context}}</div>
<div class="target" dir="auto">{{Target}}</div>
{{#Prompt}}<div class="prompt" dir="auto">{{Prompt}}</div>{{/Prompt}}
{{#FrontAudio}}<div>{{FrontAudio}}</div>{{/FrontAudio}}
"""
    elif skill == "listening":
        front = """
<div class="context" dir="auto">{{Context}}</div>
{{#Prompt}}<div class="prompt" dir="auto">{{Prompt}}</div>{{/Prompt}}
<div>{{FrontAudio}}</div>
"""
    elif skill == "production":
        front = """
<div class="context" dir="auto">{{Context}}</div>
<div class="prompt" dir="auto">{{Prompt}}</div>
{{#Hint}}<div class="label">Hint</div><div class="hint" dir="auto">{{Hint}}</div>{{/Hint}}
{{#Image}}<div class="image">{{Image}}</div>{{/Image}}
"""
        common_back = common_back.replace('{{#Image}}<div class="image">{{Image}}</div>{{/Image}}', "")
    else:
        # Do not render Target directly on the pronunciation front. For
        # sound-discrimination/minimal-pair cards that would reveal the answer.
        # Standard pronunciation cards put the written target inside Prompt.
        front = """
<div class="context" dir="auto">{{Context}}</div>
{{#Prompt}}<div class="prompt" dir="auto">{{Prompt}}</div>{{/Prompt}}
{{#Hint}}<div class="label">Hint</div><div class="hint" dir="auto">{{Hint}}</div>{{/Hint}}
{{#FrontAudio}}<div>{{FrontAudio}}</div>{{/FrontAudio}}
"""

    return genanki.Model(
        model_id,
        f"Anki Language v{MODEL_VERSION} — {SKILL_META[skill][1]}",
        fields=FIELDS,
        templates=[{"name": "Card 1", "qfmt": front, "afmt": common_back}],
        css=CSS,
    )


def card_context(target_language_name: str, skill: str) -> str:
    return f"{target_language_name} — {SKILL_META[skill][1]}"


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
        subdeck, _ = SKILL_META[skill]
        context = card_context(str(plan["target_language"]["name"]), skill)
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

        mode = normalize_mode(card)
        audio_on_front = skill == "listening" or (
            skill == "pronunciation" and mode in AUDIO_FRONT_MODES
        )

        prompt = str(card.get("prompt", "")).strip()

        fields = [
            clean(context),
            clean(prompt),
            clean(plan["target_language"]["name"]),
            clean(card.get("target_text", "")),
            clean(plan["base_language"]["name"]),
            clean(card.get("base_text", "")),
            clean(card.get("focus", "")),
            clean(card.get("hint", "")),
            clean(card.get("notes", "")),
            clean(card.get("ipa", "")),
            clean(card.get("reading", "")),
            clean(card.get("variant", "")),
            clean(card.get("grammar", "")),
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
        system_tags = workflow_system_tags(
            deck_name,
            str(plan["target_language"]["code"]),
            str(card["id"]),
        )
        note = genanki.Note(
            model=models[skill],
            fields=fields,
            tags=normalize_tags([*(card.get("tags") or []), *system_tags]),
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
        "base_language": plan.get("base_language"),
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
