# File: src/core/orchestration/service_orchestrator.py
# Purpose: Coordinate service-level orchestration flows across core runtime components.
# Owns: orchestration sequencing, orchestration lifecycle coordination
# Does Not Own: business logic execution details, persistence adapters, UI behavior
# Inputs: orchestration requests, service state/context objects
# Outputs: orchestration execution results, coordination status transitions
# Dependencies: src/core/service_base.py, src/core/orchestration/async_orchestrator.py
# Used By: src/core/unified_entry_point_system.py, runtime orchestration entrypoints
# Status: active | Last Updated: 2026-03-13
# Notes: Keep orchestration boundaries explicit and delegate concrete task logic.

"""
Service Orchestrator - Service Pipeline

<!-- SSOT Domain: integration -->
"""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from .contracts import OrchestrationContext, OrchestrationResult, Orchestrator, Step
from .registry import StepRegistry


class ServiceOrchestrator(Orchestrator):
    """Service-scope orchestration: IO, messaging, analytics service flows."""

    def __init__(self, registry: StepRegistry) -> None:
        self.registry = registry

    def plan(self, ctx: OrchestrationContext, payload: dict[str, Any]) -> Iterable[Step]:
        keys = payload.get("service_pipeline", [])
        return self.registry.build(keys)

    def execute(self, ctx: OrchestrationContext, payload: dict[str, Any]) -> OrchestrationResult:
        steps = list(self.plan(ctx, payload))
        data = dict(payload)
        for s in steps:
            data = s.run(ctx, data)
        return OrchestrationResult(
            ok=True,
            summary=f"service:{len(steps)}",
            metrics={"service_steps": len(steps)},
        )

    def report(self, result: OrchestrationResult) -> str:
        return f"[ServiceOrchestrator] {result.summary}"
