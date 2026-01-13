#!/usr/bin/env python3
"""
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
Inbox Delivery for Message Queue Processing
===========================================

Handles fallback delivery to inbox.
"""

import logging
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Tuple, Optional
<<<<<<< HEAD
=======
<!-- SSOT Domain: core -->

Delivery Inbox - Fallback Inbox Delivery
========================================

Backup path for inbox file-based delivery when PyAutoGUI fails.
"""

import logging
from typing import Optional
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
=======
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1

logger = logging.getLogger(__name__)


<<<<<<< HEAD
<<<<<<< HEAD
def deliver_fallback_inbox(recipient: str, content: str, metadata: dict, sender: str, priority_str: str) -> bool:
    """
    Deliver message to inbox as fallback.
=======
def deliver_fallback_inbox(
    recipient: str,
    content: str,
    metadata: dict,
    sender: Optional[str] = None,
    priority_str: Optional[str] = None,
) -> bool:
    """
    Backup path: Inbox file-based delivery.

    Used when PyAutoGUI delivery fails (e.g., Cursor queue full).
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console

    Args:
        recipient: Agent ID to deliver to
        content: Message content
        metadata: Message metadata
<<<<<<< HEAD
        sender: Sender identifier
        priority_str: Priority string

    Returns:
        True if delivery successful, False otherwise
    """
    try:
        if not recipient:
            logger.error("No recipient specified")
            return False

        if not content:
            logger.error("No message content")
            return False

        # Create inbox directory path - handle recipients that already start with "Agent-"
        if recipient.startswith("Agent-"):
            agent_dir = recipient
        else:
            agent_dir = f"Agent-{recipient}"

        inbox_dir = Path("agent_workspaces") / agent_dir / "inbox"
=======
def deliver_fallback_inbox(message: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
    """
    Deliver message to inbox as fallback.

    Args:
        message: Message data to deliver

    Returns:
        Tuple of (success, error_message)
    """
    try:
        # Extract delivery information
        recipient = message.get("recipient", message.get("to"))
        sender = message.get("sender", message.get("from", "system"))
        content = message.get("content", message.get("message", ""))

        if not recipient:
            return False, "No recipient specified"

        if not content:
            return False, "No message content"

        # Create inbox directory path
        inbox_dir = Path("agent_workspaces") / f"Agent-{recipient}" / "inbox"
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
        inbox_dir.mkdir(parents=True, exist_ok=True)

        # Generate message filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
<<<<<<< HEAD
        message_id = metadata.get("message_id", f"msg_{timestamp}") if isinstance(metadata, dict) else f"msg_{timestamp}"
=======
        message_id = message.get("message_id", f"msg_{timestamp}")
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
        filename = f"CAPTAIN_MESSAGE_{timestamp}_{message_id[:8]}.md"
        filepath = inbox_dir / filename

        # Format message content in standard inbox format
<<<<<<< HEAD
        message_type = metadata.get('message_type', 'text') if isinstance(metadata, dict) else 'text'
        formatted_content = f"""# 🚨 CAPTAIN MESSAGE - {message_type.upper()}

**From**: {sender}
**To**: {recipient}
**Priority**: {priority_str}
=======
        formatted_content = f"""# 🚨 CAPTAIN MESSAGE - {message.get('type', 'text').upper()}

**From**: {sender}
**To**: {recipient}
**Priority**: {message.get('priority', 'normal')}
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
**Message ID**: {message_id}
**Timestamp**: {datetime.now().isoformat()}

---

{content}

---
*Message delivered via Inbox Fallback System*
"""

        # Write message to inbox
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(formatted_content)

<<<<<<< HEAD
        logger.info(f"✅ Message delivered to inbox: {filepath}")
        return True

    except Exception as e:
        logger.error(f"❌ Inbox delivery error: {e}")
        return False
=======
        sender: Sender identifier (preserved from message)
        priority_str: Priority string (preserved from message)

    Returns:
        True if inbox delivery successful, False otherwise
    """
    try:
        from ....utils.inbox_utility import create_inbox_message

        actual_sender = sender or metadata.get("sender", "SYSTEM")
        actual_priority = priority_str or metadata.get("priority", "normal")

        success = create_inbox_message(
            recipient=recipient,
            content=content,
            sender=actual_sender,
            priority=actual_priority,
        )

        if not success:
            logger.error(f"❌ Inbox delivery failed for {recipient}")
            return False

        logger.info(f"✅ Inbox delivery verified for {recipient}")
        return True
    except ImportError:
        logger.warning("Inbox utility not available")
        return False
    except Exception as e:
        logger.error(f"Inbox delivery error: {e}", exc_info=True)
        return False
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
=======
        logger.info(f"Message delivered to inbox: {filepath}")
        return True, None

    except Exception as e:
        logger.error(f"Inbox delivery error: {e}")
        return False, f"Inbox delivery failed: {str(e)}"
    except Exception as e:
        return False, f"Inbox delivery failed: {str(e)}"
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
