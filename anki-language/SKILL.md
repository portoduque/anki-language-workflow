---
name: anki-language
description: Turn language-learning source material (text, audio, images, notes, PDFs, transcripts, or mixed inputs) into a selective, pedagogically sound Anki card plan and validated APKG package. Use when the user wants to create or update language-learning Anki decks, including reading, listening, production, pronunciation, audio, images, tags, and importable media.
---

# Anki Language

Create the smallest useful set of language-learning cards from the user's material, then build and validate an Anki package.

## Fixed defaults

- The **target language** is the language being learned.
- The **support language is English** unless the user explicitly requests another support language.
- Do not silently switch explanations to Portuguese.
- Prefer the user's own material over generic replacements.
- If an ambiguity materially changes the learning target, language, media, or card design, ask the user before building. Do not ask about minor choices that can be resolved conservatively.

## Required workflow

1. Inspect all supplied material.
2. Detect the target language if it is not explicit. Ask only when detection is materially ambiguous.
3. Segment the material into meaningful learning units.
4. For every unit, decide whether it deserves 0, 1, or more cards.
5. Create multiple cards from one unit only when they train distinct skills.
6. Classify every selected card into exactly one deck skill: `reading`, `listening`, `production`, or `pronunciation`.
7. Add linguistic tags such as `vocabulary`, `chunk`, `collocation`, `grammar`, `word-form`, `word-order`, `expression`, `spelling`, `minimal-pair`, or `sentence-mining` only when they are useful.
8. Decide whether audio and/or an image materially improves the card.
9. Write a `card-plan.json` that conforms to `schemas/card-plan.schema.json`.
10. Run `scripts/validate_plan.py`.
11. Build the package with `scripts/build_apkg.py`.
12. Validate the package with `scripts/validate_apkg.py`.
13. Return the APKG plus a concise build report.

## Deck architecture

Use one parent deck per target language:

- `<Language>::01 Reading`
- `<Language>::02 Listening`
- `<Language>::03 Production`
- `<Language>::04 Pronunciation & Sounds`

Do not create extra micro-decks for vocabulary, grammar, chunks, collocations, levels, or source names. Use tags for those dimensions.

## Selection standard

Read `references/card-selection.md` before selecting cards.

Core rule: **do not create a card merely because a template supports it**.

A source item may legitimately produce no card. High review volume is a cost.

## Production and cloze rule

Do not use blind or ambiguous cloze prompts.

Bad:

`J'ai ___ rester chez moi.`

Better:

`Complete with the expression meaning "to end up doing something": J'ai ___ rester chez moi.`

The user must know what knowledge is being retrieved without the prompt giving away the target form.

## Media

Read `references/media.md` before acquiring or generating media.

Priority for audio:

1. Original audio supplied by the user.
2. Permitted native-speaker audio from a licensed/authorized source.
3. High-quality TTS.

Never scrape, cache, redistribute, or embed media in ways that violate the source's terms or license. Forvo or similar services may be used only through a permitted API/license/workflow.

Use images primarily when they make the concept more concrete or remove translation ambiguity. Do not add decorative images.

## Card behavior

- Reading: written target-language context on the front; English meaning/explanation on the back.
- Listening: audio on the front; target transcript and English meaning on the back.
- Production: precise English/semantic/context prompt on the front; target-language answer and normally audio on the back.
- Pronunciation & Sounds: choose production, minimal-pair/perception, or spelling-sound behavior according to the actual learning target.

## Output contract

Use `schemas/card-plan.schema.json` and preserve source provenance where available.

The deterministic builder is the source of truth for APKG structure. Do not hand-edit Anki collection databases.

## Quality gate

Before delivery, verify:

- no missing media references;
- no duplicate media basenames;
- no ambiguous production prompts;
- no unnecessary sibling cards;
- support language is English unless explicitly overridden;
- deck hierarchy is correct;
- APKG opens as a valid ZIP/Anki package;
- build report counts match the plan.

Read `references/pedagogy.md`, `references/card-selection.md`, `references/media.md`, and `references/output-contract.md` for detailed rules.