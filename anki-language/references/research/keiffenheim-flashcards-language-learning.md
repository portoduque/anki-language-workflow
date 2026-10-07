# Eva Keiffenheim — “The Smartest Way to Use Flashcards for Language Learning” — Selective Adaptation Note

Source analyzed:

- https://evakeiffenheim.substack.com/p/how-to-use-anki-for-language-learning
- Published: 2026-05-25

Access note: the publicly accessible portion was reviewed in full. The article advertises additional sections below a Substack access gate (“5 Rules of Card Design”, “Flashcard Audit”, “Level-by-Level Roadmap”, and “60-Minute Formula”), but those sections were not accessible anonymously. They are therefore **not inferred, reconstructed, or treated as source evidence** here.

## What the accessible article argues

The article’s central claim is that spaced repetition is a **memory layer inside a broader language-learning method**, not a complete method by itself.

It frames a balanced program using Paul Nation’s Four Strands:
- meaning-focused input;
- meaning-focused output;
- language-focused learning;
- fluency development.

It also distinguishes:
- explicit recall from fluent application;
- vocabulary/form retention from real-time language use;
- initial deliberate learning from the richer semantic knowledge built through repeated natural encounters.

The article says Anki is especially useful for:
- early high-frequency vocabulary;
- explicit grammar/form knowledge;
- low-frequency vocabulary that may not recur naturally for a long time;
- pronunciation work;
- collocations/chunks.

It warns against:
- substituting card review for listening/reading;
- context-stripped cards;
- expecting card success to equal speaking fluency.

## What already matched this project

### Anki supports retrieval; it does not replace language use

Already explicit in the project:
- Anki should make learned material retrievable;
- it does not replace reading, listening, speaking, or writing;
- Reading, Listening, Production, and Pronunciation are distinct skills.

No new architecture is needed.

### Context matters

The project already prefers contextual words/chunks, near-i+1 material, natural examples, and meaning-first mining.

No rule such as “isolated vocabulary is always forbidden” is added; isolated items remain acceptable when they are clear, useful, and efficient.

### Production/fluency transfer is not automatic

The project already distinguishes recognition from production and explicitly treats real-world output gaps as evidence for targeted Production candidates.

Success on an Anki card is not treated as proof of conversational fluency.

### High-frequency bootstrap

The article mentions an early core of roughly 2,000–3,000 high-frequency words. The project already has a beginner bootstrap exception using vetted shared/frequency sources.

The numeric milestone is **not** adopted as a mandatory threshold.

### Grammar, pronunciation, chunks

The project already has:
- retrieval-intent-based grammar card selection;
- selective language-specific grammar/form targets;
- Pronunciation & Sounds;
- minimal-pair guidance;
- preference for useful chunks/collocations.

## Useful refinement adopted

### Natural re-encounter scarcity can increase card value

The article highlights one practical reason SRS remains useful even in an immersion-heavy approach: some useful words/forms are encountered too rarely for natural exposure alone to reinforce them soon.

This adds one missing selection factor.

When deciding whether a candidate deserves a card, consider not only:
- usefulness;
- clarity/context;
- distinctness;
- future review cost;

but also **expected natural re-encounter frequency**.

Adaptation:
- a useful low-frequency/domain-specific item may deserve a card precisely because natural input is unlikely to reinforce it soon;
- a very frequent/easy item that the learner already encounters constantly may not need a card if natural exposure is already doing the reinforcement work;
- rarity alone is never enough — obscure low-value items should still be skipped;
- this is a prioritization signal, not a numeric frequency threshold.

The intended question becomes:

> Is this item useful enough that, without deliberate review, natural exposure is unlikely to revisit it soon enough?

## Ideas intentionally NOT adopted

### Fixed 2,000–3,000-word threshold

Useful as a rough pedagogical intuition, not a workflow switch.

### “Four Strands = exactly 25% each” as a card-generation rule

The Four Strands are broader curriculum design guidance. This repository generates and maintains Anki material; it should not enforce daily study percentages.

### “Anki builds the dictionary entry, immersion builds the semantic web” as a literal architecture

Useful explanatory framing, but not a data-model requirement.

### Any inaccessible below-gate recommendations

The inaccessible “5 Rules”, “Flashcard Audit”, roadmap, and time formula are not guessed from headings and are not added to the workflow.

## Evidence check

The article’s Four Strands framing is consistent with Paul Nation’s published model: meaning-focused input, meaning-focused output, language-focused learning, and fluency development.

Its broader warning that retrieval success does not automatically equal fluent real-world application is also consistent with the project’s existing skill-separation and transfer rules.

## Net changes justified by the accessible source

1. Add **expected natural re-encounter frequency** as a candidate-selection factor.
2. Add a behavioral eval for useful rare/domain-specific items versus trivial obscure items.
3. Record the access limitation so future work does not pretend the gated sections were reviewed.

No schema, note model, deck architecture, media provider, scheduler, installer, or AnkiConnect change is justified.
