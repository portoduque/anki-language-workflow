# 04 — Deck and Deck-Configuration Actions

Deck actions inspect/create/move/delete decks and manage deck configuration groups/presets.

Project rule: decks remain broad skill containers. Do not create micro-decks merely because the API permits it.

## Important behavior

- `createDeck` creates a deck if needed and does not replace an existing deck of the same name.
- `changeDeck` moves cards, not notes, to another deck.
- `deleteDecks` is destructive; inspect the exact targets and `cardsToo` behavior before use.
- deck-config operations can affect scheduling for many cards at once.
- `getDeckStats` is read-only and useful for inspection/reporting.

## Complete current catalog

| Action | Exact source signature | Risk | Purpose |
| --- | --- | --- | --- |
| `deckNames` | `self` | `read` | Gets the complete list of deck names for the current user. |
| `deckNamesAndIds` | `self` | `read` | Gets the complete list of deck names and their respective IDs for the current user. |
| `getDecks` | `self, cards` | `read` | Accepts an array of card IDs and returns an object with each deck name as a key, and its value an array of the given cards which belong to it. |
| `createDeck` | `self, deck` | `write` | Create a new empty deck. |
| `changeDeck` | `self, cards, deck` | `write` | Moves cards with the given IDs to a different deck, creating the deck if it doesn't exist yet. |
| `deleteDecks` | `self, decks, cardsToo=False` | `destructive` | Deletes decks with the given names. |
| `getDeckConfig` | `self, deck` | `read` | Gets the configuration group object for the given deck. |
| `saveDeckConfig` | `self, config` | `write` | Saves the given configuration group, returning `true` on success or `false` if the ID of the configuration group is invalid (such as when it does not exist). |
| `setDeckConfigId` | `self, decks, configId` | `write` | Changes the configuration group for the given decks to the one with the given ID. |
| `cloneDeckConfigId` | `self, name, cloneFrom='1'` | `write` | Creates a new configuration group with the given name, cloning from the group with the given ID, or from the default group if this is unspecified. |
| `removeDeckConfigId` | `self, configId` | `destructive` | Removes the configuration group with the given ID, returning `true` if successful, or `false` if attempting to remove either the default configuration group (ID = 1) or a configuration group that does not exist. |
| `getDeckStats` | `self, decks` | `read` | Gets statistics such as total cards and cards due for the given decks. |

Discover real deck names/IDs first instead of inventing them.
