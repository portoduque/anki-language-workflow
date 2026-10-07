# Google Antigravity adapter

Antigravity distinguishes on-demand **skills** from user-invoked **workflows**. This project installs both when using the IDE adapter.

## Project/workspace install

`python anki-language/scripts/install_skill.py antigravity --scope project --project .`

Installs:
- skill: `.agents/skills/anki-language/`
- slash workflow: `.agents/workflows/anki-language.md`

Invoke with `/anki-language <material>`. The workflow is intentionally thin and delegates the real rules to the skill.

## IDE global install

`python anki-language/scripts/install_skill.py antigravity --scope user`

Installs the skill to `~/.gemini/config/skills/anki-language/` and the workflow to `~/.gemini/config/global_workflows/anki-language.md`.

## Antigravity CLI

Project skills also use `.agents/skills/`. For a CLI-specific user install use:

`python anki-language/scripts/install_skill.py antigravity-cli --scope user`

This targets `~/.gemini/antigravity-cli/skills/anki-language/`. Use `/skills` to verify discovery.

The separation is deliberate: a skill is reusable knowledge loaded on demand; a workflow gives the IDE the explicit `/anki-language` entry point.