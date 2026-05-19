"""Strawberry GraphQL types for the AG-UI bridge envelope.

The protocol payload stays as a JSON scalar so the schema does not fork the
AG-UI event surface. Only the GraphQL envelope itself gets named GraphQL
types here, mirroring the dataclasses in ``ag_ui_graphql.types``.
"""

from __future__ import annotations

from typing import List, Optional

import strawberry
from strawberry.scalars import JSON

from ..types import GraphQLAgentEvent, HitlRequirement


@strawberry.type(name="HitlRequirement")
class HitlRequirementType:
    id: str
    type: str
    payload: JSON
    tool_name: Optional[str] = None
    tool_args: Optional[JSON] = None
    user_input_schema: Optional[JSON] = None

    @classmethod
    def from_domain(cls, requirement: HitlRequirement) -> "HitlRequirementType":
        return cls(
            id=requirement.id,
            type=requirement.type,
            payload=requirement.payload,
            tool_name=requirement.tool_name,
            tool_args=requirement.tool_args,
            user_input_schema=requirement.user_input_schema,
        )


@strawberry.type(name="GraphQLAgentEvent")
class GraphQLAgentEventType:
    type: str
    payload: JSON
    timestamp: Optional[float] = None
    message_id: Optional[str] = None
    tool_call_id: Optional[str] = None
    tool_call_name: Optional[str] = None
    text_delta: Optional[str] = None
    hitl_requirements: List[HitlRequirementType] = strawberry.field(default_factory=list)

    @classmethod
    def from_domain(cls, event: GraphQLAgentEvent) -> "GraphQLAgentEventType":
        return cls(
            type=event.type,
            payload=event.payload,
            timestamp=event.timestamp,
            message_id=event.message_id,
            tool_call_id=event.tool_call_id,
            tool_call_name=event.tool_call_name,
            text_delta=event.text_delta,
            hitl_requirements=[
                HitlRequirementType.from_domain(item) for item in event.hitl_requirements
            ],
        )


__all__ = ["GraphQLAgentEventType", "HitlRequirementType"]
