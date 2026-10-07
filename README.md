# Anki Language Workflow

Portable AI skill/workflow that turns language-learning material into selective, high-quality Anki decks and a validated `.apkg` package.

## Core idea

The AI decides **what is worth learning and which skill should be trained**. Deterministic scripts handle plan validation and Anki package generation.

Default language model:

- target language: the language being learned;
- support language: **English**;
- Portuguese is used only when explicitly requested.

Decks are organized by trained skill:

- `01 Reading`
- `02 Listening`
- `03 Production`
- `04 Pronunciation & Sounds`

Linguistic categories such as `vocabulary`, `chunk`, `collocation`, `grammar`, `word-form`, `word-order`, `minimal-pair`, and `sentence-mining` are tags, not extra micro-decks.

## Card-selection rules

- A source item may create **0, 1, or more cards**.
- Multiple cards are created only when they train genuinely different skills.
- Do not create cards just because a template exists.
- Avoid ambiguous cloze deletion.
- Production prompts must make the intended retrieval target clear without giving away the answer.
- Listening normally puts audio on the front.
- Production/pronunciation normally put audio on the back, unless the task itself is sound discrimination.
- Images are used when they encode meaning, especially concrete concepts, not as decoration.
- Original/native audio is preferred over generated TTS.

## Repository layout

- `anki-language/SKILL.md` — canonical portable skill.
- `anki-language/references/` — pedagogy, card selection, media, and output rules.
- `anki-language/schemas/card-plan.schema.json` — intermediate card-plan contract.
- `anki-language/scripts/` — installer, plan validator, APKG builder, and APKG validator.
- `anki-language/examples/` — example card plan.
- `adapters/` — installation/invocation notes for Codex, Claude Code, and Antigravity.
- `tests/` — smoke tests for deterministic build/validation.

## Quick start

1. Clone this repository.
2. Install runtime dependencies: `python -m pip install -r anki-language/requirements.txt`.
3. Install the skill for your agent using `python anki-language/scripts/install_skill.py <agent> --scope project --project <path>`.
4. Give the agent your source material and invoke the `anki-language` skill.
5. The workflow creates `card-plan.json`, builds the `.apkg`, validates it, and produces a build report.

Example installs:

- Codex: `python anki-language/scripts/install_skill.py codex --scope project --project .`
- Claude Code: `python anki-language/scripts/install_skill.py claude --scope project --project .`
- Antigravity: `python anki-language/scripts/install_skill.py antigravity --scope project --project .`

## Invocation

- Claude Code: `/anki-language <material>`
- Codex: explicitly invoke/name the `anki-language` skill in the client (for clients that expose skill mentions, use `$anki-language`).
- Antigravity: select/discover `anki-language` from skills or explicitly ask the agent to use it.

## Output

Default successful output:

- `<Language>.apkg`
- `<Language>.apkg.report.json`
- `card-plan.json`

The APKG may include text, audio, images, note types, subdecks, and tags. Media is added only when it improves learning and its source/use is permitted.

## Status

Initial implementation. The project intentionally starts small: one portable skill, one intermediate schema, and a deterministic APKG builder.