# 04 — Deck and Deck-Configuration Actions

Deck actions inspect/create/move/delete decks and manage deck configuration groups/presets.

Project rule: decks remain broad skill containers. Do not create micro-decks merely because the API permits it.

## Important behavior

- `createDeck` creates a deck if needed and does not replace an existing deck of the same name.
- `changeDeck` moves cards, not notes, to another deck.
- `deleteDecks` is destructive; inspect the exact target and `cardsToo` behavior before use.
- deck-config operations can affect scheduling for many cards at once.
- `getDeckStats` is read-only and useful for inspection/reporting.

## Current catalog

| Action | Source signature | Risk |
| --- | --- | --- |
| `deckNames` | `self` | `read` |
| `deckNamesAndIds` | `self` | `read` |
| `getDecks` | `self, cards` | `read` |
| `createDeck` | `self, deck` | `write` |
| `changeDeck` | `self, cards, deck` | `write` |
| `deleteDecks` | `self, decks, cardsToo=False` | `destructive` |
| `getDeckConfig` | `self, deck` | `read` |
| `saveDeckConfig` | `self, config` | `write` |
| `setDeckConfigId` | `self, decks, configId` | `write` |
| `cloneDeckConfigId` | `self, name, cloneFrom='1'` | `write` |
| `removeDeckConfigId` | `self, configId` | `destructive` |
| `getDeckStats` | `self, decks` | `read` |

Verify model/deck names from the live collection instead of inventing them.
