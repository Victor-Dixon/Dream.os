#!/usr/bin/env python3
"""
<<<<<<< HEAD
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
=======
<!-- SSOT Domain: core -->

Delivery Inbox - Fallback Inbox Delivery
========================================

Backup path for inbox file-based delivery when PyAutoGUI fails.
"""

import logging
from typing import Optional
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console

logger = logging.getLogger(__name__)


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
        inbox_dir.mkdir(parents=True, exist_ok=True)

        # Generate message filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        message_id = metadata.get("message_id", f"msg_{timestamp}") if isinstance(metadata, dict) else f"msg_{timestamp}"
        filename = f"CAPTAIN_MESSAGE_{timestamp}_{message_id[:8]}.md"
        filepath = inbox_dir / filename

        # Format message content in standard inbox format
        message_type = metadata.get('message_type', 'text') if isinstance(metadata, dict) else 'text'
        formatted_content = f"""# 🚨 CAPTAIN MESSAGE - {message_type.upper()}

**From**: {sender}
**To**: {recipient}
**Priority**: {priority_str}
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
