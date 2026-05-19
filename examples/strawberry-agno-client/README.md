# Strawberry + Agno client

Node script that subscribes to the [`strawberry-agno`](../strawberry-agno)
GraphQL endpoint and drives a `GraphQLAgent` with the resulting envelope
stream.

## Run

In one terminal, start the backend:

```bash
cd examples/strawberry-agno
source .venv/bin/activate
uvicorn app.main:app --reload
```

In another terminal, run the client:

```bash
pnpm install
pnpm --filter @ag-ui-graphql/example-strawberry-agno-client start
```

Expected output:

```
event: RUN_STARTED
event: TEXT_MESSAGE_START
event: TEXT_MESSAGE_CONTENT
event: TEXT_MESSAGE_CONTENT
event: TEXT_MESSAGE_CONTENT
event: TEXT_MESSAGE_CONTENT
event: TEXT_MESSAGE_END
message: assistant: Hello from Agno-over-GraphQL.
event: RUN_FINISHED

final newMessages:
  assistant: Hello from Agno-over-GraphQL.
```

Set `GRAPHQL_WS_URL` to point at a different server (e.g. a real Strawberry
gateway in front of Agno).
