# Codex adapter

The canonical skill is `anki-language/`.

## Project install

`python anki-language/scripts/install_skill.py codex --scope project --project .`

This copies the skill to:

`.agents/skills/anki-language/`

## User install

`python anki-language/scripts/install_skill.py codex --scope user`

This installs under `$CODEX_HOME/skills/anki-language` (defaulting to `~/.codex/skills/anki-language`).

## Invocation

Explicitly name the `anki-language` skill in Codex. Clients that expose skill mentions can use `$anki-language`.

Give the material path(s) and target language when known. If target language is obvious from the material, the skill may infer it.