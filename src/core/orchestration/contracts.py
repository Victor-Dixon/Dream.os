"""
Orchestration Contracts - Core Interfaces
==========================================

Defines core orchestration protocols and interfaces.

Author: Agent-7 (Web Development Specialist)
License: MIT
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any, Protocol
from dataclasses import dataclass, field



@dataclass
class OrchestrationContext:
    """Context object for orchestration operations."""

    config: dict[str, Any]
    metrics: dict[str, Any] | None = None

    def emit(self, event: str, data: dict[str, Any]) -> None:
        """Emit an orchestration event."""
        pass


@dataclass
class OrchestrationResult:
    """Result object for orchestration operations."""

    ok: bool
    summary: str
    metrics: dict[str, Any] | None = None
    error: str | None = None


class Step(Protocol):
    """Protocol for orchestration steps."""

    def run(self, ctx: OrchestrationContext, data: dict[str, Any]) -> dict[str, Any]:
        """Execute the step and return updated data."""
        ...


class Orchestrator(Protocol):
    """Protocol for orchestrators."""

    def plan(self, ctx: OrchestrationContext, payload: dict[str, Any]) -> Iterable[Step]:
        """Plan the orchestration steps."""
        ...

    def execute(self, ctx: OrchestrationContext, payload: dict[str, Any]) -> OrchestrationResult:
        """Execute the orchestration."""
        ...

    def report(self, result: OrchestrationResult) -> str:
        """Generate a report from the result."""
        ...

