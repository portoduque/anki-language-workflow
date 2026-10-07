# VidToAnki card-format ecosystem — Selective Adaptation Note

Primary source:
- https://www.vidtoanki.com/blog/best-anki-card-format-language-learning

Related site material reviewed to understand the recommendation in context:
- complete video-to-Anki workflow hub;
- free editable language-learning template;
- card fields guide;
- card examples guide;
- Cloze guide;
- card CSS/mobile/night-mode guide;
- type-in-the-answer guide;
- audio/image guide;
- Basic vs Cloze guide;
- recognition vs Production guide;
- Basic/reversed guide;
- tags vs decks guide;
- sentence-mining guide;
- AI-assisted vs manual mining guide;
- new-card/FSRS workload guides;
- APKG checker/import guidance;
- blog index and related workflow pages.

Official Anki documentation was also checked for the technical claims adopted here, especially:
- card template HTML/CSS;
- right-to-left text;
- night mode selectors;
- answer scrolling through `id=answer`;
- platform/client differences.

## Exact free-template pack audit

The dedicated free-template page and the downloadable plain-text pack were later inspected directly, not only through the surrounding blog guidance:

- `language-learning-starter-deck.txt`;
- `front-template.html`;
- `back-template.html`;
- `README.txt`;
- the dedicated styling guidance associated with the pack.

The pack is deliberately transparent:

- seven semantic fields: Target sentence, Meaning, Context, Source, Audio, Image, Notes;
- ordinary Anki field replacements + HTML/CSS;
- no JavaScript;
- no bundled media;
- no APKG database or scheduling history;
- empty optional Audio/Image values instead of broken placeholder references;
- source/provenance retained separately;
- preview in Anki Desktop before syncing/bulk use.

### Why this repository is not copying the seven-field schema

The free pack uses `Context` for a short **situational/scene cue** shown around the target sentence.

This repository already separates the same roles differently:

- `Context` inside the generated Anki note is the self-orienting `<TargetLanguage> — <Skill>` header;
- `prompt` carries the learner-facing instruction and may also contain the concise situation/context that defines the retrieval task;
- `base_text` carries contextual meaning/translation;
- `source` preserves provenance/locator;
- media and Notes remain separate.

Renaming the current `Context` field or adding another schema field solely to mirror VidToAnki would force another model migration without adding retrieval capability. That is not justified.

What **is** worth making explicit is the semantic contract for `prompt`: it may contain a concise situation/scene cue when that improves retrieval without leaking the answer.

### Transparency/portability invariant reinforced by the pack

The pack's strongest technical property is that a learner can inspect every essential behavior before import. The repository already follows that design in practice, so this source justifies making it an explicit invariant:

> Generated templates must not depend on JavaScript or remote web assets for essential card behavior.

Ordinary Anki HTML/CSS/field replacements remain the baseline. This reduces mobile/client variance and makes generated card behavior auditable.

## What the site consistently argues

Across the related pages, the same design model repeats:

1. Start from the **retrieval job**, not from a favorite note type.
2. Keep one primary target.
3. Separate semantic content into stable fields.
4. Reveal verification/support only after the attempt unless it defines the prompt.
5. Use media only when it changes the retrieval task or preserves useful context.
6. Do not multiply cards merely because a note has enough fields.
7. Treat generated/imported decks as software-like artifacts that need structural checks and representative real-device review.
8. Keep templates simple, inspectable, mobile-friendly, night-mode-safe, and robust to different writing systems.

## What already matched this project

The project already covers nearly all pedagogical recommendations:

- one primary retrieval target;
- Reading, Listening, Production, Pronunciation/Sounds as distinct skills;
- no automatic reverse cards;
- selective Cloze;
- type-in only when exact form/spelling is the target;
- contextual meaning rather than dictionary dumps;
- structured fields;
- source timestamps/locators;
- selective media;
- sentence mining and near-i+1;
- human/AI judgment before cards enter the queue;
- review-cost-aware card counts;
- read-only-first maintenance and leech diagnosis;
- skill decks plus sparse content tags;
- APKG validation and media validation.

The site’s “one rich note → several optional card types” architecture was reconsidered but is still **not** adopted. This repository intentionally keeps one planned card per note because selective sibling routing, idempotent live delivery, per-card prompts/media, and migration safety currently outweigh native sibling-note convenience.

## Useful technical gap found

### Generated templates were not fully portable across night mode and bidirectional scripts

The current `Anki Language v3` templates explicitly set a white background and dark text, but had no night-mode override.

They also used left-aligned wrappers without per-field direction handling. That is weak for Arabic, Hebrew, Persian, mixed-script examples, and other bidirectional content.

Official Anki documentation confirms:
- `.card.nightMode` / `.nightMode ...` selectors are supported;
- RTL fields can be wrapped with a `dir` attribute;
- template HTML/CSS should be tested across clients;
- `id=answer` gives Anki a stable answer-scroll anchor on long cards/mobile.

## Adopted

### 1. Portable v4 template baseline

Newly generated cards use **Anki Language v4** models so existing v3 note types are not silently restyled or structurally mutated.

The v4 baseline:
- adds night-mode colors;
- adds responsive padding/box sizing;
- uses `dir="auto"` on dynamic language-bearing fields;
- uses logical `text-align: start` so RTL fields align naturally;
- adds safe wrapping for long text;
- centers/scales images without changing their learning role;
- adds `<hr id="answer">` so long cards can scroll to the answer boundary correctly.

This is a presentation/portability migration only. No card-plan schema or deck architecture changes.

### 2. Structural validation is not rendering validation

The workflow already validates APKG structure, counts, decks, and media. The VidToAnki checker correctly emphasizes that a structurally valid APKG can still render poorly on a specific Anki client.

The contract therefore now states:
- deterministic validation proves package structure, not every client’s final rendering;
- after a meaningful template/model migration, spot-check representative cards in Anki before large-scale adoption;
- useful edge cases are long text, empty optional fields, media, night mode, and target scripts such as RTL text.

This is a human QA boundary, not a reason to add browser automation or JavaScript.

## Ideas intentionally not adopted

- switching to one rich note that automatically generates Reading + Listening + Cloze + Production;
- making Basic recognition mandatory for every mined sentence;
- creating fixed 3–5 or 5 new-card/day presets from the site;
- adopting a one-language-main-deck architecture in place of the project’s skill subdecks;
- adding JavaScript or remote assets to generated cards;
- creating type-in cards by default;
- requiring screenshots/video clips when audio/text is enough;
- importing the site’s exact field names as a new schema;
- adding a separate external APKG-checker dependency when the repository already has deterministic validation.

## Net changes justified

1. Introduce **Anki Language v4** template models for portability.
2. Add night-mode-safe and bidirectional-text-safe HTML/CSS.
3. Add the answer scroll anchor for long/mobile cards.
4. Document that Anki client preview remains the final rendering authority after structural validation.
5. Add regression tests for these guarantees.
6. Make inspectability explicit: generated templates do not depend on JavaScript or remote assets for essential behavior.
7. Clarify that `prompt` may carry concise situational/scene context, avoiding an unnecessary schema/model migration just to copy the free template's field names.

No card-plan schema, deck hierarchy, media provider, scheduler, installer, or AnkiConnect protocol change is justified.
