# 09 — Miscellaneous, Profiles, Sync, Batch, and Packages

These actions handle API introspection, permissions, profiles, synchronization, batching, and APKG import/export.

`version`, `requestPermission`, and `apiReflect` are important for robust clients.

Do not make sync/profile switching/package import an automatic side effect of ordinary card generation.

## Supported actions

| Action | Status | Main documented params | Purpose |
| --- | --- | --- | --- |
| `requestPermission` | baseline | — | Requests permission to use the API exposed by this plugin. This method does not require the API key, and is the |
| `version` | baseline | — | Gets the version of the API exposed by this plugin. Currently versions `1` through `6` are defined. |
| `apiReflect` | baseline | `scopes`, `actions` | Gets information about the AnkiConnect APIs available. The request supports the following params: |
| `sync` | baseline | — | Synchronizes the local Anki collections with AnkiWeb. |
| `getProfiles` | baseline | — | Retrieve the list of profiles. |
| `getActiveProfile` | baseline | — | Retrieve the active profile. |
| `loadProfile` | baseline | `name` | Selects the profile specified in request. |
| `multi` | baseline | `actions` | Performs multiple actions in one request, returning an array with the response of each action (in the given order). |
| `exportPackage` | baseline | `deck`, `path`, `includeSched` | Exports a given deck in `.apkg` format. Returns `true` if successful or `false` otherwise. The optional property |
| `importPackage` | baseline | `path` | Imports a file in `.apkg` format into the collection. Returns `true` if successful or `false` otherwise. |
| `reloadCollection` | baseline | — | Tells anki to reload all data from the database. |

## Status policy

- **baseline**: present in the baseline public standard documentation snapshot.
- **extended / verify via `apiReflect`**: present in a newer upstream-tracking mirror but absent from the baseline mirror; verify the user's installed AnkiConnect before invoking.

## Runtime verification

Before using a version-sensitive or uncertain action, call `apiReflect` against the user's installed AnkiConnect.

## Sources

- https://github.com/ankiultimate/anki-connect
- https://github.com/JSchoreels/anki-connect
