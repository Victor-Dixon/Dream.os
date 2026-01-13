#!/usr/bin/env python3
"""
Message Router for Message Queue Processing
===========================================

Routes messages for delivery processing.
"""

from typing import Dict, Any, Optional


def route_message_delivery(validated_message: Dict[str, Any]) -> str:
    """
    Route message for delivery based on message type and priority.

    Args:
        validated_message: Validated message data

    Returns:
        Routing decision string ("core", "inbox", "error")
    """
    try:
        priority = validated_message.get("priority", "normal")
        recipient = validated_message.get("recipient", "")

        # Route based on priority
        if priority == "high" or priority == "urgent":
            return "core"  # Direct delivery via core system

        # Route based on recipient type
        if recipient.startswith("agent-") or recipient.startswith("captain"):
            return "core"  # Agent-to-agent messages go through core

        # Default to inbox for other messages
        return "inbox"

    except Exception as e:
        return "error"