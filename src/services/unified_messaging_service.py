"""Unified messaging service compatibility shim for legacy integrations/tests."""

from __future__ import annotations

from typing import Any

from .messaging_infrastructure import ConsolidatedMessagingService


class UnifiedMessagingService:
    """Thin wrapper around consolidated messaging service."""

    def __init__(self, messaging: ConsolidatedMessagingService | None = None) -> None:
        self.messaging = messaging or ConsolidatedMessagingService()

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
        return self.messaging.send_message(
            agent=agent,
            message=message,
            priority=priority,
            use_pyautogui=use_pyautogui,
            wait_for_delivery=wait_for_delivery,
            timeout=timeout,
            discord_user_id=discord_user_id,
            stalled=stalled,
            apply_template=apply_template,
            message_category=message_category,
            sender=sender,
        )

    def broadcast_message(self, message: str, priority: str = "regular") -> dict[str, Any]:
        return self.messaging.broadcast_message(message, priority)


MessagingService = UnifiedMessagingService

__all__ = ["UnifiedMessagingService", "MessagingService"]