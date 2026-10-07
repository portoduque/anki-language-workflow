# Claude Code adapter

The canonical skill is `anki-language/`.

## Project install

`python anki-language/scripts/install_skill.py claude --scope project --project .`

This copies the skill to:

`.claude/skills/anki-language/`

## User install

`python anki-language/scripts/install_skill.py claude --scope user`

This installs under:

`~/.claude/skills/anki-language/`

## Invocation

Claude Code exposes installed skills as slash commands. Use:

`/anki-language <material>`

Example:

`/anki-language ./materials/french-lesson/`