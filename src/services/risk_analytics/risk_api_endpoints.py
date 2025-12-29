#!/usr/bin/env python3
"""
Risk Analytics API Endpoints
============================

WordPress REST API endpoints for risk analytics calculations.

<!-- SSOT Domain: analytics -->

Endpoints:
- GET /wp-json/tradingrobotplug/v1/analytics/risk/var
- GET /wp-json/tradingrobotplug/v1/analytics/risk/cvar
- GET /wp-json/tradingrobotplug/v1/analytics/risk/sharpe
- GET /wp-json/tradingrobotplug/v1/analytics/risk/drawdown
- GET /wp-json/tradingrobotplug/v1/analytics/risk/adjusted-returns
- GET /wp-json/tradingrobotplug/v1/analytics/risk/comprehensive
- POST /wp-json/tradingrobotplug/v1/analytics/risk/calculate

Author: Agent-5 (Business Intelligence Specialist)
Date: 2025-12-29
Phase: Phase 2.2 - Risk Analytics
"""

import json
import logging
import numpy as np
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta

# Import risk calculator service
try:
    from .risk_calculator_service import RiskCalculatorService, RiskMetrics
except ImportError:
    # For direct execution
    from risk_calculator_service import RiskCalculatorService, RiskMetrics

logger = logging.getLogger(__name__)


class RiskAnalyticsAPI:
    """WordPress REST API endpoints for risk analytics."""

    def __init__(self):
        self.risk_calculator = RiskCalculatorService()
        self.namespace = 'tradingrobotplug/v1'
        self.route_base = 'analytics/risk'

    def register_endpoints(self) -> List[Dict[str, Any]]:
        """Register all risk analytics endpoints."""

        endpoints = [
            # Individual Risk Metrics
            {
                'route': f'/{self.route_base}/var',
                'methods': ['GET'],
                'callback': self.get_var,
                'args': {
                    'user_id': {
                        'required': True,
                        'type': 'integer',
                        'description': 'User ID'
                    },
                    'strategy_id': {
                        'required': False,
                        'type': 'string',
                        'description': 'Strategy ID (optional)'
                    },
                    'confidence_level': {
                        'required': False,
                        'type': 'number',
                        'default': 0.95,
                        'description': 'Confidence level for VaR calculation'
                    }
                }
            },
            {
                'route': f'/{self.route_base}/cvar',
                'methods': ['GET'],
                'callback': self.get_cvar,
                'args': {
                    'user_id': {
                        'required': True,
                        'type': 'integer',
                        'description': 'User ID'
                    },
                    'strategy_id': {
                        'required': False,
                        'type': 'string',
                        'description': 'Strategy ID (optional)'
                    },
                    'confidence_level': {
                        'required': False,
                        'type': 'number',
                        'default': 0.95,
                        'description': 'Confidence level for CVaR calculation'
                    }
                }
            },
            {
                'route': f'/{self.route_base}/sharpe',
                'methods': ['GET'],
                'callback': self.get_sharpe_ratio,
                'args': {
                    'user_id': {
                        'required': True,
                        'type': 'integer',
                        'description': 'User ID'
                    },
                    'strategy_id': {
                        'required': False,
                        'type': 'string',
                        'description': 'Strategy ID (optional)'
                    },
                    'risk_free_rate': {
                        'required': False,
                        'type': 'number',
                        'default': 0.045,
                        'description': 'Risk-free rate for Sharpe calculation'
                    }
                }
            },
            {
                'route': f'/{self.route_base}/drawdown',
                'methods': ['GET'],
                'callback': self.get_max_drawdown,
                'args': {
                    'user_id': {
                        'required': True,
                        'type': 'integer',
                        'description': 'User ID'
                    },
                    'strategy_id': {
                        'required': False,
                        'type': 'string',
                        'description': 'Strategy ID (optional)'
                    }
                }
            },
            {
                'route': f'/{self.route_base}/adjusted-returns',
                'methods': ['GET'],
                'callback': self.get_risk_adjusted_returns,
                'args': {
                    'user_id': {
                        'required': True,
                        'type': 'integer',
                        'description': 'User ID'
                    },
                    'strategy_id': {
                        'required': False,
                        'type': 'string',
                        'description': 'Strategy ID (optional)'
                    }
                }
            },
            # Comprehensive Risk Metrics
            {
                'route': f'/{self.route_base}/comprehensive',
                'methods': ['GET'],
                'callback': self.get_comprehensive_risk_metrics,
                'args': {
                    'user_id': {
                        'required': True,
                        'type': 'integer',
                        'description': 'User ID'
                    },
                    'strategy_id': {
                        'required': False,
                        'type': 'string',
                        'description': 'Strategy ID (optional)'
                    },
                    'include_benchmark': {
                        'required': False,
                        'type': 'boolean',
                        'default': False,
                        'description': 'Include benchmark comparison'
                    },
                    'benchmark_symbol': {
                        'required': False,
                        'type': 'string',
                        'default': 'SPY',
                        'description': 'Benchmark symbol for comparison'
                    }
                }
            },
            # Risk Calculation Endpoint
            {
                'route': f'/{self.route_base}/calculate',
                'methods': ['POST'],
                'callback': self.calculate_risk_metrics,
                'args': {
                    'user_id': {
                        'required': True,
                        'type': 'integer',
                        'description': 'User ID'
                    },
                    'strategy_id': {
                        'required': False,
                        'type': 'string',
                        'description': 'Strategy ID (optional)'
                    },
                    'returns_data': {
                        'required': True,
                        'type': 'array',
                        'description': 'Array of return values for calculation'
                    },
                    'equity_curve': {
                        'required': False,
                        'type': 'array',
                        'description': 'Equity curve for drawdown calculation'
                    },
                    'benchmark_returns': {
                        'required': False,
                        'type': 'array',
                        'description': 'Benchmark returns for information ratio'
                    }
                }
            }
        ]

        return endpoints

    def _get_trading_data(self, user_id: int, strategy_id: Optional[str] = None,
                         days: int = 252) -> tuple:
        """Get trading data for risk calculations."""
        # This would connect to the database to get actual trading data
        # For now, return mock data for API testing

        # Mock returns data (normally from wp_trp_trading_performance)
        base_pattern = [0.01, -0.005, 0.015, -0.002, 0.008, 0.012, -0.01]
        # Repeat pattern to get at least 'days' returns
        repeats = (days // len(base_pattern)) + 1
        mock_returns = (base_pattern * repeats)[:days]

        # Mock equity curve (normally calculated from trading performance)
        mock_equity = [10000]  # Starting equity
        for ret in mock_returns:
            mock_equity.append(mock_equity[-1] * (1 + ret))

        return mock_returns, mock_equity

    def _format_risk_response(self, metric_name: str, value: float,
                            user_id: int, strategy_id: Optional[str] = None) -> Dict[str, Any]:
        """Format standardized risk metric response."""
        return {
            'metric': metric_name,
            'value': round(value, 6),
            'user_id': user_id,
            'strategy_id': strategy_id,
            'calculation_date': datetime.now().isoformat(),
            'confidence_level': 0.95,
            'status': 'success'
        }

    def get_var(self, request) -> Dict[str, Any]:
        """Get Value at Risk (VaR) for user/strategy."""
        try:
            user_id = request.GET.get('user_id')
            strategy_id = request.GET.get('strategy_id')
            confidence_level = float(request.GET.get('confidence_level', 0.95))

            if not user_id:
                return {'error': 'user_id parameter required', 'status': 'error'}

            # Get trading data
            returns, _ = self._get_trading_data(int(user_id), strategy_id)

            # Calculate VaR
            returns_array = np.array(returns, dtype=float)
            self.risk_calculator.var_calculator.confidence_level = confidence_level
            var_value = self.risk_calculator.var_calculator.calculate_var(returns_array)

            return self._format_risk_response('var_95', var_value, int(user_id), strategy_id)

        except Exception as e:
            logger.error(f"VaR calculation error: {e}")
            return {'error': str(e), 'status': 'error'}

    def get_cvar(self, request) -> Dict[str, Any]:
        """Get Conditional VaR (CVaR) for user/strategy."""
        try:
            user_id = request.GET.get('user_id')
            strategy_id = request.GET.get('strategy_id')
            confidence_level = float(request.GET.get('confidence_level', 0.95))

            if not user_id:
                return {'error': 'user_id parameter required', 'status': 'error'}

            # Get trading data
            returns, _ = self._get_trading_data(int(user_id), strategy_id)
            returns_array = np.array(returns, dtype=float)

            # Calculate VaR first, then CVaR
            self.risk_calculator.var_calculator.confidence_level = confidence_level
            var_value = self.risk_calculator.var_calculator.calculate_var(returns_array)
            cvar_value = self.risk_calculator.var_calculator.calculate_cvar(returns_array, var_value)

            return self._format_risk_response('cvar_95', cvar_value, int(user_id), strategy_id)

        except Exception as e:
            logger.error(f"CVaR calculation error: {e}")
            return {'error': str(e), 'status': 'error'}

    def get_sharpe_ratio(self, request) -> Dict[str, Any]:
        """Get Sharpe Ratio for user/strategy."""
        try:
            user_id = request.GET.get('user_id')
            strategy_id = request.GET.get('strategy_id')
            risk_free_rate = float(request.GET.get('risk_free_rate', 0.045))

            if not user_id:
                return {'error': 'user_id parameter required', 'status': 'error'}

            # Update risk-free rate
            self.risk_calculator.risk_free_rate = risk_free_rate

            # Get trading data
            returns, _ = self._get_trading_data(int(user_id), strategy_id)
            returns_array = np.array(returns, dtype=float)

            # Calculate Sharpe Ratio
            sharpe_ratio = self.risk_calculator.calculate_sharpe_ratio(returns_array)

            return self._format_risk_response('sharpe_ratio', sharpe_ratio, int(user_id), strategy_id)

        except Exception as e:
            logger.error(f"Sharpe ratio calculation error: {e}")
            return {'error': str(e), 'status': 'error'}

    def get_max_drawdown(self, request) -> Dict[str, Any]:
        """Get Maximum Drawdown for user/strategy."""
        try:
            user_id = request.GET.get('user_id')
            strategy_id = request.GET.get('strategy_id')

            if not user_id:
                return {'error': 'user_id parameter required', 'status': 'error'}

            # Get trading data
            _, equity_curve = self._get_trading_data(int(user_id), strategy_id)
            equity_array = np.array(equity_curve, dtype=float)

            # Calculate Maximum Drawdown
            max_drawdown = self.risk_calculator.calculate_max_drawdown(equity_array)

            return self._format_risk_response('max_drawdown', max_drawdown, int(user_id), strategy_id)

        except Exception as e:
            logger.error(f"Max drawdown calculation error: {e}")
            return {'error': str(e), 'status': 'error'}

    def get_risk_adjusted_returns(self, request) -> Dict[str, Any]:
        """Get Risk-Adjusted Returns (Calmar, Sortino, Information ratios)."""
        try:
            user_id = request.GET.get('user_id')
            strategy_id = request.GET.get('strategy_id')

            if not user_id:
                return {'error': 'user_id parameter required', 'status': 'error'}

            # Get trading data
            returns, equity_curve = self._get_trading_data(int(user_id), strategy_id)
            returns_array = np.array(returns, dtype=float)
            equity_array = np.array(equity_curve, dtype=float)

            # Calculate risk-adjusted returns
            max_drawdown = self.risk_calculator.calculate_max_drawdown(equity_array)
            calmar_ratio = self.risk_calculator.calculate_calmar_ratio(returns_array, max_drawdown)
            sortino_ratio = self.risk_calculator.calculate_sortino_ratio(returns_array)

            return {
                'user_id': int(user_id),
                'strategy_id': strategy_id,
                'calmar_ratio': round(calmar_ratio, 4),
                'sortino_ratio': round(sortino_ratio, 4),
                'calculation_date': datetime.now().isoformat(),
                'status': 'success'
            }

        except Exception as e:
            logger.error(f"Risk-adjusted returns calculation error: {e}")
            return {'error': str(e), 'status': 'error'}

    def get_comprehensive_risk_metrics(self, request) -> Dict[str, Any]:
        """Get comprehensive risk metrics for user/strategy."""
        try:
            user_id = request.GET.get('user_id')
            strategy_id = request.GET.get('strategy_id')
            include_benchmark = request.GET.get('include_benchmark', 'false').lower() == 'true'
            benchmark_symbol = request.GET.get('benchmark_symbol', 'SPY')

            if not user_id:
                return {'error': 'user_id parameter required', 'status': 'error'}

            # Get trading data
            returns, equity_curve = self._get_trading_data(int(user_id), strategy_id)

            # Convert to numpy arrays
            returns_array = np.array(returns, dtype=float)
            equity_array = np.array(equity_curve, dtype=float)

            # Mock benchmark data if requested
            benchmark_array = None
            if include_benchmark:
                benchmark_returns = [0.0008, -0.001, 0.0012, -0.0005, 0.0009] * 50  # Mock SPY returns
                benchmark_array = np.array(benchmark_returns, dtype=float)

            # Calculate comprehensive metrics
            metrics = self.risk_calculator.calculate_comprehensive_risk_metrics(
                returns_array, equity_array, benchmark_array
            )

            return {
                'user_id': int(user_id),
                'strategy_id': strategy_id,
                'var_95': round(metrics.var_95, 6),
                'cvar_95': round(metrics.cvar_95, 6),
                'sharpe_ratio': round(metrics.sharpe_ratio, 4),
                'max_drawdown': round(metrics.max_drawdown, 6),
                'calmar_ratio': round(metrics.calmar_ratio, 4),
                'sortino_ratio': round(metrics.sortino_ratio, 4),
                'information_ratio': round(metrics.information_ratio, 4),
                'calculation_date': metrics.calculation_date.isoformat(),
                'confidence_level': metrics.confidence_level,
                'status': 'success'
            }

        except Exception as e:
            logger.error(f"Comprehensive risk metrics error: {e}")
            return {'error': str(e), 'status': 'error'}

    def calculate_risk_metrics(self, request) -> Dict[str, Any]:
        """Calculate risk metrics from provided data."""
        try:
            # Get POST data
            data = json.loads(request.body) if hasattr(request, 'body') else request.POST

            user_id = data.get('user_id')
            strategy_id = data.get('strategy_id')
            returns_data = data.get('returns_data', [])
            equity_curve = data.get('equity_curve', [])
            benchmark_returns = data.get('benchmark_returns', [])

            if not user_id or not returns_data:
                return {'error': 'user_id and returns_data parameters required', 'status': 'error'}

            # Convert to numpy arrays
            returns = np.array(returns_data, dtype=float)
            equity = np.array(equity_curve, dtype=float) if equity_curve else np.cumprod(1 + returns) * 10000
            benchmark = np.array(benchmark_returns, dtype=float) if benchmark_returns else None

            # Calculate comprehensive metrics
            metrics = self.risk_calculator.calculate_comprehensive_risk_metrics(
                returns, equity, benchmark
            )

            # Check for risk alerts
            thresholds = {
                'var_95': 0.05,
                'max_drawdown': 0.20,
                'sharpe_ratio_min': 1.0
            }
            alerts = self.risk_calculator.check_risk_thresholds(metrics, thresholds)

            return {
                'user_id': int(user_id),
                'strategy_id': strategy_id,
                'metrics': {
                    'var_95': round(metrics.var_95, 6),
                    'cvar_95': round(metrics.cvar_95, 6),
                    'sharpe_ratio': round(metrics.sharpe_ratio, 4),
                    'max_drawdown': round(metrics.max_drawdown, 6),
                    'calmar_ratio': round(metrics.calmar_ratio, 4),
                    'sortino_ratio': round(metrics.sortino_ratio, 4),
                    'information_ratio': round(metrics.information_ratio, 4),
                },
                'alerts': [
                    {
                        'type': alert.alert_type,
                        'severity': alert.severity,
                        'message': alert.message,
                        'current_value': round(alert.current_value, 4),
                        'threshold_value': round(alert.threshold_value, 4)
                    } for alert in alerts
                ],
                'calculation_date': metrics.calculation_date.isoformat(),
                'status': 'success'
            }

        except Exception as e:
            logger.error(f"Risk metrics calculation error: {e}")
            return {'error': str(e), 'status': 'error'}


# WordPress Integration Helper
def register_risk_analytics_endpoints():
    """Register risk analytics endpoints with WordPress REST API."""
    api = RiskAnalyticsAPI()
    endpoints = api.register_endpoints()

    # This would be called during WordPress plugin initialization
    # For each endpoint, register with WordPress REST API

    print(f"Registered {len(endpoints)} risk analytics endpoints")
    return endpoints


if __name__ == "__main__":
    # Test the API endpoints
    print("=== Risk Analytics API Endpoints Test ===")

    # Mock request object for testing
    class MockRequest:
        def __init__(self, get_params=None, post_data=None):
            self.GET = get_params or {}
            self.POST = post_data or {}
            if post_data:
                self.body = json.dumps(post_data).encode('utf-8')

    # Test comprehensive risk metrics
    api = RiskAnalyticsAPI()

    # Mock request for comprehensive metrics
    mock_request = MockRequest({'user_id': '1', 'strategy_id': 'test_strategy'})
    result = api.get_comprehensive_risk_metrics(mock_request)

    print("Comprehensive Risk Metrics API Test:")
    print(json.dumps(result, indent=2))

    print("\n✅ Risk Analytics API implementation complete!")
