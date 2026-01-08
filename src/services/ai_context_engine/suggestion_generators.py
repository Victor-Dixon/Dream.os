#!/usr/bin/env python3
"""
AI Context Engine Suggestion Generators
=====================================

AI-powered suggestion generation logic.

<!-- SSOT Domain: ai_context -->

Navigation References:
├── Related Files:
│   ├── Main Engine → ai_context_engine.py
│   ├── Context Processors → context_processors.py
│   ├── Data Models → models.py
│   └── Risk Calculator → src/services/risk_analytics/risk_calculator_service.py
├── Documentation:
│   └── Phase 5 Architecture → docs/PHASE5_AI_CONTEXT_ENGINE.md
└── Testing:
    └── Integration Tests → tests/integration/test_ai_context_engine.py

Classes:
- SuggestionGenerators: Collection of suggestion generation methods
"""

import time
from typing import List, Dict, Any
from datetime import datetime
import numpy as np

from .models import ContextSuggestion


class SuggestionGenerators:
    """
    Collection of AI-powered suggestion generation methods.

    Navigation:
    ├── Used by: ContextProcessor subclasses
    ├── Depends on: RiskMetrics from risk_calculator_service.py
    └── Related: AI service integration, pattern analysis results
    """

    async def generate_risk_suggestions(self, risk_metrics, context: Dict[str, Any],
                                      session_id: str) -> List[ContextSuggestion]:
        """
        Generate risk-based suggestions.

        Navigation:
        ├── Used by: TradingContextProcessor.process()
        ├── Depends on: RiskMetrics data structure
        └── Related: risk monitoring thresholds, portfolio optimization strategies
        """
        suggestions = []

        # High VaR alert
        if risk_metrics.var_95 > 0.15:  # 15% VaR threshold
            var_suggestion = ContextSuggestion(
                suggestion_id=f"var_alert_{int(time.time())}",
                session_id=session_id,
                suggestion_type="risk_alert",
                confidence_score=0.95,
                content={
                    "action": "reduce_portfolio_risk",
                    "metric": "var_95",
                    "value": risk_metrics.var_95,
                    "threshold": 0.15,
                    "suggestion": "Consider reducing position sizes or adding diversification"
                },
                reasoning=f"VaR (95%) of {risk_metrics.var_95:.1%} exceeds safe threshold",
                timestamp=datetime.now()
            )
            suggestions.append(var_suggestion)

        # Sharpe ratio optimization
        if risk_metrics.sharpe_ratio < 1.0:
            sharpe_suggestion = ContextSuggestion(
                suggestion_id=f"sharpe_opt_{int(time.time())}",
                session_id=session_id,
                suggestion_type="optimization",
                confidence_score=0.88,
                content={
                    "action": "optimize_portfolio",
                    "metric": "sharpe_ratio",
                    "value": risk_metrics.sharpe_ratio,
                    "target": 1.0,
                    "suggestion": "Portfolio optimization could improve risk-adjusted returns"
                },
                reasoning=f"Sharpe ratio of {risk_metrics.sharpe_ratio:.2f} below target of 1.0",
                timestamp=datetime.now()
            )
            suggestions.append(sharpe_suggestion)

        return suggestions

    async def generate_trading_suggestions(self, context: Dict[str, Any],
                                         session_id: str) -> List[ContextSuggestion]:
        """
        Generate trading-specific suggestions.

        Navigation:
        ├── Used by: TradingContextProcessor.process()
        ├── Related: market data APIs, volatility indicators
        └── Uses: market_volatility context data, timing strategies
        """
        suggestions = []

        # Market timing suggestions based on volatility
        volatility = context.get('market_volatility', 0)
        if volatility > 0.25:  # High volatility
            timing_suggestion = ContextSuggestion(
                suggestion_id=f"timing_{int(time.time())}",
                session_id=session_id,
                suggestion_type="action",
                confidence_score=0.75,
                content={
                    "action": "review_market_timing",
                    "volatility": volatility,
                    "suggestion": "High market volatility detected - consider defensive positioning"
                },
                reasoning=f"Market volatility at {volatility:.1%} suggests caution",
                timestamp=datetime.now()
            )
            suggestions.append(timing_suggestion)

        return suggestions