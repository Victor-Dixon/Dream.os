"""
Unit tests for policy_enforcer.py

Target: ≥85% coverage, 15+ test methods
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from src.services.protocol.policy_enforcer import PolicyEnforcer
from src.core.messaging_models_core import (
    UnifiedMessage, UnifiedMessageType, UnifiedMessagePriority,
    SenderType, RecipientType
)


class TestPolicyEnforcer:
    """Test suite for PolicyEnforcer."""

    @pytest.fixture
    def enforcer(self):
        """Create PolicyEnforcer instance."""
        with patch('src.services.protocol.policy_enforcer.load_template_policy', return_value={}):
            return PolicyEnforcer()

    @pytest.fixture
    def sample_message(self):
        """Create sample message."""
        return UnifiedMessage(
            content="Test",
            recipient=RecipientType.AGENT,
            sender=SenderType.SYSTEM,
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR,
            recipient_id="Agent-1"
        )

    def test_enforcer_initialization(self, enforcer):
        """Test enforcer initializes correctly."""
        assert enforcer is not None
        assert enforcer.policy is not None

    def test_enforce_policy_regular_message(self, enforcer, sample_message):
        """Test enforcing policy on regular message."""
        with patch.object(enforcer, '_check_type_policy', return_value=True):
            result = enforcer.enforce_policy(sample_message)
            
            assert result is True

    def test_enforce_policy_urgent_message(self, enforcer, sample_message):
        """Test enforcing policy on urgent message."""
        sample_message.priority = UnifiedMessagePriority.URGENT
        
        with patch.object(enforcer, '_check_urgent_policy', return_value=True):
            with patch.object(enforcer, '_check_type_policy', return_value=True):
                result = enforcer.enforce_policy(sample_message)
                
                assert result is True

    def test_enforce_policy_blocked_by_urgent(self, enforcer, sample_message):
        """Test policy blocking urgent message."""
        sample_message.priority = UnifiedMessagePriority.URGENT
        
        with patch.object(enforcer, '_check_urgent_policy', return_value=False):
            result = enforcer.enforce_policy(sample_message)
            
            assert result is False

    def test_validate_policy_valid(self, enforcer):
        """Test validating valid policy."""
        policy_data = {
            "version": "1.0",
            "roles": {},
            "channels": {}
        }
        
        result = enforcer.validate_policy(policy_data)
        
        assert result is True

    def test_validate_policy_missing_key(self, enforcer):
        """Test validating policy with missing key."""
        policy_data = {
            "version": "1.0",
            "roles": {}
            # Missing "channels"
        }
        
        result = enforcer.validate_policy(policy_data)
        
        assert result is False

    def test_check_permissions_captain(self, enforcer):
        """Test captain has permission to send to anyone."""
        result = enforcer.check_permissions("Captain", "Agent-1", "text")
        
        assert result is True

    def test_check_permissions_agent_to_agent(self, enforcer):
        """Test agents can send to other agents."""
        result = enforcer.check_permissions("Agent-1", "Agent-2", "text")
        
        assert result is True

