# src/services/messaging_discord.py
"""
<!-- SSOT Domain: communication -->
Discord messaging integration for unified messaging system.
"""

from src.core.messaging_core import (
    UnifiedMessagePriority,
    UnifiedMessageTag,
    UnifiedMessageType,
    send_message,
)


def send_discord_message(
    content: str, channel_id: str, priority: UnifiedMessagePriority = UnifiedMessagePriority.REGULAR
) -> bool:
    """Send a message via Discord integration using the unified messaging core."""
    tags = [UnifiedMessageTag.SYSTEM, UnifiedMessageTag.COORDINATION]
    return send_message(
        content=content,
        sender="DISCORD",
        recipient=channel_id,
        message_type=UnifiedMessageType.BROADCAST,
        priority=priority,
        tags=tags,
    )
