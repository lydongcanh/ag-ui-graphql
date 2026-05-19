"""FastAPI entrypoint for the Strawberry AG-UI bridge example.

Two routes are mounted on the same app for convenience:

* ``POST /agui`` - mock AG-UI SSE endpoint (stands in for a real Agno server).
* ``/graphql`` - Strawberry GraphQL endpoint, including a WebSocket subscription.

In a real deployment the AG-UI endpoint would live on a separate Agno
``AgentOS`` instance and ``AGUI_BASE_URL`` would point at it.
"""

from __future__ import annotations

from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from .mock_agui import router as mock_agui_router
from .schema import schema

app = FastAPI(title="ag-ui-graphql Strawberry example")

graphql_router: GraphQLRouter = GraphQLRouter(
    schema,
    subscription_protocols=["graphql-transport-ws", "graphql-ws"],
)

app.include_router(mock_agui_router)
app.include_router(graphql_router, prefix="/graphql")
