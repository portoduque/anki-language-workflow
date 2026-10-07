# “Claude Code + Anki = Learn ANYTHING!” — Selective Adaptation Note

Source analyzed:

- YouTube: https://youtu.be/1sMHcJMxYqo
- Title: “Claude Code + Anki = Learn ANYTHING!”
- Published: 2026-06-20
- Duration: 13:46

The complete spoken transcript was reviewed from start to finish.

The video demonstrates an agentic Anki workflow built around AnkiConnect. It covers:

- generating cards from videos, lectures, textbooks, and other material;
- extracting transcripts, screenshots, diagrams, and source references;
- direct Anki insertion with custom rendering;
- sentence mining for Japanese with source sentence, image, audio, context explanation, and TTS;
- using actual review outcomes to identify difficult cards and patterns;
- “leech surgery” to diagnose/rewrite repeatedly failed cards;
- detecting confusable pairs;
- “laddering” missing intermediate concepts;
- diversifying examples to avoid context-bound recall;
- reprioritizing cards around near-term goals;
- feeding practice/test or real-world performance back into card selection;
- splitting oversized cards according to the minimum-information principle.

## What already matched this project

### Agentic creation + AnkiConnect

The repository already has the safer, provider-agnostic version of the video's core architecture:

`AI → card-plan.json → deterministic validation → APKG/live AnkiConnect delivery`

It already verifies AnkiConnect capabilities, validates media before upload, preflights notes, inserts them, rereads them, and verifies uploaded media bytes.

No Claude-Code-specific dependency should be introduced.

### Source-first sentence mining

The Japanese example strongly matches existing rules:

- preserve personally encountered source material;
- prefer near-i+1 context;
- sentence mining is selective;
- use source audio/image when genuinely helpful;
- add concise contextual explanation rather than generic dictionary dumping.

No new “every mined word gets image + audio + TTS” rule is justified.

### Leech repair, confusables, example diversification, and atomicity

These ideas are already present:

- repeated failure should trigger diagnosis/redesign, not brute-force duplicates;
- relational/contrast cards may be useful when two items are confusable;
- avoid cue overfitting to one fixed example;
- split overloaded cards into one primary retrieval target;
- retire/suspend low-value material only with evidence.

The video therefore reinforces existing policy rather than creating duplicate rules.

## Useful ideas adopted

### 1. Preserve precise source locators when the source supports them

The video links cards back to the relevant lecture timestamp.

This is a low-cost, high-value improvement for language mining because a learner may need to revisit pronunciation, visual context, register, or the surrounding sentence later.

Adaptation:

- when the source has a stable locator, preserve it in `source`;
- examples: video timestamp, page number, section/chapter, transcript segment, or other stable location;
- prefer a directly reopenable locator when possible;
- do not invent precision that the source does not provide;
- source locators are provenance/support, not extra retrieval targets.

No schema change is needed because `source` already exists.

### 2. Add a read-only review-feedback audit before collection maintenance

The most important genuinely new capability is closing the loop with actual Anki review history.

The repository already documents review-history actions, but the default workflow did not expose a deterministic, read-only audit command.

Adaptation:

- add `scripts/audit_live.py`;
- default query audits workflow-created cards tagged `anki-language`;
- use only read-only AnkiConnect actions;
- collect card fields, scheduling metadata, suspension state, and review history;
- summarize rating counts and Again rate without inventing a universal “bad card” threshold;
- sort the report to make repeatedly failed cards easier for an AI/human to inspect;
- never rewrite, suspend, delete, reschedule, or reprioritize a card from the audit command.

The report is evidence for later diagnosis, not an automatic mutation plan.

### 3. Maintenance is diagnosis-first and mutation-by-approval

Review history can reveal candidates for inspection, but it does not explain causality by itself.

When a user asks to maintain an existing collection:

1. audit read-only;
2. inspect the actual card/context and review pattern;
3. diagnose likely causes such as ambiguity, insufficient context, confusable items, a missing prerequisite, malformed content, or low value;
4. propose the smallest repair;
5. mutate existing cards/scheduling only when the user explicitly approves the relevant action.

This keeps the useful “closed loop” idea from the video without allowing an AI to silently rewrite or delete the user's collection.

## Ideas intentionally NOT adopted

### Automatic scheduling reprioritization from AI guesses

The video suggests moving cards around based on an exam, sales call, or topical goal.

This repository does not let an agent silently manipulate due dates/queues. Scheduling changes can alter FSRS behavior and should be driven by an explicit user goal with current Anki guidance.

Selection of **new** cards may reflect the user's goals, but existing scheduling is not automatically rewritten.

### Automatic deletion of “low-value” cards

A model may identify rare or currently low-priority vocabulary, but that judgment is contextual.

The workflow may recommend suspend/retire when evidence supports it. It must not delete existing user cards automatically.

### Automatically adding intermediate “ladder” cards after every failure

Repeated failure can indicate a missing prerequisite, but it can also come from ambiguity, interference, poor wording, or low value.

A bridge card is allowed only when a specific missing prerequisite is identified and independently worth reviewing.

### Automatically generating more examples

Varied examples can improve transfer, but extra cards carry future review cost.

Use another context only when it adds a real retrieval benefit; do not multiply cards simply because an agent can generate them.

### Generated diagrams / web-searched images by default

The project already has selective media rules, provenance checks, and licensing constraints. Media remains optional and functional, never decorative.

## Net changes justified by this source

1. Preserve precise source locators such as timestamps/pages when available.
2. Add a deterministic read-only live-audit script over AnkiConnect review history.
3. Make existing-collection maintenance explicitly diagnosis-first and mutation-by-approval.
4. Add behavioral/regression tests for source locators and read-only feedback auditing.

No card-plan schema, note model, deck architecture, scheduler, media provider, installer, or live-delivery semantics need to change.
