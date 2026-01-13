#!/usr/bin/env python3
"""
<!-- SSOT Domain: core -->

Mission Context Models - V2 Compliance
=======================================

Mission context data structures for intelligent retrieval.

Extracted from intelligent_context_models.py for V2 compliance.
Part of 13→≤5 class consolidation (ROI 90.00).

Author: Agent-7 (Repository Cloning Specialist) - V2 Compliance Refactor
Original: Captain Agent-4 - Strategic Oversight
License: MIT
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from src.core.utils.serialization_utils import to_dict


@dataclass
class MissionContext:
    """Mission context structure for intelligent retrieval."""

    mission_id: str
    mission_type: str
    current_phase: str
    agent_assignments: dict[str, str] = field(default_factory=dict)
    critical_path: list[str] = field(default_factory=list)
    risk_factors: list[str] = field(default_factory=list)
    success_criteria: list[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    last_updated: datetime = field(default_factory=datetime.now)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary using SSOT utility."""
        return to_dict(self)


__all__ = ["MissionContext"]
