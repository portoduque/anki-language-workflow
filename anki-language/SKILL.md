---
name: anki-language
description: Creates selective, import-ready Anki language decks from text, audio, images, PDFs, transcripts, notes, or mixed study material. Language- and AI-agnostic. Use for APKG generation, sentence mining, listening, reading, production, pronunciation, audio, images, and language-learning flashcards.
---

# Anki Language

Turn source material into the smallest useful set of language-learning cards, then build and validate an Anki package.

## Mandatory first-run language setup

Before analyzing study material, look for `anki-language.config.json` in the active workspace.

If the configuration does not exist, **stop before card creation and ask the user for both:**

1. **Target language** — the language being learned.
2. **Base language** — the language used to explain, translate, cue, and guide the target language.

Do not infer either language and do not use a default. This first-run question is mandatory even when the source material appears to make the target language obvious.

After the user answers, persist the choice in the workspace with:

`python scripts/configure.py --target-name <name> --target-code <code> --base-name <name> --base-code <code> --output ./anki-language.config.json`

On later runs in the same workspace, reuse that configuration unless the user asks to change it.

All learner-facing explanations, semantic cues, translations, and production instructions must use the configured **base language** unless the card intentionally tests the target language without a translation.

## Non-negotiable card rules

Before selecting cards, read [references/card-selection.md](references/card-selection.md). These invariants are mandatory:

- Create the **minimum useful number of cards**. The same sentence, word, expression, audio, image, or passage may produce multiple cards across different skill decks when each card trains a genuinely different and worthwhile retrieval operation.
- Every card has **one primary retrieval target**.
- Every front must be **self-orienting in a mixed review**: show the target language and trained skill without revealing the answer.
- Never create a prompt that makes the learner guess what the author intended. **Blind/ambiguous cloze is forbidden.**
- Do not create automatic reverse cards. Recognition and production get separate cards only when both are worth training.
- Do not generate every card type for every item. For every extra sibling card, require enough incremental learning value to justify its future review cost; optimize memory efficiency, not volume.
- Prefer useful chunks/collocations/patterns when the combination is the knowledge that matters.
- Sentence mining is selective; do not turn every sentence into a card.
- Audio and images are optional and must add learning value.
- Listening uses audio-first; Production normally keeps answer audio on the back; sound-discrimination cards must not reveal written answers on the front.
- Keep answers concise and reviews fast.
- When a material ambiguity changes the learning target, ask the user instead of guessing.

## Workflow

1. Resolve the mandatory target/base-language configuration.
2. Inspect all supplied material before selecting cards.
3. Read [references/pedagogy.md](references/pedagogy.md); the mandatory card rules were already loaded from [references/card-selection.md](references/card-selection.md).
4. Segment the source into meaningful learning units.
5. For each unit, create zero, one, or multiple cards only when each card trains a distinct useful skill.
6. Classify each selected card as exactly one of: `reading`, `listening`, `production`, or `pronunciation`.
7. Add sparse linguistic tags only when useful.
8. If media may improve learning, read [references/media.md](references/media.md) before acquiring, generating, or attaching it.
9. Write `card-plan.json` according to [references/output-contract.md](references/output-contract.md) and `schemas/card-plan.schema.json`. Its target/base languages must match the workspace configuration.
10. Run `python scripts/build.py card-plan.json --output <Language>.apkg`.
11. Deliver the APKG, build report, and card plan. Report skipped or unresolved items concisely.

## Deck architecture

- `<TargetLanguage>::01 Reading`
- `<TargetLanguage>::02 Listening`
- `<TargetLanguage>::03 Production`
- `<TargetLanguage>::04 Pronunciation & Sounds`

Use tags, not extra micro-decks, for vocabulary, grammar, chunks, levels, sources, and similar dimensions.

## Card behavior

- **Reading:** written target-language context on the front; meaning/explanation in the configured base language on the back when useful.
- **Listening:** audio on the front; target transcript and base-language meaning/explanation on the back.
- **Production:** a precise base-language/semantic/context prompt on the front; target-language answer and normally audio on the back.
- **Pronunciation & Sounds:** use pronunciation production, sound discrimination/minimal pair, or spelling-sound behavior according to the actual target.

Never use a blind or ambiguous cloze. The learner must know what knowledge to retrieve without the prompt revealing the answer.

## Anki technical reference routing

Use the bundled Anki reference library **when a decision depends on Anki behavior**, not for ordinary language analysis.

Consult it when you need to decide or verify:

- note/field/card-type structure;
- templates, HTML/CSS, TTS, typed answers, cloze, or Image Occlusion;
- audio/image/media packaging;
- decks/tags/search/browser behavior;
- FSRS/scheduling/settings;
- CSV/TSV/APKG/COLPKG import/export;
- sync/backups/profiles/files;
- statistics/leeches/filtered decks;
- add-ons/extensions;
- AnkiConnect, APIs, or automation;
- mobile/platform compatibility;
- troubleshooting, current-version behavior, or security.

When scripts are available, route the question first:

`python scripts/find_anki_reference.py "<technical need>"`

Then read only the returned files under `references/anki/`.

Do **not** preload the full Anki library for every card-generation run. Pure pedagogical card selection should use `references/card-selection.md` and `references/pedagogy.md`.

For current/version-sensitive facts or gaps in the local summaries, consult `references/anki/SOURCES.md` and prefer the official live documentation index:

https://docs.ankiweb.net/llms.txt

Current official Anki documentation outranks old blogs, old add-on instructions, and remembered behavior.

## AI portability

`SKILL.md`, `references/`, `schemas/`, and `scripts/` are the canonical implementation. Provider-specific adapters must remain thin. If an AI supports Agent Skills, install this bundle in its skill directory. If it does not, instruct the AI to read this `SKILL.md` and use the deterministic scripts directly.

## Quality gate

Do not deliver until the deterministic pipeline passes. It validates plan structure, media references, package integrity, note/card counts, deck hierarchy, and the final APKG.

The builder, not the model, is the source of truth for package structure. Do not hand-edit Anki collection databases.