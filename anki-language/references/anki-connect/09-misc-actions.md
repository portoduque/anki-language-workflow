# 09 — Miscellaneous, Profiles, Sync, Batch, and Packages

These actions handle API introspection, permissions, profiles, synchronization, batching, and APKG import/export.

`version`, `requestPermission`, and `apiReflect` are important for robust clients.

Do not make sync/profile switching/package import an automatic side effect of ordinary card generation.

## Supported actions

| Action | Main documented params | Purpose |
| --- | --- | --- |
| `requestPermission` | — | See upstream documentation. |
| `version` | — | See upstream documentation. |
| `apiReflect` | — | See upstream documentation. |
| `sync` | — | See upstream documentation. |
| `getProfiles` | — | See upstream documentation. |
| `getActiveProfile` | — | See upstream documentation. |
| `loadProfile` | — | See upstream documentation. |
| `multi` | — | See upstream documentation. |
| `exportPackage` | — | See upstream documentation. |
| `importPackage` | — | See upstream documentation. |
| `reloadCollection` | — | See upstream documentation. |

## Runtime verification

Before using a version-sensitive or uncertain action, call `apiReflect` against the user's installed AnkiConnect. The local catalog is a curated snapshot, not a substitute for runtime capability discovery.

## Source

- https://github.com/ankiultimate/anki-connect/blob/master/README.md
