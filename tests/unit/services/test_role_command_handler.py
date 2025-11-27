"""
Tests for role_command_handler.py

Author: Agent-3 (Infrastructure & DevOps Specialist)
Date: 2025-11-27
"""

import pytest
from unittest.mock import Mock, patch
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(project_root))

from src.services.role_command_handler import RoleCommandHandler


class TestRoleCommandHandler:
    """Test RoleCommandHandler class."""

    def test_init(self):
        """Test RoleCommandHandler initialization."""
        handler = RoleCommandHandler()
        assert handler is not None
        assert hasattr(handler, 'can_handle')
        assert hasattr(handler, 'handle')

    def test_can_handle_with_role_mode(self):
        """Test can_handle returns role_mode value when args has role_mode."""
        handler = RoleCommandHandler()
        args = Mock()
        args.role_mode = "test_role"
        
        result = handler.can_handle(args)
        
        assert result == "test_role"

    def test_can_handle_without_role_mode(self):
        """Test can_handle returns False when args lacks role_mode."""
        handler = RoleCommandHandler()
        args = Mock()
        # Mock hasattr to return False
        with patch('builtins.hasattr', return_value=False):
            result = handler.can_handle(args)
            assert result is False

    def test_can_handle_with_false_role_mode(self):
        """Test can_handle returns False when role_mode is False."""
        handler = RoleCommandHandler()
        args = Mock()
        args.role_mode = False
        
        result = handler.can_handle(args)
        
        assert result is False

    def test_can_handle_with_none_role_mode(self):
        """Test can_handle returns None when role_mode is None."""
        handler = RoleCommandHandler()
        args = Mock()
        args.role_mode = None
        
        result = handler.can_handle(args)
        
        # The method returns args.role_mode if it exists, so None is returned
        assert result is None

    @patch("src.services.role_command_handler.logger")
    def test_handle_success(self, mock_logger):
        """Test handle method logs and returns True."""
        handler = RoleCommandHandler()
        args = Mock()
        args.role_mode = "test_role"
        
        result = handler.handle(args)
        
        assert result is True
        assert mock_logger.info.called
        assert any("Setting role mode" in str(call) for call in mock_logger.info.call_args_list)

    @patch("src.services.role_command_handler.logger")
    def test_handle_logs_role_mode(self, mock_logger):
        """Test handle logs the role mode correctly."""
        handler = RoleCommandHandler()
        args = Mock()
        args.role_mode = "developer"
        
        handler.handle(args)
        
        # Check that role mode was logged
        call_args = [str(call) for call in mock_logger.info.call_args_list]
        assert any("developer" in call for call in call_args)

    @patch("src.services.role_command_handler.logger")
    def test_handle_logs_development_message(self, mock_logger):
        """Test handle logs development message."""
        handler = RoleCommandHandler()
        args = Mock()
        args.role_mode = "test"
        
        handler.handle(args)
        
        # Check that development message was logged
        call_args = [str(call) for call in mock_logger.info.call_args_list]
        assert any("under development" in call.lower() for call in call_args)

    @patch("src.services.role_command_handler.logger")
    def test_handle_logs_standard_commands_message(self, mock_logger):
        """Test handle logs standard commands message."""
        handler = RoleCommandHandler()
        args = Mock()
        args.role_mode = "test"
        
        handler.handle(args)
        
        # Check that standard commands message was logged
        call_args = [str(call) for call in mock_logger.info.call_args_list]
        assert any("standard messaging" in call.lower() for call in call_args)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

