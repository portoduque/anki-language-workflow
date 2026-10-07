# Media

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
- Production often benefits from answer audio, but only when useful.
- Reading may use audio selectively.
- Images are usually valuable for concrete/visual concepts, not abstract connectors or grammar.

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
