# 08 — GUI / Browser / Reviewer Actions

GUI actions automate visible Anki windows such as Browser, Add Cards, deck overview, and reviewer.

Use them when human review/interaction is part of the workflow. Prefer non-GUI actions for deterministic bulk/headless operations.

Reviewer actions depend on current GUI state.

## Supported actions

| Action | Status | Main documented params | Purpose |
| --- | --- | --- | --- |
| `guiBrowse` | baseline | `query`, `reorderCards` | Invokes the *Card Browser* dialog and searches for a given query. Returns an array of identifiers of the cards that |
| `guiSelectCard` | baseline | `card` | Finds the open instance of the *Card Browser* dialog and selects a card given a card identifier. |
| `guiSelectedNotes` | baseline | — | Finds the open instance of the *Card Browser* dialog and returns an array of identifiers of the notes that are |
| `guiAddCards` | baseline | `note` | Invokes the *Add Cards* dialog, presets the note using the given deck and model, with the provided field values and tags. |
| `guiEditNote` | baseline | `note` | Opens the *Edit* dialog with a note corresponding to given note ID. |
| `guiCurrentCard` | baseline | — | Returns information about the current card or `null` if not in review mode. |
| `guiStartCardTimer` | baseline | — | Starts or resets the `timerStarted` value for the current card. This is useful for deferring the start time to when |
| `guiShowQuestion` | baseline | — | Shows question text for the current card; returns `true` if in review mode or `false` otherwise. |
| `guiShowAnswer` | baseline | — | Shows answer text for the current card; returns `true` if in review mode or `false` otherwise. |
| `guiAnswerCard` | baseline | `ease` | Answers the current card; returns `true` if succeeded or `false` otherwise. Note that the answer for the current |
| `guiUndo` | baseline | — | Undo the last action / card; returns `true` if succeeded or `false` otherwise. |
| `guiDeckOverview` | baseline | `name` | Opens the *Deck Overview* dialog for the deck with the given name; returns `true` if succeeded or `false` otherwise. |
| `guiDeckBrowser` | baseline | — | Opens the *Deck Browser* dialog. |
| `guiDeckReview` | baseline | `name` | Starts review for the deck with the given name; returns `true` if succeeded or `false` otherwise. |
| `guiImportFile` | baseline | `path` | Invokes the *Import... (Ctrl+Shift+I)* dialog with an optional file path. Brings up the dialog for user to review the import. Supports all file types that Anki supports. Brings open file dialog if no path is provided. Forward slashes must be used in the path on Windows. Only supported for Anki 2.1.52+. |
| `guiExitAnki` | baseline | — | Schedules a request to gracefully close Anki. This operation is asynchronous, so it will return immediately and |
| `guiCheckDatabase` | baseline | — | Requests a database check, but returns immediately without waiting for the check to complete. Therefore, the action will always return `true` even if errors are detected during the database check. |
| `guiAddNoteSetData` | extended / verify via `apiReflect` | `note` | Sets fields, tags, deck, and note type (model) in the *Add Note* dialog. Optionally appends to fields/tags instead of replacing them. |
| `guiPlayAudio` | extended / verify via `apiReflect` | — | Plays any Audio for the current side of the current card; returns `true` if succeeded or `false` otherwise. |

## Status policy

- **baseline**: present in the baseline public standard documentation snapshot.
- **extended / verify via `apiReflect`**: present in a newer upstream-tracking mirror but absent from the baseline mirror; verify the user's installed AnkiConnect before invoking.

## Runtime verification

Before using a version-sensitive or uncertain action, call `apiReflect` against the user's installed AnkiConnect.

## Sources

- https://github.com/ankiultimate/anki-connect
- https://github.com/JSchoreels/anki-connect
