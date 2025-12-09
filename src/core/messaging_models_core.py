#!/usr/bin/env python3
"""
Messaging Models Core - Backward Compatibility Re-export Module
================================================================

<!-- SSOT Domain: integration -->

This module re-exports all messaging models, templates, and formatters
for backward compatibility. The actual implementations are split into:
- messaging_models.py: Models and enums only
- messaging_template_texts.py: Template strings and formatters

Author: Agent-1 (Integration & Core Systems Specialist)
Created: 2025-10-11
License: MIT
"""

from __future__ import annotations

# Re-export models and enums
from .messaging_models import (
    DeliveryMethod,
    MessageCategory,
    RecipientType,
    SenderType,
    UnifiedMessage,
    UnifiedMessagePriority,
    UnifiedMessageTag,
    UnifiedMessageType,
)

# Re-export templates and formatters
from .messaging_template_texts import (
    AGENT_OPERATING_CYCLE_TEXT,
    CYCLE_CHECKLIST_TEXT,
    D2A_REPORT_FORMAT_TEXT,
    D2A_RESPONSE_POLICY_TEXT,
    DISCORD_REPORTING_TEXT,
    MESSAGE_TEMPLATES,
    format_d2a_payload,
    format_s2a_message,
)

__all__ = [
    # Models and enums
    "DeliveryMethod",
    "UnifiedMessageType",
    "UnifiedMessagePriority",
    "MessageCategory",
    "UnifiedMessageTag",
    "RecipientType",
    "SenderType",
    "UnifiedMessage",
    # Templates and formatters
    "MESSAGE_TEMPLATES",
    "AGENT_OPERATING_CYCLE_TEXT",
    "CYCLE_CHECKLIST_TEXT",
    "DISCORD_REPORTING_TEXT",
    "D2A_RESPONSE_POLICY_TEXT",
    "D2A_REPORT_FORMAT_TEXT",
    "format_d2a_payload",
    "format_s2a_message",
]
