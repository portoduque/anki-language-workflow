# 07 — Media Actions

Media actions manipulate files in the active profile's `collection.media` folder.

## `storeMediaFile`

Current implementations accept:
- base64 `data`;
- absolute/local `path`;
- remote `url`.

The current source signature also includes optional `skipHash` and `deleteExisting`.

Priority when multiple sources are supplied is implementation-defined/documented; use one source per request for clarity.

Capture the filename returned by AnkiConnect and reference that exact basename.

Prefix files with underscore only for special/template/config media that should be protected from unused-media cleanup; do not do this for ordinary card audio/images.

## Note-embedded media

`addNote` / `addNotes` can also accept `audio`, `video`, and `picture` objects with:
- filename;
- one source (`data`, `path`, or `url`);
- destination `fields`;
- optional `skipHash`.

Media rights/provenance rules from this project still apply.

## Current catalog

| Action | Source signature | Risk |
| --- | --- | --- |
| `storeMediaFile` | `self, filename, data=None, path=None, url=None, skipHash=None, deleteExisting=True` | `write` |
| `retrieveMediaFile` | `self, filename` | `read` |
| `getMediaFilesNames` | `self, pattern='*'` | `read` |
| `getMediaDirPath` | `self` | `read` |
| `deleteMediaFile` | `self, filename` | `destructive` |

`deleteMediaFile` is destructive; confirm references before deleting.
