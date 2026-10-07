# Google Antigravity adapter

The canonical skill is `anki-language/`.

## Project install

`python anki-language/scripts/install_skill.py antigravity --scope project --project .`

This copies the skill to:

`.agents/skills/anki-language/`

## User/global install

`python anki-language/scripts/install_skill.py antigravity --scope user`

This installs under:

`~/.gemini/config/skills/anki-language/`

## Invocation

Use Antigravity's skill discovery (`/skills`) or explicitly tell the agent to use the `anki-language` skill with the supplied material.

The workflow itself is identical to the Codex/Claude versions because the canonical `SKILL.md` is shared.