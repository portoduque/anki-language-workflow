# AnkiConnect Coverage Map

Snapshot basis: standard documented API version 6, curated 2026-10-06.

## API action coverage

| Category | Actions | Local reference |
| --- | ---: | --- |
| Card | 19 (17 baseline + 2 newer) | 03-card-actions.md |
| Deck | 12 | 04-deck-actions.md |
| Graphical | 19 (17 baseline + 2 newer) | 08-gui-actions.md |
| Media | 5 | 07-media-actions.md |
| Miscellaneous | 11 | 09-misc-actions.md |
| Model | 25 | 06-model-actions.md |
| Note | 20 | 05-note-actions.md |
| Statistic | 7 | 10-statistic-actions.md |
| **Baseline common snapshot** | **114** | ACTION_CATALOG.json |
| **Newer/version-sensitive additions** | **4** | ACTION_CATALOG.json |
| **Catalog total** | **118** | ACTION_CATALOG.json |

Every baseline action is represented, plus four newer actions seen in upstream-tracking mirrors: `gradeNow`, `repositionNewCards`, `guiAddNoteSetData`, and `guiPlayAudio`. These four are explicitly marked version-sensitive and must be verified with `apiReflect` on the user's installation.

## Configuration coverage

- installation/add-on code;
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
- Windows firewall/macOS background behavior;
- localhost vs remote-security policy.

Machine-readable configuration is in `CONFIG_REFERENCE.json`.

## Protocol coverage

- POST/JSON request shape;
- API versioning;
- modern response shape;
- legacy v4 behavior;
- authentication;
- requestPermission;
- version;
- apiReflect;
- multi;
- CORS;
- network exposure;
- Anki search syntax delegation.

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

This coverage is intentionally split into:
- local searchable snapshot for speed;
- runtime introspection (`version`, `apiReflect`) for installed capability truth;
- upstream/source map for current behavior.

Do not treat 114, 118, or any other count as immutable across future AnkiConnect releases. Runtime `apiReflect` is the final capability check.
