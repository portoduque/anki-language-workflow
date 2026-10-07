# 05 — Note and Tag Actions

Note actions are the primary live creation/update layer for language cards.

Inspect note-type fields before writing, preflight bulk creation when useful, and use stable workflow tags/IDs to find generated notes later.

`addNote` and `addNotes` can attach audio, video, and pictures. Deleting a note also deletes its generated cards.

## Supported actions

| Action | Status | Main documented params | Purpose |
| --- | --- | --- | --- |
| `addNote` | baseline | `note` | Creates a note using the given deck and model, with the provided field values and tags. Returns the identifier of |
| `addNotes` | baseline | `notes` | Creates multiple notes using the given deck and model, with the provided field values and tags. Returns an array of |
| `canAddNotes` | baseline | `notes` | Accepts an array of objects which define parameters for candidate notes (see `addNote`) and returns an array of |
| `canAddNotesWithErrorDetail` | baseline | `notes` | Accepts an array of objects which define parameters for candidate notes (see `addNote`) and returns an array of |
| `updateNoteFields` | baseline | `note` | Modify the fields of an existing note. You can also include audio, video, or picture files which will be added to the note with an |
| `updateNote` | baseline | `note` | Modify the fields and/or tags of an existing note. |
| `updateNoteModel` | baseline | `note` | Update the model, fields, and tags of an existing note. |
| `updateNoteTags` | baseline | `note`, `tags` | Set a note's tags by note ID. Old tags will be removed. |
| `getNoteTags` | baseline | `note` | Get a note's tags by note ID. |
| `addTags` | baseline | `notes`, `tags` | Adds tags to notes by note ID. |
| `removeTags` | baseline | `notes`, `tags` | Remove tags from notes by note ID. |
| `getTags` | baseline | — | Gets the complete list of tags for the current user. |
| `clearUnusedTags` | baseline | — | Clears all the unused tags in the notes for the current user. |
| `replaceTags` | baseline | `notes`, `tag_to_replace`, `replace_with_tag` | Replace tags in notes by note ID. |
| `replaceTagsInAllNotes` | baseline | `tag_to_replace`, `replace_with_tag` | Replace tags in all the notes for the current user. |
| `findNotes` | baseline | `query` | Returns an array of note IDs for a given query. Query syntax is [documented here](https://docs.ankiweb.net/searching.html). |
| `notesInfo` | baseline | `notes` | Returns a list of objects containing for each note ID the note fields, tags, note type, modification time,the cards belonging to |
| `notesModTime` | baseline | `notes` | Returns a list of objects containings for each note ID the modification time. |
| `deleteNotes` | baseline | `notes` | Deletes notes with the given ids. If a note has several cards associated with it, all associated cards will be deleted. |
| `removeEmptyNotes` | baseline | — | Removes all the empty notes for the current user. |

## Status policy

- **baseline**: present in the baseline public standard documentation snapshot.
- **extended / verify via `apiReflect`**: present in a newer upstream-tracking mirror but absent from the baseline mirror; verify the user's installed AnkiConnect before invoking.

## Runtime verification

Before using a version-sensitive or uncertain action, call `apiReflect` against the user's installed AnkiConnect.

## Sources

- https://github.com/ankiultimate/anki-connect
- https://github.com/JSchoreels/anki-connect
