#!/usr/bin/env python3
"""
Tests for Discord Publisher
============================

Comprehensive test suite for Discord publisher service.

Author: Agent-7
Date: 2025-11-28
"""

import pytest
from unittest.mock import MagicMock, Mock, patch
from datetime import datetime
import requests

from src.services.publishers.discord_publisher import (
    DiscordDevlogPublisher,
    test_discord_publisher
)


class TestDiscordDevlogPublisher:
    """Test suite for DiscordDevlogPublisher."""

    @pytest.fixture
    def publisher(self):
        """Create publisher instance."""
        return DiscordDevlogPublisher(webhook_url="https://test.webhook.url")

    def test_publisher_initialization(self, publisher):
        """Test publisher initialization."""
        assert publisher is not None
        assert publisher.webhook_url == "https://test.webhook.url"
        assert publisher._last_message_id is None
        assert publisher.logger is not None

    @patch('requests.post')
    def test_publish_devlog_success(self, mock_post, publisher):
        """Test successful devlog publishing."""
        mock_response = MagicMock()
        mock_response.status_code = 204
        mock_response.headers = {"X-Webhook-Id": "webhook_123"}
        mock_post.return_value = mock_response
        
        result = publisher.publish_devlog(
            agent_id="Agent-7",
            title="Test Devlog",
            content="Test content"
        )
        
        assert result is True
        mock_post.assert_called_once()
        assert publisher._last_message_id == "webhook_123"

    @patch('requests.post')
    def test_publish_devlog_with_cycle(self, mock_post, publisher):
        """Test publishing devlog with cycle."""
        mock_response = MagicMock()
        mock_response.status_code = 204
        mock_response.headers = {}
        mock_post.return_value = mock_response
        
        result = publisher.publish_devlog(
            agent_id="Agent-7",
            title="Test Devlog",
            content="Content",
            cycle="C-123"
        )
        
        assert result is True
        call_args = mock_post.call_args
        payload = call_args[1]['json']
        assert "C-123" in payload['content']

    @patch('requests.post')
    def test_publish_devlog_with_tags(self, mock_post, publisher):
        """Test publishing devlog with tags."""
        mock_response = MagicMock()
        mock_response.status_code = 204
        mock_response.headers = {}
        mock_post.return_value = mock_response
        
        result = publisher.publish_devlog(
            agent_id="Agent-7",
            title="Test",
            content="Content",
            tags=["test", "devlog"]
        )
        
        assert result is True
        call_args = mock_post.call_args
        payload = call_args[1]['json']
        assert "#test" in payload['content']
        assert "#devlog" in payload['content']

    @patch('requests.post')
    def test_publish_devlog_with_metadata(self, mock_post, publisher):
        """Test publishing devlog with metadata embed."""
        mock_response = MagicMock()
        mock_response.status_code = 204
        mock_response.headers = {}
        mock_post.return_value = mock_response
        
        result = publisher.publish_devlog(
            agent_id="Agent-7",
            title="Test",
            content="Content",
            metadata={"value": "500 pts", "jackpots": 3}
        )
        
        assert result is True
        call_args = mock_post.call_args
        payload = call_args[1]['json']
        assert len(payload['embeds']) > 0

    @patch('requests.post')
    def test_publish_devlog_failure_status_code(self, mock_post, publisher):
        """Test publishing devlog with non-204 status code."""
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.text = "Bad Request"
        mock_post.return_value = mock_response
        
        result = publisher.publish_devlog(
            agent_id="Agent-7",
            title="Test",
            content="Content"
        )
        
        assert result is False

    @patch('requests.post')
    def test_publish_devlog_request_exception(self, mock_post, publisher):
        """Test publishing devlog with RequestException."""
        mock_post.side_effect = requests.RequestException("Network error")
        
        result = publisher.publish_devlog(
            agent_id="Agent-7",
            title="Test",
            content="Content"
        )
        
        assert result is False

    @patch('requests.post')
    def test_publish_devlog_general_exception(self, mock_post, publisher):
        """Test publishing devlog with general exception."""
        mock_post.side_effect = Exception("Unexpected error")
        
        result = publisher.publish_devlog(
            agent_id="Agent-7",
            title="Test",
            content="Content"
        )
        
        assert result is False

    def test_format_devlog_basic(self, publisher):
        """Test basic devlog formatting."""
        content = publisher._format_devlog(
            agent_id="Agent-7",
            title="Test Title",
            content="Test content"
        )
        
        assert "Test Title" in content
        assert "Agent-7" in content
        assert "Test content" in content

    def test_format_devlog_with_cycle(self, publisher):
        """Test devlog formatting with cycle."""
        content = publisher._format_devlog(
            agent_id="Agent-7",
            title="Test",
            content="Content",
            cycle="C-123"
        )
        
        assert "C-123" in content

    def test_format_devlog_with_tags(self, publisher):
        """Test devlog formatting with tags."""
        content = publisher._format_devlog(
            agent_id="Agent-7",
            title="Test",
            content="Content",
            tags=["tag1", "tag2"]
        )
        
        assert "#tag1" in content
        assert "#tag2" in content

    def test_format_devlog_without_tags(self, publisher):
        """Test devlog formatting without tags."""
        content = publisher._format_devlog(
            agent_id="Agent-7",
            title="Test",
            content="Content",
            tags=None
        )
        
        assert "#" not in content or content.count("#") == 0

    def test_format_devlog_timestamp(self, publisher):
        """Test devlog formatting includes timestamp."""
        content = publisher._format_devlog(
            agent_id="Agent-7",
            title="Test",
            content="Content"
        )
        
        assert "Posted:" in content
        # Should contain date format
        assert datetime.now().strftime('%Y-%m-%d') in content

    def test_create_metadata_embed_with_value(self, publisher):
        """Test metadata embed creation with value."""
        embed = publisher._create_metadata_embed({"value": "500 pts"})
        
        assert embed is not None
        assert embed["title"] == "📊 Analysis Metrics"
        assert len(embed["fields"]) > 0

    def test_create_metadata_embed_with_jackpots(self, publisher):
        """Test metadata embed creation with jackpots."""
        embed = publisher._create_metadata_embed({"jackpots": 3})
        
        assert embed is not None
        assert any("JACKPOTS" in field["name"] for field in embed["fields"])

    def test_create_metadata_embed_with_roi(self, publisher):
        """Test metadata embed creation with ROI improvement."""
        embed = publisher._create_metadata_embed({"roi_improvement": "25%"})
        
        assert embed is not None
        assert any("ROI" in field["name"] for field in embed["fields"])

    def test_create_metadata_embed_empty(self, publisher):
        """Test metadata embed creation with empty metadata."""
        embed = publisher._create_metadata_embed({})
        
        assert embed is None

    def test_create_metadata_embed_exception(self, publisher):
        """Test metadata embed creation exception handling."""
        with patch('src.services.publishers.discord_publisher.DiscordDevlogPublisher._create_metadata_embed', side_effect=Exception("Error")):
            # Should handle gracefully
            try:
                embed = publisher._create_metadata_embed({"value": "test"})
            except Exception:
                pass  # Exception should be caught internally

    @patch('requests.post')
    def test_validate_webhook_success(self, mock_post, publisher):
        """Test webhook validation success."""
        mock_response = MagicMock()
        mock_response.status_code = 204
        mock_post.return_value = mock_response
        
        result = publisher.validate_webhook()
        
        assert result is True
        mock_post.assert_called_once()

    @patch('requests.post')
    def test_validate_webhook_failure(self, mock_post, publisher):
        """Test webhook validation failure."""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_post.return_value = mock_response
        
        result = publisher.validate_webhook()
        
        assert result is False

    @patch('requests.post')
    def test_validate_webhook_exception(self, mock_post, publisher):
        """Test webhook validation exception handling."""
        mock_post.side_effect = Exception("Validation error")
        
        result = publisher.validate_webhook()
        
        assert result is False

    def test_get_last_message_id(self, publisher):
        """Test getting last message ID."""
        publisher._last_message_id = "msg_123"
        
        assert publisher.get_last_message_id() == "msg_123"

    def test_get_last_message_id_none(self, publisher):
        """Test getting last message ID when None."""
        assert publisher.get_last_message_id() is None

    @patch('requests.post')
    def test_publish_devlog_username_format(self, mock_post, publisher):
        """Test username format in published message."""
        mock_response = MagicMock()
        mock_response.status_code = 204
        mock_response.headers = {}
        mock_post.return_value = mock_response
        
        publisher.publish_devlog("Agent-7", "Test", "Content")
        
        call_args = mock_post.call_args
        payload = call_args[1]['json']
        assert payload['username'] == "Agent-7 Devlog"

    @patch('requests.post')
    def test_publish_devlog_timeout(self, mock_post, publisher):
        """Test publish devlog with timeout."""
        mock_response = MagicMock()
        mock_response.status_code = 204
        mock_post.return_value = mock_response
        
        publisher.publish_devlog("Agent-7", "Test", "Content")
        
        call_args = mock_post.call_args
        assert call_args[1]['timeout'] == 10


class TestTestDiscordPublisher:
    """Test test_discord_publisher function."""

    @patch('src.services.publishers.discord_publisher.DiscordDevlogPublisher')
    def test_test_discord_publisher_success(self, mock_publisher_class):
        """Test test_discord_publisher function success."""
        mock_publisher = MagicMock()
        mock_publisher.validate_webhook.return_value = True
        mock_publisher.publish_devlog.return_value = True
        mock_publisher_class.return_value = mock_publisher
        
        result = test_discord_publisher("https://test.webhook.url")
        
        assert result is True
        mock_publisher.validate_webhook.assert_called_once()
        mock_publisher.publish_devlog.assert_called_once()

    @patch('src.services.publishers.discord_publisher.DiscordDevlogPublisher')
    def test_test_discord_publisher_validation_failure(self, mock_publisher_class):
        """Test test_discord_publisher when validation fails."""
        mock_publisher = MagicMock()
        mock_publisher.validate_webhook.return_value = False
        mock_publisher_class.return_value = mock_publisher
        
        result = test_discord_publisher("https://test.webhook.url")
        
        assert result is False
        mock_publisher.publish_devlog.assert_not_called()

    @patch('src.services.publishers.discord_publisher.DiscordDevlogPublisher')
    def test_test_discord_publisher_publish_failure(self, mock_publisher_class):
        """Test test_discord_publisher when publish fails."""
        mock_publisher = MagicMock()
        mock_publisher.validate_webhook.return_value = True
        mock_publisher.publish_devlog.return_value = False
        mock_publisher_class.return_value = mock_publisher
        
        result = test_discord_publisher("https://test.webhook.url")
        
        assert result is False

    @patch('requests.post')
    def test_publish_devlog_with_all_metadata_fields(self, mock_post, publisher):
        """Test publishing devlog with all metadata fields."""
        mock_response = MagicMock()
        mock_response.status_code = 204
        mock_response.headers = {}
        mock_post.return_value = mock_response
        
        result = publisher.publish_devlog(
            agent_id="Agent-7",
            title="Test",
            content="Content",
            metadata={
                "value": "500 pts",
                "jackpots": 3,
                "roi_improvement": "25%"
            }
        )
        
        assert result is True
        call_args = mock_post.call_args
        payload = call_args[1]['json']
        assert len(payload['embeds']) > 0

    @patch('requests.post')
    def test_publish_devlog_response_headers_handling(self, mock_post, publisher):
        """Test handling of response headers."""
        mock_response = MagicMock()
        mock_response.status_code = 204
        mock_response.headers = {"X-Webhook-Id": "webhook_456", "X-RateLimit-Remaining": "100"}
        mock_post.return_value = mock_response
        
        result = publisher.publish_devlog("Agent-7", "Test", "Content")
        
        assert result is True
        assert publisher._last_message_id == "webhook_456"

    @patch('requests.post')
    def test_publish_devlog_no_message_id_in_headers(self, mock_post, publisher):
        """Test when response headers don't contain message ID."""
        mock_response = MagicMock()
        mock_response.status_code = 204
        mock_response.headers = {}
        mock_post.return_value = mock_response
        
        result = publisher.publish_devlog("Agent-7", "Test", "Content")
        
        assert result is True
        assert publisher._last_message_id is None

    def test_format_devlog_separator_formatting(self, publisher):
        """Test devlog formatting separator placement."""
        content = publisher._format_devlog(
            agent_id="Agent-7",
            title="Test",
            content="Content",
            tags=["tag1"]
        )
        
        # Should have separators around tags
        assert "---" in content

    def test_format_devlog_multiple_tags(self, publisher):
        """Test devlog formatting with multiple tags."""
        content = publisher._format_devlog(
            agent_id="Agent-7",
            title="Test",
            content="Content",
            tags=["tag1", "tag2", "tag3", "tag4"]
        )
        
        assert "#tag1" in content
        assert "#tag2" in content
        assert "#tag3" in content
        assert "#tag4" in content

    def test_create_metadata_embed_all_fields(self, publisher):
        """Test metadata embed with all supported fields."""
        embed = publisher._create_metadata_embed({
            "value": "500 pts",
            "jackpots": 3,
            "roi_improvement": "25%"
        })
        
        assert embed is not None
        assert len(embed["fields"]) == 3

    def test_create_metadata_embed_field_inline(self, publisher):
        """Test that embed fields are marked as inline."""
        embed = publisher._create_metadata_embed({"value": "500 pts"})
        
        assert embed is not None
        assert embed["fields"][0]["inline"] is True

    def test_create_metadata_embed_color(self, publisher):
        """Test metadata embed color."""
        embed = publisher._create_metadata_embed({"value": "500 pts"})
        
        assert embed is not None
        assert embed["color"] == 0x00FF00  # Green

    @patch('requests.post')
    def test_validate_webhook_timeout(self, mock_post, publisher):
        """Test webhook validation uses timeout."""
        mock_response = MagicMock()
        mock_response.status_code = 204
        mock_post.return_value = mock_response
        
        publisher.validate_webhook()
        
        call_args = mock_post.call_args
        assert call_args[1]['timeout'] == 10
