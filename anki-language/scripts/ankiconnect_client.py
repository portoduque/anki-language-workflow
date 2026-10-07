#!/usr/bin/env python3
from __future__ import annotations

import json
import urllib.request
from typing import Any


class AnkiConnectError(RuntimeError):
    pass


class AnkiConnectClient:
    def __init__(self, endpoint: str = "http://127.0.0.1:8765", api_key: str | None = None, timeout: int = 30):
        self.endpoint = endpoint.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout

    def invoke(self, action: str, params: dict[str, Any] | None = None) -> Any:
        payload: dict[str, Any] = {"action": action, "version": 6}
        if params:
            payload["params"] = params
        if self.api_key:
            payload["key"] = self.api_key
        request = urllib.request.Request(
            self.endpoint,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                body = json.load(response)
        except Exception as exc:
            raise AnkiConnectError(f"Unable to reach AnkiConnect at {self.endpoint}: {exc}") from exc

        if not isinstance(body, dict) or "error" not in body or "result" not in body:
            raise AnkiConnectError(f"Unexpected AnkiConnect response for {action}: {body!r}")
        if body["error"] is not None:
            raise AnkiConnectError(f"{action}: {body['error']}")
        return body["result"]

    def verify_actions(self, required: set[str]) -> dict[str, Any]:
        version = self.invoke("version")
        reflected = self.invoke("apiReflect", {"scopes": ["actions"], "actions": sorted(required)})
        available = set(reflected.get("actions", [])) if isinstance(reflected, dict) else set()
        missing = sorted(required - available)
        if missing:
            raise AnkiConnectError(f"Installed AnkiConnect does not expose required actions: {missing}")
        return {"api_version": version, "actions": sorted(available)}
