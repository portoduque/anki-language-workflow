# Meredith — “Anki Setup for Language-Learning - Full Guide” — Selective Adaptation Note

Source analyzed:

- YouTube: https://youtu.be/WNoxhfCnvZY
- Channel: American Accent Training with Meredith / Phonetic Fluency
- Published: 2026-06-29
- Duration: 37:07

The complete spoken transcript was reviewed from start to finish, including all chapters on setup, shared decks, card types, spreadsheet import, audio/TTS, study settings, review buttons, sync, mobile use, and final recommendations.

## What the video teaches

### Spaced repetition and review buttons

The video explains Anki as a spaced-repetition system, demonstrates Again/Hard/Good/Easy, and uses native-language → target-language production as the speaker's preferred personal card direction.

Adaptation:
- keep current project rules: Again means failed recall; Hard means successful but difficult recall;
- do not promote native→target as the only card direction because Reading, Listening, Production, and Pronunciation are distinct skills.

### Shared decks

The speaker prefers self-created/contextual cards most of the time, but recommends a frequency/shared deck as a practical starting point for an absolute beginner with little vocabulary.

Useful adaptation adopted:
- a vetted frequency/shared deck may be a **bootstrap candidate source** for absolute beginners who lack enough comprehensible personal material;
- inspect useful fields, script/readings, audio, and information density before selecting items;
- do not blindly import the entire deck;
- progressively shift toward personally encountered/context-rich material.

### Simple card setup first

The speaker recommends starting with basic front/back/audio and adding advanced Anki features only when a real need appears.

This matches the project's existing creation-efficiency rule and needs no new architecture.

### Card types

The video demonstrates Basic, Basic + Reverse, optional reverse, type-answer, Cloze, tags, and custom field names.

Project decision:
- keep no automatic reverse cards;
- keep constrained Cloze only;
- do not add type-answer merely because it exists;
- tags remain sparse linguistic metadata;
- the existing four skill decks remain unchanged.

### Images and audio

The speaker considers images unnecessary for her native→target vocabulary cards and prefers audio when pronunciation matters. She suggests native-speaker audio and demonstrates manual Forvo/Wiktionary downloads.

Project decision:
- keep images selective rather than mandatory or banned;
- keep audio selective and skill-dependent;
- do not make Forvo/Wiktionary manual downloading the core pipeline;
- the existing media pipeline (user/original audio → permitted native audio → validated TTS; Openverse/Wikimedia images) is more portable and automatable.

### Bulk CSV import

The speaker prefers spreadsheet/CSV import for batches of vocabulary and demonstrates field mapping. She also accidentally imports the header row as a note.

Project decision:
- no new delivery mode is needed;
- the existing APKG/live pipeline is richer and safer for this skill;
- CSV remains documented as an Anki interoperability option in the technical reference library.

### Native/template TTS

The speaker uses AI-generated Anki template code to invoke a Portuguese device voice instead of manually attaching audio to every card.

Project decision:
- useful idea, but already covered by the Anki technical reference;
- native template TTS remains an optional alternative when dynamic platform speech and smaller packages are preferable;
- embedded validated audio remains preferable when exact sound must travel with the deck.

## Study-settings audit against current official Anki documentation

The video's settings section is explicitly second-hand: the speaker says she is not an Anki expert and copied the preset from another Anki-focused video.

Therefore none of the numeric/display-order settings are promoted automatically. They were checked against current Anki documentation.

### FSRS and desired retention

Video:
- enable FSRS;
- leave desired retention at 90%.

Assessment:
- broadly consistent with current Anki guidance;
- 0.90 is a default/starting balance, not a universal immutable target;
- use current Help Me Decide/simulator functionality and realistic review-time budget when available;
- optimize parameters from the learner's own history instead of copying someone else's.

### New cards/day

Video:
- personal deck can use a high limit;
- shared deck might use 20/30/50;
- demonstration uses 50.

Assessment:
- do not copy these numbers;
- current Anki docs note that 20 new/day may lead to roughly 200 reviews/day as an illustrative workload example;
- sustainable workload and backlog state should determine intake.

### Maximum reviews/day = 9999

Video rationale: avoid due reviews being pushed to later days.

Assessment:
- not adopted as a universal recommendation;
- current Anki docs explain that a review limit can intentionally smooth workload peaks;
- effectively unlimited reviews may be a conscious personal choice, not a project default.

### Learning step = 10m

Video removes the 1-minute step and retains 10 minutes.

Assessment:
- not adopted;
- FSRS guidance is to keep learning/relearning steps short and under one day;
- short-term scheduling behavior is version-sensitive, so a fixed 10m preset should not be hard-coded.

### Display order

Video sets:
- random new-card gather;
- order gathered;
- new cards before reviews;
- interday learning after reviews;
- **descending retrievability** for reviews, while describing it as prioritizing cards most at risk of forgetting.

Important correction:
- current Anki docs recommend **Due date, then random** when up to date/small backlog;
- for a large backlog under FSRS, **Ascending retrievability** is the equivalent of prioritizing cards with lower probability of recall;
- therefore the video's explanation of **Descending retrievability** is directionally incorrect and is explicitly not adopted.

### Burying

The video recommends enabling burying to avoid similar cards appearing back-to-back.

Important project-specific correction:
- native Anki sibling burying applies to multiple cards generated from the **same note**;
- the current `anki-language-workflow` builder creates one Anki note per planned card;
- Reading/Listening/Production/Pronunciation cards derived from the same source are currently separate notes;
- therefore native sibling burying does **not** automatically space those cross-skill cards.

The technical reference was corrected so it no longer implies otherwise.

### Easy Days

Video suggests making weekends low/minimum, loosely describing this as studying much less or perhaps 'down to zero'.

Assessment:
- Easy Days can shift due dates by a small amount, but it redistributes workload rather than deleting it;
- do not treat it as a zero-review-day mechanism.

### Leeches

The video correctly identifies repeated failures as leeches worth reviewing.

Project refinement already consistent with our pedagogy:
- repeated failures should trigger card diagnosis: ambiguity, overload, missing context, wrong media/answer, or low value.

## Sync and one-way conflict

The video explains upload-vs-download one-way sync conflicts based on which location contains the authoritative latest changes.

This is already captured in the technical sync reference. No new workflow rule was needed because choosing the wrong direction can overwrite data and must remain a deliberate decision.

## Mobile

The speaker prefers mobile for reviews and desktop for setup/bulk editing.

This is a personal workflow preference, not a card-generation rule. Platform capabilities/prices are version-sensitive and remain in the technical reference layer.

## Net changes justified by this source

1. Add an **absolute-beginner bootstrap exception** for vetted frequency/shared decks as candidate sources.
2. Strengthen FSRS guidance to prefer current official Anki docs + learner-specific workload instead of copied presets.
3. Correct review-sort semantics: backlog-risk prioritization under FSRS uses **Ascending retrievability**, not Descending.
4. Correct the project's sibling-burying claim because current generated cross-skill cards are separate Anki notes.
5. Clarify Easy Days, learning steps, new/review limits, and leech handling without hard-coded universal settings.

## Explicitly not adopted

- production-only native→target direction;
- automatic reverse cards;
- type-answer by default;
- universal use or avoidance of images;
- manual Forvo/Wiktionary as the core audio workflow;
- spreadsheet/CSV as a new primary delivery format;
- fixed 20/30/50 new cards/day;
- fixed maximum reviews = 9999;
- fixed 10-minute learning step;
- copied display-order preset;
- 'descending retrievability prioritizes forgotten cards';
- Easy Days as a zero-workday mechanism.

## Authoritative technical sources

- https://docs.ankiweb.net/manual/deck-options
- https://docs.ankiweb.net/manual/studying
- https://docs.ankiweb.net/manual/syncing
