# 12 — Automation, Add-on Development, and APIs

## Preferred automation layers

Choose the least invasive layer that solves the problem.

### 1. APKG generation

Best when the goal is to create an importable deck without touching a user's live collection.

Advantages:
- deterministic;
- portable;
- testable;
- Anki does not need to be running;
- easy to validate before delivery.

This is the default architecture of this project.

### 2. Text import (CSV/TSV)

Best for simple bulk imports when note types/templates already exist.

### 3. AnkiConnect

Best when an external application must interact with a running Anki collection.

Typical capabilities include:
- query/find notes/cards;
- add notes;
- update fields/tags;
- manage decks;
- add media;
- inspect models/note types.

AnkiConnect exposes a local HTTP API. Keep it localhost-only unless there is a deliberate secured networking requirement.

### 4. MCP integration

Useful when an AI assistant should interact with a live Anki collection through Model Context Protocol.

A current community project, Anki MCP Server, can bridge MCP clients to Anki and commonly relies on AnkiConnect for live collection operations. An add-on variant also exists.

Use MCP only when live collection access is actually needed. APKG generation remains simpler, safer, and more portable for offline deck creation.

Security rules:
- prefer local/STDIO/localhost modes when possible;
- treat remote tunnels/public endpoints as sensitive collection access;
- use read-only modes when the AI only needs inspection;
- verify current project docs because MCP transport/auth behavior is version-sensitive.

Sources:
- https://github.com/ankimcp/anki-mcp-server
- https://github.com/ankimcp/anki-mcp-server-addon

### 5. Native add-on

Best when functionality must run inside Anki UI/reviewer/browser or use native hooks.

## Official add-on development docs

The official documentation covers:

- basic add-on structure;
- add-on folders;
- the `anki` module;
- hooks and filters;
- background operations;
- Qt/PyQt UI;
- Python modules;
- add-on configuration;
- reviewer JavaScript;
- debugging;
- sharing/publishing;
- generated hooks reference;
- porting older add-ons.

Discovery index:
- https://docs.ankiweb.net/llms.txt

Add-on docs root:
- https://docs.ankiweb.net/addons/intro

## Hooks over monkey patching

Prefer official hooks/filters when available. Monkey patching internal methods is more fragile across Anki releases.

## Background operations

Long-running work should not block Anki's UI thread. Follow current official background-operation guidance when writing add-ons.

## Python/Rust/core APIs

Anki publishes developer documentation for Python and Rust APIs and internal architecture. These APIs can change and are more appropriate for add-ons/core development than for a simple deck-generation workflow.

Developer index:
- https://docs.ankiweb.net/llms.txt
- https://docs.ankiweb.net/developers/api-python
- https://docs.ankiweb.net/developers/api-rust
- https://docs.ankiweb.net/developers/architecture

## Internal SQLite database

Anki uses SQLite, and the manual documents some tables for statistics. Direct database writes are **not** the preferred automation interface for this project.

Reasons:
- schema/internal invariants can change;
- sync metadata can be damaged;
- media/note/card relationships are easy to corrupt.

Reading a generated APKG's SQLite database for validation is acceptable; mutating a user's live collection database is not the normal workflow.

## AnkiConnect security

AnkiConnect normally binds locally. If someone changes it to bind all network interfaces, the API may become reachable from other machines. Do not recommend that casually.

## Sources

- https://docs.ankiweb.net/addons/intro
- https://docs.ankiweb.net/addons/hooks-and-filters
- https://docs.ankiweb.net/addons/background-ops
- https://docs.ankiweb.net/developers/api-python
- https://github.com/ankiultimate/anki-connect
