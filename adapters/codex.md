# Codex adapter

The canonical implementation is `anki-language/`; Codex is only one execution surface.

## One-command install after cloning

`python install.py codex`

This installs runtime dependencies and the skill for the current user at `~/.agents/skills/anki-language/`.

Project-only install:

`python install.py codex --scope project --project /path/to/workspace`

## Invocation

Use `$anki-language` explicitly, or let Codex discover the skill from its description.

On the **first use in each workspace**, the skill must ask for target language and base language before analyzing the material. Those choices are saved in `anki-language.config.json` for later runs.

The OpenAI-specific `agents/openai.yaml` remains optional metadata; the learning workflow itself stays provider-agnostic.