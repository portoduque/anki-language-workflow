# 02 — Notes, Fields, Note Types, and Card Types

## Use separate fields for separate data

When information has a distinct function, give it a separate field.

Examples for a language-learning note:

- target text;
- base-language meaning;
- prompt;
- focus word/chunk;
- hint;
- notes;
- IPA;
- reading/romanization when useful;
- alternate written/script form when useful;
- concise grammatical attribute when useful;
- audio;
- image;
- source/provenance.

Separate fields make it possible to:

- place audio on different card sides;
- sort/search by content;
- change templates globally;
- conditionally show information;
- preserve clean exports/imports.

Avoid stuffing translation + image + audio + explanation into one giant HTML field unless there is a deliberate reason.

## Duplicate behavior

Anki warns about duplicate values in the first field within the same note type. It does not automatically compare every field.

For programmatic workflows, stable external IDs are useful even if they are not displayed.

## Reserved/special names

Avoid field names that conflict with Anki special fields such as:

- Tags
- Type
- Deck
- Card
- FrontSide

Special fields are available in templates and should not be repurposed as normal data fields.

## Card generation

A note type may contain one or more card types. Each card has independent review history.

Anki can use conditional replacement to generate a card only when required fields are populated, and each card template can use Deck Override to route generated cards into different decks. That makes a rich-note → selective-card architecture technically possible.

### Current workflow trade-off

The current deterministic builder still creates **one Anki note per selected planned card**. This keeps APKG and AnkiConnect/live delivery simple, preserves per-card prompts/media, and matches the card-first plan contract.

Therefore:
- do not claim that cross-skill cards from the same source are native Anki siblings;
- do not create extra cards merely because another card template could exist;
- use semantic fields (`Target`, `Base`, `Reading`, `Variant`, `Grammar`, media, source, etc.) so useful linguistic data is not collapsed into a generic Front/Back blob;
- revisit grouped multi-card notes only if the learning/maintenance benefit clearly outweighs the added live-delivery/model complexity.

For this workflow:
- do not equate “possible card type” with “card that should exist”;
- do not build automatic reverse templates unless the card-selection rules require them;
- use optional structured fields without treating them as reasons to create sibling cards.

## Source

- https://docs.ankiweb.net/manual/getting-started
- https://docs.ankiweb.net/manual/editing
- https://docs.ankiweb.net/manual/templates/intro
- https://docs.ankiweb.net/manual/templates/generation
