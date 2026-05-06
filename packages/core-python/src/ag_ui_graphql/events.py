"""Project canonical AG-UI events into the GraphQL transport envelope."""

from __future__ import annotations

from typing import Any, Dict, Mapping, Optional, cast

from .types import GraphQLAgentEvent, HitlRequirement


def event_to_graphql_event(event: Any) -> GraphQLAgentEvent:
    payload = event_to_payload(event)
    event_type = str(payload.get("type", "CUSTOM"))

    hitl_requirements = [
        _coerce_hitl_requirement(item)
        for item in (payload.get("hitlRequirements") or payload.get("requirements") or [])
        if isinstance(item, Mapping)
    ]

    return GraphQLAgentEvent(
        type=event_type,
        payload=payload,
        timestamp=payload.get("timestamp"),
        message_id=payload.get("messageId"),
        tool_call_id=payload.get("toolCallId"),
        tool_call_name=payload.get("toolCallName"),
        text_delta=payload.get("delta"),
        hitl_requirements=hitl_requirements,
    )


def event_to_payload(event: Any) -> Dict[str, Any]:
    if isinstance(event, dict):
        return dict(event)

    model_dump = getattr(event, "model_dump", None)
    if callable(model_dump):
        return _ensure_payload(model_dump(by_alias=True, exclude_none=True))

    dict_method = getattr(event, "dict", None)
    if callable(dict_method):
        return _ensure_payload(dict_method(by_alias=True, exclude_none=True))

    raise TypeError(f"Unsupported AG-UI event object: {type(event)!r}")


def _coerce_hitl_requirement(value: Mapping[str, Any]) -> HitlRequirement:
    payload = value.get("payload") or dict(value)
    return HitlRequirement(
        id=str(value["id"]),
        type=str(value["type"]),
        payload=payload,
        tool_name=_optional_string(value.get("toolName") or value.get("tool_name")),
        tool_args=value.get("toolArgs") or value.get("tool_args"),
        user_input_schema=value.get("userInputSchema") or value.get("user_input_schema"),
    )


def _optional_string(value: object) -> Optional[str]:
    return value if isinstance(value, str) else None


def _ensure_payload(value: object) -> Dict[str, Any]:
    if not isinstance(value, dict):
        raise TypeError(f"AG-UI event serialization returned {type(value)!r}, expected dict.")

    return cast(Dict[str, Any], value)
