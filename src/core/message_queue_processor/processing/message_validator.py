#!/usr/bin/env python3
"""
Message Validator for Message Queue Processing
==============================================

Validates message data for queue processing.
"""

from typing import Dict, Any, Tuple, Optional


def validate_message_data(parsed_message: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
    """
    Validate parsed message data.

    Args:
        parsed_message: Parsed message data dictionary

    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        # Basic validation - check required fields
        required_fields = ["message_id", "sender", "recipient", "content"]
        for field in required_fields:
            if field not in parsed_message or parsed_message[field] is None:
                return False, f"Missing required field: {field}"

        # Check if message was parsed successfully
        if not parsed_message.get("parsed", False):
            return False, "Message parsing failed"

        # Additional validation could be added here
        return True, None

    except Exception as e:
        return False, f"Validation error: {str(e)}"