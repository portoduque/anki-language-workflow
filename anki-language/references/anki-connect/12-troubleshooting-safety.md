# 12 — Troubleshooting and Safety

## Connection refused / cannot connect

Check:
1. Anki Desktop is running.
2. AnkiConnect is installed/enabled.
3. Anki was restarted after installation/update.
4. Port is correct (default 8765).
5. Bind address is correct.
6. Firewall/security software is not blocking localhost.
7. Another process is not already using the port.

Test:

`curl http://127.0.0.1:8765 -X POST -d '{"action":"version","version":6}'`

## unsupported action

Do not guess the endpoint name.

Use:

`apiReflect`

with scope `actions`, or consult `ACTION_CATALOG.json`.

This is especially important for AI agents: a plausible-sounding action may not exist.

## valid api key must be provided

The add-on's `apiKey` is configured. Include `key` in the request.

Do not print/store the key in public logs or committed config.

## CORS / origin forbidden

For browser clients:
- use `requestPermission`;
- inspect `webCorsOriginList`;
- allow the exact trusted origin;
- avoid `*`.

CLI/server-side localhost requests usually do not include browser Origin and are not blocked by browser CORS in the same way.

## AnkiConnect server fails to start

Likely causes:
- port conflict;
- invalid bind address;
- OS/firewall restrictions.

Change `webBindPort` only if the client is changed too.

## query returns nothing

Verify Anki search syntax against current manual. Quoting/escaping deck names and special characters can matter.

Use the same query in Anki Browser when possible to isolate whether the problem is the query or AnkiConnect.

## duplicate/empty note error

AnkiConnect uses Anki's note rules and duplicate logic. Check:
- first/primary field is not empty;
- note type field names match;
- duplicate policy/options;
- target deck exists where required.

Use `canAddNotesWithErrorDetail` before bulk creation.

## media missing

Check:
- returned filename from `storeMediaFile`;
- field contains exact `[sound:...]` or `<img src="...">`;
- filename collisions;
- media source URL/path is accessible;
- `skipHash` did not intentionally suppress content;
- Anki media sync has completed on other devices.

## model/template mutation breaks cards

Model actions are powerful. Before changing an existing user model:
- inspect fields/templates/styling;
- preserve user customizations;
- prefer a workflow-owned note type;
- back up collection before destructive schema changes.

## scheduling mutations

Actions such as:
- `forgetCards`;
- `relearnCards`;
- `answerCards`;
- `setDueDate`;
- `setSpecificValueOfCard`;
- `insertReviews`;

can materially alter scheduling/history.

This project's AI should not call them simply because they exist. Use them only for an explicit user goal and understand the Anki/FSRS consequences first.

## delete operations

High-risk actions include:
- `deleteNotes`;
- `deleteDecks`;
- `deleteMediaFile`;
- model field/template removals.

Require clear user intent. Prefer preview/inspection first.

## remote access security

Never recommend public exposure of port 8765 as a convenience shortcut.

If remote access is required:
- API key;
- firewall allowlist;
- secure tunnel/VPN;
- CORS restriction;
- least privilege at workflow level;
- no secrets in source control.

## Version drift

The original GitHub repository has been archived and moved by its author. Mirrors/forks can diverge.

For current behavior:
1. verify AnkiWeb listing;
2. verify current upstream/source project when accessible;
3. use runtime `version` and `apiReflect`;
4. treat local docs as a searchable reference, not an immutable truth.
