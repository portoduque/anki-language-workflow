# 08 — GUI, Browser, and Reviewer Actions

GUI actions drive visible Anki windows and reviewer state. They are useful when human review/confirmation is desirable.

Prefer non-GUI actions for headless deterministic automation.

## Important behavior

- `guiBrowse` opens/searches Browser and returns matching card IDs.
- `guiSelectCard` selects a card in an open Browser.
- `guiSelectedNotes` reads selected note IDs.
- `guiAddCards` opens Add Cards prefilled with note data.
- `guiAddNoteSetData` is a newer action in the 2026 mirror; runtime-verify before use.
- `guiEditNote` opens the note editor.
- reviewer actions show question/answer, answer the current card, and manage timer/state.
- `guiPlayAudio` is a newer action in the 2026 mirror.
- `guiImportFile` opens Anki's import UI for human review.
- `guiCheckDatabase` returns immediately; a true return does not mean the database check found no issues.
- `guiExitAnki` is asynchronous.

## Current catalog

| Action | Source signature | Risk |
| --- | --- | --- |
| `guiBrowse` | `self, query=None, reorderCards=None` | `gui-state` |
| `guiSelectCard` | `self, card` | `gui-state` |
| `guiSelectedNotes` | `self` | `gui-state` |
| `guiAddCards` | `self, note=None` | `gui-state` |
| `guiEditNote` | `self, note` | `gui-state` |
| `guiAddNoteSetData` | `self, note, append=False` | `gui-state` |
| `guiCurrentCard` | `self` | `gui-state` |
| `guiStartCardTimer` | `self` | `gui-state` |
| `guiShowQuestion` | `self` | `gui-state` |
| `guiShowAnswer` | `self` | `gui-state` |
| `guiAnswerCard` | `self, ease` | `gui-state` |
| `guiUndo` | `self` | `gui-state` |
| `guiDeckOverview` | `self, name` | `gui-state` |
| `guiDeckBrowser` | `self` | `gui-state` |
| `guiDeckReview` | `self, name` | `gui-state` |
| `guiImportFile` | `self, path=None` | `gui-state` |
| `guiExitAnki` | `self` | `gui-state` |
| `guiCheckDatabase` | `self` | `gui-state` |
| `guiPlayAudio` | `self` | `gui-state` |

GUI actions depend on current application state; failures can mean the relevant Browser/Reviewer window is not active.
