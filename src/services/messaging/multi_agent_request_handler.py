#!/usr/bin/env python3
"""
Multi-Agent Request Handler - Messaging Infrastructure
======================================================

<!-- SSOT Domain: integration -->

Handles multi-agent request creation and queuing.
Extracted from coordination_handlers.py for V2 compliance.

V2 Compliance | Author: Agent-1 | Date: 2025-12-14
"""

from __future__ import annotations

import logging
import uuid
from typing import Optional

from src.core.messaging_core import (
    UnifiedMessagePriority,
    UnifiedMessageTag,
    UnifiedMessageType,
)

from .message_formatters import _format_multi_agent_request_message

logger = logging.getLogger(__name__)


def send_multi_agent_request(
    recipients: list[str], message: str, sender: str = "CAPTAIN",
    priority=UnifiedMessagePriority.REGULAR, timeout_seconds: int = 300,
    wait_for_all: bool = False, stalled: bool = False, queue=None,
) -> str:
    """Send multi-agent request that collects responses and combines them."""
    try:
        from ...core.multi_agent_responder import get_multi_agent_responder
        from .multi_agent_request_helpers import (
            create_request_collector,
            process_multi_agent_request,
        )

        request_id = f"req_{uuid.uuid4().hex[:8]}"
        responder = get_multi_agent_responder()
        collector_id = create_request_collector(responder, request_id, sender, recipients, message, timeout_seconds, wait_for_all)
        return process_multi_agent_request(queue, sender, recipients, message, collector_id, request_id, priority, stalled, timeout_seconds)
    except Exception as e:
        logger.error(f"Error creating multi-agent request: {e}")
        return ""

