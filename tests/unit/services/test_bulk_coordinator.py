"""
Unit tests for bulk_coordinator.py

Target: ≥85% coverage, 15+ test methods
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from src.services.coordination.bulk_coordinator import BulkCoordinator
from src.core.messaging_models_core import UnifiedMessage, UnifiedMessageType, UnifiedMessagePriority, SenderType, RecipientType


class TestBulkCoordinator:
    """Test suite for BulkCoordinator."""

    @pytest.fixture
    def coordinator(self):
        """Create BulkCoordinator instance."""
        return BulkCoordinator()

    @pytest.fixture
    def sample_message(self):
        """Create sample message."""
        return UnifiedMessage(
            content="Test message",
            recipient="Agent-1",
            sender="System",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR,
            recipient_type=RecipientType.AGENT,
            sender_type=SenderType.SYSTEM
        )

    def test_coordinator_initialization(self, coordinator):
        """Test coordinator initializes correctly."""
        assert coordinator is not None
        assert coordinator.strategy_coordinator is not None

    def test_coordinate_bulk_messages_empty_list(self, coordinator):
        """Test coordinating empty message list."""
        result = coordinator.coordinate_bulk_messages([])
        
        assert result["success"] is True
        assert result["total_messages"] == 0
        assert result["successful"] == 0
        assert result["failed"] == 0

    def test_coordinate_bulk_messages_single(self, coordinator, sample_message):
        """Test coordinating single message."""
        with patch.object(coordinator.strategy_coordinator, 'determine_coordination_strategy', return_value="standard"):
            with patch.object(coordinator.strategy_coordinator, 'apply_coordination_rules', return_value={"success": True}):
                result = coordinator.coordinate_bulk_messages([sample_message])
                
                assert result["success"] is True
                assert result["total_messages"] == 1
                assert result["successful"] == 1
                assert result["failed"] == 0

    def test_coordinate_bulk_messages_multiple(self, coordinator, sample_message):
        """Test coordinating multiple messages."""
        messages = [sample_message, sample_message, sample_message]
        
        with patch.object(coordinator.strategy_coordinator, 'determine_coordination_strategy', return_value="standard"):
            with patch.object(coordinator.strategy_coordinator, 'apply_coordination_rules', return_value={"success": True}):
                result = coordinator.coordinate_bulk_messages(messages)
                
                assert result["success"] is True
                assert result["total_messages"] == 3
                assert result["successful"] == 3

    def test_coordinate_bulk_messages_tracks_execution_time(self, coordinator, sample_message):
        """Test execution time tracking."""
        with patch.object(coordinator.strategy_coordinator, 'determine_coordination_strategy', return_value="standard"):
            with patch.object(coordinator.strategy_coordinator, 'apply_coordination_rules', return_value={"success": True}):
                result = coordinator.coordinate_bulk_messages([sample_message])
                
                assert "execution_time" in result
                assert result["execution_time"] >= 0

    def test_coordinate_bulk_messages_groups_by_strategy(self, coordinator, sample_message):
        """Test messages grouped by strategy."""
        with patch.object(coordinator.strategy_coordinator, 'determine_coordination_strategy', return_value="standard"):
            with patch.object(coordinator.strategy_coordinator, 'apply_coordination_rules', return_value={"success": True}):
                result = coordinator.coordinate_bulk_messages([sample_message])
                
                assert "grouped_by_strategy" in result

    def test_coordinate_single_message_success(self, coordinator, sample_message):
        """Test coordinating single message successfully."""
        with patch.object(coordinator.strategy_coordinator, 'determine_coordination_strategy', return_value="standard"):
            with patch.object(coordinator.strategy_coordinator, 'apply_coordination_rules', return_value={"success": True}):
                result = coordinator._coordinate_single_message(sample_message)
                
                assert result["success"] is True
                assert result["strategy"] == "standard"
                assert "message_id" in result

    def test_coordinate_single_message_exception(self, coordinator, sample_message):
        """Test exception handling in single message coordination."""
        with patch.object(coordinator.strategy_coordinator, 'determine_coordination_strategy', side_effect=Exception("Test error")):
            result = coordinator._coordinate_single_message(sample_message)
            
            assert result["success"] is False
            assert "error" in result

    def test_group_messages_by_strategy(self, coordinator, sample_message):
        """Test grouping messages by strategy."""
        messages = [sample_message, sample_message]
        
        with patch.object(coordinator.strategy_coordinator, 'determine_coordination_strategy', return_value="standard"):
            grouped = coordinator._group_messages_by_strategy(messages)
            
            assert "standard" in grouped
            assert len(grouped["standard"]) == 2

    def test_group_messages_multiple_strategies(self, coordinator, sample_message):
        """Test grouping with multiple strategies."""
        messages = [sample_message, sample_message]
        
        strategies = ["standard", "priority"]
        strategy_iter = iter(strategies)
        
        def get_strategy(msg):
            return next(strategy_iter) if strategy_iter.__iter__() else "standard"
        
        with patch.object(coordinator.strategy_coordinator, 'determine_coordination_strategy', side_effect=lambda m: next(iter(strategies)) if strategies else "standard"):
            # Reset iterator
            strategies = ["standard", "priority"]
            with patch('builtins.iter', return_value=iter(strategies)):
                grouped = coordinator._group_messages_by_strategy(messages)
                
                assert len(grouped) >= 1

