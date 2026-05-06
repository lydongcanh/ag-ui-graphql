export type {
  AbstractAgent,
  AgentConfig,
  AgentSubscriber,
  BaseEvent,
  Context,
  EventType,
  Message,
  RunAgentParameters,
  RunAgentInput,
  RunAgentResult,
  State,
  Tool,
} from "@ag-ui/client";

import type { BaseEvent, RunAgentInput } from "@ag-ui/client";

export type JsonPrimitive = string | number | boolean | null;
export type JsonValue = JsonPrimitive | JsonObject | JsonValue[];
export type JsonObject = { [key: string]: JsonValue | undefined };

export type HitlRequirement = {
  id: string;
  type: string;
  toolName?: string | null;
  toolArgs?: JsonValue;
  userInputSchema?: JsonValue;
  payload: JsonValue;
};

export type GraphQLAgentEvent<TEvent extends BaseEvent = BaseEvent> = {
  type: TEvent["type"] | string;
  payload: TEvent;
  timestamp?: number | null;

  // These are GraphQL projections for client convenience. The canonical
  // protocol event remains in `payload` and is typed by @ag-ui/client.
  messageId?: string | null;
  toolCallId?: string | null;
  toolCallName?: string | null;
  textDelta?: string | null;
  hitlRequirements?: HitlRequirement[] | null;
};

export type GraphQLAgentEventStream =
  | AsyncIterable<BaseEvent | GraphQLAgentEvent>
  | Iterable<BaseEvent | GraphQLAgentEvent>;

export type GraphQLRunExecutor = (
  input: RunAgentInput,
  options: { signal: AbortSignal },
) => GraphQLAgentEventStream | Promise<GraphQLAgentEventStream>;
