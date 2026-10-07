# Anki Forums — Language-learning card structure discussion

Source analyzed:

- https://forums.ankiweb.net/t/best-practice-for-structuring-flashcards-for-long-term-retention-language-learning/63999/4
- Topic: “Best Practice for Structuring Flashcards for Long-Term Retention (Language Learning)”
- Created: 2025-07-14

Important URL detail: the supplied `/4` link points to the automatic system-closure post, not to substantive advice. The full topic was therefore reviewed, including the original question and the substantive replies in posts #2 and #3.

## What the thread discusses

The original poster asks about:
- Q/A versus cloze for grammar;
- audio and example sentences for vocabulary;
- decks versus tags;
- reducing review burden while preserving long-term retention.

The moderator reply contributes the strongest reusable idea:
- choose card design according to the intended retrieval operation;
- distinguish memorizing a rule, recognizing a structure, and applying a structure;
- use audio in its own field;
- keep example sentences as support when they are not the tested target;
- reserve decks/subdecks for groupings normally studied separately and use tags for flexible classification.

A second participant describes a more personal system with topic-specific decks, full grammar tables/cloze, reversible textbook exercises, permanent filtered decks, and deliberately separated study contexts for multiple languages.

## Already covered by this project

### Audio as structured data

The project already stores audio separately from text and other semantic fields. This supports placing audio on different card sides, changing templates globally, preserving exports, and using the same linguistic content without embedding media into a giant HTML field.

No schema or model change is needed.

### Decks classify study function; tags classify content

The thread's “use a deck only when you almost always want to study that grouping separately” heuristic is compatible with the current architecture:

- skill subdecks: Reading, Listening, Production, Pronunciation & Sounds;
- sparse tags/structured fields for vocabulary, grammar, collocation, word form, and related dimensions.

The project deliberately does not create topic microdecks for verbs/adjectives/idioms.

### Examples as support, not automatic extra targets

The project already allows non-target information to appear as support when it isolates the intended retrieval skill. Example sentences therefore belong on the back/hint/support layer unless the sentence itself is the useful retrieval target.

### Native audio versus TTS

The thread prefers native-speaker recordings when available and treats TTS as a fallback. The project already has a compatible priority order and a stricter media-validation/provenance layer.

### Reversed cards are selective

The moderator mentions Basic+reversed for some grammar recognition in a personal collection. The project already has a stronger rule: recognition and production are separate retrieval skills, and reverse cards are never generated automatically.

## Useful refinement adopted

### Grammar card design should start from retrieval intent

The thread makes one distinction worth promoting explicitly.

Before choosing cloze, direct Q/A, Reading, or Production for a grammar item, decide what the learner actually needs to retrieve:

1. **Rule recall** — the learner needs to state/identify a concise declarative rule itself.
2. **Recognition/discrimination** — the learner needs to recognize which structure/form/function is present or which competing form fits a context.
3. **Application/production** — the learner needs to select or produce the correct grammatical form in context.

Adaptation:

- do not memorize a grammar rule merely because a textbook stated it;
- create a direct declarative rule card only when recalling that rule independently is useful;
- prefer contextual Reading/contrast cards when the useful skill is recognition/discrimination;
- prefer constrained Production or a clear cloze when the useful skill is application;
- keep each card to one primary grammatical decision/form;
- never dump a complete paradigm/table onto one card merely because the source presents the rule that way;
- cloze remains optional and must be unambiguous.

This does not add a new skill/deck. Grammar remains content inside the existing skill architecture.

## Ideas intentionally not adopted

### Topic-specific vocabulary/grammar decks by default

The second participant's deck layout is a personal preference. The workflow keeps skill-based subdecks and content tags/fields because that maps directly to retrieval operations and avoids microdeck proliferation.

### Automatic reversible vocabulary/grammar cards

Rejected. Reverse direction is created only when the opposite retrieval is independently useful.

### Complete grammar tables as cloze cards

Rejected as a default because this conflicts with one-primary-target, fast review, and no full-paradigm-by-default rules.

### Permanent filtered decks as required workflow architecture

Not adopted. Filtered/custom decks are study-session tools, not necessary for deterministic card generation.

### Separate language study by time/location/background music

Not adopted. The thread provides anecdotal advice, not evidence strong enough to justify a workflow rule. The project already makes every front self-orienting with target language + skill, which is the reliable card-design safeguard for mixed review.

## Net changes justified

1. Add an explicit grammar retrieval-intent decision before card-format selection.
2. Add a behavioral eval that distinguishes rule recall, recognition, and contextual application.
3. Record the thread so already-covered audio/deck/tag/reverse-card advice is not duplicated later.

No schema, note model, deck architecture, media provider, scheduler, installer, or AnkiConnect change is justified by this thread.
