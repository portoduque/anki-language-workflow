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

## Current catalog

| Action | Source signature | Risk |
| --- | --- | --- |
| `addNote` | `self, note` | `write` |
| `addNotes` | `self, notes` | `write` |
| `canAddNotes` | `self, notes` | `read` |
| `canAddNotesWithErrorDetail` | `self, notes` | `read` |
| `updateNoteFields` | `self, note` | `write` |
| `updateNote` | `self, note` | `write` |
| `updateNoteModel` | `self, note` | `write` |
| `updateNoteTags` | `self, note, tags` | `write` |
| `getNoteTags` | `self, note` | `read` |
| `addTags` | `self, notes, tags, add=True` | `write` |
| `removeTags` | `self, notes, tags` | `write` |
| `getTags` | `self` | `read` |
| `clearUnusedTags` | `self` | `write` |
| `replaceTags` | `self, notes, tag_to_replace, replace_with_tag` | `write` |
| `replaceTagsInAllNotes` | `self, tag_to_replace, replace_with_tag` | `write` |
| `findNotes` | `self, query=None` | `read` |
| `notesInfo` | `self, notes=None, query=None` | `read` |
| `notesModTime` | `self, notes` | `read` |
| `deleteNotes` | `self, notes` | `destructive` |
| `removeEmptyNotes` | `self` | `destructive` |

Prefer stable workflow tags/source IDs so generated notes can be found deterministically later.
