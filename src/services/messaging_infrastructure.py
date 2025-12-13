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
import uuid

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

# Import formatter functions from message_formatters module
from .messaging.message_formatters import (
    _apply_template,
    _format_multi_agent_request_message,
    _format_normal_message_with_instructions,
    _is_ack_text,
    _load_last_inbound_categories,
    _map_category_from_type,
    _save_last_inbound_categories,
)

# Delivery modes for UI send


class SendMode:
    ENTER = "enter"
    CTRL_ENTER = "ctrl_enter"


# Formatter functions imported from message_formatters module (see imports above)
# Duplicate definitions removed - using imported versions

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
    
    # Queue management flags
    parser.add_argument(
        "--resend-failed",
        action="store_true",
        help="Resend failed messages from queue (resets failed messages to PENDING for retry)",
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


# CLI Handlers extracted to src/services/messaging/cli_handlers.py
# Import for backward compatibility
from .messaging.cli_handlers import (
    handle_cycle_v2_message,
    handle_message,
    handle_survey,
    handle_consolidation,
    handle_coordinates,
    handle_start_agents,
    handle_save,
    handle_leaderboard,
)


# Handler functions extracted to src/services/messaging/cli_handlers.py
# See imports above for backward compatibility


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
        """Initialize ConsolidatedMessagingService."""
        super().__init__()
        self.project_root = Path(__file__).parent.parent.parent
        self.messaging_cli = self.project_root / "src" / "services" / "messaging_cli.py"
        from ..core.message_queue import MessageQueue
        self.queue = MessageQueue()
        self.logger = logging.getLogger(__name__)

    def send_message(
        self,
        agent: str,
        message: str,
        priority: str = "regular",
        use_pyautogui: bool = True,
        stalled: bool = False,
        wait_for_delivery: bool = False,
        timeout: int = 30,
        apply_template: bool = True,
        message_category=None,
        discord_user_id: str | None = None,
    ) -> dict[str, Any]:
        """
        Send message to agent via message queue or subprocess.

        Args:
            agent: Target agent ID
            message: Message content
            priority: Message priority (regular/urgent)
            use_pyautogui: Use PyAutoGUI delivery
            stalled: Mark as stalled
            wait_for_delivery: Wait for delivery confirmation
            timeout: Delivery timeout
            apply_template: Apply message template
            message_category: Message category
            discord_user_id: Discord user ID

        Returns:
            Result dict with success status
        """
        # Resolve sender
        resolved_sender = MessageCoordinator._detect_sender()

        # Normalize priority
        priority_enum = (
            UnifiedMessagePriority.URGENT
            if priority == "urgent"
            else UnifiedMessagePriority.REGULAR
        )

        # Apply template if requested
        log_path = Path(r"d:\Agent_Cellphone_V2_Repository\.cursor\debug.log")
        # #region agent log
        try:
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(json.dumps({"id": f"log_{int(datetime.now().timestamp() * 1000)}_before_template", "timestamp": int(datetime.now().timestamp() * 1000), "location": "messaging_infrastructure.py:1466", "message": "Before template application", "data": {"apply_template": apply_template, "message_length": len(message), "message_preview": message[:100], "message_category": str(message_category) if message_category else None}, "sessionId": "debug-session", "runId": "run1", "hypothesisId": "B"}) + "\n")
        except: pass
        # #endregion
        templated_message = message
        if apply_template:
            category = message_category or MessageCategory.D2A
            templated_message = _apply_template(
                category=category,
                message=message,
                sender=resolved_sender,
                recipient=agent,
                priority=priority_enum,
                message_id=str(uuid.uuid4()),
                extra={},
            )
            # #region agent log
            try:
                message_count = templated_message.count(message)
                with open(log_path, "a", encoding="utf-8") as f:
                    f.write(json.dumps({"id": f"log_{int(datetime.now().timestamp() * 1000)}_after_template", "timestamp": int(datetime.now().timestamp() * 1000), "location": "messaging_infrastructure.py:1477", "message": "After template application", "data": {"templated_length": len(templated_message), "templated_preview": templated_message[:200], "original_in_templated": message in templated_message, "templated_ends_with_original": templated_message.endswith(message), "message_appears_count": message_count}, "sessionId": "debug-session", "runId": "run1", "hypothesisId": "B"}) + "\n")
            except: pass
            # #endregion
            # CRITICAL FIX: If templated message ends with original message, it was appended incorrectly
            # Remove the appended message (it should only be in {content} placeholder)
            if templated_message.endswith(message) and message_count > 1:
                # Message was appended - remove it
                templated_message = templated_message[:-len(message)].rstrip()
                # #region agent log
                try:
                    with open(log_path, "a", encoding="utf-8") as f:
                        f.write(json.dumps({"id": f"log_{int(datetime.now().timestamp() * 1000)}_removed_append", "timestamp": int(datetime.now().timestamp() * 1000), "location": "messaging_infrastructure.py:1485", "message": "Removed appended message from templated result", "data": {"new_length": len(templated_message)}, "sessionId": "debug-session", "runId": "run1", "hypothesisId": "B"}) + "\n")
                except: pass
                # #endregion

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
                    "sender": resolved_sender,
                    "discord_username": self._get_discord_username(discord_user_id) if discord_user_id else None,
                    "discord_user_id": discord_user_id if discord_user_id else None,
                    "recipient": agent,
                    "content": templated_message,
                    "priority": priority,
                    "source": "discord",
                    # CRITICAL FIX: Explicitly set message_type
                    "message_type": explicit_message_type,
                    "tags": [],
                    "metadata": {
                        "source": "discord",
                        "sender": resolved_sender,
                        "discord_username": self._get_discord_username(discord_user_id) if discord_user_id else None,
                        "discord_user_id": discord_user_id if discord_user_id else None,
                        "use_pyautogui": True,
                        "stalled": stalled,
                        "raw_message": message,
                        "message_category": (message_category or MessageCategory.D2A).value if apply_template else None,
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
            templated_message,
            "--priority",
            priority,
        ]

        if use_pyautogui:
            cmd.append("--pyautogui")

        # Set PYTHONPATH
        env = {"PYTHONPATH": str(self.project_root)}

        try:
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
            self.logger.error(f"Timeout sending message to {agent}")
            return {"success": False, "message": "Message timeout", "agent": agent}
        except Exception as e:
            self.logger.error(f"Error sending message to {agent}: {e}")
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
