#!/usr/bin/env python3
"""
Delivery Handlers Module - Messaging Infrastructure
===================================================

<!-- SSOT Domain: integration -->

Extracted from messaging_infrastructure.py for V2 compliance.
Handles message delivery via PyAutoGUI and inbox delivery modes.

V2 Compliance | Author: Agent-1 | Date: 2025-12-13
"""

from __future__ import annotations

from typing import Optional

from src.core.messaging_core import (
    UnifiedMessagePriority,
    UnifiedMessageTag,
    UnifiedMessageType,
    send_message,
)


def send_message_pyautogui(agent_id: str, message: str, timeout: int = 30) -> bool:
    """
    Send a message via PyAutoGUI using unified messaging core.
    
    Args:
        agent_id: Target agent ID
        message: Message content
        timeout: Timeout in seconds (default: 30)
        
    Returns:
        True if message sent successfully, False otherwise
    """
    return send_message(
        content=message,
        sender="CAPTAIN",
        recipient=agent_id,
        message_type=UnifiedMessageType.CAPTAIN_TO_AGENT,
        priority=UnifiedMessagePriority.REGULAR,
        tags=[UnifiedMessageTag.SYSTEM],
    )


def send_message_to_onboarding_coords(agent_id: str, message: str, timeout: int = 30) -> bool:
    """
    Alias for send_message_pyautogui to handle onboarding messaging.
    
    Sends message to agent's onboarding coordinates instead of regular chat coordinates.
    
    Args:
        agent_id: Target agent ID
        message: Message content
        timeout: Timeout in seconds (default: 30)
        
    Returns:
        True if message sent successfully, False otherwise
    """
    return send_message_pyautogui(agent_id, message, timeout)


# Delivery mode constants
class SendMode:
    """Delivery modes for UI send operations."""
    ENTER = "enter"
    CTRL_ENTER = "ctrl_enter"





