# Anki Reference Library

This directory is the technical reference layer for the `anki-language` skill.

## How the agent should use it

Do **not** load every file on every run.

Fastest route when scripts can be executed:

`python scripts/find_anki_reference.py "<technical need>"`

Examples:

- `python scripts/find_anki_reference.py "FSRS desired retention"`
- `python scripts/find_anki_reference.py "APKG audio media import"`
- `python scripts/find_anki_reference.py "AnkiConnect automation API"`
- `python scripts/find_anki_reference.py "cloze typed answer template"`

The router returns the highest-scoring local reference files plus the official live documentation index.

1. Read this index when an Anki-specific technical decision is required.
2. Open only the topic file(s) that match the decision.
3. Prefer the local summaries for stable concepts.
4. For version-sensitive behavior, compatibility, add-on status, release changes, or details not covered locally, consult the official live sources in [SOURCES.md](SOURCES.md).
5. The official Anki documentation publishes a machine-readable complete index at:
   - https://docs.ankiweb.net/llms.txt
6. When current internet access is available, use that official index to discover the exact page before relying on third-party material.
7. Never copy a third-party configuration blindly. Prefer official/native functionality and verify compatibility with the user's current Anki version.

## Routing table

| Need | Read first |
| --- | --- |
| What are notes, cards, fields, decks, siblings, note types? | [01-core-model-and-organization.md](01-core-model-and-organization.md) |
| Design fields/note types/card types | [02-notes-fields-card-types.md](02-notes-fields-card-types.md) |
| HTML/CSS/templates/field replacement/TTS/type-answer | [03-templates-html-css-tts.md](03-templates-html-css-tts.md) |
| Cloze, Image Occlusion, typed answers | [04-cloze-image-occlusion-typed-answer.md](04-cloze-image-occlusion-typed-answer.md) |
| Audio, images, media filenames, TTS | [05-media-audio-images-tts.md](05-media-audio-images-tts.md) |
| Decks, subdecks, tags, browser, search | [06-decks-tags-browser-search.md](06-decks-tags-browser-search.md) |
| Scheduling, answer buttons, FSRS, desired retention | [07-scheduling-fsrs-study-options.md](07-scheduling-fsrs-study-options.md) |
| CSV/TSV, APKG/COLPKG, import/export | [08-import-export-packages.md](08-import-export-packages.md) |
| Sync, backups, profiles, collection/media files | [09-sync-backup-profiles-files.md](09-sync-backup-profiles-files.md) |
| Statistics, filtered decks, leeches | [10-stats-filtered-decks-leeches.md](10-stats-filtered-decks-leeches.md) |
| Useful add-ons and compatibility cautions | [11-useful-addons.md](11-useful-addons.md) |
| AnkiConnect, add-on development, APIs, automation | [12-automation-development-apis.md](12-automation-development-apis.md) |
| Deep AnkiConnect configuration/actions/examples | [../anki-connect/INDEX.md](../anki-connect/INDEX.md) |
| AnkiMobile/AnkiDroid/platform compatibility | [13-platforms-mobile-compatibility.md](13-platforms-mobile-compatibility.md) |
| Troubleshooting, security, performance, version-sensitive decisions | [14-troubleshooting-security-performance.md](14-troubleshooting-security-performance.md) |
| Installation, upgrades, preferences, interface settings | [15-installation-preferences-configuration.md](15-installation-preferences-configuration.md) |
| RTL, furigana/ruby, fonts, dictionary links, typed-answer language details | [16-language-rendering-fonts-rtl-furigana.md](16-language-rendering-fonts-rtl-furigana.md) |
| MathJax, LaTeX, mathematical symbols | [17-math-symbols-mathjax-latex.md](17-math-symbols-mathjax-latex.md) |
| What official documentation families are covered locally | [COVERAGE.md](COVERAGE.md) |
| Authoritative URLs and live-doc discovery | [SOURCES.md](SOURCES.md) |

## Rules for this project

For normal card **pedagogy**, the source of truth remains:
- `../card-selection.md`
- `../pedagogy.md`

This Anki library answers **technical implementation questions**: what Anki supports, how templates/imports/media/scheduling work, what package format to use, and when an add-on is appropriate.

If a technical Anki choice conflicts with the project's pedagogical card rules, preserve the pedagogical rule and choose a different Anki implementation.
