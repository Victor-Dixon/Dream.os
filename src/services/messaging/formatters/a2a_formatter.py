#!/usr/bin/env python3
"""
A2A Formatter - Agent-to-Agent Message Formatting
=================================================

<!-- SSOT Domain: messaging -->

Formatter for Agent-to-Agent (A2A) messages with coordination formatting rules.

V2 Compliance | Author: Agent-1 | Date: 2026-01-16
"""

from typing import Any, Dict, Optional

from src.core.messaging_core import UnifiedMessagePriority

from ..unified_formatter import BaseMessageFormatter


class A2AFormatter(BaseMessageFormatter):
    """Formatter for Agent-to-Agent (A2A) messages."""

    def __init__(self):
        super().__init__(MessageCategory.A2A)

    def format_message(self, message: str, sender: str, recipient: str,
                      priority: UnifiedMessagePriority, message_id: str,
                      extra: Optional[Dict[str, Any]] = None) -> str:
        """Format A2A message with agent coordination formatting."""
        template_vars = self.get_template_vars(message, sender, recipient, priority, message_id, extra)

        # Add A2A-specific variables
        template_vars.update({
            'coordination_id': extra.get('coordination_id', message_id) if extra else message_id,
            'task_context': extra.get('task_context', '') if extra else '',
            'requires_response': extra.get('requires_response', True) if extra else True,
        })

        return self.apply_template(template_vars)