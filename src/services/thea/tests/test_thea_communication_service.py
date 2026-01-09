#!/usr/bin/env python3
"""
Unit Tests for Thea Communication Service
========================================

<!-- SSOT Domain: thea -->

Unit tests for the Thea communication service.
Demonstrates testing with mocked dependencies.

V2 Compliance: Isolated unit tests that prove the modular architecture works.

Author: Agent-4 (V2 Architecture Specialist)
Date: 2025-01-08
License: MIT
"""

import pytest
from unittest.mock import Mock, MagicMock

from src.services.thea.domain.models import CommunicationResult, TheaMessage, TheaResponse
from src.services.thea.domain.enums import MessagePriority
from src.services.thea.services.implementations.thea_communication_service import TheaCommunicationService


class TestTheaCommunicationService:
    """Unit tests for Thea communication service."""

    def setup_method(self):
        """Set up test fixtures with mocked dependencies."""
        self.mock_browser_repo = Mock()
        self.mock_conversation_repo = Mock()
        self.mock_auth_service = Mock()
        self.mock_response_service = Mock()

        self.service = TheaCommunicationService(
            browser_repository=self.mock_browser_repo,
            conversation_repository=self.mock_conversation_repo,
            authentication_service=self.mock_auth_service,
            response_service=self.mock_response_service
        )

    def test_validate_message_content_valid(self):
        """Test validating valid message content."""
        assert self.service.validate_message_content("Hello Thea!") is True
        assert self.service.validate_message_content("This is a valid message.") is True

    def test_validate_message_content_empty(self):
        """Test validating empty message content."""
        assert self.service.validate_message_content("") is False
        assert self.service.validate_message_content("   ") is False
        assert self.service.validate_message_content(None) is False

    def test_validate_message_content_too_long(self):
        """Test validating message content that's too long."""
        long_message = "x" * 10001  # Over 10,000 character limit
        assert self.service.validate_message_content(long_message) is False

    def test_validate_message_content_harmful(self):
        """Test validating message content with potentially harmful content."""
        harmful_content = "Hello <script>alert('xss')</script>"
        assert self.service.validate_message_content(harmful_content) is False

        harmful_content2 = "javascript:alert('xss')"
        assert self.service.validate_message_content(harmful_content2) is False

    def test_send_message_successful_flow(self):
        """Test successful message sending flow."""
        # Setup mocks
        self.mock_auth_service.ensure_authenticated.return_value = True

        mock_response = TheaResponse(
            content="Thea response",
            message_id="test-message-id"
        )
        self.mock_response_service.extract_response.return_value = mock_response
        self.mock_conversation_repo.save_conversation.return_value = True

        # Mock browser operations
        self.mock_browser_repo.get_current_url.return_value = "https://chatgpt.com"
        self.mock_browser_repo.navigate_to_url.return_value = True
        self.mock_browser_repo.is_page_ready.return_value = True
        self.mock_browser_repo.find_input_element.return_value = Mock()
        self.mock_browser_repo.send_text_to_element.return_value = True
        self.mock_browser_repo.submit_form.return_value = True

        # Execute
        result = self.service.send_message("Test message")

        # Verify
        assert result.success is True
        assert result.message.content == "Test message"
        assert result.response == mock_response
        assert result.error_message is None

        # Verify interactions
        self.mock_auth_service.ensure_authenticated.assert_called_once()
        self.mock_response_service.extract_response.assert_called_once()
        self.mock_conversation_repo.save_conversation.assert_called_once()

    def test_send_message_authentication_failure(self):
        """Test message sending when authentication fails."""
        self.mock_auth_service.ensure_authenticated.return_value = False

        result = self.service.send_message("Test message")

        assert result.success is False
        assert "Authentication failed" in result.error_message
        assert self.mock_response_service.extract_response.called is False

    def test_send_message_validation_failure(self):
        """Test message sending with invalid content."""
        result = self.service.send_message("")

        assert result.success is False
        assert "Invalid message content" in result.error_message

    def test_send_message_browser_failure(self):
        """Test message sending when browser operations fail."""
        self.mock_auth_service.ensure_authenticated.return_value = True
        self.mock_browser_repo.navigate_to_url.return_value = False

        result = self.service.send_message("Test message")

        assert result.success is False
        assert "Message delivery failed" in result.error_message

    def test_send_message_no_response(self):
        """Test message sending when no response is received."""
        # Setup mocks for successful send but no response
        self.mock_auth_service.ensure_authenticated.return_value = True
        self.mock_response_service.extract_response.return_value = None

        # Mock successful browser operations
        self.mock_browser_repo.get_current_url.return_value = "https://chatgpt.com"
        self.mock_browser_repo.navigate_to_url.return_value = True
        self.mock_browser_repo.is_page_ready.return_value = True
        self.mock_browser_repo.find_input_element.return_value = Mock()
        self.mock_browser_repo.send_text_to_element.return_value = True
        self.mock_browser_repo.submit_form.return_value = True

        result = self.service.send_message("Test message")

        assert result.success is False
        assert "No response received" in result.error_message

    def test_get_recent_conversations(self):
        """Test getting recent conversations."""
        mock_conversations = [Mock(), Mock(), Mock()]
        self.mock_conversation_repo.get_recent_conversations.return_value = mock_conversations

        result = self.service.get_recent_conversations(limit=5)

        assert result == mock_conversations
        self.mock_conversation_repo.get_recent_conversations.assert_called_once_with(5)

    def test_search_conversations(self):
        """Test searching conversations."""
        mock_results = [Mock(), Mock()]
        self.mock_conversation_repo.search_conversations.return_value = mock_results

        result = self.service.search_conversations("test query", limit=10)

        assert result == mock_results
        self.mock_conversation_repo.search_conversations.assert_called_once_with("test query", 10)

    def test_get_message_status(self):
        """Test getting message status."""
        mock_message = TheaMessage(content="test", priority=MessagePriority.NORMAL)
        mock_conversation = Mock()
        mock_conversation.message = mock_message

        self.mock_conversation_repo.get_conversations_by_message_id.return_value = [mock_conversation]

        result = self.service.get_message_status("test-id")

        assert result == mock_message
        self.mock_conversation_repo.get_conversations_by_message_id.assert_called_once_with("test-id")

    def test_get_message_status_not_found(self):
        """Test getting message status when not found."""
        self.mock_conversation_repo.get_conversations_by_message_id.return_value = []

        result = self.service.get_message_status("nonexistent-id")

        assert result is None

    def test_get_response(self):
        """Test getting response for message."""
        mock_response = TheaResponse(content="test response", message_id="test-id")
        mock_conversation = Mock()
        mock_conversation.response = mock_response

        self.mock_conversation_repo.get_conversations_by_message_id.return_value = [mock_conversation]

        result = self.service.get_response("test-id")

        assert result == mock_response

    def test_send_message_async(self):
        """Test async message sending."""
        message_id = self.service.send_message_async("Async message")

        assert isinstance(message_id, str)
        assert len(message_id) > 0  # Should return a valid message ID

    def test_wait_for_response_completed(self):
        """Test waiting for response when already completed."""
        mock_response = TheaResponse(content="completed response", message_id="test-id")
        mock_conversation = Mock()
        mock_conversation.response = mock_response

        self.mock_conversation_repo.get_conversations_by_message_id.return_value = [mock_conversation]

        result = self.service.wait_for_response("test-id", timeout_seconds=10)

        assert result == mock_response
        # Should return immediately without polling

    def test_wait_for_response_pending_timeout(self):
        """Test waiting for response when pending and times out."""
        # Conversation exists but no response yet
        mock_conversation = Mock()
        mock_conversation.response = None

        self.mock_conversation_repo.get_conversations_by_message_id.return_value = [mock_conversation]

        result = self.service.wait_for_response("test-id", timeout_seconds=1)  # Short timeout

        assert result is None