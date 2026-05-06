"""Bridge-owned types for the GraphQL transport envelope.

AG-UI protocol models come from ``ag_ui.core``. The dataclasses here describe
only the GraphQL projection we expose around those canonical events.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class HitlRequirement:
    id: str
    type: str
    payload: Any
    tool_name: Optional[str] = None
    tool_args: Any = None
    user_input_schema: Any = None

    def to_graphql(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "type": self.type,
            "toolName": self.tool_name,
            "toolArgs": self.tool_args,
            "userInputSchema": self.user_input_schema,
            "payload": self.payload,
        }


@dataclass(frozen=True)
class GraphQLAgentEvent:
    type: str
    payload: Dict[str, Any]
    timestamp: Optional[float] = None
    message_id: Optional[str] = None
    tool_call_id: Optional[str] = None
    tool_call_name: Optional[str] = None
    text_delta: Optional[str] = None
    hitl_requirements: List[HitlRequirement] = field(default_factory=list)

    def to_graphql(self) -> Dict[str, Any]:
        return {
            "type": self.type,
            "payload": self.payload,
            "timestamp": self.timestamp,
            "messageId": self.message_id,
            "toolCallId": self.tool_call_id,
            "toolCallName": self.tool_call_name,
            "textDelta": self.text_delta,
            "hitlRequirements": [item.to_graphql() for item in self.hitl_requirements],
        }
