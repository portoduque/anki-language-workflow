# Media

## Mandatory automatic audio for new v2.3 plans

The deterministic `media_enrich.py` stage automatically synthesizes a focused pronunciation for **every** card lacking valid supplied audio, plus the **complete literal text** of each `source_units[]` entry. It uses Piper `target_language.code`, caches identical language/voice/text requests, and embeds validated WAVs in APKG or AnkiConnect. Do not create extra cards merely to make audio. Generated voices require Piper installation and a compatible voice model (downloaded on first run); the pipeline stops with an explicit error if unavailable. As always, user-supplied recordings/verified clips take priority for the tested target.

APKG/AnkiConnect use the new isolated **v7** Anki note models for v2.3, with the extra `SourceAudio` field. Target audio uses the existing FrontAudio/BackAudio placement. Full-sentence contextual speech is on the **back under `{{hint:SourceAudio}}`**, so hearing a long original sentence is optional during quick reviews. If the full sentence and target audio are the same file, only the target replay is shown. Past v2.0–v2.2 plans retain their existing models and optional-media behavior; old cards are not overwritten.

Use the full pipeline (`run_pipeline.py` or `media_enrich.py` followed by delivery). Direct v2.3 export rejects unresolved audio; no silent `.apkg` without speech. Contrast targets like `Enchanté / Enchantée` are synthesized as sequential forms instead of saying the slash. Synthetic audio integrity/hash checks cannot independently certify accent, names, prosody, or naturalness. Inspect a sample of outputs for pronunciation fidelity.


Media is optional. Add it only when it improves retrieval, comprehension, listening, or pronunciation.

## Mandatory media gate

**No audio or image may be packaged into an APKG or uploaded to AnkiConnect before functional validation passes.**

The deterministic validator checks:

- audio exists, parses as real audio, has a positive duration, non-trivial size, and SHA-256;
- image exists, decodes fully with Pillow, has usable dimensions, non-trivial size, and SHA-256;
- a previously validated file has not changed before build/upload.

Run directly when debugging:

`python scripts/media_validate.py audio /path/file.wav`

`python scripts/media_validate.py image /path/file.webp`

In live AnkiConnect mode there is a second gate **after** creation: the workflow retrieves each uploaded media file from Anki, compares SHA-256 with the local validated file, and verifies that the created note field references the filename.

## Decision before generation

The AI decides whether media is pedagogically useful. The script does not add media to every card.

- Listening normally requires audio.
- Pronunciation/sound-discrimination normally requires audio.
- New Production is forbidden. Short Writing and Pronunciation answer audio is optional when useful.
- Reading may use audio selectively.
- Images are usually valuable for concrete/visual concepts, not abstract connectors or grammar.

## Audio/text alignment

A technically decodable MP3 is not proof that the recording says the target text. Before delivery, the card author should listen to the clip or inspect a reliable original transcript and verify that the answer being tested matches the recording.

- Prefer one focused recording for the target utterance instead of reusing a longer dialogue clip indiscriminately.
- **Listening and answer-feedback audio (Production, Writing, or ordinary read-aloud Pronunciation) must match the spoken `target_text` exactly**, after harmless case/punctuation normalization, when a transcript is supplied. Mere substring inclusion in a longer dialogue is not acceptable: use a matching `audio_clip`, a short dedicated original recording, or matching TTS. Reading or sound-discrimination can retain wider audio context where their tasks explicitly need it.
- When original recordings are supplied with `audio_provenance.kind = user-supplied` or `native-source`, Listening and exact-answer audio cards must include a **verified actual recording** `audio_transcript`; the validator requires it. Do not fabricate the transcript by copying the answer. Automatically resolved TTS/short clips carry their exact resolved spoken-target declaration.
- When **one audio file is reused across cards with different target text**, every use must carry the verified recording `audio_transcript`, and declarations across the shared audio must agree. The strict exact-audio rule above also applies; sharing a whole recording across different short answer targets will fail. Separate source audio files with identical SHA-256 content are checked for incompatible exact-audio targets so a different filename is not a workaround.
- These checks are **consistency checks only**. They do not listen to raw audio, verify native-speaker pronunciation, or prove a declared transcript is truthful. The author must compare the actual recording and any supplied screenshot/caption. A discrepancy such as `Ah super !` in a screenshot versus `Eh ben !` in a proposed transcript must be resolved, not quietly rewritten.
- An audio clip that illustrates an alternative phrasing rather than the specific target should not be presented as the exact target's pronunciation. Prefer omitting that optional audio or using a genuinely matching clip.

## v2.2 voice-boundary quality gate

For new v2.2 plans, generated source clips use extra lead/tail padding and a signal-level boundary check. A clip with conspicuous energy at its very start/end is blocked for review rather than being delivered as certainly complete. A quiet boundary is **not proof** that no phoneme was truncated; the operator must listen to representative clips. Older v2.0/v2.1 plans keep their original delivery behavior for compatibility. Do not silently replace uncertain original audio with unrelated TTS.

## Long recordings: one phrase per card

**Do not attach an entire dialogue/lesson as a card's `audio` when `target_text` is only one line.** Use the optional `audio_clip` request so the enricher creates a separate, focused WAV **before** APKG/AnkiConnect delivery:

```json
{
  "target_text": "Vous pouvez me suivre.",
  "audio_clip": {
    "source": "materials/dialogue.mp3",
    "start_seconds": 12.4,
    "end_seconds": 14.9
  }
}
```

When the source or transcript has **verified timestamps**, use those; no automatic speech model is required. When timestamps are missing, omit both bounds:

```json
{
  "target_text": "Vous pouvez me suivre.",
  "audio_clip": {"source": "materials/dialogue.mp3"}
}
```

This second form invokes **optional local faster-whisper** with word timestamps (CPU, small model) and matches the normalized target **exactly once** in the transcript. Exact transcription matching is deliberately conservative; OCR differences, ASR mistakes, isolated words, repeated phrases, and uncertain timing should be resolved with verified start/end times, a focused audio clip, or user confirmation. Do not guess the match. The program does **not** use forced-alignment proof or guarantee that ASR has perfectly heard the speaker.

- **Requirements:** FFmpeg executable on PATH for any `audio_clip`; install `requirements-alignment.txt` separately only when automatic timing is needed. The speech model downloads on first use; inference runs locally. Neither FFmpeg nor faster-whisper is required for ordinary audio files or Piper TTS.
- The enricher adds small lead/tail padding, creates a speech-friendly 24 kHz mono WAV, keeps the original untouched, then performs the normal decode/duration/SHA-256 validation.
- On success, `audio_clip` is replaced by `audio` and the original path, actual boundaries, and method are saved in `audio_provenance`. The **generated short clip** is what gets packaged or uploaded.
- On ambiguity, missing phrase, invalid timestamp, missing dependency, or failed FFmpeg, delivery **stops**. No silent full-audio fallback, approximate wrong segment, or unrelated synthesized alternative. Resolve the source or explicitly choose matching TTS.
- Manual timestamps still need to come from the real recording, not guesses. Inspect representative clips by listening before bulk import, especially when transcripts or subtitles differ from spoken phrasing.

`audio`, `audio_clip`, and `audio_request` are alternative input strategies: choose **one** per card. The other three skill decks and Anki note templates are unchanged.

## Audio priority

1. User-supplied original audio.
2. Permitted native-speaker audio whose terms allow the intended storage/use.
3. Local TTS.

### Automatic TTS

The built-in automatic provider is **Piper**.

The one-command repository installer installs Piper by default through `requirements-media.txt`. Use `--skip-media-deps` for a minimal installation.

A card requests synthesis with:

```json
{
  "audio_request": {
    "mode": "auto",
    "text": "J'ai fini par rester chez moi.",
    "provider": "auto"
  }
}
```

The enricher:

1. queries Piper's current voice catalog;
2. selects a voice matching the configured target-language code;
3. prefers a medium-quality voice for a practical quality/size balance;
4. downloads the selected voice when necessary;
5. synthesizes a WAV;
6. decodes/validates the WAV;
7. records provenance and a validation hash.

A specific Piper voice may be forced with `audio_request.voice`.

### Placement

- Listening: audio normally appears on the front.
- Production: audio normally appears on the back, after retrieval.
- Pronunciation production: audio normally appears on the back.
- Sound discrimination/minimal pair: audio appears on the front.

## Forvo and similar services

Forvo is **not a core automatic provider**.

Do not scrape Forvo or assume a publicly playable pronunciation may be permanently cached/redistributed. Its Anki add-ons run inside Anki and are not a stable automation API for Codex/Claude/Antigravity.

Use a Forvo pronunciation only when the user's environment and the applicable API/license explicitly permit the intended storage and embedding. Otherwise prefer user audio or Piper/permitted TTS.

## Automatic images

A card requests an image with:

```json
{
  "image_request": {
    "mode": "auto",
    "query": "squirrel",
    "provider": "auto",
    "licenses": ["cc0", "pdm"]
  }
}
```

Provider order for `auto`:

1. Openverse;
2. Wikimedia Commons fallback.

The default automatic license allowlist is deliberately strict: `cc0` and `pdm` (public-domain marking).

Openverse search uses:
- mature=false;
- dead-link filtering;
- explicit license filter;
- relevance ordering.

Wikimedia fallback uses the MediaWiki ImageInfo API with `extmetadata` and accepts only candidates whose machine-readable license matches the allowlist.

Downloaded images are normalized to WebP with a maximum 1600×1600 bounding box, then fully decoded again before acceptance.

Openverse itself warns that indexed license information may be inaccurate. Preserve `source_url`, `license`, `license_url`, and attribution when present. For redistribution outside personal study, verify the source license where required.

## Good image uses

- concrete nouns;
- visually distinctive objects/actions;
- user-provided images that directly encode the concept;
- licensed images that remove translation ambiguity.

## Poor image uses

- decorative art;
- abstract connectors where an image is ambiguous;
- grammar/function words where text is clearer;
- images that add review/search cost without improving retrieval.

## Provenance

Populate:
- `audio_provenance`;
- `image_provenance`;
- `media_validation`.

Provenance can include provider, source URL, license, license URL, and attribution.

Never invent or infer a license that was not actually supplied by the source.

## Enrichment

Resolve automatic media requests with:

`python scripts/media_enrich.py card-plan.json --output card-plan.resolved.json`

The resolved plan contains actual local media paths plus validation records.

## Packaging vs live Anki

### APKG

Validated local media is embedded by the normal builder.

### AnkiConnect live mode

Validated local media is attached to `addNotes` using local paths.

Before upload:
- local audio/image is decoded and hashed.

After upload:
- `notesInfo` must show the filename in the expected note field;
- `retrieveMediaFile` must return bytes with the same SHA-256.

If any check fails, live delivery returns an error instead of claiming success.

## Sources

- Piper: https://github.com/OHF-Voice/piper1-gpl
- Openverse API: https://api.openverse.org/v1/
- Wikimedia Commons metadata: https://www.mediawiki.org/wiki/Extension:CommonsMetadata
