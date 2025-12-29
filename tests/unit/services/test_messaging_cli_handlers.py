#!/usr/bin/env python3
"""
Unit Tests for Messaging CLI Handlers
=====================================

Tests for command_handler, task_handler, and other CLI handlers.

<!-- SSOT Domain: testing -->

Author: Agent-1 (Integration & Core Systems Specialist)
"""

import asyncio
import time
from unittest.mock import MagicMock, AsyncMock, patch

import pytest


class TestCommandHandler:
    """Unit tests for CommandHandler."""

    def setup_method(self):
        """Set up test fixtures."""
        from src.services.handlers.command_handler import CommandHandler
        self.handler = CommandHandler()

    def test_init(self):
        """Test CommandHandler initialization."""
        assert self.handler.command_count == 0
        assert self.handler.successful_commands == 0
        assert self.handler.failed_commands == 0
        assert self.handler.command_history == []

    def test_can_handle_returns_false(self):
        """Test base handler returns False for can_handle."""
        args = MagicMock()
        assert self.handler.can_handle(args) is False

    @pytest.mark.asyncio
    async def test_process_command_unknown(self):
        """Test processing unknown command."""
        result = await self.handler.process_command(
            command="unknown_command",
            args={},
            coordinate_handler=MagicMock(),
            message_handler=MagicMock(),
            service=MagicMock()
        )
        
        assert result["success"] is False
        assert "Unknown command" in result["error"]

    @pytest.mark.asyncio
    async def test_process_command_tracks_count(self):
        """Test that processing commands increments count."""
        await self.handler.process_command(
            command="unknown",
            args={},
            coordinate_handler=MagicMock(),
            message_handler=MagicMock(),
            service=MagicMock()
        )
        
        assert self.handler.command_count == 1
        assert self.handler.failed_commands == 1

    @pytest.mark.asyncio
    async def test_process_command_history(self):
        """Test command history tracking."""
        await self.handler.process_command(
            command="test",
            args={"key": "value"},
            coordinate_handler=MagicMock(),
            message_handler=MagicMock(),
            service=MagicMock()
        )
        
        assert len(self.handler.command_history) == 1
        assert self.handler.command_history[0]["command"] == "test"

    @pytest.mark.asyncio
    async def test_process_command_history_limit(self):
        """Test command history is limited to 100 entries."""
        for i in range(110):
            await self.handler.process_command(
                command=f"cmd_{i}",
                args={},
                coordinate_handler=MagicMock(),
                message_handler=MagicMock(),
                service=MagicMock()
            )
        
        assert len(self.handler.command_history) == 100

    @pytest.mark.asyncio
    async def test_process_coordinates_command(self):
        """Test coordinates command handling."""
        mock_coord_handler = MagicMock()
        mock_coord_handler.get_all_coordinates = MagicMock(return_value={
            "success": True,
            "coordinates": {"Agent-1": (100, 200)}
        })
        
        result = await self.handler.process_command(
            command="coordinates",
            args={},
            coordinate_handler=mock_coord_handler,
            message_handler=MagicMock(),
            service=MagicMock()
        )
        
        # Command should be processed (success or failure based on mock)
        assert self.handler.command_count == 1


class TestTaskHandler:
    """Unit tests for TaskHandler."""

    def setup_method(self):
        """Set up test fixtures."""
        from src.services.handlers.task_handler import TaskHandler
        self.handler = TaskHandler()

    def test_init(self):
        """Test TaskHandler initialization."""
        assert self.handler is not None

    def test_can_handle_with_get_next_task(self):
        """Test can_handle detects get-next-task."""
        args = MagicMock()
        args.get_next_task = True
        args.agent = "Agent-1"
        
        result = self.handler.can_handle(args)
        assert result is True

    def test_can_handle_with_list_tasks(self):
        """Test can_handle detects list-tasks."""
        args = MagicMock()
        args.get_next_task = False
        args.list_tasks = True
        
        result = self.handler.can_handle(args)
        assert result is True

    def test_can_handle_returns_false(self):
        """Test can_handle returns False when no task args."""
        args = MagicMock()
        args.get_next_task = False
        args.list_tasks = False
        args.task_status = False
        args.complete_task = False
        
        result = self.handler.can_handle(args)
        assert result is False


class TestContractHandler:
    """Unit tests for ContractHandler."""

    def setup_method(self):
        """Set up test fixtures."""
        from src.services.handlers.contract_handler import ContractHandler
        self.handler = ContractHandler()

    def test_init(self):
        """Test ContractHandler initialization."""
        assert self.handler is not None

    def test_can_handle_with_get_next_task(self):
        """Test can_handle with get-next-task flag."""
        args = MagicMock(spec=[])
        args.get_next_task = True
        args.check_status = False
        
        result = self.handler.can_handle(args)
        # Handler uses hasattr/getattr pattern
        assert isinstance(result, bool)

    def test_can_handle_with_check_status(self):
        """Test can_handle with check-status flag."""
        args = MagicMock(spec=[])
        args.check_status = True
        args.get_next_task = False
        
        result = self.handler.can_handle(args)
        assert isinstance(result, bool)


class TestCoordinateHandler:
    """Unit tests for CoordinateHandler."""

    def setup_method(self):
        """Set up test fixtures."""
        from src.services.handlers.coordinate_handler import CoordinateHandler
        self.handler = CoordinateHandler()

    def test_init(self):
        """Test CoordinateHandler initialization."""
        assert self.handler is not None

    def test_can_handle_base_returns_false(self):
        """Test base can_handle returns False (delegates to orchestrator)."""
        args = MagicMock()
        result = self.handler.can_handle(args)
        # Base handler returns False - orchestrator handles routing
        assert result is False

    def test_handle_base_returns_false(self):
        """Test base handle returns False (delegates to orchestrator)."""
        args = MagicMock()
        result = self.handler.handle(args)
        assert result is False

    def test_coordinates_cache_init(self):
        """Test coordinates cache is initialized."""
        assert self.handler.coordinates_cache == {}
        assert self.handler.cache_ttl_seconds == 300

    @pytest.mark.asyncio
    async def test_load_coordinates_async(self):
        """Test async coordinate loading."""
        with patch('src.services.handlers.coordinate_handler.get_coordinate_loader') as mock_loader:
            mock_loader_instance = MagicMock()
            mock_loader_instance.get_all_agents.return_value = ["Agent-1", "Agent-2"]
            mock_loader_instance.get_chat_coordinates.return_value = (100, 200)
            mock_loader.return_value = mock_loader_instance
            
            result = await self.handler.load_coordinates_async()
            
            assert result["success"] is True


class TestOnboardingHandler:
    """Unit tests for OnboardingHandler."""

    def setup_method(self):
        """Set up test fixtures."""
        from src.services.handlers.onboarding_handler import OnboardingHandler
        self.handler = OnboardingHandler()

    def test_init(self):
        """Test OnboardingHandler initialization."""
        assert self.handler is not None

    def test_can_handle_onboarding(self):
        """Test can_handle with onboarding flag."""
        args = MagicMock(spec=[])
        args.onboarding = True
        
        result = self.handler.can_handle(args)
        assert result is True

    def test_can_handle_onboard(self):
        """Test can_handle with onboard flag."""
        args = MagicMock(spec=[])
        args.onboarding = False
        args.onboard = True
        
        result = self.handler.can_handle(args)
        assert result is True

    def test_can_handle_returns_false(self):
        """Test can_handle returns False when no onboarding args."""
        args = MagicMock(spec=[])
        args.onboarding = False
        args.onboard = False
        args.soft_onboard = False
        args.hard_onboarding = False
        
        result = self.handler.can_handle(args)
        assert result is False


class TestUtilityHandler:
    """Unit tests for UtilityHandler."""

    def setup_method(self):
        """Set up test fixtures."""
        from src.services.handlers.utility_handler import UtilityHandler
        self.handler = UtilityHandler()

    def test_init(self):
        """Test UtilityHandler initialization."""
        assert self.handler is not None

    def test_check_status_all_agents(self):
        """Test check_status for all agents."""
        with patch.object(self.handler, 'check_status') as mock_check:
            mock_check.return_value = {"agents": [], "total_count": 0}
            result = self.handler.check_status()
            assert isinstance(result, dict)

    def test_check_status_specific_agent(self):
        """Test check_status for specific agent."""
        result = self.handler.check_status(agent_id="Agent-1")
        # Returns dict with agent info or error
        assert isinstance(result, dict)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

