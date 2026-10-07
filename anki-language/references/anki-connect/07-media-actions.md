# 07 — Media Actions

Media actions write/read/list/delete files in the active profile's `collection.media` directory.

`storeMediaFile` supports base64 and current implementations also support path/URL inputs.

Capture the returned filename and use exact basenames in card fields.

## Supported actions

| Action | Main documented params | Purpose |
| --- | --- | --- |
| `storeMediaFile` | — | See upstream documentation. |
| `retrieveMediaFile` | — | See upstream documentation. |
| `getMediaFilesNames` | — | See upstream documentation. |
| `getMediaDirPath` | — | See upstream documentation. |
| `deleteMediaFile` | — | See upstream documentation. |

## Runtime verification

Before using a version-sensitive or uncertain action, call `apiReflect` against the user's installed AnkiConnect. The local catalog is a curated snapshot, not a substitute for runtime capability discovery.

## Source

- https://github.com/ankiultimate/anki-connect/blob/master/README.md
