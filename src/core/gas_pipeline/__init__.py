#!/usr/bin/env python3
# Header-Variant: full
# Owner: Dream.os Platform
# Purpose: gas pipeline package initialization.
# SSOT: docs/recovery/recovery_registry.yaml

"""
<!-- SSOT Domain: core -->

Gas Pipeline System - Backward Compatibility Shim
=================================================

Backward compatibility shim for auto_gas_pipeline_system refactoring.
Maintains existing import paths while using new modular structure.
@registry docs/recovery/recovery_registry.yaml#unregistered-src-core-gas-pipeline-init
@file gas pipeline package initialization.
@summary gas pipeline package initialization.
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
