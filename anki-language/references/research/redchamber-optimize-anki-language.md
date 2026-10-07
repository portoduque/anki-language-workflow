# Dream of the Red Chamber — “How To Optimize Anki For Language Learning” — Selective Adaptation Note

Source analyzed:

- YouTube: https://youtu.be/31JgmKm78co
- Channel: Dream of the Red Chamber
- Published: 2025-08-15
- Duration: 17:53

The complete spoken transcript was reviewed from start to finish, including:

- note vs. card terminology;
- note types;
- semantic fields instead of generic Front/Back;
- Chinese traditional/simplified forms;
- pinyin/reading fields;
- grammar/language/audio fields;
- tags;
- custom card templates;
- meaning cards;
- reading-aloud cards;
- listening cards;
- handwriting cards;
- conditional card generation;
- simplified/traditional selective cards;
- custom databases vs. shared decks.

## What already matched this project

### One retrieval target per card

The video's strongest card-design rule is to test one specific thing at a time.

This is already a non-negotiable project rule.

### Semantic card context

The video adds language/grammar instructions to make mixed reviews self-explanatory.

The project already renders `<TargetLanguage> — <Skill>` on every front.

### Reading and Listening are distinct skills

Already covered:
- Reading uses written target-language input;
- Listening is audio-first;
- Production is separate;
- Pronunciation & Sounds is separate when needed.

### Sparse/manageable tags

The video recommends tags but warns against letting them become unmanageable.

This matches the project's sparse-tag policy.

## Useful ideas adopted

### 1. Distinct linguistic data deserves distinct structured fields

The video demonstrates why generic `Front` / `Back` fields are limiting. It stores Chinese text, definition, pinyin, grammar, simplified form, sound, and language separately.

This was a real gap in the current workflow.

Adaptation:

The card-plan contract now supports:

- `reading` — pinyin, kana, romanization, or another reading aid;
- `variant` — alternate script/spelling/orthographic form;
- `grammar` — concise grammatical attribute such as gender, noun class, part of speech, or form.

These remain optional. They are rendered conditionally and delivered as separate Anki fields.

Why this is better:
- preserves clean data;
- makes future search/filter/template changes easier;
- avoids hiding useful structured information inside `Notes`;
- remains language-agnostic.

### 2. Reveal non-target information to isolate one skill

The video deliberately shows pronunciation when testing meaning, and hides pronunciation when testing reading aloud.

The useful principle is not those exact templates; it is **task isolation**.

Adaptation:

- if a dimension is not the retrieval target, it may be shown as support when that makes the target clearer;
- the actual answer must stay hidden;
- the same piece of information can be support on one card and the answer on another.

Examples:
- meaning card: reading aid may be visible if decoding is not the target;
- script-decoding/pronunciation card: meaning may be visible while reading aid is hidden;
- Production: semantic context may be visible while target wording remains hidden.

### 3. Active handwriting can be treated as Production when useful

The video creates dedicated handwriting cards for Chinese.

The workflow does not add a new deck. Handwriting/written recall is an output skill and can be represented as `production` when independently useful.

This is especially relevant for:
- Chinese characters;
- Japanese kanji/kana;
- Arabic script;
- other writing systems where active written recall is a real learner goal.

Do not generate handwriting cards by default.

## Anki architecture audit

The video uses one rich note to generate several card types.

Current official Anki documentation confirms that:
- one note type may generate multiple card types;
- conditional replacement can control selective card generation;
- Card Template Deck Override can route card types into different decks.

Sources:
- https://docs.ankiweb.net/manual/templates/generation
- https://docs.ankiweb.net/manual/templates/intro

### Why this repository is NOT switching to multi-card notes yet

The current workflow intentionally produces one Anki note per selected planned card.

A grouped rich-note model could provide:
- native sibling relationships;
- shared metadata;
- conditional skill cards;
- possibly simpler manual editing.

But switching now would increase complexity in:
- the card-first JSON plan;
- per-card prompts and hints;
- per-card audio/image placement;
- AnkiConnect live insertion/update logic;
- stable idempotency;
- model migration;
- selectively routing cards to skill subdecks.

The official Anki model makes grouped notes technically possible, but the learning benefit does not currently justify the implementation cost.

Therefore the project adopts **rich semantic fields** without adopting automatic “one note → six cards”.

This decision should be revisited only if the workflow gains a concrete use case where sibling behavior/shared-note editing materially outweighs the extra complexity.

## Ideas intentionally NOT adopted

### Automatic generation of six skill cards from every note

The video ends with one note producing six card types.

Rejected as a default.

The project continues to require independent learning value for every generated card.

### Separate note type for every language as a universal rule

The video uses separate note types partly to avoid same-spelling duplicates across languages.

This workflow already stores target-language identity explicitly and uses language-specific decks plus stable external ids.

Separate note types per language are therefore unnecessary as a universal project rule.

### Always playing audio twice

The video places sound on both front/back for some cards.

Not adopted as a default:
- audio placement follows the skill;
- duplicated playback adds review time;
- use it only if there is a real learning reason.

### Ready-made decks are always bad

The video strongly recommends making your own database instead of downloading decks.

The project keeps a more nuanced rule:
- personally encountered material is usually better;
- shared/frequency decks can still be useful bootstrap candidate sources for absolute beginners;
- never bulk-import blindly.

### Creating card types merely because fields exist

Structured fields increase flexibility, but they do not create learning obligations.

A `variant`, `reading`, or `grammar` field does not automatically justify another card.

## Model migration

Adding `Reading`, `Variant`, and `Grammar` changes the generated Anki note-field contract.

Newly created notes therefore use **Anki Language v3** note types so an existing v2 note type is not silently mutated or rejected by AnkiConnect.

Existing live-delivered cards remain untouched. Stable workflow tags continue to prevent already-created card ids from being inserted again.

## Net changes justified by this source

1. Add structured `reading`, `variant`, and `grammar` fields to the card plan and generated Anki note types.
2. Add an explicit “reveal non-target support to isolate the intended skill” rule.
3. Treat handwriting/written recall as optional Production rather than adding another deck.
4. Clarify the deliberate current one-note-per-planned-card architecture and document the multi-card-note trade-off.

No new deck, media provider, installer dependency, or automatic sibling-card quota is justified by this source.
