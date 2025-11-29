"""
Tests for protocol/policy_enforcer.py

Comprehensive tests for policy enforcement, validation, and permission checking.
Target: 10+ test methods, ≥85% coverage
"""

import pytest
from unittest.mock import MagicMock, patch, Mock
from src.services.protocol.policy_enforcer import PolicyEnforcer
from src.core.messaging_models_core import (
    UnifiedMessage,
    UnifiedMessageType,
    UnifiedMessagePriority,
    SenderType,
)


class TestPolicyEnforcer:
    """Tests for PolicyEnforcer class."""

    @patch('src.services.protocol.policy_enforcer.load_template_policy')
    def test_initialization_default_policy(self, mock_load):
        """Test enforcer initialization with default policy."""
        mock_load.return_value = {"version": "1.0", "roles": {}, "channels": {}}
        enforcer = PolicyEnforcer()
        
        assert enforcer.policy is not None
        mock_load.assert_called_once_with(None)

    @patch('src.services.protocol.policy_enforcer.load_template_policy')
    def test_initialization_custom_policy_path(self, mock_load):
        """Test enforcer initialization with custom policy path."""
        mock_load.return_value = {"version": "1.0", "roles": {}, "channels": {}}
        enforcer = PolicyEnforcer("custom/policy.json")
        
        mock_load.assert_called_once_with("custom/policy.json")

    @patch('src.services.protocol.policy_enforcer.load_template_policy')
    def test_enforce_policy_urgent_captain_allowed(self, mock_load):
        """Test that urgent messages from captain are always allowed."""
        mock_load.return_value = {"urgent": {"require_captain_approval": True}}
        enforcer = PolicyEnforcer()
        
        message = UnifiedMessage(
            content="urgent",
            sender="Captain Agent-4",
            recipient="Agent-6",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.URGENT,
            sender_type=SenderType.CAPTAIN,
        )
        
        result = enforcer.enforce_policy(message)
        assert result is True

    @patch('src.services.protocol.policy_enforcer.load_template_policy')
    def test_enforce_policy_urgent_agent_with_approval_required(self, mock_load):
        """Test urgent message from agent when approval required."""
        mock_load.return_value = {"urgent": {"require_captain_approval": True}}
        enforcer = PolicyEnforcer()
        
        message = UnifiedMessage(
            content="urgent",
            sender="Agent-1",
            recipient="Agent-6",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.URGENT,
            sender_type=SenderType.AGENT,
        )
        
        result = enforcer.enforce_policy(message)
        assert result is False

    @patch('src.services.protocol.policy_enforcer.load_template_policy')
    def test_enforce_policy_urgent_agent_without_approval_required(self, mock_load):
        """Test urgent message from agent when approval not required."""
        mock_load.return_value = {"urgent": {"require_captain_approval": False}}
        enforcer = PolicyEnforcer()
        
        message = UnifiedMessage(
            content="urgent",
            sender="Agent-1",
            recipient="Agent-6",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.URGENT,
            sender_type=SenderType.AGENT,
        )
        
        result = enforcer.enforce_policy(message)
        assert result is True

    @patch('src.services.protocol.policy_enforcer.load_template_policy')
    def test_enforce_policy_type_disabled(self, mock_load):
        """Test message type that is disabled in policy."""
        mock_load.return_value = {
            "message_types": {
                "broadcast": {"enabled": False}
            }
        }
        enforcer = PolicyEnforcer()
        
        message = UnifiedMessage(
            content="test",
            sender="Agent-1",
            recipient="all",
            message_type=UnifiedMessageType.BROADCAST,
            priority=UnifiedMessagePriority.REGULAR,
            sender_type=SenderType.AGENT,
        )
        
        result = enforcer.enforce_policy(message)
        assert result is False

    @patch('src.services.protocol.policy_enforcer.load_template_policy')
    def test_enforce_policy_type_enabled(self, mock_load):
        """Test message type that is enabled in policy."""
        mock_load.return_value = {
            "message_types": {
                "text": {"enabled": True}
            }
        }
        enforcer = PolicyEnforcer()
        
        message = UnifiedMessage(
            content="test",
            sender="Agent-1",
            recipient="Agent-6",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR,
            sender_type=SenderType.AGENT,
        )
        
        result = enforcer.enforce_policy(message)
        assert result is True

    @patch('src.services.protocol.policy_enforcer.load_template_policy')
    def test_enforce_policy_exception_handling(self, mock_load):
        """Test enforce_policy handles exceptions gracefully."""
        mock_load.return_value = {}
        enforcer = PolicyEnforcer()
        
        message = UnifiedMessage(
            content="test",
            sender="Agent-1",
            recipient="Agent-6",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR,
            sender_type=SenderType.AGENT,
        )
        
        with patch.object(enforcer, '_check_type_policy', side_effect=Exception("Test error")):
            result = enforcer.enforce_policy(message)
            assert result is False

    def test_validate_policy_success(self):
        """Test validating valid policy."""
        enforcer = PolicyEnforcer.__new__(PolicyEnforcer)
        enforcer.policy = {}
        enforcer.logger = MagicMock()
        
        policy_data = {
            "version": "1.0",
            "roles": {"agent": "allowed"},
            "channels": {"general": "allowed"}
        }
        
        result = enforcer.validate_policy(policy_data)
        assert result is True

    def test_validate_policy_missing_version(self):
        """Test validating policy missing version."""
        enforcer = PolicyEnforcer.__new__(PolicyEnforcer)
        enforcer.policy = {}
        enforcer.logger = MagicMock()
        
        policy_data = {
            "roles": {"agent": "allowed"},
            "channels": {"general": "allowed"}
        }
        
        result = enforcer.validate_policy(policy_data)
        assert result is False

    def test_validate_policy_missing_roles(self):
        """Test validating policy missing roles."""
        enforcer = PolicyEnforcer.__new__(PolicyEnforcer)
        enforcer.policy = {}
        enforcer.logger = MagicMock()
        
        policy_data = {
            "version": "1.0",
            "channels": {"general": "allowed"}
        }
        
        result = enforcer.validate_policy(policy_data)
        assert result is False

    def test_check_permissions_captain(self):
        """Test permission check for captain."""
        enforcer = PolicyEnforcer.__new__(PolicyEnforcer)
        enforcer.policy = {}
        enforcer.logger = MagicMock()
        
        result = enforcer.check_permissions("CAPTAIN", "Agent-6", "text")
        assert result is True

    def test_check_permissions_agent_to_agent(self):
        """Test permission check for agent to agent."""
        enforcer = PolicyEnforcer.__new__(PolicyEnforcer)
        enforcer.policy = {}
        enforcer.logger = MagicMock()
        
        result = enforcer.check_permissions("Agent-1", "Agent-6", "text")
        assert result is True

    def test_check_permissions_default_allow(self):
        """Test permission check defaults to allow."""
        enforcer = PolicyEnforcer.__new__(PolicyEnforcer)
        enforcer.policy = {}
        enforcer.logger = MagicMock()
        
        result = enforcer.check_permissions("unknown", "unknown", "text")
        assert result is True

    @patch('src.services.protocol.policy_enforcer.load_template_policy')
    def test_check_urgent_policy_captain(self, mock_load):
        """Test urgent policy check for captain."""
        mock_load.return_value = {"urgent": {"require_captain_approval": True}}
        enforcer = PolicyEnforcer()
        
        message = UnifiedMessage(
            content="urgent",
            sender="Captain Agent-4",
            recipient="Agent-6",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.URGENT,
            sender_type=SenderType.CAPTAIN,
        )
        
        result = enforcer._check_urgent_policy(message)
        assert result is True

    @patch('src.services.protocol.policy_enforcer.load_template_policy')
    def test_check_type_policy_enabled(self, mock_load):
        """Test type policy check when enabled."""
        mock_load.return_value = {
            "message_types": {
                "text": {"enabled": True}
            }
        }
        enforcer = PolicyEnforcer()
        
        message = UnifiedMessage(
            content="test",
            sender="Agent-1",
            recipient="Agent-6",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR,
            sender_type=SenderType.AGENT,
        )
        
        result = enforcer._check_type_policy(message)
        assert result is True

