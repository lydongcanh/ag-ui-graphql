import { EventType, type BaseEvent } from "@ag-ui/client";
import { describe, expect, it } from "vitest";
import {
  GraphQLAgent,
  unwrapGraphQLAgentEvent,
  type GraphQLAgentEvent,
} from "../src";
import { readFixture } from "./fixtures";

async function* streamFixture(name: string): AsyncIterable<GraphQLAgentEvent> {
  for (const event of readFixture(name)) {
    yield event;
  }
}

describe("GraphQLAgent", () => {
  it("feeds GraphQL-wrapped AG-UI events through the official AbstractAgent pipeline", async () => {
    const agent = new GraphQLAgent({
      threadId: "thread-1",
      execute: () => streamFixture("text-stream.jsonl"),
    });

    const result = await agent.runAgent();

    expect(result.newMessages).toHaveLength(1);
    expect(result.newMessages[0]).toMatchObject({
      id: "assistant-1",
      role: "assistant",
      content: "Hello mate.",
    });
    expect(agent.messages).toHaveLength(1);
    expect(agent.messages[0]?.content).toBe("Hello mate.");
  });

  it("can unwrap GraphQL event envelopes into canonical AG-UI events", () => {
    const event = readFixture("text-stream.jsonl")[0];

    expect(unwrapGraphQLAgentEvent(event)).toEqual({
      type: EventType.RUN_STARTED,
      threadId: "thread-1",
      runId: "run-1",
    });
  });

  it("passes canonical AG-UI events through unchanged", () => {
    const event: BaseEvent = {
      type: EventType.RUN_FINISHED,
      threadId: "thread-1",
      runId: "run-1",
    };

    expect(unwrapGraphQLAgentEvent(event)).toBe(event);
  });
});
