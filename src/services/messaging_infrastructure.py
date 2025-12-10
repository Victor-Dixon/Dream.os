#!/usr/bin/env python3
"""
UNIFIED MESSAGING INFRASTRUCTURE - Services Layer Consolidation
===============================================================

<!-- SSOT Domain: integration -->

Consolidates messaging CLI support (7 files → 1): parser, formatters, handlers, service adapters
V2 Compliance | Author: Agent-2 | Date: 2025-10-15
"""

from __future__ import annotations
from src.core.constants.agent_constants import AGENT_LIST as SWARM_AGENTS

import argparse
import json
import logging
import subprocess
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

from ..utils.swarm_time import get_swarm_time_display
from ..core.config.timeout_constants import TimeoutConstants
from ..core.base.base_service import BaseService

import pyautogui

from src.core.coordinate_loader import get_coordinate_loader
from src.core.gamification.autonomous_competition_system import get_competition_system
from src.core.messaging_core import (
    UnifiedMessagePriority,
    UnifiedMessageTag,
    UnifiedMessageType,
    send_message,
)
from src.core.messaging_models_core import (
    MessageCategory,
    MESSAGE_TEMPLATES,
    format_d2a_payload,
)

logger = logging.getLogger(__name__)

# Delivery modes for UI send


class SendMode:
    ENTER = "enter"
    CTRL_ENTER = "ctrl_enter"


# Persist lightweight category tracking for no-ack enforcement.
LAST_INBOUND_FILE = Path("runtime") / "last_inbound_category.json"


def _load_last_inbound_categories() -> Dict[str, str]:
    try:
        if LAST_INBOUND_FILE.exists():
            with open(LAST_INBOUND_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    return data
    except Exception:
        logger.warning(
            "⚠️ Could not load last inbound categories", exc_info=True)
    return {}


def _save_last_inbound_categories(data: Dict[str, str]) -> None:
    try:
        LAST_INBOUND_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(LAST_INBOUND_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except Exception:
        logger.warning(
            "⚠️ Could not persist last inbound categories", exc_info=True)


def _map_category_from_type(message_type: UnifiedMessageType) -> Optional[MessageCategory]:
    if message_type == UnifiedMessageType.SYSTEM_TO_AGENT:
        return MessageCategory.S2A
    if message_type == UnifiedMessageType.CAPTAIN_TO_AGENT:
        return MessageCategory.C2A
    if message_type == UnifiedMessageType.AGENT_TO_AGENT:
        return MessageCategory.A2A
    return None


def _is_ack_text(message: str) -> bool:
    text = (message or "").lower().strip()
    noise = ["ack", "ack.", "acknowledged", "resuming",
             "got it", "copy", "copy that", "noted"]
    return any(text == n or text.startswith(n + " ") for n in noise)


def _apply_template(
    category: MessageCategory,
    message: str,
    sender: str,
    recipient: str,
    priority: UnifiedMessagePriority,
    message_id: str,
    extra: Optional[Dict[str, Any]] = None,
) -> str:
    tmpl = MESSAGE_TEMPLATES.get(category)
    if not tmpl:
        return message
    now = datetime.now().isoformat(timespec="seconds")
    meta = extra or {}
    # D2A requires extra fields; use canonical formatter to avoid KeyErrors.
    if category == MessageCategory.D2A:
        d2a_payload = {
            k: v
            for k, v in {
                "interpretation": meta.get("interpretation"),
                "actions": meta.get("actions", message),
                "fallback": meta.get("fallback"),
                "discord_response_policy": meta.get("discord_response_policy"),
                "d2a_report_format": meta.get("d2a_report_format"),
            }.items()
            if v is not None
        }
        d2a_meta = format_d2a_payload(d2a_payload)
        return tmpl.format(
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
    else:
        # Check if message is from Discord ([D2A])
        # Discord messages start with [D2A] prefix or contain [D2A] in the header
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
        else:
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

# ============================================================================
# MESSAGE TEMPLATES & FORMATTERS
# ============================================================================


CLI_HELP_EPILOG = """
🐝 SWARM MESSAGING CLI - COMMAND YOUR AGENTS!
==============================================

EXAMPLES:
--------
# Send message to specific agent
python -m src.services.messaging_cli --message "Start survey" --agent Agent-1
# Broadcast to all agents
python -m src.services.messaging_cli --message "SWARM ALERT!" --broadcast
# Send with priority and tags
python -m src.services.messaging_cli --message "URGENT: Fix issue" \\
    --agent Agent-2 --priority urgent --tags bug critical

🐝 WE. ARE. SWARM - COORDINATE THROUGH PYAUTOGUI!
"""

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

AGENT_ASSIGNMENTS = {
    "Agent-1": "Service Layer Specialist - Analyze src/services/",
    "Agent-2": "Core Systems Architect - Analyze src/core/",
    "Agent-3": "Web & API Integration - Analyze src/web/ and src/infrastructure/",
    "Agent-4": "Domain & Quality Assurance - Cross-cutting analysis + coordination",
    "Agent-5": "Trading & Gaming Systems - Analyze specialized systems",
    "Agent-6": "Testing & Infrastructure - Analyze tests/ and tools/",
    "Agent-7": "Performance & Monitoring - Analyze monitoring components",
    "Agent-8": "Integration & Coordination - Analyze integration points",
}

# Use SSOT agent constants

# ============================================================================
# ARGUMENT PARSER
# ============================================================================


def create_messaging_parser() -> argparse.ArgumentParser:
    """Create the argument parser for messaging CLI."""
    parser = argparse.ArgumentParser(
        description="🐝 SWARM Messaging CLI - Command the swarm through PyAutoGUI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=CLI_HELP_EPILOG,
    )

    # Core messaging arguments
    parser.add_argument("--message", "-m", type=str,
                        help="Message content to send")

    parser.add_argument("--agent", "-a", type=str,
                        help="Target agent ID (e.g., Agent-1, Agent-2)")

    parser.add_argument(
        "--broadcast", "-b", action="store_true", help="Broadcast message to all agents"
    )

    # Message options
    parser.add_argument(
        "--priority",
        "-p",
        choices=["normal", "regular", "urgent"],
        default="regular",
        help="Message priority (default: regular). Accepts 'normal' or 'regular' (both are equivalent).",
    )

    parser.add_argument("--tags", "-t", nargs="+",
                        help="Message tags for categorization")

    # PyAutoGUI options
    parser.add_argument(
        "--pyautogui", "--gui", action="store_true", help="Use PyAutoGUI for message delivery"
    )

    # Survey coordination flags
    parser.add_argument(
        "--survey-coordination", action="store_true", help="Initiate survey coordination mode"
    )

    parser.add_argument(
        "--consolidation-coordination",
        action="store_true",
        help="Initiate consolidation coordination mode",
    )

    parser.add_argument("--consolidation-batch", type=str,
                        help="Specify consolidation batch ID")

    parser.add_argument(
        "--consolidation-status", type=str, help="Specify consolidation status update"
    )

    # Coordinate display
    parser.add_argument(
        "--coordinates", action="store_true", help="Display agent coordinates and configuration"
    )

    # Agent start flag
    parser.add_argument(
        "--start",
        nargs="+",
        type=int,
        metavar="N",
        help="Start agents (1-8, e.g., --start 1 2 3) - sends to onboarding coordinates",
    )

    parser.add_argument(
        "--save",
        action="store_true",
        help="Send message to all agents' chat input coords and press Ctrl+Enter to save",
    )

    parser.add_argument(
        "--leaderboard",
        action="store_true",
        help="Display the autonomous competition leaderboard",
    )

    # Task system flags (SSOT Blocker Resolution - Agent-8)
    parser.add_argument(
        "--get-next-task",
        action="store_true",
        help="Claim next available assigned task (requires --agent)",
    )

    parser.add_argument(
        "--list-tasks",
        action="store_true",
        help="List all available tasks in queue",
    )

    parser.add_argument(
        "--task-status",
        type=str,
        metavar="TASK_ID",
        help="Check status of specific task",
    )

    parser.add_argument(
        "--complete-task",
        type=str,
        metavar="TASK_ID",
        help="Mark task as complete",
    )

    # Hard onboarding flags
    parser.add_argument(
        "--hard-onboarding",
        action="store_true",
        help="Execute hard onboarding protocol (5-step reset) for agent",
    )

    parser.add_argument(
        "--onboarding-file",
        type=str,
        help="Path to file containing onboarding message (for hard onboarding)",
    )

    parser.add_argument(
        "--role",
        type=str,
        help="Agent role assignment (for hard onboarding with template)",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Dry run mode - show what would be done without executing",
    )

    # Cycle V2 flags
    parser.add_argument(
        "--cycle-v2",
        action="store_true",
        help="Use CYCLE_V2 template for high-throughput cycle (requires --agent and cycle fields)",
    )
    parser.add_argument(
        "--mission",
        type=str,
        help="Mission statement (single sentence) for CYCLE_V2",
    )
    parser.add_argument(
        "--dod",
        type=str,
        help="Definition of Done (3 bullets max, use \\n for newlines) for CYCLE_V2",
    )
    parser.add_argument(
        "--ssot-constraint",
        type=str,
        help="SSOT constraint (domain) for CYCLE_V2",
    )
    parser.add_argument(
        "--v2-constraint",
        type=str,
        help="V2 constraint (e.g., 'file <400 lines') for CYCLE_V2",
    )
    parser.add_argument(
        "--touch-surface",
        type=str,
        help="Touch surface (files/modules to be changed) for CYCLE_V2",
    )
    parser.add_argument(
        "--validation",
        type=str,
        help="Validation required (tests/lint commands) for CYCLE_V2",
    )
    parser.add_argument(
        "--priority-level",
        type=str,
        default="P1",
        help="Priority level (P0/P1) for CYCLE_V2 (default: P1)",
    )
    parser.add_argument(
        "--handoff",
        type=str,
        help="Handoff expectation (what 'done' looks like) for CYCLE_V2",
    )

    # Infrastructure health monitoring
    parser.add_argument(
        "--infra-health",
        action="store_true",
        help="Check infrastructure health metrics (disk, memory, CPU, browser automation)",
    )

    return parser


# ============================================================================
# MESSAGE HANDLERS
# ============================================================================


def send_message_pyautogui(agent_id: str, message: str, timeout: int = 30) -> bool:
    """Send a message via PyAutoGUI using unified messaging core."""
    return send_message(
        content=message,
        sender="CAPTAIN",
        recipient=agent_id,
        message_type=UnifiedMessageType.CAPTAIN_TO_AGENT,
        priority=UnifiedMessagePriority.REGULAR,
        tags=[UnifiedMessageTag.SYSTEM],
    )


def send_message_to_onboarding_coords(agent_id: str, message: str, timeout: int = 30) -> bool:
    """Alias for send_message_pyautogui to handle onboarding messaging."""
    return send_message_pyautogui(agent_id, message, timeout)


class MessageCoordinator:
    """Unified message coordination system - ALL messages route through queue."""

    _queue = None

    @classmethod
    def _get_queue(cls):
        """Lazy initialization of message queue."""
        if cls._queue is None:
            try:
                from ..core.message_queue import MessageQueue
                cls._queue = MessageQueue()
                logger.info(
                    "✅ MessageCoordinator initialized with message queue")
            except Exception as e:
                logger.error(f"⚠️ Failed to initialize message queue: {e}")
                cls._queue = None
        return cls._queue

    @staticmethod
    def send_to_agent(
        agent: str,
        message,
        priority=UnifiedMessagePriority.REGULAR,
        use_pyautogui=False,
        stalled: bool = False,
        send_mode: Optional[str] = None,
        sender: str = None,
        message_category: Optional[MessageCategory] = None,
        message_metadata: Optional[Dict[str, Any]] = None,
    ):
        """
        Send message to agent via message queue (prevents race conditions).

        CRITICAL: All messages route through queue for proper PyAutoGUI orchestration.
        Queue processor handles keyboard locks to prevent concurrent operations.

        VALIDATION: Checks if agent has pending multi-agent request and blocks if needed.

        Args:
            agent: Recipient agent ID
            message: Message content
            priority: Message priority
            use_pyautogui: Use PyAutoGUI delivery
            stalled: Use stalled delivery mode
            send_mode: Optional UI send mode override ("enter" | "ctrl_enter")
            sender: Optional sender ID (auto-detected if not provided)
        """
        try:
            # DETECT SENDER: Auto-detect if not provided
            if sender is None:
                sender = MessageCoordinator._detect_sender()

            # DETERMINE MESSAGE TYPE based on sender
            message_type, sender_final = MessageCoordinator._determine_message_type(
                sender, agent)
            category = message_category or _map_category_from_type(
                message_type)

            # Enforce no-ack policy: if sender is agent and last inbound was S2A, block ack/noise replies
            if sender_final.upper().startswith("AGENT-"):
                last_inbound = _load_last_inbound_categories()
                if last_inbound.get(sender_final) == MessageCategory.S2A.value and _is_ack_text(message):
                    logger.warning(
                        f"❌ Message blocked: ack/noise reply after S2A inbound for {sender_final}")
                    return {
                        "success": False,
                        "blocked": True,
                        "reason": "ack_blocked_after_s2a",
                        "agent": agent,
                    }

            # VALIDATION LAYER 1: Check if recipient has pending multi-agent request
            # This prevents messages from being queued when recipient can't respond
            from ..core.multi_agent_request_validator import get_multi_agent_validator

            validator = get_multi_agent_validator()
            # Check if RECIPIENT has pending request (agent is the recipient)
            can_send, error_message, pending_info = validator.validate_agent_can_send_message(
                agent_id=agent,  # Recipient to check
                target_recipient=None,  # Not responding to specific recipient
                message_content=message
            )

            if not can_send:
                logger.warning(
                    f"❌ Message blocked - recipient {agent} has pending multi-agent request"
                )
                # Return error with pending request details
                return {
                    "success": False,
                    "blocked": True,
                    "reason": "pending_multi_agent_request",
                    "error_message": error_message,
                    "agent": agent,
                    "pending_info": pending_info  # Include pending info for caller
                }

            queue = MessageCoordinator._get_queue()

            # If queue available, enqueue for sequential processing
            if queue:
                # Pass stalled flag in metadata for Ctrl+Enter behavior
                metadata = {
                    "stalled": stalled,
                    "use_pyautogui": use_pyautogui,
                    "send_mode": send_mode,
                }

                # If caller provided category, assume message is already rendered; skip legacy formatter
                if category:
                    metadata["message_category"] = category.value
                    message_text = str(message)
                else:
                    # Legacy path: format only if message is str
                    if isinstance(message, str):
                        message_text = _format_normal_message_with_instructions(
                            message, "NORMAL")
                    else:
                        message_text = str(message)

                formatted_message = message_text

                queue_id = queue.enqueue(
                    message={
                        "type": "agent_message",
                        "sender": sender_final,
                        "recipient": agent,
                        "content": formatted_message,
                        "priority": priority.value if hasattr(priority, "value") else str(priority),
                        "message_type": message_type.value,
                        "tags": [UnifiedMessageTag.SYSTEM.value],
                        "metadata": metadata,
                    }
                )

                logger.info(
                    f"✅ Message queued for {agent} (ID: {queue_id}): {message[:50]}..."
                )
                if category and agent.upper().startswith("AGENT-"):
                    last_inbound = _load_last_inbound_categories()
                    last_inbound[agent] = category.value
                    _save_last_inbound_categories(last_inbound)
                return {"success": True, "queue_id": queue_id, "agent": agent}
            else:
                # Fallback to direct send if queue unavailable (should not happen in production)
                logger.warning(
                    "⚠️ Queue unavailable, falling back to direct send")
                metadata = {"stalled": stalled, "send_mode": send_mode} if (
                    stalled or send_mode) else {}
                if category:
                    metadata["message_category"] = category.value
                    message_text = str(message)
                else:
                    if isinstance(message, str):
                        message_text = _format_normal_message_with_instructions(
                            message, "NORMAL")
                    else:
                        message_text = str(message)
                result = send_message(
                    content=message_text,
                    sender=sender_final,
                    recipient=agent,
                    message_type=message_type,
                    priority=priority,
                    tags=[UnifiedMessageTag.SYSTEM],
                    metadata=metadata,
                )
                if category and agent.upper().startswith("AGENT-"):
                    last_inbound = _load_last_inbound_categories()
                    last_inbound[agent] = category.value
                    _save_last_inbound_categories(last_inbound)
                return result
        except Exception as e:
            logger.error(f"Error sending message to {agent}: {e}")
            return False

    @staticmethod
    def send_multi_agent_request(
        recipients: list[str],
        message: str,
        sender: str = "CAPTAIN",
        priority=UnifiedMessagePriority.REGULAR,
        timeout_seconds: int = 300,
        wait_for_all: bool = False,
        stalled: bool = False
    ) -> str:
        """
        Send multi-agent request that collects responses and combines them.

        Creates a response collector, sends message to all recipients,
        and will deliver combined response when all agents respond (or timeout).

        Args:
            recipients: List of agent IDs to send to
            message: Message content
            sender: Message sender (default: CAPTAIN)
            priority: Message priority
            timeout_seconds: Maximum time to wait for responses
            wait_for_all: If True, wait for all responses; if False, send on timeout
            stalled: Whether to use stalled delivery mode

        Returns:
            Collector ID for tracking responses
        """
        try:
            from ..core.multi_agent_responder import get_multi_agent_responder
            import uuid

            # Create unique request ID
            request_id = f"req_{uuid.uuid4().hex[:8]}"

            # Create response collector
            responder = get_multi_agent_responder()
            collector_id = responder.create_request(
                request_id=request_id,
                sender=sender,
                recipients=recipients,
                content=message,
                timeout_seconds=timeout_seconds,
                wait_for_all=wait_for_all
            )

            # Send message to each recipient with collector ID in metadata
            queue = MessageCoordinator._get_queue()
            if queue:
                metadata = {
                    "stalled": stalled,
                    "use_pyautogui": True,
                    "collector_id": collector_id,
                    "request_id": request_id,
                    "is_multi_agent_request": True
                }

                priority_value = priority.value if hasattr(
                    priority, "value") else str(priority)

                # Format message with response instructions
                formatted_message = _format_multi_agent_request_message(
                    message, collector_id, request_id, len(
                        recipients), timeout_seconds
                )

                queue_ids = []
                for recipient in recipients:
                    queue_id = queue.enqueue(
                        message={
                            "type": "multi_agent_request",
                            "sender": sender,
                            "recipient": recipient,
                            "content": formatted_message,
                            "priority": priority_value,
                            "message_type": UnifiedMessageType.MULTI_AGENT_REQUEST.value,
                            "tags": [UnifiedMessageTag.COORDINATION.value],
                            "metadata": metadata,
                        }
                    )
                    queue_ids.append(queue_id)

                logger.info(
                    f"✅ Multi-agent request {collector_id} queued for {len(recipients)} agents"
                )
                return collector_id
            else:
                logger.error("Queue unavailable for multi-agent request")
                return ""

        except Exception as e:
            logger.error(f"Error creating multi-agent request: {e}")
            return ""

    @staticmethod
    def broadcast_to_all(
        message: str, priority=UnifiedMessagePriority.REGULAR, stalled: bool = False
    ):
        """
        Broadcast message to all agents via message queue.

        CRITICAL: All messages route through queue for proper PyAutoGUI orchestration.
        Queue processor ensures sequential delivery with keyboard locks.

        VALIDATION: Checks each recipient for pending multi-agent requests.
        Skips agents with pending requests to prevent queue buildup.
        """
        try:
            # VALIDATION LAYER 1: Check each recipient for pending requests
            from ..core.multi_agent_request_validator import get_multi_agent_validator

            validator = get_multi_agent_validator()

            queue = MessageCoordinator._get_queue()

            # If queue available, enqueue all messages for sequential processing
            if queue:
                metadata = {
                    "stalled": stalled,
                    "use_pyautogui": True,  # Always use PyAutoGUI for broadcasts
                }

                priority_value = priority.value if hasattr(
                    priority, "value") else str(priority)

                # Format message with response instructions for normal broadcast
                formatted_message = _format_normal_message_with_instructions(
                    message, "BROADCAST")

                # Enqueue messages for all agents (with validation)
                queue_ids = []
                skipped_agents = []
                for agent in SWARM_AGENTS:
                    # Check if recipient has pending multi-agent request
                    can_send, error_message, pending_info = validator.validate_agent_can_send_message(
                        agent_id=agent,  # Recipient to check
                        target_recipient=None,  # Not responding to specific recipient
                        message_content=message
                    )

                    if not can_send:
                        # Skip this agent - they have pending request
                        logger.warning(
                            f"⏭️  Skipping {agent} in broadcast - has pending multi-agent request"
                        )
                        skipped_agents.append({
                            "agent": agent,
                            "reason": "pending_multi_agent_request",
                            "error_message": error_message,
                            "pending_info": pending_info
                        })
                        continue
                    queue_id = queue.enqueue(
                        message={
                            "type": "agent_message",
                            "sender": "CAPTAIN",
                            "recipient": agent,
                            "content": formatted_message,
                            "priority": priority_value,
                            "message_type": UnifiedMessageType.BROADCAST.value,
                            "tags": [
                                UnifiedMessageTag.SYSTEM.value,
                                UnifiedMessageTag.COORDINATION.value,
                            ],
                            "metadata": metadata,
                        }
                    )
                    queue_ids.append(queue_id)

                # Log results including skipped agents
                if skipped_agents:
                    logger.warning(
                        f"⏭️  Broadcast skipped {len(skipped_agents)} agents with pending requests: "
                        f"{[a['agent'] for a in skipped_agents]}"
                    )

                logger.info(
                    f"✅ Broadcast queued for {len(queue_ids)} agents (skipped {len(skipped_agents)}): {message[:50]}..."
                )
                return len(queue_ids)
            else:
                # Fallback to direct send with keyboard lock if queue unavailable
                logger.warning(
                    "⚠️ Queue unavailable, falling back to direct broadcast")
                from ..core.keyboard_control_lock import keyboard_control

                with keyboard_control("broadcast_all_agents"):
                    metadata = {"stalled": stalled} if stalled else {}
                    success_count = 0
                    for agent in SWARM_AGENTS:
                        ok = send_message(
                            content=message,
                            sender="CAPTAIN",
                            recipient=agent,
                            message_type=UnifiedMessageType.BROADCAST,
                            priority=priority,
                            tags=[UnifiedMessageTag.SYSTEM,
                                  UnifiedMessageTag.COORDINATION],
                            metadata=metadata,
                        )
                        if ok:
                            success_count += 1
                            # Throttle to ensure UI/transport completes before next send
                            time.sleep(1.0)
                        else:
                            # Brief pause after failure to avoid rapid-fire retries
                            time.sleep(1.0)
                    return success_count
        except Exception as e:
            logger.error(f"Error broadcasting message: {e}")
            return 0

    @staticmethod
    def coordinate_survey():
        logger.info("🐝 INITIATING SWARM SURVEY COORDINATION...")
        success_count = MessageCoordinator.broadcast_to_all(
            SURVEY_MESSAGE_TEMPLATE, UnifiedMessagePriority.URGENT
        )
        if success_count > 0:
            logger.info(
                f"✅ Survey coordination broadcast to {success_count} agents")
            return True
        else:
            logger.error("❌ Survey coordination failed - no agents reached")
            return False

    @staticmethod
    def coordinate_consolidation(batch: str, status: str):
        message = CONSOLIDATION_MESSAGE_TEMPLATE.format(
            batch=batch or "DEFAULT",
            status=status or "IN_PROGRESS",
            timestamp=get_swarm_time_display(),
        )
        success_count = MessageCoordinator.broadcast_to_all(
            message, UnifiedMessagePriority.REGULAR)
        if success_count > 0:
            logger.info(
                f"✅ Consolidation update broadcast to {success_count} agents")
            return True
        else:
            logger.error("❌ Consolidation update failed")
            return False

    @staticmethod
    def _detect_sender() -> str:
        """
        Detect actual sender from environment and context.

        Checks:
        1. AGENT_CONTEXT environment variable
        2. Current working directory for agent workspace
        3. Defaults to CAPTAIN if not detected

        Returns:
            Detected sender ID (Agent-X, CAPTAIN, SYSTEM, etc.)
        """
        import os
        from pathlib import Path

        # Check environment variable first
        agent_context = os.getenv("AGENT_CONTEXT") or os.getenv("AGENT_ID")
        if agent_context:
            # Normalize to Agent-X format
            if agent_context.startswith("Agent-"):
                return agent_context
            elif agent_context.isdigit():
                return f"Agent-{agent_context}"
            else:
                return f"Agent-{agent_context}"

        # Check current working directory
        try:
            cwd = Path.cwd().as_posix()
            for agent_id in SWARM_AGENTS:
                if f"agent_workspaces/{agent_id}" in cwd or f"/{agent_id}/" in cwd:
                    logger.debug(
                        f"📍 Detected sender from directory: {agent_id}")
                    return agent_id
        except Exception as e:
            logger.debug(f"Could not detect sender from directory: {e}")

        # Default to CAPTAIN
        logger.debug("📍 No sender detected, defaulting to CAPTAIN")
        return "CAPTAIN"

    @staticmethod
    def _determine_message_type(sender: str, recipient: str) -> tuple[UnifiedMessageType, str]:
        """
        Determine message type and normalize sender based on sender/recipient.

        Args:
            sender: Detected or provided sender
            recipient: Message recipient

        Returns:
            Tuple of (message_type, normalized_sender)
        """
        sender_upper = sender.upper() if sender else ""
        recipient_upper = recipient.upper() if recipient else ""

        # Agent-to-Agent
        if sender and sender.startswith("Agent-") and recipient and recipient.startswith("Agent-"):
            return UnifiedMessageType.AGENT_TO_AGENT, sender

        # Agent-to-Captain
        if sender and sender.startswith("Agent-") and recipient_upper in ["CAPTAIN", "AGENT-4"]:
            return UnifiedMessageType.AGENT_TO_CAPTAIN, sender

        # Captain-to-Agent
        if sender_upper in ["CAPTAIN", "AGENT-4"]:
            return UnifiedMessageType.CAPTAIN_TO_AGENT, "CAPTAIN"

        # System-to-Agent
        if sender_upper in ["SYSTEM", "DISCORD", "COMMANDER"]:
            return UnifiedMessageType.SYSTEM_TO_AGENT, sender

        # Human-to-Agent
        if sender_upper in ["HUMAN", "USER", "GENERAL"]:
            return UnifiedMessageType.HUMAN_TO_AGENT, sender

        # Default: System-to-Agent
        return UnifiedMessageType.SYSTEM_TO_AGENT, sender or "SYSTEM"


def handle_cycle_v2_message(args, parser) -> int:
    """Handle CYCLE_V2 message sending with template."""
    try:
        if not args.agent:
            print("❌ ERROR: --agent required for --cycle-v2")
            parser.print_help()
            return 1

        # Validate required fields
        required_fields = {
            "mission": args.mission,
            "dod": args.dod,
            "ssot_constraint": args.ssot_constraint,
            "v2_constraint": args.v2_constraint,
            "touch_surface": args.touch_surface,
            "validation": args.validation,
            "handoff": args.handoff,
        }

        missing = [k for k, v in required_fields.items() if not v]
        if missing:
            print(
                f"❌ ERROR: Missing required CYCLE_V2 fields: {', '.join(missing)}")
            print("Required: --mission, --dod, --ssot-constraint, --v2-constraint, --touch-surface, --validation, --handoff")
            return 1

        # Normalize priority
        normalized_priority = "regular" if args.priority == "normal" else args.priority
        priority = (
            UnifiedMessagePriority.URGENT
            if normalized_priority == "urgent"
            else UnifiedMessagePriority.REGULAR
        )

        # Render CYCLE_V2 template (stored in S2A templates but used for C2A)
        from src.core.messaging_models_core import MessageCategory, MESSAGE_TEMPLATES

        # Get CYCLE_V2 template from S2A templates
        cycle_v2_template = MESSAGE_TEMPLATES.get(
            MessageCategory.S2A, {}).get("CYCLE_V2")

        if not cycle_v2_template:
            print("❌ ERROR: CYCLE_V2 template not found")
            return 1

        # Format template directly
        message_id = f"msg_{int(time.time() * 1000)}"
        timestamp = datetime.now().isoformat()

        # Replace \n in dod with actual newlines
        dod = args.dod.replace("\\n", "\n") if args.dod else ""

        rendered = cycle_v2_template.format(
            sender="Captain Agent-4",
            recipient=args.agent,
            priority=priority.value if hasattr(
                priority, "value") else str(priority),
            message_id=message_id,
            timestamp=timestamp,
            mission=args.mission,
            dod=dod,
            ssot_constraint=args.ssot_constraint,
            v2_constraint=args.v2_constraint,
            touch_surface=args.touch_surface,
            validation_required=args.validation,
            priority_level=args.priority_level or "P1",
            handoff_expectation=args.handoff,
            fallback="Escalate to Captain if blocked with proposed fix"
        )

        # Send via MessageCoordinator
        result = MessageCoordinator.send_to_agent(
            args.agent,
            rendered,
            priority,
            stalled=getattr(args, "stalled", False),
            message_category=MessageCategory.C2A
        )

        if isinstance(result, dict) and result.get("success"):
            print(f"✅ CYCLE_V2 message sent to {args.agent}")
            print(f"   Mission: {args.mission[:50]}...")
            return 0
        else:
            print(f"❌ Failed to send CYCLE_V2 message to {args.agent}")
            return 1

    except Exception as e:
        logger.error(f"CYCLE_V2 message handling error: {e}")
        import traceback
        traceback.print_exc()
        return 1


def handle_message(args, parser) -> int:
    """Handle message sending."""
    try:
        # Check for cycle-v2 flag first
        if getattr(args, "cycle_v2", False):
            return handle_cycle_v2_message(args, parser)

        if not args.agent and not args.broadcast:
            print("❌ ERROR: Either --agent or --broadcast must be specified")
            parser.print_help()
            return 1

        # Normalize "normal" to "regular" for consistency
        normalized_priority = "regular" if args.priority == "normal" else args.priority

        priority = (
            UnifiedMessagePriority.URGENT
            if normalized_priority == "urgent"
            else UnifiedMessagePriority.REGULAR
        )

        # Get stalled flag from args (defaults to False if not present)
        stalled = getattr(args, "stalled", False)

        if args.broadcast:
            success_count = MessageCoordinator.broadcast_to_all(
                args.message, priority, stalled=stalled
            )
            if success_count > 0:
                print(f"✅ Broadcast to {success_count} agents successful")
                return 0
            else:
                print("❌ Broadcast failed")
                return 1
        else:
            result = MessageCoordinator.send_to_agent(
                args.agent, args.message, priority, stalled=stalled
            )

            # Check if result is dict (new format) or bool (old format)
            if isinstance(result, dict):
                if result.get("success"):
                    print(f"✅ Message sent to {args.agent}")
                    return 0
                elif result.get("blocked"):
                    # Message blocked - show pending request
                    print("❌ MESSAGE BLOCKED - Pending Multi-Agent Request")
                    print()
                    print(result.get("error_message",
                          "Pending request details unavailable"))
                    return 1
                else:
                    print(f"❌ Failed to send message to {args.agent}")
                    return 1
            elif result:
                # Old format (bool) - success
                print(f"✅ Message sent to {args.agent}")
                return 0
            else:
                print(f"❌ Failed to send message to {args.agent}")
                return 1

    except Exception as e:
        logger.error(f"Message handling error: {e}")
        return 1


def handle_survey() -> int:
    """Handle survey coordination initiation."""
    try:
        if MessageCoordinator.coordinate_survey():
            print("✅ Survey coordination initiated successfully")
            return 0
        else:
            print("❌ Survey coordination failed")
            return 1
    except Exception as e:
        logger.error(f"Survey coordination error: {e}")
        return 1


def handle_consolidation(args) -> int:
    """Handle consolidation coordination."""
    try:
        if MessageCoordinator.coordinate_consolidation(
            args.consolidation_batch, args.consolidation_status
        ):
            print("✅ Consolidation coordination successful")
            return 0
        else:
            print("❌ Consolidation coordination failed")
            return 1
    except Exception as e:
        logger.error(f"Consolidation coordination error: {e}")
        return 1


def handle_coordinates() -> int:
    """Display agent coordinates."""
    try:
        coord_loader = get_coordinate_loader()
        print("\n🐝 SWARM AGENT COORDINATES")
        print("=" * 50)
        for agent in SWARM_AGENTS:
            chat_coords = coord_loader.get_chat_coordinates(agent)
            onboard_coords = coord_loader.get_onboarding_coordinates(agent)
            print(f"\n{agent}:")
            print(f"  Chat:      {chat_coords}")
            print(f"  Onboarding: {onboard_coords}")
        print("\n" + "=" * 50)
        return 0
    except Exception as e:
        logger.error(f"Coordinates display error: {e}")
        return 1


def handle_start_agents(args) -> int:
    """Handle starting agents via onboarding coordinates."""
    try:
        agent_numbers = args.start
        message = args.message if hasattr(
            args, "message") and args.message else "START"

        for num in agent_numbers:
            agent_id = f"Agent-{num}"
            if agent_id not in SWARM_AGENTS:
                print(f"⚠️  Invalid agent: {agent_id}")
                continue

            if send_message_to_onboarding_coords(agent_id, message):
                print(f"✅ Started {agent_id}")
            else:
                print(f"❌ Failed to start {agent_id}")

        return 0
    except Exception as e:
        logger.error(f"Start agents error: {e}")
        return 1


def handle_save(args, parser) -> int:
    """Handle save operation (Ctrl+Enter to all agents)."""
    try:
        if not args.message:
            print("❌ ERROR: --message required for save operation")
            return 1

        coord_loader = get_coordinate_loader()
        for agent in SWARM_AGENTS:
            try:
                chat_coords = coord_loader.get_chat_coordinates(agent)
                pyautogui.click(chat_coords[0], chat_coords[1])
                time.sleep(0.2)
                pyautogui.write(args.message, interval=0.01)
                pyautogui.hotkey("ctrl", "enter")
                print(f"✅ Saved to {agent}")
                time.sleep(0.5)
            except Exception as e:
                print(f"❌ Failed to save to {agent}: {e}")

        return 0
    except Exception as e:
        logger.error(f"Save operation error: {e}")
        return 1


def handle_leaderboard() -> int:
    """Display the autonomous competition leaderboard."""
    try:
        competition_system = get_competition_system()
        leaderboard = competition_system.get_leaderboard()

        print("\n🏆 AUTONOMOUS COMPETITION LEADERBOARD")
        print("=" * 60)
        for rank, entry in enumerate(leaderboard, start=1):
            agent = entry["agent_id"]
            score = entry["score"]
            completed = entry.get("contracts_completed", 0)
            print(f"{rank}. {agent:10s} - {score:5d} pts ({completed} contracts)")
        print("=" * 60)
        return 0
    except Exception as e:
        logger.error(f"Leaderboard error: {e}")
        print("❌ Failed to display leaderboard")
        return 1


# ============================================================================
# SERVICE ADAPTERS (formerly messaging_service.py, messaging_discord.py)
# ============================================================================


class ConsolidatedMessagingService(BaseService):
    """
    Consolidated messaging service adapter for Discord bot.

    CRITICAL UPDATE (2025-01-27): Uses message queue for synchronization
    Prevents race conditions when Discord + computer + agents send messages.
    All messages go through queue for sequential delivery with global lock.
    """

    def __init__(self):
        """Initialize messaging service."""
        super().__init__("ConsolidatedMessagingService")
        self.project_root = Path(__file__).parent.parent.parent
        self.messaging_cli = self.project_root / \
            "src" / "services" / "messaging_cli.py"

        # CRITICAL: Initialize message queue for synchronization
        try:
            from src.core.message_queue import MessageQueue

            self.queue = MessageQueue()
            self.logger.info(
                "✅ ConsolidatedMessagingService initialized with message queue")
        except Exception as e:
            self.logger.error(f"⚠️ Failed to initialize message queue: {e}")
            self.queue = None

    def send_message(
        self,
        agent: str,
        message: str,
        priority: str = "regular",
        use_pyautogui: bool = True,
        wait_for_delivery: bool = False,
        timeout: float = 30.0,
        discord_user_id: str | None = None,
        stalled: bool = False
    ) -> dict[str, Any]:
        """
        Send message to agent via message queue (synchronized delivery).

        VALIDATION: Checks if agent has pending multi-agent request.
        If pending, blocks message and returns error with pending request details.

        CRITICAL: All messages go through queue to prevent race conditions.
        Discord + computer + agents synchronized through global keyboard lock.

        Args:
            agent: Target agent ID (e.g., "Agent-1")
            message: Message content
            priority: Message priority ("regular" or "urgent")
            use_pyautogui: Whether to use PyAutoGUI delivery (default: True)
            wait_for_delivery: Wait for message to be delivered before returning (default: False)
            timeout: Maximum time to wait for delivery in seconds (default: 30.0)
            discord_user_id: Discord user ID for username resolution (optional)
            stalled: Whether to use stalled delivery mode

        Returns:
            Dictionary with success status and queue ID, or blocked status with error message
        """
        try:
            # Validate agent can receive messages (check for pending multi-agent requests)
            from ..core.multi_agent_request_validator import get_multi_agent_validator

            validator = get_multi_agent_validator()
            can_send, error_message, pending_info = validator.validate_agent_can_send_message(
                agent_id=agent,
                target_recipient=None,  # Not checking recipient, just blocking if pending
                message_content=message
            )

            if not can_send:
                # Agent has pending request - block and return error
                self.logger.warning(
                    f"❌ Message blocked for {agent} - pending multi-agent request"
                )
                return {
                    "success": False,
                    "blocked": True,
                    "reason": "pending_multi_agent_request",
                    "error_message": error_message,
                    "agent": agent,
                    "pending_request_message": error_message,  # Full error with pending request
                    "pending_info": pending_info  # Include pending request data
                }
            # CRITICAL: Use message queue for PyAutoGUI delivery (synchronized delivery)
            # This ensures sequential delivery with global keyboard lock
            if self.queue and use_pyautogui:
                # Determine message type explicitly for Discord messages
                # CRITICAL FIX: Always use HUMAN_TO_AGENT for Discord messages (never ONBOARDING)
                # Only onboarding commands (!hard onboard, !soft onboard, !start) should use ONBOARDING type
                # Regular Discord messages should ALWAYS use HUMAN_TO_AGENT to route to chat input coords
                from ..core.messaging_models_core import UnifiedMessageType

                # Check if this is an onboarding command (hard onboard, soft onboard, start)
                import re
                message_lower = message.lower().strip()

                # More specific matching: only match "start" when followed by agent identifier
                is_onboarding_command = (
                    "hard onboard" in message_lower or
                    "soft onboard" in message_lower or
                    message_lower.startswith("!start") or
                    # Only match "start Agent-X" or "start X" where X is 1-8 (not generic "start")
                    bool(
                        re.match(r'^start\s+(agent-)?[1-8](\s|$)', message_lower, re.IGNORECASE))
                )

                # Set message_type explicitly: ONBOARDING only for onboarding commands, HUMAN_TO_AGENT for all others
                if is_onboarding_command:
                    explicit_message_type = UnifiedMessageType.ONBOARDING.value
                else:
                    # CRITICAL: Regular Discord messages ALWAYS use HUMAN_TO_AGENT (routes to chat input coords)
                    explicit_message_type = UnifiedMessageType.HUMAN_TO_AGENT.value

                # Enqueue message for sequential processing
                queue_id = self.queue.enqueue(
                    message={
                        "type": "agent_message",
                        "sender": self._resolve_discord_sender(discord_user_id) if discord_user_id else "DISCORD",
                        "discord_username": self._get_discord_username(discord_user_id) if discord_user_id else None,
                        "discord_user_id": discord_user_id if discord_user_id else None,
                        "recipient": agent,
                        "content": message,
                        "priority": priority,
                        "source": "discord",
                        # CRITICAL FIX: Explicitly set message_type
                        "message_type": explicit_message_type,
                        "tags": [],
                        "metadata": {
                            "source": "discord",
                            "sender": self._resolve_discord_sender(discord_user_id) if discord_user_id else "DISCORD",
                            "discord_username": self._get_discord_username(discord_user_id) if discord_user_id else None,
                            "discord_user_id": discord_user_id if discord_user_id else None,
                            "use_pyautogui": True,
                            "stalled": stalled,
                        },
                    }
                )

                self.logger.info(
                    f"✅ Message queued for {agent} (ID: {queue_id}): {message[:50]}..."
                )

                # CRITICAL: Wait for delivery if requested (blocking mode)
                if wait_for_delivery:
                    self.logger.debug(
                        f"⏳ Waiting for message {queue_id} delivery...")
                    delivered = self.queue.wait_for_delivery(
                        queue_id, timeout=timeout)
                    if delivered:
                        self.logger.info(
                            f"✅ Message {queue_id} delivered successfully")
                        return {
                            "success": True,
                            "message": f"Message delivered to {agent}",
                            "agent": agent,
                            "queue_id": queue_id,
                            "delivered": True,
                        }
                    else:
                        self.logger.warning(
                            f"⚠️ Message {queue_id} delivery failed or timeout")
                        return {
                            "success": False,
                            "message": f"Message delivery failed or timeout for {agent}",
                            "agent": agent,
                            "queue_id": queue_id,
                            "delivered": False,
                        }

                # Non-blocking: return immediately after enqueue
                return {
                    "success": True,
                    "message": f"Message queued for {agent}",
                    "agent": agent,
                    "queue_id": queue_id,
                }

            # Fallback to subprocess if queue not available
            cmd = [
                "python",
                str(self.messaging_cli),
                "--agent",
                agent,
                "--message",
                message,
                "--priority",
                priority,
            ]

            if use_pyautogui:
                cmd.append("--pyautogui")

            # Set PYTHONPATH
            env = {"PYTHONPATH": str(self.project_root)}

            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=TimeoutConstants.HTTP_DEFAULT, env=env, cwd=str(self.project_root)
            )

            if result.returncode == 0:
                self.logger.info(f"Message sent to {agent}: {message[:50]}...")
                return {"success": True, "message": f"Message sent to {agent}", "agent": agent}
            else:
                error_msg = result.stderr or "Unknown error"
                self.logger.error(
                    f"Failed to send message to {agent}: {error_msg}")
                return {
                    "success": False,
                    "message": f"Failed to send message: {error_msg}",
                    "agent": agent,
                }

        except subprocess.TimeoutExpired:
            logger.error(f"Timeout sending message to {agent}")
            return {"success": False, "message": "Message timeout", "agent": agent}
        except Exception as e:
            logger.error(f"Error sending message to {agent}: {e}")
            return {"success": False, "message": str(e), "agent": agent}

    def broadcast_message(self, message: str, priority: str = "regular") -> dict[str, Any]:
        """
        Broadcast message to all agents.

        CRITICAL: Wraps entire operation in keyboard lock to prevent conflicts.
        All 8 messages must complete before other operations can proceed.

        Args:
            message: Message content
            priority: Message priority

        Returns:
            Dictionary with success status
        """
        from ..core.keyboard_control_lock import keyboard_control

        # Get list of all agents (SSOT)
        from src.core.constants.agent_constants import AGENT_LIST
        agents = AGENT_LIST

        # CRITICAL: Wrap entire broadcast in keyboard lock
        # Prevents Discord/other sends during 8-message operation
        # Also wait for each message to be delivered before next one
        with keyboard_control("broadcast_operation"):
            results = []
            for agent in agents:
                # CRITICAL: Wait for each message to be delivered before sending next
                # This ensures proper sequential delivery even within the broadcast operation
                result = self.send_message(
                    agent,
                    message,
                    priority,
                    use_pyautogui=True,
                    wait_for_delivery=True,  # Block until delivered
                    timeout=TimeoutConstants.HTTP_DEFAULT  # 30 second timeout per message
                )
                results.append(result)

                # Small delay between agents for stability
                import time
                time.sleep(0.5)

            success_count = sum(1 for r in results if r.get("success"))
            delivered_count = sum(
                1 for r in results if r.get("delivered", False))

            logger.info(
                f"✅ Broadcast complete: {success_count}/{len(agents)} queued, "
                f"{delivered_count}/{len(agents)} delivered "
                f"(locked during entire operation to prevent conflicts)"
            )

            return {
                "success": success_count > 0,
                "message": f"Broadcast to {success_count}/{len(agents)} agents ({delivered_count} delivered)",
                "results": results,
            }
        """
        Detect actual sender from environment and context.
        
        Checks:
        1. AGENT_CONTEXT environment variable
        2. Current working directory for agent workspace
        3. Defaults to CAPTAIN if not detected
        
        Returns:
            Detected sender ID (Agent-X, CAPTAIN, SYSTEM, etc.)
        """
        import os
        from pathlib import Path

        # Check environment variable first
        agent_context = os.getenv("AGENT_CONTEXT") or os.getenv("AGENT_ID")
        if agent_context:
            # Normalize to Agent-X format
            if agent_context.startswith("Agent-"):
                return agent_context
            elif agent_context.isdigit():
                return f"Agent-{agent_context}"
            else:
                return f"Agent-{agent_context}"

        # Check current working directory
        try:
            cwd = Path.cwd().as_posix()
            for agent_id in SWARM_AGENTS:
                if f"agent_workspaces/{agent_id}" in cwd or f"/{agent_id}/" in cwd:
                    logger.debug(
                        f"📍 Detected sender from directory: {agent_id}")
                    return agent_id
        except Exception as e:
            logger.debug(f"Could not detect sender from directory: {e}")

        # Default to CAPTAIN
        logger.debug("📍 No sender detected, defaulting to CAPTAIN")
        return "CAPTAIN"

    @staticmethod
    def _determine_message_type(sender: str, recipient: str) -> tuple[UnifiedMessageType, str]:
        """
        Determine message type and normalize sender based on sender/recipient.

        Args:
            sender: Detected or provided sender
            recipient: Message recipient

        Returns:
            Tuple of (message_type, normalized_sender)
        """
        sender_upper = sender.upper() if sender else ""
        recipient_upper = recipient.upper() if recipient else ""

        # Agent-to-Agent
        if sender.startswith("Agent-") and recipient.startswith("Agent-"):
            return UnifiedMessageType.AGENT_TO_AGENT, sender

        # Agent-to-Captain
        if sender.startswith("Agent-") and recipient_upper in ["CAPTAIN", "AGENT-4"]:
            return UnifiedMessageType.AGENT_TO_CAPTAIN, sender

        # Captain-to-Agent
        if sender_upper in ["CAPTAIN", "AGENT-4"]:
            return UnifiedMessageType.CAPTAIN_TO_AGENT, "CAPTAIN"

        # System-to-Agent
        if sender_upper in ["SYSTEM", "DISCORD", "COMMANDER"]:
            return UnifiedMessageType.SYSTEM_TO_AGENT, sender

        # Human-to-Agent
        if sender_upper in ["HUMAN", "USER", "GENERAL"]:
            return UnifiedMessageType.HUMAN_TO_AGENT, sender

        # Default: System-to-Agent
        return UnifiedMessageType.SYSTEM_TO_AGENT, sender or "SYSTEM"

    def _get_discord_username(self, discord_user_id: str | None) -> str | None:
        """
        Get Discord username from user ID.

        Args:
            discord_user_id: Discord user ID

        Returns:
            Username string or None
        """
        if not discord_user_id:
            return None
        # For now, return None
        # In production, this could resolve to actual Discord username via API
        return None


# Discord integration adapter
def send_discord_message(agent: str, message: str, priority: str = "regular") -> bool:
    """Send message via Discord integration (wraps ConsolidatedMessagingService)."""
    service = ConsolidatedMessagingService()
    result = service.send_message(
        agent, message, priority, use_pyautogui=False)
    return result.get("success", False)


def broadcast_discord_message(message: str, priority: str = "regular") -> dict[str, Any]:
    """Broadcast message via Discord integration."""
    service = ConsolidatedMessagingService()
    return service.broadcast_message(message, priority)
