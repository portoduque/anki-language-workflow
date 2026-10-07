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

For this workflow:
- do not equate “possible card type” with “card that should exist”;
- do not build automatic reverse templates unless the card-selection rules require them;
- keep note fields rich enough that a single source unit can selectively generate different skill cards.

## Source

- https://docs.ankiweb.net/manual/getting-started
- https://docs.ankiweb.net/manual/editing
- https://docs.ankiweb.net/manual/templates/intro
