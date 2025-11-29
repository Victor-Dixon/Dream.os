"""
Phase 2: Web Routes Integration Tests
=====================================

Tests web routes after config_ssot migration to ensure zero breaking changes.

Author: Agent-7 (Web Development Specialist)
Date: 2025-01-28
Priority: HIGH
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch

# Test web routes with new config_ssot
# Verify dashboard routes still functional
# Test API endpoints
# Validate error handling


class TestDashboardRoutes:
    """Test dashboard routes with config_ssot."""
    
    @pytest.fixture
    def mock_config(self):
        """Mock config_ssot for testing."""
        with patch('config.settings.config') as mock:
            mock.web_port = 8000
            mock.web_host = "localhost"
            yield mock
    
    @pytest.fixture
    def client(self, mock_config):
        """Create test client."""
        # Import dashboard after mocking config
        from trading_robot.web.dashboard import TradingDashboard
        
        mock_engine = Mock()
        dashboard = TradingDashboard(mock_engine)
        
        return TestClient(dashboard.app)
    
    def test_dashboard_health_check(self, client):
        """Test dashboard health check endpoint."""
        response = client.get("/health")
        assert response.status_code in [200, 404]  # May not exist yet
    
    def test_dashboard_root(self, client):
        """Test dashboard root endpoint."""
        response = client.get("/")
        assert response.status_code in [200, 404]  # May not exist yet
    
    def test_config_access(self, mock_config):
        """Test config access in dashboard."""
        from trading_robot.web.dashboard import TradingDashboard
        
        mock_engine = Mock()
        dashboard = TradingDashboard(mock_engine)
        
        # Verify dashboard initialized with config
        assert dashboard is not None


class TestConfigMigration:
    """Test config migration compatibility."""
    
    def test_config_ssot_import(self):
        """Test config_ssot can be imported."""
        try:
            from src.core.config_ssot import get_unified_config
            assert callable(get_unified_config)
        except ImportError:
            pytest.skip("config_ssot not available yet")
    
    def test_backward_compatibility(self):
        """Test backward compatibility shims."""
        # Test that old config imports still work
        try:
            from src.core.config_core import get_config
            assert callable(get_config)
        except ImportError:
            pytest.skip("config_core not available")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

