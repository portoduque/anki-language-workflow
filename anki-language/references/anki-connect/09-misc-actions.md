# 09 — Miscellaneous: Capability Discovery, Profiles, Sync, Batching, APKG

These actions cover API discovery, profiles, sync, batching, import/export, and collection reload.

## Bootstrap actions

### `version`
Returns API version. Use early.

### `apiReflect`
Runtime reflection for supported action names. Use it before uncertain/version-sensitive calls.

### `requestPermission`
Browser-origin permission bootstrap. May prompt the user and can be called without API key.

## Profiles

- `getProfiles`
- `getActiveProfile`
- `loadProfile`

Changing profile changes which collection is targeted and may involve GUI/sync transitions.

## `multi`

Batches independent API calls into one HTTP request.

Do not assume transaction semantics across arbitrary nested actions.

## Sync

`sync` requires configured AnkiWeb authentication. If Anki reports a full-sync-required state, do not guess which direction should win.

## Package actions

- `exportPackage(deck, path, includeSched=False)`
- `importPackage(path)`

Useful for bridging live Anki with the project's APKG workflow.

## Current catalog

| Action | Source signature | Risk |
| --- | --- | --- |
| `requestPermission` | `self, origin, allowed` | `read` |
| `version` | `self` | `read` |
| `apiReflect` | `self, scopes=None, actions=None` | `read` |
| `sync` | `self` | `write` |
| `getProfiles` | `self` | `read` |
| `getActiveProfile` | `self` | `read` |
| `loadProfile` | `self, name` | `write` |
| `multi` | `self, actions` | `mixed` |
| `exportPackage` | `self, deck, path, includeSched=False` | `read-export` |
| `importPackage` | `self, path` | `destructive` |
| `reloadCollection` | `self` | `write` |
