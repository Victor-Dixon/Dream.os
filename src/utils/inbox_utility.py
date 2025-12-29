#!/usr/bin/env python3
"""
<!-- SSOT Domain: core -->

Inbox Utility - Direct File Creation for Agents
===============================================

Separate utility for agents who want to create inbox files directly.
This is NOT part of the messaging system - it's a simple file creation utility.

Usage:
    from src.utils.inbox_utility import create_inbox_message
    
    create_inbox_message(
        recipient="Agent-4",
        sender="Agent-7",
        content="Your message here",
        priority="urgent"
    )

Author: Agent-4 (Captain)
Date: 2025-11-27
"""

from __future__ import annotations

import logging
import threading
from datetime import datetime
from pathlib import Path
from typing import Optional

from ..utils.swarm_time import format_swarm_timestamp, format_swarm_timestamp_filename

logger = logging.getLogger(__name__)

# Thread-safe lock for concurrent inbox writes
_inbox_write_lock = threading.Lock()


def create_inbox_message(
    recipient: str,
    sender: str,
    content: str,
    priority: str = "normal",
    message_type: str = "text",
    tags: Optional[list[str]] = None,
) -> bool:
    """
    Create an inbox message file directly in agent's inbox directory.
    
    This is a simple file creation utility - NOT part of the messaging system.
    Agents should use this when they want to create inbox files directly.
    
    Args:
        recipient: Agent ID (e.g., "Agent-4") - MUST be Agent-1 through Agent-8
        sender: Sender identifier
        content: Message content
        priority: Message priority (normal, urgent, etc.)
        message_type: Message type (text, broadcast, etc.)
        tags: Optional list of tags
        
    Returns:
        True if file created successfully, False otherwise
    """
    # Validate agent ID format (Agent-1 through Agent-8 only)
    valid_agent_ids = {f"Agent-{i}" for i in range(1, 9)}
    if recipient not in valid_agent_ids:
        logger.error(
            f"❌ Invalid recipient agent ID: '{recipient}'. "
            f"Must be one of: {', '.join(sorted(valid_agent_ids))}"
        )
        return False
    
    try:
        # FIXED: Use absolute path from project root to prevent routing issues
        # when called from different working directories (Discord bot, queue processor, etc.)
        project_root = Path(__file__).resolve().parent.parent.parent
        inbox_dir = project_root / "agent_workspaces" / recipient / "inbox"
        inbox_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate filename with timestamp + UUID to prevent concurrent overwrites
        import uuid
        timestamp = format_swarm_timestamp_filename()
        unique_id = str(uuid.uuid4())[:8]
        filename = f"INBOX_MESSAGE_{timestamp}_{unique_id}.md"
        filepath = inbox_dir / filename
        
        # Format message content
        message_content = _format_inbox_message(
            recipient=recipient,
            sender=sender,
            content=content,
            priority=priority,
            message_type=message_type,
            tags=tags or [],
        )
        
        # FIXED: Thread-safe file write for concurrent messaging calls
        with _inbox_write_lock:
            filepath.write_text(message_content, encoding="utf-8")
        
        # VERIFICATION: Verify file was actually written
        if not filepath.exists():
            logger.error(
                f"❌ Inbox file write failed - file does not exist after write: {filepath}"
            )
            return False
        
        # Verify file has content
        try:
            file_size = filepath.stat().st_size
            if file_size == 0:
                logger.error(
                    f"❌ Inbox file write failed - file is empty: {filepath}"
                )
                return False
        except Exception as e:
            logger.error(
                f"❌ Inbox file verification failed - cannot read file stats: {filepath}, error: {e}"
            )
            return False
        
        logger.info(
            f"✅ Inbox message created and verified: {filepath} "
            f"(recipient: {recipient}, size: {file_size} bytes)"
        )
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to create inbox message: {e}")
        return False


def _format_inbox_message(
    recipient: str,
    sender: str,
    content: str,
    priority: str,
    message_type: str,
    tags: list[str],
) -> str:
    """Format message content for inbox file."""
    timestamp_str = format_swarm_timestamp()
    
    tags_str = ", ".join(tags) if tags else "none"
    
    return f"""# 🚨 INBOX MESSAGE - {message_type.upper()}

**From**: {sender}
**To**: {recipient}
**Priority**: {priority}
**Message Type**: {message_type}
**Tags**: {tags_str}
**Timestamp**: {timestamp_str}

---

{content}

---

*Message created via inbox utility (direct file creation)*
*WE. ARE. SWARM. ⚡🔥*
"""

