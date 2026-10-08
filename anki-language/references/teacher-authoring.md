# Teacher-authored chunks — normative v2.6 policy

## Objective

Act like a **language teacher**, not a transcription copier. Keep 100% of the user-supplied original words and phrases, but turn them into the **smallest defensible collection of short retrieval tasks**. New natural examples are allowed when they teach a transferable construction better than a literal quotation. Keep the four current skills (Reading, Listening, Pronunciation & Sounds, Writing); **never Production**.

## Seven-stage creation loop

1. **Read every source unit fully.** Confirm the target/base language and preserve each exact source sentence/word in `source_units`. Never replace screenshots or audio transcripts with an imagined rewrite.
2. **Mine knowledge, not punctuation.** Identify vocabulary, collocations, reusable grammatical frames, gender/agreement contrasts, natural usage, and potentially tricky sounds. A source line may contain 0, 1 or multiple worthwhile targets.
3. **Draft both authentic and teacher-created chunks.** You may shorten, adapt, recombine or replace details (e.g. a long campus name → `l'université`) to create natural standalone examples. Prefer source words and vocabulary over introducing unrelated new words; new connecting words are allowed only when needed for naturalness. Verify meaning, inflection, register and idiomatic use; if uncertain, choose an attested form or ask.
4. **Rank before adding cards.** Prefer a genuinely useful reusable target, unmastered distinction or common communicative expression. Penalize repetition of trivial greetings, proper-name variants, long institution names, low-value synonyms and prompts that are slow to answer. Never force a card count or skill ratio. Use one primary skill; a sibling requires an independent bottleneck. Do not relabel Production as Writing.
5. **Attach provenance and concise examples.** Every v2.5 card declares `origin: "source"` only when its exact target occurs in a *linked* source unit, or `origin: "teacher"` for an adapted/generated target. Never put a fabricated target in `source_excerpt`. Teacher-created targets must have an accurate base-language meaning. `teaching_examples` (0–2 short objects with `text` and optional `base_text`) are secondary support on the Back, marked "Professor · exemplo criado"; each example must add a distinct usage insight, not repeat the Front. Cards remain fast; no full paragraph memorization.
6. **Separate total source visibility from targeted retrieval.** Preserve all original text verbatim in linked Back Source fields. Record in `teacher_analysis` the lesson's communicative objectives, a concise list of original **priority vocabulary** worth retrieval, and at least one discarded alternative for multi-phrase lessons. Include each priority term in a selected target or natural short example. Other words can remain **context-only**: show them in the unmodified source, report them as such, but do not turn them into low-value cards. This avoids the v2.5 one-source-turn-one-card loophole. For each chosen card explain `learning_goal` and `selection_reason`. Do not game the audit by creating filler or copying every full utterance.
7. **Finalize and generate media.** Ensure each card has a clear prompt when required; check likely semantic near-duplicates, false friends and ambiguous targets. Validate the new plan, then run v2.4-compatible **chunk-first Piper** to synthesize only the final card target (full-source audio opt-in). Report the counts of cards by skill, teacher-created targets, original word forms covered and omissions. Do not modify Anki notes without user consent.

## Important distinction: three types of "coverage"

- **Literal preservation**: every original item occurs in a linked Back Source field, still unchanged.
- **Priority vocabulary use**: high-value words or expressions selected by the teacher must occur in a target or short teacher example. All source words are inventoried; context-only words remain visible, not silently discarded. This is mechanical, not a semantic or mastery guarantee.
- **Active retrieval**: only valuable selected chunks get dedicated questions. It is intentionally **not** 100% of distinct words tested separately.

Never claim that the validator can prove teaching quality, real mastery, pronunciation naturalness, or independent accuracy of screenshots. The AI must check those things before trusting a generated example.

## Example: a campus conversation

Sources:
- `Vous pouvez me suivre, c'est à deux minutes d'ici.`
- `Je travaille ici à l'université.`

Possible selected cards:
- Reading, **source**: `Vous pouvez me suivre` → "You can follow me."
- Reading, **teacher**: `L'université est à deux minutes d'ici.` → "The university is two minutes from here."

One useful answer-side example for the second card:
`Je travaille ici. C'est à deux minutes d'ici.` → "I work here. It's two minutes from here."

This covers the supplied original word forms without two full-sentence recitations or cards for `je`, `me`, `à` etc. The teacher-created chunk remains clearly identified as such. This is an *illustration*, not a hard-coded template or minimum number of cards.

## Distinguish derived from source

- Original quotation → `origin="source"`, card's target must be a whole-phrase substring of a linked `source_units[].text`.
- Newly authored/adapted target → `origin="teacher"`, `base_text` nonblank, no `source_excerpt`. If shown with a short extra sentence, store that in `teaching_examples`.
- All `source_units` remain original literal quotations. Never backfill original-source transcripts by copying AI inventions.
- If a grammar gender/tense contrast is valuable, use one clearly cued comparison when feasible, rather than mechanical copies of all variants.

## Review budget and report

A card is justified by expected learning benefit, not by a source unit/word count. Report:
- Original source units retained/linked;
- Unique word forms actively used in targets/examples, plus the context-only inventory; priority terms are mandatory learning content, not a per-word card quota;
- Cards by retrieval skill and source/teacher origin;
- A short rationale for the most important selected learning points and any intentionally omitted extra drills.

Keep the summary short and actionable.