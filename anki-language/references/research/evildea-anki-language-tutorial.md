# Evildea — “How to Use Anki For Language Learning” — Selective Adaptation Note

Source analyzed:

- YouTube: https://youtu.be/11CPWnGmsas
- Channel: Evildea | Hyperpolyglamorous
- Published: 2026-07-02
- Duration: 17:32
- License shown by YouTube: Creative Commons Attribution

The complete spoken transcript was reviewed from start to finish, including:

- Reading / Listening / Production deck architecture;
- sentence mining from native YouTube material;
- dictionary/AI example lookup;
- multi-context vocabulary cards;
- listening cards and TTS;
- production Cloze cards;
- native/authentic sentence sourcing;
- post-answer shadowing/chorusing;
- programming examples;
- new-card limits, stats, sync, and add-on comments.

## What already matched this project

### Skill-oriented deck architecture

The video separates language practice into:

1. Reading;
2. Listening;
3. Production/Speaking.

This directly matches the core architecture already adopted by this repository. The project keeps an additional fourth deck, **Pronunciation & Sounds**, because pronunciation/sound discrimination is a distinct retrieval skill worth isolating when needed.

No deck-architecture change is required.

### Selective multi-skill reuse

The video demonstrates the same source word/sentence being trained through Reading, Listening, and Production.

This confirms the project's existing rule:

- reusing one source across several decks is valid when each card trains a genuinely different retrieval operation;
- do not automatically create every sibling card.

### Listening is audio-first

The video puts audio on the front and written sentence on the back.

This is already the project's Listening behavior.

### Production audio belongs after retrieval

The video reveals/reference-plays audio after the learner has attempted the Production answer.

This is already the project's Production behavior.

## Useful ideas adopted

### 1. Strong near-i+1 sentence-mining default

The video rejects a candidate sentence when another unknown word competes with the target. It prefers sentences where every other word is already understood.

Adaptation:

- prefer mined sentences where essentially all context is already known except the one primary target;
- one incidental, immediately inferable item may be tolerated when it does not compete with the target;
- if multiple unknowns each demand learning, choose a cleaner sentence, split targets, or skip it.

This strengthens the existing “not overloaded with unknowns” rule without making i+1 an inflexible mathematical requirement.

### 2. Explore multiple contexts before deciding how to encode a polysemous item

The video queries several example sentences to understand the semantic range of a word before creating the Reading card.

That analysis step is useful.

Adaptation:

- inspect several trustworthy contexts when a target may be polysemous or have productive figurative uses;
- identify which senses/usages actually matter;
- then keep the review card concise.

The project **does not** adopt the video's implementation of placing roughly six example sentences on the front. That conflicts with fast review and one-primary-retrieval-target principles.

Preferred encoding:

- one clear front context;
- a small number of supporting examples on the back only when useful;
- separate cards only for distinct useful senses that deserve their own retrieval.

### 3. Production sentences need stronger authenticity/naturalness confidence

The video makes an important distinction: a grammatically possible generated sentence may not be something native speakers naturally say, and that matters more when the learner is actively training speech.

Adaptation:

- for full-sentence/chunk Production targets, prefer attested user/native material;
- dictionary/corpus/native-source examples are useful when the original material is unsuitable;
- AI-generated production sentences are allowed only when naturalness, intended meaning, variety, and register have been validated sufficiently;
- when validation is uncertain, prefer a direct semantic production prompt instead of memorizing a questionable generated sentence.

The project does **not** accept the stronger claim that unverified AI sentences are harmless for Reading/Listening. Passive examples must still be correct and natural enough not to teach bad language.

## Ideas useful as optional review behavior, but not promoted to a card-generation rule

### Post-answer shadowing / chorusing

The video recommends listening to the reference audio after revealing a Production answer and shadowing/chorusing it.

This can be useful when pronunciation/prosody is a secondary goal.

It is **not** made mandatory because:

- it increases review time;
- not every Production card needs pronunciation practice;
- the project already has a dedicated Pronunciation & Sounds deck when repeated sound practice independently deserves spaced reviews.

An agent may mention optional post-answer shadowing when pronunciation/prosody is relevant, but should not add it to every Production card or create extra cards solely for it.

## Ideas intentionally NOT adopted

### Six sentences on one Reading front

The video sometimes places around six example sentences for one target word on the same front to build a holistic sense of meaning.

Rejected as a default because:

- the video itself notes such a card can take ~30 seconds to read;
- long fronts increase review cost;
- several contexts can blur the exact retrieval target;
- our workflow already optimizes memory efficiency per review minute.

Multiple examples are valuable during **analysis**, not necessarily during every review.

### Reading deck only for difficult scripts

The video suggests a Reading deck may be unnecessary for a phonetically straightforward language such as Spanish.

The project keeps a more general rule:

- Reading cards are created only when written recognition/comprehension is independently valuable;
- orthographic/script difficulty is one reason, not the only reason.

There is no quota requiring a Reading card for every item anyway.

### Rigid “no translation / no pinyin” Listening back

The video omits translation and pinyin because it assumes reading is already mastered.

The project does not make that universal:

- target transcript belongs on the back;
- base-language meaning/explanation is optional when it helps verify comprehension;
- script/reading support is used only when useful;
- the configured base language remains valid.

### NaturalReaders as a core automatic provider

The video uses NaturalReaders and makes a very strong accuracy claim.

The project does not adopt that provider or accuracy claim.

Existing priority remains:

1. original user/source audio;
2. permitted native-speaker audio;
3. validated TTS.

Piper remains the built-in automatic TTS provider for portability and deterministic validation.

### AI examples accepted without independent validation

The video uses Gemini-generated Reading examples and is much stricter only for Production.

The project keeps a stricter baseline for all skills. Generated examples must still be correct/natural enough to avoid teaching bad language, with an especially high bar for Production.

### Fixed new-card range of roughly 6–20

The video suggests approximately 6–15, 20 maximum for its larger Reading cards.

Not adopted:

- card size/review time really does affect sustainable workload;
- the numeric range is personal and card-format-specific;
- current Anki/FSRS + the learner's real workload remain authoritative.

### No-add-ons stance

The speaker personally does not bother with add-ons.

This is preference, not a design rule. This repository keeps an add-on reference library and uses AnkiConnect when it materially improves automation.

### Mandatory tags/no-tags behavior

The video does not use tags.

The project keeps sparse tags where they materially help linguistic/source classification; no tag quota exists.

## Programming section

The programming section demonstrates typed Cloze/contextual recall for code.

It is outside the scope of this language-specific skill and does not justify expanding the repository into a generic programming-memory workflow.

The general principle — make context constrain the intended answer — already exists in the language card rules.

## Net changes justified by this source

1. Make **near-i+1** sentence mining an explicit strong default.
2. Add **polysemy/context exploration before card commitment**, while explicitly preventing multi-sentence front bloat.
3. Add a **higher authenticity/naturalness gate for full-sentence Production targets**.
4. Record shadowing as an optional review behavior, not an automatic card-generation requirement.

No schema, deck architecture, builder, media provider, or AnkiConnect change is justified by this source.
