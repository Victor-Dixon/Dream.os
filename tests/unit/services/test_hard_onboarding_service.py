"""
Unit tests for hard_onboarding_service.py
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import time

from src.services.hard_onboarding_service import (
    HardOnboardingService,
    hard_onboard_agent,
    hard_onboard_multiple_agents
)


class TestHardOnboardingService:
    """Tests for HardOnboardingService class."""

    @patch('src.services.hard_onboarding_service.PYAUTOGUI_AVAILABLE', True)
    @patch('src.services.hard_onboarding_service.pyautogui')
    def test_init_success(self, mock_pyautogui):
        """Test HardOnboardingService initialization with PyAutoGUI."""
        service = HardOnboardingService()
        assert service.pyautogui == mock_pyautogui

    @patch('src.services.hard_onboarding_service.PYAUTOGUI_AVAILABLE', False)
    def test_init_failure_no_pyautogui(self):
        """Test HardOnboardingService initialization without PyAutoGUI."""
        with pytest.raises(ImportError, match="PyAutoGUI required"):
            HardOnboardingService()

    @patch('src.services.hard_onboarding_service.get_coordinate_loader')
    @patch('src.services.hard_onboarding_service.PYAUTOGUI_AVAILABLE', True)
    @patch('src.services.hard_onboarding_service.pyautogui')
    def test_load_agent_coordinates(self, mock_pyautogui, mock_get_loader):
        """Test _load_agent_coordinates method."""
        service = HardOnboardingService()
        mock_loader = Mock()
        mock_loader.get_chat_coordinates.return_value = (100, 200)
        mock_loader.get_onboarding_coordinates.return_value = (300, 400)
        mock_get_loader.return_value = mock_loader
        
        chat_coords, onboarding_coords = service._load_agent_coordinates("Agent-1")
        
        assert chat_coords == (100, 200)
        assert onboarding_coords == (300, 400)
        mock_loader.get_chat_coordinates.assert_called_once_with("Agent-1")
        mock_loader.get_onboarding_coordinates.assert_called_once_with("Agent-1")

    @patch('src.services.hard_onboarding_service.PyAutoGUIMessagingDelivery')
    @patch('src.services.hard_onboarding_service.PYAUTOGUI_AVAILABLE', True)
    @patch('src.services.hard_onboarding_service.pyautogui')
    def test_validate_coordinates(self, mock_pyautogui, mock_delivery_class):
        """Test _validate_coordinates method."""
        service = HardOnboardingService()
        mock_delivery = Mock()
        mock_delivery.validate_coordinates.return_value = True
        mock_delivery_class.return_value = mock_delivery
        
        result = service._validate_coordinates("Agent-1", (100, 200))
        
        assert result is True
        mock_delivery.validate_coordinates.assert_called_once_with("Agent-1", (100, 200))

    @patch('src.services.hard_onboarding_service.time.sleep')
    @patch('src.services.hard_onboarding_service.get_coordinate_loader')
    @patch('src.services.hard_onboarding_service.PyAutoGUIMessagingDelivery')
    @patch('src.services.hard_onboarding_service.PYAUTOGUI_AVAILABLE', True)
    @patch('src.services.hard_onboarding_service.pyautogui')
    def test_step_1_clear_chat_success(
        self, mock_pyautogui, mock_delivery_class, mock_get_loader, mock_sleep
    ):
        """Test step_1_clear_chat with successful execution."""
        service = HardOnboardingService()
        mock_loader = Mock()
        mock_loader.get_chat_coordinates.return_value = (100, 200)
        mock_loader.get_onboarding_coordinates.return_value = (300, 400)
        mock_get_loader.return_value = mock_loader
        mock_delivery = Mock()
        mock_delivery.validate_coordinates.return_value = True
        mock_delivery_class.return_value = mock_delivery
        
        result = service.step_1_clear_chat("Agent-1")
        
        assert result is True
        mock_pyautogui.moveTo.assert_called_once_with(100, 200)
        mock_pyautogui.click.assert_called_once()
        mock_pyautogui.hotkey.assert_called_once_with("ctrl", "shift", "backspace")

    @patch('src.services.hard_onboarding_service.get_coordinate_loader')
    @patch('src.services.hard_onboarding_service.PYAUTOGUI_AVAILABLE', True)
    @patch('src.services.hard_onboarding_service.pyautogui')
    def test_step_1_clear_chat_no_coordinates(self, mock_pyautogui, mock_get_loader):
        """Test step_1_clear_chat when coordinates are missing."""
        service = HardOnboardingService()
        mock_loader = Mock()
        mock_loader.get_chat_coordinates.return_value = None
        mock_get_loader.return_value = mock_loader
        
        result = service.step_1_clear_chat("Agent-1")
        
        assert result is False

    @patch('src.services.hard_onboarding_service.time.sleep')
    @patch('src.services.hard_onboarding_service.PYAUTOGUI_AVAILABLE', True)
    @patch('src.services.hard_onboarding_service.pyautogui')
    def test_step_2_send_execute_success(self, mock_pyautogui, mock_sleep):
        """Test step_2_send_execute with successful execution."""
        service = HardOnboardingService()
        
        result = service.step_2_send_execute()
        
        assert result is True
        mock_pyautogui.hotkey.assert_called_once_with("ctrl", "enter")

    @patch('src.services.hard_onboarding_service.time.sleep')
    @patch('src.services.hard_onboarding_service.PYAUTOGUI_AVAILABLE', True)
    @patch('src.services.hard_onboarding_service.pyautogui')
    def test_step_3_new_window_success(self, mock_pyautogui, mock_sleep):
        """Test step_3_new_window with successful execution."""
        service = HardOnboardingService()
        
        result = service.step_3_new_window()
        
        assert result is True
        mock_pyautogui.hotkey.assert_called_once_with("ctrl", "n")

    @patch('src.services.hard_onboarding_service.time.sleep')
    @patch('src.services.hard_onboarding_service.get_coordinate_loader')
    @patch('src.services.hard_onboarding_service.PYAUTOGUI_AVAILABLE', True)
    @patch('src.services.hard_onboarding_service.pyautogui')
    def test_step_4_navigate_to_onboarding_success(
        self, mock_pyautogui, mock_get_loader, mock_sleep
    ):
        """Test step_4_navigate_to_onboarding with successful execution."""
        service = HardOnboardingService()
        mock_loader = Mock()
        mock_loader.get_chat_coordinates.return_value = (100, 200)
        mock_loader.get_onboarding_coordinates.return_value = (300, 400)
        mock_get_loader.return_value = mock_loader
        
        result = service.step_4_navigate_to_onboarding("Agent-1")
        
        assert result is True
        mock_pyautogui.moveTo.assert_called_once_with(300, 400)
        mock_pyautogui.click.assert_called_once()

    @patch('src.services.hard_onboarding_service.get_coordinate_loader')
    @patch('src.services.hard_onboarding_service.PYAUTOGUI_AVAILABLE', True)
    @patch('src.services.hard_onboarding_service.pyautogui')
    def test_step_4_navigate_invalid_coordinates(self, mock_pyautogui, mock_get_loader):
        """Test step_4_navigate_to_onboarding with invalid coordinates."""
        service = HardOnboardingService()
        mock_loader = Mock()
        mock_loader.get_chat_coordinates.return_value = (100, 200)
        mock_loader.get_onboarding_coordinates.return_value = (-3000, 500)  # Out of bounds
        mock_get_loader.return_value = mock_loader
        
        result = service.step_4_navigate_to_onboarding("Agent-1")
        
        assert result is False

    @patch('src.services.hard_onboarding_service.TEMPLATE_LOADER_AVAILABLE', True)
    @patch('src.services.hard_onboarding_service.load_onboarding_template')
    @patch('src.services.hard_onboarding_service.pyperclip')
    @patch('src.services.hard_onboarding_service.time.sleep')
    @patch('src.services.hard_onboarding_service.PYAUTOGUI_AVAILABLE', True)
    @patch('src.services.hard_onboarding_service.pyautogui')
    def test_step_5_send_onboarding_message_with_template(
        self, mock_pyautogui, mock_sleep, mock_pyperclip, mock_load_template
    ):
        """Test step_5_send_onboarding_message with template loader."""
        service = HardOnboardingService()
        mock_load_template.return_value = "Full template message"
        
        result = service.step_5_send_onboarding_message(
            "Agent-1", "Custom message", role="test_role"
        )
        
        assert result is True
        mock_load_template.assert_called_once_with(
            agent_id="Agent-1", role="test_role", custom_message="Custom message"
        )
        mock_pyperclip.copy.assert_called_once_with("Full template message")
        mock_pyautogui.hotkey.assert_called_once_with("ctrl", "v")
        mock_pyautogui.press.assert_called_once_with("enter")

    @patch('src.services.hard_onboarding_service.TEMPLATE_LOADER_AVAILABLE', False)
    @patch('src.services.hard_onboarding_service.pyperclip')
    @patch('src.services.hard_onboarding_service.time.sleep')
    @patch('src.services.hard_onboarding_service.PYAUTOGUI_AVAILABLE', True)
    @patch('src.services.hard_onboarding_service.pyautogui')
    def test_step_5_send_onboarding_message_without_template(
        self, mock_pyautogui, mock_sleep, mock_pyperclip
    ):
        """Test step_5_send_onboarding_message without template loader."""
        service = HardOnboardingService()
        
        result = service.step_5_send_onboarding_message("Agent-1", "Custom message")
        
        assert result is True
        mock_pyperclip.copy.assert_called_once_with("Custom message")
        mock_pyautogui.hotkey.assert_called_once_with("ctrl", "v")
        mock_pyautogui.press.assert_called_once_with("enter")

    @patch('src.services.hard_onboarding_service.HardOnboardingService.step_5_send_onboarding_message')
    @patch('src.services.hard_onboarding_service.HardOnboardingService.step_4_navigate_to_onboarding')
    @patch('src.services.hard_onboarding_service.HardOnboardingService.step_3_new_window')
    @patch('src.services.hard_onboarding_service.HardOnboardingService.step_2_send_execute')
    @patch('src.services.hard_onboarding_service.HardOnboardingService.step_1_clear_chat')
    @patch('src.services.hard_onboarding_service.PYAUTOGUI_AVAILABLE', True)
    @patch('src.services.hard_onboarding_service.pyautogui')
    def test_execute_hard_onboarding_success(
        self, mock_pyautogui, mock_step1, mock_step2, mock_step3, mock_step4, mock_step5
    ):
        """Test execute_hard_onboarding with all steps successful."""
        service = HardOnboardingService()
        mock_step1.return_value = True
        mock_step2.return_value = True
        mock_step3.return_value = True
        mock_step4.return_value = True
        mock_step5.return_value = True
        
        result = service.execute_hard_onboarding("Agent-1", "Onboarding message", role="test_role")
        
        assert result is True
        mock_step1.assert_called_once_with("Agent-1")
        mock_step2.assert_called_once()
        mock_step3.assert_called_once()
        mock_step4.assert_called_once_with("Agent-1")
        mock_step5.assert_called_once_with("Agent-1", "Onboarding message", role="test_role")

    @patch('src.services.hard_onboarding_service.HardOnboardingService.step_1_clear_chat')
    @patch('src.services.hard_onboarding_service.PYAUTOGUI_AVAILABLE', True)
    @patch('src.services.hard_onboarding_service.pyautogui')
    def test_execute_hard_onboarding_step1_failure(self, mock_pyautogui, mock_step1):
        """Test execute_hard_onboarding when step 1 fails."""
        service = HardOnboardingService()
        mock_step1.return_value = False
        
        result = service.execute_hard_onboarding("Agent-1", "Message")
        
        assert result is False
        mock_step1.assert_called_once()


class TestHardOnboardAgent:
    """Tests for hard_onboard_agent convenience function."""

    @patch('src.services.hard_onboarding_service.HardOnboardingService')
    def test_hard_onboard_agent_success(self, mock_service_class):
        """Test hard_onboard_agent with successful onboarding."""
        mock_service = Mock()
        mock_service.execute_hard_onboarding.return_value = True
        mock_service_class.return_value = mock_service
        
        result = hard_onboard_agent("Agent-1", "Onboarding message", role="test_role")
        
        assert result is True
        mock_service.execute_hard_onboarding.assert_called_once_with(
            "Agent-1", "Onboarding message", role="test_role"
        )

    @patch('src.services.hard_onboarding_service.HardOnboardingService')
    def test_hard_onboard_agent_failure(self, mock_service_class):
        """Test hard_onboard_agent when onboarding fails."""
        mock_service = Mock()
        mock_service.execute_hard_onboarding.side_effect = Exception("Onboarding error")
        mock_service_class.return_value = mock_service
        
        result = hard_onboard_agent("Agent-1", "Message")
        
        assert result is False


class TestHardOnboardMultipleAgents:
    """Tests for hard_onboard_multiple_agents function."""

    @patch('src.services.hard_onboarding_service.time.sleep')
    @patch('src.services.hard_onboarding_service.HardOnboardingService')
    def test_hard_onboard_multiple_agents_success(self, mock_service_class, mock_sleep):
        """Test hard_onboard_multiple_agents with successful onboarding."""
        mock_service = Mock()
        mock_service.execute_hard_onboarding.side_effect = [True, True, False]
        mock_service_class.return_value = mock_service
        
        agents = [("Agent-1", "Message 1"), ("Agent-2", "Message 2"), ("Agent-3", "Message 3")]
        results = hard_onboard_multiple_agents(agents, role="test_role")
        
        assert results == {"Agent-1": True, "Agent-2": True, "Agent-3": False}
        assert mock_service.execute_hard_onboarding.call_count == 3
        assert mock_sleep.call_count == 3  # Sleep between each agent

    @patch('src.services.hard_onboarding_service.time.sleep')
    @patch('src.services.hard_onboarding_service.HardOnboardingService')
    def test_hard_onboard_multiple_agents_with_role(self, mock_service_class, mock_sleep):
        """Test hard_onboard_multiple_agents with role assignment."""
        mock_service = Mock()
        mock_service.execute_hard_onboarding.return_value = True
        mock_service_class.return_value = mock_service
        
        agents = [("Agent-1", "Message 1")]
        results = hard_onboard_multiple_agents(agents, role="test_role")
        
        assert results == {"Agent-1": True}
        mock_service.execute_hard_onboarding.assert_called_once_with(
            "Agent-1", "Message 1", role="test_role"
        )

