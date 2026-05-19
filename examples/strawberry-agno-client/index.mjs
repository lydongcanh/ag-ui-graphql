// Subscribes to the strawberry-agno example over graphql-ws and drives a
// GraphQLAgent with the resulting envelope stream. The client never sees the
// raw AG-UI events directly — `GraphQLAgent` unwraps each envelope and feeds
// `@ag-ui/client`'s pipeline so message state, subscribers, and lifecycle
// stay owned by the official AG-UI runtime.

import { createClient } from "graphql-ws";
import WebSocket from "ws";
import { GraphQLAgent } from "@ag-ui-graphql/client";

const GRAPHQL_WS_URL = process.env.GRAPHQL_WS_URL ?? "ws://127.0.0.1:8000/graphql";

const RUN_AGENT_SUBSCRIPTION = /* GraphQL */ `
  subscription RunAgent($input: RunAgentInput!) {
    runAgent(input: $input) {
      type
      payload
      timestamp
      messageId
      toolCallId
      toolCallName
      textDelta
    }
  }
`;

const wsClient = createClient({
  url: GRAPHQL_WS_URL,
  webSocketImpl: WebSocket,
});

// Adapter: turn a graphql-ws iterable into the (input, { signal }) => stream
// shape that GraphQLAgent expects. Each yielded value is a GraphQL envelope
// whose `payload` is a canonical AG-UI event.
async function* runAgentSubscription(input, { signal }) {
  const iterator = wsClient.iterate({
    query: RUN_AGENT_SUBSCRIPTION,
    variables: {
      input: {
        threadId: input.threadId,
        runId: input.runId ?? `run-${Date.now()}`,
      },
    },
  });

  const onAbort = () => {
    iterator.return?.();
  };
  signal.addEventListener("abort", onAbort);

  try {
    for await (const result of iterator) {
      if (result.errors?.length) {
        throw new Error(`GraphQL errors: ${JSON.stringify(result.errors)}`);
      }
      if (result.data?.runAgent) {
        yield result.data.runAgent;
      }
    }
  } finally {
    signal.removeEventListener("abort", onAbort);
  }
}

const agent = new GraphQLAgent({
  threadId: "thread-strawberry-example",
  execute: runAgentSubscription,
});

agent.subscribe({
  onEvent({ event }) {
    console.log("event:", event.type);
  },
  onNewMessage({ message }) {
    console.log("message:", `${message.role}: ${message.content}`);
  },
});

try {
  const result = await agent.runAgent({ runId: "run-1" });
  console.log("\nfinal newMessages:");
  for (const message of result.newMessages) {
    console.log(`  ${message.role}: ${message.content}`);
  }
} finally {
  await wsClient.dispose();
}
