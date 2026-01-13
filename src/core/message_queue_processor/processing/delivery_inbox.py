#!/usr/bin/env python3
"""
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

logger = logging.getLogger(__name__)


def deliver_fallback_inbox(recipient: str, content: str, metadata: dict, sender: str, priority_str: str) -> bool:
    """
    Deliver message to inbox as fallback.

    Args:
        recipient: Agent ID to deliver to
        content: Message content
        metadata: Message metadata
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