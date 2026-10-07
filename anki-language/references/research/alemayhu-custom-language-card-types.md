# Alexander Alemayhu — “Custom Anki card types for language learning” — Selective Adaptation Note

Source analyzed:

- YouTube: https://youtu.be/_etuizTN9xU
- Channel: Alexander Alemayhu
- Published: 2020-10-08
- Duration: 10:40

The complete spoken transcript was reviewed from start to finish, including:

- the argument that languages have different high-value grammatical/lexical features;
- Norwegian noun gender and plural forms;
- verb infinitive/present/preterite/participle forms;
- target-language definitions;
- similar words;
- contextual example text;
- images;
- base-language translation;
- several cards generated from one richer note;
- image → word, definition → word, translation → word, gender, plural, and verb-form retrieval;
- the author's preference for linking concepts directly to target-language words instead of relying only on translation.

## What already matched this project

### Context matters

The project already prefers useful contextual words/chunks, selective sentence mining, and near-i+1 material. No new context rule is needed.

### Target-language definitions are optional

The video uses Norwegian definitions as a cue.

The project already allows a concise target-language definition when the learner can understand it without creating several new unknowns. It does not force monolingual cards.

### Images can cue concepts directly

The video uses images to create a concept → target-language-word relationship.

The project already supports image-based semantic cues and explicitly allows an image to replace a base-language translation when the concept is visually clear.

The stronger “use an image for most words” implication is not adopted. Images remain selective because abstract words, grammar, and many expressions are better disambiguated by text/context.

### Rich metadata does not imply automatic cards

The source builds rich notes containing translation, definition, image, gender, plural, and inflected verb forms, then generates several cards from them.

The project already has the stricter rule that every extra retrieval must independently justify future review cost. Existing structured fields and the current one-note-per-selected-card architecture remain unchanged.

## Useful idea adopted

### Adapt retrieval to high-value language-specific features

The strongest new contribution is the explicit design principle:

> Card selection should respond to the features of the target language instead of forcing the same lexical template onto every language.

Examples from the video include Norwegian:
- noun gender;
- plural form;
- present / preterite / participle forms.

This generalizes beyond Norwegian:

- grammatical gender or noun class;
- irregular or non-obvious plural formation;
- case or agreement forms;
- classifier/counter choice;
- irregular inflection/conjugation;
- aspectual or tense forms;
- script/orthographic variants;
- other language-specific dimensions that are genuinely useful and independently difficult.

Adaptation for this project:

- during source analysis, identify language-specific form/grammar dimensions that matter for actual comprehension or production;
- create a dedicated retrieval only when that dimension is useful enough to deserve repeated review;
- keep **one primary feature/form per card**;
- reveal non-target information when it isolates the tested feature;
- use existing Reading/Production/Pronunciation/Listening skills rather than creating language-specific microdecks;
- store concise labels/support in existing structured fields/tags when useful;
- do not generate a full paradigm merely because the source contains one.

Examples:

- useful Norwegian noun with unpredictable gender → Production card for determiner+noun if active recall matters;
- same noun with an irregular plural the learner needs → separate Production card for that plural only if independently worthwhile;
- verb where only the preterite is irregular and problematic → test that form, not every tense by default;
- fully predictable/automatic morphology → no extra card.

This makes the workflow more language-aware without making it language-specific.

## Ideas intentionally NOT adopted

### One custom note type/template family per language

The video recommends designing note/card types around each language's peculiarities.

The pedagogical idea is good, but implementing one Anki model per language is unnecessary here.

The workflow already has:
- target/base language configuration;
- generic structured linguistic fields;
- four skill-oriented note models;
- language-specific prompts/tags/content.

Creating a new model family for every language would increase migration, testing, AnkiConnect, and maintenance complexity without a demonstrated learning gain.

### Automatic card generation for every available field

The source demonstrates translation → word, definition → word, image → word, gender, plural, and several verb forms from one note.

Not adopted as a quota.

A field or paradigm entry is only a candidate retrieval. Create a card only when that specific skill/form is useful, distinct, clear, atomic, and worth its future review cost.

### Image cards for nearly every word

Not adopted.

Image cues are excellent for concrete/visually distinctive concepts, but weak or ambiguous for many abstract words, grammar items, discourse markers, and expressions.

### Similar-word lists as a default field/card

Not adopted as a default.

Near-synonyms and semantically similar items can create interference. Use a contrast card only when the distinction itself is useful and confusable; do not append lists of “similar words” mechanically.

### Translation should be avoided in favor of concepts

Not adopted as a rigid rule.

The project agrees that concept/image/context cues can be excellent, but base-language translation remains valid when it is the clearest and fastest semantic cue.

### Full paradigms on review cards

Not adopted.

A rich reference note may contain many forms, but the review prompt should usually test one form/relationship at a time. Full paradigm dumps increase answer ambiguity and review time.

## Net changes justified by this source

1. Add an explicit **language-specific feature targeting** rule to card selection and pedagogy.
2. Make the workflow inspect useful grammatical/morphological dimensions during source segmentation without auto-generating cards.
3. Add behavioral evals for selective gender/plural/inflection targeting and for rejecting full-paradigm card explosion.
4. Record this source as research evidence.

No schema, Anki note model, deck architecture, builder, media provider, installer, or AnkiConnect implementation change is justified by this source.
