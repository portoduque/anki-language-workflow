# Jeremiah’s Language Ideas — “My 7 Rules For Using Anki (For Language Learning)” — Selective Adaptation Note

Source analyzed:

- YouTube: https://youtu.be/Yn1YP1M8dzA
- Channel: Jeremiah’s Language Ideas
- Published: 2025-09-24
- Duration: 12:05
- Matching author-written seven-rule post: https://www.reddit.com/r/languagelearning/comments/1ohvcad/7_rules_to_make_anki_way_more_fun_and_efficient/

The video transcript and the author’s matching written version were reviewed across all seven rules:

1. only one unknown element per card;
2. audio-only fronts except when reading is the skill being trained;
3. learn vocabulary in full-sentence context;
4. optimize reviews for “instant understanding” by learning/clarifying the item before review;
5. simplify grading with a Pass/Fail add-on;
6. retire cards after they stop being useful;
7. allow breaks instead of letting Anki become the goal.

The source is useful, but several recommendations are personal workflow choices rather than universal Anki rules. The project therefore keeps only the parts that survive comparison with the existing pedagogy and current official Anki behavior.

## Already covered

### One unknown / near-i+1 context

The project already has a stronger version of Rule 1:

- one primary retrieval target per card;
- prefer near-i+1 sentence mining;
- surrounding context should already be understood;
- if several independent unknowns compete for attention, choose a cleaner sentence, split targets, or skip it.

No additional card type or schema change is needed.

### Audio-first Listening

Rule 2 matches the existing Listening architecture:

- Listening is audio-first;
- transcript stays off the front;
- transcript and base-language meaning/explanation belong on the back.

The video’s broader “audio only unless reading is the goal” advice is **not** promoted to a universal rule because this workflow deliberately separates Reading, Listening, Production, and Pronunciation. Production needs a semantic/context prompt on the front, and Pronunciation/Sounds may require a written cue or an audio discrimination cue depending on the actual skill.

### Context-rich vocabulary

Rule 3 reinforces the project’s preference for useful context, chunks, collocations, and sentence mining.

The rigid word **always** is not adopted. A full sentence is valuable when it clarifies meaning, usage, collocation, or sound, but a shorter chunk, collocation, isolated form, minimal pair, or spelling/sound item can be the better retrieval unit when that is the knowledge being trained.

## Useful ideas adopted

### 1. Clarify the target before scheduling it

Rule 4 contains one useful distinction that was present only implicitly in the project: a scheduled review should normally test retrieval of a target whose intended meaning/use has already been clarified, rather than making repeated Anki failures perform first-time semantic discovery.

Adaptation:

- an encountered unknown remains a candidate until the intended sense/form/context is understood well enough to encode;
- first exposure or clarification may happen immediately before card creation;
- prior mastery is **not** required;
- an absolute beginner may still use vetted bootstrap material;
- if meaning, register, transcription, or intended usage is still ambiguous, clarify it before scheduling the card.

This complements the existing meaning-first and candidate-before-card rules without turning source study into a mandatory ritual.

### 2. Binary grading can be done natively

Rule 5 recommends a Pass/Fail add-on to remove decision friction.

The underlying simplification can be useful, but the add-on is not required. Current official Anki documentation explicitly says that learners who find four answer buttons difficult may use only:

- **Again** for incorrect / not recalled;
- **Good** for correct.

Hard and Easy remain valid ratings. They do not inherently “ruin” FSRS or the scheduler. The problem is inaccurate grading, such as using Hard for a forgotten card.

Adaptation:

- document native Again/Good-only grading as an optional simplification;
- do not require a Pass/Fail add-on;
- do not claim that Hard/Easy inherently damage the algorithm.

Official source:
- https://docs.ankiweb.net/manual/studying

### 3. A break does not require deleting or restarting the deck

Rule 7 is correct that Anki should remain a tool and that missed days are not a reason to abandon language learning.

However, the video goes further and suggests deleting a deck when review pressure becomes stressful. That is not adopted.

Current Anki documentation says that after a long break the learner can simply resume; overdue delay is taken into account when the next interval is calculated.

Adaptation:

- do not turn daily streak perfection into a workflow requirement;
- after a break, resume the useful deck instead of deleting/resetting it merely because reviews accumulated;
- temporarily reduce new cards and handle the backlog sustainably when needed;
- prune or suspend cards for evidence-based low value, redundancy, or bad design — not because a calendar threshold elapsed.

Official source:
- https://docs.ankiweb.net/manual/studying

## Ideas intentionally NOT adopted

### Universal audio-only fronts

Rejected as a global rule.

Audio-only is correct for Listening, but this workflow is skill-specific. Reading, Production, and Pronunciation/Sounds may require different front information.

### Full sentences for every vocabulary item

Rejected as a universal requirement.

Use the smallest natural context that teaches the useful knowledge. Sometimes that is a full sentence; sometimes a chunk, collocation, word form, or sound contrast is better.

### “Instant understanding” as a pass/fail grading threshold

Fast reviews are a design goal, not a stopwatch rule.

Current official Anki semantics say:
- Again = incorrect / not recalled;
- Hard = correct but doubtful or slow;
- Good = correct with ordinary effort;
- Easy = correct with little/no effort.

The project therefore adopts **clarification before scheduling**, not “anything less than instant = fail.”

### “Hard/Easy break the algorithm”

Rejected.

Current Anki exposes all four buttons intentionally, and its own documentation describes when to use each. A learner may simplify to Again/Good, but Hard/Easy are not inherently harmful.

### Automatic retirement after roughly six months

Rejected.

A mature card with a long interval is not automatically useless. Frequency of natural input, card value, mastery evidence, redundancy, and the learner’s goals matter more than card age.

The existing project rule remains: retire/suspend redundant scaffolds only with reliable mastery evidence and no lost skill gap.

### Deleting the deck after ordinary breaks

Rejected.

Anki explicitly supports returning after a backlog. Deleting/restarting a useful deck discards mature scheduling history and is unnecessary merely because reviews were missed.

## Net changes justified by this source

1. Make **clarify the target before scheduling it** explicit in card-selection and pedagogy rules.
2. Document native **Again + Good only** grading as an optional low-friction alternative to a Pass/Fail add-on.
3. Document that learners can **resume after a long break** instead of deleting/resetting a useful deck.
4. Add behavioral evals/regression tests for those distinctions.

No schema, note model, deck architecture, builder, media provider, installer, or AnkiConnect implementation change is justified by this source.
