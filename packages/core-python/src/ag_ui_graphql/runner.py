"""Runner protocol implemented by framework-specific AG-UI bridges."""

from __future__ import annotations

from typing import Any, AsyncIterator, Mapping, Protocol, Union

AGUIEvent = Union[Any, Mapping[str, Any]]


class AgentRunner(Protocol):
    """A source of canonical AG-UI events for GraphQL resolvers.

    Native framework runners may yield ``ag_ui.core`` Pydantic models. HTTP
    proxy runners usually yield decoded AG-UI JSON dictionaries. Both shapes
    are accepted by ``event_to_graphql_event``.
    """

    async def run(self, run_input: Any) -> AsyncIterator[AGUIEvent]:
        """Start an agent run and yield AG-UI events."""
        ...

    async def continue_run(self, thread_id: str, run_id: str) -> AsyncIterator[AGUIEvent]:
        """Continue a paused agent run and yield AG-UI events."""
        ...
