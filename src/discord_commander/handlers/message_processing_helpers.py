#!/usr/bin/env python3
"""
<!-- SSOT Domain: discord -->

Message Processing Helpers
==========================

Helper functions for processing D2A messages.

V2 Compliance | Author: Agent-1 | Date: 2025-12-14
"""

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import discord

logger = logging.getLogger(__name__)


def parse_message_format(
    content: str, has_prefix: bool, developer_prefix: str
) -> tuple[str, str, str]:
    """Parse message format and extract recipient, content, and prefix."""
    lines = content.split('\n', 1)
    supported_prefixes = ('[D2A]', '[CHRIS]', '[ARIA]',
                          '[VICTOR]', '[CARYMN]', '[CHARLES]')

    if has_prefix:
        # Format: [PREFIX] Agent-X\n\nMessage content
        if len(lines) < 2:
            raise ValueError(f"Invalid message format: {content[:50]}")

        header = lines[0].strip()
        message_content = lines[1].strip()

        # Parse recipient (e.g., "[D2A] Agent-1" -> "Agent-1")
        parts = header.split()
        if len(parts) < 2:
            raise ValueError(f"Could not parse recipient from: {header}")

        recipient = parts[1]
        message_prefix = parts[0] if parts[0] in supported_prefixes else developer_prefix
    else:
        # Simple format: Agent-X\n\nMessage content
        if len(lines) < 2:
            raise ValueError(f"Invalid message format: {content[:50]}")

        header = lines[0].strip()
        message_content = lines[1].strip()
        recipient = header
        message_prefix = developer_prefix

    return recipient, message_content, message_prefix


async def validate_recipient(
    message: "discord.Message", recipient: str, logger: logging.Logger
) -> bool:
    """Validate recipient format and agent name."""
    # Validate recipient format
    if not recipient.startswith('Agent-'):
        logger.warning(f"Invalid recipient format: {recipient}")
        await message.add_reaction("❌")
        return False

    # Validate agent name is in allowed list
    from ..discord_agent_communication import AgentCommunicationEngine
    engine = AgentCommunicationEngine()
    if not engine.is_valid_agent(recipient):
        logger.warning(
            f"Invalid agent name: {recipient} (must be Agent-1 through Agent-8)")
        await message.add_reaction("❌")
        await message.channel.send(
            f"❌ Invalid agent name: `{recipient}`. "
            f"Only Agent-1 through Agent-8 are allowed."
        )
        return False

    return True


def build_devlog_command(recipient: str) -> str:
    """Build devlog command for recipient."""
    return (
        f"python tools/devlog_poster.py --agent {recipient} --file <devlog_path>\n"
        f"# Fallback:\n"
        f"python -m tools.toolbelt --devlog-post --agent {recipient}"
    )


def create_unified_message(
    message: "discord.Message", recipient: str, message_content: str
) -> "UnifiedMessage":
    """Create UnifiedMessage with D2A category."""
    from src.core.messaging_models_core import (
        UnifiedMessage,
        MessageCategory,
        UnifiedMessageType,
        UnifiedMessagePriority,
    )
    import uuid
    from datetime import datetime

    return UnifiedMessage(
        content=message_content,
        sender=f"Discord User ({message.author.name})",
        recipient=recipient,
        message_type=UnifiedMessageType.HUMAN_TO_AGENT,
        priority=UnifiedMessagePriority.REGULAR,
        category=MessageCategory.D2A,
        message_id=str(uuid.uuid4()),
        timestamp=datetime.now().isoformat(),
    )


async def handle_message_result(
    message: "discord.Message", result: dict,
    recipient: str, message_prefix: str, logger: logging.Logger
) -> None:
    """Handle message sending result."""
    if result.get("success"):
        queue_id = result.get("queue_id", "unknown")
        logger.info(
            f"✅ Message queued: {queue_id} → {recipient} ({message_prefix})")
        await message.add_reaction("✅")
        await message.channel.send(
            f"✅ Message queued for **{recipient}** (Queue ID: `{queue_id[:8]}...`)",
            reference=message
        )
    else:
        error = result.get("error", "Unknown error")
        logger.error(f"❌ Failed to queue message: {error}")
        await message.add_reaction("❌")
        await message.channel.send(
            f"❌ Failed to queue message: {error}",
            reference=message
        )

