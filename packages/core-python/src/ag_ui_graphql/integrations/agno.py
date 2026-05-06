"""Agno integration helpers.

Agno already exposes agents over AG-UI via ``AgentOS`` + ``AGUI``. The first
integration path intentionally uses that standard endpoint instead of calling
CopilotKit or redefining AG-UI.
"""

from __future__ import annotations

from typing import Dict, Optional
from urllib.parse import urljoin

from ..http import HttpAGUIRunner


class AgnoRunner(HttpAGUIRunner):
    """AG-UI HTTP runner for an Agno ``/agui`` endpoint."""

    def __init__(self, base_url: str, *, path: str = "/agui", headers: Optional[Dict[str, str]] = None) -> None:
        url = urljoin(base_url.rstrip("/") + "/", path.lstrip("/"))
        super().__init__(url, headers=headers)
