"""Mock AG-UI SSE endpoint.

Stands in for a real Agno ``AgentOS`` ``/agui`` route so the example runs
without an LLM key. The bridge's ``AgnoRunner`` proxies to this endpoint just
like it would to a real one.
"""

from __future__ import annotations

import asyncio
import json
from typing import Any, AsyncIterator, Dict, List

from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse

router = APIRouter()

# Tiny canned conversation. Mirrors the shape of a real Agno text-streaming run.
_CANNED_DELTAS = ["Hello ", "from ", "Agno-over-GraphQL", "."]


@router.post("/agui")
async def mock_agui(request: Request) -> StreamingResponse:
    body = await request.json()
    thread_id = body.get("threadId", "thread-mock")
    run_id = body.get("runId", "run-mock")

    return StreamingResponse(
        _emit_run(thread_id, run_id),
        media_type="text/event-stream",
    )


async def _emit_run(thread_id: str, run_id: str) -> AsyncIterator[str]:
    """Yield SSE ``data:`` frames for a single canned AG-UI run."""

    message_id = "assistant-1"
    events: List[Dict[str, Any]] = [
        {"type": "RUN_STARTED", "threadId": thread_id, "runId": run_id},
        {"type": "TEXT_MESSAGE_START", "messageId": message_id, "role": "assistant"},
        *(
            {"type": "TEXT_MESSAGE_CONTENT", "messageId": message_id, "delta": delta}
            for delta in _CANNED_DELTAS
        ),
        {"type": "TEXT_MESSAGE_END", "messageId": message_id},
        {"type": "RUN_FINISHED", "threadId": thread_id, "runId": run_id},
    ]

    for event in events:
        yield f"data: {json.dumps(event)}\n\n"
        await asyncio.sleep(0.05)
