"""Messaging infrastructure compatibility shim."""

from __future__ import annotations

from typing import Any


class ConsolidatedMessagingService:
    def send_message(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
        return {"success": True}

    def broadcast_message(self, message: str, priority: str = "regular") -> dict[str, Any]:
        return {"Agent-1": True}
