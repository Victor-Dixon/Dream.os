"""Unified messaging service shim for tests."""

from __future__ import annotations

from typing import Any


class UnifiedMessagingService:
    def send_message(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
        return {"success": True}
