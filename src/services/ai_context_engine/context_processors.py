#!/usr/bin/env python3
"""
AI Context Engine Context Processors
===================================

Context processing logic for different context types.

<!-- SSOT Domain: ai_context -->

Navigation References:
├── Related Files:
│   ├── Main Engine → ai_context_engine.py
│   ├── Data Models → models.py
│   ├── Suggestion Generators → suggestion_generators.py
│   └── Risk Calculator → src/services/risk_analytics/risk_calculator_service.py
├── Documentation:
│   └── Phase 5 Architecture → docs/PHASE5_AI_CONTEXT_ENGINE.md
└── Testing:
    └── Integration Tests → tests/integration/test_ai_context_engine.py

Classes:
- ContextProcessor: Base class for context processors
- TradingContextProcessor: Handles trading context processing
- CollaborationContextProcessor: Handles collaboration context
- AnalysisContextProcessor: Handles analytical context
- RiskContextProcessor: Handles risk-focused context
"""

import time
from typing import List, Dict, Any
from datetime import datetime
import logging

from .models import ContextSession, ContextSuggestion
from .suggestion_generators import SuggestionGenerators
from src.services.risk_analytics.risk_calculator_service import RiskCalculatorService

logger = logging.getLogger(__name__)


class ContextProcessor:
    """
    Base class for context processors.

    Navigation:
    ├── Subclasses: TradingContextProcessor, CollaborationContextProcessor, etc.
    ├── Used by: AIContextEngine._process_context()
    └── Related: ContextSession, ContextSuggestion
    """

    def __init__(self):
        """Initialize the context processor."""
        self.suggestion_generators = SuggestionGenerators()

    async def process(self, session: ContextSession) -> List[ContextSuggestion]:
        """
        Process context and generate suggestions.

        Args:
            session: The context session to process

        Returns:
            List of context suggestions
        """
        raise NotImplementedError("Subclasses must implement process()")


class TradingContextProcessor(ContextProcessor):
    """
    Processes trading context with risk integration.

    Navigation:
    ├── Used by: AIContextEngine._process_context()
    ├── Depends on: RiskCalculatorService, SuggestionGenerators
    └── Related: trading_robot data structures, market data APIs
    """

    def __init__(self):
        """Initialize trading context processor."""
        super().__init__()
        self.risk_calculator = RiskCalculatorService()

    async def process(self, session: ContextSession) -> List[ContextSuggestion]:
        """
        Process trading context with risk integration.

        Navigation:
        ├── Calls: RiskCalculatorService.calculate_comprehensive_risk_metrics()
        ├── Uses: SuggestionGenerators.generate_risk_suggestions()
        └── Related: TradingRobotApp portfolio data, market volatility indicators
        """
        suggestions = []

        # Extract trading data
        context = session.context_data
        positions = context.get('positions', [])

        # Calculate risk metrics if we have position data
        if positions:
            try:
                # Convert positions to returns for risk calculation
                returns = self._extract_returns_from_positions(positions)
                if len(returns) >= 30:
                    risk_metrics = self.risk_calculator.calculate_comprehensive_risk_metrics(
                        np.array(returns),
                        np.array([p.get('equity', 10000) for p in positions])
                    )
                    session.risk_metrics = risk_metrics

                    # Generate risk-based suggestions
                    risk_suggestions = await self.suggestion_generators.generate_risk_suggestions(
                        risk_metrics, context, session.session_id)
                    suggestions.extend(risk_suggestions)

            except Exception as e:
                logger.error(f"Risk calculation error: {e}")

        # Generate trading-specific suggestions
        trading_suggestions = await self.suggestion_generators.generate_trading_suggestions(
            context, session.session_id)
        suggestions.extend(trading_suggestions)

        return suggestions

    def _extract_returns_from_positions(self, positions: List[Dict[str, Any]]) -> List[float]:
        """
        Extract return series from position data.

        Navigation:
        ├── Used by: process()
        └── Related: TradingRobotApp position data structures
        """
        returns = []
        for position in positions:
            if 'return' in position:
                returns.append(position['return'])
            elif 'pnl' in position and 'initial_value' in position:
                initial = position['initial_value']
                if initial > 0:
                    returns.append(position['pnl'] / initial)

        return returns if returns else [0.0]


class CollaborationContextProcessor(ContextProcessor):
    """
    Processes collaborative context for real-time collaboration.

    Navigation:
    ├── Used by: AIContextEngine._process_context()
    ├── Related: WebSocket collaboration features, user session management
    └── Documentation: docs/PHASE5_AI_CONTEXT_ENGINE.md#collaboration-features
    """

    async def process(self, session: ContextSession) -> List[ContextSuggestion]:
        """
        Process collaborative context for real-time collaboration.

        Navigation:
        ├── Related: ai_context_websocket.py collaboration features
        └── Uses: session collaborators data, current activity tracking
        """
        context = session.context_data
        collaborators = context.get('collaborators', [])
        current_activity = context.get('current_activity', '')

        suggestions = []

        # Generate collaboration suggestions
        if len(collaborators) > 1:
            collab_suggestion = ContextSuggestion(
                suggestion_id=f"collab_{session.session_id}_{int(time.time())}",
                session_id=session.session_id,
                suggestion_type="collaboration",
                confidence_score=0.85,
                content={
                    "action": "suggest_collaborative_action",
                    "collaborators": collaborators,
                    "suggestion": f"Consider coordinating with {len(collaborators)} other collaborators on {current_activity}"
                },
                reasoning="Multiple collaborators detected - suggesting coordination opportunities",
                timestamp=datetime.now()
            )
            suggestions.append(collab_suggestion)

        return suggestions


class AnalysisContextProcessor(ContextProcessor):
    """
    Processes analytical context for intelligent insights.

    Navigation:
    ├── Used by: AIContextEngine._process_context()
    ├── Depends on: PatternAnalysisEngine from core.analytics.intelligence
    └── Related: data analysis workflows, pattern recognition systems
    """

    async def process(self, session: ContextSession) -> List[ContextSuggestion]:
        """
        Process analytical context for intelligent insights.

        Navigation:
        ├── Uses: PatternAnalysisEngine.analyze_patterns()
        └── Related: data visualization components, analytical dashboards
        """
        from src.core.analytics.intelligence.pattern_analysis_engine import PatternAnalysisEngine

        context = session.context_data
        data_points = context.get('data_points', [])

        if not data_points:
            return []

        # Use pattern analysis for insights
        try:
            pattern_analyzer = PatternAnalysisEngine()
            patterns = await pattern_analyzer.analyze_patterns(data_points)

            if patterns:
                analysis_suggestion = ContextSuggestion(
                    suggestion_id=f"analysis_{session.session_id}_{int(time.time())}",
                    session_id=session.session_id,
                    suggestion_type="insight",
                    confidence_score=0.78,
                    content={
                        "action": "show_pattern_insights",
                        "patterns": patterns,
                        "data_points": len(data_points)
                    },
                    reasoning=f"Pattern analysis detected {len(patterns)} significant patterns in {len(data_points)} data points",
                    timestamp=datetime.now()
                )
                return [analysis_suggestion]

        except Exception as e:
            logger.error(f"Pattern analysis error: {e}")

        return []


class RiskContextProcessor(ContextProcessor):
    """
    Processes risk-focused context.

    Navigation:
    ├── Used by: AIContextEngine._process_context()
    ├── Related: Risk monitoring dashboards, compliance systems
    └── Documentation: docs/PHASE5_AI_CONTEXT_ENGINE.md#risk-monitoring
    """

    async def process(self, session: ContextSession) -> List[ContextSuggestion]:
        """
        Process risk-focused context.

        Navigation:
        ├── Related: risk_websocket_server.py real-time risk streaming
        └── Uses: risk indicators, monitoring thresholds
        """
        context = session.context_data
        risk_indicators = context.get('risk_indicators', [])

        suggestions = []

        # Generate risk monitoring suggestions
        if risk_indicators:
            risk_suggestion = ContextSuggestion(
                suggestion_id=f"risk_monitor_{session.session_id}_{int(time.time())}",
                session_id=session.session_id,
                suggestion_type="risk_alert",
                confidence_score=0.92,
                content={
                    "action": "enhance_risk_monitoring",
                    "indicators": risk_indicators,
                    "recommendation": "Consider implementing additional risk monitoring for these indicators"
                },
                reasoning=f"Risk context detected with {len(risk_indicators)} risk indicators requiring attention",
                timestamp=datetime.now()
            )
            suggestions.append(risk_suggestion)

        return suggestions