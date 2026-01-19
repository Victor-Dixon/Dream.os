"""
Status Reader - Legacy Compatibility
===================================

SSOT adapter for status access in tests and legacy code.

<!-- SSOT Domain: discord -->
"""

from __future__ import annotations

from .status_service import status_service


class StatusReader:
    """Simple status reader wrapper."""

    def __init__(self) -> None:
        self.status_service = status_service

    def get_agent_status(self, agent_id: str):
        return self.status_service.read_agent_status(agent_id)

