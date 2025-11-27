"""
Unit tests for soft_onboarding_service.py
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import sys
import subprocess

from src.services.soft_onboarding_service import (
    SoftOnboardingService,
    soft_onboard_agent,
    soft_onboard_multiple_agents,
    generate_cycle_accomplishments_report
)


class TestSoftOnboardingService:
    """Tests for SoftOnboardingService class."""

    def test_init(self):
        """Test SoftOnboardingService initialization."""
        service = SoftOnboardingService()
        assert service._handler is None
        assert hasattr(service, 'handler')

    @patch('src.services.handlers.soft_onboarding_handler.SoftOnboardingHandler')
    def test_handler_lazy_loading(self, mock_handler_class):
        """Test handler lazy loading property."""
        service = SoftOnboardingService()
        mock_handler_instance = Mock()
        mock_handler_class.return_value = mock_handler_instance
        
        # Access handler property
        handler = service.handler
        
        # Verify handler was created
        assert handler == mock_handler_instance
        mock_handler_class.assert_called_once()
        
        # Verify handler is cached
        handler2 = service.handler
        assert handler2 == handler
        assert mock_handler_class.call_count == 1

    @patch('src.services.handlers.soft_onboarding_handler.SoftOnboardingHandler')
    def test_onboard_agent_success(self, mock_handler_class):
        """Test onboard_agent with successful handler."""
        service = SoftOnboardingService()
        mock_handler = Mock()
        mock_handler.handle.return_value = True
        mock_handler_class.return_value = mock_handler
        
        result = service.onboard_agent("Agent-1", "Test message")
        
        assert result is True
        mock_handler.handle.assert_called_once()
        call_args = mock_handler.handle.call_args[0][0]
        assert call_args.agent == "Agent-1"
        assert call_args.message == "Test message"

    @patch('src.services.handlers.soft_onboarding_handler.SoftOnboardingHandler')
    def test_onboard_agent_with_kwargs(self, mock_handler_class):
        """Test onboard_agent with additional kwargs."""
        service = SoftOnboardingService()
        mock_handler = Mock()
        mock_handler.handle.return_value = True
        mock_handler_class.return_value = mock_handler
        
        result = service.onboard_agent("Agent-2", "Test", role="test_role")
        
        assert result is True
        call_args = mock_handler.handle.call_args[0][0]
        assert call_args.role == "test_role"

    @patch('src.services.handlers.soft_onboarding_handler.SoftOnboardingHandler')
    def test_onboard_agent_failure(self, mock_handler_class):
        """Test onboard_agent when handler raises exception."""
        service = SoftOnboardingService()
        mock_handler = Mock()
        mock_handler.handle.side_effect = Exception("Handler error")
        mock_handler_class.return_value = mock_handler
        
        result = service.onboard_agent("Agent-1", "Test")
        
        assert result is False

    @patch('src.services.soft_onboarding_service.keyboard_control')
    @patch('src.services.handlers.soft_onboarding_handler.SoftOnboardingHandler')
    def test_execute_soft_onboarding_success(self, mock_handler_class, mock_keyboard_control):
        """Test execute_soft_onboarding with successful execution."""
        service = SoftOnboardingService()
        mock_handler = Mock()
        mock_handler.handle.return_value = True
        mock_handler_class.return_value = mock_handler
        mock_keyboard_control.return_value.__enter__ = Mock()
        mock_keyboard_control.return_value.__exit__ = Mock()
        
        result = service.execute_soft_onboarding(
            "Agent-1", "Onboarding message", role="test_role"
        )
        
        assert result is True
        mock_keyboard_control.assert_called_once_with("soft_onboard_Agent-1")
        mock_handler.handle.assert_called_once()

    @patch('src.services.soft_onboarding_service.keyboard_control')
    @patch('src.services.handlers.soft_onboarding_handler.SoftOnboardingHandler')
    def test_execute_soft_onboarding_failure(self, mock_handler_class, mock_keyboard_control):
        """Test execute_soft_onboarding when handler fails."""
        service = SoftOnboardingService()
        mock_handler = Mock()
        mock_handler.handle.side_effect = Exception("Handler error")
        mock_handler_class.return_value = mock_handler
        mock_keyboard_control.return_value.__enter__ = Mock()
        mock_keyboard_control.return_value.__exit__ = Mock()
        
        result = service.execute_soft_onboarding("Agent-1", "Message")
        
        assert result is False


class TestSoftOnboardAgent:
    """Tests for soft_onboard_agent convenience function."""

    @patch('src.services.soft_onboarding_service.is_locked')
    @patch('src.services.soft_onboarding_service.keyboard_control')
    @patch('src.services.soft_onboarding_service.SoftOnboardingService')
    def test_soft_onboard_agent_success(self, mock_service_class, mock_keyboard_control, mock_is_locked):
        """Test soft_onboard_agent with successful onboarding."""
        mock_is_locked.return_value = False
        mock_service = Mock()
        mock_service.onboard_agent.return_value = True
        mock_service_class.return_value = mock_service
        mock_keyboard_control.return_value.__enter__ = Mock()
        mock_keyboard_control.return_value.__exit__ = Mock()
        
        result = soft_onboard_agent("Agent-1", "Test message")
        
        assert result is True
        mock_keyboard_control.assert_called_once_with("soft_onboard_Agent-1")
        mock_service.onboard_agent.assert_called_once_with("Agent-1", "Test message")

    @patch('src.services.soft_onboarding_service.is_locked')
    @patch('src.services.soft_onboarding_service.SoftOnboardingService')
    def test_soft_onboard_agent_lock_already_held(self, mock_service_class, mock_is_locked):
        """Test soft_onboard_agent when lock is already held."""
        mock_is_locked.return_value = True
        mock_service = Mock()
        mock_service.onboard_agent.return_value = True
        mock_service_class.return_value = mock_service
        
        result = soft_onboard_agent("Agent-1", "Test message")
        
        assert result is True
        mock_service.onboard_agent.assert_called_once()
        # Should not acquire lock again
        mock_is_locked.assert_called_once()


class TestSoftOnboardMultipleAgents:
    """Tests for soft_onboard_multiple_agents function."""

    @patch('src.services.soft_onboarding_service.time.sleep')
    @patch('src.services.soft_onboarding_service.soft_onboard_agent')
    @patch('src.services.soft_onboarding_service.keyboard_control')
    def test_soft_onboard_multiple_agents_success(self, mock_keyboard_control, mock_onboard, mock_sleep):
        """Test soft_onboard_multiple_agents with successful onboarding."""
        mock_keyboard_control.return_value.__enter__ = Mock()
        mock_keyboard_control.return_value.__exit__ = Mock()
        mock_onboard.side_effect = [True, True, False]
        
        agents = [("Agent-1", "Message 1"), ("Agent-2", "Message 2"), ("Agent-3", "Message 3")]
        results = soft_onboard_multiple_agents(agents, role="test_role")
        
        assert results == {"Agent-1": True, "Agent-2": True, "Agent-3": False}
        assert mock_onboard.call_count == 3
        mock_keyboard_control.assert_called_once_with("soft_onboard_multiple")

    @patch('subprocess.run')
    @patch('pathlib.Path.exists')
    @patch('src.services.soft_onboarding_service.soft_onboard_agent')
    @patch('src.services.soft_onboarding_service.keyboard_control')
    def test_soft_onboard_multiple_with_cycle_report(
        self, mock_keyboard_control, mock_onboard, mock_exists, mock_subprocess
    ):
        """Test soft_onboard_multiple_agents with cycle report generation."""
        mock_keyboard_control.return_value.__enter__ = Mock()
        mock_keyboard_control.return_value.__exit__ = Mock()
        mock_onboard.return_value = True
        mock_exists.return_value = True
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "Report generated: /path/to/report.md"
        mock_subprocess.return_value = mock_result
        
        agents = [("Agent-1", "Message 1")]
        results = soft_onboard_multiple_agents(agents, generate_cycle_report=True)
        
        assert results == {"Agent-1": True}
        mock_subprocess.assert_called_once()

    @patch('src.services.soft_onboarding_service.soft_onboard_agent')
    @patch('src.services.soft_onboarding_service.keyboard_control')
    def test_soft_onboard_multiple_without_cycle_report(self, mock_keyboard_control, mock_onboard):
        """Test soft_onboard_multiple_agents without cycle report."""
        mock_keyboard_control.return_value.__enter__ = Mock()
        mock_keyboard_control.return_value.__exit__ = Mock()
        mock_onboard.return_value = True
        
        agents = [("Agent-1", "Message 1")]
        results = soft_onboard_multiple_agents(agents, generate_cycle_report=False)
        
        assert results == {"Agent-1": True}


class TestGenerateCycleAccomplishmentsReport:
    """Tests for generate_cycle_accomplishments_report function."""

    @patch('subprocess.run')
    @patch('pathlib.Path.exists')
    def test_generate_cycle_report_success(self, mock_exists, mock_subprocess):
        """Test successful cycle report generation."""
        mock_exists.return_value = True
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "Report generated: /path/to/report.md"
        mock_subprocess.return_value = mock_result
        
        result = generate_cycle_accomplishments_report()
        
        assert result is not None
        assert isinstance(result, Path)
        mock_subprocess.assert_called_once()

    @patch('pathlib.Path.exists')
    def test_generate_cycle_report_script_not_found(self, mock_exists):
        """Test cycle report generation when script doesn't exist."""
        mock_exists.return_value = False
        
        result = generate_cycle_accomplishments_report()
        
        assert result is None

    @patch('subprocess.run')
    @patch('pathlib.Path.exists')
    def test_generate_cycle_report_with_cycle_id(self, mock_exists, mock_subprocess):
        """Test cycle report generation with cycle ID."""
        mock_exists.return_value = True
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "Report generated: /path/to/report.md"
        mock_subprocess.return_value = mock_result
        
        result = generate_cycle_accomplishments_report("C-123")
        
        assert result is not None
        # Verify cycle ID was passed to script
        call_args = mock_subprocess.call_args[0][0]
        assert "--cycle" in call_args
        assert "C-123" in call_args

    @patch('subprocess.run')
    @patch('pathlib.Path.exists')
    def test_generate_cycle_report_failure(self, mock_exists, mock_subprocess):
        """Test cycle report generation when subprocess fails."""
        mock_exists.return_value = True
        mock_result = Mock()
        mock_result.returncode = 1
        mock_result.stderr = "Error message"
        mock_subprocess.return_value = mock_result
        
        result = generate_cycle_accomplishments_report()
        
        assert result is None

