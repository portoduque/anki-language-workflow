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

MODEL_VERSION = 5

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
  --page: #f4f6fb;
  --surface: #ffffff;
  --surface-soft: #f7f8fc;
  --surface-strong: #eef1f7;
  --text: #172033;
  --muted: #667085;
  --faint: #98a2b3;
  --border: #e4e7ec;
  --shadow: 0 12px 34px rgba(16, 24, 40, .08);
  --accent: #5b5bd6;
  --accent-soft: #eeeeff;
  --accent-text: #4141a6;

  box-sizing: border-box;
  margin: 0;
  padding: 24px 14px 30px;
  background: var(--page);
  color: var(--text);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
  font-size: 20px;
  line-height: 1.5;
  text-align: start;
  overflow-wrap: anywhere;
}

.card.nightMode {
  --page: #111318;
  --surface: #1b1e25;
  --surface-soft: #222630;
  --surface-strong: #2a2f3a;
  --text: #f3f5f7;
  --muted: #b7bec9;
  --faint: #8f98a7;
  --border: #333845;
  --shadow: 0 14px 34px rgba(0, 0, 0, .26);
  --accent-soft: #2b2b5f;
  --accent-text: #d8d8ff;
}

.anki-card,
.answer-shell {
  box-sizing: border-box;
  width: 100%;
  max-width: 760px;
  margin: 0 auto;
  border: 1px solid var(--border);
  border-radius: 22px;
  background: var(--surface);
  box-shadow: var(--shadow);
  overflow: hidden;
}

.anki-card::before,
.answer-shell::before {
  content: "";
  display: block;
  height: 5px;
  background: var(--accent);
}

.skill-reading {
  --accent: #5b5bd6;
  --accent-soft: #eeeeff;
  --accent-text: #4141a6;
}
.skill-listening {
  --accent: #0e9f9a;
  --accent-soft: #e7f8f6;
  --accent-text: #08736f;
}
.skill-production {
  --accent: #d97706;
  --accent-soft: #fff4df;
  --accent-text: #9a4d00;
}
.skill-pronunciation {
  --accent: #d94f70;
  --accent-soft: #fff0f4;
  --accent-text: #a92f50;
}

.nightMode .skill-reading {
  --accent: #8b8cf6;
  --accent-soft: #2b2b5f;
  --accent-text: #dedfff;
}
.nightMode .skill-listening {
  --accent: #45c6bf;
  --accent-soft: #153d3b;
  --accent-text: #c8fffb;
}
.nightMode .skill-production {
  --accent: #f1aa4b;
  --accent-soft: #4a3317;
  --accent-text: #ffe2b4;
}
.nightMode .skill-pronunciation {
  --accent: #f07d99;
  --accent-soft: #4a2330;
  --accent-text: #ffd4df;
}

.card-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  padding: 17px 22px 0;
}

.skill-chip,
.language-chip,
.answer-chip {
  display: inline-flex;
  align-items: center;
  min-width: 0;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 700;
  line-height: 1;
  letter-spacing: .045em;
}

.skill-chip {
  gap: 8px;
  padding: 9px 12px;
  background: var(--accent-soft);
  color: var(--accent-text);
  text-transform: uppercase;
}

.skill-dot {
  width: 8px;
  height: 8px;
  flex: 0 0 auto;
  border-radius: 999px;
  background: var(--accent);
}

.language-chip {
  max-width: 48%;
  padding: 9px 12px;
  background: var(--surface-soft);
  color: var(--muted);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.card-main {
  padding: 34px 28px 30px;
}

.front-stage {
  display: flex;
  min-height: 180px;
  flex-direction: column;
  justify-content: center;
  gap: 18px;
}

.stage-label,
.section-label {
  color: var(--muted);
  font-size: 11px;
  font-weight: 750;
  letter-spacing: .08em;
  text-transform: uppercase;
}

.target,
.prompt,
.answer-value,
.support-value,
.info-value,
.notes,
.source {
  unicode-bidi: plaintext;
}

.target.hero {
  margin: 0;
  color: var(--text);
  font-size: clamp(29px, 5.5vw, 42px);
  font-weight: 720;
  line-height: 1.18;
  letter-spacing: -.025em;
}

.prompt.hero {
  margin: 0;
  color: var(--text);
  font-size: clamp(25px, 4.8vw, 36px);
  font-weight: 680;
  line-height: 1.28;
  letter-spacing: -.018em;
}

.cue,
.hint-card,
.support-panel,
.info-card,
.notes-panel,
.media-panel {
  border: 1px solid var(--border);
  border-radius: 16px;
  background: var(--surface-soft);
}

.cue {
  padding: 14px 16px;
  color: var(--muted);
  font-size: 16px;
  line-height: 1.48;
}

.hint-card {
  padding: 13px 15px;
  border-inline-start: 4px solid var(--accent);
}

.hint-card .section-label {
  margin-bottom: 5px;
  color: var(--accent-text);
}

.hint {
  color: var(--muted);
  font-size: 15px;
}

.audio-stage {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 90px;
  padding: 18px;
  border: 1px solid var(--border);
  border-radius: 18px;
  background: var(--accent-soft);
}

.media-panel {
  padding: 12px;
}

.image img,
.media-panel img {
  display: block;
  width: auto;
  max-width: 100%;
  max-height: 360px;
  margin: 0 auto;
  border-radius: 13px;
  object-fit: contain;
}

.replay-button,
a.replay-button {
  display: inline-flex !important;
  align-items: center;
  justify-content: center;
  min-width: 54px;
  min-height: 54px;
  padding: 10px !important;
  border: 0 !important;
  border-radius: 17px !important;
  background: var(--accent) !important;
  box-shadow: 0 6px 16px rgba(16, 24, 40, .14);
}

.replay-button svg,
a.replay-button svg {
  width: 28px !important;
  height: 28px !important;
  fill: #ffffff !important;
  color: #ffffff !important;
}

#answer {
  width: 100%;
  max-width: 760px;
  height: 0;
  margin: 16px auto;
  border: 0;
}

.answer-shell {
  margin-top: 0;
  box-shadow: none;
}

.answer-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  padding: 17px 22px 0;
}

.answer-chip {
  padding: 9px 12px;
  background: var(--accent-soft);
  color: var(--accent-text);
  text-transform: uppercase;
}

.answer-body {
  padding: 24px 28px 28px;
}

.answer-primary {
  padding: 20px 0 22px;
}

.answer-primary + .support-panel,
.answer-primary + .reference-panel {
  margin-top: 0;
}

.answer-value {
  margin-top: 7px;
  color: var(--text);
  font-size: clamp(28px, 5vw, 39px);
  font-weight: 720;
  line-height: 1.22;
  letter-spacing: -.02em;
}

.support-panel,
.reference-panel,
.info-card,
.notes-panel {
  margin-top: 12px;
  padding: 14px 16px;
}

.reference-panel {
  border: 1px solid var(--border);
  border-radius: 16px;
  background: var(--surface-soft);
}

.support-value,
.info-value {
  margin-top: 5px;
  color: var(--text);
  font-size: 17px;
  line-height: 1.48;
}

.info-card {
  border-inline-start: 3px solid var(--accent);
}

.back-audio {
  display: flex;
  justify-content: center;
  margin-top: 14px;
  padding: 12px;
}

.notes-panel .notes {
  margin-top: 6px;
  color: var(--muted);
  font-size: 15px;
}

.source-row {
  margin-top: 18px;
  padding-top: 14px;
  border-top: 1px solid var(--border);
}

.source-row .source {
  margin-top: 4px;
  color: var(--faint);
  font-size: 12px;
  line-height: 1.45;
}

@media (max-width: 480px) {
  .card {
    padding: 12px 8px 22px;
    font-size: 19px;
  }

  .anki-card,
  .answer-shell {
    border-radius: 18px;
  }

  .card-head,
  .answer-head {
    padding: 14px 16px 0;
  }

  .card-main {
    padding: 27px 18px 24px;
  }

  .front-stage {
    min-height: 155px;
    gap: 15px;
  }

  .answer-body {
    padding: 18px 18px 22px;
  }

  .skill-chip,
  .language-chip,
  .answer-chip {
    font-size: 11px;
  }

  .target.hero {
    font-size: clamp(27px, 9vw, 36px);
  }

  .prompt.hero {
    font-size: clamp(24px, 7.5vw, 32px);
  }
}

@media (prefers-reduced-motion: reduce) {
  * {
    scroll-behavior: auto !important;
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
    skill_label = SKILL_META[skill][1]
    skill_class = f"skill-{skill}"

    shell_open = """
<div class="anki-card __SKILL_CLASS__">
  <div class="card-head">
    <div class="skill-chip"><span class="skill-dot"></span>__SKILL_LABEL__</div>
    <div class="language-chip" dir="auto">{{TargetLanguage}}</div>
  </div>
  <div class="card-main">
""".replace("__SKILL_CLASS__", skill_class).replace("__SKILL_LABEL__", skill_label)
    shell_close = """
  </div>
</div>
"""

    if skill == "reading":
        front_body = """
    <div class="front-stage">
      <div class="stage-label">Read</div>
      <div class="target hero" dir="auto">{{Target}}</div>
      {{#Prompt}}<div class="cue" dir="auto">{{Prompt}}</div>{{/Prompt}}
      {{#FrontAudio}}<div class="audio-stage">{{FrontAudio}}</div>{{/FrontAudio}}
    </div>
"""
        answer_lead = """
    {{#Base}}
    <section class="answer-primary">
      <div class="section-label">{{BaseLanguage}}</div>
      <div class="answer-value" dir="auto">{{Base}}</div>
    </section>
    {{/Base}}
    {{#Target}}
    <section class="reference-panel">
      <div class="section-label">{{TargetLanguage}}</div>
      <div class="support-value" dir="auto">{{Target}}</div>
    </section>
    {{/Target}}
"""
    elif skill == "listening":
        front_body = """
    <div class="front-stage">
      <div class="stage-label">Listen</div>
      {{#Prompt}}<div class="cue" dir="auto">{{Prompt}}</div>{{/Prompt}}
      <div class="audio-stage">{{FrontAudio}}</div>
    </div>
"""
        answer_lead = """
    {{#Target}}
    <section class="answer-primary">
      <div class="section-label">{{TargetLanguage}}</div>
      <div class="answer-value" dir="auto">{{Target}}</div>
    </section>
    {{/Target}}
    {{#Base}}
    <section class="support-panel">
      <div class="section-label">{{BaseLanguage}}</div>
      <div class="support-value" dir="auto">{{Base}}</div>
    </section>
    {{/Base}}
"""
    elif skill == "production":
        front_body = """
    <div class="front-stage">
      <div class="stage-label">Produce</div>
      <div class="prompt hero" dir="auto">{{Prompt}}</div>
      {{#Hint}}
      <div class="hint-card">
        <div class="section-label">Hint</div>
        <div class="hint" dir="auto">{{Hint}}</div>
      </div>
      {{/Hint}}
      {{#Image}}<div class="media-panel image">{{Image}}</div>{{/Image}}
    </div>
"""
        answer_lead = """
    {{#Target}}
    <section class="answer-primary">
      <div class="section-label">{{TargetLanguage}}</div>
      <div class="answer-value" dir="auto">{{Target}}</div>
    </section>
    {{/Target}}
    {{#Base}}
    <section class="support-panel">
      <div class="section-label">{{BaseLanguage}}</div>
      <div class="support-value" dir="auto">{{Base}}</div>
    </section>
    {{/Base}}
"""
    else:
        # Pronunciation fronts never render Target directly because some modes
        # use audio/contrast prompts where the written answer would leak the target.
        front_body = """
    <div class="front-stage">
      <div class="stage-label">Pronounce / identify</div>
      {{#Prompt}}<div class="prompt hero" dir="auto">{{Prompt}}</div>{{/Prompt}}
      {{#Hint}}
      <div class="hint-card">
        <div class="section-label">Hint</div>
        <div class="hint" dir="auto">{{Hint}}</div>
      </div>
      {{/Hint}}
      {{#FrontAudio}}<div class="audio-stage">{{FrontAudio}}</div>{{/FrontAudio}}
    </div>
"""
        answer_lead = """
    {{#Target}}
    <section class="answer-primary">
      <div class="section-label">{{TargetLanguage}}</div>
      <div class="answer-value" dir="auto">{{Target}}</div>
    </section>
    {{/Target}}
    {{#Base}}
    <section class="support-panel">
      <div class="section-label">{{BaseLanguage}}</div>
      <div class="support-value" dir="auto">{{Base}}</div>
    </section>
    {{/Base}}
"""

    front = shell_open + front_body + shell_close

    support = """
    {{#Focus}}
    <section class="info-card">
      <div class="section-label">Focus</div>
      <div class="info-value" dir="auto">{{Focus}}</div>
    </section>
    {{/Focus}}
    {{#IPA}}
    <section class="info-card">
      <div class="section-label">IPA</div>
      <div class="info-value" dir="auto">{{IPA}}</div>
    </section>
    {{/IPA}}
    {{#Reading}}
    <section class="info-card">
      <div class="section-label">Reading</div>
      <div class="info-value" dir="auto">{{Reading}}</div>
    </section>
    {{/Reading}}
    {{#Variant}}
    <section class="info-card">
      <div class="section-label">Variant</div>
      <div class="info-value" dir="auto">{{Variant}}</div>
    </section>
    {{/Variant}}
    {{#Grammar}}
    <section class="info-card">
      <div class="section-label">Grammar</div>
      <div class="info-value" dir="auto">{{Grammar}}</div>
    </section>
    {{/Grammar}}
    {{#BackAudio}}<div class="back-audio">{{BackAudio}}</div>{{/BackAudio}}
    {{#Image}}<div class="media-panel image">{{Image}}</div>{{/Image}}
    {{#Notes}}
    <section class="notes-panel">
      <div class="section-label">Notes</div>
      <div class="notes" dir="auto">{{Notes}}</div>
    </section>
    {{/Notes}}
    {{#Source}}
    <div class="source-row">
      <div class="section-label">Source</div>
      <div class="source" dir="auto">{{Source}}</div>
    </div>
    {{/Source}}
"""

    if skill == "production":
        support = support.replace('{{#Image}}<div class="media-panel image">{{Image}}</div>{{/Image}}', "")

    back = (
        """
{{FrontSide}}
<hr id="answer">
<div class="answer-shell __SKILL_CLASS__">
  <div class="answer-head">
    <div class="answer-chip">Answer</div>
    <div class="language-chip" dir="auto">{{TargetLanguage}}</div>
  </div>
  <div class="answer-body">
"""
        + answer_lead
        + support
        + """
  </div>
</div>
"""
    ).replace("__SKILL_CLASS__", skill_class)

    return genanki.Model(
        model_id,
        f"Anki Language v{MODEL_VERSION} — {skill_label}",
        fields=FIELDS,
        templates=[{"name": "Card 1", "qfmt": front, "afmt": back}],
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
            skill,
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
