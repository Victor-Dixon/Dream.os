#!/usr/bin/env python3
"""
Messaging Models - V2 Compliance Module
=======================================

<!-- SSOT Domain: integration -->

Core messaging models and enums.

Author: Agent-1 (Integration & Core Systems Specialist)
Created: 2025-10-11
License: MIT
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class DeliveryMethod(Enum):
    """Delivery methods for messages."""

    PYAUTOGUI = "pyautogui"
    INBOX = "inbox"
    BROADCAST = "broadcast"


class UnifiedMessageType(Enum):
    """Message types for unified messaging."""

    TEXT = "text"
    BROADCAST = "broadcast"
    ONBOARDING = "onboarding"
    AGENT_TO_AGENT = "agent_to_agent"
    CAPTAIN_TO_AGENT = "captain_to_agent"
    SYSTEM_TO_AGENT = "system_to_agent"
    HUMAN_TO_AGENT = "human_to_agent"
    MULTI_AGENT_REQUEST = "multi_agent_request"


class UnifiedMessagePriority(Enum):
    """Message priorities for unified messaging."""

    REGULAR = "regular"
    URGENT = "urgent"


class MessageCategory(Enum):
    """
    High-level routing categories for messaging templates.

    S2A = System-to-Agent control/ops/cycles (includes Debate system cycles)
    D2A = Discord-to-Agent human/command intake
    C2A = Captain-to-Agent directives
    A2A = Agent-to-Agent coordination
    A2C = Agent-to-Captain coordination and reporting
    """

    S2A = "s2a"
    D2A = "d2a"
    C2A = "c2a"
    A2A = "a2a"
    A2C = "a2c"


class UnifiedMessageTag(Enum):
    """Message tags for unified messaging."""

    CAPTAIN = "captain"
    ONBOARDING = "onboarding"
    WRAPUP = "wrapup"
    COORDINATION = "coordination"
    SYSTEM = "system"


class RecipientType(Enum):
    """Recipient types for unified messaging."""

    AGENT = "agent"
    CAPTAIN = "captain"
    SYSTEM = "system"
    HUMAN = "human"


class SenderType(Enum):
    """Sender types for unified messaging."""

    AGENT = "agent"
    CAPTAIN = "captain"
    SYSTEM = "system"
    HUMAN = "human"


class MessageStatus(Enum):
    """Message delivery status."""

    QUEUED = "queued"
    PENDING = "pending"
    DELIVERED = "delivered"
    FAILED = "failed"
    RETRYING = "retrying"
    EXPIRED = "expired"


@dataclass
class UnifiedMessage:
    """Core message structure for unified messaging."""

    content: str
    sender: str
    recipient: str
    message_type: UnifiedMessageType
    priority: UnifiedMessagePriority = UnifiedMessagePriority.REGULAR
    tags: list[UnifiedMessageTag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    message_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    category: MessageCategory = MessageCategory.S2A
    sender_type: SenderType = SenderType.SYSTEM
    recipient_type: RecipientType = RecipientType.AGENT


__all__ = [
    "DeliveryMethod",
    "UnifiedMessageType",
    "UnifiedMessagePriority",
    "MessageCategory",
    "UnifiedMessageTag",
    "RecipientType",
    "SenderType",
    "MessageStatus",
    "UnifiedMessage",
]

