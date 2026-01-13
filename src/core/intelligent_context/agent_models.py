#!/usr/bin/env python3
"""
<!-- SSOT Domain: core -->

Agent Context Models - V2 Compliance
=====================================

Agent capability and recommendation data structures.

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
class AgentCapability:
    """Agent capability structure for matching and optimization."""

    agent_id: str
    primary_role: str
    skills: set[str] = field(default_factory=set)
    experience_level: str = "intermediate"
    current_workload: int = 0
    success_rate: float = 0.8
    specialization: list[str] = field(default_factory=list)
    availability_status: str = "available"
    last_active: datetime = field(default_factory=datetime.now)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary using SSOT utility."""
        result = to_dict(self)
        # Ensure skills set is converted to list
        if "skills" in result and isinstance(result["skills"], set):
            result["skills"] = list(result["skills"])
        return result


@dataclass
class AgentRecommendation:
    """Agent recommendation structure."""

    agent_id: str
    recommendation_score: float
    reasoning: list[str] = field(default_factory=list)
    specialization_match: str = ""
    workload_impact: float = 0.0
    success_probability: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)


__all__ = ["AgentCapability", "AgentRecommendation"]
