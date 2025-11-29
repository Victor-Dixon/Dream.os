"""
Unit tests for orchestration/orchestrator_components.py - MEDIUM PRIORITY

Tests OrchestratorComponents class functionality.
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
components_path = project_root / "src" / "core" / "orchestration" / "orchestrator_components.py"
spec = importlib.util.spec_from_file_location("orchestrator_components", components_path)
orchestrator_components = importlib.util.module_from_spec(spec)
orchestrator_components.__package__ = 'src.core.orchestration'
spec.loader.exec_module(orchestrator_components)

OrchestratorComponents = orchestrator_components.OrchestratorComponents


class TestOrchestratorComponents:
    """Test suite for OrchestratorComponents class."""

    @pytest.fixture
    def components(self):
        """Create an OrchestratorComponents instance."""
        return OrchestratorComponents("test_orchestrator")

    @pytest.fixture
    def sample_component(self):
        """Create a sample component."""
        return Mock()

    def test_initialization(self, components):
        """Test OrchestratorComponents initialization."""
        assert components.orchestrator_name == "test_orchestrator"
        assert components.components == {}
        assert components.logger is not None

    def test_register_component_success(self, components, sample_component):
        """Test registering a component successfully."""
        components.register_component("test_component", sample_component)
        
        assert "test_component" in components.components
        assert components.components["test_component"] == sample_component

    def test_register_component_empty_name(self, components, sample_component):
        """Test registering component with empty name raises error."""
        with pytest.raises(ValueError, match="Component name cannot be empty"):
            components.register_component("", sample_component)
        
        with pytest.raises(ValueError, match="Component name cannot be empty"):
            components.register_component("   ", sample_component)

    def test_register_component_replaces_existing(self, components, sample_component):
        """Test registering component replaces existing one."""
        old_component = Mock()
        components.register_component("test", old_component)
        components.register_component("test", sample_component)
        
        assert components.components["test"] == sample_component
        assert components.components["test"] != old_component

    def test_get_component_exists(self, components, sample_component):
        """Test getting an existing component."""
        components.register_component("test", sample_component)
        
        retrieved = components.get_component("test")
        
        assert retrieved == sample_component

    def test_get_component_not_exists(self, components):
        """Test getting a non-existent component."""
        retrieved = components.get_component("nonexistent")
        
        assert retrieved is None

    def test_has_component_true(self, components, sample_component):
        """Test has_component returns True for existing component."""
        components.register_component("test", sample_component)
        
        assert components.has_component("test") is True

    def test_has_component_false(self, components):
        """Test has_component returns False for non-existent component."""
        assert components.has_component("nonexistent") is False

    def test_unregister_component_success(self, components, sample_component):
        """Test unregistering an existing component."""
        components.register_component("test", sample_component)
        
        result = components.unregister_component("test")
        
        assert result is True
        assert "test" not in components.components

    def test_unregister_component_not_exists(self, components):
        """Test unregistering a non-existent component."""
        result = components.unregister_component("nonexistent")
        
        assert result is False

    def test_clear_all_components(self, components):
        """Test clearing all components."""
        components.register_component("comp1", Mock())
        components.register_component("comp2", Mock())
        components.register_component("comp3", Mock())
        
        components.clear_all_components()
        
        assert len(components.components) == 0

    def test_multiple_operations(self, components):
        """Test multiple operations in sequence."""
        comp1 = Mock()
        comp2 = Mock()
        
        # Register
        components.register_component("comp1", comp1)
        components.register_component("comp2", comp2)
        assert components.has_component("comp1") is True
        assert components.has_component("comp2") is True
        
        # Get
        assert components.get_component("comp1") == comp1
        
        # Unregister
        assert components.unregister_component("comp1") is True
        assert components.has_component("comp1") is False
        
        # Clear
        components.clear_all_components()
        assert len(components.components) == 0

