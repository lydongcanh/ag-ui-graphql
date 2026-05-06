"""In-memory HITL requirement storage for local development and tests."""

from __future__ import annotations

from typing import Dict, List

from ..types import HitlRequirement


class MemoryHitlStore:
    def __init__(self) -> None:
        self._items: Dict[str, List[HitlRequirement]] = {}

    def set(self, run_id: str, requirements: List[HitlRequirement]) -> None:
        self._items[run_id] = list(requirements)

    def get(self, run_id: str) -> List[HitlRequirement]:
        return list(self._items.get(run_id, []))

    def delete(self, run_id: str) -> None:
        self._items.pop(run_id, None)
