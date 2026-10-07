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

- `mode`: deterministic retrieval subtype. Valid values are `standard`, `minimal-pair`, `sound-discrimination`, `spelling-sound`, and `audio-to-spelling`;
- `base_text`;
- `prompt`: learner-facing instruction or a concise situational/scene cue that defines the retrieval task without revealing the target;
- `focus`;
- `hint`;
- `notes`;
- `ipa`;
- `reading`: optional target-script reading/romanization aid such as pinyin, kana, or another reading representation;
- `variant`: optional alternate written/script/orthographic form such as simplified/traditional or another spelling variant;
- `grammar`: optional concise grammatical attribute such as gender, noun class, part of speech, or form;
- `audio`: resolved media path;
- `image`: resolved media path;
- `audio_request`: request for automatic Piper TTS;
- `image_request`: request for licensed image search/download;
- `audio_provenance` / `image_provenance`;
- `media_validation`: deterministic validation record including SHA-256;
- `media_issues`: non-fatal failures for optional media that was skipped;
- `source`: source/provenance text; when the material exposes a stable locator, preserve the most useful precise locator available (for example a video timestamp, page, chapter/section, or transcript anchor);
- `tags`.

These structured fields are **metadata/support**, not card-generation quotas. Populate them only when they help the selected retrieval target. An empty field creates no extra card by itself in this workflow.

### Mode contract

`mode` is not an open-ended label. The deterministic pipeline validates it against the selected skill:

- Reading, Listening, and Production currently support only `standard`;
- Pronunciation & Sounds supports `standard`, `minimal-pair`, `sound-discrimination`, `spelling-sound`, and `audio-to-spelling`;
- Pronunciation subtypes that depend on sound require resolved audio before delivery. This includes `spelling-sound`, even though its audio is normally feedback rather than the front-side cue.

Unknown modes and cross-skill mode combinations are rejected instead of silently falling back to standard behavior.

### Workflow identity

Delivery injects system tags deterministically; the AI/card plan does not need to author them:

- `anki-language` marks workflow-owned notes so read-only audits can find them regardless of whether they arrived through APKG or live delivery;
- a scoped identity tag is derived from deck name + target-language code + skill + stable card `id`.

The scoped identity prevents an unrelated card with the same local `id` in another deck/language workspace from being mistaken for an already-delivered note.

Live reruns are conflict-aware. An existing workflow note is skipped only after its expected fields/media references are verified. If the same stable identity now describes different content, delivery stops and reports drift instead of silently skipping or overwriting the note.

Legacy live notes created with the older card-id-only identity tag remain detectable in their expected deck. They are verified read-only and are not silently migrated.

The generated card templates must remain inspectable and portable: **essential card behavior may not depend on JavaScript or remote web assets**. Use ordinary Anki field replacements, HTML, CSS, and local packaged media for the core review experience.

Do not invent source precision. A precise locator is kept only when the supplied/source material actually supports it.

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

`provider` currently supports `auto` and `piper`. A specific `voice` is optional. Set `required: true` when failure must block delivery. Listening audio is always required, and sound-dependent Pronunciation modes (`minimal-pair`, `sound-discrimination`, `spelling-sound`, `audio-to-spelling`) also treat audio as required even when the flag is omitted.

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

A Listening card or sound-dependent Pronunciation card may contain an unresolved `audio_request` during planning, but **final build/live delivery requires an actual validated `audio` file**.

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
5. APKG: validate package/database/media manifest, expected decks/counts, and workflow identity tags;
6. live: inspect the workflow-owned model fields/templates/CSS, verify any existing-note identity/content match, then verify uploaded media bytes and note-field references.

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

## Rendering boundary

Deterministic APKG validation checks package/database/media structure. It does **not** prove that every Anki client will render every template perfectly.

After a meaningful template/model migration, spot-check representative cards in Anki before large-scale adoption. Include:
- a long card that requires answer scrolling;
- empty optional fields;
- audio/image media when used;
- night mode;
- the target writing system, especially right-to-left or mixed-direction text.

Anki client rendering is the final authority for presentation. Do not claim cross-client rendering success from structural APKG validation alone.
