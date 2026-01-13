#!/usr/bin/env python3
"""
<!-- SSOT Domain: core -->

Intelligent Context Core Models
================================

Core data models for mission context and agent capabilities.

Author: Agent-7 - Knowledge & OSS Contribution Specialist
Refactored from intelligent_context_models.py for V2 compliance
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
