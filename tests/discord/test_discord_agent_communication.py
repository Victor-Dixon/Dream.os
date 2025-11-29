#!/usr/bin/env python3
"""
Tests for Discord Agent Communication
======================================

Comprehensive test suite for Discord agent communication functionality.

Author: Agent-7
Date: 2025-11-28
"""

import asyncio
import json
import os
import pytest
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, Mock, patch, mock_open
from datetime import datetime

from src.discord_commander.discord_agent_communication import (
    AgentCommunicationEngine,
    create_agent_communication_engine,
)
from src.discord_commander.discord_models import CommandResult


class TestAgentCommunicationEngine:
    """Test suite for AgentCommunicationEngine."""

    @pytest.fixture
    def engine(self):
        """Create engine instance."""
        with patch('src.discord_commander.discord_agent_communication.get_unified_utility'):
            engine = AgentCommunicationEngine()
            return engine

    @pytest.fixture
    def mock_utility(self):
        """Mock unified utility."""
        utility = MagicMock()
        utility.path = os.path
        utility.makedirs = os.makedirs
        return utility

    def test_engine_initialization(self, engine):
        """Test engine initialization."""
        assert engine is not None
        assert engine.logger is not None
        assert engine._utility is not None

    def test_setup_logger(self, engine):
        """Test logger setup."""
        logger = engine._setup_logger()
        assert logger is not None
        assert logger.name == "discord_commander"
        assert logger.level == 20  # INFO level

    def test_get_unified_utility(self, engine):
        """Test getting unified utility."""
        utility = engine._get_unified_utility()
        assert utility is not None

    @pytest.mark.asyncio
    async def test_send_to_agent_inbox_success(self, engine):
        """Test successful message sending to agent inbox."""
        with patch('src.discord_commander.discord_agent_communication.create_inbox_message', return_value=True), \
             patch('pathlib.Path.glob') as mock_glob, \
             patch('pathlib.Path.stat') as mock_stat:
            
            # Mock file path
            mock_file = MagicMock()
            mock_file.name = "INBOX_MESSAGE_2025-11-28_120000.md"
            mock_file.stat.return_value.st_mtime = 1234567890
            mock_glob.return_value = [mock_file]
            
            result = await engine.send_to_agent_inbox("Agent-7", "Test message", "TestSender")
            
            assert result.success is True
            assert "successfully delivered" in result.message.lower()
            assert result.agent == "Agent-7"
            assert result.data is not None

    @pytest.mark.asyncio
    async def test_send_to_agent_inbox_failure(self, engine):
        """Test failed message sending to agent inbox."""
        with patch('src.discord_commander.discord_agent_communication.create_inbox_message', return_value=False):
            result = await engine.send_to_agent_inbox("Agent-7", "Test message", "TestSender")
            
            assert result.success is False
            assert "failed" in result.message.lower()
            assert result.agent == "Agent-7"

    @pytest.mark.asyncio
    async def test_send_to_agent_inbox_exception(self, engine):
        """Test exception handling in send_to_agent_inbox."""
        with patch('src.discord_commander.discord_agent_communication.create_inbox_message', side_effect=Exception("Test error")):
            result = await engine.send_to_agent_inbox("Agent-7", "Test message", "TestSender")
            
            assert result.success is False
            assert "failed" in result.message.lower()

    @pytest.mark.asyncio
    async def test_broadcast_to_all_agents_success(self, engine):
        """Test successful broadcast to all agents."""
        with patch.object(engine, 'send_to_agent_inbox') as mock_send:
            mock_result = CommandResult(success=True, message="Success")
            mock_send.return_value = mock_result
            
            result = await engine.broadcast_to_all_agents("Test broadcast", "TestSender")
            
            assert result.success is True
            assert mock_send.call_count == 8  # All 8 agents
            assert "successfully delivered" in result.message.lower()

    @pytest.mark.asyncio
    async def test_broadcast_to_all_agents_partial_failure(self, engine):
        """Test broadcast with partial failures."""
        with patch.object(engine, 'send_to_agent_inbox') as mock_send:
            # First 4 succeed, last 4 fail
            mock_send.side_effect = [
                CommandResult(success=True, message="Success"),
                CommandResult(success=True, message="Success"),
                CommandResult(success=True, message="Success"),
                CommandResult(success=True, message="Success"),
                CommandResult(success=False, message="Failed"),
                CommandResult(success=False, message="Failed"),
                CommandResult(success=False, message="Failed"),
                CommandResult(success=False, message="Failed"),
            ]
            
            result = await engine.broadcast_to_all_agents("Test broadcast", "TestSender")
            
            assert result.success is False
            assert "partially failed" in result.message.lower()
            assert result.data["successful_deliveries"] == 4

    @pytest.mark.asyncio
    async def test_broadcast_to_all_agents_exception(self, engine):
        """Test exception handling in broadcast."""
        with patch.object(engine, 'send_to_agent_inbox', side_effect=Exception("Test error")):
            result = await engine.broadcast_to_all_agents("Test broadcast", "TestSender")
            
            assert result.success is False
            assert "failed" in result.message.lower()

    @pytest.mark.asyncio
    async def test_send_human_prompt_to_captain(self, engine):
        """Test sending human prompt to Captain."""
        with patch.object(engine, 'send_to_agent_inbox') as mock_send:
            mock_result = CommandResult(success=True, message="Success", agent="Agent-4")
            mock_send.return_value = mock_result
            
            result = await engine.send_human_prompt_to_captain("Test prompt", "TestSender")
            
            assert result.success is True
            mock_send.assert_called_once_with("Agent-4", "Test prompt", "TestSender")

    @pytest.mark.asyncio
    async def test_send_human_prompt_to_captain_exception(self, engine):
        """Test exception handling in send_human_prompt_to_captain."""
        with patch.object(engine, 'send_to_agent_inbox', side_effect=Exception("Test error")):
            result = await engine.send_human_prompt_to_captain("Test prompt", "TestSender")
            
            assert result.success is False
            assert "failed" in result.message.lower()

    @pytest.mark.asyncio
    async def test_execute_agent_command_success(self, engine):
        """Test successful command execution."""
        with patch('asyncio.sleep'):
            result = await engine.execute_agent_command("Agent-7", "test_command")
            
            assert result.success is True
            assert "executed successfully" in result.message.lower()
            assert result.agent == "Agent-7"
            assert result.execution_time is not None

    @pytest.mark.asyncio
    async def test_execute_agent_command_exception(self, engine):
        """Test exception handling in command execution."""
        with patch('asyncio.sleep', side_effect=Exception("Test error")):
            result = await engine.execute_agent_command("Agent-7", "test_command")
            
            assert result.success is False
            assert "failed" in result.message.lower()
            assert result.execution_time is not None

    def test_get_agent_status_file_path(self, engine, mock_utility):
        """Test getting agent status file path."""
        engine._utility = mock_utility
        path = engine.get_agent_status_file_path("Agent-7")
        
        assert "agent_workspaces" in path
        assert "Agent-7" in path
        assert "status.json" in path

    @pytest.mark.asyncio
    async def test_read_agent_status_success(self, engine):
        """Test successful status reading."""
        test_status = {"agent_id": "Agent-7", "status": "ACTIVE"}
        
        with patch('builtins.open', mock_open(read_data=json.dumps(test_status))), \
             patch.object(engine._utility.path, 'exists', return_value=True):
            result = await engine.read_agent_status("Agent-7")
            
            assert result is not None
            assert result["agent_id"] == "Agent-7"

    @pytest.mark.asyncio
    async def test_read_agent_status_file_not_found(self, engine):
        """Test status reading when file doesn't exist."""
        with patch.object(engine._utility.path, 'exists', return_value=False):
            result = await engine.read_agent_status("Agent-7")
            
            assert result is None

    @pytest.mark.asyncio
    async def test_read_agent_status_exception(self, engine):
        """Test exception handling in status reading."""
        with patch.object(engine._utility.path, 'exists', return_value=True), \
             patch('builtins.open', side_effect=Exception("Test error")):
            result = await engine.read_agent_status("Agent-7")
            
            assert result is None

    @pytest.mark.asyncio
    async def test_cleanup_old_messages_success(self, engine):
        """Test successful message cleanup."""
        with patch('os.listdir', return_value=["INBOX_MESSAGE_old.md", "INBOX_MESSAGE_new.md"]), \
             patch('os.path.getmtime', side_effect=[1000000000, 2000000000]), \
             patch('os.remove'), \
             patch.object(engine._utility.path, 'exists', return_value=True), \
             patch('datetime.datetime') as mock_datetime:
            
            mock_datetime.utcnow.return_value.timestamp.return_value = 2000000000
            
            result = await engine.cleanup_old_messages("Agent-7", max_age_hours=1)
            
            assert result >= 0

    @pytest.mark.asyncio
    async def test_cleanup_old_messages_no_inbox(self, engine):
        """Test cleanup when inbox doesn't exist."""
        with patch.object(engine._utility.path, 'exists', return_value=False):
            result = await engine.cleanup_old_messages("Agent-7")
            
            assert result == 0

    @pytest.mark.asyncio
    async def test_cleanup_old_messages_exception(self, engine):
        """Test exception handling in cleanup."""
        with patch.object(engine._utility.path, 'exists', return_value=True), \
             patch('os.listdir', side_effect=Exception("Test error")):
            result = await engine.cleanup_old_messages("Agent-7")
            
            assert result == 0

    def test_is_valid_agent(self, engine):
        """Test agent validation."""
        assert engine.is_valid_agent("Agent-1") is True
        assert engine.is_valid_agent("Agent-8") is True
        assert engine.is_valid_agent("Agent-9") is False
        assert engine.is_valid_agent("Invalid") is False

    def test_get_all_agent_names(self, engine):
        """Test getting all agent names."""
        names = engine.get_all_agent_names()
        
        assert len(names) == 8
        assert "Agent-1" in names
        assert "Agent-8" in names

    def test_validate_agent_name(self, engine):
        """Test agent name validation."""
        assert engine.validate_agent_name("Agent-1") is True
        assert engine.validate_agent_name("Agent-8") is True
        assert engine.validate_agent_name("") is False
        assert engine.validate_agent_name(None) is False
        assert engine.validate_agent_name("Agent") is False
        assert engine.validate_agent_name("Invalid") is False

    def test_format_timestamp(self, engine):
        """Test timestamp formatting."""
        timestamp = engine.format_timestamp()
        
        assert timestamp is not None
        assert isinstance(timestamp, str)

    def test_create_message_metadata(self, engine):
        """Test message metadata creation."""
        metadata = engine.create_message_metadata("Sender", "Recipient", "HIGH")
        
        assert metadata["sender"] == "Sender"
        assert metadata["recipient"] == "Recipient"
        assert metadata["priority"] == "HIGH"
        assert "timestamp" in metadata
        assert metadata["source"] == "discord_commander"

    def test_create_message_metadata_default_priority(self, engine):
        """Test message metadata creation with default priority."""
        metadata = engine.create_message_metadata("Sender", "Recipient")
        
        assert metadata["priority"] == "NORMAL"

    @pytest.mark.asyncio
    async def test_send_to_agent_inbox_no_files_found(self, engine):
        """Test message sending when no files found in inbox."""
        with patch('src.discord_commander.discord_agent_communication.create_inbox_message', return_value=True), \
             patch('pathlib.Path.glob', return_value=[]):
            
            result = await engine.send_to_agent_inbox("Agent-7", "Test message", "TestSender")
            
            assert result.success is True
            assert result.data is not None
            assert result.data.get("filename") == "unknown"

    @pytest.mark.asyncio
    async def test_cleanup_old_messages_with_non_md_files(self, engine):
        """Test cleanup when inbox contains non-.md files."""
        with patch('os.listdir', return_value=["INBOX_MESSAGE_old.md", "other_file.txt", "README.md"]), \
             patch('os.path.getmtime', side_effect=[1000000000, 2000000000, 2000000000]), \
             patch('os.remove') as mock_remove, \
             patch.object(engine._utility.path, 'exists', return_value=True), \
             patch('datetime.datetime') as mock_datetime:
            
            mock_datetime.utcnow.return_value.timestamp.return_value = 2000000000
            
            result = await engine.cleanup_old_messages("Agent-7", max_age_hours=1)
            
            # Should only remove .md files
            assert mock_remove.call_count == 1  # Only INBOX_MESSAGE_old.md

    @pytest.mark.asyncio
    async def test_cleanup_old_messages_keeps_recent_files(self, engine):
        """Test cleanup keeps files that are not old enough."""
        current_time = 2000000000
        recent_time = current_time - 1800  # 30 minutes ago (less than 1 hour)
        
        with patch('os.listdir', return_value=["INBOX_MESSAGE_recent.md"]), \
             patch('os.path.getmtime', return_value=recent_time), \
             patch('os.remove') as mock_remove, \
             patch.object(engine._utility.path, 'exists', return_value=True), \
             patch('datetime.datetime') as mock_datetime:
            
            mock_datetime.utcnow.return_value.timestamp.return_value = current_time
            
            result = await engine.cleanup_old_messages("Agent-7", max_age_hours=1)
            
            # Should not remove recent files
            assert mock_remove.call_count == 0
            assert result == 0

    @pytest.mark.asyncio
    async def test_cleanup_old_messages_removes_old_files(self, engine):
        """Test cleanup removes files older than max_age_hours."""
        current_time = 2000000000
        old_time = current_time - 7200  # 2 hours ago (more than 1 hour)
        
        with patch('os.listdir', return_value=["INBOX_MESSAGE_old.md"]), \
             patch('os.path.getmtime', return_value=old_time), \
             patch('os.remove') as mock_remove, \
             patch.object(engine._utility.path, 'exists', return_value=True), \
             patch('datetime.datetime') as mock_datetime:
            
            mock_datetime.utcnow.return_value.timestamp.return_value = current_time
            
            result = await engine.cleanup_old_messages("Agent-7", max_age_hours=1)
            
            # Should remove old files
            assert mock_remove.call_count == 1
            assert result == 1

    @pytest.mark.asyncio
    async def test_cleanup_old_messages_file_removal_exception(self, engine):
        """Test cleanup handles file removal exceptions."""
        with patch('os.listdir', return_value=["INBOX_MESSAGE_old.md"]), \
             patch('os.path.getmtime', return_value=1000000000), \
             patch('os.remove', side_effect=PermissionError("Permission denied")), \
             patch.object(engine._utility.path, 'exists', return_value=True), \
             patch('datetime.datetime') as mock_datetime:
            
            mock_datetime.utcnow.return_value.timestamp.return_value = 2000000000
            
            # Should handle exception gracefully
            result = await engine.cleanup_old_messages("Agent-7", max_age_hours=1)
            
            # Should return 0 on exception
            assert result == 0

    def test_validate_agent_name_edge_cases(self, engine):
        """Test agent name validation with edge cases."""
        # Valid cases
        assert engine.validate_agent_name("Agent-1") is True
        assert engine.validate_agent_name("Agent-8") is True
        assert engine.validate_agent_name("Agent-10") is False  # Only 1-8 valid
        
        # Invalid cases
        assert engine.validate_agent_name("") is False
        assert engine.validate_agent_name(None) is False
        assert engine.validate_agent_name("Agent") is False
        assert engine.validate_agent_name("Agent-") is False
        assert engine.validate_agent_name("agent-1") is False  # Case sensitive
        assert engine.validate_agent_name("Agent-0") is False
        assert engine.validate_agent_name("Invalid-Name") is False

    def test_is_valid_agent_all_agents(self, engine):
        """Test validation for all valid agent IDs."""
        for i in range(1, 9):
            assert engine.is_valid_agent(f"Agent-{i}") is True
        
        # Invalid agents
        assert engine.is_valid_agent("Agent-0") is False
        assert engine.is_valid_agent("Agent-9") is False
        assert engine.is_valid_agent("agent-1") is False  # Case sensitive

    @pytest.mark.asyncio
    async def test_broadcast_to_all_agents_all_fail(self, engine):
        """Test broadcast when all agents fail."""
        with patch.object(engine, 'send_to_agent_inbox') as mock_send:
            mock_send.side_effect = [
                CommandResult(success=False, message="Failed") for _ in range(8)
            ]
            
            result = await engine.broadcast_to_all_agents("Test broadcast", "TestSender")
            
            assert result.success is False
            assert result.data["successful_deliveries"] == 0
            assert len(result.data["failed_deliveries"]) == 8

    @pytest.mark.asyncio
    async def test_read_agent_status_json_decode_error(self, engine):
        """Test status reading with invalid JSON."""
        with patch.object(engine._utility.path, 'exists', return_value=True), \
             patch('builtins.open', mock_open(read_data="invalid json")):
            result = await engine.read_agent_status("Agent-7")
            
            # Should handle JSON decode error gracefully
            assert result is None

    @pytest.mark.asyncio
    async def test_execute_agent_command_timing(self, engine):
        """Test command execution timing measurement."""
        with patch('asyncio.sleep') as mock_sleep, \
             patch('asyncio.get_event_loop') as mock_loop:
            
            # Mock time progression
            mock_loop.return_value.time.side_effect = [0.0, 1.5]
            
            result = await engine.execute_agent_command("Agent-7", "test_command")
            
            assert result.success is True
            assert result.execution_time is not None
            assert result.execution_time > 0


class TestFactoryFunction:
    """Test factory function."""

    def test_create_agent_communication_engine(self):
        """Test factory function."""
        with patch('src.discord_commander.discord_agent_communication.get_unified_utility'):
            engine = create_agent_communication_engine()
            
            assert engine is not None
            assert isinstance(engine, AgentCommunicationEngine)
