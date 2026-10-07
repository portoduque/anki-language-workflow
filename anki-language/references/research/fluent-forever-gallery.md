# Fluent Forever Gallery — Selective Adaptation Note

Source family analyzed: Gabriel Wyner's Fluent Forever “Gallery” and its linked card-type pages.

Primary URLs:

- https://blog.fluent-forever.com/gallery/
- https://blog.fluent-forever.com/ear-training-flashcards/
- https://blog.fluent-forever.com/spelling-sound-flashcards/
- https://blog.fluent-forever.com/simple-word-flashcards/
- https://blog.fluent-forever.com/new-word-flashcards/
- https://blog.fluent-forever.com/new-word-form-flashcards/
- https://blog.fluent-forever.com/word-order-flashcards/

## Context

The Gallery was originally published in 2014. The site itself added 2022 notices saying these are older Anki instructions and that much has changed.

Treat the material as **pedagogical inspiration**, not current Anki configuration documentation.

Current Anki implementation details come from the project's official Anki reference library instead.

## Useful ideas adopted

### 1. Different retrieval operations deserve different card designs

The Gallery distinguishes:
- ear training/minimal pairs;
- spelling↔sound;
- written vocabulary recognition;
- production;
- word forms;
- word order.

This aligns with this project's skill-based architecture and selective multi-card rule.

### 2. Minimal pairs should isolate the sound contrast

The Gallery prefers the same person pronouncing both members when possible because it makes the learner attend to the target acoustic difference.

Adaptation:
- prefer the same speaker/voice and similar recording conditions;
- do not make it a hard blocker when matched recordings are unavailable.

### 3. Spelling/sound cards should fade out

The Gallery reports that spelling cards were especially useful early and became easy/boring after roughly 100–300 words.

Adaptation:
- treat spelling/spelling-sound as scaffolding;
- stop generating them when representative spelling↔sound mappings are reliably automatic;
- do **not** hard-code 100–300 words as a universal threshold.

### 4. Contextual vocabulary and morphology

The Gallery moves abstract vocabulary, conjugations, inflections, and word order into understandable example sentences.

Adaptation:
- preserve contextual word/chunk learning;
- use sentence mining selectively;
- use guided prompts so the learner knows exactly which form/function is being retrieved.

### 5. Semantic success may differ from exact example reproduction

For some comprehension/usage cards, the Gallery explicitly accepts another valid example sentence/context instead of requiring the stored example.

Adaptation:
- when the target is meaning or valid usage, another natural demonstration can count as correct;
- exact wording remains required when wording/collocation/morphology/spelling/word order is the actual target.

### 6. Target-language definitions can become useful later

The Gallery suggests monolingual definitions at intermediate/advanced levels.

Adaptation:
- target-language definitions are optional when easily comprehensible and useful;
- they do not replace the configured base language by rule;
- do not add difficult monolingual definitions that create new learning targets.

### 7. Personal associations can strengthen concrete vocabulary

The Gallery recommends connecting simple vocabulary to real personal associations.

Adaptation:
- use a genuine association only when supplied naturally by the user/material;
- never invent private/personal details merely to make a card “personal.”

## Ideas intentionally NOT adopted

### Rigid “no translation on cards”

The Gallery strongly favors images/context over translation.

This project does not adopt a translation ban. The configured base language is permitted when it creates the clearest, fastest, least ambiguous retrieval cue.

### An image for almost every sentence

The Gallery often recommends a loosely related picture even when it is not a precise representation.

This project keeps the stricter rule: images must improve retrieval/comprehension. Decorative or ambiguous images add search/build/review cost without enough benefit.

### Fixed phase progression

The Gallery organizes study into Sounds → Simple Words → Sentences/Grammar.

This is useful as a conceptual progression but not a mandatory workflow. The skill reacts to the learner's material and demonstrated needs instead of forcing everyone through the same stages.

### Automatic generation of every related card type

Some Gallery note types naturally generate comprehension + production + optional spelling siblings.

This project keeps selective multi-card generation. Each sibling must independently justify its future review cost.

### Old Anki scheduling settings

The minimal-pair page describes special settings requiring several consecutive correct answers.

Do not copy these historical settings. Scheduling behavior is governed by current Anki/FSRS guidance in the technical reference library.

### Forvo/Google Images as default automation

Those recommendations reflect the older manual workflow.

Current project media rules use permitted sources, provenance, validation, Piper TTS, Openverse/Wikimedia, and AnkiConnect delivery where appropriate.
