#!/usr/bin/env python3
"""
Tests for Discord GUI Modals Base
==================================

Comprehensive tests for src/discord_commander/discord_gui_modals_base.py

Author: Agent-7 (Web Development Specialist)
Date: 2025-11-30
Target: 80%+ coverage
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch, Mock


class TestBaseMessageModal:
    """Test suite for BaseMessageModal."""

    @pytest.fixture
    def mock_discord(self):
        """Mock Discord library."""
        with patch.dict('sys.modules', {
            'discord': MagicMock(),
            'discord.ui': MagicMock(),
            'discord.ext': MagicMock()
        }):
            yield

    @pytest.fixture
    def mock_messaging_service(self):
        """Mock ConsolidatedMessagingService."""
        service = MagicMock()
        service.send_message = Mock(return_value={"success": True})
        return service

    def test_initialization_basic(self, mock_discord, mock_messaging_service):
        """Test basic modal initialization."""
        from src.discord_commander.discord_gui_modals_base import BaseMessageModal

        modal = BaseMessageModal(
            title="Test Modal",
            messaging_service=mock_messaging_service,
            include_priority=False,
            include_agent_selection=False
        )
        
        assert modal is not None
        assert modal.messaging_service == mock_messaging_service
        assert hasattr(modal, 'message_input')

    def test_initialization_with_priority(self, mock_discord, mock_messaging_service):
        """Test modal initialization with priority input."""
        from src.discord_commander.discord_gui_modals_base import BaseMessageModal

        modal = BaseMessageModal(
            title="Test Modal",
            messaging_service=mock_messaging_service,
            include_priority=True,
            include_agent_selection=False
        )
        
        assert hasattr(modal, 'priority_input')

    def test_initialization_with_agent_selection(self, mock_discord, mock_messaging_service):
        """Test modal initialization with agent selection."""
        from src.discord_commander.discord_gui_modals_base import BaseMessageModal

        modal = BaseMessageModal(
            title="Test Modal",
            messaging_service=mock_messaging_service,
            include_priority=False,
            include_agent_selection=True
        )
        
        assert hasattr(modal, 'agent_input')

    def test_get_message_preview_short(self, mock_discord, mock_messaging_service):
        """Test message preview with short message."""
        from src.discord_commander.discord_gui_modals_base import BaseMessageModal

        modal = BaseMessageModal(
            title="Test",
            messaging_service=mock_messaging_service
        )
        
        message = "Short message"
        preview = modal._get_message_preview(message)
        assert preview == message

    def test_get_message_preview_long(self, mock_discord, mock_messaging_service):
        """Test message preview with long message."""
        from src.discord_commander.discord_gui_modals_base import BaseMessageModal

        modal = BaseMessageModal(
            title="Test",
            messaging_service=mock_messaging_service
        )
        
        message = "A" * 600
        preview = modal._get_message_preview(message, max_length=500)
        assert len(preview) == 500
        assert preview.endswith("...")

    def test_send_to_agent_regular(self, mock_discord, mock_messaging_service):
        """Test sending message to agent (regular priority)."""
        from src.discord_commander.discord_gui_modals_base import BaseMessageModal

        modal = BaseMessageModal(
            title="Test",
            messaging_service=mock_messaging_service
        )
        
        result = modal._send_to_agent("Agent-1", "Test message", priority="regular")
        assert result["success"] is True
        mock_messaging_service.send_message.assert_called_once()

    def test_send_to_agent_jet_fuel(self, mock_discord, mock_messaging_service):
        """Test sending message to agent (jet fuel mode)."""
        from src.discord_commander.discord_gui_modals_base import BaseMessageModal

        modal = BaseMessageModal(
            title="Test",
            messaging_service=mock_messaging_service
        )
        
        result = modal._send_to_agent("Agent-1", "Test message", priority="regular", jet_fuel=True)
        assert result["success"] is True
        call_args = mock_messaging_service.send_message.call_args
        assert "JET FUEL MESSAGE" in call_args[1]["message"]
        assert call_args[1]["priority"] == "urgent"

    def test_broadcast_to_agents_success(self, mock_discord, mock_messaging_service):
        """Test broadcasting to multiple agents (success)."""
        from src.discord_commander.discord_gui_modals_base import BaseMessageModal

        modal = BaseMessageModal(
            title="Test",
            messaging_service=mock_messaging_service
        )
        
        agents = ["Agent-1", "Agent-2", "Agent-3"]
        success_count, errors = modal._broadcast_to_agents(agents, "Test message", priority="regular")
        
        assert success_count == 3
        assert len(errors) == 0
        assert mock_messaging_service.send_message.call_count == 3

    def test_broadcast_to_agents_with_errors(self, mock_discord, mock_messaging_service):
        """Test broadcasting to multiple agents (with errors)."""
        from src.discord_commander.discord_gui_modals_base import BaseMessageModal

        # Mock service to return errors for some agents
        def mock_send_message(agent, message, priority, use_pyautogui):
            if agent == "Agent-2":
                return {"success": False, "error": "Connection failed"}
            return {"success": True}

        mock_messaging_service.send_message = Mock(side_effect=lambda **kwargs: mock_send_message(
            kwargs.get("agent"), kwargs.get("message"), kwargs.get("priority"), kwargs.get("use_pyautogui")
        ))

        modal = BaseMessageModal(
            title="Test",
            messaging_service=mock_messaging_service
        )
        
        agents = ["Agent-1", "Agent-2", "Agent-3"]
        success_count, errors = modal._broadcast_to_agents(agents, "Test message", priority="regular")
        
        assert success_count == 2
        assert len(errors) == 1
        assert "Agent-2" in errors[0]

    def test_broadcast_to_agents_jet_fuel(self, mock_discord, mock_messaging_service):
        """Test broadcasting to multiple agents (jet fuel mode)."""
        from src.discord_commander.discord_gui_modals_base import BaseMessageModal

        modal = BaseMessageModal(
            title="Test",
            messaging_service=mock_messaging_service
        )
        
        agents = ["Agent-1", "Agent-2"]
        success_count, errors = modal._broadcast_to_agents(agents, "Test message", priority="regular", jet_fuel=True)
        
        assert success_count == 2
        # Verify jet fuel message format
        call_args_list = mock_messaging_service.send_message.call_args_list
        for call_args in call_args_list:
            assert "JET FUEL MESSAGE" in call_args[1]["message"]
            assert call_args[1]["priority"] == "urgent"

    def test_get_all_agents(self, mock_discord, mock_messaging_service):
        """Test getting list of all agents."""
        from src.discord_commander.discord_gui_modals_base import BaseMessageModal

        modal = BaseMessageModal(
            title="Test",
            messaging_service=mock_messaging_service
        )
        
        agents = modal._get_all_agents()
        assert len(agents) == 8
        assert "Agent-1" in agents
        assert "Agent-8" in agents

    def test_format_error_message(self, mock_discord, mock_messaging_service):
        """Test formatting error message list."""
        from src.discord_commander.discord_gui_modals_base import BaseMessageModal

        modal = BaseMessageModal(
            title="Test",
            messaging_service=mock_messaging_service
        )
        
        errors = ["Error 1", "Error 2", "Error 3", "Error 4", "Error 5"]
        formatted = modal._format_error_message(errors, max_errors=3)
        
        assert len(formatted.split("\n")) == 3
        assert "Error 1" in formatted
        assert "Error 5" not in formatted

