# Generic / other AI adapter

`anki-language` is intentionally AI-agnostic. The canonical bundle does not depend on Codex, Claude, or Antigravity.

## If your AI supports Agent Skills

Find the directory where that AI discovers skills, then run:

`python install.py generic --dest /path/to/that-ai/skills/anki-language`

The installer copies the complete canonical skill and installs the Python runtime dependencies.

## If your AI does not support Agent Skills

Give the AI access to this repository and instruct it to read `anki-language/SKILL.md` as the workflow contract. It can then use the deterministic scripts under `anki-language/scripts/` directly.

For fully automatic APKG generation, the AI/runtime needs filesystem access and the ability to execute Python. A chat-only model without file/shell tools can still produce a card plan, but cannot independently build the final APKG.

## First run

Regardless of AI provider, the first run in a workspace must ask the user for:

1. target language;
2. base language.

No language is assumed or hardcoded.