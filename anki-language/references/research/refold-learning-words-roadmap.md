# Refold Roadmap — Learning words with Anki

Primary source:
- https://refold.la/roadmap/library/learning-words-with-anki

Reviewed in full: What Is Anki?, What Anki Does and Doesn't Do, Getting Set Up, Recommended Settings, How to Study, Tips for Long-Term Success, Where to Get a Deck, When to Move Beyond Pre-Made Decks, and Research and Reasoning.

The roadmap sidebar/submenus were also expanded so the article was interpreted in context: Phases 0–7, Phase X, and the relevant Library references, especially Sentence Mining, Sentence Mining While Listening, Vocabulary Size, Habit Health, The Pillars of Language Learning, and The Reading-Listening Gap.

## Core model

Refold treats Anki as priming, not complete language acquisition:
- Anki creates an initial retrievable representation;
- natural encounters enrich nuance, usage, register, collocations, and automaticity;
- immersion remains the main acquisition environment.

This already matches the project principle that Anki supports retrieval but does not replace real language use.

## Already covered

- One meaning / limited card scope: already covered by one-primary-sense cards and polysemy analysis.
- Beginner pre-made decks: already covered by vetted shared/frequency decks as candidate sources, never blind imports.
- Sentence mining: already covered by near-i+1 mining, one primary target, candidate-before-card, and usefulness/context/review-cost filtering.
- Listening: already covered by the distinct audio-first Listening skill.
- Again/Good and FSRS: already covered by the Anki reference layer and workload-aware scheduling rules.


## Useful improvement adopted

### Candidate-source strategy should evolve with learner evidence

The best candidate source can change as the learner changes:

1. If there is too little comprehensible personal material, a vetted frequency/shared source may bootstrap candidates.
2. Once useful natural input is comprehensible, personally encountered/context-rich candidates should usually outrank generic lists.
3. When listening is the evidenced bottleneck, audio-first source evidence may justify Listening cards.
4. At advanced levels, real output/domain gaps are valid candidate sources.

Do not hard-code Refold phase numbers or vocabulary counts as switching thresholds. Use learner evidence, available source quality, and actual goals.

### Output/domain gaps are candidates, not literal translations

A repeated speaking/writing gap is useful evidence, but the learner's base-language thought must not become an unverified Production answer.

Preferred flow:
1. capture the intended meaning/situation/domain as a candidate;
2. find or verify a natural target-language expression for the intended variety/register;
3. clarify the useful sense/form;
4. create a Production card only if the gap is useful/recurring enough to justify review;
5. preserve attested context/source when possible.

This extends the existing Production naturalness rule without changing the schema.


## Intentionally not adopted

- required Refold phase field or Phase 0 to 7 workflow state;
- fixed 1k/2k/3k/etc vocabulary thresholds for card-generation decisions;
- fixed 5 to 10 new cards/day;
- mandatory completion of every due review every day;
- fixed 25 to 30 percent study-time cap or phase percentage tables;
- automatic deletion of every difficult card;
- commercial deck/vendor dependencies.

Repeated failure remains diagnosis-first: repair a valuable card when possible, suspend/delete low-value cards when justified, and require approval before mutating an existing collection.

## Technical audit

Current official Anki guidance confirms:
- learners may use only Again + Good;
- new-card intake increases future review load;
- a backlog is a reason to pause new cards;
- review limits may smooth workload peaks;
- FSRS is native and should be tuned using current guidance and learner-specific history.

## Net changes justified

1. Explicit candidate-source progression driven by learner evidence, not fixed stages/counts.
2. Output/domain-gap mining as a valid candidate source, with naturalness verification before Production.
3. Behavioral evals for both.
4. No schema, config, deck, note-model, media, scheduler, installer, or AnkiConnect change.
