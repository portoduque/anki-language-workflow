---
description: Turn language-learning material into selective Anki cards with automatic validated media and APKG/live delivery
---

When the user invokes `/anki-language`, use the installed `anki-language` skill as the source of truth.

Before analyzing material, check for `anki-language.config.json` in the active workspace. If it does not exist, ask the user for the **target language** and **base language** first, persist them with the skill's configuration helper, and only then continue. Never assume either language.

Treat any text or path provided after the command as source material. If no argument is supplied, use the language-learning material already provided in the conversation or workspace.

Follow the skill's full workflow. In particular: create the minimum useful number of cards; allow the same source item to create cards in multiple skill decks when each trains a distinct worthwhile retrieval operation; never generate all card types automatically; require the learning benefit of every extra sibling card to justify its future review cost; keep one primary retrieval target per card; make every front self-orienting; forbid blind/ambiguous cloze; create recognition/production siblings only when both skills matter; add audio/images only when useful. For text-only cards, use automatic media requests when they add learning value. Run the end-to-end media pipeline so every audio/image is decoded and hashed before packaging/upload. For live AnkiConnect delivery, additionally verify the uploaded bytes and note-field references after creation. Never bypass media validation or claim success after a failed validation.

If another ambiguity would materially change meaning, media, or card design, ask the user before building. Do not interrupt for minor choices.