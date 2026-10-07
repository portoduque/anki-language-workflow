# Anki Language Workflow

AI-agnostic and language-agnostic workflow that turns study material into a small, selective, import-ready Anki `.apkg` deck with optional audio, images, tags, and validated card templates.

**The repository has no default language and no required AI provider.** Codex, Claude Code, and Google Antigravity have ready-made adapters, while any other AI can use the same canonical `SKILL.md` and deterministic Python pipeline.

## What happens on first use

Every workspace starts unconfigured. Before the AI analyzes the first material, it must ask you two questions:

1. **Target language** — the language you are learning, such as French, Japanese, Spanish, German, Arabic, etc.
2. **Base language** — the language that should explain, translate, cue, and guide the target language, such as English, Portuguese, Spanish, etc.

There is **no default** for either value. The answers are stored in `anki-language.config.json` in that workspace and reused on later runs until you change them.

Examples of valid configurations:

- target French / base English;
- target Japanese / base Portuguese;
- target German / base Spanish;
- target English / base French.

## What the workflow creates

The AI first decides whether each source item deserves a card at all. A source item may create zero, one, or several cards, but multiple cards are allowed only when they train genuinely different skills.

Deck hierarchy:

- `<TargetLanguage>::01 Reading`
- `<TargetLanguage>::02 Listening`
- `<TargetLanguage>::03 Production`
- `<TargetLanguage>::04 Pronunciation & Sounds`

Vocabulary, grammar, chunks, collocations, word forms, minimal pairs, source names, and similar dimensions are stored as tags instead of extra micro-decks.

Core rules:

- no card is created just because a template exists;
- no blind or ambiguous cloze;
- listening normally places audio on the front;
- production normally places audio on the back;
- images are added only when they improve retrieval;
- original/native permitted audio is preferred over TTS;
- explanations and cues use the configured base language;
- all generated APKG files pass deterministic validation before delivery.

## Official card-creation rules

These are product rules, not suggestions. The complete normative specification lives in `anki-language/references/card-selection.md`.

1. **Minimum useful set:** each source unit may generate 0, 1, or several cards.
2. **Selective multi-card reuse:** the same sentence, word, expression, audio, image, or passage may appear in multiple skill decks when each card trains a genuinely different and worthwhile retrieval operation.
3. **Marginal-benefit rule:** every extra sibling card must add enough learning value to justify its future review cost. Optimize **memory efficiency per review minute**, not card volume.
4. **No quotas:** never create Reading + Listening + Production + Pronunciation automatically.
5. **One retrieval target:** each card tests one primary piece of knowledge or skill.
6. **Self-orienting front:** every front identifies `<TargetLanguage> — <Skill>` so mixed reviews never show a contextless question.
7. **No guessing the author's intention:** prompts must make the intended retrieval clear without revealing the answer.
8. **No blind cloze:** a blank is used only when a semantic/function cue, lemma, or other constraint makes the intended answer sufficiently unambiguous.
9. **No automatic reverse cards:** recognition and production are different skills and get separate cards only when both matter.
10. **Translation is allowed:** the configured base language may be used when it is the clearest/fastest cue; translation is not banned on principle.
11. **Reading is selective:** use natural written context for useful recognition; skip material already understood reliably.
12. **Listening is audio-first:** do not reveal the transcript on the front; put transcript/base-language meaning on the back.
13. **Production is constrained:** front uses a precise base-language meaning/situation/context; answer and normally audio stay on the back.
14. **Pronunciation/Sounds is targeted:** use pronunciation, minimal pairs, sound discrimination, or spelling-sound cards only when sound is worth training; never reveal the written answer on a discrimination front.
15. **Prefer useful chunks/collocations/patterns:** do not reduce a useful expression to isolated words when the combination is the knowledge that matters.
16. **Sentence mining is selective:** do not turn every source sentence into a card; prefer natural, useful, comprehensible context with one main focus.
17. **Images are functional, not decorative:** prioritize concrete/visual concepts; skip ambiguous images that do not improve retrieval.
18. **Audio is functional, not mandatory:** prefer user-supplied original audio, then permitted native-speaker audio, then permitted high-quality TTS.
19. **Avoid redundancy/interference:** skip near-duplicate cards and improve prompts that make similar answers confusable.
20. **Fast reviews:** answers should be concise enough to verify recall quickly; extra explanation is secondary.
21. **Prefer the user's material:** preserve useful source sentences/audio/context instead of replacing them with generic content without reason.
22. **Ask instead of guessing:** if uncertainty changes meaning, target expression, transcription, register, acceptable answers, or media rights, ask the user before building.

A source reused across multiple decks is valid only when each card covers a real additional skill gap. If the extra card mostly repeats the same retrieval, discard it.

Final acceptance test for every card: **useful, distinct, clear, atomic, fast**. If one fails, revise or discard the card.

## Requirements

- Git;
- Python 3.11+;
- an AI coding/agent environment with filesystem and Python execution for fully automatic APKG generation.

A chat-only AI can still follow the pedagogical rules and produce `card-plan.json`, but building the final `.apkg` requires a runtime capable of executing the included Python scripts.

## Installation from zero

### 1. Clone the repository

`git clone https://github.com/portoduque/anki-language-workflow.git`

`cd anki-language-workflow`

### 2. Install for your AI with one command

Choose exactly one:

**Codex**

`python install.py codex`

**Claude Code**

`python install.py claude`

**Google Antigravity IDE**

`python install.py antigravity`

**Antigravity CLI**

`python install.py antigravity-cli`

**Any other Agent-Skills-compatible AI**

`python install.py generic --dest /path/to/your-ai/skills/anki-language`

The one-command installer installs the Python dependencies and copies the canonical skill to the correct user-level location. Use `--skip-deps` if you manage Python dependencies yourself.

To install only inside one project/workspace instead of globally, add:

`--scope project --project /path/to/workspace`

## How to use after installation

Open the workspace containing your language-learning material.

### Codex

Invoke:

`$anki-language`

Then provide or point to the material. On the first run, Codex asks for target language and base language before doing anything else.

### Claude Code

Invoke:

`/anki-language <material>`

Example:

`/anki-language ./materials/lesson-01/`

On the first run, Claude asks for target language and base language.

### Google Antigravity

Invoke:

`/anki-language <material>`

The installer adds both the skill and a thin Antigravity workflow. On the first run, Antigravity asks for target language and base language.

### Any other AI

If it supports Agent Skills, invoke the installed skill through that product's normal skill mechanism. If it does not, instruct the AI:

`Read anki-language/SKILL.md and follow it as the workflow contract for this material.`

## First-run configuration details

After the user answers the two language questions, the agent persists them with the included helper:

`python scripts/configure.py --target-name French --target-code fr --base-name English --base-code en --output ./anki-language.config.json`

The exact values are examples only; no language is preferred by the project.

To switch languages later, ask the AI to change the target/base configuration or run the helper again with new values.

## End-to-end workflow

1. User invokes the skill/workflow and provides material.
2. If this is the first run in the workspace, the AI asks for target language and base language and saves them.
3. AI inspects all source material.
4. AI selects only useful learning units.
5. AI assigns Reading, Listening, Production, or Pronunciation & Sounds.
6. AI decides whether audio/image actually adds value.
7. AI creates `card-plan.json` using the configured target/base languages.
8. Deterministic scripts validate the plan and media.
9. Builder generates the `.apkg`.
10. Validator opens the internal Anki SQLite collection and checks notes, cards, decks, and media.
11. AI returns the final `.apkg`, report, and card plan.

## Deterministic build

From the installed skill directory:

`python scripts/build.py /path/to/card-plan.json --output /path/to/Language.apkg`

The pipeline checks JSON Schema, semantic rules, media existence/collisions, APKG ZIP/media manifest, embedded Anki SQLite database, note/card counts, and expected subdecks.

## Repository architecture

- `anki-language/SKILL.md` — canonical provider-independent workflow.
- `anki-language/references/` — pedagogy, card selection, media, output contract.
- `anki-language/schemas/` — workspace configuration and card-plan schemas.
- `anki-language/scripts/` — configuration, build, install, and validation scripts.
- `anki-language/assets/` — thin provider-specific assets such as the Antigravity workflow.
- `anki-language/agents/openai.yaml` — optional OpenAI/Codex interface metadata.
- `adapters/` — usage notes for specific AIs plus a generic adapter.
- `evals/` — behavioral evaluation cases.
- `tests/` — deterministic regression tests.

## AI-agnostic design rule

The canonical behavior must stay in `anki-language/SKILL.md`, `references/`, `schemas/`, and `scripts/`. Provider-specific files must remain thin adapters. A feature must not require one particular model/vendor unless it is explicitly optional.

## README maintenance rule

**Every repository change must update this README when the change affects behavior, installation, usage, architecture, configuration, dependencies, commands, outputs, or supported agents.**

To make that rule enforceable, pull-request CI checks that code/project changes include a `README.md` update. The README is treated as part of the product, not an afterthought.

## Validation and development

Validate the Agent Skill bundle:

`python anki-language/scripts/validate_skill.py anki-language`

Run tests:

`pytest -q`

## Output

A normal successful run produces:

- `<TargetLanguage>.apkg`;
- `<TargetLanguage>.apkg.report.json`;
- `card-plan.json`;
- optional media files embedded inside the APKG.

Media is only included when useful and when its use is permitted.