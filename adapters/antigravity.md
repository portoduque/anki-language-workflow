# Google Antigravity adapter

The canonical implementation is `anki-language/`; Antigravity adds a thin slash-workflow because it distinguishes skills from user-invoked workflows.

## One-command IDE install after cloning

`python install.py antigravity`

This installs runtime dependencies, the user skill at `~/.gemini/config/skills/anki-language/`, and the global `/anki-language` workflow.

Project/workspace-only install:

`python install.py antigravity --scope project --project /path/to/workspace`

This installs:

- `.agents/skills/anki-language/`
- `.agents/workflows/anki-language.md`

## Invocation

`/anki-language <material>`

On the **first use in each workspace**, Antigravity must ask for target language and base language before analyzing the material and persist them in `anki-language.config.json`.

## Antigravity CLI

Use `python install.py antigravity-cli`. Project skills use `.agents/skills/`; a user install targets `~/.gemini/antigravity-cli/skills/anki-language/`.