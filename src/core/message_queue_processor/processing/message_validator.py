#!/usr/bin/env python3
"""
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
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
<<<<<<< HEAD
        return False, f"Validation error: {str(e)}"
=======
<!-- SSOT Domain: core -->

Message Validator - Validate Message Data
=========================================

Validates message data for required fields and correctness.
"""

import logging
from typing import Any, Optional

logger = logging.getLogger(__name__)


def validate_message_data(
    queue_id: str,
    recipient: Optional[str],
    content: Optional[str],
    tracker: Optional[Any] = None,
) -> tuple[bool, Optional[str]]:
    """
    Validate message data for required fields.
    
    Args:
        queue_id: Queue entry ID
        recipient: Recipient identifier
        content: Message content
        tracker: Optional activity tracker
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not recipient:
        error_msg = "missing_recipient"
        logger.warning(f"Entry {queue_id} missing recipient")
        if tracker and recipient and recipient.startswith("Agent-"):
            try:
                tracker.mark_inactive(recipient)
            except Exception:
                pass  # Non-critical tracking failure
        return False, error_msg
    
    if not content:
        error_msg = "missing_content"
        logger.warning(f"Entry {queue_id} missing content")
        if tracker and recipient and recipient.startswith("Agent-"):
            try:
                tracker.mark_inactive(recipient)
            except Exception:
                pass  # Non-critical tracking failure
        return False, error_msg
    
    return True, None
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
=======
        return False, f"Validation error: {str(e)}"
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
