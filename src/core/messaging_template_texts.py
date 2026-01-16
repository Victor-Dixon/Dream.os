#!/usr/bin/env python3
"""
Messaging Template Texts - Core Layer
====================================

Basic template text handling for messaging operations.
Provides template storage and formatting functions.

<!-- SSOT Domain: communication -->

V2 Compliance | Author: Agent-1 | Date: 2026-01-16
"""

from __future__ import annotations

from typing import Any, Dict

from messaging_models import MessageCategory


# Basic message templates (can be extended)
MESSAGE_TEMPLATES = {
    MessageCategory.S2A: {
        "CONTROL": "System control message",
        "ONBOARDING": "Agent onboarding message",
        "COORDINATON": "Swarm coordination message"
    },
    MessageCategory.D2A: "Discord to Agent message template",
    MessageCategory.C2A: "Captain to Agent message template",
    MessageCategory.A2A: "Agent to Agent coordination template"
}


def format_d2a_payload(payload: Dict[str, Any]) -> str:
    """
    Format Discord-to-Agent payload.

    Args:
        payload: Payload data

    Returns:
        Formatted payload string
    """
    return f"D2A: {payload}"


def format_s2a_message(message: str, **kwargs) -> str:
    """
    Format System-to-Agent message.

    Args:
        message: Base message
        **kwargs: Additional formatting parameters

    Returns:
        Formatted message string
    """
    return f"S2A: {message}"