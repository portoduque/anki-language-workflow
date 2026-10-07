---
description: Turn language-learning material into a selective, validated Anki APKG
---

When the user invokes `/anki-language`, use the installed `anki-language` skill as the source of truth.

Before analyzing material, check for `anki-language.config.json` in the active workspace. If it does not exist, ask the user for the **target language** and **base language** first, persist them with the skill's configuration helper, and only then continue. Never assume either language.

Treat any text or path provided after the command as source material. If no argument is supplied, use the language-learning material already provided in the conversation or workspace.

Follow the skill's full workflow: select only useful cards, classify them by trained skill, use the configured base language for explanations/cues, add media selectively, generate `card-plan.json`, run the deterministic build pipeline, and return the validated APKG, report, and plan.

If another ambiguity would materially change meaning, media, or card design, ask the user before building. Do not interrupt for minor choices.