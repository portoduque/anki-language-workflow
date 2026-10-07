# 01 — Installation and Configuration

## What AnkiConnect is

AnkiConnect is an Anki desktop add-on that exposes a local HTTP API so external programs can inspect and modify the active Anki collection.

It is intended for **live integration with a running Anki instance**. For offline deck creation, this project's deterministic APKG builder remains the default because it is simpler and does not require Anki to be open.

## Installation

Official AnkiWeb add-on code:

`2055492159`

Typical installation:

1. Open Anki Desktop.
2. Open **Tools → Add-ons → Get Add-ons**.
3. Enter `2055492159`.
4. Install.
5. Restart Anki.

Anki must remain running for API calls to work.

Basic health check:

`curl http://127.0.0.1:8765 -X POST -d '{"action":"version","version":6}'`

Expected modern response shape:

`{"result":6,"error":null}`

## Current compatibility notes

The recent 2026 public mirror inspected by this project declares minimum Anki **23.10.0** in code. The AnkiWeb listing/add-on package can change independently, so verify the installed version when troubleshooting.

Compatibility is version-sensitive. Before diagnosing an integration problem, verify:
- Anki version;
- AnkiConnect version/listing;
- API version returned by `version` or `requestPermission`.

## Configuration location

Open:

**Tools → Add-ons → AnkiConnect → Config**

The current public config exposes:

```json
{
  "apiKey": null,
  "apiLogPath": null,
  "webBindAddress": "127.0.0.1",
  "webBindPort": 8765,
  "webCorsOriginList": ["http://localhost"],
  "ignoreOriginList": []
}
```

Additional runtime defaults present in the implementation include:

- `apiVersion: 6`
- `apiPollInterval: 25`
- `webBacklog: 5`
- `webTimeout: 10000`

These internal/default fields may not all be shown in the standard config editor. Do not invent config keys: verify current implementation before changing undocumented settings.

## Configuration fields

### apiKey

Default: `null`.

When set to a non-empty secret, API calls other than permission negotiation must include:

`"key": "<configured-secret>"`

Use an API key whenever the service is exposed beyond a strictly local/trusted environment.

### apiLogPath

Default: `null`.

When configured, AnkiConnect can log request/reply events to the specified path. Useful for debugging; avoid logging sensitive card content or API keys in shared locations.

### webBindAddress

Default: `127.0.0.1`.

This is the safest normal setting because only the local computer can connect.

Setting `0.0.0.0` exposes the server on all network interfaces. Never recommend this without a specific network requirement, authentication, firewall controls, and explicit user awareness.

The implementation also supports the environment variable:

`ANKICONNECT_BIND_ADDRESS`

### webBindPort

Default: `8765`.

Change only when:
- port 8765 is already in use;
- multiple instances/integrations require separation;
- the client is configured to use the same changed port.

### webCorsOriginList

Default includes:

`http://localhost`

Controls browser-origin access. Add only origins that should be allowed to modify the user's collection.

A wildcard `*` effectively permits all browser origins and is unsafe for normal use.

### ignoreOriginList

Origins denied through the permission dialog can be remembered here so repeated permission prompts are suppressed.

## Environment compatibility

The inspected implementation also recognizes legacy/environment-based settings such as:
- `ANKICONNECT_BIND_ADDRESS`
- `ANKICONNECT_CORS_ORIGIN`

Prefer the documented Anki add-on config unless a deployment specifically needs environment-based configuration.

## Windows

A firewall prompt may appear because Anki hosts a local HTTP server. Local use requires Anki/AnkiConnect to be allowed to listen appropriately.

## macOS

App Nap can suspend background Anki and interrupt integrations. Current upstream documentation includes commands to disable App Nap for relevant Anki/Qt application identifiers. Treat those commands as platform/version-sensitive and consult upstream docs before prescribing them verbatim.

## Project decision rule

Use AnkiConnect when the user needs **live collection operations**, such as:
- inspect existing decks/models/cards;
- update notes already in Anki;
- push generated media directly into collection.media;
- interact with the reviewer/browser;
- synchronize or manage active profiles.

Use APKG generation when the user only needs a portable deck package.

## Sources

- https://ankiweb.net/shared/info/2055492159
- https://git.sr.ht/~foosoft/anki-connect (authoritative upstream)
- https://github.com/JSchoreels/anki-connect (recent 2026 readable mirror used for current action surface)
- https://github.com/ankiultimate/anki-connect (older readable mirror used for core implementation cross-checks)
- https://github.com/FooSoft/anki-connect (archived historical repository)
