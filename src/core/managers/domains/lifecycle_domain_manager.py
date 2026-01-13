"""
<!-- SSOT Domain: core -->

Single Source of Truth (SSOT) for Lifecycle Domain Management
Domain: Lifecycle (Onboarding + Recovery)
Owner: Agent-2 (Architecture & Design)
Last Updated: 2025-12-08

Lifecycle Domain Manager - V2 Compliant Module
==============================================

Consolidates agent lifecycle operations including:
- Agent onboarding and initialization
- Error recovery and resilience mechanisms
- State transitions and lifecycle management

This SSOT replaces:
- src/core/managers/core_onboarding_manager.py
- src/core/managers/core_recovery_manager.py

V2 Compliance: < 300 lines, single domain responsibility.
Consolidation: 2 managers → 1 SSOT (-50% code reduction)

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict

from ..contracts import Manager, ManagerContext, ManagerResult
from ..constants.manager import COMPLETION_SIGNAL


@dataclass
class OnboardingSession:
    """Represents a single onboarding session."""
    agent_id: str
    agent_name: str
    role: str
    template: str
    status: str = "pending"
    start_time: datetime | None = None
    end_time: datetime | None = None
    notes: str | None = None


class LifecycleDomainManager(Manager):
    """
    SSOT for all agent lifecycle operations.

    Consolidates:
    - Agent onboarding (from CoreOnboardingManager)
    - Error recovery (from CoreRecoveryManager)
    """

    def __init__(self) -> None:
        # Onboarding state (from CoreOnboardingManager)
        self._onboarding_templates = ["default", "advanced"]
        self._onboarding_sessions: Dict[str, OnboardingSession] = {}

        # Recovery state (from CoreRecoveryManager)
        self._recovery_strategies: Dict[str, Dict[str, Any]] = {
            "default_retry": {
                "type": "retry",
                "conditions": {},
                "actions": ["retry"],
                "enabled": True,
            }
        }

    def initialize(self, context: ManagerContext) -> bool:
        """Initialize lifecycle domain manager."""
        context.logger("LifecycleDomainManager initialized - Onboarding + Recovery consolidated")
        return True

    def execute(
        self, context: ManagerContext, operation: str, payload: Dict[str, Any]
    ) -> ManagerResult:
        """Execute lifecycle operation (onboarding or recovery)."""
        handlers = {
            # Onboarding operations
            "onboard_agent": self.onboard_agent,
            "start_onboarding": self.start_onboarding,
            "complete_onboarding": self.complete_onboarding,
            "get_onboarding_status": self.get_onboarding_status,

            # Recovery operations
            "register_recovery_strategy": self.register_recovery_strategy,
            "recover_from_error": self.recover_from_error,
            "get_recovery_strategies": self.get_recovery_strategies,
        }

        handler = handlers.get(operation)
        if not handler:
            return ManagerResult(False, {}, {}, f"Unknown lifecycle operation: {operation}")
        return handler(context, payload)

    def cleanup(self, context: ManagerContext) -> bool:
        """Cleanup all lifecycle resources."""
        self._onboarding_sessions.clear()
        self._recovery_strategies.clear()
        context.logger("LifecycleDomainManager cleaned up")
        return True

    def get_status(self) -> Dict[str, Any]:
        """Return consolidated lifecycle status."""
        return {
            "onboarding": {
                "templates": self._onboarding_templates,
                "total_sessions": len(self._onboarding_sessions),
            },
            "recovery": {
                "strategies": list(self._recovery_strategies.keys()),
            },
            "consolidated_operations": [
                "onboard_agent", "start_onboarding", "complete_onboarding", "get_onboarding_status",
                "register_recovery_strategy", "recover_from_error", "get_recovery_strategies"
            ]
        }

    # Onboarding Handlers ---------------------------------------------------------------

    def onboard_agent(self, context: ManagerContext, payload: Dict[str, Any]) -> ManagerResult:
        """Create new onboarding session."""
        agent_id = payload["agent_id"]
        session_id = str(uuid.uuid4())
        session = OnboardingSession(
            agent_id=agent_id,
            agent_name=payload.get("agent_name", agent_id),
            role=payload.get("role", "unknown"),
            template=payload.get("template", "default"),
        )
        self._onboarding_sessions[session_id] = session
        context.logger(f"Onboarding session created: {session_id} for agent {agent_id}")
        return ManagerResult(True, {"session_id": session_id, "agent_id": agent_id}, {})

    def start_onboarding(self, context: ManagerContext, payload: Dict[str, Any]) -> ManagerResult:
        """Start onboarding session."""
        session = self._onboarding_sessions.get(payload["session_id"])
        if not session:
            return ManagerResult(False, {}, {}, "Onboarding session not found")

        session.status = "in_progress"
        session.start_time = datetime.utcnow()
        context.logger(f"Onboarding session started: {payload['session_id']}")
        return ManagerResult(True, {"session_id": payload["session_id"]}, {})

    def complete_onboarding(self, context: ManagerContext, payload: Dict[str, Any]) -> ManagerResult:
        """Complete onboarding session."""
        session = self._onboarding_sessions.get(payload["session_id"])
        if not session:
            return ManagerResult(False, {}, {}, "Onboarding session not found")

        session.status = "completed" if payload.get("success", True) else "failed"
        session.end_time = datetime.utcnow()
        session.notes = payload.get("notes")

        context.logger(
            f"Onboarding session completed: {payload['session_id']} {COMPLETION_SIGNAL}"
        )
        return ManagerResult(
            True,
            {"session_id": payload["session_id"], "status": session.status},
            {},
        )

    def get_onboarding_status(self, context: ManagerContext, payload: Dict[str, Any]) -> ManagerResult:
        """Get onboarding session status."""
        session = self._onboarding_sessions.get(payload["session_id"])
        if not session:
            return ManagerResult(False, {}, {}, "Onboarding session not found")

        data = {
            "session_id": payload["session_id"],
            "status": session.status,
            "start_time": session.start_time,
            "end_time": session.end_time,
            "notes": session.notes,
        }
        return ManagerResult(True, data, {})

    # Recovery Handlers ----------------------------------------------------------------

    def register_recovery_strategy(self, context: ManagerContext, payload: Dict[str, Any]) -> ManagerResult:
        """Register new recovery strategy."""
        name = payload["strategy_name"]
        self._recovery_strategies[name] = {
            "type": payload.get("strategy_type", "retry"),
            "conditions": payload.get("conditions", {}),
            "actions": payload.get("actions", []),
            "enabled": payload.get("enabled", True),
        }
        context.logger(f"Recovery strategy registered: {name}")
        return ManagerResult(True, {"strategy_name": name, "registered": True}, {})

    def recover_from_error(self, context: ManagerContext, payload: Dict[str, Any]) -> ManagerResult:
        """Execute error recovery."""
        recovery_id = str(uuid.uuid4())
        error_type = payload.get("error_type", "unknown")
        context.logger(f"Recovery invoked for {error_type} with id {recovery_id}")
        return ManagerResult(True, {"recovery_id": recovery_id}, {})

    def get_recovery_strategies(self, context: ManagerContext, payload: Dict[str, Any]) -> ManagerResult:
        """Get all recovery strategies."""
        return ManagerResult(True, {"strategies": self._recovery_strategies}, {})
