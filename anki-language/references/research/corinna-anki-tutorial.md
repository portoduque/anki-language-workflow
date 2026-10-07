# Corinna Languages — “How to Learn a Language with Anki (Tutorial)” — Selective Adaptation Note

Source analyzed:

- YouTube: https://youtu.be/8GnsTxkuePg
- Channel: Corinna Languages
- Published: 2026-05-27
- Duration: 14:48

The complete transcript was reviewed from start to finish, including:

- why Anki / spaced repetition;
- installation;
- decks and Basic / reversed cards;
- Cloze;
- custom fields and pronunciation recording;
- Fluent Forever picture/all-purpose cards;
- Forvo Pronunciation Downloader;
- Review Heatmap;
- grammar-card extra information;
- AnkiWeb/mobile sync;
- daily limits/settings;
- common mistakes and practical tips.

## What the video mostly confirms

A large portion was already covered by this project:

- spaced repetition / daily review;
- selective use of Basic/reverse behavior;
- no automatic reverse-card generation;
- Cloze only when the target is constrained;
- custom fields for pronunciation, examples, notes, media, and provenance;
- concrete images can improve vocabulary cards;
- pronunciation/audio can materially help difficult cards;
- original/user context is preferable to random word lists;
- Forvo is optional and not a core automation dependency;
- Review Heatmap is optional and motivational, not pedagogically essential;
- sync/mobile behavior belongs in the technical Anki reference layer;
- media must be selective and validated.

No architecture change was needed for those points.

## Useful ideas adopted

### 1. Separate capture from card commitment

The video describes collecting unknown words while watching/reading, and in books sometimes underlining first and adding later after the chapter.

Adaptation:

- an encountered unknown word/phrase becomes a **candidate**, not an automatic card;
- preserve sentence/timestamp/source context when practical;
- batch the selection decision after the current passage/chapter/clip when that reduces interruption;
- still allow immediate creation for obviously high-value items with sufficient context.

This improves both study flow and card quality.

### 2. Creation/customization time is a real cost

The video explicitly warns against spending more time customizing cards than reviewing them.

Adaptation:

- the workflow now treats creation time as part of the efficiency objective;
- do not over-invest in decorative formatting, perfect-image hunting, redundant pronunciation variants, or long explanations;
- use automation to reduce friction, not to justify more decoration;
- prefer the simplest card that trains the intended retrieval effectively.

### 3. Concise grammar explanation on the back can help

The video adds brief AI/web grammar explanations to the extra-info field for harder grammar/conjugation cards.

Adaptation:

- a short back-side rule/contrast is useful when it explains **why the answer is correct** or prevents a predictable confusion;
- do not paste full conjugation tables or long AI dumps by default;
- the retrieval target stays on the front; explanation stays secondary on the back.

### 4. Personally encountered context beats random lists

The video criticizes random shared decks and generic word lists because they lack personal/contextual meaning.

Adaptation:

- personally encountered material is preferred when available;
- shared decks/frequency lists may still be useful **candidate sources**;
- they are not banned, but every entry must pass the same usefulness/context/review-cost filter.

## Ideas intentionally NOT adopted

### Rigid “images instead of translations”

The speaker reports using images rather than English translations and finding them more memorable.

This project keeps a selective policy:

- images for concrete/visual concepts when they improve retrieval;
- configured base-language cues remain valid when clearer, faster, or less ambiguous;
- no translation ban.

### Google Images as the default image pipeline

The video manually uses Google Images.

This project already has a safer automated media pipeline using Openverse/Wikimedia with provenance/license filtering and functional validation.

### Forvo add-on as the core audio pipeline

The video uses the Forvo Pronunciation Downloader add-on.

This project keeps Forvo optional because the add-on runs inside Anki and is not a stable cross-agent API. Automatic audio remains user/native-permitted audio first, then Piper TTS.

### Universal 20 new / 200 review rule

The video describes the default 20 new cards/day and 200 reviews/day, then says reviews should generally be around 10× new cards and that she personally raised her limits.

Current official Anki documentation does use 20 new cards/day → roughly 200 reviews/day as an **illustrative workload example**, and recommends lowering new-card intake when review burden becomes too high. It does not justify a universal project rule that everyone must use a fixed 10× ratio.

This workflow therefore does **not** set or recommend a universal numeric quota. Current Anki/FSRS documentation remains authoritative for scheduling.

Official reference:
- https://docs.ankiweb.net/manual/deck-options

### “Just do three cards” habit rule

The video suggests doing only three reviews on low-motivation days to preserve the habit.

This may be useful motivational advice, but it is outside the card-generation workflow and is not promoted to a skill rule.

### Review Heatmap as required

Useful for motivation/consistency visualization, but it does not improve scheduling or card quality by itself. It remains optional in the add-on reference.

### Browser/mobile limitations as permanent workflow rules

UI limitations can change by Anki version. They belong in the current technical Anki reference layer, not in permanent pedagogical rules.

## Net effect

The video does not justify new card types, new decks, new schema fields, or new media providers.

Its real contribution is narrower:

1. **candidate capture before card commitment**;
2. **creation-efficiency as part of the cost function**;
3. **short grammar explanations only when they prevent confusion**;
4. **personally encountered context preferred over blindly imported lists/decks**.
