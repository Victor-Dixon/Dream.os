#!/usr/bin/env python3
"""
Service Adapters Module - Messaging Infrastructure
==================================================

<!-- SSOT Domain: integration -->

Extracted from messaging_infrastructure.py for V2 compliance.
Handles service adapters for Discord bot integration and external service wrappers.

V2 Compliance | Author: Agent-1 | Date: 2025-12-13
"""

from __future__ import annotations

import logging
import time
from pathlib import Path
from typing import Any

from src.core.config.timeout_constants import TimeoutConstants
from ...core.base.base_service import BaseService

from .discord_message_handler import send_discord_message_to_agent as _send_discord_message_to_agent

logger = logging.getLogger(__name__)


class ConsolidatedMessagingService(BaseService):
    """
    Consolidated messaging service adapter for Discord bot.

    CRITICAL UPDATE (2025-01-27): Uses message queue for synchronization
    Prevents race conditions when Discord + computer + agents send messages.
    All messages go through queue for sequential delivery with global lock.
    """

    def __init__(self):
        """Initialize messaging service."""
        super().__init__("ConsolidatedMessagingService")
        self.project_root = Path(__file__).parent.parent.parent
        self.messaging_cli = self.project_root / \
            "src" / "services" / "messaging_cli.py"

        # CRITICAL: Initialize message queue for synchronization
        try:
            from src.core.message_queue import MessageQueue

            self.queue = MessageQueue()
            self.logger.info(
                "✅ ConsolidatedMessagingService initialized with message queue")
        except Exception as e:
            self.logger.error(f"⚠️ Failed to initialize message queue: {e}")
            self.queue = None

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
        message_category: MessageCategory | None = None,
        sender: str | None = None,
    ) -> dict[str, Any]:
        """Send message to agent via message queue (synchronized delivery)."""
        return _send_discord_message_to_agent(
            agent=agent, message=message, priority=priority,
            use_pyautogui=use_pyautogui, wait_for_delivery=wait_for_delivery,
            timeout=timeout, discord_user_id=discord_user_id, stalled=stalled,
            apply_template=apply_template, message_category=message_category,
            sender=sender, queue=self.queue, messaging_cli_path=self.messaging_cli,
            project_root=self.project_root,
            resolve_discord_sender_func=self._resolve_discord_sender,
            get_discord_username_func=self._get_discord_username,
        )

    def broadcast_message(self, message: str, priority: str = "regular") -> dict[str, Any]:
        """Broadcast message to all agents with keyboard lock."""
        from .service_adapter_helpers import execute_broadcast_operation
        return execute_broadcast_operation(self.send_message, message, priority)

    def _resolve_discord_sender(self, discord_user_id: str | None) -> str:
        """Resolve Discord user ID to sender name."""
        if not discord_user_id:
            return "DISCORD"
        # For now, return DISCORD
        # In production, this could resolve to actual Discord username via API
        return "DISCORD"

    def _get_discord_username(self, discord_user_id: str | None) -> str | None:
        """
        Get Discord username from user ID.

        Args:
            discord_user_id: Discord user ID

        Returns:
            Username string or None
        """
        if not discord_user_id:
            return None
        # For now, return None
        # In production, this could resolve to actual Discord username via API
        return None


# Discord integration adapter functions
def send_discord_message(agent: str, message: str, priority: str = "regular") -> bool:
    """Send message via Discord integration (wraps ConsolidatedMessagingService)."""
    service = ConsolidatedMessagingService()
    result = service.send_message(
        agent, message, priority, use_pyautogui=False)
    return result.get("success", False)


def broadcast_discord_message(message: str, priority: str = "regular") -> dict[str, Any]:
    """Broadcast message via Discord integration."""
    service = ConsolidatedMessagingService()
    return service.broadcast_message(message, priority)

