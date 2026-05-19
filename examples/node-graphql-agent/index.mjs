import { GraphQLAgent } from "@ag-ui-graphql/client";

async function* fakeGraphQLSubscription(input, { signal }) {
  const threadId = input.threadId;
  const runId = input.runId ?? "run-example";

  const events = [
    {
      type: "RUN_STARTED",
      payload: {
        type: "RUN_STARTED",
        threadId,
        runId,
      },
    },
    {
      type: "TEXT_MESSAGE_START",
      payload: {
        type: "TEXT_MESSAGE_START",
        messageId: "assistant-1",
        role: "assistant",
      },
    },
    {
      type: "TEXT_MESSAGE_CONTENT",
      payload: {
        type: "TEXT_MESSAGE_CONTENT",
        messageId: "assistant-1",
        delta: "Hello from GraphQLAgent.",
      },
    },
    {
      type: "TEXT_MESSAGE_END",
      payload: {
        type: "TEXT_MESSAGE_END",
        messageId: "assistant-1",
      },
    },
    {
      type: "RUN_FINISHED",
      payload: {
        type: "RUN_FINISHED",
        threadId,
        runId,
      },
    },
  ];

  for (const event of events) {
    if (signal.aborted) {
      return;
    }

    yield event;
  }
}

const agent = new GraphQLAgent({
  threadId: "thread-example",
  execute: fakeGraphQLSubscription,
});

agent.subscribe({
  onEvent({ event }) {
    console.log("event:", event.type);
  },
  onNewMessage({ message }) {
    console.log("message:", message.content);
  },
});

const result = await agent.runAgent({ runId: "run-example" });

console.log("newMessages:", result.newMessages.map((message) => message.content));
console.log("agent.messages:", agent.messages.map((message) => message.content));
