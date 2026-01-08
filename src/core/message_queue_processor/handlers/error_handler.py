#!/usr/bin/env python3
"""
Error Handler for Message Queue Processing
==========================================

Handles delivery errors and logging.
"""

import logging
from typing import Any, Optional

logger = logging.getLogger(__name__)


def handle_delivery_error(message: Any, error: Exception, attempt: int) -> str:
    """
    Handle delivery error and determine next action.

    Args:
        message: Message that failed to deliver
        error: The exception that occurred
        attempt: Current delivery attempt number

    Returns:
        Action string ("retry", "fail", "escalate")
    """
    try:
        logger.error(f"Delivery error on attempt {attempt}: {str(error)}")

        # Simple error handling logic
        if attempt < 3:
            return "retry"  # Retry up to 3 times
        elif "auth" in str(error).lower():
            return "escalate"  # Authentication errors need escalation
        else:
            return "fail"  # Give up after 3 attempts

    except Exception as e:
        logger.error(f"Error in error handler: {str(e)}")
        return "fail"