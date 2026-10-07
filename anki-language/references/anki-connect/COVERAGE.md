# AnkiConnect Coverage Map

Snapshot curated: 2026-10-06.

The local catalog contains **118 documented actions** from the recent 2026 readable mirror, while preserving the distinction between the older/core **114-action baseline** and **4 newer/version-sensitive actions**. Runtime `version` + `apiReflect` remains authoritative for the user's installed add-on.

## API action coverage

| Category | Actions | Local reference |
| --- | ---: | --- |
| Card | 19 | 03-card-actions.md |
| Deck | 12 | 04-deck-actions.md |
| Graphical | 19 | 08-gui-actions.md |
| Media | 5 | 07-media-actions.md |
| Miscellaneous | 11 | 09-misc-actions.md |
| Model | 25 | 06-model-actions.md |
| Note | 20 | 05-note-actions.md |
| Statistic | 7 | 10-statistic-actions.md |
| **Total** | **118** | ACTION_CATALOG.json |

The four actions present in the recent 2026 mirror beyond the older 114-action baseline are:

- `gradeNow`
- `repositionNewCards`
- `guiAddNoteSetData`
- `guiPlayAudio`

They are marked version-sensitive in the catalog and must be checked with `apiReflect` before use.

## Per-action metadata coverage

Every catalog entry contains:

- action name;
- category;
- concise upstream-derived description;
- exact source signature from the recent mirror;
- normalized parameter names;
- risk classification;
- baseline/extended status;
- source repository;
- version-sensitivity marker;
- source anchor.

## Configuration coverage

- install/add-on code;
- health check;
- standard config JSON;
- implementation defaults;
- API key;
- bind address/port;
- CORS origins;
- ignored origins;
- logging;
- timeout/poll/backlog defaults;
- environment overrides;
- Windows/macOS notes;
- minimum Anki version observed in the recent mirror;
- localhost vs remote-security policy.

Machine-readable configuration is in `CONFIG_REFERENCE.json`.

## Protocol coverage

- POST/JSON request shape;
- API versioning;
- modern response shape;
- legacy v4 behavior;
- authentication;
- `requestPermission`;
- `version`;
- `apiReflect`;
- `multi`;
- CORS;
- network exposure;
- Anki search syntax delegation;
- source/runtime version drift.

## Workflow coverage

- inspect existing live environment;
- create/update note types;
- preflight notes;
- add one/batch notes;
- attach/store media;
- update existing notes/tags;
- query cards/reviews;
- GUI-assisted verification;
- APKG import/export;
- sync;
- read-only inspection;
- fallback to deterministic APKG generation.

## Safety coverage

- destructive note/deck/media/model operations;
- scheduling/review-history mutations;
- network/API-key/CORS exposure;
- unsupported-action hallucination;
- version drift/forks;
- backups/human verification patterns.

## Version policy

This library intentionally combines:
- a fast local snapshot;
- runtime introspection (`version`, `apiReflect`);
- an authority/source map.

Do not treat 118 as immutable across future AnkiConnect releases.
