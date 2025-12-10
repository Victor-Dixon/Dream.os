"""
Tests for core_service_manager.py - CoreServiceManager class.

Target: ≥85% coverage, 10+ tests.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

# Import with patching to avoid circular import from __init__.py
with patch('src.core.managers.core_configuration_manager', create=True):
    from src.core.managers.core_service_manager import CoreServiceManager
    from src.core.managers.contracts import ManagerContext, ManagerResult


class TestCoreServiceManager:
    """Test CoreServiceManager class."""

    def test_init(self):
        """Test CoreServiceManager initialization."""
        manager = CoreServiceManager()
        assert manager is not None
        assert hasattr(manager, "onboarding")
        assert hasattr(manager, "recovery")
        assert hasattr(manager, "results")

    def test_get_onboarding_manager(self):
        """Test get_onboarding_manager method."""
        manager = CoreServiceManager()
        onboarding = manager.get_onboarding_manager()
        assert onboarding is not None
        assert onboarding == manager.onboarding

    def test_get_recovery_manager(self):
        """Test get_recovery_manager method."""
        manager = CoreServiceManager()
        recovery = manager.get_recovery_manager()
        assert recovery is not None
        assert recovery == manager.recovery

    def test_get_results_manager(self):
        """Test get_results_manager method."""
        manager = CoreServiceManager()
        results = manager.get_results_manager()
        assert results is not None
        assert results == manager.results

    def test_is_initialized_false(self):
        """Test is_initialized returns False before initialization."""
        manager = CoreServiceManager()
        assert manager.is_initialized() is False

    def test_is_initialized_true(self):
        """Test is_initialized returns True after initialization."""
        manager = CoreServiceManager()
        context = ManagerContext(
            config={},
            logger=Mock(),
            metrics={},
            timestamp=datetime.now()
        )
        manager.initialize(context)
        assert manager.is_initialized() is True

    def test_get_status(self):
        """Test get_status method."""
        manager = CoreServiceManager()
        status = manager.get_status()
        
        assert isinstance(status, dict)
        assert "initialized" in status
        assert "onboarding_available" in status
        assert "recovery_available" in status
        assert "results_available" in status
        assert status["initialized"] is False

    def test_get_status_after_init(self):
        """Test get_status after initialization."""
        manager = CoreServiceManager()
        context = ManagerContext(
            config={},
            logger=Mock(),
            metrics={},
            timestamp=datetime.now()
        )
        manager.initialize(context)
        
        status = manager.get_status()
        assert status["initialized"] is True

    def test_inherits_from_coordinator(self):
        """Test that CoreServiceManager inherits from CoreServiceCoordinator."""
        manager = CoreServiceManager()
        from src.core.managers.core_service_coordinator import CoreServiceCoordinator
        assert isinstance(manager, CoreServiceCoordinator)

    def test_execute_delegates_to_coordinator(self):
        """Test that execute method delegates to coordinator."""
        manager = CoreServiceManager()
        context = ManagerContext(
            config={},
            logger=Mock(),
            metrics={},
            timestamp=datetime.now()
        )
        manager.initialize(context)
        
        result = manager.execute(context, "onboard_agent", {"agent_id": "Agent-1"})
        assert isinstance(result, ManagerResult)

