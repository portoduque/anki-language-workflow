---
name: anki-language
description: Creates selective, import-ready Anki language decks from text, audio, images, PDFs, transcripts, notes, or mixed study material. Language- and AI-agnostic. Use for APKG generation, sentence mining, listening, reading, pronunciation, selective writing, audio, images, and language-learning flashcards.
---

# Anki Language

## Current contract: four skills, complete source coverage

New `card-plan.json` files **must use version 2.8** (analysis version **1.1**). Only **Reading, Listening, Pronunciation & Sounds, and Writing** may be generated. **Never create Production cards** or disguise them as Writing. Versions 2.0–2.7 remain compatible for existing exports. Production is rejected by 2.1–2.8; 2.0 may be processed only for historic imports.

**Unchanged v2.4-compatible chunk-first automatic audio in v2.5:** first extract, compare and mine each original sentence; select only useful, fast-revision chunk cards; only then synthesize one **focused target recording** for each distinct selected card text. **No full original phrase audio by default**; all original text still appears verbatim on the Back for 100% coverage. Extra full-phrase audio is available only when `audio_settings.include_source_audio` is explicitly `true`. The Anki card keeps normal Reading/Listening front/back audio positioning. This reduces slow and redundant media generation. Piper voice is configurable (`audio_settings.voice`) and speed through `audio_settings.length_scale` (0.93 default; smaller is faster). Prefer `fr_FR-siwis-medium` for French when available, but sample other voices and use the student's choice if it sounds better. Flag unusually long short-chunk WAVs for listening review; metadata alone never proves pronunciation quality. v2.4 sends bytes via verified Base64 for Flatpak AnkiConnect. Do not add extra cards simply because audio exists. Production remains retired; v2.0–v2.3 remain compatible.

**Professor IA — competitive audit of omitted opportunities (v2.8).** Before final card selection read [references/teacher-authoring.md](references/teacher-authoring.md). After the first pass, re-read **every source sentence and word** for useful vocabulary that was overlooked; record `source_assessments[].examined_expressions` with `practice` or `context` decisions. Generate genuinely different natural teacher-authored alternatives to the most important constructions; compare selected and rejected candidates in `review.tradeoffs` and describe gaps, redundancy, and transfer in `review.omission_scan`, `review.redundancy_scan`, and `review.transfer_scan`. No quota of invented cards, no per-word card quota, no repetition solely for volume. **Verify the full analysis contract 1.1 before composing the card-plan 2.8**, and recheck the quality of translations. Reject a lesson that declares every candidate selected without credible tradeoffs. Deliver the exporter-produced paired `<deck>.resolved.json` with its APKG and hash report to prevent cross-run media mismatches.

**Previous v2.7 contract:** Before creating any cards, read [references/teacher-authoring.md](references/teacher-authoring.md) and write `lesson-analysis.json`, following [schemas/lesson-analysis.schema.json](schemas/lesson-analysis.schema.json). Run `python scripts/validate_lesson.py lesson-analysis.json` **before** writing `card-plan.json`. Analyze every source sentence/word, identify high-value reusable concepts, explore attested and teacher-created natural candidates, choose/dismiss each based on independent learning gain, and consider all four retrieval skills. The AI makes these decisions autonomously; ask the user only when source wording or learning intent cannot be resolved safely. Final cards must match approved candidates via `learning_point_id` and `candidate_id`. A teacher-authored example is not mandatory when it adds no value. **Do not invent filler cards, quotas, or unverified language.**

**Legacy v2.6 professor contract:** Read [references/teacher-authoring.md](references/teacher-authoring.md) **before designing any card**. Do not merely copy text. Analyze all supplied words/phrases, identify reusable lexical and grammatical patterns, and allow new, natural, short teacher-created target chunks and optional example sentences that combine the supplied vocabulary. Every new card has `origin="source"` (exact quote from a linked source unit) or `origin="teacher"` (deliberate, checked adaptation), and teacher-written examples live in `teaching_examples`, explicitly labelled on the Back. Never misrepresent generated examples as screenshots/transcripts. Verify grammar, register, meaning and naturalness; when uncertain, avoid the generated candidate rather than inventing authority.

In **v2.7 (and v2.6), preservation and practice are separate**. Preserve EVERY original word and phrase literally in `source_units` and linked Back Source fields. **Do not try to place every single source word in Front targets**. Select useful skills/knowledge first. Specify `teacher_analysis.summary`, a short, justified `teacher_analysis.priority_vocabulary` list of original words/expressions worth active practice, and one or more `teacher_analysis.discarded_candidates` when multiple inputs are provided. Each card must state `learning_goal` and `selection_reason` and be a natural, short chunk. The validator requires prioritized vocabulary to appear in a Front target or short Back teacher example, reports all context-only words, rejects mass verbatim long-turn copying and excessive Reading length, **not** a card for every word. All other original words still appear in verbatim contextual text on card Backs (100% visibility). This removes the v2.5 incentive to paste every utterance into a card. Priority is learning value, not an arbitrary card quota. Never cheat via random example word stuffing. 2.5 plans retain their old exact lexical rules.

**100% visible material coverage, no per-word card quota.** List **every user-supplied target-language sentence and individual word** as a verbatim `source_units[]` entry, each linked via `card_ids[]` to at least one real card. Each full sentence/word appears automatically in that card's **back-side Source footer**, not as a long Front or a separate repetitive memory test. For Reading cards that display contrasted forms separated by / or vs., supply a concise prompt identifying which distinction is tested. For long sentences choose one or more quick useful chunks for the Front; the full sentence is retained on the Back. Never skip an explicitly supplied sentence/word because it is trivial; you may omit an extra retrieval card when the same existing card already displays that source unit. For source files that are lists of phrases/words, set `source_text_file` to the actual .txt/.json source so the validator independently checks that all lines/items were inventoried. If a screenshot/audio cannot be reliably transcribed, do **not** guess and do not claim complete coverage; ask for a transcript or confirmation. The validator can verify declared items and linked display, but cannot independently read speech/images.

For a supplied audio collection, **enumerate EVERY original audio** before selecting cards, match it to the corresponding source text, and examine **every entire sentence for natural, independently useful chunks**. A long source may produce several cards if they train *different useful chunks*; do not ignore useful material merely to keep the smallest possible count. Yet trivial, known, ambiguous, repeated or unhelpful material may yield zero cards. Write a `source_inventory` manifest listing every input audio from `audio_root` (a directory or ZIP), mapping each audio to the full spoken phrase through `source_unit_ids` and to cards (or, for duplicate/silent recordings only, a specific skip reason). Link cards with `source_item_id`. Physical source omissions are rejected by the validator; semantic choices still need human/AI judgment. Report the coverage results to the user.


Turn source material into the smallest useful set of language-learning cards, then build and validate an Anki package.

## Mandatory first-run language setup

Before analyzing study material, look for `anki-language.config.json` in the active workspace.

If the configuration does not exist, **stop before card creation and ask the user for both:**

1. **Target language** — the language being learned.
2. **Base language** — the language used to explain, translate, cue, and guide the target language.

Do not infer either language and do not use a default. This first-run question is mandatory even when the source material appears to make the target language obvious.

After the user answers, persist the choice in the workspace with:

`python scripts/configure.py --target-name <name> --target-code <code> --base-name <name> --base-code <code> --output ./anki-language.config.json`

On later runs in the same workspace, reuse that configuration unless the user asks to change it.

All learner-facing explanations, semantic cues, translations, and production instructions must use the configured **base language** unless the card intentionally tests the target language without a translation.

## Non-negotiable card rules

Before selecting cards, read [references/card-selection.md](references/card-selection.md). These invariants are mandatory:

- Create the **minimum useful number of cards**. The same sentence, word, expression, audio, image, or passage may produce multiple cards across different skill decks when each card trains a genuinely different and worthwhile retrieval operation.
- Every card has **one primary retrieval target**.
- Reveal non-target information when it cleanly isolates the intended skill, but never reveal the actual retrieval target.
- Every front must be **self-orienting in a mixed review**: show the target language and trained skill without revealing the answer.
- Never create a prompt that makes the learner guess what the author intended. **Blind/ambiguous cloze is forbidden.**
- Do not create automatic reverse cards or invent full-sentence production/typing exercises.
- **Writing is an optional fourth skill** for fast **typed** orthographic/grammatical retrieval. After reading [references/card-selection.md](references/card-selection.md), consult [references/writing.md](references/writing.md) for its native Anki typing constraints. Pick a short natural sentence, exactly one word/short chunk to type, and a precise `prompt` that removes ambiguity; never make the user type a whole long sentence. **No automatic Writing sibling** for every Reading/Production card.
- Do not generate every card type for every item. For every extra sibling card, require enough incremental learning value to justify its future review cost; optimize memory efficiency, not volume.
- Prefer useful chunks/collocations/patterns when the combination is the knowledge that matters.
- **Mandatory long-source chunk mining:** even when all supplied screenshots, transcripts, sentences, or recordings are long, first look inside each complete sentence/turn for the **shortest natural, meaningful and reusable chunks** worth learning. A long source sentence is **not** a mandate to make a long card. Generate separate short cards for distinct high-value chunks if justified, not one card for every clause and not a multi-clause mega-card.
- **Review speed is a top priority:** every Front must be quick to understand and answer, and every Back quick to verify. Prefer one practical phrase/construction per card; keep only the context needed to make retrieval unambiguous. If a full-sentence target is genuinely essential and remains quick, it is allowed. Do not impose arbitrary word-count limits, mandatory chunk counts, or mechanical splits.
- Preserve the original meaning and native phrasing when extracting chunks; reject incomplete/unidiomatic fragments, semantically empty fragments, and redundant near-duplicates. More chunks are **not** automatically better; each must independently earn its future review cost.
- A contrast/relationship may be one primary retrieval target when the distinction itself is the useful knowledge; do not turn this into a multi-answer mega card.
- Avoid cue overfitting: the learner should retrieve the language, not merely recognize one fixed card wording. Use varied natural contexts only when each adds real transfer value.
- Sentence mining is selective; do not turn every sentence into a card.
- Prefer near-i+1 mined sentences: the surrounding context should already be understood, with one primary unknown/focus item. If several independent unknowns compete for attention, choose a cleaner sentence, split targets, or skip it.
- For polysemous words/expressions, inspect multiple trustworthy contexts during analysis, but keep each review front concise; prefer one primary sense/usage per card when a multi-definition answer would overload retrieval.
- Mnemonics are optional scaffolding for difficult items. Verified cognates/etymology may help; invented sound-alike mnemonics must be labeled as mnemonics, and AI must not fabricate linguistic ancestry.
- For genuinely difficult arbitrary grammatical attributes such as gender/noun class, a stable concrete mnemonic code may be used as secondary scaffolding; keep the real target form/chunk primary and never hard-code one universal mapping.
- For continuous natural material, prefer a meaning-first pass before intensive lookup/card extraction when comprehension is still possible; do not interrupt the source for every unknown.
- An encountered unknown word/phrase is only a **candidate** until it passes the usefulness/context/review-cost test; preserve source context and batch selection after a passage/chapter/clip when practical.
- Before promoting a candidate to a scheduled card, clarify its intended meaning/form/usage enough that review tests retrieval rather than first-time semantic discovery; prior mastery is not required.
- For an absolute beginner with too little comprehensible personal material to mine, a vetted frequency/shared deck may be used as a **candidate source**; never bulk-adopt it blindly.
- Let candidate sources evolve with learner evidence: as useful natural input becomes comprehensible, prefer personally encountered/context-rich items over generic lists; when repeated real speaking/writing/domain gaps appear, treat them as candidates for targeted verification.
- Consider expected natural re-encounter frequency when deciding whether a candidate deserves SRS: useful rare/domain-specific items may benefit from deliberate review when natural exposure will not reinforce them soon, while constantly re-encountered easy items may not need cards. Rarity alone is never sufficient.
- Never hard-code an external roadmap phase, corpus-frequency cutoff, or vocabulary-count milestone as a mandatory source-strategy switch.
- Do not turn a speaking/output gap into a forced translation card: author only a justified current-format comprehension, sound or short Writing task.
- Card-creation/customization time also counts. Prefer simple cards and selective enrichment over decorative complexity that does not improve retrieval.
- For grammar, choose the card format from the retrieval intent: rule recall, recognition/discrimination, or contextual application/production. Create declarative rule cards only when recalling the rule itself is independently useful; do not default to full tables/paradigms.
- Grammar/morphology explanations on the back should be brief and only added when they explain why the target form is correct or prevent a predictable confusion.
- Adapt card selection to genuinely useful target-language-specific features (for example gender/class, irregular plural/inflection, case/agreement, classifiers, irregular verb forms, or script variants). Treat each feature as a candidate, create only independently worthwhile atomic retrievals, and never generate a full paradigm by default.
- Use structured optional fields `reading`, `variant`, and `grammar` when those data are useful; never generate extra cards merely because an auxiliary field is populated.
- Use `prompt` for a concise learner-facing instruction or situational/scene context when it helps define the retrieval task without leaking the answer; do not add duplicate fields merely to mirror an external template.
- Use only documented card modes. Reading/Listening/Writing use `standard`; Pronunciation & Sounds may additionally use `minimal-pair`, `sound-discrimination`, `spelling-sound`, or `audio-to-spelling`. Do not invent mode strings.
- Every Pronunciation Front must contain a usable retrieval cue, not a generic instruction. The deterministic builder shows the written target for `standard` (read-aloud) and `spelling-sound`; it hides the target for audio-identification modes and requires the front audio there. Never create Pronunciation cards for whole dialogue lines without a specific independent sound/rhythm/spelling difficulty.
- Select short, useful written/auditory comprehension targets; do not create full-sentence Production tasks.
- If a recording is reused across different target texts, attach `audio_transcript` verified from the actual clip to each reuse; otherwise use separate focused recordings or omit optional audio. The validator checks transcript consistency, not acoustic truth.
- **Long source audio is not card audio.** When supplied speech contains multiple lines but the card tests only one, create an `audio_clip` request from the original recording, not a full `audio` reference. Prefer *verified* `start_seconds`/`end_seconds` from source timestamps; without them, use optional local word-timestamp recognition to locate `target_text` conservatively. Never invent boundaries, silently attach a whole dialogue, or force TTS to replace a useful original.
- A `audio_clip` match that is absent, repeated, transcription-uncertain, or technically unavailable is **blocked for clarification or source correction**; do not mark unresolved media as validated. Check [references/media.md](references/media.md).

- Keep generated templates inspectable and portable: essential card behavior must not depend on JavaScript or remote web assets.
- Visual presentation is deterministic and workflow-owned. New cards use the Anki Language v5 UI from [references/card-ui.md](references/card-ui.md); the AI must not invent per-card HTML, colors, icons, or layout variants.
- Selective Writing cards train one short missing written form; do not create full-sentence typing or handwriting cards by default.
- Prioritize verified natural wording, especially for quoted source chunks; never invent an original audio transcript.
- Audio and images are optional and must add learning value.
- For minimal-pair/sound-discrimination cards, prefer the same speaker/voice and comparable recording conditions when feasible so irrelevant audio cues do not solve the card.
- Spelling/spelling-sound cards are scaffolding: stop generating them once the learner handles representative patterns reliably, except for genuinely difficult exceptions.
- When a card tests meaning or valid usage, accept semantically correct alternative examples; require exact wording only when wording/form/order is the actual target.
- Listening uses audio-first; pronunciation and selective Writing may keep answer audio on the back; sound-discrimination fronts must not reveal answers.
- Keep answers concise and reviews fast. In Writing, type one small, meaningful missing part, not the entire long utterance.
- Preserve precise source locators (for example video timestamps, pages, sections, or transcript anchors) when the source provides them; never invent precision. Avoid screenshot-only references without an accessible path/URL in a portable deck.
- When maintaining an existing collection, use review history to identify cards that deserve inspection, but treat the history as evidence rather than an automatic diagnosis. Start read-only, inspect the actual card/source, and require explicit user approval before rewriting, suspending, deleting, rescheduling, or reprioritizing existing cards.
- When reliable mastery evidence is available, prefer retiring redundant scaffolds that are fully subsumed by richer contextual cards; never infer mastery from age alone or delete user cards without permission.
- When a material ambiguity changes the learning target, ask the user instead of guessing.

## Workflow

1. Resolve the mandatory target/base-language configuration.
2. Inspect all supplied material before selecting cards.
3. Read [references/teacher-authoring.md](references/teacher-authoring.md) and [references/pedagogy.md](references/pedagogy.md); the mandatory card rules were already loaded from [references/card-selection.md](references/card-selection.md).
4. When supplied multiple recordings, first enumerate all audio files and match each with its transcript/screenshots. Read/understand **each complete source**, then **mine short, natural, meaningful chunk candidates even from exclusively long source sentences**; identify useful collocations, phrases, and grammatical frames instead of defaulting to full-sentence cards. Never split blindly by punctuation/word count.
5. **Mandatory autonomous professor pass before card authoring (v2.7):** write `lesson-analysis.json` with one `source_assessments` record for **every** phrase/word; identify all teachable language concepts; justify priority high/medium/context from usage, difficulty, reusability, novelty and review cost; draft *both* original and teacher-created candidate chunks when genuinely useful; explicitly accept or reject candidates with reasons. Record `skill_review` for Reading, Listening, Pronunciation and Writing. Run `python scripts/validate_lesson.py lesson-analysis.json`; stop and fix any failures. **Only after this gate may the AI create the card plan.** Next, explain briefly what communicative skills/structures the whole material teaches. Draft original and natural teacher-created chunks, compare and reject redundancies (record short evidence in `teacher_analysis`). Choose a valuable, independent `learning_goal` for each selected card; do NOT turn each entire original sentence into one Reading card just to satisfy source coverage.  do not stop after a few attractive utterances. Rank chunk candidates by usefulness, clarity, distinctness, and expected review effort. Keep **zero, one, or several** independent targets from one long source only when each earns its review cost; reject filler and redundant fragments. Prefer fast, single-target cards; retain a complete sentence only when the whole utterance is the actual independently valuable target. **Select chunks first, then route each to its best primary skill.** Use the two-stage routing matrix in `references/card-selection.md`. **Before authoring, assess the four supported retrieval skills for the batch**, not only the modalities already present in the first few cards. Decide based on the learner's actual or stated gap; do not produce former Production cards or mechanically pair skills. Missing subdecks are valid when justified, never a reason to manufacture filler.
6. For each selected v2.7 candidate, copy its wording and provenance **exactly** from the previously approved lesson analysis; set `learning_point_id` and `candidate_id` on the corresponding card and give it an independent `learning_goal`. If high-priority knowledge supports a second distinct learning task, a second candidate/card is permitted, with a separate retrieval reason, not by default. Do a **teacher-revision pass** checking idiomatic meaning, base-language explanation, transfer to a new situation, trivial greetings and semantic near-duplicates; revise the analysis file and revalidate it before accepting any changed candidate. For each selected chunk, declare `origin` and add `teaching_examples` (0–2) only when useful. A teacher-created card requires a verified base-language meaning and may NOT claim a literal `source_excerpt`. For each selected chunk, create a short, answerable Front and a glance-checkable Back with only sufficient context. **Cross-check quotations against the supplied text/screenshot/transcript and their audio when available.** Populate `source_excerpt` with the exact original wording when directly quoting supplied text, never with a reconstruction. If a screenshot and actual audio disagree, do not silently choose or combine versions: verify which was spoken and either represent the verified version correctly or ask. Match any original audio to the selected short wording using `audio_clip` or independently verified dedicated audio; do not use a whole dialogue when a focused Listening/sound target needs only a chunk.
7. Before finalizing, check priority vocabulary in targets/examples, and identify all other words as preserved in original Back context. Write `learning_goal` and `selection_reason` per card. Validate with `validate_plan.py`: long Reading fronts and repeated whole-turn copying are rejected for v2.6. Classify each selected card as exactly one of: `reading`, `listening`, `pronunciation`, or `writing`. A second card for the same chunk needs its own learning gap, retrieval cue and marginal benefit; never automatically generate all skills. **Perform a quick skill-selection audit:** (a) what must be recalled (written meaning, spoken meaning, active use, difficult sound, or exact spelling/grammar)? (b) what would be missed if this card were removed? (c) did the inventory leave any recording or useful candidate unexplained? If so, re-evaluate each sibling independently. Before delivery, compare all candidates for overlapping chunks, same-skill prompts and near-paraphrases. Existing user cards may inform selection when available, without modifying them.
8. Add sparse linguistic tags only when useful.
9. If media may improve learning, read [references/media.md](references/media.md) before acquiring, generating, or attaching it.
10. Write **v2.8** `card-plan.json` (lesson analysis v1.1) with `lesson_analysis_file: "lesson-analysis.json"`, `learning_point_id` and `candidate_id` on every card. Then run `python scripts/validate_plan.py card-plan.json --allow-missing-media`. Legacy: write **v2.6** `card-plan.json` only when explicitly processing a historic plan; with nonempty `source_units`, one per source phrase/word, each linked to a card. For an audio collection, include `source_inventory` with all files, `source_unit_ids` and decisions plus a matching `source_item_id` on each selected card. Follow [references/output-contract.md](references/output-contract.md) and `schemas/card-plan.schema.json`. Its target/base languages must match the workspace configuration. Use `audio_clip` for selected spoken excerpts from longer original recordings; use `audio_request` / `image_request` only where generated media adds real value.
11. Select delivery: `apkg` by default; `live` only when the user wants direct AnkiConnect delivery; `both` when live insertion plus a portable APKG is useful.
12. Run `python scripts/run_pipeline.py card-plan.json --delivery <apkg|live|both>`. This resolves media, validates it, then delivers it. Deterministic delivery adds workflow identity tags automatically; do not ask the model to invent them.
13. In live mode, an existing workflow identity is idempotent only when the stored note still matches the expected content. Treat changed content/model/template/CSS as drift and stop rather than silently skipping or overwriting it.
14. Treat deterministic APKG validation as structural validation, not proof of cross-client rendering. After a meaningful template/model migration, ask for or perform a representative Anki spot-check (long text, empty optional fields, media, night mode, and the target writing system) before large-scale adoption.
15. Deliver the **v2.8 lesson analysis, exact paired resolved-plan snapshot, APKG hash report**, APKG/live report, and counts of focused target audio, optional context audio and duration warnings; report failures instead of claiming success. Also deliver and a **100% source-unit coverage report** (source unit count, linked card count), plus a per-audio coverage summary explaining exactly what was selected or skipped and why. Give a **brief selection summary** stating counts by skill, why omitted skills were unnecessary for this specific source/learner, and any unverifiable audio/source assumptions. Do not invent learner weaknesses to justify variety. Never claim media or rendering success when the relevant validation/spot-check did not occur.

## Optional live maintenance / feedback audit

When the user explicitly asks to inspect, maintain, repair, or diagnose an existing live Anki collection, use a **read-only-first** workflow.

1. Ensure Anki Desktop + AnkiConnect are available.
2. Run:
   `python scripts/audit_live.py --query "tag:anki-language" --output anki-audit.json`
   or use a narrower Anki search query chosen for the user's goal.
3. Use the report to identify cards with meaningful review evidence that deserve inspection.
4. Inspect the actual prompt/answer/source context before inferring why a card is difficult.
5. Diagnose the smallest likely cause: ambiguity, overload, insufficient context, confusable items, missing prerequisite, malformed content, low value, or another evidence-supported issue.
6. Propose the smallest repair.
7. Do **not** mutate existing notes/cards/scheduling until the user explicitly approves the relevant action.

The audit command itself is read-only. It uses AnkiConnect review/card inspection actions and reports fields, interval/suspension metadata, review counts, rating counts, Again rate, and latest review ID. New workflow-owned notes receive the `anki-language` system tag in both APKG and live delivery, so imported APKG cards can enter the same audit path. It deliberately does not define a universal leech threshold or make scheduling changes.

## Deck architecture

- `<TargetLanguage>::01 Reading`
- `<TargetLanguage>::02 Listening`
- `<TargetLanguage>::03 Production` — legacy only; **never generate**
- `<TargetLanguage>::04 Pronunciation & Sounds`
- `<TargetLanguage>::05 Writing`

Use tags, not extra micro-decks, for vocabulary, grammar, chunks, levels, sources, and similar dimensions.

## Card behavior

- **Reading:** written target-language context on the front; meaning/explanation in the configured base language on the back when useful.
- **Listening:** audio on the front; target transcript and base-language meaning/explanation on the back.
- **Production:** retired for v2.1; only historic v2.0 decks may contain it.
- **Writing:** a short target-language sentence with **one hidden word/chunk** on the Front, a semantic/grammar cue, and native `{{type:WritingAnswer}}` input; the Back compares typed text, shows the complete sentence and optionally plays short audio. Do not use blind gaps or entire-paragraph typing.
- **Pronunciation & Sounds:** use pronunciation production, sound discrimination/minimal pair, or spelling-sound behavior according to the actual target. The written target is visible only for read-aloud/spelling-to-sound; identification-by-ear modes have audio on the front and conceal the written answer.

Never use a blind or ambiguous cloze. The learner must know what knowledge to retrieve without the prompt revealing the answer.

## Automatic media and delivery

The AI decides **whether media is worth adding**. Deterministic scripts decide how to generate/fetch, validate, and deliver it.

### Audio

Priority:

1. user-supplied original audio;
2. permitted native audio;
3. automatic local TTS.

For current v2.4 text-only material, **do not request whole-dialogue audio**: run the media pipeline *after card selection* to synthesize only selected target chunks. Full source text stays on the Back; extra source speech is opt-in through `audio_settings.include_source_audio`. v2.3 legacy plan behavior is unchanged.

Do not use the Forvo add-on as the core automation path. It runs inside Anki and is not a stable cross-agent media API. Do not scrape Forvo. Use it only through a workflow whose terms permit storage/embedding.

### Images

Use `image_request` only for concepts where an image improves retrieval.

Automatic provider order:

1. Openverse with explicit license filter;
2. Wikimedia Commons fallback with machine-readable license metadata.

Default automatic licenses are intentionally restricted to `cc0` and `pdm`.

### Mandatory validation before any upload/build

Before media is attached to a card, the pipeline must validate the actual local file:

- audio must decode and have positive duration;
- image must fully decode and have usable dimensions;
- SHA-256 is recorded;
- a file that changed after validation is rejected.

Never bypass this gate.

Required media failures block delivery. Optional media failures are recorded in `media_issues` and the card continues without that media; never upload a broken fallback merely to fill the field.

### AnkiConnect live delivery

When delivery mode is `live` or `both`:

1. verify AnkiConnect with `version` + `apiReflect`;
2. inspect/create required decks/models;
3. for an existing workflow-owned model, verify fields **and** templates/CSS; never overwrite model drift automatically;
4. derive the scoped workflow identity and inspect any existing matching note before deciding it is already delivered;
5. skip an existing note only when its stored fields/media references still match the expected card; otherwise stop with a drift conflict;
6. validate every local media file **before** `addNotes`;
7. preflight new notes with `canAddNotesWithErrorDetail`;
8. create notes with local audio/image paths;
9. re-read created notes with `notesInfo`;
10. retrieve uploaded media with `retrieveMediaFile`;
11. compare uploaded bytes against the prevalidated local SHA-256.

Success requires identity/content consistency plus the note-field reference and uploaded bytes to validate. If an existing note changed, or post-upload verification fails, report failure instead of silently overwriting, silently skipping, or claiming success.

### Delivery modes

- `apkg`: portable validated package only.
- `live`: direct validated insertion into running Anki.
- `both`: direct insertion plus APKG.

## Anki technical reference routing

Use the bundled Anki reference library **when a decision depends on Anki behavior**, not for ordinary language analysis.

Consult it when you need to decide or verify:

- note/field/card-type structure;
- templates, HTML/CSS, TTS, typed answers, cloze, or Image Occlusion;
- audio/image/media packaging;
- decks/tags/search/browser behavior;
- FSRS/scheduling/settings;
- CSV/TSV/APKG/COLPKG import/export;
- sync/backups/profiles/files;
- statistics/leeches/filtered decks;
- add-ons/extensions;
- AnkiConnect, APIs, or automation;
- mobile/platform compatibility;
- troubleshooting, current-version behavior, or security.

When scripts are available, route the question first:

`python scripts/find_anki_reference.py "<technical need>"`

Then read only the returned files under `references/anki/`.

Do **not** preload the full Anki library for every card-generation run. Pure pedagogical card selection should use `references/card-selection.md` and `references/pedagogy.md`.

For current/version-sensitive facts or gaps in the local summaries, consult `references/anki/SOURCES.md` and prefer the official live documentation index:

https://docs.ankiweb.net/llms.txt

Current official Anki documentation outranks old blogs, old add-on instructions, and remembered behavior.

For scheduling/FSRS advice, do not copy fixed numeric/display-order presets from research videos or another user's collection. Use current official semantics plus the learner's own workload/review history.

## AnkiConnect live-integration reference

When the user wants to **inspect or modify a running Anki collection**, configure/troubleshoot AnkiConnect, or asks how to perform an AnkiConnect action, route to the dedicated sub-library:

`references/anki-connect/INDEX.md`

When scripts are available, use:

`python scripts/find_ankiconnect_reference.py "<goal or action>"`

Examples:

- `python scripts/find_ankiconnect_reference.py "addNote audio duplicate"`
- `python scripts/find_ankiconnect_reference.py "createModel templates css"`
- `python scripts/find_ankiconnect_reference.py "api key cors permission"`
- `python scripts/find_ankiconnect_reference.py "review history stats"`

The router understands both natural-language goals and exact action names. It searches a dated 2026 catalog of 118 documented actions (114 baseline + 4 newer/version-sensitive actions), enriched with descriptions, exact source signatures, parameters and risk metadata.

### Mandatory live-integration rules

- AnkiConnect is optional; APKG generation remains the default when live collection access is unnecessary.
- Before using an uncertain/version-sensitive action, prefer live `version` + `apiReflect` capability discovery.
- Never invent plausible AnkiConnect actions.
- Do not assume fork-specific actions exist in standard AnkiConnect.
- Preserve localhost binding by default.
- Never expose port 8765 publicly as a convenience shortcut.
- Use API-key authentication and network restrictions when access extends beyond localhost.
- Treat delete, scheduling, review-history, model-schema, sync, and profile-changing actions as higher risk.
- Use human-visible GUI actions when user verification is valuable.
- Use the AnkiConnect reference library selectively; do not load the full action catalog into context unless exhaustive API analysis is actually required.

## AI portability

`SKILL.md`, `references/`, `schemas/`, and `scripts/` are the canonical implementation. Provider-specific adapters must remain thin. If an AI supports Agent Skills, install this bundle in its skill directory. If it does not, instruct the AI to read this `SKILL.md` and use the deterministic scripts directly.

## Quality gate

Do not deliver until the deterministic pipeline passes. It validates plan structure, actual media decodability, media hashes, package integrity, note/card counts, deck hierarchy, and the final APKG. In live mode it additionally verifies AnkiConnect-uploaded bytes and note-field references.

The builder, not the model, is the source of truth for package structure. Do not hand-edit Anki collection databases.