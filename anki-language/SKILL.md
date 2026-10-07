---
name: anki-language
description: Creates selective, import-ready Anki language decks from text, audio, images, PDFs, transcripts, notes, or mixed study material. Use when the user wants language-learning flashcards, an APKG package, sentence mining, listening/reading/production/pronunciation practice, or audio/images organized into Anki.
---

# Anki Language

Turn source material into the smallest useful set of language-learning cards, then build and validate an Anki package.

## Defaults

- Treat the language being learned as the **target language**.
- Use **English as the support language** unless the user explicitly requests another support language.
- Prefer the user's source material over generic replacements.
- Ask only when an ambiguity materially changes the learning target, language, media, or card design. Resolve minor choices conservatively.

## Workflow

1. Inspect all supplied material before selecting cards.
2. Read [references/pedagogy.md](references/pedagogy.md) and [references/card-selection.md](references/card-selection.md).
3. Segment the source into meaningful learning units.
4. For each unit, create zero, one, or multiple cards only when each card trains a distinct useful skill.
5. Classify each selected card as exactly one of: `reading`, `listening`, `production`, or `pronunciation`.
6. Add sparse linguistic tags only when useful.
7. If media may improve learning, read [references/media.md](references/media.md) before acquiring, generating, or attaching it.
8. Write `card-plan.json` according to [references/output-contract.md](references/output-contract.md) and `schemas/card-plan.schema.json`.
9. Run `python scripts/build.py card-plan.json --output <Language>.apkg`.
10. Deliver the APKG, build report, and card plan. Report skipped or unresolved items concisely.

## Deck architecture

- `<Language>::01 Reading`
- `<Language>::02 Listening`
- `<Language>::03 Production`
- `<Language>::04 Pronunciation & Sounds`

Use tags, not extra micro-decks, for vocabulary, grammar, chunks, levels, sources, and similar dimensions.

## Card behavior

- **Reading:** written target-language context on the front; English meaning/explanation on the back.
- **Listening:** audio on the front; transcript and English meaning on the back.
- **Production:** a precise English/semantic/context prompt on the front; target-language answer and normally audio on the back.
- **Pronunciation & Sounds:** use pronunciation production, sound discrimination/minimal pair, or spelling-sound behavior according to the actual target.

Never use a blind or ambiguous cloze. The learner must know what knowledge to retrieve without the prompt revealing the answer.

## Quality gate

Do not deliver until the deterministic pipeline passes. It validates plan structure, media references, package integrity, note/card counts, deck hierarchy, and the final APKG.

The builder, not the model, is the source of truth for package structure. Do not hand-edit Anki collection databases.