#!/usr/bin/env python3
"""
Activity Detector Models
========================

<!-- SSOT Domain: infrastructure -->

Data models and enums for activity detection system.
Extracted from hardened_activity_detector.py for V2 compliance.

V2 Compliance | Author: Agent-3 | Date: 2025-12-14
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Dict, Any, List, Optional
from datetime import datetime


class ActivityConfidence(Enum):
    """Confidence levels for activity detection."""
    VERY_HIGH = 0.9  # Multiple tier-1 sources agree
    HIGH = 0.7  # Single tier-1 source or multiple tier-2
    MEDIUM = 0.5  # Single tier-2 source
    LOW = 0.3  # Weak signal, needs validation
    VERY_LOW = 0.1  # Unreliable signal


class ActivitySource(Enum):
    """Activity source types with reliability tiers."""
    # Tier 1: Most reliable (direct agent actions)
    TELEMETRY_EVENT = (1, 0.9)  # ActivityEmitter events
    GIT_COMMIT = (1, 0.85)  # Git commits with agent name
    CONTRACT_CLAIMED = (1, 0.85)  # Contract system activity
    TEST_EXECUTION = (1, 0.8)  # Test runs
    
    # Tier 2: Reliable (file modifications)
    STATUS_UPDATE = (2, 0.7)  # status.json with meaningful content
    FILE_MODIFICATION = (2, 0.65)  # Workspace file changes
    DEVLOG_CREATED = (2, 0.7)  # Devlog creation
    INBOX_PROCESSING = (2, 0.6)  # Inbox message processing
    
    # Tier 3: Less reliable (indirect signals)
    MESSAGE_QUEUE = (3, 0.4)  # Message queue activity
    WORKSPACE_ACCESS = (3, 0.3)  # File access patterns
    
    def __init__(self, tier: int, base_confidence: float):
        """Initialize activity source with tier and confidence."""
        self.tier = tier
        self.base_confidence = base_confidence


@dataclass
class ActivitySignal:
    """Detected activity signal with metadata."""
    source: ActivitySource
    timestamp: float
    confidence: float
    metadata: Dict[str, Any]
    agent_id: str


@dataclass
class ActivityAssessment:
    """Final assessment of agent activity."""
    agent_id: str
    is_active: bool
    confidence: float
    last_activity: Optional[datetime]
    inactivity_minutes: float
    signals: List[ActivitySignal]
    validation_passed: bool
    reasons: List[str]


__all__ = [
    "ActivityConfidence",
    "ActivitySource",
    "ActivitySignal",
    "ActivityAssessment",
]


