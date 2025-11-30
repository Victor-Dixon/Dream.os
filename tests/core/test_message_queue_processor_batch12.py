"""
Batch 12: Expanded tests for message_queue_processor.py
Focus: Integration tests, queue persistence, messaging_core integration
Target: ≥85% coverage, 15+ tests
"""

import pytest
from unittest.mock import Mock, MagicMock, patch, call
from datetime import datetime
import sys
import uuid
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.message_queue_processor import MessageQueueProcessor
from src.core.message_queue import MessageQueue, QueueConfig
from src.core.message_queue_persistence import QueueEntry
from src.core.messaging_models_core import (
    UnifiedMessageType,
    UnifiedMessagePriority,
    UnifiedMessageTag
)


class TestMessageQueueProcessorBatch12:
    """Batch 12: Expanded integration tests for MessageQueueProcessor."""

    @pytest.fixture
    def mock_queue(self):
        """Create mock message queue."""
        mock = MagicMock(spec=MessageQueue)
        mock.dequeue.return_value = []
        mock.mark_delivered.return_value = True
        mock.mark_failed.return_value = True
        return mock

    @pytest.fixture
    def mock_messaging_core(self):
        """Create mock messaging core for dependency injection."""
        mock = MagicMock()
        mock.send_message.return_value = True
        return mock

    @pytest.fixture
    def processor_with_mock_core(self, mock_queue, mock_messaging_core):
        """Create processor with injected mock messaging core."""
        return MessageQueueProcessor(
            queue=mock_queue,
            messaging_core=mock_messaging_core
        )

    def test_deliver_via_core_with_injected_mock(self, processor_with_mock_core, mock_messaging_core):
        """Test delivery via injected messaging core (no keyboard control)."""
        result = processor_with_mock_core._deliver_via_core(
            "Agent-1", "test content", {}, "text", "SYSTEM", "regular", ["system"]
        )
        
        assert result is True
        mock_messaging_core.send_message.assert_called_once()
        call_args = mock_messaging_core.send_message.call_args
        assert call_args.kwargs["content"] == "test content"
        assert call_args.kwargs["recipient"] == "Agent-1"

    def test_deliver_via_core_message_type_parsing(self, processor_with_mock_core):
        """Test message type string parsing to enum."""
        # Test various message type strings
        test_cases = [
            ("captain_to_agent", UnifiedMessageType.CAPTAIN_TO_AGENT),
            ("agent_to_agent", UnifiedMessageType.AGENT_TO_AGENT),
            ("agent_to_captain", UnifiedMessageType.AGENT_TO_AGENT),  # Fixed: Maps to AGENT_TO_AGENT (not separate type)
            ("system_to_agent", UnifiedMessageType.SYSTEM_TO_AGENT),
            ("text", UnifiedMessageType.TEXT),
            ("broadcast", UnifiedMessageType.BROADCAST),
        ]
        
        for type_str, expected_type in test_cases:
            processor_with_mock_core._deliver_via_core(
                "Agent-1", "test", {}, type_str, "SYSTEM", "regular", []
            )
            call_args = processor_with_mock_core.messaging_core.send_message.call_args
            assert call_args.kwargs["message_type"] == expected_type

    def test_deliver_via_core_priority_parsing(self, processor_with_mock_core):
        """Test priority string parsing."""
        # Test regular priority
        processor_with_mock_core._deliver_via_core(
            "Agent-1", "test", {}, None, "SYSTEM", "regular", []
        )
        call_args = processor_with_mock_core.messaging_core.send_message.call_args
        assert call_args.kwargs["priority"] == UnifiedMessagePriority.REGULAR
        
        # Test urgent priority
        processor_with_mock_core._deliver_via_core(
            "Agent-1", "test", {}, None, "SYSTEM", "urgent", []
        )
        call_args = processor_with_mock_core.messaging_core.send_message.call_args
        assert call_args.kwargs["priority"] == UnifiedMessagePriority.URGENT

    def test_deliver_via_core_tags_parsing(self, processor_with_mock_core):
        """Test tags list parsing."""
        # Test with tags
        processor_with_mock_core._deliver_via_core(
            "Agent-1", "test", {}, None, "SYSTEM", "regular", ["system", "captain"]
        )
        call_args = processor_with_mock_core.messaging_core.send_message.call_args
        assert len(call_args.kwargs["tags"]) == 2
        assert UnifiedMessageTag.SYSTEM in call_args.kwargs["tags"]
        assert UnifiedMessageTag.CAPTAIN in call_args.kwargs["tags"]
        
        # Test default tags when empty
        processor_with_mock_core._deliver_via_core(
            "Agent-1", "test", {}, None, "SYSTEM", "regular", []
        )
        call_args = processor_with_mock_core.messaging_core.send_message.call_args
        assert len(call_args.kwargs["tags"]) == 1
        assert UnifiedMessageTag.SYSTEM in call_args.kwargs["tags"]

    def test_deliver_via_core_invalid_message_type_fallback(self, processor_with_mock_core):
        """Test fallback to SYSTEM_TO_AGENT for invalid message type."""
        processor_with_mock_core._deliver_via_core(
            "Agent-1", "test", {}, "invalid_type", "SYSTEM", "regular", []
        )
        call_args = processor_with_mock_core.messaging_core.send_message.call_args
        assert call_args.kwargs["message_type"] == UnifiedMessageType.SYSTEM_TO_AGENT

    def test_deliver_via_core_invalid_priority_fallback(self, processor_with_mock_core):
        """Test fallback to REGULAR for invalid priority."""
        processor_with_mock_core._deliver_via_core(
            "Agent-1", "test", {}, None, "SYSTEM", "invalid_priority", []
        )
        call_args = processor_with_mock_core.messaging_core.send_message.call_args
        assert call_args.kwargs["priority"] == UnifiedMessagePriority.REGULAR

    def test_route_delivery_queue_full_skip_pygui(self, processor_with_mock_core):
        """Test routing skips PyAutoGUI when queue is full."""
        with patch('src.utils.agent_queue_status.AgentQueueStatus') as mock_status_class:
            mock_status = MagicMock()
            mock_status.is_queue_full.return_value = True
            mock_status_class.return_value = mock_status
            
            with patch.object(processor_with_mock_core, '_deliver_fallback_inbox', return_value=True):
                result = processor_with_mock_core._route_delivery("Agent-1", "test", {})
                
                assert result is True
                processor_with_mock_core._deliver_fallback_inbox.assert_called_once()
                # Should not call messaging core when queue is full
                assert processor_with_mock_core.messaging_core.send_message.call_count == 0

    def test_route_delivery_queue_status_import_error(self, processor_with_mock_core):
        """Test routing continues normally when queue status import fails."""
        with patch('src.utils.agent_queue_status.AgentQueueStatus', side_effect=ImportError()):
            processor_with_mock_core._deliver_via_core = MagicMock(return_value=True)
            
            result = processor_with_mock_core._route_delivery("Agent-1", "test", {})
            
            assert result is True
            processor_with_mock_core._deliver_via_core.assert_called_once()

    def test_route_delivery_exception_fallback(self, processor_with_mock_core):
        """Test routing falls back to inbox on exception."""
        processor_with_mock_core._deliver_via_core = MagicMock(side_effect=Exception("Test error"))
        
        with patch.object(processor_with_mock_core, '_deliver_fallback_inbox', return_value=True):
            result = processor_with_mock_core._route_delivery("Agent-1", "test", {})
            
            assert result is True
            processor_with_mock_core._deliver_fallback_inbox.assert_called_once()

    def test_route_delivery_fallback_also_fails(self, processor_with_mock_core):
        """Test routing returns False when both core and fallback fail."""
        processor_with_mock_core._deliver_via_core = MagicMock(return_value=False)
        processor_with_mock_core._deliver_fallback_inbox = MagicMock(return_value=False)
        
        result = processor_with_mock_core._route_delivery("Agent-1", "test", {})
        
        assert result is False

    def test_deliver_entry_with_message_type_preservation(self, processor_with_mock_core, mock_queue):
        """Test entry delivery preserves message_type from queue entry."""
        now = datetime.now()
        entry = QueueEntry(
            message={
                "content": "test",
                "recipient": "Agent-1",
                "sender": "SYSTEM",
                "message_type": "captain_to_agent",
                "priority": "urgent",
                "tags": ["system", "captain"]
            },
            queue_id="test-id",
            priority_score=0.9,
            status="PENDING",
            created_at=now,
            updated_at=now
        )
        
        processor_with_mock_core._route_delivery = MagicMock(return_value=True)
        result = processor_with_mock_core._deliver_entry(entry)
        
        assert result is True
        call_args = processor_with_mock_core._route_delivery.call_args
        # _route_delivery is called with positional args: (recipient, content, metadata, message_type_str, sender, priority_str, tags_list)
        assert call_args[0][0] == "Agent-1"  # recipient
        assert call_args[0][1] == "test"  # content
        assert call_args[0][2] == {}  # metadata (empty dict)
        assert call_args[0][3] == "captain_to_agent"  # message_type_str
        assert call_args[0][4] == "SYSTEM"  # sender
        assert call_args[0][5] == "urgent"  # priority_str
        assert call_args[0][6] == ["system", "captain"]  # tags_list

    def test_deliver_entry_with_metadata(self, processor_with_mock_core, mock_queue):
        """Test entry delivery includes metadata."""
        now = datetime.now()
        entry = QueueEntry(
            message={
                "content": "test",
                "recipient": "Agent-1",
                "sender": "SYSTEM",
                "metadata": {"key": "value", "timestamp": "2025-01-01"}
            },
            queue_id="test-id",
            priority_score=0.8,
            status="PENDING",
            created_at=now,
            updated_at=now
        )
        
        processor_with_mock_core._route_delivery = MagicMock(return_value=True)
        result = processor_with_mock_core._deliver_entry(entry)
        
        assert result is True
        call_args = processor_with_mock_core._route_delivery.call_args
        # _route_delivery is called with positional args: (recipient, content, metadata, message_type_str, sender, priority_str, tags_list)
        assert call_args[0][2] == {"key": "value", "timestamp": "2025-01-01"}  # metadata (3rd positional arg)

    def test_process_queue_batch_processing(self, processor_with_mock_core, mock_queue):
        """Test batch processing of multiple entries."""
        now = datetime.now()
        entries = [
            QueueEntry(
                message={"content": f"test{i}", "recipient": f"Agent-{i}", "sender": "SYSTEM"},
                queue_id=f"id-{i}",
                priority_score=0.8,
                status="PENDING",
                created_at=now,
                updated_at=now
            )
            for i in range(1, 4)
        ]
        
        mock_queue.dequeue.return_value = entries
        processor_with_mock_core._deliver_entry = MagicMock(return_value=True)
        
        result = processor_with_mock_core.process_queue(max_messages=3, batch_size=3)
        
        assert result == 3
        assert processor_with_mock_core._deliver_entry.call_count == 3

    def test_process_queue_respects_max_messages(self, processor_with_mock_core, mock_queue):
        """Test processing respects max_messages limit."""
        now = datetime.now()
        entries = [
            QueueEntry(
                message={"content": f"test{i}", "recipient": f"Agent-{i}", "sender": "SYSTEM"},
                queue_id=f"id-{i}",
                priority_score=0.8,
                status="PENDING",
                created_at=now,
                updated_at=now
            )
            for i in range(1, 6)
        ]
        
        mock_queue.dequeue.return_value = entries
        processor_with_mock_core._deliver_entry = MagicMock(return_value=True)
        
        result = processor_with_mock_core.process_queue(max_messages=2, batch_size=5)
        
        assert result == 2
        assert processor_with_mock_core._deliver_entry.call_count == 2

    def test_deliver_fallback_inbox_metadata_extraction(self, processor_with_mock_core):
        """Test inbox fallback extracts sender and priority from metadata."""
        with patch('src.utils.inbox_utility.create_inbox_message', return_value=True) as mock_inbox:
            metadata = {"sender": "CAPTAIN", "priority": "urgent"}
            processor_with_mock_core._deliver_fallback_inbox("Agent-1", "test", metadata)
            
            mock_inbox.assert_called_once_with(
                recipient="Agent-1",
                content="test",
                sender="CAPTAIN",
                priority="urgent"
            )

    def test_deliver_fallback_inbox_default_metadata(self, processor_with_mock_core):
        """Test inbox fallback uses defaults when metadata missing."""
        with patch('src.utils.inbox_utility.create_inbox_message', return_value=True) as mock_inbox:
            processor_with_mock_core._deliver_fallback_inbox("Agent-1", "test", {})
            
            mock_inbox.assert_called_once_with(
                recipient="Agent-1",
                content="test",
                sender="SYSTEM",
                priority="normal"
            )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
