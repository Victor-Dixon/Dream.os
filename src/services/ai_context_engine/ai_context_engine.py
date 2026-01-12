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
    AnalysisContextProcessor, RiskContextProcessor, UXContextProcessor
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

        # Initialize components
        self.session_manager = SessionManager()
        self.context_processors = self._init_context_processors()
        self.performance_stats = self._init_performance_stats()

        logger.info("🧠 AI Context Engine initialized (V2 Compliant)")

    def _init_context_processors(self) -> Dict[str, ContextProcessor]:
        """Initialize context processors with error handling."""
        processors = {}
        processor_classes = {
            'trading': TradingContextProcessor,
            'collaboration': CollaborationContextProcessor,
            'analysis': AnalysisContextProcessor,
            'risk': RiskContextProcessor,
            'ux': UXContextProcessor
        }

        for name, processor_class in processor_classes.items():
            try:
                processors[name] = processor_class()
                logger.debug(f"✅ Initialized context processor: {name}")
            except Exception as e:
                logger.error(f"❌ Failed to initialize context processor {name}: {e}")
                # Continue with other processors even if one fails
                continue

        if not processors:
            logger.warning("⚠️ No context processors could be initialized")

        return processors

    def _init_performance_stats(self) -> Dict[str, Any]:
        """Initialize performance tracking statistics."""
        return {
            'total_sessions': 0,
            'active_sessions': 0,
            'suggestions_generated': 0,
            'suggestions_applied': 0,
            'processing_time_avg': 0.0,
            'risk_integrations': 0
        }

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
        Update context data for an active session with enhanced validation and error handling.

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
        try:
            # Validate inputs
            if not session_id or not isinstance(session_id, str):
                raise ValueError("Invalid session_id: must be non-empty string")

            if not isinstance(context_updates, dict):
                raise ValueError("Invalid context_updates: must be dictionary")

            # Get session with error handling
            session = self.session_manager.get_session(session_id)
            if not session:
                logger.warning(f"Session {session_id} not found for context update")
                return {
                    'error': 'Session not found',
                    'session_id': session_id
                }

            # Validate session state
            if session.status != 'active':
                logger.warning(f"Attempted to update inactive session {session_id}")
                return {
                    'error': f'Session is {session.status}',
                    'session_id': session_id
                }

            # Update session activity
            await self.session_manager.update_session_activity(session_id)

            # Validate and sanitize context updates
            validated_updates = self._validate_context_updates(context_updates)
            if not validated_updates:
                logger.warning(f"No valid context updates provided for session {session_id}")
                return {
                    'session_id': session_id,
                    'updated_context': session.context_data,
                    'new_suggestions': [],
                    'processing_time': 0.0
                }

            # Update context data
            session.context_data.update(validated_updates)

            # Process context and generate suggestions with timeout protection
            start_time = time.time()
            try:
                suggestions = await asyncio.wait_for(
                    self._process_context(session),
                    timeout=30.0  # 30 second timeout for context processing
                )
            except asyncio.TimeoutError:
                logger.error(f"Context processing timeout for session {session_id}")
                suggestions = []
            except Exception as e:
                logger.error(f"Context processing error for session {session_id}: {e}")
                suggestions = []

            processing_time = time.time() - start_time

            # Update performance metrics
            session.performance_metrics['last_processing_time'] = processing_time
            self.performance_stats['processing_time_avg'] = (
                (self.performance_stats['processing_time_avg'] * 0.9) + (processing_time * 0.1)
            )

            # Add suggestions to session with validation
            valid_suggestions = []
            for suggestion in suggestions:
                try:
                    if self._validate_suggestion(suggestion):
                        session.ai_suggestions.append(asdict(suggestion))
                        valid_suggestions.append(asdict(suggestion))
                        self.performance_stats['suggestions_generated'] += 1
                except Exception as e:
                    logger.error(f"Invalid suggestion format: {e}")
                    continue

            logger.info(f"✅ Updated context for session {session_id}: {len(validated_updates)} updates, {len(valid_suggestions)} suggestions")

            return {
                'session_id': session_id,
                'updated_context': session.context_data,
                'new_suggestions': valid_suggestions,
                'processing_time': processing_time
            }

        except Exception as e:
            logger.error(f"Failed to update session context {session_id}: {e}")
            return {
                'error': str(e),
                'session_id': session_id
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

    def _validate_context_updates(self, updates: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate and sanitize context updates.

        Args:
            updates: Raw context updates

        Returns:
            Validated and sanitized updates
        """
        validated = {}

        for key, value in updates.items():
            # Basic validation - ensure keys are strings and values are serializable
            if not isinstance(key, str) or not key:
                logger.warning(f"Skipping invalid context key: {key}")
                continue

            try:
                # Test JSON serializability
                import json
                json.dumps({key: value})
                validated[key] = value
            except (TypeError, ValueError) as e:
                logger.warning(f"Skipping non-serializable context value for key {key}: {e}")
                continue

        return validated

    def _validate_suggestion(self, suggestion: ContextSuggestion) -> bool:
        """
        Validate suggestion format and content.

        Args:
            suggestion: Suggestion to validate

        Returns:
            True if suggestion is valid
        """
        required_fields = ['suggestion_id', 'type', 'content', 'confidence']
        if not hasattr(suggestion, '__dict__'):
            return False

        suggestion_dict = suggestion.__dict__ if hasattr(suggestion, '__dict__') else suggestion

        for field in required_fields:
            if field not in suggestion_dict:
                logger.warning(f"Suggestion missing required field: {field}")
                return False

        # Validate confidence is between 0 and 1
        confidence = suggestion_dict.get('confidence', 0)
        if not isinstance(confidence, (int, float)) or not (0 <= confidence <= 1):
            logger.warning(f"Invalid suggestion confidence: {confidence}")
            return False

        return True

    async def _process_context(self, session: ContextSession) -> List[ContextSuggestion]:
        """
        Process context and generate AI suggestions with error handling.

        Navigation:
        ├── Uses: ContextProcessor subclasses from context_processors module
        ├── Routes to: appropriate processor based on context_type
        └── Related: context processing pipeline, suggestion generation
        """
        context_type = session.context_type

        if context_type not in self.context_processors:
            logger.warning(f"Unknown context type: {context_type}")
            return []

        try:
            processor = self.context_processors[context_type]
            suggestions = await processor.process(session)

            # Validate all suggestions
            valid_suggestions = []
            for suggestion in suggestions:
                if self._validate_suggestion(suggestion):
                    valid_suggestions.append(suggestion)
                else:
                    logger.warning(f"Filtered out invalid suggestion from {context_type} processor")

            return valid_suggestions

        except Exception as e:
            logger.error(f"Context processing failed for {context_type}: {e}")
            return []


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