#!/usr/bin/env python3
"""
C2A Formatter - Client-to-Agent Message Formatting
==================================================

<!-- SSOT Domain: messaging -->

Formatter for Client-to-Agent (C2A) messages with client interaction formatting rules.

V2 Compliance | Author: Agent-1 | Date: 2026-01-16
"""

from typing import Any, Dict, Optional

from src.core.messaging_core import UnifiedMessagePriority

from ..unified_formatter import BaseMessageFormatter


class C2AFormatter(BaseMessageFormatter):
    """Formatter for Client-to-Agent (C2A) messages."""

    def __init__(self):
        super().__init__(MessageCategory.C2A)

    def format_message(self, message: str, sender: str, recipient: str,
                      priority: UnifiedMessagePriority, message_id: str,
                      extra: Optional[Dict[str, Any]] = None) -> str:
        """Format C2A message with client interaction formatting."""
        template_vars = self.get_template_vars(message, sender, recipient, priority, message_id, extra)

        # Add C2A-specific variables
        template_vars.update({
            'client_type': extra.get('client_type', 'unknown') if extra else 'unknown',
            'session_id': extra.get('session_id', message_id) if extra else message_id,
            'user_context': extra.get('user_context', {}) if extra else {},
        })

        return self.apply_template(template_vars)