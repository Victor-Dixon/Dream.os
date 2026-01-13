#!/usr/bin/env python3
"""
<!-- SSOT Domain: core -->

Intelligent Context Metrics
============================

Metrics tracking for context retrieval operations.

Author: Agent-7 - Knowledge & OSS Contribution Specialist
Refactored from intelligent_context_models.py for V2 compliance
License: MIT
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from src.core.utils.serialization_utils import to_dict


@dataclass
class ContextMetrics:
    """Metrics for context retrieval operations."""

    total_retrievals: int = 0
    successful_retrievals: int = 0
    failed_retrievals: int = 0
    average_execution_time_ms: float = 0.0
    total_execution_time_ms: float = 0.0
    emergency_interventions: int = 0
    agent_optimizations: int = 0
    risk_assessments: int = 0
    success_predictions: int = 0
    last_updated: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary using SSOT utility."""
        return to_dict(self)
