# Output Contract

The AI produces an intermediate `card-plan.json`; deterministic scripts turn that plan into the APKG.

## Required plan-level fields

- `version`
- `target_language.name`
- `target_language.code`
- `support_language.name`
- `support_language.code`
- `deck_name`
- `cards`

The default support language is English (`en`).

## Card fields

Each card includes:

- `id`: stable unique string;
- `skill`: `reading`, `listening`, `production`, or `pronunciation`;
- `mode`: optional subtype such as `standard`, `minimal-pair`, `sound-discrimination`, or `spelling-sound`;
- `target_text`: target-language answer/context;
- `support_text`: English meaning/explanation when useful;
- `prompt`: precise learner-facing task;
- `focus`: target word/chunk/structure when useful;
- `hint`: optional disambiguating cue;
- `notes`: optional concise explanation;
- `ipa`: optional pronunciation field;
- `audio`: optional path relative to the plan file;
- `image`: optional path relative to the plan file;
- `audio_provenance` / `image_provenance`: optional structured provenance (`kind`, provider, source URL, license note) when known;
- `source`: optional provenance;
- `tags`: optional linguistic/content tags.

## Build pipeline

Run `python scripts/build.py card-plan.json --output <Language>.apkg`.

The pipeline validates the JSON Schema and semantic rules, checks referenced media, builds the package, opens the embedded Anki collection database, verifies note/card counts and deck names, and verifies the media manifest.

## Report

The APKG builder writes a sibling `.report.json` containing:

- target/support language;
- total card count;
- per-skill counts;
- media count;
- skipped count when provided by the plan;
- output path.