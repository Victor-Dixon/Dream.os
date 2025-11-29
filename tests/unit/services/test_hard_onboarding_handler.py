"""
Unit tests for hard_onboarding_handler.py
Target: ≥85% coverage
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
from src.services.handlers.hard_onboarding_handler import HardOnboardingHandler


class TestHardOnboardingHandler:
    """Tests for HardOnboardingHandler class."""

    def test_init(self):
        """Test HardOnboardingHandler initialization."""
        handler = HardOnboardingHandler()
        assert handler.exit_code == 0

    def test_can_handle_hard_onboarding_flag(self):
        """Test can_handle returns True for hard_onboarding flag."""
        handler = HardOnboardingHandler()
        args = Mock(hard_onboarding=True)
        assert handler.can_handle(args) is True

    def test_can_handle_false(self):
        """Test can_handle returns False when flag not set."""
        handler = HardOnboardingHandler()
        args = Mock(spec=[])
        assert handler.can_handle(args) is False

    def test_handle_missing_agent(self):
        """Test handle returns error when agent missing."""
        handler = HardOnboardingHandler()
        args = Mock(agent=None, message="Test", onboarding_file=None)
        
        result = handler.handle(args)
        assert result is True
        assert handler.exit_code == 1

    def test_handle_missing_message_and_file(self):
        """Test handle returns error when message and file missing."""
        handler = HardOnboardingHandler()
        args = Mock(agent="Agent-1", message=None, onboarding_file=None)
        
        result = handler.handle(args)
        assert result is True
        assert handler.exit_code == 1

    def test_handle_load_from_file_success(self):
        """Test handle loads message from file successfully."""
        handler = HardOnboardingHandler()
        args = Mock(
            agent="Agent-1",
            message=None,
            onboarding_file="test.md",
            role="Test Role",
            dry_run=False
        )
        
        with patch('pathlib.Path.exists', return_value=True):
            with patch('pathlib.Path.read_text', return_value="File content"):
                with patch('src.services.handlers.hard_onboarding_handler.HardOnboardingService') as mock_service:
                    mock_svc = Mock()
                    mock_svc.execute_hard_onboarding.return_value = True
                    mock_service.return_value = mock_svc
                    
                    result = handler.handle(args)
                    assert result is True
                    assert handler.exit_code == 0

    def test_handle_file_not_found(self):
        """Test handle handles file not found."""
        handler = HardOnboardingHandler()
        args = Mock(
            agent="Agent-1",
            message=None,
            onboarding_file="nonexistent.md",
            role=None
        )
        
        with patch('pathlib.Path.exists', return_value=False):
            result = handler.handle(args)
            assert result is True
            assert handler.exit_code == 1

    def test_handle_file_read_error(self):
        """Test handle handles file read error."""
        handler = HardOnboardingHandler()
        args = Mock(
            agent="Agent-1",
            message=None,
            onboarding_file="test.md",
            role=None
        )
        
        with patch('pathlib.Path.exists', return_value=True):
            with patch('pathlib.Path.read_text', side_effect=Exception("Read error")):
                result = handler.handle(args)
                assert result is True
                assert handler.exit_code == 1

    def test_handle_dry_run(self):
        """Test handle handles dry run."""
        handler = HardOnboardingHandler()
        args = Mock(
            agent="Agent-1",
            message="Test message",
            onboarding_file=None,
            role="Test Role",
            dry_run=True
        )
        
        result = handler.handle(args)
        assert result is True
        assert handler.exit_code == 0

    def test_handle_success(self):
        """Test handle executes hard onboarding successfully."""
        handler = HardOnboardingHandler()
        args = Mock(
            agent="Agent-1",
            message="Test message",
            onboarding_file=None,
            role="Test Role",
            dry_run=False
        )
        
        with patch('src.services.handlers.hard_onboarding_handler.HardOnboardingService') as mock_service:
            mock_svc = Mock()
            mock_svc.execute_hard_onboarding.return_value = True
            mock_service.return_value = mock_svc
            
            result = handler.handle(args)
            assert result is True
            assert handler.exit_code == 0

    def test_handle_failure(self):
        """Test handle handles hard onboarding failure."""
        handler = HardOnboardingHandler()
        args = Mock(
            agent="Agent-1",
            message="Test message",
            onboarding_file=None,
            role="Test Role",
            dry_run=False
        )
        
        with patch('src.services.handlers.hard_onboarding_handler.HardOnboardingService') as mock_service:
            mock_svc = Mock()
            mock_svc.execute_hard_onboarding.return_value = False
            mock_service.return_value = mock_svc
            
            result = handler.handle(args)
            assert result is True
            assert handler.exit_code == 1

    def test_handle_import_error(self):
        """Test handle handles ImportError."""
        handler = HardOnboardingHandler()
        args = Mock(agent="Agent-1", message="Test")
        
        with patch('src.services.handlers.hard_onboarding_handler.HardOnboardingService', side_effect=ImportError("Service not available")):
            result = handler.handle(args)
            assert result is True
            assert handler.exit_code == 1

    def test_handle_general_exception(self):
        """Test handle handles general exceptions."""
        handler = HardOnboardingHandler()
        args = Mock(agent="Agent-1", message="Test")
        
        with patch('src.services.handlers.hard_onboarding_handler.HardOnboardingService', side_effect=Exception("General error")):
            result = handler.handle(args)
            assert result is True
            assert handler.exit_code == 1

    def test_handle_uses_message_when_provided(self):
        """Test handle uses message when both message and file provided."""
        handler = HardOnboardingHandler()
        args = Mock(
            agent="Agent-1",
            message="Direct message",
            onboarding_file="test.md",
            role="Test Role",
            dry_run=False
        )
        
        with patch('src.services.handlers.hard_onboarding_handler.HardOnboardingService') as mock_service:
            mock_svc = Mock()
            mock_svc.execute_hard_onboarding.return_value = True
            mock_service.return_value = mock_svc
            
            result = handler.handle(args)
            # Verify execute_hard_onboarding was called with direct message
            mock_svc.execute_hard_onboarding.assert_called_once()
            call_args = mock_svc.execute_hard_onboarding.call_args
            assert call_args[1]['onboarding_message'] == "Direct message"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

