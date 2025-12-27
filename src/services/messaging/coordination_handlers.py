#!/usr/bin/env python3
"""
Coordination Handlers Module - Messaging Infrastructure
======================================================

<!-- SSOT Domain: integration -->

Orchestrator for agent coordination, message routing, and multi-agent requests.
Delegates to specialized handlers for V2 compliance.

V2 Compliance | Author: Agent-1 | Date: 2025-12-14
"""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional

from src.core.messaging_core import UnifiedMessagePriority
from src.core.messaging_models_core import MessageCategory
from src.utils.swarm_time import get_swarm_time_display

from .broadcast_handler import broadcast_to_all as _broadcast_to_all
from .message_formatters import (
    CONSOLIDATION_MESSAGE_TEMPLATE,
    SURVEY_MESSAGE_TEMPLATE,
)
from .agent_message_handler import send_to_agent as _send_to_agent
from .multi_agent_request_handler import send_multi_agent_request as _send_multi_agent_request

logger = logging.getLogger(__name__)


class MessageCoordinator:
    """Unified message coordination system - ALL messages route through queue repository."""

    _queue_repository = None

    @classmethod
    def _get_queue(cls):
        """
        Lazy initialization of queue repository.
        
        Returns queue repository if available, None if initialization fails.
        When None is returned, handlers will fall back to direct send.
        """
        if cls._queue_repository is None:
            try:
                from .repositories.queue_repository import QueueRepository
                cls._queue_repository = QueueRepository()
                logger.info(
                    "✅ MessageCoordinator initialized with queue repository")
            except Exception as e:
                logger.warning(
                    f"⚠️ Failed to initialize queue repository: {e}. "
                    "Messages will be sent directly (fallback mode). "
                    "Note: Queue processor must be running for queued delivery.")
                cls._queue_repository = None
        return cls._queue_repository

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

        Includes coordination throttling for A2A messages to prevent spam.

        Delegates to agent_message_handler for V2 compliance.
        """
        # Check coordination throttling for A2A messages
        if message_category == MessageCategory.A2A and sender:
            from src.services.coordination.coordination_throttler import get_coordination_throttler
            throttler = get_coordination_throttler()

            can_send, reason, wait_seconds = throttler.can_send_coordination(agent, sender)
            if not can_send:
                logger.warning(f"Coordination throttled: {sender} -> {agent}: {reason}")
                return {
                    "success": False,
                    "throttled": True,
                    "reason": reason,
                    "wait_seconds": wait_seconds
                }

        queue_repository = MessageCoordinator._get_queue()
        result = _send_to_agent(
            agent=agent,
            message=message,
            priority=priority,
            use_pyautogui=use_pyautogui,
            stalled=stalled,
            send_mode=send_mode,
            sender=sender,
            message_category=message_category,
            message_metadata=message_metadata,
            queue_repository=queue_repository,
            detect_sender_func=MessageCoordinator._detect_sender,
            determine_message_type_func=MessageCoordinator._determine_message_type,
        )

        # Record coordination for throttling if it was sent successfully
        if (result and result.get("success") and message_category == MessageCategory.A2A and sender):
            from src.services.coordination.coordination_throttler import get_coordination_throttler
            throttler = get_coordination_throttler()
            throttler.record_coordination(agent, sender)
        
        return result

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

        Delegates to multi_agent_request_handler for V2 compliance.
        """
        queue_repository = MessageCoordinator._get_queue()
        return _send_multi_agent_request(
            recipients=recipients,
            message=message,
            sender=sender,
            priority=priority,
            timeout_seconds=timeout_seconds,
            wait_for_all=wait_for_all,
            stalled=stalled,
            queue_repository=queue_repository,
        )

    @staticmethod
    def broadcast_to_all(
        message: str, priority=UnifiedMessagePriority.REGULAR, stalled: bool = False
    ):
        """
        Broadcast message to all agents via message queue.

        Delegates to broadcast_handler for V2 compliance.
        """
        queue_repository = MessageCoordinator._get_queue()
        return _broadcast_to_all(
            message=message,
            priority=priority,
            stalled=stalled,
            queue_repository=queue_repository,
        )

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
        """Detect actual sender from environment and context."""
        from .coordination_helpers import detect_sender
        return detect_sender()

    @staticmethod
    def _determine_message_type(sender: str, recipient: str) -> tuple[UnifiedMessageType, str]:
        """Determine message type and normalize sender based on sender/recipient."""
        from .coordination_helpers import determine_message_type
        return determine_message_type(sender, recipient)

