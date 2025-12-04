"""
Unit Tests for Engine Registry Discovery Pattern
================================================

Tests for Plugin Discovery Pattern implementation in registry.py.
Validates auto-discovery, engine registration, and protocol compliance.

<!-- SSOT Domain: qa -->

Author: Agent-8 (Testing & Quality Assurance Specialist)
Date: 2025-12-03
V2 Compliant: Yes (<300 lines)
"""

import pytest
import importlib
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from typing import Any, Dict

# Import registry and contracts
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from src.core.engines.registry import EngineRegistry
from src.core.engines.contracts import Engine, EngineContext


class TestEngineRegistryDiscovery:
    """Test engine discovery functionality."""
    
    def test_registry_initialization(self):
        """Test that registry initializes and discovers engines."""
        registry = EngineRegistry()
        
        assert registry is not None
        assert hasattr(registry, '_engines')
        assert hasattr(registry, '_instances')
        assert isinstance(registry._engines, dict)
        assert isinstance(registry._instances, dict)
    
    def test_discovery_finds_engines(self):
        """Test that discovery finds all 14 engines."""
        registry = EngineRegistry()
        engine_types = registry.get_engine_types()
        
        # Should discover all 14 engines
        assert len(engine_types) == 14, f"Expected 14 engines, found {len(engine_types)}"
        
        # Verify expected engine types
        expected_engines = {
            'analysis', 'communication', 'coordination', 'data',
            'integration', 'ml', 'monitoring', 'orchestration',
            'performance', 'processing', 'security', 'storage',
            'utility', 'validation'
        }
        
        actual_engines = set(engine_types)
        assert actual_engines == expected_engines, \
            f"Expected {expected_engines}, got {actual_engines}"
    
    def test_get_engine_types(self):
        """Test getting all engine types."""
        registry = EngineRegistry()
        types = registry.get_engine_types()
        
        assert isinstance(types, list)
        assert len(types) > 0
        assert all(isinstance(t, str) for t in types)
    
    def test_get_engine_creates_instance(self):
        """Test that get_engine creates and returns engine instance."""
        registry = EngineRegistry()
        engine_types = registry.get_engine_types()
        
        if not engine_types:
            pytest.skip("No engines discovered")
        
        # Test first engine
        engine_type = engine_types[0]
        engine = registry.get_engine(engine_type)
        
        assert engine is not None
        assert engine_type in registry._instances
    
    def test_get_engine_lazy_instantiation(self):
        """Test that engines are created lazily (only when requested)."""
        registry = EngineRegistry()
        engine_types = registry.get_engine_types()
        
        if len(engine_types) < 2:
            pytest.skip("Need at least 2 engines for this test")
        
        # Initially, no instances should exist
        assert len(registry._instances) == 0
        
        # Get first engine
        engine1 = registry.get_engine(engine_types[0])
        assert len(registry._instances) == 1
        
        # Get same engine again - should reuse instance
        engine1_again = registry.get_engine(engine_types[0])
        assert len(registry._instances) == 1
        assert engine1 is engine1_again  # Same instance
        
        # Get second engine
        engine2 = registry.get_engine(engine_types[1])
        assert len(registry._instances) == 2
    
    def test_get_engine_invalid_type(self):
        """Test that get_engine raises error for invalid engine type."""
        registry = EngineRegistry()
        
        with pytest.raises(ValueError, match="Unknown engine type"):
            registry.get_engine("nonexistent_engine")
    
    def test_all_engines_protocol_compliant(self):
        """Test that all discovered engines implement Engine protocol."""
        registry = EngineRegistry()
        engine_types = registry.get_engine_types()
        
        required_methods = ['initialize', 'execute', 'cleanup', 'get_status']
        
        for engine_type in engine_types:
            engine = registry.get_engine(engine_type)
            
            # Check all required methods exist
            for method in required_methods:
                assert hasattr(engine, method), \
                    f"Engine {engine_type} missing method {method}"
                assert callable(getattr(engine, method)), \
                    f"Engine {engine_type} method {method} is not callable"


class TestEngineRegistryOperations:
    """Test registry operations (initialize, cleanup, status)."""
    
    @pytest.fixture
    def mock_context(self):
        """Create mock EngineContext."""
        context = Mock(spec=EngineContext)
        context.logger = Mock()
        return context
    
    def test_initialize_all(self, mock_context):
        """Test initializing all engines."""
        registry = EngineRegistry()
        engine_types = registry.get_engine_types()
        
        if not engine_types:
            pytest.skip("No engines discovered")
        
        results = registry.initialize_all(mock_context)
        
        assert isinstance(results, dict)
        assert len(results) == len(engine_types)
        
        # All engines should be initialized (or at least attempted)
        for engine_type in engine_types:
            assert engine_type in results
            assert isinstance(results[engine_type], bool)
    
    def test_cleanup_all(self, mock_context):
        """Test cleaning up all engines."""
        registry = EngineRegistry()
        engine_types = registry.get_engine_types()
        
        if not engine_types:
            pytest.skip("No engines discovered")
        
        # First initialize some engines
        for engine_type in engine_types[:3]:  # Initialize first 3
            registry.get_engine(engine_type)
        
        results = registry.cleanup_all(mock_context)
        
        assert isinstance(results, dict)
        # Should have results for initialized engines
        assert len(results) <= len(engine_types)
    
    def test_get_all_status(self):
        """Test getting status of all engines."""
        registry = EngineRegistry()
        engine_types = registry.get_engine_types()
        
        if not engine_types:
            pytest.skip("No engines discovered")
        
        # Initialize some engines
        for engine_type in engine_types[:3]:
            registry.get_engine(engine_type)
        
        status = registry.get_all_status()
        
        assert isinstance(status, dict)
        assert len(status) <= len(engine_types)
        
        # Each status should be a dict
        for engine_type, engine_status in status.items():
            assert isinstance(engine_status, dict)


class TestEngineDiscoveryEdgeCases:
    """Test edge cases and error handling in discovery."""
    
    @patch('src.core.engines.registry.pkgutil.iter_modules')
    def test_discovery_handles_import_errors(self, mock_iter_modules):
        """Test that discovery handles import errors gracefully."""
        # Mock iter_modules to return a module that will fail to import
        mock_iter_modules.return_value = [
            (Mock(), 'invalid_core_engine', False)
        ]
        
        # Should not raise exception
        registry = EngineRegistry()
        
        # Should handle gracefully (may log warnings)
        assert registry is not None
    
    @patch('src.core.engines.registry.pkgutil.iter_modules')
    def test_discovery_skips_non_engine_modules(self, mock_iter_modules):
        """Test that discovery skips modules not ending with _core_engine."""
        mock_iter_modules.return_value = [
            (Mock(), 'regular_module', False),
            (Mock(), 'helper_module', False),
            (Mock(), 'test_module', False),
        ]
        
        registry = EngineRegistry()
        
        # Should not discover any engines from these modules
        assert len(registry.get_engine_types()) == 0
    
    def test_discovery_handles_missing_package(self):
        """Test that discovery handles missing package gracefully."""
        # This is tested implicitly by the actual discovery
        # If package doesn't exist, should log error but not crash
        registry = EngineRegistry()
        
        # Should still initialize (may have 0 engines)
        assert registry is not None


class TestAll14Engines:
    """Test all 14 specific engines individually."""
    
    @pytest.mark.parametrize("engine_type", [
        'analysis', 'communication', 'coordination', 'data',
        'integration', 'ml', 'monitoring', 'orchestration',
        'performance', 'processing', 'security', 'storage',
        'utility', 'validation'
    ])
    def test_engine_exists_and_works(self, engine_type):
        """Test that each engine can be retrieved and used."""
        registry = EngineRegistry()
        
        # Should be able to get engine
        engine = registry.get_engine(engine_type)
        assert engine is not None
        
        # Should have required methods
        assert hasattr(engine, 'initialize')
        assert hasattr(engine, 'execute')
        assert hasattr(engine, 'cleanup')
        assert hasattr(engine, 'get_status')
        
        # Should be able to get status
        status = engine.get_status()
        assert isinstance(status, dict)
    
    @pytest.mark.parametrize("engine_type", [
        'analysis', 'communication', 'coordination', 'data',
        'integration', 'ml', 'monitoring', 'orchestration',
        'performance', 'processing', 'security', 'storage',
        'utility', 'validation'
    ])
    def test_engine_initialization(self, engine_type):
        """Test that each engine can be initialized."""
        registry = EngineRegistry()
        engine = registry.get_engine(engine_type)
        
        # Create mock context
        mock_context = Mock(spec=EngineContext)
        mock_context.logger = Mock()
        
        # Should be able to initialize
        result = engine.initialize(mock_context)
        assert isinstance(result, bool)


class TestNoRegressions:
    """Test that discovery pattern doesn't break existing functionality."""
    
    def test_registry_singleton_behavior(self):
        """Test that registry behaves consistently across instances."""
        registry1 = EngineRegistry()
        registry2 = EngineRegistry()
        
        # Each instance should discover engines independently
        types1 = registry1.get_engine_types()
        types2 = registry2.get_engine_types()
        
        # Should discover same engines
        assert set(types1) == set(types2)
    
    def test_no_circular_dependencies(self):
        """Test that registry doesn't create circular dependencies."""
        # This is tested by the fact that we can import registry
        # without circular import errors
        from src.core.engines.registry import EngineRegistry
        
        # Should be able to create instance
        registry = EngineRegistry()
        assert registry is not None
    
    def test_backward_compatibility(self):
        """Test that registry maintains backward compatibility."""
        registry = EngineRegistry()
        
        # Old API should still work
        engine_types = registry.get_engine_types()
        assert isinstance(engine_types, list)
        
        if engine_types:
            engine = registry.get_engine(engine_types[0])
            assert engine is not None

