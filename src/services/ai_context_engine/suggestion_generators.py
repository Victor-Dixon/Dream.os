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
<<<<<<< HEAD
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

try:
    import numpy as np
except ImportError:
    np = None
    logging.warning("NumPy not available, some suggestion calculations may be limited")

from .models import ContextSuggestion

logger = logging.getLogger(__name__)

=======
from typing import List, Dict, Any
from datetime import datetime
import numpy as np

from .models import ContextSuggestion

>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1

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
<<<<<<< HEAD
        Generate risk-based suggestions with enhanced error handling and validation.
=======
        Generate risk-based suggestions.
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1

        Navigation:
        ├── Used by: TradingContextProcessor.process()
        ├── Depends on: RiskMetrics data structure
        └── Related: risk monitoring thresholds, portfolio optimization strategies
        """
        suggestions = []

<<<<<<< HEAD
        try:
            # Validate inputs
            if not risk_metrics:
                logger.warning("No risk metrics provided for suggestion generation")
                return suggestions

            if not session_id or not isinstance(session_id, str):
                logger.warning("Invalid session_id for risk suggestions")
                return suggestions

            if not isinstance(context, dict):
                logger.warning("Invalid context format for risk suggestions")
                context = {}

            # High VaR alert with validation
            if hasattr(risk_metrics, 'var_95') and risk_metrics.var_95 is not None:
                try:
                    var_95 = float(risk_metrics.var_95)
                    if var_95 > 0.15:  # 15% VaR threshold
                        var_suggestion = ContextSuggestion(
                            suggestion_id=f"var_alert_{session_id}_{int(time.time())}",
                            session_id=session_id,
                            suggestion_type="risk_alert",
                            confidence_score=0.95,
                            content={
                                "action": "reduce_portfolio_risk",
                                "metric": "var_95",
                                "value": var_95,
                                "threshold": 0.15,
                                "suggestion": "Consider reducing position sizes or adding diversification"
                            },
                            reasoning=f"VaR (95%) of {var_95:.1%} exceeds safe threshold",
                            timestamp=datetime.now()
                        )
                        if self._validate_suggestion(var_suggestion):
                            suggestions.append(var_suggestion)
                            logger.info(f"Generated VaR alert suggestion for session {session_id}")
                except (ValueError, AttributeError) as e:
                    logger.warning(f"Error processing VaR metric: {e}")

            # Sharpe ratio optimization with validation
            if hasattr(risk_metrics, 'sharpe_ratio') and risk_metrics.sharpe_ratio is not None:
                try:
                    sharpe_ratio = float(risk_metrics.sharpe_ratio)
                    if sharpe_ratio < 1.0:
                        sharpe_suggestion = ContextSuggestion(
                            suggestion_id=f"sharpe_opt_{session_id}_{int(time.time())}",
                            session_id=session_id,
                            suggestion_type="optimization",
                            confidence_score=0.88,
                            content={
                                "action": "optimize_portfolio",
                                "metric": "sharpe_ratio",
                                "value": sharpe_ratio,
                                "target": 1.0,
                                "suggestion": "Portfolio optimization could improve risk-adjusted returns"
                            },
                            reasoning=f"Sharpe ratio of {sharpe_ratio:.2f} below target of 1.0",
                            timestamp=datetime.now()
                        )
                        if self._validate_suggestion(sharpe_suggestion):
                            suggestions.append(sharpe_suggestion)
                            logger.info(f"Generated Sharpe ratio optimization suggestion for session {session_id}")
                except (ValueError, AttributeError) as e:
                    logger.warning(f"Error processing Sharpe ratio metric: {e}")

            # Additional risk metrics suggestions
            try:
                additional_suggestions = await self._generate_additional_risk_suggestions(risk_metrics, context, session_id)
                for suggestion in additional_suggestions:
                    if self._validate_suggestion(suggestion):
                        suggestions.append(suggestion)
            except Exception as e:
                logger.error(f"Error generating additional risk suggestions: {e}")

        except Exception as e:
            logger.error(f"Error in risk suggestion generation: {e}")

        logger.info(f"Generated {len(suggestions)} risk-based suggestions for session {session_id}")
        return suggestions

    async def _generate_additional_risk_suggestions(self, risk_metrics, context: Dict[str, Any],
                                                  session_id: str) -> List[ContextSuggestion]:
        """
        Generate additional risk-based suggestions beyond VaR and Sharpe ratio.

        Args:
            risk_metrics: Risk metrics object
            context: Session context
            session_id: Session identifier

        Returns:
            List of additional risk suggestions
        """
        suggestions = []

        try:
            # Maximum drawdown alert
            if hasattr(risk_metrics, 'max_drawdown') and risk_metrics.max_drawdown is not None:
                try:
                    max_drawdown = float(risk_metrics.max_drawdown)
                    if max_drawdown > 0.20:  # 20% drawdown threshold
                        drawdown_suggestion = ContextSuggestion(
                            suggestion_id=f"drawdown_alert_{session_id}_{int(time.time())}",
                            session_id=session_id,
                            suggestion_type="risk_alert",
                            confidence_score=0.92,
                            content={
                                "action": "implement_risk_management",
                                "metric": "max_drawdown",
                                "value": max_drawdown,
                                "threshold": 0.20,
                                "suggestion": "Consider implementing stop-loss orders or position sizing limits"
                            },
                            reasoning=f"Maximum drawdown of {max_drawdown:.1%} exceeds risk threshold",
                            timestamp=datetime.now()
                        )
                        if self._validate_suggestion(drawdown_suggestion):
                            suggestions.append(drawdown_suggestion)
                except (ValueError, AttributeError):
                    pass

            # Volatility alert
            if hasattr(risk_metrics, 'volatility') and risk_metrics.volatility is not None:
                try:
                    volatility = float(risk_metrics.volatility)
                    if volatility > 0.30:  # 30% volatility threshold
                        volatility_suggestion = ContextSuggestion(
                            suggestion_id=f"volatility_alert_{session_id}_{int(time.time())}",
                            session_id=session_id,
                            suggestion_type="risk_alert",
                            confidence_score=0.85,
                            content={
                                "action": "reduce_volatility_exposure",
                                "metric": "volatility",
                                "value": volatility,
                                "threshold": 0.30,
                                "suggestion": "Consider hedging strategies or reducing leverage"
                            },
                            reasoning=f"Portfolio volatility of {volatility:.1%} indicates high risk",
                            timestamp=datetime.now()
                        )
                        if self._validate_suggestion(volatility_suggestion):
                            suggestions.append(volatility_suggestion)
                except (ValueError, AttributeError):
                    pass

        except Exception as e:
            logger.error(f"Error in additional risk suggestions: {e}")

        return suggestions

    def _validate_suggestion(self, suggestion: Any) -> bool:
        """
        Validate suggestion format and content.

        Args:
            suggestion: Suggestion to validate

        Returns:
            True if suggestion is valid
        """
        if not suggestion:
            return False

        required_attrs = ['suggestion_id', 'session_id', 'suggestion_type', 'confidence_score', 'content']
        if not hasattr(suggestion, '__dict__'):
            return False

        suggestion_dict = suggestion.__dict__
        for attr in required_attrs:
            if attr not in suggestion_dict:
                return False

        # Validate confidence score
        confidence = suggestion_dict.get('confidence_score', 0)
        if not isinstance(confidence, (int, float)) or not (0 <= confidence <= 1):
            return False

        # Validate session_id
        if not suggestion_dict.get('session_id') or not isinstance(suggestion_dict['session_id'], str):
            return False

        return True

    async def generate_trading_suggestions(self, context: Dict[str, Any],
                                         session_id: str) -> List[ContextSuggestion]:
        """
        Generate trading-specific suggestions with enhanced error handling and validation.
=======
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
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1

        Navigation:
        ├── Used by: TradingContextProcessor.process()
        ├── Related: market data APIs, volatility indicators
        └── Uses: market_volatility context data, timing strategies
        """
        suggestions = []

<<<<<<< HEAD
        try:
            # Validate inputs
            if not session_id or not isinstance(session_id, str):
                logger.warning("Invalid session_id for trading suggestions")
                return suggestions

            if not isinstance(context, dict):
                logger.warning("Invalid context format for trading suggestions")
                context = {}

            # Market timing suggestions based on volatility
            volatility = context.get('market_volatility', 0)
            if volatility is not None:
                try:
                    volatility = float(volatility)
                    if volatility > 0.25:  # High volatility threshold
                        timing_suggestion = ContextSuggestion(
                            suggestion_id=f"timing_{session_id}_{int(time.time())}",
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
                        if self._validate_suggestion(timing_suggestion):
                            suggestions.append(timing_suggestion)
                            logger.info(f"Generated market timing suggestion for session {session_id}")
                except (ValueError, TypeError) as e:
                    logger.warning(f"Error processing volatility data: {e}")

            # Position sizing suggestions
            try:
                position_suggestions = await self._generate_position_suggestions(context, session_id)
                for suggestion in position_suggestions:
                    if self._validate_suggestion(suggestion):
                        suggestions.append(suggestion)
            except Exception as e:
                logger.error(f"Error generating position suggestions: {e}")

            # Market condition analysis
            try:
                market_suggestions = await self._generate_market_condition_suggestions(context, session_id)
                for suggestion in market_suggestions:
                    if self._validate_suggestion(suggestion):
                        suggestions.append(suggestion)
            except Exception as e:
                logger.error(f"Error generating market condition suggestions: {e}")

        except Exception as e:
            logger.error(f"Error in trading suggestion generation: {e}")

        logger.info(f"Generated {len(suggestions)} trading suggestions for session {session_id}")
        return suggestions

    async def _generate_position_suggestions(self, context: Dict[str, Any],
                                          session_id: str) -> List[ContextSuggestion]:
        """
        Generate position sizing and risk management suggestions.

        Args:
            context: Trading context
            session_id: Session identifier

        Returns:
            List of position-related suggestions
        """
        suggestions = []

        try:
            positions = context.get('positions', [])
            if not isinstance(positions, list):
                positions = []

            # Check for over-concentration
            if len(positions) > 0:
                # Calculate position concentrations
                total_value = sum(p.get('market_value', 0) for p in positions if isinstance(p, dict))
                if total_value > 0:
                    for position in positions:
                        if isinstance(position, dict):
                            market_value = position.get('market_value', 0)
                            concentration = market_value / total_value if market_value > 0 else 0

                            if concentration > 0.3:  # 30% concentration threshold
                                concentration_suggestion = ContextSuggestion(
                                    suggestion_id=f"concentration_{session_id}_{int(time.time())}",
                                    session_id=session_id,
                                    suggestion_type="risk_management",
                                    confidence_score=0.80,
                                    content={
                                        "action": "diversify_portfolio",
                                        "concentration": concentration,
                                        "symbol": position.get('symbol', 'Unknown'),
                                        "suggestion": "Position represents significant portfolio concentration - consider diversification"
                                    },
                                    reasoning=f"Position concentration of {concentration:.1%} exceeds diversification threshold",
                                    timestamp=datetime.now()
                                )
                                if self._validate_suggestion(concentration_suggestion):
                                    suggestions.append(concentration_suggestion)

        except Exception as e:
            logger.error(f"Error in position suggestions: {e}")

        return suggestions

    async def _generate_market_condition_suggestions(self, context: Dict[str, Any],
                                                   session_id: str) -> List[ContextSuggestion]:
        """
        Generate suggestions based on market conditions.

        Args:
            context: Trading context
            session_id: Session identifier

        Returns:
            List of market condition suggestions
        """
        suggestions = []

        try:
            # Trend analysis suggestions
            trend = context.get('market_trend', '')
            if trend and isinstance(trend, str):
                if trend.lower() in ['bullish', 'bearish']:
                    trend_suggestion = ContextSuggestion(
                        suggestion_id=f"trend_{session_id}_{int(time.time())}",
                        session_id=session_id,
                        suggestion_type="strategy",
                        confidence_score=0.70,
                        content={
                            "action": "align_with_trend",
                            "trend": trend,
                            "suggestion": f"Market showing {trend} trend - consider trend-following strategies"
                        },
                        reasoning=f"Market trend analysis indicates {trend} conditions",
                        timestamp=datetime.now()
                    )
                    if self._validate_suggestion(trend_suggestion):
                        suggestions.append(trend_suggestion)

            # Volume analysis
            volume = context.get('trading_volume', 0)
            if volume is not None:
                try:
                    volume = float(volume)
                    avg_volume = context.get('avg_volume', 0)
                    if avg_volume and volume > avg_volume * 2:  # 2x average volume
                        volume_suggestion = ContextSuggestion(
                            suggestion_id=f"volume_{session_id}_{int(time.time())}",
                            session_id=session_id,
                            suggestion_type="opportunity",
                            confidence_score=0.65,
                            content={
                                "action": "monitor_volume_spike",
                                "current_volume": volume,
                                "avg_volume": avg_volume,
                                "suggestion": "Unusual trading volume detected - monitor for significant moves"
                            },
                            reasoning=f"Trading volume {volume:.0f} exceeds 2x average volume",
                            timestamp=datetime.now()
                        )
                        if self._validate_suggestion(volume_suggestion):
                            suggestions.append(volume_suggestion)
                except (ValueError, TypeError):
                    pass

        except Exception as e:
            logger.error(f"Error in market condition suggestions: {e}")
=======
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
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1

        return suggestions