"""
Unit tests for Risk Analytics API Endpoints

<!-- SSOT Domain: analytics -->
"""

import pytest
import json
import numpy as np
from unittest.mock import Mock, patch, MagicMock
from src.services.risk_analytics.risk_api_endpoints import RiskAnalyticsAPI


class MockRequest:
    """Mock request object for testing."""

    def __init__(self, get_params=None, post_data=None):
        self.GET = get_params or {}
        self.POST = post_data or {}
        if post_data:
            self.body = json.dumps(post_data).encode('utf-8')


@pytest.fixture
def risk_api():
    """Create RiskAnalyticsAPI instance."""
    return RiskAnalyticsAPI()


@pytest.fixture
def sample_returns():
    """Generate sample returns."""
    np.random.seed(42)
    return np.random.normal(0.001, 0.02, 252).tolist()


@pytest.fixture
def sample_equity_curve(sample_returns):
    """Generate sample equity curve."""
    equity = [10000]
    for ret in sample_returns:
        equity.append(equity[-1] * (1 + ret))
    return equity


class TestRiskAnalyticsAPI:
    """Test Risk Analytics API endpoints."""

    def test_init(self, risk_api):
        """Test API initialization."""
        assert risk_api.risk_calculator is not None
        assert risk_api.namespace == 'tradingrobotplug/v1'
        assert risk_api.route_base == 'analytics/risk'

    def test_register_endpoints(self, risk_api):
        """Test endpoint registration."""
        endpoints = risk_api.register_endpoints()
        
        assert isinstance(endpoints, list)
        assert len(endpoints) > 0
        
        # Check that all endpoints have required fields
        for endpoint in endpoints:
            assert 'route' in endpoint
            assert 'methods' in endpoint
            assert 'callback' in endpoint
            assert 'args' in endpoint

    def test_get_var_success(self, risk_api):
        """Test VaR endpoint success."""
        request = MockRequest({'user_id': '1', 'strategy_id': 'test'})
        result = risk_api.get_var(request)
        
        assert result['status'] == 'success'
        assert 'value' in result
        assert result['user_id'] == 1
        assert result['metric'] == 'var_95'

    def test_get_var_missing_user_id(self, risk_api):
        """Test VaR endpoint with missing user_id."""
        request = MockRequest({'strategy_id': 'test'})
        result = risk_api.get_var(request)
        
        assert result['status'] == 'error'
        assert 'error' in result

    def test_get_var_with_confidence_level(self, risk_api):
        """Test VaR endpoint with custom confidence level."""
        request = MockRequest({
            'user_id': '1',
            'confidence_level': '0.99'
        })
        result = risk_api.get_var(request)
        
        assert result['status'] == 'success'

    def test_get_cvar_success(self, risk_api):
        """Test CVaR endpoint success."""
        request = MockRequest({'user_id': '1'})
        result = risk_api.get_cvar(request)
        
        assert result['status'] == 'success'
        assert 'value' in result
        assert result['metric'] == 'cvar_95'

    def test_get_cvar_missing_user_id(self, risk_api):
        """Test CVaR endpoint with missing user_id."""
        request = MockRequest()
        result = risk_api.get_cvar(request)
        
        assert result['status'] == 'error'

    def test_get_sharpe_ratio_success(self, risk_api):
        """Test Sharpe ratio endpoint success."""
        request = MockRequest({'user_id': '1'})
        result = risk_api.get_sharpe_ratio(request)
        
        assert result['status'] == 'success'
        assert 'value' in result
        assert result['metric'] == 'sharpe_ratio'

    def test_get_sharpe_ratio_with_risk_free_rate(self, risk_api):
        """Test Sharpe ratio with custom risk-free rate."""
        request = MockRequest({
            'user_id': '1',
            'risk_free_rate': '0.03'
        })
        result = risk_api.get_sharpe_ratio(request)
        
        assert result['status'] == 'success'

    def test_get_max_drawdown_success(self, risk_api):
        """Test max drawdown endpoint success."""
        request = MockRequest({'user_id': '1'})
        result = risk_api.get_max_drawdown(request)
        
        assert result['status'] == 'success'
        assert 'value' in result
        assert result['metric'] == 'max_drawdown'

    def test_get_risk_adjusted_returns_success(self, risk_api):
        """Test risk-adjusted returns endpoint success."""
        request = MockRequest({'user_id': '1'})
        result = risk_api.get_risk_adjusted_returns(request)
        
        assert result['status'] == 'success'
        assert 'calmar_ratio' in result
        assert 'sortino_ratio' in result

    def test_get_comprehensive_risk_metrics_success(self, risk_api):
        """Test comprehensive risk metrics endpoint success."""
        request = MockRequest({'user_id': '1'})
        result = risk_api.get_comprehensive_risk_metrics(request)
        
        assert result['status'] == 'success'
        assert 'var_95' in result
        assert 'cvar_95' in result
        assert 'sharpe_ratio' in result
        assert 'max_drawdown' in result
        assert 'calmar_ratio' in result
        assert 'sortino_ratio' in result

    def test_get_comprehensive_risk_metrics_with_benchmark(self, risk_api):
        """Test comprehensive metrics with benchmark."""
        request = MockRequest({
            'user_id': '1',
            'include_benchmark': 'true',
            'benchmark_symbol': 'SPY'
        })
        result = risk_api.get_comprehensive_risk_metrics(request)
        
        assert result['status'] == 'success'
        assert 'information_ratio' in result

    def test_get_comprehensive_risk_metrics_missing_user_id(self, risk_api):
        """Test comprehensive metrics with missing user_id."""
        request = MockRequest()
        result = risk_api.get_comprehensive_risk_metrics(request)
        
        assert result['status'] == 'error'

    def test_calculate_risk_metrics_success(self, risk_api, sample_returns, sample_equity_curve):
        """Test calculate risk metrics endpoint success."""
        request = MockRequest(post_data={
            'user_id': 1,
            'returns_data': sample_returns,
            'equity_curve': sample_equity_curve
        })
        result = risk_api.calculate_risk_metrics(request)
        
        assert result['status'] == 'success'
        assert 'metrics' in result
        assert 'alerts' in result
        assert isinstance(result['alerts'], list)

    def test_calculate_risk_metrics_missing_user_id(self, risk_api, sample_returns):
        """Test calculate metrics with missing user_id."""
        request = MockRequest(post_data={
            'returns_data': sample_returns
        })
        result = risk_api.calculate_risk_metrics(request)
        
        assert result['status'] == 'error'

    def test_calculate_risk_metrics_missing_returns(self, risk_api):
        """Test calculate metrics with missing returns_data."""
        request = MockRequest(post_data={
            'user_id': 1
        })
        result = risk_api.calculate_risk_metrics(request)
        
        assert result['status'] == 'error'

    def test_calculate_risk_metrics_with_benchmark(
        self, risk_api, sample_returns, sample_equity_curve
    ):
        """Test calculate metrics with benchmark."""
        benchmark_returns = np.random.normal(0.0008, 0.015, len(sample_returns)).tolist()
        request = MockRequest(post_data={
            'user_id': 1,
            'returns_data': sample_returns,
            'equity_curve': sample_equity_curve,
            'benchmark_returns': benchmark_returns
        })
        result = risk_api.calculate_risk_metrics(request)
        
        assert result['status'] == 'success'
        assert 'information_ratio' in result['metrics']

    def test_calculate_risk_metrics_generates_equity_curve(self, risk_api, sample_returns):
        """Test calculate metrics generates equity curve if not provided."""
        request = MockRequest(post_data={
            'user_id': 1,
            'returns_data': sample_returns
        })
        result = risk_api.calculate_risk_metrics(request)
        
        assert result['status'] == 'success'
        assert 'metrics' in result

    def test_format_risk_response(self, risk_api):
        """Test risk response formatting."""
        response = risk_api._format_risk_response('test_metric', 0.05, 1, 'test_strategy')
        
        assert response['metric'] == 'test_metric'
        assert response['value'] == 0.05
        assert response['user_id'] == 1
        assert response['strategy_id'] == 'test_strategy'
        assert response['status'] == 'success'
        assert 'calculation_date' in response

    def test_get_trading_data(self, risk_api):
        """Test trading data retrieval."""
        returns, equity = risk_api._get_trading_data(1, 'test_strategy')
        
        assert isinstance(returns, list)
        assert isinstance(equity, list)
        assert len(equity) == len(returns) + 1  # Equity starts with initial value

    def test_get_trading_data_with_days(self, risk_api):
        """Test trading data retrieval with custom days."""
        returns, equity = risk_api._get_trading_data(1, None, days=100)
        
        assert len(returns) == 100

    @patch('src.services.risk_analytics.risk_api_endpoints.logger')
    def test_get_var_error_handling(self, mock_logger, risk_api):
        """Test VaR endpoint error handling."""
        # Create a request that will cause an error
        request = Mock()
        request.GET = {'user_id': 'invalid'}
        
        result = risk_api.get_var(request)
        
        assert result['status'] == 'error'
        assert 'error' in result

    @patch('src.services.risk_analytics.risk_api_endpoints.logger')
    def test_calculate_risk_metrics_error_handling(self, mock_logger, risk_api):
        """Test calculate metrics error handling."""
        # Create a request with invalid JSON
        request = Mock()
        request.body = b'invalid json'
        request.POST = {}
        
        result = risk_api.calculate_risk_metrics(request)
        
        assert result['status'] == 'error'


@pytest.mark.unit
class TestRiskAnalyticsAPIIntegration:
    """Integration tests for Risk Analytics API."""

    def test_full_workflow(self, risk_api, sample_returns, sample_equity_curve):
        """Test full workflow from calculation to response."""
        # Calculate comprehensive metrics
        request = MockRequest({'user_id': '1'})
        comprehensive = risk_api.get_comprehensive_risk_metrics(request)
        
        assert comprehensive['status'] == 'success'
        
        # Calculate individual metrics
        var_request = MockRequest({'user_id': '1'})
        var_result = risk_api.get_var(var_request)
        
        assert var_result['status'] == 'success'
        
        # Calculate with POST
        post_request = MockRequest(post_data={
            'user_id': 1,
            'returns_data': sample_returns,
            'equity_curve': sample_equity_curve
        })
        post_result = risk_api.calculate_risk_metrics(post_request)
        
        assert post_result['status'] == 'success'
        assert len(post_result['metrics']) > 0

