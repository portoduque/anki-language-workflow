# Claude Code adapter

The canonical skill is `anki-language/`.

## Project install

`python anki-language/scripts/install_skill.py claude --scope project --project .`

Installs to `.claude/skills/anki-language/`.

## User install

`python anki-language/scripts/install_skill.py claude --scope user`

Installs to `~/.claude/skills/anki-language/`.

## Invocation

Claude Code can discover skills automatically or invoke them directly as slash commands:

`/anki-language <material>`

Example: `/anki-language ./materials/french-lesson/`

No separate legacy `.claude/commands/` file is required. The reusable workflow belongs in the skill, while always-on project conventions belong in `CLAUDE.md` or scoped rules.