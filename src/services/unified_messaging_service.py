"""
Unified Messaging Service - Wrapper for Messaging Service
==========================================================

<!-- SSOT Domain: communication -->

Provides unified interface to messaging system.
Wraps ConsolidatedMessagingService for backward compatibility.

Navigation References:
├── Related Files:
│   ├── Core Messaging → src/services/messaging_infrastructure.py
│   ├── CLI Interface → messaging_cli_unified.py
│   ├── Message Queue → src/core/message_queue/message_queue_impl.py
│   ├── WebSocket Server → src/services/risk_analytics/risk_websocket_server.py
│   └── Discord Integration → src/services/messaging_discord.py
├── Documentation:
│   ├── Messaging Architecture → docs/architecture/MESSAGING_ARCHITECTURE.md
│   ├── Agent Communication → docs/AGENTS.md
│   └── Messaging Contracts → docs/messaging-contracts.mdc
├── API Endpoints:
│   ├── REST API → src/services/messaging/messaging_rest_api.py
│   └── WebSocket API → ws://localhost:8765/ws/risk/live
└── Usage:
    └── CLI Tool → python -m src.services.messaging_cli --help

V2 Compliance: Wrapper pattern, <400 lines
"""

from typing import Any

from src.core.base.base_service import BaseService
from .messaging_infrastructure import ConsolidatedMessagingService


class UnifiedMessagingService(BaseService):
    """Unified messaging service wrapper."""

    def __init__(self):
        """Initialize unified messaging service."""
        super().__init__("UnifiedMessagingService")
        self.messaging = ConsolidatedMessagingService()
        self.logger.info("UnifiedMessagingService initialized")

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
        message_category=None,
        sender: str | None = None,
    ) -> dict[str, Any]:
        """
        Send message to agent.

        Args:
            agent: Target agent ID
            message: Message content
            priority: Message priority (regular/urgent)
            use_pyautogui: Use PyAutoGUI delivery
            wait_for_delivery: Wait for delivery confirmation
            timeout: Timeout in seconds
            discord_user_id: Discord user ID (optional)
            stalled: Whether message is for stalled agent
            apply_template: Apply SSOT template before sending (default: False)
            message_category: Explicit template category (defaults to D2A for Discord)
            sender: Override sender name when templating

        Returns:
            Dictionary with success status and queue_id
        """
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

    def broadcast_message(self, message: str, priority: str = "regular") -> dict:
        """
        Broadcast message to all agents.

        Args:
            message: Message content
            priority: Message priority

        Returns:
            Dictionary of results {agent_id: success}
        """
        return self.messaging.broadcast_message(message, priority)


# Alias for backward compatibility
MessagingService = UnifiedMessagingService
