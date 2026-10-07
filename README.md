# Anki Language Workflow

Portable Agent Skill/workflow that turns language-learning material into selective, high-quality Anki decks and a deeply validated `.apkg` package.

It targets **Codex, Claude Code, and Google Antigravity** without maintaining three copies of the learning logic.

## Design

The model decides **what is worth learning and which skill should be trained**. Deterministic scripts handle schema validation, media checks, APKG generation, and package verification.

Defaults:

- target language: the language being learned;
- support language: **English**;
- Portuguese is used only when explicitly requested.

Decks are organized by trained skill:

- `01 Reading`
- `02 Listening`
- `03 Production`
- `04 Pronunciation & Sounds`

Linguistic dimensions such as `vocabulary`, `chunk`, `collocation`, `grammar`, `word-form`, `word-order`, `minimal-pair`, and `sentence-mining` are tags, not extra micro-decks.

## Cross-agent architecture

All three products support filesystem-based Agent Skills centered on `SKILL.md`. This repository keeps one canonical skill and adds only the product-specific surface each agent needs:

| Product | Project skill path | Explicit invocation | Product-specific layer |
| --- | --- | --- | --- |
| Codex | `.agents/skills/anki-language/` | `$anki-language` | `agents/openai.yaml` |
| Claude Code | `.claude/skills/anki-language/` | `/anki-language` | none required |
| Antigravity IDE | `.agents/skills/anki-language/` | `/anki-language` | thin `.agents/workflows/anki-language.md` |

This deliberately avoids pretending the products have identical command systems.

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
- `anki-language/agents/openai.yaml` — optional OpenAI/Codex interface metadata.
- `anki-language/references/` — detailed pedagogy, selection, media, and output rules.
- `anki-language/schemas/card-plan.schema.json` — intermediate plan contract.
- `anki-language/scripts/` — installer, validators, APKG builder, and one-command build pipeline.
- `anki-language/assets/antigravity-workflow.md` — thin Antigravity slash-workflow template.
- `anki-language/examples/` — example card plan.
- `adapters/` — product-specific installation/invocation notes.
- `tests/` — deterministic and cross-agent contract tests.

## Quick start

Install dependencies:

`python -m pip install -r anki-language/requirements.txt`

Install the skill:

- Codex project: `python anki-language/scripts/install_skill.py codex --scope project --project .`
- Claude Code project: `python anki-language/scripts/install_skill.py claude --scope project --project .`
- Antigravity project: `python anki-language/scripts/install_skill.py antigravity --scope project --project .`

Then invoke:

- Codex: `$anki-language`
- Claude Code: `/anki-language`
- Antigravity IDE: `/anki-language`

## Deterministic build

After the agent creates `card-plan.json`, run the pipeline from the installed skill directory:

`python scripts/build.py /path/to/card-plan.json --output /path/to/French.apkg`

The pipeline validates:

1. JSON Schema and workflow-specific semantic rules.
2. Required audio for Listening/sound-discrimination cards.
3. Media existence and basename collisions.
4. APKG ZIP structure and media manifest.
5. The embedded Anki SQLite collection.
6. Expected note/card counts.
7. Expected subdeck names.

## Output

- `<Language>.apkg`
- `<Language>.apkg.report.json`
- `card-plan.json`

The APKG may include text, audio, images, note types, subdecks, and tags. Media is added only when it improves learning and its use is permitted.

## Validation

Validate the portable skill bundle:

`python anki-language/scripts/validate_skill.py anki-language`

Run all tests:

`pytest -q`