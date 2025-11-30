#!/usr/bin/env python3
"""
Unit tests for multi_agent_responder.py - SSOT & System Integration Test Coverage

Tests MultiAgentResponder, ResponseCollector, and AgentResponse classes.
Target: ≥10 tests, ≥85% coverage, 100% passing.

Author: Agent-8 (SSOT & System Integration Specialist)
Date: 2025-11-29
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime, timedelta
import sys
import threading
import time
from pathlib import Path
import tempfile
import shutil

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.multi_agent_responder import (
    MultiAgentResponder,
    ResponseCollector,
    AgentResponse,
    ResponseStatus,
    get_multi_agent_responder
)


class TestResponseStatus:
    """Test suite for ResponseStatus enum."""
    
    def test_status_values(self):
        """Test all status enum values exist."""
        assert ResponseStatus.PENDING.value == "pending"
        assert ResponseStatus.COLLECTING.value == "collecting"
        assert ResponseStatus.COMPLETE.value == "complete"
        assert ResponseStatus.TIMEOUT.value == "timeout"
        assert ResponseStatus.PARTIAL.value == "partial"


class TestAgentResponse:
    """Test suite for AgentResponse dataclass."""
    
    def test_init(self):
        """Test AgentResponse initialization."""
        response = AgentResponse(
            agent_id="Agent-1",
            response="Test response",
            timestamp=datetime.now()
        )
        assert response.agent_id == "Agent-1"
        assert response.response == "Test response"
        assert response.received is True


class TestResponseCollector:
    """Test suite for ResponseCollector class."""
    
    @pytest.fixture
    def collector(self):
        """Create ResponseCollector instance."""
        return ResponseCollector(
            collector_id="collector123",
            request_id="req123",
            sender="Agent-4",
            recipients=["Agent-1", "Agent-2"],
            original_message="Test message",
            timeout_seconds=300,
            wait_for_all=True
        )
    
    def test_init(self, collector):
        """Test ResponseCollector initialization."""
        assert collector.collector_id == "collector123"
        assert collector.request_id == "req123"
        assert collector.sender == "Agent-4"
        assert collector.recipients == ["Agent-1", "Agent-2"]
        assert collector.status == ResponseStatus.PENDING
        assert collector.wait_for_all is True
    
    def test_add_response_valid(self, collector):
        """Test adding valid response."""
        result = collector.add_response("Agent-1", "Response 1")
        
        assert "Agent-1" in collector.responses
        assert collector.responses["Agent-1"].response == "Response 1"
        assert collector.status == ResponseStatus.COLLECTING
        assert result is False  # Not complete yet (wait_for_all=True)
    
    def test_add_response_invalid_recipient(self, collector):
        """Test adding response from non-recipient."""
        result = collector.add_response("Agent-99", "Response")
        
        assert "Agent-99" not in collector.responses
        assert result is False
    
    def test_add_response_update_existing(self, collector):
        """Test updating existing response."""
        collector.add_response("Agent-1", "Response 1")
        collector.add_response("Agent-1", "Response 2")
        
        assert collector.responses["Agent-1"].response == "Response 2"
    
    def test_add_response_complete_wait_for_all(self, collector):
        """Test collector completes when all responses received (wait_for_all=True)."""
        result1 = collector.add_response("Agent-1", "Response 1")
        result2 = collector.add_response("Agent-2", "Response 2")
        
        assert result1 is False
        assert result2 is True  # Complete
        assert collector.status == ResponseStatus.COMPLETE
    
    def test_add_response_complete_no_wait(self):
        """Test collector completes with first response (wait_for_all=False)."""
        collector = ResponseCollector(
            collector_id="collector123",
            request_id="req123",
            sender="Agent-4",
            recipients=["Agent-1", "Agent-2"],
            original_message="Test",
            timeout_seconds=300,
            wait_for_all=False
        )
        
        result = collector.add_response("Agent-1", "Response 1")
        
        assert result is True  # Complete after first response
        assert collector.status == ResponseStatus.COMPLETE
    
    def test_is_complete_wait_for_all(self, collector):
        """Test is_complete check with wait_for_all=True."""
        collector.add_response("Agent-1", "Response 1")
        assert collector._is_complete() is False
        
        collector.add_response("Agent-2", "Response 2")
        assert collector._is_complete() is True
    
    def test_is_timed_out(self, collector):
        """Test timeout check."""
        assert collector.is_timed_out() is False
        
        # Mock old timestamp
        collector.created_at = datetime.now() - timedelta(seconds=400)
        assert collector.is_timed_out() is True
    
    def test_get_missing_agents(self, collector):
        """Test getting missing agents."""
        collector.add_response("Agent-1", "Response 1")
        
        missing = collector.get_missing_agents()
        assert missing == ["Agent-2"]
    
    def test_get_response_count(self, collector):
        """Test getting response count."""
        assert collector.get_response_count() == 0
        
        collector.add_response("Agent-1", "Response 1")
        assert collector.get_response_count() == 1
    
    def test_get_total_expected(self, collector):
        """Test getting total expected responses."""
        assert collector.get_total_expected() == 2


class TestMultiAgentResponder:
    """Test suite for MultiAgentResponder class."""
    
    @pytest.fixture
    def temp_storage(self):
        """Create temporary storage directory."""
        temp_dir = Path(tempfile.mkdtemp())
        yield temp_dir
        shutil.rmtree(temp_dir, ignore_errors=True)
    
    @pytest.fixture
    def responder(self, temp_storage):
        """Create MultiAgentResponder instance."""
        responder = MultiAgentResponder(storage_dir=str(temp_storage))
        responder._timeout_checker_running = False  # Stop background thread
        return responder
    
    def test_init(self, responder, temp_storage):
        """Test responder initialization."""
        assert responder.storage_dir == temp_storage
        assert len(responder.collectors) == 0
    
    def test_create_request(self, responder):
        """Test creating a new request."""
        collector_id = responder.create_request(
            request_id="req123",
            sender="Agent-4",
            recipients=["Agent-1", "Agent-2"],
            content="Test message",
            timeout_seconds=300,
            wait_for_all=True
        )
        
        assert collector_id is not None
        assert collector_id in responder.collectors
        collector = responder.collectors[collector_id]
        assert collector.request_id == "req123"
        assert collector.sender == "Agent-4"
        assert collector.recipients == ["Agent-1", "Agent-2"]
    
    def test_submit_response(self, responder):
        """Test submitting a response."""
        collector_id = responder.create_request(
            request_id="req123",
            sender="Agent-4",
            recipients=["Agent-1"],
            content="Test",
            timeout_seconds=300
        )
        
        result = responder.submit_response(collector_id, "Agent-1", "Response")
        
        assert result is True  # Complete
        assert "Agent-1" in responder.collectors[collector_id].responses
    
    def test_submit_response_collector_not_found(self, responder):
        """Test submitting response to non-existent collector."""
        result = responder.submit_response("nonexistent", "Agent-1", "Response")
        assert result is False
    
    def test_submit_response_already_finalized(self, responder):
        """Test submitting response to finalized collector."""
        collector_id = responder.create_request(
            request_id="req123",
            sender="Agent-4",
            recipients=["Agent-1"],
            content="Test",
            timeout_seconds=300
        )
        
        responder.collectors[collector_id].status = ResponseStatus.COMPLETE
        result = responder.submit_response(collector_id, "Agent-1", "Response")
        
        assert result is False
    
    def test_combine_responses(self, responder):
        """Test combining multiple responses."""
        collector = ResponseCollector(
            collector_id="collector123",
            request_id="req123",
            sender="Agent-4",
            recipients=["Agent-1", "Agent-2"],
            original_message="Test message",
            timeout_seconds=300,
            wait_for_all=False
        )
        
        collector.add_response("Agent-1", "Response 1")
        collector.add_response("Agent-2", "Response 2")
        
        combined = responder._combine_responses(collector)
        
        assert "Combined Response" in combined
        assert "Agent-1 Response" in combined
        assert "Agent-2 Response" in combined
        assert "Response 1" in combined
        assert "Response 2" in combined
    
    def test_combine_responses_missing(self, responder):
        """Test combining responses with missing agents."""
        collector = ResponseCollector(
            collector_id="collector123",
            request_id="req123",
            sender="Agent-4",
            recipients=["Agent-1", "Agent-2"],
            original_message="Test",
            timeout_seconds=300,
            wait_for_all=False
        )
        
        collector.add_response("Agent-1", "Response 1")
        
        combined = responder._combine_responses(collector)
        
        assert "No response received" in combined
        assert "Missing Responses" in combined
    
    def test_is_complete(self, responder):
        """Test checking if collector is complete."""
        collector_id = responder.create_request(
            request_id="req123",
            sender="Agent-4",
            recipients=["Agent-1"],
            content="Test",
            timeout_seconds=300
        )
        
        assert responder.is_complete(collector_id) is False
        
        responder.submit_response(collector_id, "Agent-1", "Response")
        assert responder.is_complete(collector_id) is True
    
    def test_get_collector_status(self, responder):
        """Test getting collector status."""
        collector_id = responder.create_request(
            request_id="req123",
            sender="Agent-4",
            recipients=["Agent-1"],
            content="Test",
            timeout_seconds=300
        )
        
        status = responder.get_collector_status(collector_id)
        
        assert status is not None
        assert status["collector_id"] == collector_id
        assert status["status"] == "pending"
        assert status["total_expected"] == 1
    
    def test_get_collector_status_not_found(self, responder):
        """Test getting status for non-existent collector."""
        status = responder.get_collector_status("nonexistent")
        assert status is None
    
    @patch('src.core.multi_agent_responder.MessageCoordinator')
    def test_finalize_collector(self, mock_coordinator, responder, temp_storage):
        """Test finalizing collector and delivering combined message."""
        mock_coordinator.send_to_agent.return_value = {"success": True, "queue_id": "queue123"}
        
        collector_id = responder.create_request(
            request_id="req123",
            sender="Agent-4",
            recipients=["Agent-1"],
            content="Test",
            timeout_seconds=300
        )
        
        responder.submit_response(collector_id, "Agent-1", "Response")
        
        # Check that storage file was created
        storage_file = temp_storage / f"{collector_id}.json"
        assert storage_file.exists()
        
        # Check that delivery was attempted
        assert mock_coordinator.send_to_agent.called


class TestGlobalFunctions:
    """Test suite for global functions."""
    
    def test_get_multi_agent_responder_singleton(self):
        """Test global responder singleton."""
        with patch('src.core.multi_agent_responder._responder_instance', None):
            responder1 = get_multi_agent_responder()
            responder2 = get_multi_agent_responder()
            assert responder1 is responder2
            assert isinstance(responder1, MultiAgentResponder)

