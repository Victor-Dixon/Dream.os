#!/usr/bin/env python3
# Header-Variant: full
# Owner: @dreamos/platform
# Purpose: metrics_models module.
# SSOT: docs/recovery/recovery_registry.yaml#src-core-intelligent-context-metrics-models
# @registry docs/recovery/recovery_registry.yaml#src-core-intelligent-context-metrics-models

"""
<!-- SSOT Domain: core -->

Context Metrics Models - V2 Compliance
=======================================

Metrics tracking for context retrieval operations.

Extracted from intelligent_context_models.py for V2 compliance.
Part of 13→≤5 class consolidation (ROI 90.00).

Author: Agent-7 (Repository Cloning Specialist) - V2 Compliance Refactor
Original: Captain Agent-4 - Strategic Oversight
License: MIT
@registry docs/recovery/recovery_registry.yaml#src-core-intelligent-context-metrics-models
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


__all__ = ["ContextMetrics"]
