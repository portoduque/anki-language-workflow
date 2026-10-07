# 08 — GUI / Browser / Reviewer Actions

GUI actions automate visible Anki windows such as Browser, Add Cards, deck overview, and reviewer.

Use them when human review/interaction is part of the workflow. Prefer non-GUI actions for deterministic bulk/headless operations.

Reviewer actions depend on current GUI state.

## Supported actions

| Action | Main documented params | Purpose |
| --- | --- | --- |
| `guiBrowse` | — | See upstream documentation. |
| `guiSelectCard` | — | See upstream documentation. |
| `guiSelectedNotes` | — | See upstream documentation. |
| `guiAddCards` | — | See upstream documentation. |
| `guiEditNote` | — | See upstream documentation. |
| `guiCurrentCard` | — | See upstream documentation. |
| `guiStartCardTimer` | — | See upstream documentation. |
| `guiShowQuestion` | — | See upstream documentation. |
| `guiShowAnswer` | — | See upstream documentation. |
| `guiAnswerCard` | — | See upstream documentation. |
| `guiUndo` | — | See upstream documentation. |
| `guiDeckOverview` | — | See upstream documentation. |
| `guiDeckBrowser` | — | See upstream documentation. |
| `guiDeckReview` | — | See upstream documentation. |
| `guiImportFile` | — | See upstream documentation. |
| `guiExitAnki` | — | See upstream documentation. |
| `guiCheckDatabase` | — | See upstream documentation. |

## Runtime verification

Before using a version-sensitive or uncertain action, call `apiReflect` against the user's installed AnkiConnect. The local catalog is a curated snapshot, not a substitute for runtime capability discovery.

## Source

- https://github.com/ankiultimate/anki-connect/blob/master/README.md
