"""HTTP/SSE runner for AG-UI-compatible endpoints."""

from __future__ import annotations

import json
from importlib import import_module
from typing import Any, AsyncIterator, Dict, Optional

from .events import event_to_payload


class HttpAGUIRunner:
    """Proxy a GraphQL run into an AG-UI HTTP endpoint.

    This is useful for frameworks such as Agno that already expose a compliant
    ``/agui`` route. Native pause/resume adapters can be layered in later
    without changing the GraphQL event contract.
    """

    def __init__(self, url: str, *, headers: Optional[Dict[str, str]] = None) -> None:
        self.url = url
        self.headers = headers or {}

    async def run(self, run_input: Any) -> AsyncIterator[Dict[str, Any]]:
        httpx = _load_httpx()

        payload = event_to_payload(run_input) if not isinstance(run_input, dict) else run_input
        headers = {
            "Accept": "text/event-stream",
            "Content-Type": "application/json",
            **self.headers,
        }

        async with httpx.AsyncClient(timeout=None) as client:
            async with client.stream("POST", self.url, json=payload, headers=headers) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    event = _decode_sse_line(line)
                    if event is not None:
                        yield event

    async def continue_run(self, thread_id: str, run_id: str) -> AsyncIterator[Dict[str, Any]]:
        raise NotImplementedError(
            "HttpAGUIRunner cannot resume framework-native HITL yet. "
            "Use a framework-specific runner when direct continue_run support is required."
        )


def _decode_sse_line(line: str) -> Optional[Dict[str, Any]]:
    if not line.startswith("data:"):
        return None

    data = line[len("data:") :].strip()
    if not data or data == "[DONE]":
        return None

    return json.loads(data)


def _load_httpx() -> Any:
    try:
        return import_module("httpx")
    except ImportError as exc:  # pragma: no cover - depends on optional extra
        raise RuntimeError('Install "ag-ui-graphql[http]" to use HttpAGUIRunner.') from exc
