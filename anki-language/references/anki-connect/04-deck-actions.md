# 04 — Deck and Deck-Config Actions

Deck actions inspect/create/move/delete decks and manage deck configuration groups.

For this project, decks remain broad skill containers; do not create micro-decks merely because the API permits them.

`deleteDecks` is destructive, and deck-config changes can affect many cards.

## Supported actions

| Action | Status | Main documented params | Purpose |
| --- | --- | --- | --- |
| `deckNames` | baseline | — | Gets the complete list of deck names for the current user. |
| `deckNamesAndIds` | baseline | — | Gets the complete list of deck names and their respective IDs for the current user. |
| `getDecks` | baseline | `cards` | Accepts an array of card IDs and returns an object with each deck name as a key, and its value an array of the given |
| `createDeck` | baseline | `deck` | Create a new empty deck. Will not overwrite a deck that exists with the same name. |
| `changeDeck` | baseline | `cards`, `deck` | Moves cards with the given IDs to a different deck, creating the deck if it doesn't exist yet. |
| `deleteDecks` | baseline | `decks`, `cardsToo` | Deletes decks with the given names. |
| `getDeckConfig` | baseline | `deck` | Gets the configuration group object for the given deck. |
| `saveDeckConfig` | baseline | `config` | Saves the given configuration group, returning `true` on success or `false` if the ID of the configuration group is |
| `setDeckConfigId` | baseline | `decks`, `configId` | Changes the configuration group for the given decks to the one with the given ID. Returns `true` on success or |
| `cloneDeckConfigId` | baseline | `name`, `cloneFrom` | Creates a new configuration group with the given name, cloning from the group with the given ID, or from the default |
| `removeDeckConfigId` | baseline | `configId` | Removes the configuration group with the given ID, returning `true` if successful, or `false` if attempting to |
| `getDeckStats` | baseline | `decks` | Gets statistics such as total cards and cards due for the given decks. |

## Status policy

- **baseline**: present in the baseline public standard documentation snapshot.
- **extended / verify via `apiReflect`**: present in a newer upstream-tracking mirror but absent from the baseline mirror; verify the user's installed AnkiConnect before invoking.

## Runtime verification

Before using a version-sensitive or uncertain action, call `apiReflect` against the user's installed AnkiConnect.

## Sources

- https://github.com/ankiultimate/anki-connect
- https://github.com/JSchoreels/anki-connect
