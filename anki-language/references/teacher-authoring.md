## v2.8 — Professor IA opportunity review and competitive selection

For **new lessons**, write `lesson-analysis.json` using analysis contract **1.1** and card-plan version **2.8**. The AI performs a **second, adversarial teacher pass** after reading *every word and sentence* but **before producing cards**:

1. In every `source_assessments[].examined_expressions`, record actual short spans from the original with a decision `practice` (linked to its `learning_point_id`) or `context`, and explain why. Long source lines need more than a single easy phrase examined. Include common reusable verbs, time markers, collocations, nationality, study fields and productive grammar, not only greetings. The audit is source-grounded and does **not** impose a card per term.
2. Compare useful original *and* teacher-authored ways to express high-value concepts, trying new communicative contexts by recombining supplied vocabulary. Mark `card`, `example` or `reject`, checking accuracy, word choice and whether a second task would teach anything independent. Use meaningful `review.tradeoffs` to identify the actual chosen and rejected/example-only candidate and the learning gain per minute of review. Multi-line substantial lessons must show comparisons for distinct knowledge points; this is a small **candidate evaluation** requirement, never a quota of created flashcards.
3. Write `review.omission_scan`, `review.redundancy_scan`, and `review.transfer_scan`: inspect the full source *again*, specifically looking for accidentally ignored useful patterns (e.g. `j'habite en France`, `aujourd'hui`, `en sociologie`, nationality) before accepting trivial social expressions as scheduled reviews. Replace weaker selected candidates if the new opportunity provides better learning value. Prioritize short, natural, independently useful Fronts, especially contextual transfers; optional Back examples can teach some high-value details without generating more cards.
4. Run `validate_lesson.py` **before** creating card-plan.json. Validator verifies the original provenance of screened expressions, actual rejected alternatives, tradeoff references, and coverage decisions. It **cannot prove idiomatic naturalness or actually independent reflection**. Treat the recorded audit as evidence to review, not an automated score of pedagogy.
5. Produce exactly the selected candidates with `learning_point_id`/`candidate_id`; run plan validation and audio generation only after the second teacher review. Report explicit context-only decisions; do not pad examples to pass any quota. Reading/Listening/Pronunciation/Writing skills must match learning bottlenecks; Production stays retired.

**Media consistency gate:** The v2.8 APKG exporter compares each packaged WAV/image's **actual bytes** to the SHA-256 recorded in the resolved card plan. It refuses corrupt/inconsistent packages, writes `French.resolved.json` next to `French.apkg` (named from actual output stem), and records SHA-256 for package, snapshot and each media file in `French.apkg.report.json`. **Deliver the paired snapshot with the APKG** rather than a stale `card-plan.resolved.json` from another attempt. Audio TTS voice/speed are unchanged. Legacy v2.0–2.7 plans still work using their original rules.

## v2.7 autonomous Professor IA — complete analysis before cards

This section is **normative** for every *new* lesson. It replaces the v2.6 pattern of annotating card choices after they already exist. **Do not begin the card plan until a separate lesson analysis is written and validated.** The AI must make instructional decisions itself; do not ask the student to choose chunks, grammar, or card types unless the source is ambiguous or essential preferences are unknown.

### Pass A — Analyze each original utterance or word

Capture every exact source unit (ID + text) and produce one `source_assessments` entry each. Explain the teachable vocabulary, collocations, grammar, communicative function, confusing sounds/forms and whether the full utterance merits practice or merely reference. Consider the whole lesson, not just isolated sentences: important frames recur and combine across lines.

### Pass B — Rank the **knowledge**, then create alternatives

Identify `learning_points` independently of cards and mark priority `high`, `medium`, or `context`. Justify each from communicative utility, transfer, novelty/learner evidence, difficulty and review cost. Do not promote trivial expressions solely to force every original word into a Front. For each point consider short, grammatical candidates:
- `origin=source`: attested original phrase (must be in linked source);
- `origin=teacher`: new natural chunk or transfer example combining material, verified with a precise base-language meaning;
- mark each candidate `card`, `example`, or `reject`, with short justification.

High-priority knowledge must have at least one candidate selected for a card. **Consider an authored alternative** for important points, recording `teacher_option=explored` with the authored candidate, or `unnecessary` with a concrete explanation. This ensures a teacher-style decision without forcing an artificial invented card or a fixed teacher/original ratio. One high-priority item *may* yield multiple selected card candidates only when a separate learning goal/retrieval bottleneck justifies the added review burden. The default is one independently useful task.

### Pass C — Select skills and validate the analysis

Fill `skill_review` with compact rationales for Reading, Listening, Pronunciation and Writing, even when a skill is legitimately unused. Never turn optional TTS availability into unnecessary Listening cards; never reintroduce Production. Run:

```bash
python anki-language/scripts/validate_lesson.py materials/lesson-analysis.json
```

Do not proceed if this fails. This stage is a **separate file**, not just the v2.6 post-hoc `teacher_analysis` text field.

### Pass D — Convert approved candidates into cards, review twice

Only now create `card-plan.json` version `2.7`. Point its `lesson_analysis_file` to the existing analysis file and set each card's `learning_point_id` and `candidate_id`. The validator checks exact candidate wording, source provenance, selected status, high-priority coverage and distinct card references. Review the batch for unnatural teaching examples, misleading meanings, duplicated retrieval, long fronts and low-benefit cards. Modify/revalidate the analysis if a better candidate replaces a selection, rather than silently editing the card in isolation.

Original source text remains visibly linked on the Back. Do **not** require an active card for each original word; keep low-value words in the original context. Preserve the existing v2.4/v2.6 short-audio process, Flatpak and safe content-addressed uploads unchanged.

**Important limitation:** JSON validation cannot prove the AI actually analyzed alternatives chronologically, nor can it prove native-language naturalness. The two-stage deliverable and comparison review make its choices inspectable; the actual quality must still be tested with lesson examples.

# Legacy v2.6 teacher-authoring guidance

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