"""
Unit tests for core_service_manager.py - HIGH PRIORITY

Comprehensive tests for CoreServiceManager class (wrapper for CoreServiceCoordinator).
Target: ≥85% coverage, 10+ test methods.
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.managers.contracts import ManagerContext, ManagerResult
from src.core.managers.core_service_manager import CoreServiceManager
from src.core.managers.core_service_coordinator import CoreServiceCoordinator


class TestCoreServiceManager:
    """Test suite for CoreServiceManager class."""

    @pytest.fixture
    def mock_context(self):
        """Create mock manager context."""
        return ManagerContext(
            config={"test": "config"},
            logger=lambda msg: None,
            metrics={},
            timestamp=datetime.now()
        )

    @pytest.fixture
    def manager(self):
        """Create CoreServiceManager instance with mocked coordinator."""
        with patch('src.core.managers.core_service_manager.CoreServiceCoordinator') as mock_coord_class:
            mock_coord = MagicMock()
            mock_coord.initialize.return_value = True
            mock_coord.cleanup.return_value = True
            mock_coord.get_status.return_value = {
                "onboarding_status": {},
                "recovery_status": {},
                "results_status": {},
                "total_onboarding_sessions": 0,
                "initialized": False
            }
            mock_coord.execute.return_value = ManagerResult(
                success=True,
                data={},
                metrics={}
            )
            mock_coord_class.return_value = mock_coord
            
            manager = CoreServiceManager()
            manager.onboarding = mock_coord.onboarding
            manager.recovery = mock_coord.recovery
            manager.results = mock_coord.results
            manager.initialized = False
            return manager

    def test_manager_initialization(self, manager):
        """Test manager initialization."""
        assert manager is not None
        assert isinstance(manager, CoreServiceManager)

    def test_manager_is_wrapper(self):
        """Test that CoreServiceManager is a wrapper for CoreServiceCoordinator."""
        assert issubclass(CoreServiceManager, CoreServiceCoordinator)

    def test_manager_inheritance(self):
        """Test that CoreServiceManager inherits from CoreServiceCoordinator."""
        manager = CoreServiceManager()
        assert isinstance(manager, CoreServiceCoordinator)

    def test_initialize(self, manager, mock_context):
        """Test manager initialization with context."""
        result = manager.initialize(mock_context)
        
        assert result is True
        assert manager.initialized is True

    def test_initialize_failure(self, manager, mock_context):
        """Test manager initialization failure."""
        manager.onboarding.initialize.return_value = False
        
        result = manager.initialize(mock_context)
        
        # Should still return True (coordinator initializes all)
        assert result is True

    def test_execute_onboarding_operation(self, manager, mock_context):
        """Test execute with onboarding operation."""
        expected_result = ManagerResult(
            success=True,
            data={"agent_id": "Agent-1"},
            metrics={}
        )
        manager.onboarding.execute.return_value = expected_result
        
        result = manager.execute(mock_context, "onboard_agent", {"agent_id": "Agent-1"})
        
        assert result.success is True
        assert result.data["agent_id"] == "Agent-1"
        manager.onboarding.execute.assert_called_once()

    def test_execute_recovery_operation(self, manager, mock_context):
        """Test execute with recovery operation."""
        expected_result = ManagerResult(
            success=True,
            data={"recovery_id": "rec-1"},
            metrics={}
        )
        manager.recovery.execute.return_value = expected_result
        
        result = manager.execute(mock_context, "recover_from_error", {"error": "test"})
        
        assert result.success is True
        manager.recovery.execute.assert_called_once()

    def test_execute_results_operation(self, manager, mock_context):
        """Test execute with results operation."""
        expected_result = ManagerResult(
            success=True,
            data={"results": []},
            metrics={}
        )
        manager.results.execute.return_value = expected_result
        
        result = manager.execute(mock_context, "process_results", {"results_data": []})
        
        assert result.success is True
        manager.results.execute.assert_called_once()

    def test_execute_unknown_operation(self, manager, mock_context):
        """Test execute with unknown operation."""
        result = manager.execute(mock_context, "unknown_operation", {})
        
        assert result.success is False
        assert "Unknown operation" in result.error

    def test_cleanup(self, manager, mock_context):
        """Test cleanup operation."""
        result = manager.cleanup(mock_context)
        
        assert result is True
        manager.onboarding.cleanup.assert_called_once_with(mock_context)
        manager.recovery.cleanup.assert_called_once_with(mock_context)
        manager.results.cleanup.assert_called_once_with(mock_context)

    def test_get_status(self, manager):
        """Test get_status operation."""
        manager.onboarding.get_status.return_value = {"total_sessions": 5}
        manager.recovery.get_status.return_value = {"strategies": 3}
        manager.results.get_status.return_value = {"processed": 10}
        manager.initialized = True
        
        status = manager.get_status()
        
        assert status["initialized"] is True
        assert status["total_onboarding_sessions"] == 5
        assert "onboarding_status" in status
        assert "recovery_status" in status
        assert "results_status" in status

    def test_execute_all_onboarding_operations(self, manager, mock_context):
        """Test all onboarding operations route correctly."""
        onboarding_ops = [
            "onboard_agent",
            "start_onboarding",
            "complete_onboarding",
            "get_onboarding_status"
        ]
        
        for op in onboarding_ops:
            manager.execute(mock_context, op, {})
            manager.onboarding.execute.assert_called()
            manager.onboarding.reset_mock()

    def test_execute_all_recovery_operations(self, manager, mock_context):
        """Test all recovery operations route correctly."""
        recovery_ops = [
            "register_recovery_strategy",
            "recover_from_error",
            "get_recovery_strategies"
        ]
        
        for op in recovery_ops:
            manager.execute(mock_context, op, {})
            manager.recovery.execute.assert_called()
            manager.recovery.reset_mock()

    def test_execute_all_results_operations(self, manager, mock_context):
        """Test all results operations route correctly."""
        results_ops = ["process_results", "get_results"]
        
        for op in results_ops:
            manager.execute(mock_context, op, {})
            manager.results.execute.assert_called()
            manager.results.reset_mock()

    def test_execute_with_payload_extraction(self, manager, mock_context):
        """Test execute extracts correct payload data."""
        manager.onboarding.execute.return_value = ManagerResult(
            success=True, data={}, metrics={}
        )
        
        # Test onboarding with agent_data
        manager.execute(mock_context, "onboard_agent", {
            "agent_data": {"agent_id": "Agent-1"},
            "other": "ignored"
        })
        
        # Should pass agent_data to onboarding
        call_args = manager.onboarding.execute.call_args
        assert call_args[0][1] == "onboard_agent"
        assert "agent_id" in call_args[0][2]

    def test_cleanup_calls_all_managers(self, manager, mock_context):
        """Test cleanup calls all specialized managers."""
        manager.cleanup(mock_context)
        
        manager.onboarding.cleanup.assert_called_once_with(mock_context)
        manager.recovery.cleanup.assert_called_once_with(mock_context)
        manager.results.cleanup.assert_called_once_with(mock_context)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
