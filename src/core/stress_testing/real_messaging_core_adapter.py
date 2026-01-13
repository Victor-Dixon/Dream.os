"""
<!-- SSOT Domain: core -->

Real Messaging Core Adapter - Wraps real messaging_core for protocol compliance

Adapter that wraps the real messaging_core.send_message function to match
the MessagingCoreProtocol interface.

Author: Agent-2 (Architecture & Design Specialist)
Date: 2025-11-28
License: MIT
"""

from typing import Any, Callable

from ..messaging_models_core import (
    UnifiedMessageType,
    UnifiedMessagePriority,
    UnifiedMessageTag,
)


class RealMessagingCoreAdapter:
    """Adapter wrapping real messaging_core.send_message for protocol compliance."""

    def __init__(self, send_message_func: Callable):
        """
        Initialize adapter with real send_message function.

        Args:
            send_message_func: The real send_message function from messaging_core
        """
        self._send_message = send_message_func

    def send_message(
        self,
        content: str,
        sender: str,
        recipient: str,
        message_type: UnifiedMessageType,
        priority: UnifiedMessagePriority = UnifiedMessagePriority.REGULAR,
        tags: list[UnifiedMessageTag] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> bool:
        """
        Delegate to real messaging core.

        Args:
            content: Message content
            sender: Message sender
            recipient: Message recipient
            message_type: Type of message
            priority: Message priority
            tags: Message tags
            metadata: Additional metadata

        Returns:
            True if delivery successful, False otherwise
        """
        return self._send_message(
            content, sender, recipient, message_type, priority, tags, metadata
        )




