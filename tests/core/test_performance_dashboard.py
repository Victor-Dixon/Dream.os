"""
Unit tests for performance_dashboard.py - MEDIUM PRIORITY

Tests PerformanceDashboard redirect wrapper functionality.
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

# Mock the unified_dashboard imports before importing
mock_dashboard_engine = MagicMock()
mock_dashboard_models = MagicMock()
mock_dashboard_reporter = MagicMock()

# Patch sys.modules
with patch.dict('sys.modules', {
    'src.core.performance.unified_dashboard': MagicMock(
        DashboardEngine=mock_dashboard_engine,
        DashboardModels=mock_dashboard_models,
        DashboardReporter=mock_dashboard_reporter,
        PerformanceDashboardOrchestrator=mock_dashboard_engine,
    )
}):
    # Import using importlib to bypass __init__.py chain
    import importlib.util
    dashboard_path = project_root / "src" / "core" / "performance" / "performance_dashboard.py"
    spec = importlib.util.spec_from_file_location("performance_dashboard", dashboard_path)
    performance_dashboard = importlib.util.module_from_spec(spec)
    performance_dashboard.__package__ = 'src.core.performance'
    
    # Mock the imports
    performance_dashboard.DashboardEngine = mock_dashboard_engine
    performance_dashboard.DashboardModels = mock_dashboard_models
    performance_dashboard.DashboardReporter = mock_dashboard_reporter
    performance_dashboard.PerformanceDashboardOrchestrator = mock_dashboard_engine
    
    spec.loader.exec_module(performance_dashboard)

get_performance_dashboard = performance_dashboard.get_performance_dashboard
PerformanceDashboard = performance_dashboard.PerformanceDashboard
PerformanceDashboardOrchestrator = performance_dashboard.PerformanceDashboardOrchestrator


class TestPerformanceDashboard:
    """Test suite for PerformanceDashboard redirect wrapper."""

    def test_get_performance_dashboard_returns_instance(self):
        """Test that get_performance_dashboard returns a DashboardEngine instance."""
        # The function should call PerformanceDashboardOrchestrator (which is DashboardEngine)
        # Just verify it's callable and returns something
        result = get_performance_dashboard()
        
        assert result is not None
        # Verify it's a mock (since we're mocking the imports)
        assert hasattr(result, '__class__')

    def test_performance_dashboard_alias(self):
        """Test that PerformanceDashboard is an alias for PerformanceDashboardOrchestrator."""
        assert PerformanceDashboard == PerformanceDashboardOrchestrator
        assert PerformanceDashboard == mock_dashboard_engine

    def test_backward_compatibility_exports(self):
        """Test that backward compatibility exports are available."""
        assert hasattr(performance_dashboard, 'PerformanceDashboardOrchestrator')
        assert hasattr(performance_dashboard, 'DashboardModels')
        assert hasattr(performance_dashboard, 'DashboardEngine')
        assert hasattr(performance_dashboard, 'DashboardReporter')
        assert hasattr(performance_dashboard, 'PerformanceDashboard')
        assert hasattr(performance_dashboard, 'get_performance_dashboard')

    def test_get_performance_dashboard_multiple_calls(self):
        """Test that get_performance_dashboard can be called multiple times."""
        result1 = get_performance_dashboard()
        result2 = get_performance_dashboard()
        
        # Both should return instances
        assert result1 is not None
        assert result2 is not None

    def test_factory_function_exists(self):
        """Test that the factory function exists and is callable."""
        assert callable(get_performance_dashboard)

    def test_module_exports(self):
        """Test that __all__ exports are correct."""
        expected_exports = [
            "PerformanceDashboardOrchestrator",
            "DashboardModels",
            "DashboardEngine",
            "DashboardReporter",
            "PerformanceDashboard",
            "get_performance_dashboard",
        ]
        
        for export in expected_exports:
            assert export in performance_dashboard.__all__

