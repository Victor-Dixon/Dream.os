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
        inbox_dir.mkdir(parents=True, exist_ok=True)

        # Generate message filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        message_id = message.get("message_id", f"msg_{timestamp}")
        filename = f"CAPTAIN_MESSAGE_{timestamp}_{message_id[:8]}.md"
        filepath = inbox_dir / filename

        # Format message content in standard inbox format
        formatted_content = f"""# 🚨 CAPTAIN MESSAGE - {message.get('type', 'text').upper()}

**From**: {sender}
**To**: {recipient}
**Priority**: {message.get('priority', 'normal')}
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

        logger.info(f"Message delivered to inbox: {filepath}")
        return True, None

    except Exception as e:
        logger.error(f"Inbox delivery error: {e}")
        return False, f"Inbox delivery failed: {str(e)}"
    except Exception as e:
        return False, f"Inbox delivery failed: {str(e)}"