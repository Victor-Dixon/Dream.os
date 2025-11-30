#!/usr/bin/env python3
"""
Unit tests for multi_agent_request_validator.py - SSOT & System Integration Test Coverage

Tests MultiAgentRequestValidator class and validation methods.
Target: ≥10 tests, ≥85% coverage, 100% passing.

Author: Agent-8 (SSOT & System Integration Specialist)
Date: 2025-11-29
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime, timedelta
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.multi_agent_request_validator import (
    MultiAgentRequestValidator,
    get_multi_agent_validator
)
from src.core.multi_agent_responder import ResponseStatus, ResponseCollector, AgentResponse


class TestMultiAgentRequestValidator:
    """Test suite for MultiAgentRequestValidator class."""
    
    @pytest.fixture
    def validator(self):
        """Create MultiAgentRequestValidator instance."""
        with patch('src.core.multi_agent_request_validator.get_multi_agent_responder'):
            return MultiAgentRequestValidator()
    
    @pytest.fixture
    def mock_responder(self):
        """Create mock responder."""
        responder = Mock()
        responder.lock = Mock()
        responder.collectors = {}
        return responder
    
    def test_init(self, validator):
        """Test validator initialization."""
        assert validator is not None
        assert validator.responder is not None
    
    def test_check_pending_request_no_pending(self, validator, mock_responder):
        """Test checking for pending request when none exists."""
        validator.responder = mock_responder
        mock_responder.collectors = {}
        mock_responder.lock.__enter__ = Mock(return_value=None)
        mock_responder.lock.__exit__ = Mock(return_value=None)
        
        result = validator.check_pending_request("Agent-1")
        assert result is None
    
    def test_check_pending_request_with_pending(self, validator, mock_responder):
        """Test checking for pending request when one exists."""
        validator.responder = mock_responder
        
        # Create mock collector with pending request
        collector = Mock()
        collector.status = ResponseStatus.PENDING
        collector.collector_id = "collector123"
        collector.request_id = "req123"
        collector.sender = "Agent-4"
        collector.recipients = ["Agent-1", "Agent-2"]
        collector.responses = {}
        collector.original_message = "Test message"
        collector.timeout_seconds = 300
        collector.created_at = datetime.now()
        collector.get_response_count = Mock(return_value=0)
        
        mock_responder.collectors = {"collector123": collector}
        mock_responder.lock.__enter__ = Mock(return_value=None)
        mock_responder.lock.__exit__ = Mock(return_value=None)
        
        result = validator.check_pending_request("Agent-1")
        
        assert result is not None
        assert result["collector_id"] == "collector123"
        assert result["sender"] == "Agent-4"
        assert result["is_pending"] is True
    
    def test_check_pending_request_already_responded(self, validator, mock_responder):
        """Test checking for pending request when agent already responded."""
        validator.responder = mock_responder
        
        collector = Mock()
        collector.status = ResponseStatus.PENDING
        collector.recipients = ["Agent-1"]
        collector.responses = {"Agent-1": Mock()}  # Already responded
        
        mock_responder.collectors = {"collector123": collector}
        mock_responder.lock.__enter__ = Mock(return_value=None)
        mock_responder.lock.__exit__ = Mock(return_value=None)
        
        result = validator.check_pending_request("Agent-1")
        assert result is None
    
    def test_validate_agent_can_send_message_no_pending(self, validator):
        """Test validation when no pending request."""
        with patch.object(validator, 'check_pending_request', return_value=None):
            can_send, error, pending = validator.validate_agent_can_send_message("Agent-1")
            
            assert can_send is True
            assert error is None
            assert pending is None
    
    def test_validate_agent_can_send_message_with_pending(self, validator):
        """Test validation when pending request exists."""
        pending_info = {
            "sender": "Agent-4",
            "collector_id": "collector123",
            "request_id": "req123",
            "original_message": "Test",
            "created_at": datetime.now(),
            "recipient_count": 2,
            "responses_received": 0,
            "timeout_seconds": 300
        }
        
        with patch.object(validator, 'check_pending_request', return_value=pending_info):
            can_send, error, pending = validator.validate_agent_can_send_message(
                "Agent-1",
                target_recipient="Agent-2"
            )
            
            assert can_send is False
            assert error is not None
            assert pending == pending_info
            assert "MESSAGING BLOCKED" in error
    
    def test_validate_agent_can_send_message_responding_to_sender(self, validator):
        """Test validation allows response to request sender."""
        pending_info = {
            "sender": "Agent-4",
            "collector_id": "collector123",
            "request_id": "req123",
            "original_message": "Test",
            "created_at": datetime.now(),
            "recipient_count": 2,
            "responses_received": 0,
            "timeout_seconds": 300
        }
        
        with patch.object(validator, 'check_pending_request', return_value=pending_info):
            can_send, error, pending = validator.validate_agent_can_send_message(
                "Agent-1",
                target_recipient="Agent-4"
            )
            
            # Should allow response to sender
            assert can_send is True
            assert error is None
            assert pending == pending_info
    
    def test_format_pending_request_error(self, validator):
        """Test formatting of pending request error message."""
        pending = {
            "sender": "Agent-4",
            "request_id": "req123",
            "collector_id": "collector123",
            "created_at": datetime.now() - timedelta(minutes=5),
            "original_message": "Test message",
            "recipient_count": 3,
            "responses_received": 1,
            "timeout_seconds": 300
        }
        
        error_msg = validator._format_pending_request_error("Agent-1", pending)
        
        assert "MESSAGING BLOCKED" in error_msg
        assert "Agent-1" in error_msg
        assert "Agent-4" in error_msg
        assert "req123" in error_msg
        assert "Test message" in error_msg
        assert "5" in error_msg  # elapsed minutes
    
    def test_get_pending_request_message_none(self, validator):
        """Test getting pending request message when none exists."""
        with patch.object(validator, 'check_pending_request', return_value=None):
            result = validator.get_pending_request_message("Agent-1")
            assert result is None
    
    def test_get_pending_request_message_with_pending(self, validator):
        """Test getting pending request message when pending exists."""
        pending_info = {
            "sender": "Agent-4",
            "collector_id": "collector123",
            "request_id": "req123",
            "original_message": "Test",
            "created_at": datetime.now(),
            "recipient_count": 2,
            "responses_received": 0,
            "timeout_seconds": 300
        }
        
        with patch.object(validator, 'check_pending_request', return_value=pending_info):
            with patch.object(validator, '_format_pending_request_error', return_value="Error message"):
                result = validator.get_pending_request_message("Agent-1")
                
                assert result == "Error message"
    
    def test_check_pending_request_exception_handling(self, validator, mock_responder):
        """Test exception handling in check_pending_request."""
        validator.responder = mock_responder
        mock_responder.lock.__enter__ = Mock(side_effect=Exception("Test error"))
        
        result = validator.check_pending_request("Agent-1")
        assert result is None


class TestGlobalFunctions:
    """Test suite for global functions."""
    
    def test_get_multi_agent_validator_singleton(self):
        """Test global validator singleton."""
        with patch('src.core.multi_agent_request_validator._validator_instance', None):
            validator1 = get_multi_agent_validator()
            validator2 = get_multi_agent_validator()
            assert validator1 is validator2
            assert isinstance(validator1, MultiAgentRequestValidator)

