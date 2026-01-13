#!/usr/bin/env python3
"""
Broadcast Handler - Messaging Infrastructure
============================================

<!-- SSOT Domain: integration -->

Handles broadcast message delivery to all agents via message queue.
Extracted from coordination_handlers.py for V2 compliance.

V2 Compliance | Author: Agent-1 | Date: 2025-12-14
"""

from __future__ import annotations

import logging
import time
from typing import Optional

from src.core.constants.agent_constants import AGENT_LIST as SWARM_AGENTS
from src.core.messaging_core import (
    UnifiedMessagePriority,
    UnifiedMessageTag,
    UnifiedMessageType,
    send_message,
)

from .broadcast_helpers import (
    build_broadcast_metadata,
    process_broadcast_agents,
    send_broadcast_fallback,
)
from .message_formatters import _format_normal_message_with_instructions

logger = logging.getLogger(__name__)


def broadcast_to_all(
    message: str,
    priority=UnifiedMessagePriority.REGULAR,
    stalled: bool = False,
    queue_repository=None,
) -> int:
    """
    Broadcast message to all agents via message queue.

    CRITICAL: All messages route through queue for proper PyAutoGUI orchestration.
    Queue processor ensures sequential delivery with keyboard locks.

    VALIDATION: Checks each recipient for pending multi-agent requests.
    Skips agents with pending requests to prevent queue buildup.

    Args:
        message: Message content
        priority: Message priority
        stalled: Use stalled delivery mode
        queue_repository: Queue repository instance (injected dependency)

    Returns:
        Number of messages successfully queued
    """
    try:
        from ...core.multi_agent_request_validator import get_multi_agent_validator
        from .broadcast_helpers import execute_broadcast_delivery

        validator = get_multi_agent_validator()
        return execute_broadcast_delivery(
            queue_repository, message, priority, stalled, validator
        )
    except Exception as e:
        logger.error(f"Error broadcasting message: {e}")
        return 0

