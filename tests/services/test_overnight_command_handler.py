"""
Tests for overnight_command_handler.py

Comprehensive tests for overnight command handler.
Target: ≥85% coverage
"""

import pytest
from unittest.mock import MagicMock, patch
from src.services.overnight_command_handler import OvernightCommandHandler


class TestOvernightCommandHandler:
    """Tests for OvernightCommandHandler."""

    def test_initialization(self):
        """Test handler initialization."""
        handler = OvernightCommandHandler()
        assert handler is not None

    def test_can_handle_with_overnight_flag(self):
        """Test can_handle when overnight flag is present."""
        handler = OvernightCommandHandler()
        args = MagicMock()
        args.overnight = True
        
        result = handler.can_handle(args)
        
        assert result is True

    def test_can_handle_without_overnight_flag(self):
        """Test can_handle when overnight flag is missing."""
        handler = OvernightCommandHandler()
        args = MagicMock()
        del args.overnight
        
        result = handler.can_handle(args)
        
        assert result is False

    def test_can_handle_with_overnight_false(self):
        """Test can_handle when overnight flag is False."""
        handler = OvernightCommandHandler()
        args = MagicMock()
        args.overnight = False
        
        result = handler.can_handle(args)
        
        assert result is False

    def test_can_handle_without_args_attribute(self):
        """Test can_handle when args doesn't have overnight attribute."""
        handler = OvernightCommandHandler()
        args = object()  # Plain object without overnight attribute
        
        result = handler.can_handle(args)
        
        assert result is False

    @patch('src.services.overnight_command_handler.logger')
    def test_handle_success(self, mock_logger):
        """Test handle method success."""
        handler = OvernightCommandHandler()
        args = MagicMock()
        
        result = handler.handle(args)
        
        assert result is True
        assert mock_logger.info.call_count >= 3

    @patch('src.services.overnight_command_handler.logger')
    def test_handle_logs_messages(self, mock_logger):
        """Test that handle logs appropriate messages."""
        handler = OvernightCommandHandler()
        args = MagicMock()
        
        handler.handle(args)
        
        # Check that specific log messages were called
        log_calls = [call[0][0] for call in mock_logger.info.call_args_list]
        assert any("overnight" in msg.lower() for msg in log_calls)
        assert any("development" in msg.lower() for msg in log_calls)

    def test_handle_returns_true(self):
        """Test that handle always returns True."""
        handler = OvernightCommandHandler()
        args = MagicMock()
        
        result = handler.handle(args)
        
        assert result is True

    def test_handle_with_different_args(self):
        """Test handle with different argument types."""
        handler = OvernightCommandHandler()
        
        # Test with various arg types
        args1 = MagicMock()
        args2 = object()
        
        result1 = handler.handle(args1)
        result2 = handler.handle(args2)
        
        assert result1 is True
        assert result2 is True

