#!/usr/bin/env python3
"""
Messaging Service Adapters (Compatibility Shim)
==============================================

<!-- SSOT Domain: discord -->
"""

from __future__ import annotations

from typing import Any


class ConsolidatedMessagingService:
    """Minimal messaging service shim for Discord commander tests."""

    def send_message(
        self,
        agent: str,
        message: str,
        priority: str = "regular",
        use_pyautogui: bool = True,
        wait_for_delivery: bool = False,
        timeout: float = 30.0,
        discord_user_id: str | None = None,
        stalled: bool = False,
        apply_template: bool = False,
        message_category: Any = None,
        sender: str | None = None,
    ) -> dict[str, Any]:
        return {"success": True}

    def broadcast_message(self, message: str, priority: str = "regular") -> dict[str, Any]:
        return {"success": True}


__all__ = ["ConsolidatedMessagingService"]
