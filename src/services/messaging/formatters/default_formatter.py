#!/usr/bin/env python3
"""
Default Formatter - Fallback Message Formatting
===============================================

<!-- SSOT Domain: messaging -->

Default formatter for unrecognized message categories with minimal formatting.

V2 Compliance | Author: Agent-1 | Date: 2026-01-16
"""

from typing import Any, Dict, Optional

from src.core.messaging_core import UnifiedMessagePriority

from ..unified_formatter import BaseMessageFormatter


class DefaultFormatter(BaseMessageFormatter):
    """Default formatter for unrecognized message categories."""

    def __init__(self):
        super().__init__(MessageCategory.A2A)  # Default to A2A template

    def format_message(self, message: str, sender: str, recipient: str,
                      priority: UnifiedMessagePriority, message_id: str,
                      extra: Optional[Dict[str, Any]] = None) -> str:
        """Format message with minimal default formatting."""
        template_vars = self.get_template_vars(message, sender, recipient, priority, message_id, extra)
        return self.apply_template(template_vars)