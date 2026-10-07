# Writing cards — fast, single-gap typing

## Source evidence

- Official Anki Manual: [Checking Your Answer](https://docs.ankiweb.net/templates/fields.html#checking-your-answer) documents `{{type:Field}}` on a **regular** note type, comparison on reveal with `{{FrontSide}}`, one single-line typing comparison per card, and user-controlled review ratings. The feature is **not available as an input box in AnkiWeb or Anki's preview**, and its display/feedback may differ on mobile. Exact accents are compared unless `type:nc` is used.
- Official Anki Manual: [Card Generation / Cloze Templates](https://docs.ankiweb.net/templates/generation.html) explains that real Anki Cloze cards use a special note type and may generate multiple sibling cards. This workflow intentionally does **not** need that structure.
- Official Anki Manual: [Card Templates](https://docs.ankiweb.net/templates/intro.html) documents portable HTML/CSS note templates.
- [Anki community discussion: typing French](https://www.reddit.com/r/Anki/comments/oz8hi0/) describes the tradeoff: whole-phrase translation can feel like sentence memorization and minor typos can make reviews feel costly. Contextual gaps are one alternative, not a requirement to multiply card directions.
- [Anki community discussion: contextual clozes](https://www.reddit.com/r/languagelearning/comments/we1p07/) describes the utility of writing phrases in context. Community experiences are anecdotes, not performance guarantees.
- [Anki community discussion: overfitting on clozes](https://www.reddit.com/r/Anki/comments/1qagj9z/) flags that a familiar card pattern can be memorized without transferable language ability; avoid massive batches of nearly identical gaps.

## Decision for this repository

Add a fifth, selectively generated skill deck: `05 Writing`. It is **independent writing/orthographic recall**, not an automatic reversed Production card or a handwriting exercise.

Use a dedicated ordinary Anki model, **Anki Language v5 — Writing**, sharing the existing UI/CSS system with a distinct blue skill accent. No add-on, JavaScript, separate cloze model, type-answer comparison engine, external API, or new scheduler.

The agent supplies only:

- `target_text`: a **short natural sentence/utterance**, for example `Je vais à l'école.`;
- `writing_answer`: one **exact, unique** word or useful short chunk within the sentence, for example `à l'école`;
- `prompt`: a **short semantic or grammatical cue** that makes the missing part answerable without showing it (in configured base language where helpful);
- optional `base_text`, `source`, `notes`, `focus`, and audio on **the back**, only when useful.

The deterministic builder splits `target_text` around `writing_answer` into fields `WritingBefore`, `WritingAfter`, and `WritingAnswer`. The front renders the two visible parts with **one clearly marked gap** and `{{type:WritingAnswer}}`, while hiding `{{Target}}`. The back uses `{{FrontSide}}` to trigger the built-in comparison, then shows the whole correct sentence, the exact missing chunk, and concise optional support.

### Creation/review gates

1. **Fast:** one short word or reusable chunk to type, not an entire multi-clause sentence; the visible sentence is itself short.
2. **Answerable:** enough semantic/grammar context to identify the intended word/form; never a blind ambiguous blank.
3. **Independent:** choose Writing when producing **correct spelling, accent, article, conjugation, or small written phrase** matters beyond existing Reading/Production. Do **not** automatically create Writing for every source chunk.
4. **Natural:** do not cut inside a word or fixed expression just to create a gap. One answer appears **exactly once**; if it appears multiple times, select a clearer short sentence. Writing also supports meaningful chunks from scripts without spaces (e.g., Japanese/Chinese); their semantic boundaries remain an AI selection decision, not a Latin whitespace assumption.
5. **Single-line:** one typed answer only. No multi-gap cloze sets, handwriting canvas, typing of complete paragraphs, or arbitrary word-count caps.
6. **Feedback, not automatic scoring:** Anki shows the typed comparison; the learner grades the review. Normal spelling/diacritic differences matter for Writing, so do **not** disable accent checking by default.
7. **Portability:** type-answer input is available during compatible Anki Desktop/mobile reviews. The AnkiWeb reviewer and preview do not show the typing input; in those environments this is not an interactive Writing test. Spot-check on intended devices.
8. **Audio:** optional original or generated answer audio is played only after reveal; if source audio is long, select the matching short `audio_clip` before delivery.

### What this intentionally does not test

Typing a missing chunk practices local written recall and orthography, not free writing or composition. Longer composition, register decisions, and unrestricted sentence planning still require separate practice. The policy targets fast Anki reviews, so it deliberately does not turn every grammar/sentence source into multiple typed cards.
