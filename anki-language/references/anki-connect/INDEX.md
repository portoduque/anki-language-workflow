# AnkiConnect Reference Library

This directory is the technical reference for **live Anki automation through AnkiConnect**.

Do not load it during normal card pedagogy or ordinary APKG generation.

## When the AI should consult this library

Consult when the user wants to:
- read or modify an existing live Anki collection;
- push cards/notes directly into open Anki;
- inspect decks, note types, templates, tags, cards, or review history;
- upload/retrieve media through Anki;
- import/export packages through running Anki;
- control Browser/Reviewer GUI;
- sync or switch profiles;
- configure or troubleshoot AnkiConnect;
- build an integration using its HTTP API.

Do not consult it just to decide whether a sentence deserves a Listening/Production card.

## Fast routing

When scripts can run:

`python scripts/find_ankiconnect_reference.py "<goal or action>"`

Examples:

- `python scripts/find_ankiconnect_reference.py "install api key cors"`
- `python scripts/find_ankiconnect_reference.py "addNote audio picture duplicate"`
- `python scripts/find_ankiconnect_reference.py "create model template css"`
- `python scripts/find_ankiconnect_reference.py "find notes update tags"`
- `python scripts/find_ankiconnect_reference.py "review history stats"`

For an exact action name, the router checks `ACTION_CATALOG.json`.

## Reference map

| Need | Read |
| --- | --- |
| Install/configure AnkiConnect | [01-installation-configuration.md](01-installation-configuration.md) |
| HTTP request/response, versions, auth, CORS, permissions | [02-protocol-auth-security.md](02-protocol-auth-security.md) |
| Cards/scheduling actions | [03-card-actions.md](03-card-actions.md) |
| Deck/config actions | [04-deck-actions.md](04-deck-actions.md) |
| Notes/tags actions | [05-note-actions.md](05-note-actions.md) |
| Models/fields/templates/CSS actions | [06-model-actions.md](06-model-actions.md) |
| Media actions | [07-media-actions.md](07-media-actions.md) |
| GUI/reviewer/browser actions | [08-gui-actions.md](08-gui-actions.md) |
| Version/profiles/sync/multi/APKG actions | [09-misc-actions.md](09-misc-actions.md) |
| Stats/review-history actions | [10-statistic-actions.md](10-statistic-actions.md) |
| Language-workflow integration recipes | [11-language-workflow-recipes.md](11-language-workflow-recipes.md) |
| Troubleshooting/security/destructive operations | [12-troubleshooting-safety.md](12-troubleshooting-safety.md) |
| Concrete JSON payload examples | [13-request-examples.md](13-request-examples.md) |
| All 114 documented actions machine-readable | [ACTION_CATALOG.json](ACTION_CATALOG.json) |
| Configuration defaults machine-readable | [CONFIG_REFERENCE.json](CONFIG_REFERENCE.json) |
| Coverage/audit map | [COVERAGE.md](COVERAGE.md) |
| Source authority/currentness | [SOURCES.md](SOURCES.md) |

## Important project policy

AnkiConnect is **optional**.

Default deck delivery remains:

`card-plan.json → validated APKG`

Use AnkiConnect only when live collection integration adds real value.

Before invoking an uncertain action, prefer runtime discovery with `apiReflect`. Never hallucinate plausible action names.
