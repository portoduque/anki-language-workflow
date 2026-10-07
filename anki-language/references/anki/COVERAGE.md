# Anki Documentation Coverage Map

This map shows where the major official documentation families are represented in the local reference library.

The **official exhaustive source index** remains:

https://docs.ankiweb.net/llms.txt

The local library is a curated operational summary. For details, edge cases, exact UI text, release-specific behavior, or topics not summarized locally, follow the official live index.

## Desktop Manual

| Official topic | Local reference |
| --- | --- |
| Introduction / Getting Started / Background | 01, 15 |
| Studying | 07 |
| Adding/Editing | 01, 02, 04, 06 |
| Preferences | 15 |
| Deck Options | 07 |
| Syncing with AnkiWeb | 09 |
| Profiles | 09 |
| Browsing | 06 |
| Filtered Decks & Cramming | 06, 10 |
| Searching | 06 |
| Exporting | 08 |
| Backups | 09 |
| Managing Files | 09, 14 |
| Statistics | 10 |
| Media | 05 |
| Math & Symbols | 17 |
| Leeches | 10 |
| Add-ons | 11 |
| Troubleshooting | 14 |
| Self-hosted Sync Server | SOURCES/live docs |
| Miscellaneous / Resources | SOURCES/live docs |
| Platform Notes (Windows/macOS/Linux) | 13, 15 |

## Templates

| Official topic | Local reference |
| --- | --- |
| Card Templates intro | 02, 03 |
| Field Replacements | 03, 16 |
| Card Generation | 02, 03 |
| Styling & HTML | 03, 16 |
| Checks and Errors | 14 |

## Importing

| Official topic | Local reference |
| --- | --- |
| Import intro | 08 |
| Text Files | 08, 05 |
| Packaged Decks | 08 |

## FAQs

FAQ coverage is routed by topic:
- cards/templates/cloze/media → 03, 04, 05, 14;
- decks/scheduling → 06, 07;
- sync/AnkiWeb → 09, 14;
- desktop/platform → 13, 15;
- FSRS → 07;
- data recovery → 09, 14.

For an exact FAQ, use the official `llms.txt` index.

## Add-on Development

Covered in:
- 11 useful add-ons;
- 12 automation/development/APIs;
- 14 troubleshooting/security.

The exact official hook/API reference should be opened live when writing or updating an add-on.

## Core Development

Covered at routing/reference level in 12 and SOURCES. Core Anki contribution/build internals are intentionally **live-doc only** because they change quickly and are not needed for normal deck generation.

## AnkiMobile / AnkiDroid

Covered in 13 and 16, with live manual links in SOURCES.

## Releases

Release notes and known issues are **live-doc first**. Use:
- https://docs.ankiweb.net/releases/changes/changes/intro
- https://docs.ankiweb.net/releases/changes/known-issues

Do not freeze release-specific details into permanent workflow assumptions.
