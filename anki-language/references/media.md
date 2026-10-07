# Media

Media is optional. Add it only when it improves retrieval, comprehension, or pronunciation.

## Audio priority

1. User-supplied original audio.
2. Native-speaker audio obtained through a source whose API/license permits the intended use.
3. High-quality TTS when original/native audio is unavailable or impractical.

### Placement

- Listening: audio normally appears on the front.
- Production: audio normally appears on the back, after the learner attempts retrieval.
- Pronunciation production: audio normally appears on the back.
- Sound discrimination/minimal pair: audio appears on the front.

## Forvo and similar services

Do not scrape media sites. Do not assume that a publicly playable pronunciation may be downloaded, cached, redistributed, or embedded in an APKG.

Use Forvo or another provider only when the user/environment has a permitted API/license/workflow. If no permitted source is available, use a lawful alternative such as user-supplied audio or permitted TTS.

## Images

Good uses:

- concrete nouns;
- visually distinctive objects/actions;
- a user-provided image that directly encodes the concept;
- a generated/licensed image that removes translation ambiguity.

Poor uses:

- decorative art;
- abstract connectors where the image is ambiguous;
- images that add search/review complexity without improving retrieval.

## Provenance

When media is used, populate `audio_provenance` or `image_provenance` in the card plan when the information is known. Preserve whether the asset was user-supplied, sourced from a native recording provider, synthesized with TTS, generated, or otherwise licensed.

Never infer a license that was not actually verified.

## Packaging

Media files referenced by the plan must exist before APKG build.

Media basenames must be unique inside one package. The validator rejects collisions to avoid Anki media-reference ambiguity.

Record provenance in the card `source` field or notes when useful.