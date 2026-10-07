# AnkiConnect Sources and Authority Map

Last curated: 2026-10-06.

## Authority chain

### 1. AnkiWeb add-on listing

https://ankiweb.net/shared/info/2055492159

Use for:
- installation code;
- current listing/update status;
- supported Anki version metadata;
- user-facing release information.

### 2. Original project lineage

Historical GitHub:
https://github.com/FooSoft/anki-connect

The owner archived this repository on GitHub and states that the project moved to SourceHut.

Current upstream location advertised by the archived repository:
https://git.sr.ht/~foosoft/anki-connect

If SourceHut is unavailable to the agent, do not silently replace authority with a random fork.

### 3. Public readable mirror used for API extraction

https://github.com/ankiultimate/anki-connect

This repository exposes the current-style README/API documentation and implementation files used to build the local action catalog.

Important files:
- README.md — API documentation/examples;
- plugin/config.json — normal exposed config defaults;
- plugin/util.py — runtime defaults;
- plugin/web.py — HTTP/CORS server behavior;
- plugin/__init__.py — action implementation and minimum-version checks.

### 4. Official Anki search syntax

https://docs.ankiweb.net/searching.html

AnkiConnect passes search queries into Anki. Use official Anki search documentation for query syntax.

## Runtime truth

For an installed AnkiConnect instance, runtime introspection outranks a stale local action list:

- `version`
- `apiReflect`

Use `apiReflect` to confirm actions before invoking uncertain/version-sensitive APIs.

## Source priority

When sources disagree:

1. runtime behavior of user's installed AnkiConnect (`version`, `apiReflect`);
2. current upstream/original project docs;
3. AnkiWeb add-on listing;
4. current public mirror of upstream docs/code;
5. this local summarized reference;
6. forks/community posts.

Community forks such as AnkiConnect Plus/Extended/Fixed may expose actions not present in standard AnkiConnect. Never assume fork-specific actions exist in the standard add-on.

## Web research notes

The original GitHub repo was archived in 2025 and links to SourceHut. Current AnkiWeb directory data in 2026 still lists AnkiConnect add-on code 2055492159.

For exact current compatibility after future Anki releases, verify again rather than relying on this date-stamped summary.
