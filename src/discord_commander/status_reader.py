#!/usr/bin/env python3
"""
Status Reader (Compatibility Shim)
==================================

<!-- SSOT Domain: discord -->
"""

from __future__ import annotations

from typing import Any

from .status_service import status_service


class StatusReader:
    """Simple status reader for tests and legacy imports."""

    def get_agent_status(self, agent_id: str) -> dict[str, Any] | None:
        return status_service.read_agent_status(agent_id)


__all__ = ["StatusReader"]
