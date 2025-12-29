#!/usr/bin/env python3
"""
<!-- SSOT Domain: core -->

Gas Pipeline System - Backward Compatibility Shim
=================================================

Backward compatibility shim for auto_gas_pipeline_system refactoring.
Maintains existing import paths while using new modular structure.
"""

from __future__ import annotations

from .core.pipeline import AutoGasPipelineSystem
from .core.integration import PipelineMonitorIntegration
from .core.models import AgentState, PipelineAgent
from .core.optimizer import JetFuelOptimizer

__all__ = [
    "AutoGasPipelineSystem",
    "PipelineMonitorIntegration",
    "JetFuelOptimizer",
    "AgentState",
    "PipelineAgent",
]
