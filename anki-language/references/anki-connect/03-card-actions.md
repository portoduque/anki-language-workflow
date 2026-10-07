# 03 — Card Actions

Card actions operate on generated review cards and their scheduling state.

Use read-only actions for inspection. Scheduling mutations require an explicit user goal because they can change review behavior/history.

High-risk actions include `setSpecificValueOfCard`, `forgetCards`, `relearnCards`, `answerCards`, and `setDueDate`.

## Supported actions

| Action | Main documented params | Purpose |
| --- | --- | --- |
| `getEaseFactors` | — | See upstream documentation. |
| `setEaseFactors` | — | See upstream documentation. |
| `setSpecificValueOfCard` | — | See upstream documentation. |
| `suspend` | — | See upstream documentation. |
| `unsuspend` | — | See upstream documentation. |
| `suspended` | — | See upstream documentation. |
| `areSuspended` | — | See upstream documentation. |
| `areDue` | — | See upstream documentation. |
| `getIntervals` | — | See upstream documentation. |
| `findCards` | — | See upstream documentation. |
| `cardsToNotes` | — | See upstream documentation. |
| `cardsModTime` | — | See upstream documentation. |
| `cardsInfo` | — | See upstream documentation. |
| `forgetCards` | — | See upstream documentation. |
| `relearnCards` | — | See upstream documentation. |
| `answerCards` | — | See upstream documentation. |
| `setDueDate` | — | See upstream documentation. |

## Runtime verification

Before using a version-sensitive or uncertain action, call `apiReflect` against the user's installed AnkiConnect. The local catalog is a curated snapshot, not a substitute for runtime capability discovery.

## Source

- https://github.com/ankiultimate/anki-connect/blob/master/README.md
