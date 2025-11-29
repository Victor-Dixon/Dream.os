#!/usr/bin/env python3
"""
Tests for Debate Discord Integration
=====================================

Comprehensive test suite for Discord debate integration functionality.

Author: Agent-7
Date: 2025-11-28
"""

import json
import pytest
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch, mock_open
import requests


class TestDebateDiscordPoster:
    """Test suite for DebateDiscordPoster."""

    @pytest.fixture
    def poster(self):
        """Create poster instance."""
        with patch.dict('os.environ', {'DISCORD_WEBHOOK_URL': 'https://test.webhook.url'}):
            from src.discord_commander.debate_discord_integration import DebateDiscordPoster
            return DebateDiscordPoster()

    @pytest.fixture
    def poster_no_webhook(self):
        """Create poster instance without webhook."""
        with patch.dict('os.environ', {}, clear=True):
            from src.discord_commander.debate_discord_integration import DebateDiscordPoster
            return DebateDiscordPoster()

    def test_poster_initialization_with_webhook(self, poster):
        """Test poster initialization with webhook URL."""
        assert poster is not None
        assert poster.webhook_url == 'https://test.webhook.url'

    def test_poster_initialization_without_webhook(self, poster_no_webhook):
        """Test poster initialization without webhook URL."""
        assert poster_no_webhook is not None
        assert poster_no_webhook.webhook_url is None

    def test_poster_initialization_custom_webhook(self):
        """Test poster initialization with custom webhook."""
        from src.discord_commander.debate_discord_integration import DebateDiscordPoster
        poster = DebateDiscordPoster(webhook_url="https://custom.webhook.url")
        assert poster.webhook_url == "https://custom.webhook.url"

    def test_post_debate_start_success(self, poster):
        """Test successful debate start posting."""
        debate_data = {
            "topic": "Test Topic",
            "description": "Test Description",
            "options": ["Option 1", "Option 2"],
            "debate_id": "test-debate-1",
            "deadline": "2025-12-01"
        }
        
        with patch.object(poster, '_send_to_discord', return_value=True):
            result = poster.post_debate_start(debate_data)
            assert result is True

    def test_post_debate_start_no_webhook(self, poster_no_webhook):
        """Test debate start posting without webhook."""
        debate_data = {"topic": "Test", "options": ["Option 1"]}
        result = poster_no_webhook.post_debate_start(debate_data)
        assert result is False

    def test_post_debate_start_exception(self, poster):
        """Test exception handling in post_debate_start."""
        debate_data = {"topic": "Test", "options": ["Option 1"]}
        
        with patch.object(poster, '_format_debate_start', side_effect=Exception("Test error")):
            result = poster.post_debate_start(debate_data)
            assert result is False

    def test_post_vote_success(self, poster):
        """Test successful vote posting."""
        debate_id = "test-debate-1"
        debate_data = {
            "topic": "Test Topic",
            "options": ["Option 1", "Option 2"]
        }
        
        with patch('pathlib.Path.exists', return_value=True), \
             patch('pathlib.Path.read_text', return_value=json.dumps(debate_data)), \
             patch.object(poster, '_send_to_discord', return_value=True):
            result = poster.post_vote(debate_id, "Agent-7", "Option 1", "Test argument", 8)
            assert result is True

    def test_post_vote_no_webhook(self, poster_no_webhook):
        """Test vote posting without webhook."""
        result = poster_no_webhook.post_vote("test-debate-1", "Agent-7", "Option 1")
        assert result is False

    def test_post_vote_debate_not_found(self, poster):
        """Test vote posting when debate file doesn't exist."""
        with patch('pathlib.Path.exists', return_value=False):
            result = poster.post_vote("test-debate-1", "Agent-7", "Option 1")
            assert result is False

    def test_post_vote_exception(self, poster):
        """Test exception handling in post_vote."""
        with patch('pathlib.Path.exists', return_value=True), \
             patch('pathlib.Path.read_text', side_effect=Exception("Test error")):
            result = poster.post_vote("test-debate-1", "Agent-7", "Option 1")
            assert result is False

    def test_post_debate_status_success(self, poster):
        """Test successful status posting."""
        status_data = {
            "topic": "Test Topic",
            "total_votes": 8,
            "vote_distribution": {"Option 1": 5, "Option 2": 3},
            "debate_id": "test-debate-1"
        }
        
        with patch.object(poster, '_send_to_discord', return_value=True):
            result = poster.post_debate_status("test-debate-1", status_data)
            assert result is True

    def test_post_debate_status_no_webhook(self, poster_no_webhook):
        """Test status posting without webhook."""
        status_data = {"topic": "Test", "total_votes": 0}
        result = poster_no_webhook.post_debate_status("test-debate-1", status_data)
        assert result is False

    def test_post_debate_status_exception(self, poster):
        """Test exception handling in post_debate_status."""
        status_data = {"topic": "Test", "total_votes": 0}
        
        with patch.object(poster, '_format_status', side_effect=Exception("Test error")):
            result = poster.post_debate_status("test-debate-1", status_data)
            assert result is False

    def test_format_debate_start(self, poster):
        """Test debate start formatting."""
        debate_data = {
            "topic": "Test Topic",
            "description": "Test Description",
            "options": ["Option 1", "Option 2", "Option 3"],
            "debate_id": "test-debate-1",
            "deadline": "2025-12-01"
        }
        
        content = poster._format_debate_start(debate_data)
        
        assert "NEW DEBATE STARTED" in content
        assert "Test Topic" in content
        assert "Test Description" in content
        assert "Option 1" in content
        assert "test-debate-1" in content
        assert "2025-12-01" in content

    def test_format_debate_start_no_description(self, poster):
        """Test debate start formatting without description."""
        debate_data = {
            "topic": "Test Topic",
            "options": ["Option 1"],
            "debate_id": "test-debate-1"
        }
        
        content = poster._format_debate_start(debate_data)
        
        assert "Test Topic" in content
        assert "test-debate-1" in content

    def test_format_vote(self, poster):
        """Test vote formatting."""
        content = poster._format_vote(
            agent_id="Agent-7",
            option="Option 1",
            argument="This is a test argument",
            confidence=8,
            topic="Test Topic",
            debate_id="test-debate-1"
        )
        
        assert "Agent-7" in content
        assert "Option 1" in content
        assert "Test Topic" in content
        assert "8/10" in content
        assert "This is a test argument" in content
        assert "test-debate-1" in content

    def test_format_vote_long_argument(self, poster):
        """Test vote formatting with long argument."""
        long_argument = "A" * 400
        content = poster._format_vote(
            agent_id="Agent-7",
            option="Option 1",
            argument=long_argument,
            confidence=5,
            topic="Test Topic",
            debate_id="test-debate-1"
        )
        
        assert "..." in content
        assert len(content) < len(long_argument) + 200

    def test_format_vote_no_argument(self, poster):
        """Test vote formatting without argument."""
        content = poster._format_vote(
            agent_id="Agent-7",
            option="Option 1",
            argument="",
            confidence=5,
            topic="Test Topic",
            debate_id="test-debate-1"
        )
        
        assert "Agent-7" in content
        assert "Option 1" in content
        assert "Argument" not in content

    def test_format_vote_confidence_emoji(self, poster):
        """Test confidence emoji mapping."""
        for confidence in [1, 5, 10]:
            content = poster._format_vote(
                agent_id="Agent-7",
                option="Option 1",
                argument="",
                confidence=confidence,
                topic="Test",
                debate_id="test-1"
            )
            assert str(confidence) in content

    def test_format_status(self, poster):
        """Test status formatting."""
        status_data = {
            "topic": "Test Topic",
            "total_votes": 8,
            "vote_distribution": {"Option 1": 5, "Option 2": 3},
            "debate_id": "test-debate-1",
            "arguments_count": 3
        }
        
        content = poster._format_status(status_data)
        
        assert "DEBATE STATUS UPDATE" in content
        assert "Test Topic" in content
        assert "8/8" in content
        assert "Option 1" in content
        assert "Option 2" in content
        assert "test-debate-1" in content
        assert "3" in content

    def test_format_status_with_consensus(self, poster):
        """Test status formatting with consensus."""
        status_data = {
            "topic": "Test Topic",
            "total_votes": 8,
            "vote_distribution": {"Option 1": 5, "Option 2": 3},
            "debate_id": "test-debate-1",
            "consensus": {
                "option": "Option 1",
                "percent": 62.5
            }
        }
        
        content = poster._format_status(status_data)
        
        assert "Leading Option" in content
        assert "Option 1" in content
        assert "62.5" in content
        assert "MAJORITY REACHED" in content

    def test_format_status_strong_consensus(self, poster):
        """Test status formatting with strong consensus."""
        status_data = {
            "topic": "Test Topic",
            "total_votes": 8,
            "vote_distribution": {"Option 1": 6, "Option 2": 2},
            "debate_id": "test-debate-1",
            "consensus": {
                "option": "Option 1",
                "percent": 75.0
            }
        }
        
        content = poster._format_status(status_data)
        
        assert "STRONG CONSENSUS" in content

    def test_send_to_discord_success(self, poster):
        """Test successful Discord sending."""
        mock_response = MagicMock()
        mock_response.status_code = 204
        
        with patch('requests.post', return_value=mock_response):
            result = poster._send_to_discord("Test content", "Test User")
            assert result is True

    def test_send_to_discord_failure(self, poster):
        """Test failed Discord sending."""
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.text = "Bad Request"
        
        with patch('requests.post', return_value=mock_response):
            result = poster._send_to_discord("Test content", "Test User")
            assert result is False

    def test_send_to_discord_exception(self, poster):
        """Test exception handling in Discord sending."""
        with patch('requests.post', side_effect=Exception("Test error")):
            result = poster._send_to_discord("Test content", "Test User")
            assert result is False

    def test_send_to_discord_timeout(self, poster):
        """Test Discord sending with timeout."""
        with patch('requests.post', side_effect=requests.Timeout("Timeout")):
            result = poster._send_to_discord("Test content", "Test User")
            assert result is False


class TestHelperFunctions:
    """Test helper functions."""

    def test_post_debate_start_to_discord(self):
        """Test post_debate_start_to_discord helper."""
        from src.discord_commander.debate_discord_integration import post_debate_start_to_discord
        
        debate_data = {"topic": "Test", "options": ["Option 1"]}
        
        with patch('src.discord_commander.debate_discord_integration.DebateDiscordPoster') as mock_poster_class:
            mock_poster = MagicMock()
            mock_poster.post_debate_start.return_value = True
            mock_poster_class.return_value = mock_poster
            
            result = post_debate_start_to_discord(debate_data)
            assert result is True
            mock_poster.post_debate_start.assert_called_once_with(debate_data)

    def test_post_vote_to_discord(self):
        """Test post_vote_to_discord helper."""
        from src.discord_commander.debate_discord_integration import post_vote_to_discord
        
        with patch('src.discord_commander.debate_discord_integration.DebateDiscordPoster') as mock_poster_class:
            mock_poster = MagicMock()
            mock_poster.post_vote.return_value = True
            mock_poster_class.return_value = mock_poster
            
            result = post_vote_to_discord("test-1", "Agent-7", "Option 1", "Argument", 8)
            assert result is True
            mock_poster.post_vote.assert_called_once_with("test-1", "Agent-7", "Option 1", "Argument", 8)

    def test_post_debate_status_to_discord(self):
        """Test post_debate_status_to_discord helper."""
        from src.discord_commander.debate_discord_integration import post_debate_status_to_discord
        
        status_data = {"topic": "Test", "total_votes": 0}
        
        with patch('src.discord_commander.debate_discord_integration.DebateDiscordPoster') as mock_poster_class:
            mock_poster = MagicMock()
            mock_poster.post_debate_status.return_value = True
            mock_poster_class.return_value = mock_poster
            
            result = post_debate_status_to_discord("test-1", status_data)
            assert result is True
            mock_poster.post_debate_status.assert_called_once_with("test-1", status_data)

    def test_format_vote_all_confidence_levels(self, poster):
        """Test vote formatting with all confidence levels."""
        confidence_levels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 0, 11, 99]  # Including edge cases
        
        for confidence in confidence_levels:
            content = poster._format_vote(
                agent_id="Agent-7",
                option="Option 1",
                argument="",
                confidence=confidence,
                topic="Test",
                debate_id="test-1"
            )
            assert "Agent-7" in content
            assert str(confidence) in content or "0" in content

    def test_format_status_zero_votes(self, poster):
        """Test status formatting with zero votes."""
        status_data = {
            "topic": "Test Topic",
            "total_votes": 0,
            "vote_distribution": {},
            "debate_id": "test-debate-1"
        }
        
        content = poster._format_status(status_data)
        
        assert "0/8" in content
        assert "Test Topic" in content

    def test_format_status_no_consensus(self, poster):
        """Test status formatting without consensus."""
        status_data = {
            "topic": "Test Topic",
            "total_votes": 8,
            "vote_distribution": {"Option 1": 4, "Option 2": 4},
            "debate_id": "test-debate-1"
        }
        
        content = poster._format_status(status_data)
        
        assert "8/8" in content
        assert "Option 1" in content
        assert "Option 2" in content
        # Should not have "Leading Option" without consensus
        assert "Leading Option" not in content

    def test_format_status_consensus_below_50(self, poster):
        """Test status formatting with consensus below 50%."""
        status_data = {
            "topic": "Test Topic",
            "total_votes": 8,
            "vote_distribution": {"Option 1": 3, "Option 2": 5},
            "debate_id": "test-debate-1",
            "consensus": {
                "option": "Option 2",
                "percent": 37.5
            }
        }
        
        content = poster._format_status(status_data)
        
        assert "Leading Option" in content
        assert "37.5" in content
        assert "MAJORITY REACHED" not in content

    def test_format_status_no_arguments_count(self, poster):
        """Test status formatting without arguments_count."""
        status_data = {
            "topic": "Test Topic",
            "total_votes": 8,
            "vote_distribution": {"Option 1": 5, "Option 2": 3},
            "debate_id": "test-debate-1"
        }
        
        content = poster._format_status(status_data)
        
        assert "Arguments Posted" not in content

    def test_format_debate_start_no_deadline(self, poster):
        """Test debate start formatting without deadline."""
        debate_data = {
            "topic": "Test Topic",
            "description": "Test Description",
            "options": ["Option 1", "Option 2"],
            "debate_id": "test-debate-1"
        }
        
        content = poster._format_debate_start(debate_data)
        
        assert "Test Topic" in content
        assert "test-debate-1" in content
        assert "Deadline" not in content

    def test_post_vote_invalid_json(self, poster):
        """Test vote posting with invalid JSON in debate file."""
        with patch('pathlib.Path.exists', return_value=True), \
             patch('pathlib.Path.read_text', return_value="invalid json"):
            result = poster.post_vote("test-debate-1", "Agent-7", "Option 1")
            assert result is False

    def test_send_to_discord_connection_error(self, poster):
        """Test Discord sending with connection error."""
        import requests
        with patch('requests.post', side_effect=requests.ConnectionError("Connection error")):
            result = poster._send_to_discord("Test content", "Test User")
            assert result is False

    def test_send_to_discord_non_204_status(self, poster):
        """Test Discord sending with non-204 status codes."""
        for status_code in [200, 201, 400, 401, 403, 404, 500]:
            mock_response = MagicMock()
            mock_response.status_code = status_code
            mock_response.text = f"Status {status_code}"
            
            with patch('requests.post', return_value=mock_response):
                result = poster._send_to_discord("Test content", "Test User")
                assert result is False