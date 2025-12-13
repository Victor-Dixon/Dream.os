#!/usr/bin/env python3
"""
Coordination Handlers Module - Messaging Infrastructure
======================================================

<!-- SSOT Domain: integration -->

Extracted from messaging_infrastructure.py for V2 compliance.
Handles agent coordination, message routing, and multi-agent requests.

V2 Compliance | Author: Agent-1 | Date: 2025-12-13
"""

from __future__ import annotations

import logging
import time
from typing import Any, Dict, Optional

from src.core.constants.agent_constants import AGENT_LIST as SWARM_AGENTS
from src.core.messaging_core import (
    UnifiedMessagePriority,
    UnifiedMessageTag,
    UnifiedMessageType,
    send_message,
)
from src.core.messaging_models_core import MessageCategory
from src.utils.swarm_time import get_swarm_time_display

from .message_formatters import (
    CONSOLIDATION_MESSAGE_TEMPLATE,
    SURVEY_MESSAGE_TEMPLATE,
    _format_multi_agent_request_message,
    _format_normal_message_with_instructions,
    _is_ack_text,
    _load_last_inbound_categories,
    _map_category_from_type,
    _save_last_inbound_categories,
)

logger = logging.getLogger(__name__)


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

