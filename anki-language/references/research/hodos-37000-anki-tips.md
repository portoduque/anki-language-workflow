# Hodos — “After 37 000 Cards, These Are My Top 10 Anki Tips for Language Learning” — Selective Adaptation Note

Source analyzed:

- YouTube: https://youtu.be/nBpOIywo8so
- Channel: Hodos
- Published: 2026-06-11
- Duration: ~14:04

The complete spoken transcript was reviewed from start to finish, including:

- micro-context sentences;
- listening/phonological priming;
- one-definition vocabulary cards;
- mnemonic associations and cognates;
- minimizing the base language;
- “overlearning” with multiple cards/custom note types;
- FSRS desired retention;
- monthly deck switching;
- leeches;
- strict grading/exact wording;
- the “two-second rule” and timers;
- Cloze with hints/images;
- manual post-session review.

## Useful ideas adopted

### 1. One primary sense/usage per card

The video describes an early mistake: copying several dictionary translations for one polysemous word onto one card and trying to recall all of them.

This aligns with the project's atomicity rule and strengthens the newer polysemy guidance.

Adaptation:

- inspect multiple contexts before encoding a polysemous target;
- prefer **one primary sense/usage per card** when a list of glosses would overload retrieval;
- let context carry secondary nuance;
- create another card only when another sense is distinct, useful, and independently worth reviewing.

This is not “one dictionary definition forever.” It means one retrieval target per card.

### 2. Mnemonics can be useful scaffolding

The video recommends cognates and keyword/sound associations.

This idea is supported by vocabulary-learning research on the keyword mnemonic method, including work combining keyword mnemonics with retrieval practice.

Adaptation:

- use a mnemonic selectively for genuinely difficult items;
- keep it secondary/back-side so the real target is still retrieved;
- verified cognates/borrowings/etymological relationships may be especially efficient;
- an invented sound-alike association is allowed but must be labeled as a mnemonic, not etymology;
- AI may propose mnemonic candidates but may not invent linguistic ancestry or false cognate relationships.

Research references:
- https://doi.org/10.1016/j.heliyon.2024.e25212
- https://doi.org/10.1016/j.learninstruc.2007.02.008
- https://doi.org/10.1016/S0959-4752(97)00016-9

## Already covered

### Micro-context / sentence learning

The project already prefers contextual words/chunks and selective near-i+1 sentence mining. No new architecture is needed.

### Multiple retrieval angles

The video's “overlearning” idea overlaps with the project's selective multi-card reuse of one source.

The project keeps the stricter rule: multiple cards are valid only when each trains a genuinely distinct useful retrieval skill. Automatic duplicate/doubled cards are not adopted.

### Cloze with hints

Already covered. Cloze is allowed only when the intended target is constrained and clearer/faster than direct production.

### Images

Already covered. Images are selective and functional, not mandatory decoration.

### FSRS desired retention

Already covered by the current Anki reference:
- ~0.90 is a reasonable default;
- raising desired retention increases workload sharply;
- use learner-specific workload/simulator guidance instead of copying a creator's preset.

## Ideas intentionally NOT adopted

### “Listen before every Anki review”

The video recommends listening through the sentences before active review to prime them and activate the phonological loop.

Useful distinction:

- pre-exposure/listening can be useful during **initial learning** or source study;
- immediately replaying the exact answer before a due retrieval would cue the answer and weaken the diagnostic value of active recall.

The workflow therefore keeps audio-first Listening cards and optional audio support, but does not mandate pre-listening to the exact due material before every review.

The strong claim that reading hardly activates phonological working memory is also not promoted as a project rule.

### Rigidly minimize the base language

The speaker prefers target-language production and regards target→English cards as wasted effort.

The project keeps a more nuanced rule:
- recognition and production are different skills;
- use the configured base language when it creates the clearest/fastest cue;
- do not create automatic reverse cards;
- do not ban translation for methodological purity.

### Automatic “doubled” cards / overlearning

Rejected as a default.

Every extra sibling creates future review cost. Duplicate exposure is only justified when it trains a distinct retrieval target or skill.

### Monthly deck retirement

The video suggests switching to a new deck roughly every month and later giving the old deck one final pass.

Not adopted:
- worthwhile mature cards are exactly where long-term spaced repetition provides value;
- abandoning a deck to avoid reviews throws away scheduled spacing;
- workload should instead be controlled by new-card intake, pruning, leech repair, redundancy removal, and workload-aware FSRS settings.

### Leech threshold = six + automatic suspension as universal setting

The project keeps leeches as a **diagnostic**:
- ambiguous prompt?
- overloaded target?
- wrong answer/media?
- missing context?
- low-value item?

Suspending/deleting low-value cards can be correct, but a fixed six-lapse threshold is not made universal and valuable content should be repaired when possible.

### Exact wording must always be reproduced

The video recommends pressing Again when wording differs even if the alternative wording is not strictly necessary.

Rejected because it conflicts with the project's semantic-success rule.

Exact wording is required only when wording, collocation, morphology, spelling, or word order is itself the target. A natural equivalent is acceptable when the card tests meaning or valid usage.

### “Two-second rule” = Again

This conflicts with current official Anki semantics.

Official Anki says:
- Again = incorrect / could not recall;
- Hard = correct but doubtful or slow;
- Good = correct with normal effort;
- Easy = correct with little/no effort.

The manual suggests moving on if the learner still cannot answer after roughly 10 seconds, but this is an anti-stalling heuristic — not a universal fail threshold.

Therefore a correct answer that takes >2 seconds is **not automatically Again**.

### On-screen timer “limits” the card

The video describes setting the on-screen timer to ~3 seconds as if this limits the review.

Current Anki documentation says:
- normal answer time does not influence scheduling;
- Maximum answer seconds caps recorded statistics;
- the on-screen timer displays elapsed time;
- automatic timed actions require the separate Auto Advance feature.

The project's scheduling reference was updated to make this explicit.

### Mandatory manual extra review after each session

The speaker recommends manually replaying difficult items for ~60 seconds after each session.

This may be a useful personal study habit, but it is not promoted to a workflow rule:
- Anki already schedules failed/difficult cards;
- hard items should first be diagnosed for card-quality problems;
- extra unscheduled repetition is optional, not required.

## Net changes justified by this source

1. Add **one primary sense/usage per card** to polysemy handling.
2. Add **selective mnemonic scaffolding**, with strict distinction between verified cognates/etymology and invented keyword mnemonics.
3. Explicitly reject arbitrary 2–3 second fail thresholds; slow-but-correct recall maps to Hard under current Anki semantics.
4. Clarify that normal Anki timers do not affect scheduling.
5. Clarify that arbitrary monthly deck retirement is not a workload-management strategy.

No schema, builder, media provider, deck architecture, or AnkiConnect change is justified by this source.
