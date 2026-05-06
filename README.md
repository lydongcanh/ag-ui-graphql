# ag-ui-graphql

GraphQL transport bridge for AG-UI agent applications.

The project goal is to connect agent frameworks such as Agno to GraphQL gateways without CopilotKit. GraphQL is the outer transport; AG-UI remains the inner event model.

## Repository Layout

- `packages/core-python/` - Python bridge core published as `ag-ui-graphql`.
- `packages/client/` - TypeScript GraphQL transport adapter for the official `@ag-ui/client`.

## Design Rules

- Do not reimplement AG-UI protocol types.
- Python uses `ag-ui-protocol` / `ag_ui.core`.
- TypeScript uses `@ag-ui/client`, which re-exports the official AG-UI core types.
- This repo owns only the GraphQL bridge envelope, projections, runners, and integrations.
- Browser-side transport should leverage `@ag-ui/client`; this repo provides a GraphQL-backed adapter, not a competing client runtime.
- A2UI is intentionally out of scope for the first bridge package. It can be added later as a separate package once the GraphQL transport is stable.

## Current Milestone

- Python bridge skeleton in `packages/core-python`.
- TypeScript GraphQL agent adapter in `packages/client` kept for later client work.

The first runnable example should be a real Agno AG-UI agent exposed through a
Strawberry GraphQL subscription.

## Quick Mental Model

Backend:

```python
from ag_ui_graphql.events import event_to_graphql_event
from ag_ui_graphql.integrations.agno import AgnoRunner

runner = AgnoRunner("http://localhost:8000")

async for agui_event in runner.run(input):
    yield event_to_graphql_event(agui_event).to_graphql()
```

Frontend:

```ts
import { GraphQLAgent } from "@ag-ui-graphql/client";

const agent = new GraphQLAgent({
  threadId: "thread-1",
  execute: (input, { signal }) => subscribeToRunAgent(input, signal),
});

await agent.runAgent();
```
