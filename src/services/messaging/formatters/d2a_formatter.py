#!/usr/bin/env python3
"""
D2A Formatter - Discord-to-Agent Message Formatting
===================================================

<!-- SSOT Domain: messaging -->

Formatter for Discord-to-Agent (D2A) messages with Discord-specific formatting rules.

V2 Compliance | Author: Agent-1 | Date: 2026-01-16
"""

from typing import Any, Dict, Optional

from src.core.messaging_core import UnifiedMessagePriority
from src.core.messaging_models_core import MessageCategory, format_d2a_payload

from ..unified_formatter import BaseMessageFormatter


class D2AFormatter(BaseMessageFormatter):
    """Formatter for Discord-to-Agent (D2A) messages."""

    def __init__(self):
        super().__init__(MessageCategory.D2A)

    def format_message(self, message: str, sender: str, recipient: str,
                      priority: UnifiedMessagePriority, message_id: str,
                      extra: Optional[Dict[str, Any]] = None) -> str:
        """Format D2A message with Discord-specific formatting."""
        template_vars = self.get_template_vars(message, sender, recipient, priority, message_id, extra)

        # D2A template uses 'content' instead of 'message'
        template_vars['content'] = message

        # Add D2A-specific variables
        template_vars.update({
            'discord_sender': sender,
            'agent_recipient': recipient,
            'channel_info': extra.get('channel', 'unknown') if extra else 'unknown',
            'is_private': extra.get('is_private', False) if extra else False,
        })

        # Apply D2A payload formatting with defaults
        d2a_payload = format_d2a_payload(extra or {})
        template_vars.update(d2a_payload)

        return self.apply_template(template_vars)