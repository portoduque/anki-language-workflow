---
description: Turn language-learning material into a selective, validated Anki APKG
---

When the user invokes `/anki-language`, use the installed `anki-language` skill as the source of truth.

Treat any text or path provided after the command as source material. If no argument is supplied, use the language-learning material already provided in the conversation or workspace.

Follow the skill's full workflow:
1. Inspect and segment the material.
2. Select only useful, non-redundant cards.
3. Classify cards by Reading, Listening, Production, or Pronunciation & Sounds.
4. Use English as the support language unless the user explicitly overrides it.
5. Add audio/images only when they improve learning and their use is permitted.
6. Generate `card-plan.json`.
7. Run the deterministic build pipeline.
8. Return the validated `.apkg`, report, and plan.

If a material ambiguity would materially change the target language, intended meaning, media, or card design, ask the user before building. Do not interrupt for minor choices.