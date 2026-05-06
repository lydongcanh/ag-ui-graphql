# @ag-ui-graphql/client

GraphQL transport adapter for the official AG-UI JavaScript client.

This package does not redefine the AG-UI protocol or reimplement client state handling. It uses `@ag-ui/client` as the runtime engine and provides a `GraphQLAgent` that turns GraphQL subscription results into canonical AG-UI events.

A2UI rendering is intentionally left out of this package for now. It should live in a separate optional package once the core GraphQL transport is stable.

## Usage

`GraphQLAgent` takes an `execute` function. That function should subscribe to
your GraphQL API and yield GraphQL event envelopes whose `payload` is a
canonical AG-UI event.

```ts
import { GraphQLAgent, type GraphQLAgentEvent } from "@ag-ui-graphql/client";

async function* runAgentSubscription(): AsyncIterable<GraphQLAgentEvent> {
  yield {
    type: "RUN_STARTED",
    payload: {
      type: "RUN_STARTED",
      threadId: "thread-1",
      runId: "run-1",
    },
  };

  yield {
    type: "TEXT_MESSAGE_START",
    payload: {
      type: "TEXT_MESSAGE_START",
      messageId: "assistant-1",
      role: "assistant",
    },
  };

  yield {
    type: "TEXT_MESSAGE_CONTENT",
    payload: {
      type: "TEXT_MESSAGE_CONTENT",
      messageId: "assistant-1",
      delta: "hello",
    },
  };

  yield {
    type: "TEXT_MESSAGE_END",
    payload: {
      type: "TEXT_MESSAGE_END",
      messageId: "assistant-1",
    },
  };

  yield {
    type: "RUN_FINISHED",
    payload: {
      type: "RUN_FINISHED",
      threadId: "thread-1",
      runId: "run-1",
    },
  };
}

const agent = new GraphQLAgent({
  threadId: "thread-1",
  execute: () => runAgentSubscription(),
});

const result = await agent.runAgent();
console.log(result.newMessages[0]?.content);
// "hello"
```

`GraphQLAgent` unwraps each envelope and passes the `payload` to
`@ag-ui/client`'s `AbstractAgent` pipeline. Message state, subscribers,
tool-call handling, and other client behavior stay owned by AG-UI.
