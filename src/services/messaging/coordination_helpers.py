#!/usr/bin/env python3
"""
Coordination Helpers Module - Messaging Infrastructure
======================================================

<!-- SSOT Domain: integration -->

Helper functions for message coordination extracted for V2 compliance.
Handles sender detection and message type determination.

V2 Compliance | Author: Agent-1 | Date: 2025-12-13
"""

from __future__ import annotations

import logging
import os
from pathlib import Path

from src.core.constants.agent_constants import AGENT_LIST as SWARM_AGENTS
from src.core.messaging_core import UnifiedMessageType

logger = logging.getLogger(__name__)


def detect_sender() -> str:
    """
    Detect actual sender from environment and context.

    Checks:
    1. AGENT_CONTEXT environment variable
    2. Current working directory for agent workspace
    3. Defaults to CAPTAIN if not detected

    Returns:
        Detected sender ID (Agent-X, CAPTAIN, SYSTEM, etc.)
    """
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

    # Default to Agent-4 (CAPTAIN)
    logger.debug("📍 No sender detected, defaulting to Agent-4 (CAPTAIN)")
    return "Agent-4"


def determine_message_type(sender: str, recipient: str) -> tuple[UnifiedMessageType, str]:
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
        # Normalize to "Agent-4" for clarity in templates (CAPTAIN is Agent-4)
        return UnifiedMessageType.CAPTAIN_TO_AGENT, "Agent-4"

    # System-to-Agent
    if sender_upper in ["SYSTEM", "DISCORD", "COMMANDER"]:
        return UnifiedMessageType.SYSTEM_TO_AGENT, sender

    # Human-to-Agent
    if sender_upper in ["HUMAN", "USER", "GENERAL"]:
        return UnifiedMessageType.HUMAN_TO_AGENT, sender

    # Default: System-to-Agent
    return UnifiedMessageType.SYSTEM_TO_AGENT, sender or "SYSTEM"



