# Codex adapter

The canonical skill is `anki-language/`.

## Project install

`python anki-language/scripts/install_skill.py codex --scope project --project .`

Installs to `.agents/skills/anki-language/`, the repo-local skill layout used by Codex.

## User install

`python anki-language/scripts/install_skill.py codex --scope user`

Installs to `~/.agents/skills/anki-language/`.

## Invocation

Use `$anki-language` for explicit invocation. Codex may also select the skill automatically when the request matches its description.

The bundled `agents/openai.yaml` supplies OpenAI-facing display metadata and a default prompt while the portable logic stays in `SKILL.md`.

Keep repository-wide coding conventions in `AGENTS.md`; keep this repeatable language-learning procedure in the skill.