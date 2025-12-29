"""
<!-- SSOT Domain: core -->

Orchestration Contracts - Core Interfaces
==========================================

Defines core orchestration protocols and interfaces.

Author: Agent-7 (Web Development Specialist)
License: MIT
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, field
from typing import Any, Protocol


@dataclass
class OrchestrationContext:
    """Context object for orchestration operations."""

    orchestrator_id: str = ""
    config: dict[str, Any] = field(default_factory=dict)
    metrics: dict[str, Any] | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    _events: list[tuple[str, dict[str, Any]]] = field(default_factory=list, repr=False)

    def emit(self, event: str, data: dict[str, Any] | None = None) -> None:
        """Emit an orchestration event."""
        self._events.append((event, data or {}))

    def get_events(self) -> list[tuple[str, dict[str, Any]]]:
        """Get all emitted events."""
        return list(self._events)


@dataclass
class OrchestrationResult:
    """Result object for orchestration operations."""

    ok: bool
    summary: str
    metrics: dict[str, Any] = field(default_factory=dict)
    error: str | None = None


class Step(Protocol):
    """Protocol for orchestration steps."""

    def name(self) -> str:
        """Return step name."""
        ...

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
