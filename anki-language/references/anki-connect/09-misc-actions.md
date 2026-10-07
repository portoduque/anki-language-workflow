# 09 — Miscellaneous: Capability Discovery, Profiles, Sync, Batching, APKG

These actions cover API discovery, profiles, sync, batching, import/export, and collection reload.

## Bootstrap actions

- `version`: returns exposed API version.
- `apiReflect`: runtime reflection for supported action names.
- `requestPermission`: browser-origin permission bootstrap; may prompt the user and is exempt from normal API-key checking.

## Profiles

`getProfiles`, `getActiveProfile`, and `loadProfile` control which profile/collection is targeted.

## `multi`

Batches independent API calls into one HTTP request. Do not assume transaction semantics across arbitrary nested actions.

## Sync

`sync` requires configured AnkiWeb authentication. If Anki reports a full-sync-required state, do not guess which direction should win.

## Package actions

- `exportPackage(deck, path, includeSched=False)`
- `importPackage(path)`

Useful for bridging live Anki with the project's APKG workflow.

## Complete current catalog

| Action | Exact source signature | Risk | Purpose |
| --- | --- | --- | --- |
| `requestPermission` | `self, origin, allowed` | `read` | Requests permission to use the API exposed by this plugin. |
| `version` | `self` | `read` | Gets the version of the API exposed by this plugin. |
| `apiReflect` | `self, scopes=None, actions=None` | `read` | Gets information about the AnkiConnect APIs available. |
| `sync` | `self` | `write` | Synchronizes the local Anki collections with AnkiWeb. |
| `getProfiles` | `self` | `read` | Retrieve the list of profiles. |
| `getActiveProfile` | `self` | `read` | Retrieve the active profile. |
| `loadProfile` | `self, name` | `write` | Selects the profile specified in request. |
| `multi` | `self, actions` | `mixed` | Performs multiple actions in one request, returning an array with the response of each action (in the given order). |
| `exportPackage` | `self, deck, path, includeSched=False` | `read-export` | Exports a given deck in `.apkg` format. |
| `importPackage` | `self, path` | `destructive` | Imports a file in `.apkg` format into the collection. |
| `reloadCollection` | `self` | `write` | Tells anki to reload all data from the database. |
