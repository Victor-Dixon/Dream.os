"""
Unit tests for batch_message_handler.py
Target: ≥85% coverage
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from src.services.handlers.batch_message_handler import BatchMessageHandler


class TestBatchMessageHandler:
    """Tests for BatchMessageHandler class."""

    def test_init(self):
        """Test handler initialization."""
        handler = BatchMessageHandler()
        assert handler.exit_code == 0

    def test_can_handle_batch_start(self):
        """Test can_handle with batch_start."""
        handler = BatchMessageHandler()
        args = Mock()
        args.batch_start = True
        args.batch_add = False
        args.batch_send = False
        args.batch_status = False
        args.batch_cancel = False
        args.batch = False
        assert handler.can_handle(args) is True

    def test_can_handle_batch_add(self):
        """Test can_handle with batch_add."""
        handler = BatchMessageHandler()
        args = Mock()
        args.batch_start = False
        args.batch_add = True
        args.batch_send = False
        args.batch_status = False
        args.batch_cancel = False
        args.batch = False
        assert handler.can_handle(args) is True

    def test_can_handle_batch_send(self):
        """Test can_handle with batch_send."""
        handler = BatchMessageHandler()
        args = Mock()
        args.batch_start = False
        args.batch_add = False
        args.batch_send = True
        args.batch_status = False
        args.batch_cancel = False
        args.batch = False
        assert handler.can_handle(args) is True

    def test_can_handle_batch_status(self):
        """Test can_handle with batch_status."""
        handler = BatchMessageHandler()
        args = Mock()
        args.batch_start = False
        args.batch_add = False
        args.batch_send = False
        args.batch_status = True
        args.batch_cancel = False
        args.batch = False
        assert handler.can_handle(args) is True

    def test_can_handle_batch_cancel(self):
        """Test can_handle with batch_cancel."""
        handler = BatchMessageHandler()
        args = Mock()
        args.batch_start = False
        args.batch_add = False
        args.batch_send = False
        args.batch_status = False
        args.batch_cancel = True
        args.batch = False
        assert handler.can_handle(args) is True

    def test_can_handle_batch(self):
        """Test can_handle with batch."""
        handler = BatchMessageHandler()
        args = Mock()
        args.batch_start = False
        args.batch_add = False
        args.batch_send = False
        args.batch_status = False
        args.batch_cancel = False
        args.batch = True
        assert handler.can_handle(args) is True

    def test_can_handle_false(self):
        """Test can_handle returns False when no batch flags."""
        handler = BatchMessageHandler()
        args = Mock()
        args.batch_start = False
        args.batch_add = False
        args.batch_send = False
        args.batch_status = False
        args.batch_cancel = False
        args.batch = False
        assert handler.can_handle(args) is False

    @patch('src.core.messaging_core.send_message')
    @patch('src.services.message_batching_service.get_batching_service')
    def test_handle_simplified_batch_success(self, mock_service, mock_send):
        """Test handle with simplified batch (success)."""
        handler = BatchMessageHandler()
        args = Mock()
        args.batch = ["Message 1", "Message 2"]
        args.agent = "Agent-1"
        args.priority = "regular"

        mock_batch_service = Mock()
        mock_batch_service.start_batch.return_value = True
        mock_batch_service.add_to_batch.return_value = True
        mock_batch_service.send_batch.return_value = (True, "Consolidated message")
        mock_service.return_value = mock_batch_service
        mock_send.return_value = True

        result = handler.handle(args)
        assert result is True
        assert handler.exit_code == 0
        mock_batch_service.start_batch.assert_called_once()
        assert mock_batch_service.add_to_batch.call_count == 2
        mock_batch_service.send_batch.assert_called_once()
        mock_send.assert_called_once()

    @patch('src.services.message_batching_service.get_batching_service')
    def test_handle_simplified_batch_no_messages(self, mock_service):
        """Test handle with simplified batch (no messages)."""
        handler = BatchMessageHandler()
        args = Mock()
        args.batch = None
        args.agent = "Agent-1"

        result = handler.handle(args)
        assert result is True
        assert handler.exit_code == 1

    @patch('src.core.messaging_core.send_message')
    @patch('src.services.message_batching_service.get_batching_service')
    def test_handle_simplified_batch_send_failure(self, mock_service, mock_send):
        """Test handle with simplified batch (send failure)."""
        handler = BatchMessageHandler()
        args = Mock()
        args.batch = ["Message 1"]
        args.agent = "Agent-1"
        args.priority = "regular"

        mock_batch_service = Mock()
        mock_batch_service.start_batch.return_value = True
        mock_batch_service.add_to_batch.return_value = True
        mock_batch_service.send_batch.return_value = (True, "Consolidated message")
        mock_service.return_value = mock_batch_service
        mock_send.return_value = False

        result = handler.handle(args)
        assert result is True
        assert handler.exit_code == 1

    @patch('src.services.message_batching_service.get_batching_service')
    def test_handle_simplified_batch_create_failure(self, mock_service):
        """Test handle with simplified batch (create failure)."""
        handler = BatchMessageHandler()
        args = Mock()
        args.batch = ["Message 1"]
        args.agent = "Agent-1"
        args.priority = "regular"

        mock_batch_service = Mock()
        mock_batch_service.start_batch.return_value = True
        mock_batch_service.add_to_batch.return_value = True
        mock_batch_service.send_batch.return_value = (False, None)
        mock_service.return_value = mock_batch_service

        result = handler.handle(args)
        assert result is True
        assert handler.exit_code == 1

    @patch('src.services.message_batching_service.get_batching_service')
    def test_handle_batch_start_success(self, mock_service):
        """Test handle with batch-start (success)."""
        handler = BatchMessageHandler()
        args = Mock()
        args.batch_start = True
        args.batch_add = False
        args.batch_send = False
        args.batch_status = False
        args.batch_cancel = False
        args.batch = False
        args.agent = "Agent-1"

        mock_batch_service = Mock()
        mock_batch_service.start_batch.return_value = True
        mock_service.return_value = mock_batch_service

        result = handler.handle(args)
        assert result is True
        assert handler.exit_code == 0
        mock_batch_service.start_batch.assert_called_once()

    @patch('src.services.message_batching_service.get_batching_service')
    def test_handle_batch_start_failure(self, mock_service):
        """Test handle with batch-start (failure)."""
        handler = BatchMessageHandler()
        args = Mock()
        args.batch_start = True
        args.batch_add = False
        args.batch_send = False
        args.batch_status = False
        args.batch_cancel = False
        args.batch = False
        args.agent = "Agent-1"

        mock_batch_service = Mock()
        mock_batch_service.start_batch.return_value = False
        mock_service.return_value = mock_batch_service

        result = handler.handle(args)
        assert result is True
        assert handler.exit_code == 1

    @patch('src.services.message_batching_service.get_batching_service')
    def test_handle_batch_add_success(self, mock_service):
        """Test handle with batch-add (success)."""
        handler = BatchMessageHandler()
        args = Mock()
        args.batch_start = False
        args.batch_add = "New message"
        args.batch_send = False
        args.batch_status = False
        args.batch_cancel = False
        args.batch = False
        args.agent = "Agent-1"

        mock_batch_service = Mock()
        mock_batch_service.add_to_batch.return_value = True
        mock_batch_service.get_batch_status.return_value = {
            "exists": True,
            "message_count": 1
        }
        mock_service.return_value = mock_batch_service

        result = handler.handle(args)
        assert result is True
        assert handler.exit_code == 0
        mock_batch_service.add_to_batch.assert_called_once()

    @patch('src.services.message_batching_service.get_batching_service')
    def test_handle_batch_add_no_message(self, mock_service):
        """Test handle with batch-add (no message)."""
        handler = BatchMessageHandler()
        args = Mock()
        args.batch_start = False
        args.batch_add = None
        args.batch_send = False
        args.batch_status = False
        args.batch_cancel = False
        args.batch = False

        result = handler.handle(args)
        assert result is True
        assert handler.exit_code == 1

    @patch('src.services.message_batching_service.get_batching_service')
    def test_handle_batch_add_failure(self, mock_service):
        """Test handle with batch-add (failure)."""
        handler = BatchMessageHandler()
        args = Mock()
        args.batch_start = False
        args.batch_add = "New message"
        args.batch_send = False
        args.batch_status = False
        args.batch_cancel = False
        args.batch = False
        args.agent = "Agent-1"

        mock_batch_service = Mock()
        mock_batch_service.add_to_batch.return_value = False
        mock_service.return_value = mock_batch_service

        result = handler.handle(args)
        assert result is True
        assert handler.exit_code == 1

    @patch('src.core.messaging_core.send_message')
    @patch('src.services.message_batching_service.get_batching_service')
    def test_handle_batch_send_success(self, mock_service, mock_send):
        """Test handle with batch-send (success)."""
        handler = BatchMessageHandler()
        args = Mock()
        args.batch_start = False
        args.batch_add = False
        args.batch_send = True
        args.batch_status = False
        args.batch_cancel = False
        args.batch = False
        args.agent = "Agent-1"
        args.priority = "regular"

        mock_batch_service = Mock()
        mock_batch_service.send_batch.return_value = (True, "Consolidated message")
        mock_service.return_value = mock_batch_service
        mock_send.return_value = True

        result = handler.handle(args)
        assert result is True
        assert handler.exit_code == 0
        mock_batch_service.send_batch.assert_called_once()
        mock_send.assert_called_once()

    @patch('src.core.messaging_core.send_message')
    @patch('src.services.message_batching_service.get_batching_service')
    def test_handle_batch_send_urgent_priority(self, mock_service, mock_send):
        """Test handle with batch-send (urgent priority)."""
        handler = BatchMessageHandler()
        args = Mock()
        args.batch_start = False
        args.batch_add = False
        args.batch_send = True
        args.batch_status = False
        args.batch_cancel = False
        args.batch = False
        args.agent = "Agent-1"
        args.priority = "urgent"

        mock_batch_service = Mock()
        mock_batch_service.send_batch.return_value = (True, "Consolidated message")
        mock_service.return_value = mock_batch_service
        mock_send.return_value = True

        result = handler.handle(args)
        assert result is True
        assert handler.exit_code == 0

    @patch('src.services.message_batching_service.get_batching_service')
    def test_handle_batch_send_failure(self, mock_service):
        """Test handle with batch-send (failure)."""
        handler = BatchMessageHandler()
        args = Mock()
        args.batch_start = False
        args.batch_add = False
        args.batch_send = True
        args.batch_status = False
        args.batch_cancel = False
        args.batch = False
        args.agent = "Agent-1"
        args.priority = "regular"

        mock_batch_service = Mock()
        mock_batch_service.send_batch.return_value = (False, None)
        mock_service.return_value = mock_batch_service

        result = handler.handle(args)
        assert result is True
        assert handler.exit_code == 1

    @patch('src.services.message_batching_service.get_batching_service')
    def test_handle_batch_status_exists(self, mock_service):
        """Test handle with batch-status (exists)."""
        handler = BatchMessageHandler()
        args = Mock()
        args.batch_start = False
        args.batch_add = False
        args.batch_send = False
        args.batch_status = True
        args.batch_cancel = False
        args.batch = False
        args.agent = "Agent-1"

        mock_batch_service = Mock()
        mock_batch_service.get_batch_status.return_value = {
            "exists": True,
            "agent_id": "Agent-1",
            "recipient": "Agent-4",
            "message_count": 3,
            "created_at": "2025-11-28"
        }
        mock_service.return_value = mock_batch_service

        result = handler.handle(args)
        assert result is True
        assert handler.exit_code == 0

    @patch('src.services.message_batching_service.get_batching_service')
    def test_handle_batch_status_not_exists(self, mock_service):
        """Test handle with batch-status (not exists)."""
        handler = BatchMessageHandler()
        args = Mock()
        args.batch_start = False
        args.batch_add = False
        args.batch_send = False
        args.batch_status = True
        args.batch_cancel = False
        args.batch = False
        args.agent = "Agent-1"

        mock_batch_service = Mock()
        mock_batch_service.get_batch_status.return_value = {
            "exists": False,
            "message": "No active batch"
        }
        mock_service.return_value = mock_batch_service

        result = handler.handle(args)
        assert result is True
        assert handler.exit_code == 0

    @patch('src.services.message_batching_service.get_batching_service')
    def test_handle_batch_cancel_success(self, mock_service):
        """Test handle with batch-cancel (success)."""
        handler = BatchMessageHandler()
        args = Mock()
        args.batch_start = False
        args.batch_add = False
        args.batch_send = False
        args.batch_status = False
        args.batch_cancel = True
        args.batch = False
        args.agent = "Agent-1"

        mock_batch_service = Mock()
        mock_batch_service.cancel_batch.return_value = True
        mock_service.return_value = mock_batch_service

        result = handler.handle(args)
        assert result is True
        assert handler.exit_code == 0
        mock_batch_service.cancel_batch.assert_called_once()

    @patch('src.services.message_batching_service.get_batching_service')
    def test_handle_batch_cancel_no_batch(self, mock_service):
        """Test handle with batch-cancel (no batch)."""
        handler = BatchMessageHandler()
        args = Mock()
        args.batch_start = False
        args.batch_add = False
        args.batch_send = False
        args.batch_status = False
        args.batch_cancel = True
        args.batch = False
        args.agent = "Agent-1"

        mock_batch_service = Mock()
        mock_batch_service.cancel_batch.return_value = False
        mock_service.return_value = mock_batch_service

        result = handler.handle(args)
        assert result is True
        assert handler.exit_code == 0

    @patch('src.services.message_batching_service.get_batching_service')
    def test_handle_import_error(self, mock_service):
        """Test handle with ImportError."""
        handler = BatchMessageHandler()
        args = Mock()
        args.batch_start = True
        args.agent = "Agent-1"

        mock_service.side_effect = ImportError("Service not available")

        result = handler.handle(args)
        assert result is True
        assert handler.exit_code == 1

    @patch('src.services.message_batching_service.get_batching_service')
    def test_handle_exception(self, mock_service):
        """Test handle with general exception."""
        handler = BatchMessageHandler()
        args = Mock()
        args.batch_start = True
        args.agent = "Agent-1"

        mock_service.side_effect = Exception("Unexpected error")

        result = handler.handle(args)
        assert result is True
        assert handler.exit_code == 1

    @patch('src.core.messaging_core.send_message')
    @patch('src.services.message_batching_service.get_batching_service')
    def test_handle_normal_priority_normalized(self, mock_service, mock_send):
        """Test handle normalizes 'normal' priority to 'regular'."""
        handler = BatchMessageHandler()
        args = Mock()
        args.batch = ["Message 1"]
        args.agent = "Agent-1"
        args.priority = "normal"

        mock_batch_service = Mock()
        mock_batch_service.start_batch.return_value = True
        mock_batch_service.add_to_batch.return_value = True
        mock_batch_service.send_batch.return_value = (True, "Consolidated message")
        mock_service.return_value = mock_batch_service
        mock_send.return_value = True

        result = handler.handle(args)
        assert result is True
        # Verify send_batch was called with 'regular' priority
        call_args = mock_batch_service.send_batch.call_args
        assert call_args[1]['priority'] == 'regular'


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

