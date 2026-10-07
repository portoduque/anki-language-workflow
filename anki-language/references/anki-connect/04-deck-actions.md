# 04 — Deck and Deck-Config Actions

Deck actions inspect/create/move/delete decks and manage deck configuration groups.

For this project, decks remain broad skill containers; do not create micro-decks merely because the API permits them.

`deleteDecks` is destructive, and deck-config changes can affect many cards.

## Supported actions

| Action | Main documented params | Purpose |
| --- | --- | --- |
| `deckNames` | — | See upstream documentation. |
| `deckNamesAndIds` | — | See upstream documentation. |
| `getDecks` | — | See upstream documentation. |
| `createDeck` | — | See upstream documentation. |
| `changeDeck` | — | See upstream documentation. |
| `deleteDecks` | — | See upstream documentation. |
| `getDeckConfig` | — | See upstream documentation. |
| `saveDeckConfig` | — | See upstream documentation. |
| `setDeckConfigId` | — | See upstream documentation. |
| `cloneDeckConfigId` | — | See upstream documentation. |
| `removeDeckConfigId` | — | See upstream documentation. |
| `getDeckStats` | — | See upstream documentation. |

## Runtime verification

Before using a version-sensitive or uncertain action, call `apiReflect` against the user's installed AnkiConnect. The local catalog is a curated snapshot, not a substitute for runtime capability discovery.

## Source

- https://github.com/ankiultimate/anki-connect/blob/master/README.md
