# Claude Code adapter

The canonical implementation is `anki-language/`; Claude Code is only one execution surface.

## One-command install after cloning

`python install.py claude`

This installs runtime dependencies and the skill for the current user at `~/.claude/skills/anki-language/`.

Project-only install:

`python install.py claude --scope project --project /path/to/workspace`

## Invocation

`/anki-language <material>`

On the **first use in each workspace**, Claude must ask for target language and base language before analyzing the material. Those choices are saved in `anki-language.config.json`.

No duplicate `.claude/commands/` implementation is needed; the canonical rules stay in the portable skill.