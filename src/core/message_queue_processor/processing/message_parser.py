#!/usr/bin/env python3
"""
<<<<<<< HEAD
Message Parser for Message Queue Processing
===========================================

Parses message data for queue processing.
"""

from typing import Dict, Any, Optional


def parse_message_data(message_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse message data for processing.

    Args:
        message_data: Raw message data dictionary from queue

    Returns:
        Parsed message data with all required fields
    """
    try:
        # Handle the actual message structure from the queue
        parsed = {
            "message_id": message_data.get("message_id") or "unknown",  # Handle None message_id
            "sender": message_data.get("sender", "system"),
            "recipient": message_data.get("recipient", "unknown"),
            "content": message_data.get("content", ""),
            "timestamp": message_data.get("timestamp") or message_data.get("created_at"),  # Fallback to created_at
            "priority": message_data.get("priority", "normal"),
            "parsed": True
        }

        # Extract message_type_str from message_type or type field
        message_type = message_data.get("message_type") or message_data.get("type", "text")
        parsed["message_type_str"] = message_type

        # Extract priority_str (for consistency)
        parsed["priority_str"] = message_data.get("priority", "normal")

        # Extract tags list
        tags = message_data.get("tags", [])
        parsed["tags_list"] = tags if isinstance(tags, list) else []

        # Extract metadata
        parsed["metadata"] = message_data.get("metadata", {})

        return parsed
    except Exception as e:
        return {"error": f"Failed to parse message: {str(e)}", "parsed": False}
=======
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
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
