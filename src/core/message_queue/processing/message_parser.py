#!/usr/bin/env python3
"""
<!-- SSOT Domain: core -->

Message Parser - Extract and Parse Message Data
===============================================

Parses message data from queue entries, handling both dict and UnifiedMessage formats.
"""

from typing import Any, Optional


def parse_message_data(message: Any) -> dict[str, Any]:
    """
    Parse message data from queue entry.

    Handles both dict (serialized) and UnifiedMessage object formats.
    Supports concurrent calls from different sources (Discord, CLI, queue, etc.).

    Args:
        message: Message data (dict or UnifiedMessage object)

    Returns:
        Dictionary with parsed message fields:
        - recipient: str | None
        - content: str | None
        - message_type_str: str | None
        - sender: str
        - priority_str: str
        - tags_list: list
        - metadata: dict
    """
    if isinstance(message, dict):
        # Message is a dict (serialized format)
        return {
            "recipient": message.get("recipient") or message.get("to"),
            "content": message.get("content"),
            "message_type_str": message.get("message_type") or message.get("type"),
            "sender": message.get("sender") or message.get("from", "SYSTEM"),
            "priority_str": message.get("priority", "regular"),
            "tags_list": message.get("tags", []),
            "metadata": message.get("metadata", {}),
        }
    else:
        # Message is UnifiedMessage object (object format)
        message_type_attr = getattr(message, "message_type", None)
        if message_type_attr:
            message_type_str = getattr(
                message_type_attr, "value", None) or str(message_type_attr)
        else:
            message_type_str = None

        priority_attr = getattr(message, "priority", None)
        if priority_attr:
            priority_str = getattr(
                priority_attr, "value", None) or str(priority_attr)
        else:
            priority_str = "regular"

        tags_attr = getattr(message, "tags", [])
        tags_list = [
            getattr(t, "value", None) or str(t)
            for t in tags_attr
        ] if tags_attr else []

        return {
            "recipient": getattr(message, "recipient", None),
            "content": getattr(message, "content", None),
            "message_type_str": message_type_str,
            "sender": getattr(message, "sender", "SYSTEM"),
            "priority_str": priority_str,
            "tags_list": tags_list,
            "metadata": getattr(message, "metadata", {}),
        }
