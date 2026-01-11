#!/usr/bin/env python3
"""
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