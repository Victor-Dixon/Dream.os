"""
Unit tests for contract_notifications_integration.py
Target: ≥85% coverage
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from src.services.contract_system.contract_notifications_integration import (
    ContractNotificationHooks,
    get_notification_hooks,
    notify_assigned,
    notify_started,
    notify_completed,
    notify_blocked,
)


class TestContractNotificationHooks:
    """Tests for ContractNotificationHooks class."""

    def test_init(self):
        """Test ContractNotificationHooks initialization."""
        with patch('src.services.contract_system.contract_notifications_integration.ContractNotifier') as mock_notifier:
            hooks = ContractNotificationHooks()
            assert hooks.notifier is not None

    def test_on_contract_assigned_success(self):
        """Test on_contract_assigned sends notification successfully."""
        hooks = ContractNotificationHooks()
        hooks.notifier = Mock()
        hooks.notifier.notify_contract_assigned.return_value = True
        
        contract_data = {
            "name": "Test Contract",
            "priority": "HIGH",
            "estimated_hours": 25
        }
        
        result = hooks.on_contract_assigned("C1", "Agent-1", contract_data)
        
        assert result is True
        hooks.notifier.notify_contract_assigned.assert_called_once_with(
            contract_id="C1",
            agent_id="Agent-1",
            contract_name="Test Contract",
            priority="HIGH",
            estimated_hours=25
        )

    def test_on_contract_assigned_defaults(self):
        """Test on_contract_assigned uses default values."""
        hooks = ContractNotificationHooks()
        hooks.notifier = Mock()
        hooks.notifier.notify_contract_assigned.return_value = True
        
        result = hooks.on_contract_assigned("C1", "Agent-1", {})
        
        assert result is True
        call_args = hooks.notifier.notify_contract_assigned.call_args[1]
        assert call_args["contract_name"] == "Unnamed Contract"
        assert call_args["priority"] == "MEDIUM"
        assert call_args["estimated_hours"] == 0

    def test_on_contract_assigned_failure(self):
        """Test on_contract_assigned handles notification failure."""
        hooks = ContractNotificationHooks()
        hooks.notifier = Mock()
        hooks.notifier.notify_contract_assigned.return_value = False
        
        result = hooks.on_contract_assigned("C1", "Agent-1", {"name": "Test"})
        
        assert result is False

    def test_on_contract_assigned_exception(self):
        """Test on_contract_assigned handles exceptions."""
        hooks = ContractNotificationHooks()
        hooks.notifier = Mock()
        hooks.notifier.notify_contract_assigned.side_effect = Exception("Error")
        
        result = hooks.on_contract_assigned("C1", "Agent-1", {"name": "Test"})
        
        assert result is False

    def test_on_contract_started_success(self):
        """Test on_contract_started sends notification successfully."""
        hooks = ContractNotificationHooks()
        hooks.notifier = Mock()
        hooks.notifier.notify_contract_started.return_value = True
        
        result = hooks.on_contract_started("C1", "Agent-1", "Test Contract")
        
        assert result is True
        hooks.notifier.notify_contract_started.assert_called_once_with(
            contract_id="C1",
            agent_id="Agent-1",
            contract_name="Test Contract"
        )

    def test_on_contract_started_failure(self):
        """Test on_contract_started handles notification failure."""
        hooks = ContractNotificationHooks()
        hooks.notifier = Mock()
        hooks.notifier.notify_contract_started.return_value = False
        
        result = hooks.on_contract_started("C1", "Agent-1", "Test Contract")
        
        assert result is False

    def test_on_contract_started_exception(self):
        """Test on_contract_started handles exceptions."""
        hooks = ContractNotificationHooks()
        hooks.notifier = Mock()
        hooks.notifier.notify_contract_started.side_effect = Exception("Error")
        
        result = hooks.on_contract_started("C1", "Agent-1", "Test Contract")
        
        assert result is False

    def test_on_contract_completed_success(self):
        """Test on_contract_completed sends notification successfully."""
        hooks = ContractNotificationHooks()
        hooks.notifier = Mock()
        hooks.notifier.notify_contract_completed.return_value = True
        
        contract_data = {"name": "Test Contract"}
        metrics = {"points": 500, "hours": 22.5, "quality": 9.5}
        
        result = hooks.on_contract_completed("C1", "Agent-1", contract_data, metrics)
        
        assert result is True
        hooks.notifier.notify_contract_completed.assert_called_once_with(
            contract_id="C1",
            agent_id="Agent-1",
            contract_name="Test Contract",
            points_earned=500,
            actual_hours=22.5
        )

    def test_on_contract_completed_defaults(self):
        """Test on_contract_completed uses default values."""
        hooks = ContractNotificationHooks()
        hooks.notifier = Mock()
        hooks.notifier.notify_contract_completed.return_value = True
        
        result = hooks.on_contract_completed("C1", "Agent-1", {}, {})
        
        assert result is True
        call_args = hooks.notifier.notify_contract_completed.call_args[1]
        assert call_args["contract_name"] == "Unnamed Contract"
        assert call_args["points_earned"] == 0
        assert call_args["actual_hours"] == 0.0

    def test_on_contract_completed_exception(self):
        """Test on_contract_completed handles exceptions."""
        hooks = ContractNotificationHooks()
        hooks.notifier = Mock()
        hooks.notifier.notify_contract_completed.side_effect = Exception("Error")
        
        result = hooks.on_contract_completed("C1", "Agent-1", {}, {})
        
        assert result is False

    def test_on_contract_blocked_success(self):
        """Test on_contract_blocked sends notification successfully."""
        hooks = ContractNotificationHooks()
        hooks.notifier = Mock()
        hooks.notifier.notify_contract_blocked.return_value = True
        
        result = hooks.on_contract_blocked("C1", "Agent-1", "Test Contract", "Waiting for approval")
        
        assert result is True
        hooks.notifier.notify_contract_blocked.assert_called_once_with(
            contract_id="C1",
            agent_id="Agent-1",
            contract_name="Test Contract",
            blocker="Waiting for approval"
        )

    def test_on_contract_blocked_failure(self):
        """Test on_contract_blocked handles notification failure."""
        hooks = ContractNotificationHooks()
        hooks.notifier = Mock()
        hooks.notifier.notify_contract_blocked.return_value = False
        
        result = hooks.on_contract_blocked("C1", "Agent-1", "Test Contract", "Blocker")
        
        assert result is False

    def test_on_contract_blocked_exception(self):
        """Test on_contract_blocked handles exceptions."""
        hooks = ContractNotificationHooks()
        hooks.notifier = Mock()
        hooks.notifier.notify_contract_blocked.side_effect = Exception("Error")
        
        result = hooks.on_contract_blocked("C1", "Agent-1", "Test Contract", "Blocker")
        
        assert result is False


class TestConvenienceFunctions:
    """Tests for convenience functions."""

    def test_get_notification_hooks_creates_instance(self):
        """Test get_notification_hooks creates instance."""
        with patch('src.services.contract_system.contract_notifications_integration._notification_hooks', None):
            with patch('src.services.contract_system.contract_notifications_integration.ContractNotificationHooks') as mock_class:
                mock_instance = Mock()
                mock_class.return_value = mock_instance
                
                result = get_notification_hooks()
                
                assert result == mock_instance
                mock_class.assert_called_once()

    def test_get_notification_hooks_returns_existing(self):
        """Test get_notification_hooks returns existing instance."""
        existing_hooks = Mock()
        with patch('src.services.contract_system.contract_notifications_integration._notification_hooks', existing_hooks):
            result = get_notification_hooks()
            assert result == existing_hooks

    def test_notify_assigned(self):
        """Test notify_assigned convenience function."""
        mock_hooks = Mock()
        mock_hooks.on_contract_assigned.return_value = True
        
        with patch('src.services.contract_system.contract_notifications_integration.get_notification_hooks', return_value=mock_hooks):
            result = notify_assigned("C1", "Agent-1", {"name": "Test"})
            
            assert result is True
            mock_hooks.on_contract_assigned.assert_called_once_with("C1", "Agent-1", {"name": "Test"})

    def test_notify_started(self):
        """Test notify_started convenience function."""
        mock_hooks = Mock()
        mock_hooks.on_contract_started.return_value = True
        
        with patch('src.services.contract_system.contract_notifications_integration.get_notification_hooks', return_value=mock_hooks):
            result = notify_started("C1", "Agent-1", "Test Contract")
            
            assert result is True
            mock_hooks.on_contract_started.assert_called_once_with("C1", "Agent-1", "Test Contract")

    def test_notify_completed(self):
        """Test notify_completed convenience function."""
        mock_hooks = Mock()
        mock_hooks.on_contract_completed.return_value = True
        
        with patch('src.services.contract_system.contract_notifications_integration.get_notification_hooks', return_value=mock_hooks):
            result = notify_completed("C1", "Agent-1", {"name": "Test"}, {"points": 500})
            
            assert result is True
            mock_hooks.on_contract_completed.assert_called_once_with("C1", "Agent-1", {"name": "Test"}, {"points": 500})

    def test_notify_blocked(self):
        """Test notify_blocked convenience function."""
        mock_hooks = Mock()
        mock_hooks.on_contract_blocked.return_value = True
        
        with patch('src.services.contract_system.contract_notifications_integration.get_notification_hooks', return_value=mock_hooks):
            result = notify_blocked("C1", "Agent-1", "Test Contract", "Blocker")
            
            assert result is True
            mock_hooks.on_contract_blocked.assert_called_once_with("C1", "Agent-1", "Test Contract", "Blocker")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

