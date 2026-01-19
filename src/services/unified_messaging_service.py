"""
Unified Messaging Service
=========================

SSOT placeholder for messaging orchestration.

<!-- SSOT Domain: integration -->
"""

from __future__ import annotations

from typing import Any, Dict


class UnifiedMessagingService:
    """Minimal UnifiedMessagingService for compatibility."""

    def __init__(self) -> None:
        self.agent_data: Dict[str, Dict[str, Any]] = {}

    def send_message(self, **kwargs: Any) -> Dict[str, Any]:
        return {"success": True}

    def broadcast_message(self, **kwargs: Any) -> bool:
        return True

