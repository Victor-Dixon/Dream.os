#!/usr/bin/env python3
"""
AI Context Engine - Phase 5 Core Intelligence
============================================

AI-powered context processing system for real-time collaboration and intelligent UX.

<!-- SSOT Domain: ai_context -->

Navigation References:
├── Related Files:
│   ├── Data Models → models.py
│   ├── Context Processors → context_processors.py
│   ├── Suggestion Generators → suggestion_generators.py
│   ├── Session Manager → session_manager.py
│   ├── Risk Analytics → src/services/risk_analytics/risk_calculator_service.py
│   ├── WebSocket Server → src/services/risk_analytics/risk_websocket_server.py
│   ├── Dashboard Integration → src/web/static/js/trading-robot/risk-dashboard-integration.js
│   ├── FastAPI Infrastructure → src/web/fastapi_app.py
│   └── Real-time Processing → src/core/analytics/engines/realtime_analytics_engine.py
├── Documentation:
│   ├── Phase 5 Architecture → docs/PHASE5_AI_CONTEXT_ENGINE.md
│   ├── Real-time Integration → docs/analytics/TRADINGROBOTPLUG_ANALYTICS_ARCHITECTURE.md
│   └── Infrastructure Validation → docs/PHASE4_TO_PHASE5_TRANSITION_VALIDATION_2026-01-07.md
└── Testing:
    └── Integration Tests → tests/integration/test_ai_context_engine.py

Features:
- Real-time context awareness for collaborative sessions
- AI-powered intelligent suggestions and recommendations
- Risk-aware context processing integration
- Session state management with persistence
- Context-driven UX personalization
- Performance metrics and analytics integration

Author: Agent-5 (Business Intelligence Specialist)
Date: 2026-01-08
Phase: Phase 5 - AI Context Engine (V2 Compliant Refactoring)
"""

import asyncio
import logging
import time
from typing import Dict, List, Any, Optional
from dataclasses import asdict

from src.core.base.base_service import BaseService

# Extracted modules for V2 compliance
from .models import ContextSession, ContextSuggestion
from .context_processors import (
    ContextProcessor, TradingContextProcessor, CollaborationContextProcessor,
    AnalysisContextProcessor, RiskContextProcessor
)
from .session_manager import SessionManager

logger = logging.getLogger(__name__)


class AIContextEngine(BaseService):
    """
    AI-powered context processing engine for real-time collaboration.

    Navigation:
    ├── Uses: SessionManager, ContextProcessor subclasses
    ├── Depends on: RiskCalculatorService, AIService
    └── Related: ai_context_websocket.py, ai_context_integration.js

    Features:
    - Real-time context awareness and processing
    - Risk-integrated intelligent suggestions
    - Session state management with persistence
    - Performance monitoring and optimization
    - Collaborative context sharing
    """

    def __init__(self):
        """
        Initialize the AI Context Engine.

        Navigation:
        ├── Creates: SessionManager, context processor instances
        └── Related: BaseService initialization
        """
        super().__init__("AIContextEngine")

        # Session management (extracted to SessionManager)
        self.session_manager = SessionManager()

        # Context processors (extracted to separate module)
        self.context_processors: Dict[str, ContextProcessor] = {
            'trading': TradingContextProcessor(),
            'collaboration': CollaborationContextProcessor(),
            'analysis': AnalysisContextProcessor(),
            'risk': RiskContextProcessor()
        }

        # Performance tracking
        self.performance_stats = {
            'total_sessions': 0,
            'active_sessions': 0,
            'suggestions_generated': 0,
            'suggestions_applied': 0,
            'processing_time_avg': 0.0,
            'risk_integrations': 0
        }

        logger.info("🧠 AI Context Engine initialized (V2 Compliant)")

    async def start_engine(self):
        """
        Start the AI Context Engine with background tasks.

        Navigation:
        ├── Delegates to: SessionManager.start_background_tasks()
        └── Related: FastAPI startup integration
        """
        await self.session_manager.start_background_tasks()
        logger.info("🚀 AI Context Engine started with background processing")

    async def stop_engine(self):
        """
        Stop the AI Context Engine and cleanup.

        Navigation:
        ├── Delegates to: SessionManager.stop_background_tasks()
        └── Related: FastAPI shutdown integration
        """
        await self.session_manager.stop_background_tasks()
        logger.info("🛑 AI Context Engine stopped")

    async def create_session(self, user_id: str, context_type: str,
                           initial_context: Dict[str, Any]) -> str:
        """
        Create a new context processing session.

        Navigation:
        ├── Delegates to: SessionManager.create_session()
        ├── Updates: performance_stats counters
        └── Related: session lifecycle management

        Args:
            user_id: User identifier
            context_type: Type of context ('trading', 'collaboration', etc.)
            initial_context: Initial context data

        Returns:
            Session ID for the created session
        """
        session_id = await self.session_manager.create_session(user_id, context_type, initial_context)

        self.performance_stats['total_sessions'] += 1
        self.performance_stats['active_sessions'] += 1

        logger.info(f"📝 Created context session: {session_id} for user {user_id}")
        return session_id

    async def update_session_context(self, session_id: str,
                                   context_updates: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update context data for an active session.

        Navigation:
        ├── Uses: SessionManager for session access, ContextProcessor for suggestions
        ├── Updates: performance_stats, session activity
        └── Related: real-time context processing pipeline

        Args:
            session_id: Session identifier
            context_updates: Context data updates

        Returns:
            Updated context data and any new suggestions
        """
        session = self.session_manager.get_session(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")

        await self.session_manager.update_session_activity(session_id)

        # Update context data
        session.context_data.update(context_updates)

        # Process context and generate suggestions
        start_time = time.time()
        suggestions = await self._process_context(session)
        processing_time = time.time() - start_time

        # Update performance metrics
        session.performance_metrics['last_processing_time'] = processing_time
        self.performance_stats['processing_time_avg'] = (
            (self.performance_stats['processing_time_avg'] * 0.9) + (processing_time * 0.1)
        )

        # Add suggestions to session
        for suggestion in suggestions:
            session.ai_suggestions.append(asdict(suggestion))
            self.performance_stats['suggestions_generated'] += 1

        return {
            'session_id': session_id,
            'updated_context': session.context_data,
            'new_suggestions': [asdict(s) for s in suggestions],
            'processing_time': processing_time
        }

    async def get_session_context(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Get current context for a session.

        Navigation:
        ├── Delegates to: SessionManager.get_session_context()
        └── Related: WebSocket client data retrieval
        """
        return self.session_manager.get_session_context(session_id)

    async def apply_suggestion(self, session_id: str, suggestion_id: str) -> bool:
        """
        Mark a suggestion as applied.

        Navigation:
        ├── Uses: SessionManager for session access
        ├── Updates: performance_stats counters
        └── Related: suggestion tracking and analytics
        """
        session = self.session_manager.get_session(session_id)
        if not session:
            return False

        for suggestion in session.ai_suggestions:
            if suggestion.get('suggestion_id') == suggestion_id:
                suggestion['applied'] = True
                self.performance_stats['suggestions_applied'] += 1
                logger.info(f"✅ Applied suggestion {suggestion_id} in session {session_id}")
                return True

        return False

    async def end_session(self, session_id: str) -> Dict[str, Any]:
        """
        End a context session and return final metrics.

        Navigation:
        ├── Delegates to: SessionManager.end_session()
        ├── Updates: performance_stats counters
        └── Related: session lifecycle completion
        """
        session_summary = await self.session_manager.end_session(session_id)
        if not session_summary:
            return {'error': 'Session not found'}

        self.performance_stats['active_sessions'] -= 1
        return session_summary

    async def _process_context(self, session: ContextSession) -> List[ContextSuggestion]:
        """
        Process context and generate AI suggestions.

        Navigation:
        ├── Uses: ContextProcessor subclasses from context_processors module
        ├── Routes to: appropriate processor based on context_type
        └── Related: context processing pipeline, suggestion generation
        """
        context_type = session.context_type

        if context_type not in self.context_processors:
            logger.warning(f"Unknown context type: {context_type}")
            return []

        processor = self.context_processors[context_type]
        return await processor.process(session)


    def get_performance_stats(self) -> Dict[str, Any]:
        """
        Get current performance statistics.

        Navigation:
        ├── Combines: local performance_stats with SessionManager stats
        └── Related: monitoring dashboards, performance reporting
        """
        session_stats = self.session_manager.get_performance_stats()
        return {**self.performance_stats, **session_stats}


# Global instance for service access
ai_context_engine = AIContextEngine()

# Example usage and testing
async def main():
    """
    Example usage of the AI Context Engine.

    Navigation:
    ├── Demonstrates: full session lifecycle
    └── Related: integration testing, API usage examples
    """
    engine = AIContextEngine()
    await engine.start_engine()

    try:
        # Create a trading session
        session_id = await engine.create_session(
            user_id="trader_001",
            context_type="trading",
            initial_context={
                "portfolio_value": 100000,
                "positions": [
                    {"symbol": "AAPL", "quantity": 100, "price": 150.00, "pnl": 2500},
                    {"symbol": "GOOGL", "quantity": 50, "price": 2800.00, "pnl": -1200}
                ],
                "market_volatility": 0.18
            }
        )

        print(f"Created session: {session_id}")

        # Update context and get suggestions
        result = await engine.update_session_context(session_id, {
            "new_position": {"symbol": "MSFT", "quantity": 75, "price": 300.00},
            "market_data": {"vix": 22.5}
        })

        print(f"Context updated with {len(result['new_suggestions'])} suggestions")

        # Get final context
        final_context = await engine.get_session_context(session_id)
        print(f"Final context: {len(final_context['ai_suggestions'])} total suggestions")

        # End session
        summary = await engine.end_session(session_id)
        print(f"Session ended: {summary['duration_seconds']:.1f}s duration")

    finally:
        await engine.stop_engine()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())