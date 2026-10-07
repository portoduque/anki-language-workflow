# 05 — Note and Tag Actions

Note actions are the primary live creation/update layer for language cards.

Inspect note-type fields before writing, preflight bulk creation when useful, and use stable workflow tags/IDs to find generated notes later.

`addNote` and `addNotes` can attach audio, video, and pictures. Deleting a note also deletes its generated cards.

## Supported actions

| Action | Main documented params | Purpose |
| --- | --- | --- |
| `addNote` | — | See upstream documentation. |
| `addNotes` | — | See upstream documentation. |
| `canAddNotes` | — | See upstream documentation. |
| `canAddNotesWithErrorDetail` | — | See upstream documentation. |
| `updateNoteFields` | — | See upstream documentation. |
| `updateNote` | — | See upstream documentation. |
| `updateNoteModel` | — | See upstream documentation. |
| `updateNoteTags` | — | See upstream documentation. |
| `getNoteTags` | — | See upstream documentation. |
| `addTags` | — | See upstream documentation. |
| `removeTags` | — | See upstream documentation. |
| `getTags` | — | See upstream documentation. |
| `clearUnusedTags` | — | See upstream documentation. |
| `replaceTags` | — | See upstream documentation. |
| `replaceTagsInAllNotes` | — | See upstream documentation. |
| `findNotes` | — | See upstream documentation. |
| `notesInfo` | — | See upstream documentation. |
| `notesModTime` | — | See upstream documentation. |
| `deleteNotes` | — | See upstream documentation. |
| `removeEmptyNotes` | — | See upstream documentation. |

## Runtime verification

Before using a version-sensitive or uncertain action, call `apiReflect` against the user's installed AnkiConnect. The local catalog is a curated snapshot, not a substitute for runtime capability discovery.

## Source

- https://github.com/ankiultimate/anki-connect/blob/master/README.md
