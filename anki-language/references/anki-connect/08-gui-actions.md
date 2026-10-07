# 08 — GUI, Browser, and Reviewer Actions

GUI actions drive visible Anki windows and reviewer state. They are useful when human review/confirmation is desirable.

Prefer non-GUI actions for headless deterministic automation.

## Important behavior

- `guiBrowse` opens/searches Browser and returns matching card IDs.
- `guiSelectCard` selects a card in an open Browser.
- `guiSelectedNotes` reads selected note IDs.
- `guiAddCards` opens Add Cards prefilled with note data.
- `guiAddNoteSetData` is a newer action in the 2026 mirror; runtime-verify before use.
- reviewer actions show question/answer, answer the current card, and manage timer/state.
- `guiPlayAudio` is a newer action in the 2026 mirror; runtime-verify before use.
- `guiImportFile` opens Anki's import UI for human review.
- `guiCheckDatabase` returns immediately; a true return does not mean the database check found no issues.
- `guiExitAnki` is asynchronous.

## Complete current catalog

| Action | Exact source signature | Risk | Purpose |
| --- | --- | --- | --- |
| `guiBrowse` | `self, query=None, reorderCards=None` | `gui-state` | Invokes the *Card Browser* dialog and searches for a given query. |
| `guiSelectCard` | `self, card` | `gui-state` | Finds the open instance of the *Card Browser* dialog and selects a card given a card identifier. |
| `guiSelectedNotes` | `self` | `gui-state` | Finds the open instance of the *Card Browser* dialog and returns an array of identifiers of the notes that are selected. |
| `guiAddCards` | `self, note=None` | `gui-state` | Invokes the *Add Cards* dialog, presets the note using the given deck and model, with the provided field values and tags. |
| `guiEditNote` | `self, note` | `gui-state` | Opens the *Edit* dialog with a note corresponding to given note ID. |
| `guiCurrentCard` | `self` | `gui-state` | Returns information about the current card or `null` if not in review mode. |
| `guiStartCardTimer` | `self` | `gui-state` | Starts or resets the `timerStarted` value for the current card. |
| `guiShowQuestion` | `self` | `gui-state` | Shows question text for the current card; returns `true` if in review mode or `false` otherwise. |
| `guiShowAnswer` | `self` | `gui-state` | Shows answer text for the current card; returns `true` if in review mode or `false` otherwise. |
| `guiAnswerCard` | `self, ease` | `gui-state` | Answers the current card; returns `true` if succeeded or `false` otherwise. |
| `guiUndo` | `self` | `gui-state` | Undo the last action / card; returns `true` if succeeded or `false` otherwise. |
| `guiDeckOverview` | `self, name` | `gui-state` | Opens the *Deck Overview* dialog for the deck with the given name; returns `true` if succeeded or `false` otherwise. |
| `guiDeckBrowser` | `self` | `gui-state` | Opens the *Deck Browser* dialog. |
| `guiDeckReview` | `self, name` | `gui-state` | Starts review for the deck with the given name; returns `true` if succeeded or `false` otherwise. |
| `guiImportFile` | `self, path=None` | `gui-state` | Invokes the *Import... |
| `guiExitAnki` | `self` | `gui-state` | Schedules a request to gracefully close Anki. |
| `guiCheckDatabase` | `self` | `gui-state` | Requests a database check, but returns immediately without waiting for the check to complete. |
| `guiAddNoteSetData` | `self, note, append=False` | `gui-state` | Sets fields, tags, deck, and note type (model) in the *Add Note* dialog. |
| `guiPlayAudio` | `self` | `gui-state` | Plays any Audio for the current side of the current card; returns `true` if succeeded or `false` otherwise. |

GUI actions depend on current application state; failures can mean the relevant Browser/Reviewer window is not active.
