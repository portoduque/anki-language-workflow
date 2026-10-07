# 07 — Media Actions

Media actions manipulate files in the active profile's `collection.media` folder.

## `storeMediaFile`

The recent 2026 source signature is:

`storeMediaFile(self, filename, data=None, path=None, url=None, skipHash=None, deleteExisting=True)`

Supported source forms include:
- base64 `data`;
- local/absolute `path`;
- remote `url`.

If several are supplied, upstream documentation states the preference order is data → path → URL. For clarity, supply only one source.

Capture the filename returned by AnkiConnect and reference that exact basename.

Use underscore-prefixed filenames only for special/template/config media that should survive unused-media cleanup; ordinary card media should normally not be underscored.

## Note-embedded media

`addNote` / `addNotes` can also accept `audio`, `video`, and `picture` entries with filename, source, destination fields, and optional hash controls.

Media rights/provenance rules from this project still apply.

## Complete current catalog

| Action | Exact source signature | Risk | Purpose |
| --- | --- | --- | --- |
| `storeMediaFile` | `self, filename, data=None, path=None, url=None, skipHash=None, deleteExisting=True` | `write` | Stores a file with the specified base64-encoded contents inside the media folder. |
| `retrieveMediaFile` | `self, filename` | `read` | Retrieves the base64-encoded contents of the specified file, returning `false` if the file does not exist. |
| `getMediaFilesNames` | `self, pattern='*'` | `read` | Gets the names of media files matched the pattern. |
| `getMediaDirPath` | `self` | `read` | Gets the full path to the `collection.media` folder of the currently opened profile. |
| `deleteMediaFile` | `self, filename` | `destructive` | Deletes the specified file inside the media folder. |

`deleteMediaFile` is destructive; confirm references before deleting.
