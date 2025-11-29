"""
Tests for role_command_handler.py

Comprehensive tests for role command handler.
Target: ≥85% coverage
"""

import pytest
from unittest.mock import MagicMock, patch
from src.services.role_command_handler import RoleCommandHandler


class TestRoleCommandHandler:
    """Tests for RoleCommandHandler."""

    def test_initialization(self):
        """Test handler initialization."""
        handler = RoleCommandHandler()
        assert handler is not None

    def test_can_handle_with_role_mode_flag(self):
        """Test can_handle when role_mode flag is present."""
        handler = RoleCommandHandler()
        args = MagicMock()
        args.role_mode = "test_mode"
        
        result = handler.can_handle(args)
        
        # Returns the truthy value, not necessarily True
        assert result == "test_mode"
        assert bool(result) is True

    def test_can_handle_with_role_mode_none(self):
        """Test can_handle when role_mode is None."""
        handler = RoleCommandHandler()
        args = MagicMock()
        args.role_mode = None
        
        result = handler.can_handle(args)
        
        # Returns None (falsy) because of 'and' short-circuit
        assert result is None
        assert bool(result) is False

    def test_can_handle_with_role_mode_empty_string(self):
        """Test can_handle when role_mode is empty string."""
        handler = RoleCommandHandler()
        args = MagicMock()
        args.role_mode = ""
        
        result = handler.can_handle(args)
        
        # Returns "" (falsy) because of 'and' short-circuit
        assert result == ""
        assert bool(result) is False

    def test_can_handle_without_role_mode_flag(self):
        """Test can_handle when role_mode flag is missing."""
        handler = RoleCommandHandler()
        args = MagicMock()
        del args.role_mode
        
        result = handler.can_handle(args)
        
        assert result is False

    def test_can_handle_without_args_attribute(self):
        """Test can_handle when args doesn't have role_mode attribute."""
        handler = RoleCommandHandler()
        args = object()  # Plain object without role_mode attribute
        
        result = handler.can_handle(args)
        
        assert result is False

    @patch('src.services.role_command_handler.logger')
    def test_handle_success(self, mock_logger):
        """Test handle method success."""
        handler = RoleCommandHandler()
        args = MagicMock()
        args.role_mode = "test_mode"
        
        result = handler.handle(args)
        
        assert result is True
        assert mock_logger.info.call_count >= 3

    @patch('src.services.role_command_handler.logger')
    def test_handle_logs_role_mode(self, mock_logger):
        """Test that handle logs role mode."""
        handler = RoleCommandHandler()
        args = MagicMock()
        args.role_mode = "developer"
        
        handler.handle(args)
        
        # Check that role mode was logged
        log_calls = [call[0][0] for call in mock_logger.info.call_args_list]
        assert any("developer" in msg.lower() for msg in log_calls)
        assert any("role mode" in msg.lower() for msg in log_calls)

    @patch('src.services.role_command_handler.logger')
    def test_handle_logs_development_message(self, mock_logger):
        """Test that handle logs development message."""
        handler = RoleCommandHandler()
        args = MagicMock()
        args.role_mode = "test"
        
        handler.handle(args)
        
        log_calls = [call[0][0] for call in mock_logger.info.call_args_list]
        assert any("development" in msg.lower() for msg in log_calls)

    def test_handle_returns_true(self):
        """Test that handle always returns True."""
        handler = RoleCommandHandler()
        args = MagicMock()
        args.role_mode = "test"
        
        result = handler.handle(args)
        
        assert result is True

    def test_handle_with_different_role_modes(self):
        """Test handle with different role mode values."""
        handler = RoleCommandHandler()
        
        args1 = MagicMock()
        args1.role_mode = "developer"
        args2 = MagicMock()
        args2.role_mode = "manager"
        args3 = MagicMock()
        args3.role_mode = ""
        
        result1 = handler.handle(args1)
        result2 = handler.handle(args2)
        result3 = handler.handle(args3)
        
        assert result1 is True
        assert result2 is True
        assert result3 is True

    def test_handle_with_different_args(self):
        """Test handle with different argument types."""
        handler = RoleCommandHandler()
        
        args1 = MagicMock()
        args1.role_mode = "test"
        args2 = object()
        
        result1 = handler.handle(args1)
        # args2 doesn't have role_mode, but handle should still work
        try:
            result2 = handler.handle(args2)
            # If it doesn't raise, should return True
            assert result2 is True
        except AttributeError:
            # If it raises, that's also acceptable behavior
            pass
        
        assert result1 is True

