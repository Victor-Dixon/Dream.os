"""
Tests for bulk_coordinator.py

Comprehensive tests for bulk message coordination, grouping, and batch operations.
Target: 10+ test methods, ≥85% coverage
"""

import pytest
from unittest.mock import MagicMock, patch
from src.services.coordination.bulk_coordinator import BulkCoordinator
from src.core.messaging_models_core import (
    UnifiedMessage,
    UnifiedMessageType,
    UnifiedMessagePriority,
    SenderType,
)


class TestBulkCoordinator:
    """Tests for BulkCoordinator."""

    def test_initialization(self):
        """Test coordinator initialization."""
        coordinator = BulkCoordinator()
        assert coordinator.strategy_coordinator is not None

    def test_coordinate_bulk_messages_empty_list(self):
        """Test coordinating empty message list."""
        coordinator = BulkCoordinator()
        result = coordinator.coordinate_bulk_messages([])
        
        assert result["success"] is True
        assert result["total_messages"] == 0
        assert result["successful"] == 0
        assert result["failed"] == 0
        assert result["execution_time"] >= 0
        assert result["results"] == []
        assert result["grouped_by_strategy"] == 0

    def test_coordinate_bulk_messages_single_message(self):
        """Test coordinating single message."""
        coordinator = BulkCoordinator()
        message = UnifiedMessage(
            content="test",
            sender="Agent-1",
            recipient="Agent-6",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR,
            sender_type=SenderType.AGENT,
        )
        result = coordinator.coordinate_bulk_messages([message])
        
        assert result["success"] is True
        assert result["total_messages"] == 1
        assert result["successful"] == 1
        assert result["failed"] == 0
        assert len(result["results"]) == 1
        assert result["results"][0]["success"] is True

    def test_coordinate_bulk_messages_multiple_messages(self):
        """Test coordinating multiple messages."""
        coordinator = BulkCoordinator()
        messages = [
            UnifiedMessage(
                content=f"test {i}",
                sender="Agent-1",
                recipient="Agent-6",
                message_type=UnifiedMessageType.TEXT,
                priority=UnifiedMessagePriority.REGULAR,
                sender_type=SenderType.AGENT,
            )
            for i in range(5)
        ]
        result = coordinator.coordinate_bulk_messages(messages)
        
        assert result["success"] is True
        assert result["total_messages"] == 5
        assert result["successful"] == 5
        assert result["failed"] == 0
        assert len(result["results"]) == 5

    def test_coordinate_bulk_messages_with_exception(self):
        """Test coordinating messages when exception occurs."""
        coordinator = BulkCoordinator()
        message = UnifiedMessage(
            content="test",
            sender="Agent-1",
            recipient="Agent-6",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR,
            sender_type=SenderType.AGENT,
        )
        
        # Patch the strategy coordinator to raise exception during coordination
        with patch.object(
            coordinator.strategy_coordinator,
            'apply_coordination_rules',
            side_effect=Exception("Test error")
        ):
            result = coordinator.coordinate_bulk_messages([message])
            
            assert result["success"] is True  # Bulk operation succeeds
            assert result["total_messages"] == 1
            assert result["successful"] == 0
            assert result["failed"] == 1
            assert result["results"][0]["success"] is False
            assert "error" in result["results"][0]

    def test_group_messages_by_strategy(self):
        """Test grouping messages by strategy."""
        coordinator = BulkCoordinator()
        messages = [
            UnifiedMessage(
                content="urgent",
                sender="Agent-1",
                recipient="Agent-6",
                message_type=UnifiedMessageType.TEXT,
                priority=UnifiedMessagePriority.URGENT,
                sender_type=SenderType.AGENT,
            ),
            UnifiedMessage(
                content="regular",
                sender="Agent-1",
                recipient="Agent-6",
                message_type=UnifiedMessageType.TEXT,
                priority=UnifiedMessagePriority.REGULAR,
                sender_type=SenderType.AGENT,
            ),
        ]
        grouped = coordinator._group_messages_by_strategy(messages)
        
        assert isinstance(grouped, dict)
        assert len(grouped) > 0
        # All messages should be in groups
        total_grouped = sum(len(group) for group in grouped.values())
        assert total_grouped == 2

    def test_coordinate_messages_by_priority(self):
        """Test coordinating messages grouped by priority."""
        coordinator = BulkCoordinator()
        messages = [
            UnifiedMessage(
                content="urgent",
                sender="Agent-1",
                recipient="Agent-6",
                message_type=UnifiedMessageType.TEXT,
                priority=UnifiedMessagePriority.URGENT,
                sender_type=SenderType.AGENT,
            ),
            UnifiedMessage(
                content="regular",
                sender="Agent-1",
                recipient="Agent-6",
                message_type=UnifiedMessageType.TEXT,
                priority=UnifiedMessagePriority.REGULAR,
                sender_type=SenderType.AGENT,
            ),
        ]
        result = coordinator.coordinate_messages_by_priority(messages)
        
        assert result["success"] is True
        assert result["total_messages"] == 2
        assert "priority_groups" in result
        assert "urgent" in result["priority_groups"]
        assert "regular" in result["priority_groups"]

    def test_coordinate_messages_by_priority_empty_groups(self):
        """Test coordinating messages by priority with empty groups."""
        coordinator = BulkCoordinator()
        messages = [
            UnifiedMessage(
                content="urgent",
                sender="Agent-1",
                recipient="Agent-6",
                message_type=UnifiedMessageType.TEXT,
                priority=UnifiedMessagePriority.URGENT,
                sender_type=SenderType.AGENT,
            ),
        ]
        result = coordinator.coordinate_messages_by_priority(messages)
        
        assert result["success"] is True
        assert result["total_messages"] == 1
        assert "urgent" in result["priority_groups"]

    def test_coordinate_messages_by_type(self):
        """Test coordinating messages grouped by type."""
        coordinator = BulkCoordinator()
        messages = [
            UnifiedMessage(
                content="broadcast",
                sender="Agent-1",
                recipient="all",
                message_type=UnifiedMessageType.BROADCAST,
                priority=UnifiedMessagePriority.REGULAR,
                sender_type=SenderType.AGENT,
            ),
            UnifiedMessage(
                content="text",
                sender="Agent-1",
                recipient="Agent-6",
                message_type=UnifiedMessageType.TEXT,
                priority=UnifiedMessagePriority.REGULAR,
                sender_type=SenderType.AGENT,
            ),
        ]
        result = coordinator.coordinate_messages_by_type(messages)
        
        assert result["success"] is True
        assert result["total_messages"] == 2
        assert "type_groups" in result
        assert "broadcast" in result["type_groups"]
        assert "text" in result["type_groups"]

    def test_coordinate_messages_by_type_empty_list(self):
        """Test coordinating messages by type with empty list."""
        coordinator = BulkCoordinator()
        result = coordinator.coordinate_messages_by_type([])
        
        assert result["success"] is True
        assert result["total_messages"] == 0
        assert "type_groups" in result

    def test_coordinate_messages_by_sender(self):
        """Test coordinating messages grouped by sender type."""
        coordinator = BulkCoordinator()
        messages = [
            UnifiedMessage(
                content="captain",
                sender="Captain Agent-4",
                recipient="Agent-6",
                message_type=UnifiedMessageType.TEXT,
                priority=UnifiedMessagePriority.REGULAR,
                sender_type=SenderType.CAPTAIN,
            ),
            UnifiedMessage(
                content="agent",
                sender="Agent-1",
                recipient="Agent-6",
                message_type=UnifiedMessageType.TEXT,
                priority=UnifiedMessagePriority.REGULAR,
                sender_type=SenderType.AGENT,
            ),
        ]
        result = coordinator.coordinate_messages_by_sender(messages)
        
        assert result["success"] is True
        assert result["total_messages"] == 2
        assert "sender_groups" in result
        assert "captain" in result["sender_groups"]
        assert "agent" in result["sender_groups"]

    def test_coordinate_messages_by_sender_empty_list(self):
        """Test coordinating messages by sender with empty list."""
        coordinator = BulkCoordinator()
        result = coordinator.coordinate_messages_by_sender([])
        
        assert result["success"] is True
        assert result["total_messages"] == 0
        assert "sender_groups" in result

    def test_get_bulk_coordinator_status(self):
        """Test getting bulk coordinator status."""
        coordinator = BulkCoordinator()
        status = coordinator.get_bulk_coordinator_status()
        
        assert "strategy_coordinator_status" in status
        assert "available_grouping_methods" in status
        assert isinstance(status["available_grouping_methods"], list)
        assert "strategy" in status["available_grouping_methods"]
        assert "priority" in status["available_grouping_methods"]
        assert "type" in status["available_grouping_methods"]
        assert "sender" in status["available_grouping_methods"]

    def test_coordinate_single_message_success(self):
        """Test coordinating a single message successfully."""
        coordinator = BulkCoordinator()
        message = UnifiedMessage(
            content="test",
            sender="Agent-1",
            recipient="Agent-6",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR,
            sender_type=SenderType.AGENT,
        )
        result = coordinator._coordinate_single_message(message)
        
        assert result["success"] is True
        assert "strategy" in result
        assert "coordination_result" in result
        assert result["message_id"] == message.message_id
        assert result["recipient"] == message.recipient

    def test_coordinate_single_message_failure(self):
        """Test coordinating a single message with failure."""
        coordinator = BulkCoordinator()
        message = UnifiedMessage(
            content="test",
            sender="Agent-1",
            recipient="Agent-6",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR,
            sender_type=SenderType.AGENT,
        )
        
        with patch.object(
            coordinator.strategy_coordinator,
            'determine_coordination_strategy',
            side_effect=Exception("Test error")
        ):
            result = coordinator._coordinate_single_message(message)
            
            assert result["success"] is False
            assert "error" in result
            assert result["message_id"] == message.message_id

