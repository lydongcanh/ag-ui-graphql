# Strawberry + Agno example

End-to-end demo of the GraphQL bridge:

```
GraphQLAgent  ── graphql-ws ──▶  Strawberry  ── AgnoRunner ──▶  /agui (SSE)
  (Node)                          (FastAPI)                      (mock here)
```

The same app serves both the Strawberry subscription and a mock AG-UI SSE
endpoint, so this runs with zero external dependencies. Point `AGUI_BASE_URL`
at a real Agno `AgentOS` instance to swap in a real agent.

## Run

```bash
cd examples/strawberry-agno
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

* GraphQL playground: <http://127.0.0.1:8000/graphql>
* Subscription WebSocket: `ws://127.0.0.1:8000/graphql`
* Mock AG-UI endpoint: `POST http://127.0.0.1:8000/agui`

## Try the subscription

```graphql
subscription Run {
  runAgent(input: { threadId: "t-1", runId: "r-1" }) {
    type
    messageId
    textDelta
    payload
  }
}
```

You should see a `RUN_STARTED` -> `TEXT_MESSAGE_*` stream -> `RUN_FINISHED`.

## Node client

See [`examples/strawberry-agno-client`](../strawberry-agno-client) for a Node
script that consumes this subscription through `@ag-ui-graphql/client`.
