# Output Contract

The AI produces an intermediate `card-plan.json`; deterministic scripts enrich media, validate it, and deliver the result.

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

Optional plan-level field:

- `delivery.mode`: `apkg`, `live`, or `both`.

## Card fields

Each card includes:

- `id`: stable unique string;
- `skill`: `reading`, `listening`, `production`, or `pronunciation`;
- `target_text`: target-language answer/context.

Optional fields:

- `mode`: subtype such as `standard`, `minimal-pair`, `sound-discrimination`, `spelling-sound`, or `audio-to-spelling`;
- `base_text`;
- `prompt`;
- `focus`;
- `hint`;
- `notes`;
- `ipa`;
- `audio`: resolved media path;
- `image`: resolved media path;
- `audio_request`: request for automatic Piper TTS;
- `image_request`: request for licensed image search/download;
- `audio_provenance` / `image_provenance`;
- `media_validation`: deterministic validation record including SHA-256;
- `media_issues`: non-fatal failures for optional media that was skipped;
- `source`;
- `tags`.

## Automatic audio request

Example:

```json
{
  "audio_request": {
    "mode": "auto",
    "text": "Bonjour",
    "provider": "auto"
  }
}
```

`provider` currently supports `auto` and `piper`. A specific `voice` is optional. Set `required: true` when failure must block delivery; Listening and sound-discrimination audio is treated as required even when the flag is omitted.

## Automatic image request

Example:

```json
{
  "image_request": {
    "mode": "auto",
    "query": "red squirrel",
    "provider": "auto",
    "licenses": ["cc0", "pdm"]
  }
}
```

`provider=auto` tries Openverse then Wikimedia Commons. Images are optional by default; set `required: true` only when the card itself depends on the image.

## Resolved-plan rule

A Listening/sound-discrimination card may contain an unresolved `audio_request` during planning, but **final build/live delivery requires an actual validated `audio` file**.

Automatic requests are resolved with:

`python scripts/media_enrich.py card-plan.json --output card-plan.resolved.json`

## End-to-end pipeline

Preferred command:

`python scripts/run_pipeline.py card-plan.json --delivery apkg`

Live Anki:

`python scripts/run_pipeline.py card-plan.json --delivery live`

Both:

`python scripts/run_pipeline.py card-plan.json --delivery both --output <Language>.apkg`

Stages:

1. resolve requested media;
2. functionally validate every local audio/image;
3. write resolved card plan with provenance + SHA-256;
4. deliver as APKG and/or via AnkiConnect;
5. APKG: validate package/database/media manifest;
6. live: verify uploaded media bytes and note-field references.

## Direct APKG build

When the plan already contains resolved media:

`python scripts/build.py card-plan.resolved.json --output <Language>.apkg`

## Reports

APKG writes `.report.json`.

The end-to-end pipeline prints a JSON report containing:
- enrichment counts;
- resolved-plan path;
- APKG validation when used;
- live note IDs and post-upload media verification when used.
