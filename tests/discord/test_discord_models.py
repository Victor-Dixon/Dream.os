#!/usr/bin/env python3
"""
Tests for Discord Models
=========================

Tests for Discord data models.

Author: Agent-7
Date: 2025-11-26
"""

import pytest
from unittest.mock import MagicMock, patch


class TestDiscordModels:
    """Test suite for Discord models."""

    def test_command_result_creation(self):
        """Test CommandResult model creation."""
        from src.discord_commander.discord_models import CommandResult, create_command_result
        
        # Test direct creation
        result = CommandResult(
            success=True,
            message="Test message",
            data={"key": "value"}
        )
        assert result.success is True
        assert result.message == "Test message"
        assert result.data == {"key": "value"}
        assert result.timestamp is not None
        
        # Test factory function
        result2 = create_command_result(
            success=False,
            message="Error message",
            error_code="TEST_ERROR"
        )
        assert result2.success is False
        assert result2.error_code == "TEST_ERROR"

    def test_discord_message_creation(self):
        """Test DiscordMessage model creation."""
        from src.discord_commander.discord_models import DiscordMessage
        
        message = DiscordMessage(
            content="Test content",
            author="TestAuthor",
            channel="TestChannel"
        )
        assert message.content == "Test content"
        assert message.author == "TestAuthor"
        assert message.channel == "TestChannel"
        assert message.timestamp is not None

    def test_agent_command_validation(self):
        """Test AgentCommand validation."""
        from src.discord_commander.discord_models import AgentCommand
        
        # Valid command
        valid_cmd = AgentCommand(
            agent_id="Agent-7",
            command="test",
            priority="HIGH"
        )
        assert valid_cmd.validate() is True
        
        # Invalid command (missing agent_id)
        invalid_cmd = AgentCommand(
            agent_id="",
            command="test"
        )
        assert invalid_cmd.validate() is False
        
        # Invalid priority
        invalid_priority = AgentCommand(
            agent_id="Agent-7",
            command="test",
            priority="INVALID"
        )
        assert invalid_priority.validate() is False

    def test_communication_stats(self):
        """Test CommunicationStats model."""
        from src.discord_commander.discord_models import CommunicationStats
        
        stats = CommunicationStats(
            messages_sent=10,
            messages_received=5,
            commands_executed=3
        )
        assert stats.messages_sent == 10
        assert stats.messages_received == 5
        
        # Test to_dict
        stats_dict = stats.to_dict()
        assert isinstance(stats_dict, dict)
        assert stats_dict["messages_sent"] == 10

