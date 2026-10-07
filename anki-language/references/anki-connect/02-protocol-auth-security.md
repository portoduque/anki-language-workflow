# 02 — HTTP Protocol, API Versions, Authentication, CORS, and Permissions

## Endpoint

Default endpoint:

`http://127.0.0.1:8765`

Requests are HTTP POST with JSON bodies.

## Request shape

Modern request:

```json
{
  "action": "deckNames",
  "version": 6,
  "params": {}
}
```

If API-key authentication is enabled:

```json
{
  "action": "deckNames",
  "version": 6,
  "params": {},
  "key": "YOUR_SECRET"
}
```

`params` may be omitted for actions that take no parameters.

## Response shape

For API versions above 4:

```json
{
  "result": "...",
  "error": null
}
```

On failure:

```json
{
  "result": null,
  "error": "description"
}
```

Always inspect `error`; HTTP 200 does not imply the Anki action succeeded.

If no request `version` is supplied, AnkiConnect defaults to API version 4 for backward compatibility. Version <=4 responses use the older bare-result behavior. New integrations should explicitly send version 6.

## Discovery/bootstrap calls

### requestPermission

Use early for browser/web-origin integrations.

It:
- can be called without API key;
- can be called from an untrusted origin;
- may trigger a user permission dialog;
- reports whether permission is granted;
- reports whether an API key is required;
- reports API version when granted.

This is the preferred bootstrap for browser-origin clients.

**Version-sensitive field-name caveat:** current inspected source returns `requireApikey`, while older README wording uses `requireApiKey`. Treat the actual response as authoritative rather than hardcoding the documentation spelling.

### version

Returns the exposed API version.

### apiReflect

Can query available actions at runtime. This is valuable for AI/automation clients because it prevents hallucinating unsupported actions.

Recommended pattern:
1. call `version`;
2. call `apiReflect` for required actions;
3. use only confirmed actions.

This project explicitly warns against inventing actions such as `createFilteredDeck` when they are not in the reflected/current action list.

## multi

`multi` sends several AnkiConnect actions in one HTTP request and returns results in order.

Use it to reduce HTTP overhead for independent operations.

Do not assume transactional semantics across all nested actions. For operations that must be atomic, verify the specific action's behavior. For example, current `addNotes` implementation intentionally rolls back notes created in that call when one note fails.

## CORS/origin behavior

AnkiConnect checks browser `Origin` against `webCorsOriginList`.

- localhost is trusted by default;
- extension origins may receive special localhost treatment;
- untrusted origins can use `requestPermission`;
- wildcard origins should be avoided.

CORS is a browser security boundary. It does not replace API-key authentication when the server is network-accessible.

## Network exposure

Default localhost binding should be preserved unless remote access is truly required.

If binding to LAN/all interfaces:
- enable `apiKey`;
- restrict firewall ingress;
- restrict CORS origins;
- do not expose port 8765 directly to the public internet;
- prefer a secured local tunnel/VPN/reverse proxy only when necessary.

AnkiConnect can perform destructive actions, including deleting notes/decks and modifying scheduling data.

## Minimal client helper pattern

Python pseudocode:

```python
def invoke(action, params=None):
    payload = {
        "action": action,
        "version": 6,
        "params": params or {}
    }
    # add key when configured
    # POST to http://127.0.0.1:8765
    # parse JSON
    # raise if response["error"] is not None
    # return response["result"]
```

## Search queries

Actions such as `findNotes` and `findCards` use Anki's own search syntax. Consult current Anki Searching documentation instead of inventing query syntax.

## Sources

- https://github.com/ankiultimate/anki-connect
- https://docs.ankiweb.net/searching.html
