#!/usr/bin/env python3
"""
Risk Calculator Service
=======================

A standalone service for calculating advanced risk metrics for trading performance.

<!-- SSOT Domain: analytics -->

Navigation References:
├── Related Files:
│   ├── API Endpoints → src/services/risk_analytics/risk_api_endpoints.py
│   ├── WebSocket Server → src/services/risk_analytics/risk_websocket_server.py
│   ├── Risk Integration → src/web/static/js/trading-robot/risk-dashboard-integration.js
│   ├── Trading Dashboard → src/web/static/js/trading-robot/trading-dashboard.js
│   ├── Database Schema → database/migrations/phase2_2_risk_analytics_schema.sql
│   └── Dashboard UI → docs/analytics/risk_dashboard.html
├── Documentation:
│   ├── Architecture → docs/analytics/TRADINGROBOTPLUG_ANALYTICS_ARCHITECTURE.md
│   ├── Integration Demo → docs/analytics/trading_robot_risk_integration_demo.html
│   └── Phase 2.2 Guide → docs/analytics/AGENT2_PHASE2_GUIDANCE.md
└── Testing:
    └── Unit Tests → tests/unit/services/test_risk_*.py

Bidirectional Links:
├── From Code to Docs:
│   ├── This service → docs/analytics/TRADINGROBOTPLUG_ANALYTICS_ARCHITECTURE.md
│   ├── This service → docs/analytics/risk_dashboard.html
│   └── This service → docs/analytics/trading_robot_risk_integration_demo.html
└── From Docs to Code:
    ├── docs/analytics/TRADINGROBOTPLUG_ANALYTICS_ARCHITECTURE.md → This service
    ├── docs/analytics/risk_dashboard.html → This service
    └── docs/analytics/trading_robot_risk_integration_demo.html → This service

Features:
- Value at Risk (VaR) calculations
- Conditional VaR (CVaR) calculations
- Sharpe Ratio calculations
- Maximum Drawdown tracking
- Risk-Adjusted Returns (Calmar, Sortino, Information ratios)

Author: Agent-5 (Business Intelligence Specialist)
Date: 2025-12-29
Phase: Phase 2.2 - Risk Analytics
"""

import logging
import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime, timedelta
from dataclasses import dataclass
from abc import ABC, abstractmethod


logger = logging.getLogger(__name__)


@dataclass
class RiskMetrics:
    """Container for risk calculation results."""
    var_95: float
    cvar_95: float
    sharpe_ratio: float
    max_drawdown: float
    calmar_ratio: float
    sortino_ratio: float
    information_ratio: float
    calculation_date: datetime
    confidence_level: float = 0.95


@dataclass
class RiskAlert:
    """Container for risk alerts."""
    alert_type: str
    threshold_value: float
    current_value: float
    severity: str
    message: str
    user_id: int
    strategy_id: Optional[str] = None


class RiskCalculatorBase(ABC):
    """Base class for risk calculation methods."""

    def __init__(self, confidence_level: float = 0.95):
        self.confidence_level = confidence_level

    @abstractmethod
    def calculate_var(self, returns: np.ndarray) -> float:
        """Calculate Value at Risk."""
        pass

    @abstractmethod
    def calculate_cvar(self, returns: np.ndarray, var_value: float) -> float:
        """Calculate Conditional VaR."""
        pass


class HistoricalSimulationCalculator(RiskCalculatorBase):
    """Historical simulation method for VaR and CVaR calculations."""

    def calculate_var(self, returns: np.ndarray) -> float:
        """Calculate VaR using historical simulation."""
        if len(returns) < 30:
            logger.warning(f"Insufficient data for VaR calculation: {len(returns)} returns")
            return 0.0

        # Sort returns in ascending order (worst to best)
        sorted_returns = np.sort(returns)

        # Find the return at the confidence level percentile
        var_index = int((1 - self.confidence_level) * len(sorted_returns))
        var_value = -sorted_returns[var_index]  # Convert to positive loss

        return var_value

    def calculate_cvar(self, returns: np.ndarray, var_value: float) -> float:
        """Calculate CVaR (Expected Shortfall) beyond VaR threshold."""
        if len(returns) < 30:
            logger.warning(f"Insufficient data for CVaR calculation: {len(returns)} returns")
            return 0.0

        # Find returns that exceed the VaR threshold (worse than VaR)
        losses = -returns  # Convert returns to losses
        var_losses = losses[losses >= var_value]

        if len(var_losses) == 0:
            return var_value  # If no losses exceed VaR, CVaR equals VaR

        # Calculate average of losses beyond VaR
        cvar_value = np.mean(var_losses)
        return cvar_value


class RiskCalculatorService:
    """Main risk calculator service implementing all risk metrics."""

    def __init__(self, risk_free_rate: float = 0.045):  # 4.5% default (approx 10-year Treasury)
        self.risk_free_rate = risk_free_rate
        self.var_calculator = HistoricalSimulationCalculator()

    def calculate_sharpe_ratio(self, returns: np.ndarray, annualize: bool = True) -> float:
        """Calculate Sharpe Ratio."""
        if len(returns) < 30:
            return 0.0

        # Calculate annualized return and volatility if requested
        if annualize:
            # Assuming daily returns, annualize to 252 trading days
            avg_return = np.mean(returns) * 252
            volatility = np.std(returns) * np.sqrt(252)
            risk_free_annual = self.risk_free_rate
        else:
            avg_return = np.mean(returns)
            volatility = np.std(returns)
            risk_free_annual = self.risk_free_rate / 252  # Daily risk-free rate

        if volatility == 0:
            return 0.0

        sharpe_ratio = (avg_return - risk_free_annual) / volatility
        return sharpe_ratio

    def calculate_max_drawdown(self, equity_curve: np.ndarray) -> float:
        """Calculate maximum drawdown from equity curve."""
        if len(equity_curve) < 2:
            return 0.0

        # Calculate running maximum
        running_max = np.maximum.accumulate(equity_curve)

        # Calculate drawdown
        drawdown = (running_max - equity_curve) / running_max

        # Find maximum drawdown
        max_drawdown = np.max(drawdown)
        return max_drawdown

    def calculate_sortino_ratio(self, returns: np.ndarray, annualize: bool = True) -> float:
        """Calculate Sortino Ratio (downside deviation only)."""
        if len(returns) < 30:
            return 0.0

        # Calculate downside returns (negative returns only)
        downside_returns = returns[returns < 0]

        if len(downside_returns) == 0:
            return float("inf")  # No downside risk

        # Calculate downside deviation
        downside_deviation = np.std(downside_returns)

        if downside_deviation == 0:
            return float("inf")

        # Calculate average return
        if annualize:
            avg_return = np.mean(returns) * 252
            risk_free_annual = self.risk_free_rate
            downside_deviation_annual = downside_deviation * np.sqrt(252)
        else:
            avg_return = np.mean(returns)
            risk_free_annual = self.risk_free_rate / 252
            downside_deviation_annual = downside_deviation

        sortino_ratio = (avg_return - risk_free_annual) / downside_deviation_annual
        return sortino_ratio

    def calculate_calmar_ratio(self, returns: np.ndarray, max_drawdown: float) -> float:
        """Calculate Calmar Ratio (annual return / max drawdown)."""
        if len(returns) < 30 or max_drawdown <= 0:
            return 0.0

        # Calculate annualized return
        annual_return = np.mean(returns) * 252

        calmar_ratio = annual_return / max_drawdown
        return calmar_ratio

    def calculate_information_ratio(self, strategy_returns: np.ndarray, benchmark_returns: np.ndarray) -> float:
        """Calculate Information Ratio (active return / tracking error)."""
        if len(strategy_returns) != len(benchmark_returns) or len(strategy_returns) < 30:
            return 0.0

        # Calculate active returns (strategy - benchmark)
        active_returns = strategy_returns - benchmark_returns

        # Calculate tracking error (standard deviation of active returns)
        tracking_error = np.std(active_returns)

        if tracking_error == 0:
            return 0.0

        # Calculate annualized information ratio
        annual_active_return = np.mean(active_returns) * 252
        annual_tracking_error = tracking_error * np.sqrt(252)

        information_ratio = annual_active_return / annual_tracking_error
        return information_ratio

    def calculate_comprehensive_risk_metrics(
        self,
        returns: np.ndarray,
        equity_curve: np.ndarray,
        benchmark_returns: Optional[np.ndarray] = None,
    ) -> RiskMetrics:
        """Calculate all supported risk metrics."""
        if len(returns) < 30 or len(equity_curve) < 2:
            return self._create_empty_metrics()

        var_95 = self.var_calculator.calculate_var(returns)
        cvar_95 = self.var_calculator.calculate_cvar(returns, var_95)
        sharpe_ratio = self.calculate_sharpe_ratio(returns)
        max_drawdown = self.calculate_max_drawdown(equity_curve)
        calmar_ratio = self.calculate_calmar_ratio(returns, max_drawdown)
        sortino_ratio = self.calculate_sortino_ratio(returns)
        information_ratio = 0.0
        if benchmark_returns is not None:
            information_ratio = self.calculate_information_ratio(returns, benchmark_returns)

        return RiskMetrics(
            var_95=var_95,
            cvar_95=cvar_95,
            sharpe_ratio=sharpe_ratio,
            max_drawdown=max_drawdown,
            calmar_ratio=calmar_ratio,
            sortino_ratio=sortino_ratio,
            information_ratio=information_ratio,
            calculation_date=datetime.now(),
            confidence_level=self.var_calculator.confidence_level,
        )

    def check_risk_thresholds(
        self,
        metrics: RiskMetrics,
        thresholds: Dict[str, float],
        user_id: int = 0,
        strategy_id: Optional[str] = None,
    ) -> List[RiskAlert]:
        """Check metrics against thresholds and return alerts."""
        alerts: List[RiskAlert] = []

        var_threshold = thresholds.get("var_95")
        if var_threshold is not None and metrics.var_95 > var_threshold:
            alerts.append(
                RiskAlert(
                    alert_type="var_95",
                    threshold_value=var_threshold,
                    current_value=metrics.var_95,
                    severity="high",
                    message=f"VaR exceeded threshold ({metrics.var_95:.2%} > {var_threshold:.2%})",
                    user_id=user_id,
                    strategy_id=strategy_id,
                )
            )

        drawdown_threshold = thresholds.get("max_drawdown")
        if drawdown_threshold is not None and metrics.max_drawdown > drawdown_threshold:
            alerts.append(
                RiskAlert(
                    alert_type="max_drawdown",
                    threshold_value=drawdown_threshold,
                    current_value=metrics.max_drawdown,
                    severity="high",
                    message=(
                        f"Max drawdown exceeded threshold "
                        f"({metrics.max_drawdown:.2%} > {drawdown_threshold:.2%})"
                    ),
                    user_id=user_id,
                    strategy_id=strategy_id,
                )
            )

        sharpe_min = thresholds.get("sharpe_ratio_min")
        if sharpe_min is not None and metrics.sharpe_ratio < sharpe_min:
            alerts.append(
                RiskAlert(
                    alert_type="sharpe_ratio",
                    threshold_value=sharpe_min,
                    current_value=metrics.sharpe_ratio,
                    severity="medium",
                    message=(
                        f"Sharpe ratio below threshold ({metrics.sharpe_ratio:.2f} < {sharpe_min:.2f})"
                    ),
                    user_id=user_id,
                    strategy_id=strategy_id,
                )
            )

        return alerts

    def _create_empty_metrics(self) -> RiskMetrics:
        """Create empty risk metrics for insufficient data cases."""
        return RiskMetrics(
            var_95=0.0,
            cvar_95=0.0,
            sharpe_ratio=0.0,
            max_drawdown=0.0,
            calmar_ratio=0.0,
            sortino_ratio=0.0,
            information_ratio=0.0,
            calculation_date=datetime.now(),
            confidence_level=self.var_calculator.confidence_level,
        )


# Example usage and testing
if __name__ == "__main__":
    # Initialize service
    risk_service = RiskCalculatorService(risk_free_rate=0.045)

    # Generate sample data for testing
    np.random.seed(42)
    n_days = 252  # One year of trading days

    # Simulate daily returns (normal distribution with slight positive bias)
    returns = np.random.normal(0.001, 0.02, n_days)  # 0.1% average return, 2% volatility

    # Create equity curve from returns
    equity_curve = np.cumprod(1 + returns) * 10000  # Starting with $10,000

    # Calculate comprehensive risk metrics
    metrics = risk_service.calculate_comprehensive_risk_metrics(returns, equity_curve)

    print("=== Risk Calculator Service Test Results ===")
    print(f"VaR (95%): {metrics.var_95:.2%}")
    print(f"CVaR (95%): {metrics.cvar_95:.2%}")
    print(f"Sharpe Ratio: {metrics.sharpe_ratio:.2f}")
    print(f"Maximum Drawdown: {metrics.max_drawdown:.2%}")
    print(f"Calmar Ratio: {metrics.calmar_ratio:.2f}")
    print(f"Sortino Ratio: {metrics.sortino_ratio:.2f}")
    print(f"Information Ratio: {metrics.information_ratio:.2f}")

    # Test risk alerts
    thresholds = {
        'var_95': 0.05,  # 5% VaR threshold
        'max_drawdown': 0.20,  # 20% max drawdown threshold
        'sharpe_ratio_min': 1.0  # Minimum Sharpe ratio
    }

    alerts = risk_service.check_risk_thresholds(metrics, thresholds)
    print(f"\nRisk Alerts Generated: {len(alerts)}")
    for alert in alerts:
        print(f"- {alert.severity.upper()}: {alert.message}")

    print("\n✅ Risk Calculator Service implementation complete!")

