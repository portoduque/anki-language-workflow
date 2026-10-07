# 08 — Import, Export, APKG, COLPKG, CSV/TSV

## Plain-text import

Anki can import UTF-8 text files with fields separated by commas, semicolons, tabs, and other supported separators.

Important behavior:

- first non-comment row helps determine field count;
- columns can map to note fields and tags;
- HTML may be enabled during import;
- media references can be included as `[sound:file.mp3]` or `<img src="file.jpg">`;
- duplicate/update behavior is configurable;
- file headers can predefine separator, HTML mode, tags, columns, note type, deck, deck column, tags column, and GUID column.

Text import is useful when:
- users want inspectable/editable data;
- media packaging is not required;
- note types/templates already exist.

## APKG

`.apkg` is an Anki deck package.

It can include:
- notes;
- cards;
- note types/templates;
- deck/subdeck hierarchy;
- scheduling information depending on export/build choices;
- media.

This is the preferred final format for this project because the user can import one package and receive templates + media + hierarchy together.

## COLPKG

`.colpkg` is a full collection package intended for collection backup/transfer. Importing it can replace the current collection, so it is **not** the normal output for this workflow.

## Export

Anki can export:
- notes as text;
- deck packages;
- collection packages.

## Programmatic package generation

This project uses a deterministic builder rather than manually editing a user's live collection database.

Package generation must be followed by validation of:
- ZIP/package structure;
- media manifest;
- embedded collection database;
- note/card counts;
- expected deck names;
- referenced media.

## GUID/identity

For text re-import/update workflows, stable IDs in a normal field are often safer than inventing Anki-internal GUID semantics.

## Sources

- https://docs.ankiweb.net/manual/importing/intro
- https://docs.ankiweb.net/manual/importing/text-files
- https://docs.ankiweb.net/manual/importing/packaged-decks
- https://docs.ankiweb.net/manual/exporting
