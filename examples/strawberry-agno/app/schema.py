"""Strawberry schema for the AG-UI GraphQL bridge example.

The schema exposes a single ``runAgent`` subscription that proxies an AG-UI
HTTP endpoint (real Agno or the bundled mock) and projects each event into
the bridge envelope provided by ``ag_ui_graphql``.
"""

from __future__ import annotations

import os
from typing import Any, AsyncIterator, Dict, Optional

import strawberry
from strawberry.scalars import JSON

from ag_ui_graphql.events import event_to_graphql_event
from ag_ui_graphql.integrations.agno import AgnoRunner
from ag_ui_graphql.integrations.strawberry import GraphQLAgentEventType


@strawberry.input(name="RunAgentInput")
class RunAgentInput:
    """Minimal mirror of AG-UI's RunAgentInput.

    Nested fields stay as JSON to avoid reimplementing AG-UI's protocol types
    inside the GraphQL schema.
    """

    thread_id: str
    run_id: str
    messages: Optional[JSON] = None
    state: Optional[JSON] = None
    tools: Optional[JSON] = None
    context: Optional[JSON] = None
    forwarded_props: Optional[JSON] = None


@strawberry.type
class Query:
    @strawberry.field
    def health(self) -> str:
        return "ok"


@strawberry.type
class Subscription:
    @strawberry.subscription
    async def run_agent(self, input: RunAgentInput) -> AsyncIterator[GraphQLAgentEventType]:
        runner = AgnoRunner(_agui_base_url())
        async for event in runner.run(_to_agui_payload(input)):
            yield GraphQLAgentEventType.from_domain(event_to_graphql_event(event))


def _agui_base_url() -> str:
    return os.environ.get("AGUI_BASE_URL", "http://127.0.0.1:8000")


def _to_agui_payload(input: RunAgentInput) -> Dict[str, Any]:
    payload: Dict[str, Any] = {
        "threadId": input.thread_id,
        "runId": input.run_id,
    }

    optional_fields = (
        ("messages", input.messages),
        ("state", input.state),
        ("tools", input.tools),
        ("context", input.context),
        ("forwardedProps", input.forwarded_props),
    )

    for field_name, value in optional_fields:
        if value is not None:
            payload[field_name] = value

    return payload


schema = strawberry.Schema(query=Query, subscription=Subscription)
