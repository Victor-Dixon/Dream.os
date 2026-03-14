#!/usr/bin/env python3
# Header-Variant: full
# Owner: Dream.os
# Purpose: Module implementation and orchestration logic.
# SSOT: docs/recovery/recovery_registry.yaml#src-core-messaging-models-core
# @registry docs/recovery/recovery_registry.yaml#src-core-messaging-models-core

"""
Messaging Models Core - Backward Compatibility Re-export Hub

<!-- SSOT Domain: infrastructure -->

==============================================================

This module re-exports models from messaging_models.py for backward compatibility.
All new code should import directly from messaging_models.py.

Author: Agent-1 (Integration & Core Systems Specialist)
Created: 2025-12-09
License: MIT
"""

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
try:
    from .messaging_template_texts import (
        MESSAGE_TEMPLATES,
        format_d2a_payload,
        format_s2a_message,
    )
except Exception:
    MESSAGE_TEMPLATES = {}

    def format_d2a_payload(*_args, **_kwargs):
        return ""

    def format_s2a_message(*_args, **_kwargs):
        return ""

__all__ = [
    "DeliveryMethod",
    "MessageCategory",
    "RecipientType",
    "SenderType",
    "UnifiedMessage",
    "UnifiedMessagePriority",
    "UnifiedMessageTag",
    "UnifiedMessageType",
    "MESSAGE_TEMPLATES",
    "format_d2a_payload",
    "format_s2a_message",
]

