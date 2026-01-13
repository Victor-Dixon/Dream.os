"""
Messaging Core Protocol - Type-safe interface for messaging core (real or mock)

<!-- SSOT Domain: infrastructure -->

Defines the protocol that both real and mock messaging cores must implement.

Author: Agent-2 (Architecture & Design Specialist)
Date: 2025-11-28
License: MIT
"""

from typing import Protocol, Any
from ..messaging_models_core import (
    UnifiedMessageType,
    UnifiedMessagePriority,
    UnifiedMessageTag,
)


class MessagingCoreProtocol(Protocol):
    """Protocol for messaging core (real or mock)."""

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
        Send message - matches real messaging_core.send_message signature.

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
        ...




