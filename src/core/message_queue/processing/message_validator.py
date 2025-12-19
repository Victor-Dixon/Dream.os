#!/usr/bin/env python3
"""
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
