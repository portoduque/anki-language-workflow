# 05 — Note and Tag Actions

Note actions are the main live-creation/update layer for this language workflow.

## Recommended creation flow

1. discover deck/model/field names;
2. build candidate note objects;
3. preflight with `canAddNotesWithErrorDetail`;
4. add with `addNote` or `addNotes`;
5. verify with `notesInfo` or a stable query/tag.

## Important behavior

- `addNote` supports fields, tags, duplicate controls, and optional audio/video/picture attachments.
- duplicate controls include `allowDuplicate`, duplicate scope, deck scope, child-deck checks, and cross-model checks.
- `addNotes` currently gathers errors and rolls back notes created by that call if any item fails; still preflight first.
- `updateNoteFields` updates existing fields and can attach media.
- `updateNote` can update fields and/or tags.
- `updateNoteModel` changes note type/model and therefore deserves extra caution.
- `deleteNotes` also removes generated cards for those notes.
- `findNotes` uses Anki's search syntax.
- tag actions operate at note level.

## Complete current catalog

| Action | Exact source signature | Risk | Purpose |
| --- | --- | --- | --- |
| `addNote` | `self, note` | `write` | Creates a note using the given deck and model, with the provided field values and tags. |
| `addNotes` | `self, notes` | `write` | Creates multiple notes using the given deck and model, with the provided field values and tags. |
| `canAddNotes` | `self, notes` | `read` | Accepts an array of objects which define parameters for candidate notes (see `addNote`) and returns an array of booleans indicating whether or not the parameters at the corresponding index could be used to create a new note. |
| `canAddNotesWithErrorDetail` | `self, notes` | `read` | Accepts an array of objects which define parameters for candidate notes (see `addNote`) and returns an array of objects with fields `canAdd` and `error`. |
| `updateNoteFields` | `self, note` | `write` | Modify the fields of an existing note. |
| `updateNote` | `self, note` | `write` | Modify the fields and/or tags of an existing note. |
| `updateNoteModel` | `self, note` | `write` | Update the model, fields, and tags of an existing note. |
| `updateNoteTags` | `self, note, tags` | `write` | Set a note's tags by note ID. |
| `getNoteTags` | `self, note` | `read` | Get a note's tags by note ID. |
| `addTags` | `self, notes, tags, add=True` | `write` | Adds tags to notes by note ID. |
| `removeTags` | `self, notes, tags` | `write` | Remove tags from notes by note ID. |
| `getTags` | `self` | `read` | Gets the complete list of tags for the current user. |
| `clearUnusedTags` | `self` | `write` | Clears all the unused tags in the notes for the current user. |
| `replaceTags` | `self, notes, tag_to_replace, replace_with_tag` | `write` | Replace tags in notes by note ID. |
| `replaceTagsInAllNotes` | `self, tag_to_replace, replace_with_tag` | `write` | Replace tags in all the notes for the current user. |
| `findNotes` | `self, query=None` | `read` | Returns an array of note IDs for a given query. |
| `notesInfo` | `self, notes=None, query=None` | `read` | Returns a list of objects containing for each note ID the note fields, tags, note type, modification time,the cards belonging to the note and the profile where the note was created. |
| `notesModTime` | `self, notes` | `read` | Returns a list of objects containings for each note ID the modification time. |
| `deleteNotes` | `self, notes` | `destructive` | Deletes notes with the given ids. |
| `removeEmptyNotes` | `self` | `destructive` | Removes all the empty notes for the current user. |

Prefer stable workflow tags/source IDs so generated notes can be found deterministically later.
