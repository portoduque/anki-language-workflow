# Sources and Live Documentation Map

Last curated: 2026-10-06.

This file points to authoritative/current sources. Local files in this directory are concise operational summaries, not replacements for the upstream documentation.

## Highest-priority source

### Official Anki Docs master index

https://docs.ankiweb.net/llms.txt

This is the preferred discovery entrypoint. It currently indexes the official:

- Desktop Manual;
- AnkiMobile Manual;
- Support FAQs;
- Add-on Development docs;
- Core Developer docs;
- Translator docs;
- Release notes;
- platform-specific pages.

When a local reference does not contain enough detail, use this index to find the exact current official page.

## Desktop Manual — core topics

- Getting Started: https://docs.ankiweb.net/manual/getting-started
- Studying: https://docs.ankiweb.net/manual/studying
- Adding/Editing: https://docs.ankiweb.net/manual/editing
- Preferences: https://docs.ankiweb.net/manual/preferences
- Deck Options / FSRS: https://docs.ankiweb.net/manual/deck-options
- Syncing: https://docs.ankiweb.net/manual/syncing
- Profiles: https://docs.ankiweb.net/manual/profiles
- Browsing: https://docs.ankiweb.net/manual/browsing
- Filtered Decks: https://docs.ankiweb.net/manual/filtered-decks
- Searching: https://docs.ankiweb.net/manual/searching
- Exporting: https://docs.ankiweb.net/manual/exporting
- Backups: https://docs.ankiweb.net/manual/backups
- Managing Files: https://docs.ankiweb.net/manual/files
- Statistics: https://docs.ankiweb.net/manual/stats
- Media: https://docs.ankiweb.net/manual/media
- Math & Symbols: https://docs.ankiweb.net/manual/math
- Leeches: https://docs.ankiweb.net/manual/leeches
- Add-ons: https://docs.ankiweb.net/manual/addons
- Troubleshooting: https://docs.ankiweb.net/manual/troubleshooting

## Templates

- Intro: https://docs.ankiweb.net/manual/templates/intro
- Field replacements/TTS/type-answer: https://docs.ankiweb.net/manual/templates/fields
- Card generation: https://docs.ankiweb.net/manual/templates/generation
- Styling/HTML/CSS: https://docs.ankiweb.net/manual/templates/styling
- Template checks/errors: https://docs.ankiweb.net/manual/templates/errors

## Importing

- Intro: https://docs.ankiweb.net/manual/importing/intro
- Text files/CSV/TSV/media headers: https://docs.ankiweb.net/manual/importing/text-files
- Packaged decks: https://docs.ankiweb.net/manual/importing/packaged-decks
- Exporting/APKG/COLPKG: https://docs.ankiweb.net/manual/exporting

## FAQs especially relevant to this project

Use the official llms index to locate FAQ pages. High-value topics include:

- FSRS FAQ;
- spaced repetition algorithm;
- missing sounds/images;
- TTS support;
- card template problems;
- cloze errors;
- cards reversed/duplicated;
- syncing/media-sync;
- backups/data recovery;
- study order;
- exam preparation;
- scheduler behavior.

## Add-on development

Root/index:
- https://docs.ankiweb.net/addons/intro
- https://docs.ankiweb.net/llms.txt

Important topics:
- basic add-on;
- `anki` module;
- hooks/filters;
- background operations;
- Qt/PyQt;
- config;
- reviewer JavaScript;
- debugging;
- sharing;
- hook reference;
- porting.

## Core development/APIs

- Python API: https://docs.ankiweb.net/developers/api-python
- Rust API: https://docs.ankiweb.net/developers/api-rust
- Architecture: https://docs.ankiweb.net/developers/architecture
- Core repository: https://github.com/ankitects/anki

## Mobile

- AnkiMobile: https://docs.ankiweb.net/ankimobile/intro
- AnkiDroid manual: https://docs.ankidroid.org/manual.html

## Add-ons discovery

- Official AnkiWeb add-on directory: https://ankiweb.net/shared/addons
- Official/community support forum: https://forums.ankiweb.net/c/anki/add-ons/11

Specific projects used in the curated add-on guide:
- AnkiConnect: https://github.com/ankiultimate/anki-connect
- HyperTTS: https://github.com/Vocab-Apps/anki-hyper-tts
- FSRS Helper: https://github.com/open-spaced-repetition/fsrs4anki-helper
- Review Heatmap: https://github.com/glutanimate/review-heatmap
- AnkiMorphs: https://github.com/mortii/anki-morphs

## Source priority

When sources disagree, use this order:

1. current official Anki Docs page;
2. current official release notes/FAQ;
3. current AnkiWeb add-on listing;
4. maintained add-on's official source repository/docs;
5. Anki Forums support thread;
6. other community material.

Do not let an old blog post override current native Anki behavior.
