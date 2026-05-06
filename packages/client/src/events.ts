import type { BaseEvent } from "@ag-ui/client";
import type { GraphQLAgentEvent } from "./types";

export function unwrapGraphQLAgentEvent(event: BaseEvent | GraphQLAgentEvent): BaseEvent {
  return isGraphQLAgentEvent(event) ? event.payload : event;
}

export function isGraphQLAgentEvent(event: BaseEvent | GraphQLAgentEvent): event is GraphQLAgentEvent {
  if (!event || typeof event !== "object" || !("payload" in event)) {
    return false;
  }

  const payload = (event as { payload?: unknown }).payload;
  return (
    !!payload &&
    typeof payload === "object" &&
    "type" in payload &&
    typeof (payload as { type?: unknown }).type === "string" &&
    (payload as { type: string }).type === (event as { type?: unknown }).type
  );
}
