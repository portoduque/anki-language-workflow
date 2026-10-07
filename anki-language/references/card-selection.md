# Card Selection

Evaluate each source unit independently.

## First question: should this become a card?

Create a card when the item is useful, non-trivial, likely to recur, or exposes a real comprehension, production, listening, or pronunciation gap.

Skip a card when the item is already obvious, redundant, low-value, too context-dependent, or would create disproportionate review cost.

## Skill classification

### Reading

Use when the retrieval target is recognition/comprehension of written target-language material.

### Listening

Use when the learner should understand spoken target-language material without seeing the text first. Audio belongs on the front.

### Production

Use when the learner should actively retrieve a word, chunk, expression, grammatical form, or sentence. The prompt must constrain the intended answer and should be written in the configured base language when an explanation/cue is needed.

### Pronunciation & Sounds

Use for pronunciation production, sound discrimination/minimal pairs, or spelling-sound relationships. Do not create these cards unless sound is actually a learning target.

## Multiple-card decision

One source unit may create more than one card only when each card trains a meaningfully different skill.

Valid example:

- Listening card: target-language audio -> understand/transcribe.
- Production card: base-language meaning/context -> produce the target-language expression.

Invalid example:

- three near-identical recognition cards that differ only in cosmetic formatting.

## Cloze rule

Never create an ambiguous blank that could accept many correct expressions.

Use a semantic/function cue in the configured base language, a provided lemma, or another precise constraint.

Good pattern:

`Complete with the expression meaning <base-language meaning>: <target-language sentence with one constrained blank>.`

Bad pattern:

`<target-language sentence with an unconstrained blank>.`

## Tags

Use sparse tags for useful content dimensions such as `vocabulary`, `chunk`, `collocation`, `grammar`, `word-form`, `word-order`, `expression`, `spelling`, `minimal-pair`, and `sentence-mining`.