# 03 — Card Actions

Card actions operate on generated review cards and their scheduling state.

Use read-only actions for inspection. Scheduling mutations require an explicit user goal because they can change review behavior/history.

High-risk actions include `setSpecificValueOfCard`, `forgetCards`, `relearnCards`, `answerCards`, `gradeNow`, `setDueDate`, and `repositionNewCards`.

## Supported actions

| Action | Status | Main documented params | Purpose |
| --- | --- | --- | --- |
| `getEaseFactors` | baseline | `cards` | Returns an array with the ease factor for each of the given cards (in the same order). |
| `setEaseFactors` | baseline | `cards`, `easeFactors` | Sets ease factor of cards by card ID; returns `true` if successful (all cards existed) or `false` otherwise. |
| `setSpecificValueOfCard` | baseline | `card`, `keys`, `newValues` | Sets specific value of a single card. Given the risk of wreaking havor in the database when changing some of the values of a card, some of the keys require the argument "warning_check" set to True. |
| `suspend` | baseline | `cards` | Suspend cards by card ID; returns `true` if successful (at least one card wasn't already suspended) or `false` |
| `unsuspend` | baseline | `cards` | Unsuspend cards by card ID; returns `true` if successful (at least one card was previously suspended) or `false` |
| `suspended` | baseline | `card` | Check if card is suspended by its ID. Returns `true` if suspended, `false` otherwise. |
| `areSuspended` | baseline | `cards` | Returns an array indicating whether each of the given cards is suspended (in the same order). If card doesn't |
| `areDue` | baseline | `cards` | Returns an array indicating whether each of the given cards is due (in the same order). *Note*: cards in the |
| `getIntervals` | baseline | `cards` | Returns an array of the most recent intervals for each given card ID, or a 2-dimensional array of all the intervals |
| `findCards` | baseline | `query` | Returns an array of card IDs for a given query. Functionally identical to `guiBrowse` but doesn't use the GUI for |
| `cardsToNotes` | baseline | `cards` | Returns an unordered array of note IDs for the given card IDs. For cards with the same note, the ID is only given |
| `cardsModTime` | baseline | `cards` | Returns a list of objects containings for each card ID the modification time. |
| `cardsInfo` | baseline | `cards` | Returns a list of objects containing for each card ID the card fields, front and back sides including CSS, note |
| `forgetCards` | baseline | `cards` | Forget cards, making the cards new again. |
| `relearnCards` | baseline | `cards` | Make cards be "relearning". |
| `answerCards` | baseline | `answers` | Answer cards. Ease is between 1 (Again) and 4 (Easy). Will start the timer immediately before answering. Returns `true` if card exists, `false` otherwise. |
| `setDueDate` | baseline | `cards`, `days` | Set Due Date. Turns cards into review cards if they are new, and makes them due on a certain date. |
| `gradeNow` | extended / verify via `apiReflect` | `cards`, `ease` | Grades cards immediately using the same rating scale as review answers. `ease` must be between 1 (Again) and 4 (Easy). Returns `true` when the operation succeeds. |
| `repositionNewCards` | extended / verify via `apiReflect` | `orderedCardIds`, `startPosition`, `step`, `shift` | Repositions eligible new cards using Anki native reposition logic while preserving caller order. |

## Status policy

- **baseline**: present in the baseline public standard documentation snapshot.
- **extended / verify via `apiReflect`**: present in a newer upstream-tracking mirror but absent from the baseline mirror; verify the user's installed AnkiConnect before invoking.

## Runtime verification

Before using a version-sensitive or uncertain action, call `apiReflect` against the user's installed AnkiConnect.

## Sources

- https://github.com/ankiultimate/anki-connect
- https://github.com/JSchoreels/anki-connect
