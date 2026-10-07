# 01 — Core Model and Organization

## Mental model

Anki separates **content** from **review instances**.

- **Note:** a record containing related information.
- **Field:** one piece of information inside a note.
- **Note type:** schema that defines fields and card-generation rules.
- **Card type/template:** blueprint that generates a review card from note fields.
- **Card:** one question/answer review item with its own scheduling history.
- **Sibling cards:** cards generated from the same note.
- **Deck:** container a card belongs to for study/scheduling organization.
- **Tag:** note-level label for flexible classification.
- **Collection:** the complete Anki database, including notes, cards, decks, note types, scheduling data, and configuration.

One note can create multiple cards, and those sibling cards are scheduled independently. This is technically useful for recognition vs production, but the project must create multiple cards only when the pedagogical benefit justifies the added review cost.

## Built-in note types

Modern Anki includes:

- **Basic** — one Front → Back card.
- **Basic (and reversed card)** — automatically creates forward and reverse cards.
- **Basic (optional reversed card)** — reverse card only when the extra field is populated.
- **Basic (type in the answer)** — provides a typed-answer comparison.
- **Cloze** — creates cards by hiding marked text.
- **Image Occlusion** — native in Anki 23.10+, creates cloze-like cards from masked image regions.

For this project, built-in note types are reference points, not mandatory choices. Custom note types/templates are preferred when they better match the workflow.

## Deck hierarchy

Subdecks are represented with double colons:

`Parent::Child`

Anki's own manual recommends decks for broad categories and tags/fields for finer classification. This aligns with this project:

- deck = trained skill;
- tag = linguistic/content dimension.

## Important independence

Note types and decks are independent. A single note type can generate cards into decks, and a deck can contain cards from different note types.

## Sources

- https://docs.ankiweb.net/manual/getting-started
- https://docs.ankiweb.net/manual/editing
