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
<<<<<<< HEAD
<<<<<<< HEAD
AGENT_ID_PATTERN = re.compile(
    r"^Agent-[1-8]$|^CAPTAIN$|^SYSTEM$|^DISCORD$", re.IGNORECASE)
=======
AGENT_ID_PATTERN = re.compile(r"^Agent-[1-8]$|^CAPTAIN$|^SYSTEM$|^DISCORD$", re.IGNORECASE)
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
=======
AGENT_ID_PATTERN = re.compile(
    r"^Agent-[1-8]$|^CAPTAIN$|^SYSTEM$|^DISCORD$", re.IGNORECASE)
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1


def validate_sender_format(sender: str) -> Tuple[bool, Optional[str]]:
    """
    Validate sender format matches expected agent ID pattern.
<<<<<<< HEAD
<<<<<<< HEAD

    Args:
        sender: Sender identifier to validate

=======
    
    Args:
        sender: Sender identifier to validate
        
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
=======

    Args:
        sender: Sender identifier to validate

>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not sender:
        return False, "Sender cannot be empty"
<<<<<<< HEAD
<<<<<<< HEAD

    if not isinstance(sender, str):
        return False, f"Sender must be a string, got {type(sender).__name__}"

    sender_upper = sender.upper()

    # Check if it matches the agent ID pattern
    if AGENT_ID_PATTERN.match(sender):
        return True, None

    # Check if it's in the AGENT_LIST (case-insensitive)
    if sender in AGENT_LIST:
        return True, None

=======
    
=======

>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
    if not isinstance(sender, str):
        return False, f"Sender must be a string, got {type(sender).__name__}"

    sender_upper = sender.upper()

    # Check if it matches the agent ID pattern
    if AGENT_ID_PATTERN.match(sender):
        return True, None

    # Check if it's in the AGENT_LIST (case-insensitive)
    if sender in AGENT_LIST:
        return True, None
<<<<<<< HEAD
    
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
=======

>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
    # Check case-insensitive match
    for agent_id in AGENT_LIST:
        if sender_upper == agent_id.upper():
            return True, None
<<<<<<< HEAD
<<<<<<< HEAD

    # Special cases that are valid
    valid_senders = ["CAPTAIN", "SYSTEM",
                     "DISCORD", "AGENT-4"]  # Agent-4 is CAPTAIN
    if sender_upper in [s.upper() for s in valid_senders]:
        return True, None

=======
    
=======

>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
    # Special cases that are valid
    valid_senders = ["CAPTAIN", "SYSTEM",
                     "DISCORD", "AGENT-4"]  # Agent-4 is CAPTAIN
    if sender_upper in [s.upper() for s in valid_senders]:
        return True, None
<<<<<<< HEAD
    
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
=======

>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
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
<<<<<<< HEAD
<<<<<<< HEAD

    For A2A messages, we require explicit sender identification to ensure
    proper routing and tracking. This prevents messages from defaulting to CAPTAIN.

=======
    
    For A2A messages, we require explicit sender identification to ensure
    proper routing and tracking. This prevents messages from defaulting to CAPTAIN.
    
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
=======

    For A2A messages, we require explicit sender identification to ensure
    proper routing and tracking. This prevents messages from defaulting to CAPTAIN.

>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
    Args:
        sender: Explicit sender provided via CLI (--sender flag)
        category: Message category (A2A messages require explicit sender)
        detected_sender: Auto-detected sender from environment/context
<<<<<<< HEAD
<<<<<<< HEAD

=======
        
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
=======

>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
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
<<<<<<< HEAD
<<<<<<< HEAD

=======
    
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
=======

>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
    # For A2A messages, require explicit sender identification
    if not sender:
        detected_str = f" (detected: {detected_sender})" if detected_sender else ""
        error_msg = (
            f"❌ A2A messages require explicit sender identification. "
            f"Use --sender Agent-X flag to identify yourself.{detected_str} "
            f"This ensures proper routing and allows tracking which agents performed which actions."
        )
        return False, None, error_msg
<<<<<<< HEAD
<<<<<<< HEAD

=======
    
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
=======

>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
    # Validate the sender format
    is_valid, format_error = validate_sender_format(sender)
    if not is_valid:
        return False, None, format_error
<<<<<<< HEAD
<<<<<<< HEAD

=======
    
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
=======

>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
    # Normalize sender (use case from AGENT_LIST if available)
    normalized = sender
    for agent_id in AGENT_LIST:
        if sender.upper() == agent_id.upper():
            normalized = agent_id
            break
<<<<<<< HEAD
<<<<<<< HEAD

=======
    
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
=======

>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
    # Special case: Agent-4 is CAPTAIN
    if normalized.upper() == "AGENT-4":
        normalized = "CAPTAIN"
    elif normalized.upper() == "CAPTAIN":
        normalized = "CAPTAIN"
<<<<<<< HEAD
<<<<<<< HEAD

=======
    
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
=======

>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
    return True, normalized, None


def log_agent_activity(
    sender: str,
    recipient: str,
    category: MessageCategory,
    message_id: Optional[str] = None,
) -> None:
    """
    Log agent activity for status tracking and monitoring.
<<<<<<< HEAD
<<<<<<< HEAD

    This allows the system to track which agents performed which actions,
    which can be tied to status.json updates and agent monitoring.

=======
    
    This allows the system to track which agents performed which actions,
    which can be tied to status.json updates and agent monitoring.
    
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
=======

    This allows the system to track which agents performed which actions,
    which can be tied to status.json updates and agent monitoring.

>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
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
<<<<<<< HEAD
<<<<<<< HEAD
            logger.warning(
                f"⚠️ Cannot log activity for invalid sender '{sender}': {error_msg}")
            return

=======
            logger.warning(f"⚠️ Cannot log activity for invalid sender '{sender}': {error_msg}")
            return
        
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
=======
            logger.warning(
                f"⚠️ Cannot log activity for invalid sender '{sender}': {error_msg}")
            return

>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
        # Log the activity (could be extended to write to status.json or tracking system)
        logger.info(
            f"📊 Agent Activity: {sender} → {recipient} "
            f"(category={category.value}, message_id={message_id or 'N/A'})"
        )
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1

        # Extended activity tracking implementation
        import asyncio
        try:
            asyncio.run(_update_agent_status(
                sender, message_id, category, recipient))
            asyncio.run(_write_central_activity_log(
                sender, recipient, category, message_id))
        except RuntimeError:
            # If there's already an event loop running, create a task
            loop = asyncio.get_event_loop()
            loop.create_task(_update_agent_status(
                sender, message_id, category, recipient))
            loop.create_task(_write_central_activity_log(
                sender, recipient, category, message_id))

<<<<<<< HEAD
=======
        
        # TODO: Could extend this to:
        # - Update agent_workspaces/{sender}/status.json with last_activity
        # - Write to a central activity log
        # - Update agent monitoring dashboard
        
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
=======
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
    except Exception as e:
        logger.warning(f"⚠️ Failed to log agent activity: {e}", exc_info=True)


<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
async def _update_agent_status(sender: str, message_id: Optional[str],
                               category: MessageCategory, recipient: str) -> None:
    """
    Update agent's status.json with last activity information.

    Args:
        sender: Agent ID that sent the message
        message_id: Unique message identifier
        category: Message category (A2A, C2A, etc.)
        recipient: Agent ID that received the message
    """
    import json
    import os
    from datetime import datetime

    try:
        # Construct path to agent's status file
        status_path = f"agent_workspaces/{sender}/status.json"

        # Read current status if it exists
        status_data = {}
        if os.path.exists(status_path):
            try:
                with open(status_path, 'r') as f:
                    status_data = json.load(f)
            except json.JSONDecodeError:
                logger.warning(
                    f"⚠️ Could not parse status file for {sender}, creating new one")
                status_data = {}

        # Update with activity information
        status_data.update({
            "last_activity": {
                "timestamp": datetime.now().isoformat(),
                "message_id": message_id,
                "category": category.value,
                "recipient": recipient
            },
            "last_updated": datetime.now().isoformat()
        })

        # Ensure required fields exist
        if "agent_id" not in status_data:
            status_data["agent_id"] = sender
        if "agent_name" not in status_data:
            status_data["agent_name"] = f"{sender} Agent"

        # Write updated status
        os.makedirs(os.path.dirname(status_path), exist_ok=True)
        with open(status_path, 'w') as f:
            json.dump(status_data, f, indent=2)

        logger.debug(f"✅ Updated status for {sender}")

    except Exception as e:
        logger.warning(f"⚠️ Failed to update agent status for {sender}: {e}")


async def _write_central_activity_log(sender: str, recipient: str,
                                      category: MessageCategory, message_id: Optional[str]) -> None:
    """
    Write message activity to central activity log.

    Args:
        sender: Agent ID that sent the message
        recipient: Agent ID that received the message
        category: Message category
        message_id: Unique message identifier
    """
    import json
    import os
    from datetime import datetime

    try:
        # Create logs directory if it doesn't exist
        log_dir = "logs"
        os.makedirs(log_dir, exist_ok=True)

        # Log file path (daily rotation)
        today = datetime.now().strftime("%Y-%m-%d")
        log_path = f"{log_dir}/agent_activity_{today}.jsonl"

        # Create activity log entry
        activity_entry = {
            "timestamp": datetime.now().isoformat(),
            "sender": sender,
            "recipient": recipient,
            "category": category.value,
            "message_id": message_id,
            "type": "message_activity"
        }

        # Append to log file (JSON Lines format)
        with open(log_path, 'a') as f:
            f.write(json.dumps(activity_entry) + '\n')

        logger.debug(f"✅ Logged activity: {sender} → {recipient}")

    except Exception as e:
        logger.warning(f"⚠️ Failed to write central activity log: {e}")
<<<<<<< HEAD
=======
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
=======
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
