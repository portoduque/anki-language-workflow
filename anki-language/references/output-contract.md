# Output Contract

**Current version: `2.1`, four authorable skills.** Only `reading`, `listening`, `pronunciation`, and `writing` may be created. `production` is retired and explicitly rejected by the v2.1 validator. Version 2.0 is supported only to read/build historical plans; do not author v2.0 as a workaround.


The AI produces an intermediate `card-plan.json`; deterministic scripts enrich media, validate it, and deliver the result.

## Language contract

The workflow has **no default languages**. On first use in a workspace, the AI must ask for:

- target language: the language being learned;
- base language: the language used for explanations, translations, semantic cues, and learner-facing instructions.

These choices are stored in `anki-language.config.json` and must be copied into each generated card plan.

## Required plan-level fields

- `version` = `2.1` for every new plan
- `target_language.name`
- `target_language.code`
- `base_language.name`
- `base_language.code`
- `deck_name`
- `cards`

Optional plan-level field:

- `delivery.mode`: `apkg`, `live`, or `both`.

## Auditable source coverage for multiple recordings

For a folder or ZIP of supplied source audio, scan and inspect **every original file** before selecting cards. Include a `source_inventory` object in the current v2.1 plan:

```json
{
  "source_inventory": {
    "audio_root": "materials/audios",
    "items": [
      {"id": "01", "file": "audio_1.mp3", "status": "selected", "card_ids": ["listen-01"]},
      {"id": "02", "file": "audio_2.mp3", "status": "skipped", "reason": "Only trivial or fully duplicated material."}
    ]
  }
}
```

Every selected card includes `"source_item_id": "01"` (matching the inventory item's ID); `card_ids` list every selected card from that source. All audio files in the declared directory or ZIP must be listed once. The deterministic validator checks the source files, selected/skipped status, reasons, and bidirectional card links **before** generating any media. It refuses incomplete inventories, but cannot itself recognize unselected meaningful chunks. The AI must inspect every entire sentence and justify omissions; no one-card-per-audio quota. Text-only or unrelated material without a source-audio collection may omit this section.

## Card fields

Each card includes:

- `id`: stable unique string;
- `skill`: `reading`, `listening`, `pronunciation`, or `writing` (v2.1);
- `target_text`: target-language answer/context.

Optional fields:

- `mode`: deterministic retrieval subtype. Valid values are `standard`, `minimal-pair`, `sound-discrimination`, `spelling-sound`, and `audio-to-spelling`;
- `writing_answer`: Writing only; the exact unique missing word/short chunk inside `target_text`, in one line. The builder derives the two visible sentence parts; do not author HTML or cloze markup;
- `base_text`;
- `prompt`: learner-facing instruction or a concise situational/scene cue that defines the retrieval task without revealing the target;
- `focus`;
- `hint`;
- `notes`;
- `ipa`;
- `reading`: optional target-script reading/romanization aid such as pinyin, kana, or another reading representation;
- `variant`: optional alternate written/script/orthographic form such as simplified/traditional or another spelling variant;
- `grammar`: optional concise grammatical attribute such as gender, noun class, part of speech, or form;
- `audio`: resolved audio path containing the exact selected utterance (not an unrelated full-dialogue recording);
- `audio_clip`: optional source-audio clipping request: `source` plus either **both** verified `start_seconds`/`end_seconds` or neither (optional local speech alignment); mutually exclusive with `audio` and `audio_request`;
- `audio_transcript`: optional **verified actual wording** of a recording; mandatory whenever the same resolved audio file serves cards with different target texts, and validated for target-text inclusion;
- `image`: resolved media path;
- `audio_request`: request for automatic Piper TTS;
- `image_request`: request for licensed image search/download;
- `audio_provenance` / `image_provenance`;
- `media_validation`: deterministic validation record including SHA-256;
- `media_issues`: non-fatal failures for optional media that was skipped;
- `source_item_id`: mandatory for cards in a declared multi-audio inventory; must link to exactly one inventory item;
- `source`: source/provenance text; when the material exposes a stable locator, preserve the most useful precise locator available (for example a video timestamp, page, chapter/section, or transcript anchor);
- `source_excerpt`: optional **verbatim verified original-language excerpt** from the user's written/screenshot/transcript source, useful for grounding cards; when present, `target_text` must occur as a whole phrase within it. Do not insert generated/adapted language as if it were quoted from the source;
- `tags`.

These structured fields are **metadata/support**, not card-generation quotas. Populate them only when they help the selected retrieval target. An empty field creates no extra card by itself in this workflow.

### Long source, short card — content contract

An original sentence/turn may be long, but `target_text` should **normally contain the selected useful chunk or short utterance**, not automatically the whole source line. One long sentence may supply zero, one, or multiple **distinct** short `cards[]` entries; selection is based on independent retrieval value and fast review, not a required quantity.

- **Reading:** use a natural, readable target phrase with just enough context to understand what is being tested; do not force the learner to process an irrelevant long paragraph.
- **Production:** retired; never create for a v2.1 plan. Choose a useful comprehension or short written-form task only when independently justified.
- **Writing:** use a short natural `target_text`, one meaningful `writing_answer` occurring exactly once, and a clear non-leaking `prompt`. The learner types only the missing part; compare with Anki's native type-answer mechanism, not JavaScript. Writing audio (when useful) stays on the back.
- **Listening / Pronunciation:** when the chosen unit is a chunk from a longer recording, set `audio_clip` for the **same exact spoken portion**. Source text and audio must align; never replay an entire dialogue for a short target.
- **Source:** preserve the original material's valid locator in `source` (and only minimal helpful explanation on the back). Do not insert the full original sentence into every Front as mandatory context.
- A complete sentence is allowed when the **entire utterance** is what the learner must retrieve and the card still passes the quick-answer/quick-verification test.
- No automatic slicing by punctuation/word count, fixed chunk quota, new deck type, note model, or extra schema field is required. The selection step is semantic and remains the responsibility of the AI operating the skill.
- Select distinct learning **chunks first**; assign one primary skill to each, then add other skill cards only for independently useful retrieval operations. Scan the final batch for near-paraphrases.
- Exact duplicate retrieval tasks **within one plan** are rejected even if IDs, tags, source or notes differ; this is not a semantic similarity or existing-Anki-collection audit.
- For standard modes and Pronunciation `spelling-sound`, `audio_request.text` must match the card's spoken `target_text` (ignoring case/punctuation/spacing), to prevent unrelated TTS.
- Verified `audio_transcript` must equal `target_text` for Listening, Writing and standard/spelling-sound Pronunciation (plus legacy v2.0 Production); a target **contained inside** a longer audio recording is insufficient for these skills. When `audio_provenance.kind` indicates original user/native audio, exact-audio skills require a verified transcript. The media enricher replaces long-source transcripts with the resolved exact target after successful clipping and records TTS text as the transcript. Audio bytes with identical hashes cannot serve different exact-audio target texts, even under different file names.
- The deterministic checks are not ASR and cannot establish the truthfulness of a submitted transcript or a transcript extracted from screenshots. Resolve disagreements by listening/checking source evidence, not by guessing.

For each candidate, mentally simulate one review: can the learner tell what to retrieve immediately, recover one target, and check the answer quickly? Otherwise simplify, split useful targets, or skip.

### Mode contract

`mode` is not an open-ended label. The deterministic pipeline validates it against the selected skill:

- Reading, Listening, and Writing currently support only `standard`;
- Pronunciation & Sounds supports `standard`, `minimal-pair`, `sound-discrimination`, `spelling-sound`, and `audio-to-spelling`;
- Pronunciation `standard` and `spelling-sound` deterministically show the written target on the front (internal `FrontCue` field); audio-identification modes keep the answer hidden and use front audio;
- generic "say this" pronunciation fronts without a target/recognition cue are invalid study tasks; only create an extra Pronunciation card when it trains an independent relevant difficulty;
- Pronunciation subtypes that depend on sound require resolved audio before delivery. This includes `spelling-sound`, even though its audio is normally feedback rather than the front-side cue.

Unknown modes and cross-skill mode combinations are rejected instead of silently falling back to standard behavior.

### Writing contract

**Writing is selective short-gap typed recall:** it practices the **correct spelling/form** of one written chunk in an already-short sentence. The card must specify `writing_answer` and `prompt`; validation rejects missing/non-unique answers, full-sentence blanks, unaligned word fragments, newlines, and use of `writing_answer` on other skills.

```json
{
  "id": "write-01",
  "skill": "writing",
  "target_text": "Je vais à l'école.",
  "writing_answer": "à l'école",
  "prompt": "Complete a frase com a expressão que significa 'para a escola'."
}
```

The deterministic model **Anki Language v5 — Writing** uses the same visual family with dedicated fields `WritingBefore`, `WritingAfter`, `WritingAnswer`. The Front has visible context plus **one native `{{type:WritingAnswer}}` input**, and the Back has **`{{FrontSide}}` comparison** plus complete answer. The comparison is for single-line typing and the learner selects the review rating. AnkiWeb/preview do not display an interactive typing input; spot-check on desktop/mobile Anki. Additional reference: `references/writing.md`.

Do not generate Writing for every learned chunk or force multiword, multigap, full-sentence transcription.

### Workflow identity

Delivery injects system tags deterministically; the AI/card plan does not need to author them:

- `anki-language` marks workflow-owned notes so read-only audits can find them regardless of whether they arrived through APKG or live delivery;
- a scoped identity tag is derived from deck name + target-language code + skill + stable card `id`.

The scoped identity prevents an unrelated card with the same local `id` in another deck/language workspace from being mistaken for an already-delivered note.

Live reruns are conflict-aware. An existing workflow note is skipped only after its expected fields/media references are verified. If the same stable identity now describes different content, delivery stops and reports drift instead of silently skipping or overwriting the note.

Legacy live notes created with the older card-id-only identity tag remain detectable in their expected deck. They are verified read-only and are not silently migrated.

Validated audio formats/hashes only prove file integrity, not spoken content. When a file is reused for different target texts, `audio_transcript` is required for each use; the validator checks transcript consistency and wording inclusion, but a human/source review must verify that the recording really says it. Favor focused clips; an unrelated long clip should not masquerade as exact answer audio.

The generated card templates must remain inspectable and portable: **essential card behavior may not depend on JavaScript or remote web assets**. Use ordinary Anki field replacements, HTML, CSS, and local packaged media for the core review experience.

### Presentation contract

New delivery uses **Anki Language v5** note models with the workflow-owned visual system documented in `references/card-ui.md`.

Presentation is deterministic, not model-authored:
- the AI chooses content/skill/mode, not arbitrary colors/layout HTML;
- skill identity is always visible as text and reinforced with a stable accent;
- the primary retrieval target is visually dominant;
- hints, metadata, notes, media, and source stay subordinate;
- Reading promotes base-language meaning on the answer; Listening/Production/Pronunciation promote the target-language answer;
- responsive mobile, night mode, and `dir="auto"` support are part of the template contract;
- v3/v4 models are not silently mutated when v5 is introduced.
- The new Writing note type v5 is independent and does not mutate existing v5/v6 types.
- Pronunciation alone now uses a v6 note model with an internal FrontCue field; Reading, Listening, and Production remain v5, with the same approved CSS/visual appearance. Existing v5 Pronunciation notes are not changed automatically.

Do not invent source precision. A precise locator is kept only when the supplied/source material actually supports it.

## Original source-audio clipping

When a supplied audio file contains several utterances, select an excerpt with:

```json
{
  "target_text": "Vous pouvez me suivre.",
  "audio_clip": {
    "source": "lesson.mp3",
    "start_seconds": 12.4,
    "end_seconds": 14.9
  }
}
```

Verified source timestamps take precedence. When the timing is unknown, `{"source":"lesson.mp3"}` invokes **optional** faster-whisper word transcription plus one unambiguous exact phrase match against `target_text`; it may fail and request correction. Only **FFmpeg** is needed for already-known boundaries. Install `requirements-alignment.txt` separately if automatic discovery is wanted. No default install or extra service required for cards without `audio_clip`.

The enricher replaces `audio_clip` with the validated short `audio` file and records original path, clip boundaries, and alignment method under `audio_provenance`. It **fails closed** for ambiguous/missing text, repeated phrases, out-of-range boundaries, or missing dependencies. Acoustic correctness cannot be guaranteed by matching words on paper alone; review source-timestamp accuracy and representative output by listening.

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

A Listening card or sound-dependent Pronunciation card may contain an unresolved `audio_request` or `audio_clip` during planning, but **final build/live delivery requires an actual validated `audio` file**.

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

1. resolve requested media, including source-audio clip alignment/FFmpeg extraction when selected;
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
