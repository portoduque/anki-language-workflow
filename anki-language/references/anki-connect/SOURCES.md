# AnkiConnect Sources and Authority Map

Last curated: 2026-10-06.

## Authority chain

### 1. Running AnkiConnect instance

For what the user's installed add-on actually supports, runtime discovery wins:

- `version`
- `apiReflect`

Use these before relying on a version-sensitive action.

### 2. Authoritative upstream lineage

Historical GitHub:

https://github.com/FooSoft/anki-connect

That repository was archived on 2025-11-04 and states that the project permanently moved to:

https://git.sr.ht/~foosoft/anki-connect

SourceHut is the authoritative upstream.

### 3. AnkiWeb add-on listing

Add-on code:

`2055492159`

https://ankiweb.net/shared/info/2055492159

Use it for installation/listing/support metadata.

### 4. Recent machine-readable mirror used for the 2026 catalog

https://github.com/JSchoreels/anki-connect

Inspected head:

`9c88a41c0e919fe02153dda0f0afa9a0f9cb232a`

This mirror has 2026 commits and exposes 118 documented actions, including actions not present in older 2025 mirrors:

- `gradeNow`
- `repositionNewCards`
- `guiAddNoteSetData`
- `guiPlayAudio`

Because it is a mirror/fork, do not treat it as more authoritative than the SourceHut upstream or the user's live runtime.

### 5. Older readable mirror useful for core behavior/config source

https://github.com/ankiultimate/anki-connect

Inspected historical/current-readable head:

`47da1c5039f42ad004acc57f528d6f873caffdc9`

It documents the core 114-action surface and confirms the standard config/protocol implementation.

## Official Anki dependencies

Anki search syntax used by `findCards` / `findNotes`:

https://docs.ankiweb.net/searching.html

General Anki docs index:

https://docs.ankiweb.net/llms.txt

## Runtime truth and version drift

The local `ACTION_CATALOG.json` is a dated searchable snapshot, not a claim that every installed AnkiConnect exposes all 118 actions.

For a live integration:

1. call `version`;
2. call `apiReflect` for the needed actions;
3. use the local reference to understand signatures/risk;
4. consult current upstream/mirror source for version-sensitive semantics.

## Source priority

When sources disagree:

1. live user's AnkiConnect capability/behavior;
2. SourceHut upstream;
3. AnkiWeb listing for installation/support metadata;
4. recent synchronized mirror;
5. older readable mirrors;
6. this local summary;
7. unrelated forks/community posts.

Fork-specific actions must never be assumed to exist in standard AnkiConnect.

## Licensing/copying policy

The local library stores summaries and factual API metadata. It does not vendor the upstream README wholesale. Follow source links for full upstream examples/implementation.
