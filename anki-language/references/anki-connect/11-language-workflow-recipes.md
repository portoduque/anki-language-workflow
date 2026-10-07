# 11 — Practical Recipes for This Language Workflow

These are decision patterns, not mandatory implementation paths.

## Recipe A — Check live AnkiConnect availability

1. Call `version`.
2. Confirm response `error == null`.
3. Optionally call `apiReflect` for actions the workflow plans to use.
4. If unavailable, fall back to APKG generation rather than blocking ordinary deck creation.

## Recipe B — Inspect user's existing environment before creating live notes

Use:
- `deckNames` / `deckNamesAndIds`;
- `modelNames` / `modelNamesAndIds`;
- `modelFieldNames`;
- `modelTemplates`;
- `modelStyling`.

This prevents creating duplicate decks/note types or assuming field names.

## Recipe C — Create project note type through AnkiConnect

Typical sequence:

1. `modelNames` — determine whether note type exists.
2. If absent, `createModel`.
3. If present, inspect:
   - `modelFieldNames`;
   - `modelTemplates`;
   - `modelStyling`.
4. Update only when necessary using:
   - `updateModelTemplates`;
   - `updateModelStyling`;
   - field/template mutation actions.

For workflow-owned model names, field compatibility alone is insufficient: compare templates and CSS too. If template drift or CSS drift exists relative to the deterministic model, stop and surface the conflict rather than silently replacing the user's/customized model.

Do not overwrite user-customized models casually. Prefer a namespaced workflow-specific note type.

## Recipe D — Add one note safely

1. Resolve deck/model.
2. Build fields from approved card plan.
3. Call `canAddNotesWithErrorDetail` first when validation matters.
4. Call `addNote`.
5. Store returned note ID in logs/report when useful.

For this repository, deterministic delivery adds both the broad `anki-language` tag and a scoped identity derived from deck + target-language code + skill + stable card id. Before adding a live note, locate that identity and verify the stored note content. An identity match with different content is a conflict, not permission to skip or overwrite.

`addNote` supports optional:
- tags;
- duplicate options;
- audio;
- video;
- picture.

Media objects can supply:
- filename;
- data (base64);
- path;
- url;
- fields to attach the resulting media reference to;
- optional skipHash/deleteExisting controls where supported.

## Recipe E — Add a batch

Use `addNotes`.

Current implementation gathers errors and rolls back created notes from that call if any note errors. Still validate inputs before sending a large batch and chunk very large operations for observability.

## Recipe F — Add audio/image media separately

Use `storeMediaFile` when:
- media has already been generated/downloaded;
- you need exact filename control;
- you want to reference it manually in fields.

Then include:
- audio: `[sound:filename.mp3]`;
- image: `<img src="filename.webp">`.

Alternatively, pass media objects directly inside `addNote`/supported update actions.

## Recipe G — Update notes produced earlier

1. Locate with `findNotes` using stable tags/IDs.
2. Inspect with `notesInfo`.
3. Use:
   - `updateNoteFields`;
   - `updateNote`;
   - `updateNoteTags`;
   - tag-specific actions.

Never identify generated notes only by vague text when a stable workflow tag/ID can be used. The current scoped identity intentionally avoids treating the same local card id in another deck/language as the same note. Legacy card-id-only tags are recognized only inside the expected deck and should be verified before any future migration.

## Recipe H — Query current cards/reviews

Use:
- `findCards`;
- `cardsInfo`;
- `cardsModTime`;
- `getIntervals`;
- `getReviewsOfCards`;
- `getLatestReviewID`.

For this repository's workflow-owned cards, the deterministic read-only helper is:

`python scripts/audit_live.py --query "tag:anki-language" --output anki-audit.json`

It summarizes card fields plus review-rating history without applying a universal leech threshold and without calling mutation actions. Newly generated APKG notes receive the same broad `anki-language` ownership tag as live notes, so an imported package can enter this audit path as well.

This can support analytics/progress inspection, but the project should not change scheduling simply because the API permits it. Treat review history as evidence for inspection; inspect the actual card/source before diagnosing a cause, and require explicit user approval before any existing-card or scheduling mutation.

## Recipe I — Import/export APKG through live Anki

Use:
- `importPackage`;
- `exportPackage`.

This can bridge this repository's APKG builder into a live Anki session, but only when the user wants live import/export automation.

## Recipe J — Open UI for human review

Use GUI actions when the user should verify before committing:
- `guiAddCards`;
- `guiBrowse`;
- `guiEditNote`;
- `guiImportFile`.

Prefer UI-assisted flow for risky or ambiguous operations instead of silently mutating a collection.

## Recipe K — Sync

Use `sync` only when:
- AnkiWeb authentication is configured;
- the user wants live sync;
- no full-sync conflict requiring manual choice is expected.

Do not use sync as an automatic side effect of every card creation.

## Recipe L — Read-only inspection

AnkiConnect itself is not a read-only API. If an AI only needs information, restrict the workflow to non-mutating actions:
- version/apiReflect;
- deck/model names;
- findNotes/findCards;
- notesInfo/cardsInfo;
- stats;
- media listing/retrieval.

Do not call mutation actions without a user goal that requires them.

## Recommended architecture in this repository

Default:
`AI → card-plan.json → deterministic APKG builder`

Optional live mode:
`AI → AnkiConnect reference → inspect live collection → explicit live mutations`

APKG remains the safer portable default. AnkiConnect is an optional execution channel.
