#!/usr/bin/env python3
"""
Message Formatters Module - Messaging Infrastructure
====================================================

<!-- SSOT Domain: integration -->

Extracted from messaging_infrastructure.py for V2 compliance.
Handles message formatting, template application, and output formatting.

V2 Compliance | Author: Agent-1 | Date: 2025-12-12
"""

from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

from src.core.messaging_core import UnifiedMessagePriority
from src.core.messaging_models_core import (
    MessageCategory,
    MESSAGE_TEMPLATES,
    format_d2a_payload,
)

# Message templates for coordination
SURVEY_MESSAGE_TEMPLATE = """
🐝 SWARM SURVEY INITIATED - SRC/ DIRECTORY ANALYSIS
================================================

**OBJECTIVE:** Comprehensive analysis of src/ directory for consolidation planning
**TARGET:** 683 → ~250 files with full functionality preservation

**PHASES:**
1. Structural Analysis (Directories, files, dependencies)
2. Functional Analysis (Services, capabilities, relationships)
3. Quality Assessment (V2 compliance, violations, anti-patterns)
4. Consolidation Planning (Opportunities, risks, rollback strategies)

**COORDINATION:** Real-time via PyAutoGUI messaging system
**COMMANDER:** Captain Agent-4 (Quality Assurance Specialist)

🐝 WE ARE SWARM - UNITED IN ANALYSIS!
"""

ASSIGNMENT_MESSAGE_TEMPLATE = """
🐝 SURVEY ASSIGNMENT - {agent}
============================

**ROLE:** {assignment}

**DELIVERABLES:**
1. Structural Analysis Report
2. Functional Analysis Report
3. Quality Assessment Report
4. Consolidation Recommendations

**TIMELINE:** 8 days total survey
**COORDINATION:** Real-time via PyAutoGUI

🐝 YOUR EXPERTISE IS CRUCIAL FOR SUCCESSFUL CONSOLIDATION!
"""

CONSOLIDATION_MESSAGE_TEMPLATE = """
🔧 CONSOLIDATION UPDATE
======================

**BATCH:** {batch}
**STATUS:** {status}
**TIMESTAMP:** {timestamp}

**COORDINATION:** Real-time swarm coordination active
**COMMANDER:** Captain Agent-4

🔧 CONSOLIDATION PROGRESS CONTINUES...
"""


def _apply_template(
    category: MessageCategory,
    message: str,
    sender: str,
    recipient: str,
    priority: UnifiedMessagePriority,
    message_id: str,
    extra: Optional[Dict[str, Any]] = None,
) -> str:
    """
    Apply message template based on category.
    
    Args:
        category: Message category (D2A, A2A, etc.)
        message: Message content
        sender: Sender identifier
        recipient: Recipient identifier
        priority: Message priority
        message_id: Unique message ID
        extra: Additional metadata for template
        
    Returns:
        Formatted message string
    """
    tmpl = MESSAGE_TEMPLATES.get(category)
    if not tmpl:
        return message
    
    now = datetime.now().isoformat(timespec="seconds")
    meta = extra or {}
    
    # D2A requires extra fields; use canonical formatter to avoid KeyErrors.
    if category == MessageCategory.D2A:
        # CRITICAL FIX: Don't default actions to message - let format_d2a_payload set proper default
        # Otherwise message appears twice: once in {content} and once in {actions}
        d2a_payload = {
            k: v
            for k, v in {
                "interpretation": meta.get("interpretation"),
                "actions": meta.get("actions"),  # Only include if explicitly provided
                "fallback": meta.get("fallback"),
                "discord_response_policy": meta.get("discord_response_policy"),
                "d2a_report_format": meta.get("d2a_report_format"),
            }.items()
            if v is not None
        }
        d2a_meta = format_d2a_payload(d2a_payload)
        
        try:
            result = tmpl.format(
                sender=sender,
                recipient=recipient,
                priority=priority.value,
                message_id=message_id,
                timestamp=now,
                content=message,
                interpretation=d2a_meta["interpretation"],
                actions=d2a_meta["actions"],
                discord_response_policy=d2a_meta["discord_response_policy"],
                d2a_report_format=d2a_meta["d2a_report_format"],
                fallback=d2a_meta["fallback"],
            )
            
            # CRITICAL FIX: Validate message appears exactly once in template
            # If message appears multiple times, it means it's being duplicated
            message_count = result.count(message)
            if message_count > 1:
                # Message appears multiple times - fix duplication
                user_message_section = "User Message:\n"
                if user_message_section in result:
                    # Find the content section and ensure message only appears there
                    section_start = result.find(user_message_section) + len(user_message_section)
                    section_end = result.find("\n\n", section_start)
                    if section_end == -1:
                        section_end = len(result)
                    content_section = result[section_start:section_end]
                    # If message appears in content section, remove it from elsewhere
                    if message in content_section:
                        # Remove message from after the template (if appended)
                        if result.endswith(message):
                            result = result[:-len(message)].rstrip()
                        # Remove message from actions if it's there
                        if f"Proposed Action:\n{message}" in result:
                            result = result.replace(
                                f"Proposed Action:\n{message}",
                                f"Proposed Action:\n{d2a_meta['actions']}"
                            )
            return result
        except Exception:
            return message

    # A2A needs ask/context/next_step/fallback populated for clean rendering.
    if category == MessageCategory.A2A:
        return tmpl.format(
            sender=sender,
            recipient=recipient,
            priority=priority.value,
            message_id=message_id,
            timestamp=now,
            ask=meta.get("ask", message),
            context=meta.get("context", ""),
            next_step=meta.get("next_step", ""),
            fallback=meta.get(
                "fallback",
                "If blocked: send blocker + proposed fix + owner.",
            ),
        )

    return tmpl.format(
        sender=sender,
        recipient=recipient,
        priority=priority.value,
        message_id=message_id,
        timestamp=now,
        context=meta.get("context", ""),
        actions=meta.get("actions", message),
        fallback=meta.get("fallback", "Escalate to Captain"),
        task=meta.get("task", message),
        deliverable=meta.get("deliverable", ""),
        eta=meta.get("eta", ""),
        ask=meta.get("ask", message),
        next_step=meta.get("next_step", ""),
    )


def _format_multi_agent_request_message(
    message: str,
    collector_id: str,
    request_id: str,
    recipient_count: int,
    timeout_seconds: int
) -> str:
    """
    Format multi-agent request message with response instructions.
    
    Args:
        message: Original message content
        collector_id: Collector ID for responses
        request_id: Request ID
        recipient_count: Number of recipients
        timeout_seconds: Timeout in seconds
        
    Returns:
        Formatted message with instructions
    """
    timeout_minutes = timeout_seconds // 60
    return f"""{message}

---
📋 **MULTI-AGENT REQUEST** - Response Collection Active
---

**How to Respond:**
1. This is a MULTI-AGENT REQUEST - your response will be combined with other agents
2. Respond normally in this chat (your response will be collected automatically)
3. Collector ID: `{collector_id}`
4. Request ID: `{request_id}`
5. Waiting for {recipient_count} agent(s) to respond
6. Timeout: {timeout_minutes} minutes

**Response Format:**
Just type your response normally. The system will automatically:
- Collect your response
- Combine with other agents' responses
- Send 1 combined message to the sender

**Note:** This is different from normal messages - responses are collected and combined!
🐝 WE. ARE. SWARM. ⚡🔥"""


# Helper functions for category tracking and message processing
def _load_last_inbound_categories() -> Dict[str, str]:
    """Load last inbound message categories from persistent storage."""
    from pathlib import Path
    import json
    
    LAST_INBOUND_FILE = Path("runtime") / "last_inbound_category.json"
    try:
        if LAST_INBOUND_FILE.exists():
            with open(LAST_INBOUND_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    return data
    except Exception:
        import logging
        logger = logging.getLogger(__name__)
        logger.warning(
            "⚠️ Could not load last inbound categories", exc_info=True)
    return {}


def _save_last_inbound_categories(data: Dict[str, str]) -> None:
    """Save last inbound message categories to persistent storage."""
    from pathlib import Path
    import json
    
    LAST_INBOUND_FILE = Path("runtime") / "last_inbound_category.json"
    try:
        LAST_INBOUND_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(LAST_INBOUND_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except Exception:
        import logging
        logger = logging.getLogger(__name__)
        logger.warning(
            "⚠️ Could not persist last inbound categories", exc_info=True)


def _map_category_from_type(message_type: UnifiedMessageType) -> Optional[MessageCategory]:
    """Map UnifiedMessageType to MessageCategory."""
    if message_type == UnifiedMessageType.SYSTEM_TO_AGENT:
        return MessageCategory.S2A
    if message_type == UnifiedMessageType.CAPTAIN_TO_AGENT:
        return MessageCategory.C2A
    if message_type == UnifiedMessageType.AGENT_TO_AGENT:
        return MessageCategory.A2A
    return None


def _is_ack_text(message: str) -> bool:
    """Check if message is an acknowledgment."""
    text = (message or "").lower().strip()
    noise = ["ack", "ack.", "acknowledged", "resuming",
             "got it", "copy", "copy that", "noted"]
    return any(text == n or text.startswith(n + " ") for n in noise)


def _format_normal_message_with_instructions(message: str, message_type: str = "NORMAL") -> str:
    """
    Format normal message with response instructions.
    
    Args:
        message: Original message content
        message_type: Type of message (NORMAL, BROADCAST)
        
    Returns:
        Formatted message with instructions
    """
    if message_type == "BROADCAST":
        return f"""{message}

---
📨 **BROADCAST MESSAGE** - Standard Response
---

**How to Respond:**
1. This is a NORMAL/BROADCAST message
2. Respond directly in this chat (normal response, not collected)
3. Your response goes directly to the sender
4. No response collection - standard one-to-one messaging

**Response Format:**
Just type your response normally. It will be sent directly to the sender.

**Note:** This is a standard message - respond normally, no special handling needed!
🐝 WE. ARE. SWARM. ⚡🔥"""
    
    # Check if message is from Discord ([D2A])
    is_discord_message = (
        message.strip().startswith("[D2A]") or
        "\n[D2A]" in message or
        (message.startswith("[D2A]") and len(message) > 5)
    )

    if is_discord_message:
        return f"""{message}

---
📨 **DISCORD MESSAGE [D2A]** - Respond in Discord
---

**How to Respond:**
1. This is a DISCORD message ([D2A])
2. **CRITICAL**: Your response must be sent BACK to Discord
3. **Use Discord Router**: `python tools/post_to_discord_router.py --agent <your-agent-id> --message "<your response>"`
4. **Example**: `python tools/post_to_discord_router.py --agent Agent-4 --message "Response to Discord user"`
5. Do NOT just respond in this chat - Discord user is waiting for response in Discord

**Response Format:**
Post your response to Discord router channel using post_to_discord_router.py script.

**Note:** Discord messages [D2A] require responses to be posted back to Discord channel!
🐝 WE. ARE. SWARM. ⚡🔥"""
    
    return f"""{message}

---
📨 **STANDARD MESSAGE** - Normal Response
---

**How to Respond:**
1. This is a NORMAL message
2. Respond directly in this chat (normal response)
3. Your response goes directly to the sender
4. No response collection - standard one-to-one messaging

**Response Format:**
Just type your response normally. It will be sent directly to the sender.

**Note:** This is a standard message - respond normally, no special handling needed!
🐝 WE. ARE. SWARM. ⚡🔥"""



