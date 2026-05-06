# ag-ui-graphql

Python core package for AG-UI over GraphQL.

This package does not reimplement AG-UI. It depends on `ag-ui-protocol` and uses `ag_ui.core` as the protocol source of truth. The package owns only the GraphQL bridge layer: event projection, runner interfaces, and integration helpers.

A2UI is intentionally out of scope for this first package. It can be added later as a separate optional bridge once the core transport is stable.

## Optional integrations

```bash
pip install "ag-ui-graphql[agno]"
pip install "ag-ui-graphql[strawberry]"
```

## Usage

Project an AG-UI event into the GraphQL transport envelope:

```python
from ag_ui_graphql.events import event_to_graphql_event

graphql_event = event_to_graphql_event(
    {
        "type": "TEXT_MESSAGE_CONTENT",
        "messageId": "assistant-1",
        "delta": "hello",
    }
)

assert graphql_event.to_graphql() == {
    "type": "TEXT_MESSAGE_CONTENT",
    "payload": {
        "type": "TEXT_MESSAGE_CONTENT",
        "messageId": "assistant-1",
        "delta": "hello",
    },
    "timestamp": None,
    "messageId": "assistant-1",
    "toolCallId": None,
    "toolCallName": None,
    "textDelta": "hello",
    "hitlRequirements": [],
}
```

Proxy an existing Agno `/agui` endpoint:

```python
from ag_ui_graphql.events import event_to_graphql_event
from ag_ui_graphql.integrations.agno import AgnoRunner

runner = AgnoRunner("http://localhost:8000")


async def run_agent(input):
    async for agui_event in runner.run(input):
        yield event_to_graphql_event(agui_event).to_graphql()
```
