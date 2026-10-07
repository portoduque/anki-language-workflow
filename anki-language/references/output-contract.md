# Output Contract

The AI produces an intermediate `card-plan.json`; deterministic scripts turn that plan into the APKG.

## Language contract

The workflow has **no default languages**. On first use in a workspace, the AI must ask for:

- target language: the language being learned;
- base language: the language used for explanations, translations, semantic cues, and learner-facing instructions.

These choices are stored in `anki-language.config.json` and must be copied into each generated card plan.

## Required plan-level fields

- `version` = `2.0`
- `target_language.name`
- `target_language.code`
- `base_language.name`
- `base_language.code`
- `deck_name`
- `cards`

## Card fields

Each card includes:

- `id`: stable unique string;
- `skill`: `reading`, `listening`, `production`, or `pronunciation`;
- `target_text`: target-language answer/context.

Optional fields:

- `mode`: subtype such as `standard`, `minimal-pair`, `sound-discrimination`, `spelling-sound`, or `audio-to-spelling`;
- `base_text`: meaning/explanation in the configured base language when useful;
- `prompt`: precise learner-facing task written in the configured base language. Required for production and pronunciation cards;
- `focus`: target word/chunk/structure;
- `hint`: disambiguating cue;
- `notes`: concise explanation, normally in the base language unless linguistic notation is more appropriate;
- `ipa`: pronunciation;
- `audio`: media path relative to the plan file;
- `image`: media path relative to the plan file;
- `audio_provenance` / `image_provenance`: structured provenance when known;
- `source`: source-material provenance;
- `tags`: sparse linguistic/content tags.

## Build pipeline

Run `python scripts/build.py card-plan.json --output <Language>.apkg`.

The pipeline validates the JSON Schema and semantic rules, checks referenced media, builds the package, opens the embedded Anki collection database, verifies note/card counts and deck names, and verifies the media manifest.

## Report

The APKG builder writes a sibling `.report.json` containing target/base language, total card count, per-skill counts, media count, skipped count, and output path.