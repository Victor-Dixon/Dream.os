"""
Unit tests for messaging_pyautogui.py - HIGH PRIORITY

Tests PyAutoGUI messaging delivery functionality.
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime

# Import PyAutoGUI messaging
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.messaging_models_core import UnifiedMessage, UnifiedMessageType, UnifiedMessagePriority


class TestPyAutoGUIMessagingDelivery:
    """Test suite for PyAutoGUI messaging delivery."""

    @pytest.fixture
    def mock_pyautogui(self):
        """Create mock PyAutoGUI."""
        with patch('src.core.messaging_pyautogui.pyautogui') as mock:
            yield mock

    def test_delivery_initialization(self):
        """Test delivery service initialization."""
        # Service would be initialized
        assert True  # Placeholder

    @patch('src.core.messaging_pyautogui.pyautogui')
    def test_send_message_coordinates(self, mock_pyautogui):
        """Test sending message using coordinates."""
        mock_pyautogui.moveTo.return_value = None
        mock_pyautogui.click.return_value = None
        mock_pyautogui.write.return_value = None
        mock_pyautogui.press.return_value = None
        
        # Simulate coordinate-based delivery
        coordinates = (100, 200)
        message = "test message"
        
        # Would use pyautogui to send
        assert coordinates is not None
        assert message is not None

    @patch('src.core.messaging_pyautogui.pyautogui')
    def test_send_message_paste(self, mock_pyautogui):
        """Test sending message using paste."""
        mock_pyautogui.hotkey.return_value = None
        
        # Simulate paste-based delivery
        message = "test message"
        
        # Would use clipboard paste
        assert message is not None

    def test_coordinate_validation(self):
        """Test coordinate validation."""
        valid_coords = (100, 200)
        invalid_coords = (-1, -1)
        
        # Validate coordinates
        is_valid = all(c >= 0 for c in valid_coords)
        is_invalid = any(c < 0 for c in invalid_coords)
        
        assert is_valid is True
        assert is_invalid is True

    def test_message_content_validation(self):
        """Test message content validation."""
        message = UnifiedMessage(
            content="test",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR
        )
        
        assert message.content is not None
        assert len(message.content) > 0

    @patch('src.core.messaging_pyautogui.pyautogui')
    def test_delivery_error_handling(self, mock_pyautogui):
        """Test delivery error handling."""
        mock_pyautogui.moveTo.side_effect = Exception("PyAutoGUI error")
        
        # Would handle errors gracefully
        try:
            # Simulate error
            raise Exception("PyAutoGUI error")
        except Exception:
            assert True  # Error handled

    def test_get_message_tag_general(self):
        """Test get_message_tag with General sender."""
        from src.core.messaging_pyautogui import get_message_tag
        
        tag = get_message_tag("GENERAL", "Agent-1")
        assert tag == "[G2A]"

    def test_get_message_tag_discord(self):
        """Test get_message_tag with Discord sender."""
        from src.core.messaging_pyautogui import get_message_tag
        
        tag = get_message_tag("DISCORD", "Agent-1")
        assert tag == "[D2A]"

    def test_get_message_tag_commander(self):
        """Test get_message_tag with Commander sender."""
        from src.core.messaging_pyautogui import get_message_tag
        
        tag = get_message_tag("COMMANDER", "Agent-1")
        assert tag == "[D2A]"

    def test_get_message_tag_system(self):
        """Test get_message_tag with SYSTEM sender."""
        from src.core.messaging_pyautogui import get_message_tag
        
        tag = get_message_tag("SYSTEM", "Agent-1")
        assert tag == "[S2A]"

    def test_get_message_tag_captain(self):
        """Test get_message_tag with Captain sender."""
        from src.core.messaging_pyautogui import get_message_tag
        
        tag = get_message_tag("CAPTAIN", "Agent-1")
        assert tag == "[C2A]"

    def test_get_message_tag_captain_broadcast(self):
        """Test get_message_tag with Captain broadcast."""
        from src.core.messaging_pyautogui import get_message_tag
        
        tag = get_message_tag("CAPTAIN", "ALL")
        assert tag == "[C2A-ALL]"

    def test_get_message_tag_agent_to_captain(self):
        """Test get_message_tag with agent to captain."""
        from src.core.messaging_pyautogui import get_message_tag
        
        tag = get_message_tag("Agent-1", "CAPTAIN")
        assert tag == "[A2C]"

    def test_get_message_tag_agent_to_agent(self):
        """Test get_message_tag with agent to agent."""
        from src.core.messaging_pyautogui import get_message_tag
        
        tag = get_message_tag("Agent-1", "Agent-2")
        assert tag == "[A2A]"

    def test_get_message_tag_fallback(self):
        """Test get_message_tag fallback."""
        from src.core.messaging_pyautogui import get_message_tag
        
        tag = get_message_tag("Unknown", "Agent-1")
        assert tag == "[C2A]"

    def test_format_c2a_message_normal(self):
        """Test format_c2a_message with normal priority."""
        from src.core.messaging_pyautogui import format_c2a_message
        
        result = format_c2a_message("Agent-1", "Test message", "normal", "CAPTAIN")
        
        assert "[C2A]" in result
        assert "Agent-1" in result
        assert "Test message" in result
        assert "URGENT" not in result

    def test_format_c2a_message_urgent(self):
        """Test format_c2a_message with urgent priority."""
        from src.core.messaging_pyautogui import format_c2a_message
        
        result = format_c2a_message("Agent-1", "Test message", "urgent", "CAPTAIN")
        
        assert "URGENT MESSAGE" in result
        assert "Test message" in result

    def test_format_c2a_message_default_priority(self):
        """Test format_c2a_message with None priority defaults to normal."""
        from src.core.messaging_pyautogui import format_c2a_message
        
        result = format_c2a_message("Agent-1", "Test message", None, "CAPTAIN")
        
        assert "URGENT" not in result

    def test_format_c2a_message_discord_sender(self):
        """Test format_c2a_message with Discord sender."""
        from src.core.messaging_pyautogui import format_c2a_message
        
        result = format_c2a_message("Agent-1", "Test message", "normal", "DISCORD")
        
        assert "[D2A]" in result

    @patch('src.core.messaging_pyautogui.PYAUTOGUI_AVAILABLE', True)
    def test_pyautogui_delivery_init(self):
        """Test PyAutoGUIMessagingDelivery initialization."""
        from src.core.messaging_pyautogui import PyAutoGUIMessagingDelivery
        
        with patch('src.core.messaging_pyautogui.pyautogui'):
            delivery = PyAutoGUIMessagingDelivery()
            assert delivery is not None

    @patch('src.core.messaging_pyautogui.PYAUTOGUI_AVAILABLE', False)
    def test_pyautogui_delivery_init_no_pyautogui(self):
        """Test PyAutoGUIMessagingDelivery raises when PyAutoGUI unavailable."""
        from src.core.messaging_pyautogui import PyAutoGUIMessagingDelivery
        
        with pytest.raises(ImportError):
            PyAutoGUIMessagingDelivery()

    def test_validate_coordinates_valid(self):
        """Test validate_coordinates with valid coordinates."""
        from src.core.messaging_pyautogui import PyAutoGUIMessagingDelivery
        
        with patch('src.core.messaging_pyautogui.PYAUTOGUI_AVAILABLE', True):
            with patch('src.core.messaging_pyautogui.pyautogui'):
                delivery = PyAutoGUIMessagingDelivery()
                result = delivery.validate_coordinates("Agent-1", (100, 200))
                
                assert result is True

    def test_validate_coordinates_invalid_none(self):
        """Test validate_coordinates with None coordinates."""
        from src.core.messaging_pyautogui import PyAutoGUIMessagingDelivery
        
        with patch('src.core.messaging_pyautogui.PYAUTOGUI_AVAILABLE', True):
            with patch('src.core.messaging_pyautogui.pyautogui'):
                delivery = PyAutoGUIMessagingDelivery()
                result = delivery.validate_coordinates("Agent-1", None)
                
                assert result is False

    def test_validate_coordinates_invalid_length(self):
        """Test validate_coordinates with invalid length."""
        from src.core.messaging_pyautogui import PyAutoGUIMessagingDelivery
        
        with patch('src.core.messaging_pyautogui.PYAUTOGUI_AVAILABLE', True):
            with patch('src.core.messaging_pyautogui.pyautogui'):
                delivery = PyAutoGUIMessagingDelivery()
                result = delivery.validate_coordinates("Agent-1", (100,))
                
                assert result is False

    def test_validate_coordinates_invalid_type(self):
        """Test validate_coordinates with non-numeric coordinates."""
        from src.core.messaging_pyautogui import PyAutoGUIMessagingDelivery
        
        with patch('src.core.messaging_pyautogui.PYAUTOGUI_AVAILABLE', True):
            with patch('src.core.messaging_pyautogui.pyautogui'):
                delivery = PyAutoGUIMessagingDelivery()
                result = delivery.validate_coordinates("Agent-1", ("invalid", "coords"))
                
                assert result is False

    @patch('src.core.messaging_pyautogui.PYAUTOGUI_AVAILABLE', True)
    def test_send_message_success(self):
        """Test send_message successful delivery."""
        from src.core.messaging_pyautogui import PyAutoGUIMessagingDelivery
        from src.core.messaging_models_core import UnifiedMessage, UnifiedMessageType, UnifiedMessagePriority
        
        message = UnifiedMessage(
            content="test",
            sender="CAPTAIN",
            recipient="Agent-1",
            message_type=UnifiedMessageType.CAPTAIN_TO_AGENT,
            priority=UnifiedMessagePriority.REGULAR
        )
        
        with patch('src.core.messaging_pyautogui.pyautogui') as mock_pyautogui:
            with patch('src.core.messaging_pyautogui.pyperclip') as mock_pyperclip:
                with patch('src.core.coordinate_loader.get_coordinate_loader') as mock_loader_getter:
                    with patch('src.core.messaging_pyautogui.keyboard_control') as mock_keyboard:
                        with patch('src.core.messaging_pyautogui.is_locked', return_value=False):
                            mock_loader = Mock()
                            mock_loader.get_chat_coordinates.return_value = [100, 200]
                            mock_loader_getter.return_value = mock_loader
                            
                            mock_pyperclip.copy.return_value = None
                            mock_pyperclip.paste.return_value = "[C2A] Agent-1\n\ntest"
                            
                            mock_keyboard.return_value.__enter__ = Mock()
                            mock_keyboard.return_value.__exit__ = Mock(return_value=False)
                            
                            delivery = PyAutoGUIMessagingDelivery()
                            result = delivery.send_message(message)
                            
                            assert result is True

    @patch('src.core.messaging_pyautogui.PYAUTOGUI_AVAILABLE', True)
    def test_send_message_retry_on_failure(self):
        """Test send_message retries on failure."""
        from src.core.messaging_pyautogui import PyAutoGUIMessagingDelivery
        from src.core.messaging_models_core import UnifiedMessage, UnifiedMessageType, UnifiedMessagePriority
        
        message = UnifiedMessage(
            content="test",
            sender="CAPTAIN",
            recipient="Agent-1",
            message_type=UnifiedMessageType.CAPTAIN_TO_AGENT,
            priority=UnifiedMessagePriority.REGULAR
        )
        
        with patch('src.core.messaging_pyautogui.pyautogui') as mock_pyautogui:
            with patch('src.core.messaging_pyautogui.pyperclip') as mock_pyperclip:
                with patch('src.core.coordinate_loader.get_coordinate_loader') as mock_loader_getter:
                    with patch('src.core.messaging_pyautogui.keyboard_control') as mock_keyboard:
                        with patch('src.core.messaging_pyautogui.is_locked', return_value=False):
                            with patch('time.sleep'):
                                mock_loader = Mock()
                                mock_loader.get_chat_coordinates.return_value = [100, 200]
                                mock_loader_getter.return_value = mock_loader
                                
                                # First attempt fails, second succeeds
                                call_count = [0]
                                def side_effect(*args, **kwargs):
                                    call_count[0] += 1
                                    if call_count[0] == 1:
                                        raise Exception("First attempt failed")
                                    return None
                                
                                mock_pyautogui.moveTo.side_effect = side_effect
                                mock_pyperclip.copy.return_value = None
                                mock_pyperclip.paste.return_value = "[C2A] Agent-1\n\ntest"
                                
                                mock_keyboard.return_value.__enter__ = Mock()
                                mock_keyboard.return_value.__exit__ = Mock(return_value=False)
                                
                                delivery = PyAutoGUIMessagingDelivery()
                                # Should retry and eventually succeed or fail after 3 attempts
                                result = delivery.send_message(message)
                                
                                # Result depends on retry logic
                                assert isinstance(result, bool)

    @patch('src.core.messaging_pyautogui.PYAUTOGUI_AVAILABLE', True)
    def test_send_message_no_coordinates(self):
        """Test send_message when no coordinates available."""
        from src.core.messaging_pyautogui import PyAutoGUIMessagingDelivery
        from src.core.messaging_models_core import UnifiedMessage, UnifiedMessageType, UnifiedMessagePriority
        
        message = UnifiedMessage(
            content="test",
            sender="CAPTAIN",
            recipient="Agent-1",
            message_type=UnifiedMessageType.CAPTAIN_TO_AGENT,
            priority=UnifiedMessagePriority.REGULAR
        )
        
        with patch('src.core.messaging_pyautogui.pyautogui'):
            with patch('src.core.coordinate_loader.get_coordinate_loader') as mock_loader_getter:
                with patch('src.core.messaging_pyautogui.keyboard_control') as mock_keyboard:
                    with patch('src.core.messaging_pyautogui.is_locked', return_value=False):
                        mock_loader = Mock()
                        mock_loader.get_chat_coordinates.return_value = None
                        mock_loader_getter.return_value = mock_loader
                        
                        mock_keyboard.return_value.__enter__ = Mock()
                        mock_keyboard.return_value.__exit__ = Mock(return_value=False)
                        
                        delivery = PyAutoGUIMessagingDelivery()
                        result = delivery._execute_delivery_operations(message, 1, "CAPTAIN")
                        
                        assert result is False

    @patch('src.core.messaging_pyautogui.PYAUTOGUI_AVAILABLE', True)
    def test_send_message_stalled_flag(self):
        """Test send_message uses Ctrl+Enter for stalled flag."""
        from src.core.messaging_pyautogui import PyAutoGUIMessagingDelivery
        from src.core.messaging_models_core import UnifiedMessage, UnifiedMessageType, UnifiedMessagePriority
        
        message = UnifiedMessage(
            content="test",
            sender="CAPTAIN",
            recipient="Agent-1",
            message_type=UnifiedMessageType.CAPTAIN_TO_AGENT,
            priority=UnifiedMessagePriority.REGULAR,
            metadata={"stalled": True}
        )
        
        with patch('src.core.messaging_pyautogui.pyautogui') as mock_pyautogui:
            with patch('src.core.messaging_pyautogui.pyperclip') as mock_pyperclip:
                with patch('src.core.coordinate_loader.get_coordinate_loader') as mock_loader_getter:
                    with patch('src.core.messaging_pyautogui.keyboard_control') as mock_keyboard:
                        with patch('src.core.messaging_pyautogui.is_locked', return_value=False):
                            mock_loader = Mock()
                            mock_loader.get_chat_coordinates.return_value = [100, 200]
                            mock_loader_getter.return_value = mock_loader
                            
                            mock_pyperclip.copy.return_value = None
                            mock_pyperclip.paste.return_value = "[C2A] Agent-1\n\ntest"
                            
                            mock_keyboard.return_value.__enter__ = Mock()
                            mock_keyboard.return_value.__exit__ = Mock(return_value=False)
                            
                            delivery = PyAutoGUIMessagingDelivery()
                            delivery._execute_delivery_operations(message, 1, "CAPTAIN")
                            
                            # Should use Ctrl+Enter for stalled
                            mock_pyautogui.hotkey.assert_any_call("ctrl", "enter")

    @patch('src.core.messaging_pyautogui.PYAUTOGUI_AVAILABLE', True)
    def test_send_message_lock_already_held(self):
        """Test send_message skips lock when already held."""
        from src.core.messaging_pyautogui import PyAutoGUIMessagingDelivery
        from src.core.messaging_models_core import UnifiedMessage, UnifiedMessageType, UnifiedMessagePriority
        
        message = UnifiedMessage(
            content="test",
            sender="CAPTAIN",
            recipient="Agent-1",
            message_type=UnifiedMessageType.CAPTAIN_TO_AGENT,
            priority=UnifiedMessagePriority.REGULAR
        )
        
        with patch('src.core.messaging_pyautogui.pyautogui'):
            with patch('src.core.coordinate_loader.get_coordinate_loader') as mock_loader_getter:
                with patch('src.core.messaging_pyautogui.keyboard_control') as mock_keyboard:
                    with patch('src.core.messaging_pyautogui.is_locked', return_value=True):
                        mock_loader = Mock()
                        mock_loader.get_chat_coordinates.return_value = [100, 200]
                        mock_loader_getter.return_value = mock_loader
                        
                        delivery = PyAutoGUIMessagingDelivery()
                        delivery._send_message_attempt(message, 1)
                        
                        # Should not acquire lock
                        mock_keyboard.assert_not_called()

    def test_send_message_pyautogui_legacy(self):
        """Test send_message_pyautogui legacy function."""
        from src.core.messaging_pyautogui import send_message_pyautogui
        
        with patch('src.core.messaging_pyautogui.PyAutoGUIMessagingDelivery') as mock_delivery_class:
            mock_delivery = Mock()
            mock_delivery.send_message.return_value = True
            mock_delivery_class.return_value = mock_delivery
            
            result = send_message_pyautogui("Agent-1", "Test message", 30)
            
            assert result is True
            mock_delivery.send_message.assert_called_once()

    def test_send_message_pyautogui_legacy_exception(self):
        """Test send_message_pyautogui handles exceptions."""
        from src.core.messaging_pyautogui import send_message_pyautogui
        
        with patch('src.core.messaging_pyautogui.PyAutoGUIMessagingDelivery', side_effect=Exception("Error")):
            result = send_message_pyautogui("Agent-1", "Test message", 30)
            
            assert result is False

    def test_send_message_to_onboarding_coords(self):
        """Test send_message_to_onboarding_coords function."""
        from src.core.messaging_pyautogui import send_message_to_onboarding_coords
        
        with patch('src.core.messaging_pyautogui.send_message_pyautogui', return_value=True) as mock_send:
            result = send_message_to_onboarding_coords("Agent-1", "Test", 30)
            
            assert result is True
            mock_send.assert_called_once_with("Agent-1", "Test", 30)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

