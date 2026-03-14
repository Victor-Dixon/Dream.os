"""AI Context Engine package."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, Dict, List

import numpy as np

from .models import ContextSession, ContextSuggestion
from ..risk_analytics.risk_calculator_service import RiskMetrics


class AIContextEngine:
    """Minimal AI context engine implementation for tests."""

    def __init__(self) -> None:
        self.active_sessions: Dict[str, ContextSession] = {}
        self.running = False

    async def start_engine(self) -> None:
        self.running = True

    async def stop_engine(self) -> None:
        self.running = False
        self.active_sessions.clear()

    async def create_session(
        self,
        user_id: str,
        context_type: str,
        initial_context: Dict[str, Any],
    ) -> str:
        session_id = str(uuid.uuid4())
        now = datetime.utcnow()
        session = ContextSession(
            session_id=session_id,
            user_id=user_id,
            context_type=context_type,
            start_time=now,
            last_activity=now,
            context_data=dict(initial_context),
        )
        session.ai_suggestions = []
        session.risk_metrics = None
        self.active_sessions[session_id] = session

        if context_type == "trading":
            self._hydrate_risk_metrics(session)

        self._add_suggestion(
            session,
            suggestion_type="insight",
            content={"summary": "Session initialized."},
            reasoning="Initial context processed.",
        )
        return session_id

    async def update_session_context(self, session_id: str, context_updates: Dict[str, Any]) -> Dict[str, Any]:
        session = self.active_sessions.get(session_id)
        if not session:
            raise ValueError("Session not found")

        session.context_data.update(context_updates)
        session.last_activity = datetime.utcnow()

        suggestion = self._add_suggestion(
            session,
            suggestion_type="analysis",
            content={"summary": "Context updated."},
            reasoning="New data received.",
        )

        return {
            "success": True,
            "session_id": session_id,
            "new_suggestions": [suggestion],
        }

    async def end_session(self, session_id: str) -> Dict[str, Any]:
        existed = session_id in self.active_sessions
        self.active_sessions.pop(session_id, None)
        return {"success": existed}

    async def apply_suggestion(self, session_id: str, suggestion_id: str) -> bool:
        session = self.active_sessions.get(session_id)
        if not session:
            return False
        return any(s["suggestion_id"] == suggestion_id for s in session.ai_suggestions)

    def _add_suggestion(
        self,
        session: ContextSession,
        suggestion_type: str,
        content: Dict[str, Any],
        reasoning: str,
    ) -> Dict[str, Any]:
        suggestion = {
            "suggestion_id": str(uuid.uuid4()),
            "session_id": session.session_id,
            "suggestion_type": suggestion_type,
            "confidence_score": 0.75,
            "content": content,
            "reasoning": reasoning,
            "timestamp": datetime.utcnow(),
        }
        session.ai_suggestions.append(suggestion)
        return suggestion

    def _hydrate_risk_metrics(self, session: ContextSession) -> None:
        returns = np.array(session.context_data.get("returns", []), dtype=float)
        equity = np.array(session.context_data.get("equity_curve", []), dtype=float)
        if returns.size == 0 or equity.size == 0:
            return
        session.risk_metrics = RiskMetrics(
            var_95=float(np.percentile(returns, 5)) if returns.size else 0.0,
            cvar_95=float(np.mean(returns)) if returns.size else 0.0,
            sharpe_ratio=float(np.mean(returns)) if returns.size else 0.0,
            max_drawdown=float(np.max(equity) - np.min(equity)) if equity.size else 0.0,
            calmar_ratio=0.0,
            sortino_ratio=0.0,
            information_ratio=0.0,
            calculation_date=datetime.utcnow(),
            confidence_level=0.95,
        )


ai_context_engine = AIContextEngine()

__all__ = [
    "AIContextEngine",
    "ContextSession",
    "ContextSuggestion",
    "ai_context_engine",
]
