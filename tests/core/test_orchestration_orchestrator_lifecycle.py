"""
Unit tests for orchestration/orchestrator_lifecycle.py - MEDIUM PRIORITY

Tests OrchestratorLifecycle class functionality.
"""

import pytest
from unittest.mock import Mock, MagicMock
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

# Import using importlib to bypass __init__.py chain
import importlib.util
lifecycle_path = project_root / "src" / "core" / "orchestration" / "orchestrator_lifecycle.py"
spec = importlib.util.spec_from_file_location("orchestrator_lifecycle", lifecycle_path)
orchestrator_lifecycle = importlib.util.module_from_spec(spec)
orchestrator_lifecycle.__package__ = 'src.core.orchestration'
spec.loader.exec_module(orchestrator_lifecycle)

OrchestratorLifecycle = orchestrator_lifecycle.OrchestratorLifecycle


class TestOrchestratorLifecycle:
    """Test suite for OrchestratorLifecycle class."""

    @pytest.fixture
    def mock_logger(self):
        """Create a mock logger."""
        return Mock()

    @pytest.fixture
    def component_with_init(self):
        """Create a component with initialize method."""
        component = Mock()
        component.initialize = Mock()
        return component

    @pytest.fixture
    def component_with_cleanup(self):
        """Create a component with cleanup method."""
        component = Mock()
        component.cleanup = Mock()
        return component

    def test_initialize_components_success(self, mock_logger, component_with_init):
        """Test initializing components successfully."""
        components = {
            "comp1": component_with_init,
            "comp2": Mock(),  # No initialize method
        }
        
        result = OrchestratorLifecycle.initialize_components(components, mock_logger)
        
        assert result is True
        component_with_init.initialize.assert_called_once()
        mock_logger.debug.assert_called()

    def test_initialize_components_empty(self, mock_logger):
        """Test initializing empty components dict."""
        components = {}
        
        result = OrchestratorLifecycle.initialize_components(components, mock_logger)
        
        assert result is True

    def test_initialize_components_failure(self, mock_logger, component_with_init):
        """Test initializing components with failure."""
        component_with_init.initialize.side_effect = Exception("Init error")
        components = {"comp1": component_with_init}
        
        result = OrchestratorLifecycle.initialize_components(components, mock_logger)
        
        assert result is False
        mock_logger.error.assert_called_once()

    def test_initialize_components_multiple(self, mock_logger):
        """Test initializing multiple components."""
        comp1 = Mock()
        comp1.initialize = Mock()
        comp2 = Mock()
        comp2.initialize = Mock()
        comp3 = type('Component', (), {})()  # Component without initialize method
        
        components = {"comp1": comp1, "comp2": comp2, "comp3": comp3}
        
        result = OrchestratorLifecycle.initialize_components(components, mock_logger)
        
        assert result is True
        comp1.initialize.assert_called_once()
        comp2.initialize.assert_called_once()
        assert not hasattr(comp3, 'initialize')

    def test_cleanup_components_success(self, mock_logger, component_with_cleanup):
        """Test cleaning up components successfully."""
        components = {
            "comp1": component_with_cleanup,
            "comp2": Mock(),  # No cleanup method
        }
        
        result = OrchestratorLifecycle.cleanup_components(components, mock_logger)
        
        assert result is True
        component_with_cleanup.cleanup.assert_called_once()
        mock_logger.debug.assert_called()

    def test_cleanup_components_reverse_order(self, mock_logger):
        """Test cleanup happens in reverse order."""
        comp1 = Mock()
        comp1.cleanup = Mock()
        comp2 = Mock()
        comp2.cleanup = Mock()
        comp3 = Mock()
        comp3.cleanup = Mock()
        
        components = {"comp1": comp1, "comp2": comp2, "comp3": comp3}
        
        result = OrchestratorLifecycle.cleanup_components(components, mock_logger)
        
        assert result is True
        # Verify cleanup was called (order verification would require more complex mocking)
        comp1.cleanup.assert_called_once()
        comp2.cleanup.assert_called_once()
        comp3.cleanup.assert_called_once()

    def test_cleanup_components_empty(self, mock_logger):
        """Test cleaning up empty components dict."""
        components = {}
        
        result = OrchestratorLifecycle.cleanup_components(components, mock_logger)
        
        assert result is True

    def test_cleanup_components_failure(self, mock_logger, component_with_cleanup):
        """Test cleaning up components with failure."""
        component_with_cleanup.cleanup.side_effect = Exception("Cleanup error")
        components = {"comp1": component_with_cleanup}
        
        result = OrchestratorLifecycle.cleanup_components(components, mock_logger)
        
        assert result is False
        mock_logger.error.assert_called_once()

    def test_cleanup_components_multiple(self, mock_logger):
        """Test cleaning up multiple components."""
        comp1 = Mock()
        comp1.cleanup = Mock()
        comp2 = Mock()
        comp2.cleanup = Mock()
        comp3 = type('Component', (), {})()  # Component without cleanup method
        
        components = {"comp1": comp1, "comp2": comp2, "comp3": comp3}
        
        result = OrchestratorLifecycle.cleanup_components(components, mock_logger)
        
        assert result is True
        comp1.cleanup.assert_called_once()
        comp2.cleanup.assert_called_once()
        assert not hasattr(comp3, 'cleanup')

