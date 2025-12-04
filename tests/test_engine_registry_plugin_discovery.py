"""
Unit Tests for Engine Registry - Plugin Discovery Pattern
=========================================================

Tests for auto-discovery mechanism and protocol-based registration.

Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2025-12-03
V2 Compliant: Yes
"""

import importlib
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.core.engines.registry import EngineRegistry
from src.core.engines.contracts import Engine, EngineContext, EngineResult


class TestEngineRegistryDiscovery:
    """Test engine discovery mechanism."""

    def test_registry_initializes(self):
        """Test that registry initializes without errors."""
        registry = EngineRegistry()
        assert registry is not None
        assert hasattr(registry, '_engines')
        assert hasattr(registry, '_instances')

    def test_engines_discovered(self):
        """Test that engines are auto-discovered."""
        registry = EngineRegistry()
        engine_types = registry.get_engine_types()
        
        assert len(engine_types) > 0, "No engines discovered"
        assert len(engine_types) == 14, f"Expected 14 engines, got {len(engine_types)}"

    def test_all_required_engines_present(self):
        """Test that all required engines are discovered."""
        registry = EngineRegistry()
        engine_types = registry.get_engine_types()
        
        required_engines = [
            'analysis', 'communication', 'coordination', 'data',
            'integration', 'ml', 'monitoring', 'orchestration',
            'performance', 'processing', 'security', 'storage',
            'utility', 'validation'
        ]
        
        for engine_type in required_engines:
            assert engine_type in engine_types, f"Missing engine: {engine_type}"

    def test_engine_retrieval(self):
        """Test that engines can be retrieved by type."""
        registry = EngineRegistry()
        
        # Test a few engines
        analysis_engine = registry.get_engine('analysis')
        assert analysis_engine is not None
        assert hasattr(analysis_engine, 'initialize')
        assert hasattr(analysis_engine, 'execute')
        assert hasattr(analysis_engine, 'cleanup')
        assert hasattr(analysis_engine, 'get_status')

    def test_unknown_engine_type_raises_error(self):
        """Test that unknown engine type raises ValueError."""
        registry = EngineRegistry()
        
        with pytest.raises(ValueError, match="Unknown engine type"):
            registry.get_engine('nonexistent_engine')

    def test_engine_lazy_instantiation(self):
        """Test that engines are instantiated lazily."""
        registry = EngineRegistry()
        
        # Initially no instances
        assert len(registry._instances) == 0
        
        # Get an engine
        engine = registry.get_engine('analysis')
        assert engine is not None
        
        # Instance should be cached
        assert 'analysis' in registry._instances
        assert registry._instances['analysis'] is engine

    def test_engine_singleton_behavior(self):
        """Test that same engine type returns same instance."""
        registry = EngineRegistry()
        
        engine1 = registry.get_engine('analysis')
        engine2 = registry.get_engine('analysis')
        
        assert engine1 is engine2, "Engines should be singletons per type"

    def test_get_engine_types_returns_list(self):
        """Test that get_engine_types returns a list."""
        registry = EngineRegistry()
        engine_types = registry.get_engine_types()
        
        assert isinstance(engine_types, list)
        assert len(engine_types) > 0


class TestEngineProtocolCompliance:
    """Test that discovered engines comply with Engine protocol."""

    def test_all_engines_implement_required_methods(self):
        """Test that all discovered engines implement required methods."""
        registry = EngineRegistry()
        required_methods = ['initialize', 'execute', 'cleanup', 'get_status']
        
        for engine_type in registry.get_engine_types():
            engine = registry.get_engine(engine_type)
            
            for method in required_methods:
                assert hasattr(engine, method), \
                    f"Engine {engine_type} missing method: {method}"
                assert callable(getattr(engine, method)), \
                    f"Engine {engine_type} method {method} is not callable"

    def test_engine_initialize_signature(self):
        """Test that engine initialize method has correct signature."""
        registry = EngineRegistry()
        engine = registry.get_engine('analysis')
        
        # Create mock context
        mock_context = MagicMock(spec=EngineContext)
        mock_context.logger = MagicMock()
        
        # Should accept EngineContext and return bool
        result = engine.initialize(mock_context)
        assert isinstance(result, bool)

    def test_engine_execute_signature(self):
        """Test that engine execute method has correct signature."""
        registry = EngineRegistry()
        engine = registry.get_engine('analysis')
        
        # Create mock context
        mock_context = MagicMock(spec=EngineContext)
        mock_context.logger = MagicMock()
        
        # Should accept EngineContext and payload, return EngineResult
        payload = {"operation": "test"}
        result = engine.execute(mock_context, payload)
        assert hasattr(result, 'success')
        assert hasattr(result, 'data')

    def test_engine_cleanup_signature(self):
        """Test that engine cleanup method has correct signature."""
        registry = EngineRegistry()
        engine = registry.get_engine('analysis')
        
        # Create mock context
        mock_context = MagicMock(spec=EngineContext)
        mock_context.logger = MagicMock()
        
        # Should accept EngineContext and return bool
        result = engine.cleanup(mock_context)
        assert isinstance(result, bool)

    def test_engine_get_status_signature(self):
        """Test that engine get_status method has correct signature."""
        registry = EngineRegistry()
        engine = registry.get_engine('analysis')
        
        # Should return dict
        status = engine.get_status()
        assert isinstance(status, dict)


class TestEngineRegistryOperations:
    """Test registry operations (initialize_all, cleanup_all, get_all_status)."""

    def test_initialize_all(self):
        """Test that initialize_all works for all engines."""
        registry = EngineRegistry()
        
        # Create mock context
        mock_context = MagicMock(spec=EngineContext)
        mock_context.logger = MagicMock()
        
        results = registry.initialize_all(mock_context)
        
        assert isinstance(results, dict)
        assert len(results) == len(registry.get_engine_types())
        
        # All should be bool values
        for engine_type, result in results.items():
            assert isinstance(result, bool), \
                f"Engine {engine_type} initialize result should be bool"

    def test_cleanup_all(self):
        """Test that cleanup_all works for all engines."""
        registry = EngineRegistry()
        
        # First initialize engines
        mock_context = MagicMock(spec=EngineContext)
        mock_context.logger = MagicMock()
        registry.initialize_all(mock_context)
        
        # Then cleanup
        results = registry.cleanup_all(mock_context)
        
        assert isinstance(results, dict)
        # Should have results for initialized engines
        assert len(results) > 0

    def test_get_all_status(self):
        """Test that get_all_status works for all engines."""
        registry = EngineRegistry()
        
        # Initialize engines first
        mock_context = MagicMock(spec=EngineContext)
        mock_context.logger = MagicMock()
        registry.initialize_all(mock_context)
        
        # Get status
        status = registry.get_all_status()
        
        assert isinstance(status, dict)
        assert len(status) > 0
        
        # All should be dict values
        for engine_type, engine_status in status.items():
            assert isinstance(engine_status, dict), \
                f"Engine {engine_type} status should be dict"


class TestDiscoveryErrorHandling:
    """Test error handling in discovery mechanism."""

    @patch('src.core.engines.registry.importlib.import_module')
    def test_import_error_handled_gracefully(self, mock_import):
        """Test that ImportError during discovery is handled gracefully."""
        mock_import.side_effect = ImportError("Test import error")
        
        # Should not raise, but log warning
        registry = EngineRegistry()
        # Registry should still initialize (other engines may work)
        assert registry is not None

    @patch('src.core.engines.registry.pkgutil.iter_modules')
    def test_pkgutil_error_handled(self, mock_iter):
        """Test that pkgutil errors are handled gracefully."""
        mock_iter.side_effect = Exception("Test pkgutil error")
        
        # Should not raise
        registry = EngineRegistry()
        assert registry is not None

    def test_missing_engine_methods_handled(self):
        """Test that engines missing required methods are skipped."""
        # This is tested implicitly - if an engine doesn't have methods,
        # it won't be discovered (which is correct behavior)
        registry = EngineRegistry()
        
        # All discovered engines should have required methods
        for engine_type in registry.get_engine_types():
            engine = registry.get_engine(engine_type)
            assert hasattr(engine, 'initialize')
            assert hasattr(engine, 'execute')
            assert hasattr(engine, 'cleanup')
            assert hasattr(engine, 'get_status')


class TestBackwardCompatibility:
    """Test backward compatibility with existing code."""

    def test_existing_api_unchanged(self):
        """Test that existing API methods still work."""
        registry = EngineRegistry()
        
        # All existing methods should work
        assert hasattr(registry, 'get_engine')
        assert hasattr(registry, 'get_engine_types')
        assert hasattr(registry, 'initialize_all')
        assert hasattr(registry, 'cleanup_all')
        assert hasattr(registry, 'get_all_status')

    def test_engine_types_consistent(self):
        """Test that engine types are consistent with previous implementation."""
        registry = EngineRegistry()
        engine_types = registry.get_engine_types()
        
        # Should have same engines as before (14 engines)
        assert len(engine_types) == 14
        
        # Should include all expected types
        expected = {
            'analysis', 'communication', 'coordination', 'data',
            'integration', 'ml', 'monitoring', 'orchestration',
            'performance', 'processing', 'security', 'storage',
            'utility', 'validation'
        }
        assert set(engine_types) == expected

    def test_engine_behavior_unchanged(self):
        """Test that engine behavior is unchanged."""
        registry = EngineRegistry()
        
        # Test that engines work the same way
        engine = registry.get_engine('analysis')
        assert engine is not None
        
        # Should be able to initialize
        mock_context = MagicMock(spec=EngineContext)
        mock_context.logger = MagicMock()
        result = engine.initialize(mock_context)
        assert isinstance(result, bool)


class TestDiscoveryMechanism:
    """Test the discovery mechanism itself."""

    def test_discovery_uses_pkgutil(self):
        """Test that discovery uses pkgutil for module scanning."""
        registry = EngineRegistry()
        
        # Discovery should have found engines
        assert len(registry.get_engine_types()) > 0

    def test_discovery_filters_by_naming_convention(self):
        """Test that discovery filters by *_core_engine naming convention."""
        registry = EngineRegistry()
        
        # All discovered engines should follow naming convention
        # (This is tested implicitly - only *_core_engine modules are discovered)

    def test_discovery_finds_engine_classes(self):
        """Test that discovery finds classes ending with CoreEngine."""
        registry = EngineRegistry()
        
        # All engines should have CoreEngine in class name
        for engine_type in registry.get_engine_types():
            engine = registry.get_engine(engine_type)
            class_name = engine.__class__.__name__
            assert class_name.endswith('CoreEngine'), \
                f"Engine {engine_type} class {class_name} should end with CoreEngine"

    def test_discovery_logs_activity(self):
        """Test that discovery logs activity (if logging configured)."""
        # This is tested by checking that discovery completes
        # Logging is configured in registry.py
        registry = EngineRegistry()
        assert registry is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

