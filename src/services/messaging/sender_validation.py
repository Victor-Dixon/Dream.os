#!/usr/bin/env python3
"""
Sender Validation Module - Messaging Infrastructure
===================================================

<!-- SSOT Domain: integration -->

Validates agent sender identification for proper routing and tracking.
Enforces that agents properly identify themselves when sending messages.

V2 Compliance | Author: Agent-1 | Date: 2025-12-21
"""

from __future__ import annotations

import logging
import re
from typing import Optional, Tuple

from src.core.constants.agent_constants import AGENT_LIST
from src.core.messaging_models_core import MessageCategory

logger = logging.getLogger(__name__)

# Regex pattern for valid agent IDs (Agent-1 through Agent-8, CAPTAIN, SYSTEM, etc.)

AGENT_ID_PATTERN = re.compile(
    r"^Agent-[1-8]$|^CAPTAIN$|^SYSTEM$|^DISCORD$", re.IGNORECASE)



def validate_sender_format(sender: str) -> Tuple[bool, Optional[str]]:
    """
    Validate sender format matches expected agent ID pattern.


    Args:
        sender: Sender identifier to validate


    Returns:
        Tuple of (is_valid, error_message)
    """
    if not sender:
        return False, "Sender cannot be empty"



    # Check case-insensitive match
    for agent_id in AGENT_LIST:
        if sender_upper == agent_id.upper():
            return True, None



    return False, (
        f"Invalid sender format: '{sender}'. "
        f"Expected format: Agent-1 through Agent-8, CAPTAIN, SYSTEM, or DISCORD. "
        f"Use --sender Agent-X to specify your agent ID."
    )


def validate_a2a_sender_identification(
    sender: Optional[str],
    category: Optional[MessageCategory],
    detected_sender: Optional[str] = None,
) -> Tuple[bool, Optional[str], Optional[str]]:
    """
    Validate that A2A messages have proper sender identification.


    For A2A messages, we require explicit sender identification to ensure
    proper routing and tracking. This prevents messages from defaulting to CAPTAIN.


    Args:
        sender: Explicit sender provided via CLI (--sender flag)
        category: Message category (A2A messages require explicit sender)
        detected_sender: Auto-detected sender from environment/context



    Returns:
        Tuple of (is_valid, normalized_sender, error_message)
        - is_valid: True if sender is properly identified
        - normalized_sender: The sender to use (validated and normalized)
        - error_message: Error message if validation fails, None if valid
    """
    # Only enforce for A2A messages
    if category != MessageCategory.A2A:
        # For non-A2A, use detected sender or default
        final_sender = sender or detected_sender or "SYSTEM"
        is_valid, error_msg = validate_sender_format(final_sender)
        if not is_valid:
            return False, None, error_msg
        return True, final_sender, None



    # For A2A messages, require explicit sender identification
    if not sender:
        detected_str = f" (detected: {detected_sender})" if detected_sender else ""
        error_msg = (
            f"❌ A2A messages require explicit sender identification. "
            f"Use --sender Agent-X flag to identify yourself.{detected_str} "
            f"This ensures proper routing and allows tracking which agents performed which actions."
        )
        return False, None, error_msg



    # Validate the sender format
    is_valid, format_error = validate_sender_format(sender)
    if not is_valid:
        return False, None, format_error



    # Normalize sender (use case from AGENT_LIST if available)
    normalized = sender
    for agent_id in AGENT_LIST:
        if sender.upper() == agent_id.upper():
            normalized = agent_id
            break



    # Special case: Agent-4 is CAPTAIN
    if normalized.upper() == "AGENT-4":
        normalized = "CAPTAIN"
    elif normalized.upper() == "CAPTAIN":
        normalized = "CAPTAIN"



    return True, normalized, None


def log_agent_activity(
    sender: str,
    recipient: str,
    category: MessageCategory,
    message_id: Optional[str] = None,
) -> None:
    """
    Log agent activity for status tracking and monitoring.


    This allows the system to track which agents performed which actions,
    which can be tied to status.json updates and agent monitoring.


    Args:
        sender: Sender agent ID
        recipient: Recipient agent ID
        category: Message category
        message_id: Optional message ID for tracking
    """
    try:
        # Validate sender before logging
        is_valid, error_msg = validate_sender_format(sender)
        if not is_valid:

            logger.warning(
                f"⚠️ Cannot log activity for invalid sender '{sender}': {error_msg}")
            return


        # Log the activity (could be extended to write to status.json or tracking system)
        logger.info(
            f"📊 Agent Activity: {sender} → {recipient} "
            f"(category={category.value}, message_id={message_id or 'N/A'})"
        )


    except Exception as e:
        logger.warning(f"⚠️ Failed to log agent activity: {e}", exc_info=True)




