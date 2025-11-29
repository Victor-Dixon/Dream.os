"""
Tests for policy_enforcer.py

Comprehensive tests for policy enforcement.
Target: ≥85% coverage
"""

import pytest
from unittest.mock import patch, MagicMock
from src.services.protocol.policy_enforcer import PolicyEnforcer
from src.core.messaging_models_core import (
    UnifiedMessage,
    UnifiedMessageType,
    UnifiedMessagePriority,
    SenderType,
)


class TestPolicyEnforcer:
    """Tests for PolicyEnforcer."""

    def test_policy_enforcer_initialization_default(self):
        """Test PolicyEnforcer initialization with default policy."""
        enforcer = PolicyEnforcer()
        assert enforcer.policy is not None
        assert "version" in enforcer.policy

    def test_policy_enforcer_initialization_custom_path(self):
        """Test PolicyEnforcer initialization with custom policy path."""
        with patch("src.services.protocol.policy_enforcer.load_template_policy") as mock_load:
            mock_load.return_value = {"version": 1, "roles": {}, "channels": {}}
            enforcer = PolicyEnforcer("custom/path.yaml")
            assert enforcer.policy is not None

    def test_enforce_policy_success(self):
        """Test enforcing policy on valid message."""
        enforcer = PolicyEnforcer()
        message = UnifiedMessage(
            content="Test",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR,
            sender_type=SenderType.AGENT,
        )
        
        result = enforcer.enforce_policy(message)
        
        assert result is True

    def test_enforce_policy_urgent_captain(self):
        """Test enforcing policy on urgent message from captain."""
        enforcer = PolicyEnforcer()
        message = UnifiedMessage(
            content="Urgent",
            sender="Captain",
            recipient="Agent-1",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.URGENT,
            sender_type=SenderType.CAPTAIN,
        )
        
        result = enforcer.enforce_policy(message)
        
        assert result is True

    def test_validate_policy_success(self):
        """Test validating valid policy."""
        enforcer = PolicyEnforcer()
        policy_data = {
            "version": 1,
            "roles": {"defaults": {}},
            "channels": {"standard": "compact"},
        }
        
        result = enforcer.validate_policy(policy_data)
        
        assert result is True

    def test_validate_policy_missing_key(self):
        """Test validating policy with missing key."""
        enforcer = PolicyEnforcer()
        policy_data = {
            "version": 1,
            "roles": {},
        }
        
        result = enforcer.validate_policy(policy_data)
        
        assert result is False

    def test_check_permissions_captain(self):
        """Test checking permissions for captain."""
        enforcer = PolicyEnforcer()
        
        result = enforcer.check_permissions("CAPTAIN", "Agent-1", "text")
        
        assert result is True

    def test_check_permissions_agent_to_agent(self):
        """Test checking permissions for agent to agent."""
        enforcer = PolicyEnforcer()
        
        result = enforcer.check_permissions("Agent-1", "Agent-2", "text")
        
        assert result is True

    def test_check_permissions_default(self):
        """Test checking permissions with default case."""
        enforcer = PolicyEnforcer()
        
        result = enforcer.check_permissions("Unknown", "Unknown", "text")
        
        assert result is True

    def test_enforce_policy_exception_handling(self):
        """Test policy enforcement with exception handling."""
        enforcer = PolicyEnforcer()
        # Create message that might cause exception
        message = UnifiedMessage(
            content="",
            sender="",
            recipient="",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR,
            sender_type=SenderType.AGENT,
        )
        
        # Should handle gracefully
        result = enforcer.enforce_policy(message)
        
        # Should return False or True, not raise
        assert isinstance(result, bool)
