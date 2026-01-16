#!/usr/bin/env python3
"""
S2A Formatter - System-to-Agent Message Formatting
==================================================

<!-- SSOT Domain: messaging -->

Formatter for System-to-Agent (S2A) messages with system notification formatting rules.

V2 Compliance | Author: Agent-1 | Date: 2026-01-16
"""

from typing import Any, Dict, Optional

from src.core.messaging_core import UnifiedMessagePriority

from ..unified_formatter import BaseMessageFormatter


class S2AFormatter(BaseMessageFormatter):
    """Formatter for System-to-Agent (S2A) messages."""

    def __init__(self):
        super().__init__(MessageCategory.S2A)

    def format_message(self, message: str, sender: str, recipient: str,
                      priority: UnifiedMessagePriority, message_id: str,
                      extra: Optional[Dict[str, Any]] = None) -> str:
        """Format S2A message with system notification formatting."""
        template_vars = self.get_template_vars(message, sender, recipient, priority, message_id, extra)

        # Add S2A-specific variables
        template_vars.update({
            'system_component': sender,
            'notification_type': extra.get('notification_type', 'info') if extra else 'info',
            'requires_acknowledgment': extra.get('requires_ack', False) if extra else False,
        })

        return self.apply_template(template_vars)