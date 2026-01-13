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

<<<<<<< HEAD
from ..core.logging_mixin import LoggingMixin

=======
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
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


<<<<<<< HEAD
class RiskCalculatorService(LoggingMixin):
=======
class RiskCalculatorService:
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
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
            return float('inf')  # No downside risk

        # Calculate downside deviation
        downside_deviation = np.std(downside_returns)

        if downside_deviation == 0:
            return float('inf')

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
        benchmark_returns: Optional[np.ndarray] = None
    ) -> RiskMetrics:
<<<<<<< HEAD
<<<<<<< HEAD
        """
        Calculate all comprehensive risk metrics with enhanced validation and error handling.
=======
        """
        Calculate all comprehensive risk metrics.
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1

        Navigation References:
        ├── Risk Metrics → See RiskMetrics dataclass above for output structure
        ├── WebSocket Streaming → src/services/risk_analytics/risk_websocket_server.py::_generate_live_risk_data()
        ├── Dashboard Display → src/web/static/js/trading-robot/risk-dashboard-integration.js::updateRiskMetrics()
        ├── Chart Visualization → docs/analytics/risk_dashboard.html#risk-metrics-display
        ├── Validation Testing → tests/unit/services/test_risk_calculator_service.py
        └── Performance Benchmark → docs/analytics/TRADINGROBOTPLUG_ANALYTICS_ARCHITECTURE.md#performance-requirements

        Complex processing pipeline:
        1. Statistical validation of input data
        2. VaR/CVaR calculation using Historical Simulation method
        3. Sharpe ratio with annualized returns/volatility
        4. Maximum drawdown from equity curve analysis
        5. Sortino ratio with downside deviation
        6. Calmar ratio combining return and drawdown
        7. Information ratio vs benchmark (if provided)
        """
<<<<<<< HEAD
        try:
            # Validate inputs
            validation_errors = self._validate_calculation_inputs(returns, equity_curve, benchmark_returns)
            if validation_errors:
                logger.warning(f"Risk calculation input validation failed: {', '.join(validation_errors)}")
                return self._create_empty_metrics()

            # Calculate VaR and CVaR with error handling
            try:
                var_95 = self.var_calculator.calculate_var(returns)
                cvar_95 = self.var_calculator.calculate_cvar(returns, var_95)
            except Exception as e:
                logger.error(f"VaR/CVaR calculation failed: {e}")
                var_95 = cvar_95 = 0.0

            # Calculate Sharpe Ratio with error handling
            try:
                sharpe_ratio = self.calculate_sharpe_ratio(returns)
            except Exception as e:
                logger.error(f"Sharpe ratio calculation failed: {e}")
                sharpe_ratio = 0.0

            # Calculate Maximum Drawdown with error handling
            try:
                max_drawdown = self.calculate_max_drawdown(equity_curve)
            except Exception as e:
                logger.error(f"Maximum drawdown calculation failed: {e}")
                max_drawdown = 0.0

            # Calculate Sortino Ratio with error handling
            try:
                sortino_ratio = self.calculate_sortino_ratio(returns)
            except Exception as e:
                logger.error(f"Sortino ratio calculation failed: {e}")
                sortino_ratio = 0.0

            # Calculate Calmar Ratio with error handling
            try:
                calmar_ratio = self.calculate_calmar_ratio(returns, max_drawdown)
            except Exception as e:
                logger.error(f"Calmar ratio calculation failed: {e}")
                calmar_ratio = 0.0

            # Calculate Information Ratio (if benchmark provided) with error handling
            information_ratio = 0.0
            if benchmark_returns is not None:
                try:
                    information_ratio = self.calculate_information_ratio(returns, benchmark_returns)
                except Exception as e:
                    logger.error(f"Information ratio calculation failed: {e}")

            metrics = RiskMetrics(
                var_95=var_95,
                cvar_95=cvar_95,
                sharpe_ratio=sharpe_ratio,
                max_drawdown=max_drawdown,
                calmar_ratio=calmar_ratio,
                sortino_ratio=sortino_ratio,
                information_ratio=information_ratio,
                calculation_date=datetime.now()
            )

            logger.info(f"Successfully calculated comprehensive risk metrics: VaR={var_95:.3f}, Sharpe={sharpe_ratio:.2f}")
            return metrics

        except Exception as e:
            logger.error(f"Comprehensive risk calculation failed: {e}")
            return self._create_empty_metrics()

    def _validate_calculation_inputs(self, returns: np.ndarray, equity_curve: np.ndarray,
                                   benchmark_returns: Optional[np.ndarray]) -> List[str]:
        """
        Validate inputs for comprehensive risk calculations.

        Args:
            returns: Array of returns
            equity_curve: Array of equity values
            benchmark_returns: Optional array of benchmark returns

        Returns:
            List of validation error messages (empty if valid)
        """
        errors = []

        # Validate returns
        if not isinstance(returns, np.ndarray):
            errors.append("returns must be a numpy array")
        elif len(returns) < 30:
            errors.append(f"insufficient returns data: {len(returns)} (minimum 30)")
        elif not np.isfinite(returns).all():
            errors.append("returns contains non-finite values")

        # Validate equity curve
        if not isinstance(equity_curve, np.ndarray):
            errors.append("equity_curve must be a numpy array")
        elif len(equity_curve) < 2:
            errors.append(f"insufficient equity data: {len(equity_curve)} (minimum 2)")
        elif not np.isfinite(equity_curve).all():
            errors.append("equity_curve contains non-finite values")
        elif np.any(equity_curve <= 0):
            errors.append("equity_curve contains non-positive values")

        # Validate benchmark returns if provided
        if benchmark_returns is not None:
            if not isinstance(benchmark_returns, np.ndarray):
                errors.append("benchmark_returns must be a numpy array")
            elif len(benchmark_returns) != len(returns):
                errors.append(f"benchmark_returns length mismatch: {len(benchmark_returns)} vs {len(returns)}")
            elif not np.isfinite(benchmark_returns).all():
                errors.append("benchmark_returns contains non-finite values")

        return errors
=======
        """Calculate all comprehensive risk metrics."""
=======
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
        if len(returns) < 30:
            logger.warning(f"Insufficient data for risk calculations: {len(returns)} returns")
            return self._create_empty_metrics()

        # Calculate VaR and CVaR
        var_95 = self.var_calculator.calculate_var(returns)
        cvar_95 = self.var_calculator.calculate_cvar(returns, var_95)

        # Calculate Sharpe Ratio
        sharpe_ratio = self.calculate_sharpe_ratio(returns)

        # Calculate Maximum Drawdown
        max_drawdown = self.calculate_max_drawdown(equity_curve)

        # Calculate Sortino Ratio
        sortino_ratio = self.calculate_sortino_ratio(returns)

        # Calculate Calmar Ratio
        calmar_ratio = self.calculate_calmar_ratio(returns, max_drawdown)

        # Calculate Information Ratio (if benchmark provided)
        if benchmark_returns is not None:
            information_ratio = self.calculate_information_ratio(returns, benchmark_returns)
        else:
            information_ratio = 0.0

        return RiskMetrics(
            var_95=var_95,
            cvar_95=cvar_95,
            sharpe_ratio=sharpe_ratio,
            max_drawdown=max_drawdown,
            calmar_ratio=calmar_ratio,
            sortino_ratio=sortino_ratio,
            information_ratio=information_ratio,
            calculation_date=datetime.now()
        )
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console

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
            calculation_date=datetime.now()
        )

<<<<<<< HEAD
    def check_risk_thresholds(self, metrics: RiskMetrics, thresholds: Dict[str, float],
                            user_id: int = 0, strategy_id: Optional[str] = None) -> List[RiskAlert]:
        """Check risk metrics against predefined thresholds and generate alerts with enhanced validation."""
        alerts = []

        try:
            # Validate inputs
            if not isinstance(metrics, RiskMetrics):
                logger.error("Invalid metrics object provided to check_risk_thresholds")
                return alerts

            if not isinstance(thresholds, dict):
                logger.error("Invalid thresholds format provided to check_risk_thresholds")
                return alerts

            # VaR Alert with validation
            if 'var_95' in thresholds and isinstance(thresholds['var_95'], (int, float)):
                try:
                    threshold = float(thresholds['var_95'])
                    if metrics.var_95 > threshold:
                        alerts.append(RiskAlert(
                            alert_type='var_threshold',
                            threshold_value=threshold,
                            current_value=metrics.var_95,
                            severity='high',
                            message=f'VaR (95%) of {metrics.var_95:.2%} exceeds threshold of {threshold:.2%}',
                            user_id=user_id,
                            strategy_id=strategy_id
                        ))
                        logger.info(f"Generated VaR alert for user {user_id}: {metrics.var_95:.3f} > {threshold:.3f}")
                except (ValueError, TypeError) as e:
                    logger.warning(f"Error processing VaR threshold: {e}")

            # Maximum Drawdown Alert with validation
            if 'max_drawdown' in thresholds and isinstance(thresholds['max_drawdown'], (int, float)):
                try:
                    threshold = float(thresholds['max_drawdown'])
                    if metrics.max_drawdown > threshold:
                        alerts.append(RiskAlert(
                            alert_type='drawdown_threshold',
                            threshold_value=threshold,
                            current_value=metrics.max_drawdown,
                            severity='critical',
                            message=f'Maximum drawdown of {metrics.max_drawdown:.2%} exceeds threshold of {threshold:.2%}',
                            user_id=user_id,
                            strategy_id=strategy_id
                        ))
                        logger.info(f"Generated drawdown alert for user {user_id}: {metrics.max_drawdown:.3f} > {threshold:.3f}")
                except (ValueError, TypeError) as e:
                    logger.warning(f"Error processing drawdown threshold: {e}")

            # Sharpe Ratio Alert (low Sharpe is concerning) with validation
            if 'sharpe_ratio_min' in thresholds and isinstance(thresholds['sharpe_ratio_min'], (int, float)):
                try:
                    threshold = float(thresholds['sharpe_ratio_min'])
                    if metrics.sharpe_ratio < threshold:
                        alerts.append(RiskAlert(
                            alert_type='sharpe_ratio_low',
                            threshold_value=threshold,
                            current_value=metrics.sharpe_ratio,
                            severity='medium',
                            message=f'Sharpe ratio of {metrics.sharpe_ratio:.2f} below minimum threshold of {threshold:.2f}',
                            user_id=user_id,
                            strategy_id=strategy_id
                        ))
                        logger.info(f"Generated Sharpe ratio alert for user {user_id}: {metrics.sharpe_ratio:.2f} < {threshold:.2f}")
                except (ValueError, TypeError) as e:
                    logger.warning(f"Error processing Sharpe ratio threshold: {e}")

            # Sortino Ratio Alert with validation
            if 'sortino_ratio_min' in thresholds and isinstance(thresholds['sortino_ratio_min'], (int, float)):
                try:
                    threshold = float(thresholds['sortino_ratio_min'])
                    if metrics.sortino_ratio < threshold and metrics.sortino_ratio != float('inf'):
                        alerts.append(RiskAlert(
                            alert_type='sortino_ratio_low',
                            threshold_value=threshold,
                            current_value=metrics.sortino_ratio,
                            severity='medium',
                            message=f'Sortino ratio of {metrics.sortino_ratio:.2f} below minimum threshold of {threshold:.2f}',
                            user_id=user_id,
                            strategy_id=strategy_id
                        ))
                        logger.info(f"Generated Sortino ratio alert for user {user_id}: {metrics.sortino_ratio:.2f} < {threshold:.2f}")
                except (ValueError, TypeError) as e:
                    logger.warning(f"Error processing Sortino ratio threshold: {e}")

            # CVaR Alert with validation
            if 'cvar_95' in thresholds and isinstance(thresholds['cvar_95'], (int, float)):
                try:
                    threshold = float(thresholds['cvar_95'])
                    if metrics.cvar_95 > threshold:
                        alerts.append(RiskAlert(
                            alert_type='cvar_threshold',
                            threshold_value=threshold,
                            current_value=metrics.cvar_95,
                            severity='high',
                            message=f'CVaR (95%) of {metrics.cvar_95:.2%} exceeds threshold of {threshold:.2%}',
                            user_id=user_id,
                            strategy_id=strategy_id
                        ))
                        logger.info(f"Generated CVaR alert for user {user_id}: {metrics.cvar_95:.3f} > {threshold:.3f}")
                except (ValueError, TypeError) as e:
                    logger.warning(f"Error processing CVaR threshold: {e}")

        except Exception as e:
            logger.error(f"Error in risk threshold checking: {e}")

        logger.info(f"Generated {len(alerts)} risk alerts for user {user_id}")
=======
    def check_risk_thresholds(self, metrics: RiskMetrics, thresholds: Dict[str, float]) -> List[RiskAlert]:
        """Check risk metrics against predefined thresholds and generate alerts."""
        alerts = []

        # VaR Alert
        if 'var_95' in thresholds and metrics.var_95 > thresholds['var_95']:
            alerts.append(RiskAlert(
                alert_type='var_threshold',
                threshold_value=thresholds['var_95'],
                current_value=metrics.var_95,
                severity='high',
                message=f'VaR (95%) of {metrics.var_95:.2%} exceeds threshold of {thresholds["var_95"]:.2%}',
                user_id=0  # To be set by caller
            ))

        # Maximum Drawdown Alert
        if 'max_drawdown' in thresholds and metrics.max_drawdown > thresholds['max_drawdown']:
            alerts.append(RiskAlert(
                alert_type='drawdown_threshold',
                threshold_value=thresholds['max_drawdown'],
                current_value=metrics.max_drawdown,
                severity='critical',
                message=f'Maximum drawdown of {metrics.max_drawdown:.2%} exceeds threshold of {thresholds["max_drawdown"]:.2%}',
                user_id=0  # To be set by caller
            ))

        # Sharpe Ratio Alert (low Sharpe is concerning)
        if 'sharpe_ratio_min' in thresholds and metrics.sharpe_ratio < thresholds['sharpe_ratio_min']:
            alerts.append(RiskAlert(
                alert_type='sharpe_ratio_low',
                threshold_value=thresholds['sharpe_ratio_min'],
                current_value=metrics.sharpe_ratio,
                severity='medium',
                message=f'Sharpe ratio of {metrics.sharpe_ratio:.2f} below minimum threshold of {thresholds["sharpe_ratio_min"]:.2f}',
                user_id=0  # To be set by caller
            ))

>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
        return alerts


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

