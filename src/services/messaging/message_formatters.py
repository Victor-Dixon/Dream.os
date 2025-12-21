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

from src.core.messaging_core import (
    UnifiedMessagePriority,
    UnifiedMessageType,
)
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
    """Apply message template based on category."""
    from .template_helpers import prepare_a2a_template, prepare_d2a_template, prepare_default_template

    tmpl = MESSAGE_TEMPLATES.get(category)
    if not tmpl:
        return message
    
    now = datetime.now().isoformat(timespec="seconds")
    meta = extra or {}
    
    if category == MessageCategory.D2A:
        return prepare_d2a_template(tmpl, sender, recipient, priority, message_id, message, now, meta)
    
    if category == MessageCategory.A2A:
        return prepare_a2a_template(tmpl, sender, recipient, priority, message_id, message, now, meta)
    
    return prepare_default_template(tmpl, sender, recipient, priority, message_id, message, now)


def _format_multi_agent_request_message(
    message: str,
    collector_id: str,
    request_id: str,
    recipient_count: int,
    timeout_seconds: int
) -> str:
    """Format multi-agent request message with response instructions."""
    from .message_formatting_helpers import format_multi_agent_request_body
    timeout_minutes = timeout_seconds // 60
    return format_multi_agent_request_body(message, collector_id, request_id, recipient_count, timeout_minutes)


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
    """Format normal message with response instructions."""
    from .message_formatting_helpers import (
        format_broadcast_instructions,
        format_discord_instructions,
        format_normal_instructions,
        is_discord_message,
    )

    if message_type == "BROADCAST":
        return message + format_broadcast_instructions()
    
    if is_discord_message(message):
        return message + format_discord_instructions()
    
    return message + format_normal_instructions()



