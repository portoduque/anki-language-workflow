# 07 — Media Actions

Media actions write/read/list/delete files in the active profile's `collection.media` directory.

`storeMediaFile` supports base64 and current implementations also support path/URL inputs.

Capture the returned filename and use exact basenames in card fields.

## Supported actions

| Action | Status | Main documented params | Purpose |
| --- | --- | --- | --- |
| `storeMediaFile` | baseline | `filename`, `data` | Stores a file with the specified base64-encoded contents inside the media folder. Alternatively you can specify a |
| `retrieveMediaFile` | baseline | `filename` | Retrieves the base64-encoded contents of the specified file, returning `false` if the file does not exist. |
| `getMediaFilesNames` | baseline | `pattern` | Gets the names of media files matched the pattern. Returning all names by default. |
| `getMediaDirPath` | baseline | — | Gets the full path to the `collection.media` folder of the currently opened profile. |
| `deleteMediaFile` | baseline | `filename` | Deletes the specified file inside the media folder. |

## Status policy

- **baseline**: present in the baseline public standard documentation snapshot.
- **extended / verify via `apiReflect`**: present in a newer upstream-tracking mirror but absent from the baseline mirror; verify the user's installed AnkiConnect before invoking.

## Runtime verification

Before using a version-sensitive or uncertain action, call `apiReflect` against the user's installed AnkiConnect.

## Sources

- https://github.com/ankiultimate/anki-connect
- https://github.com/JSchoreels/anki-connect
