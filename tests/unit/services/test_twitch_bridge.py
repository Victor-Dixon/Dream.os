"""
Unit tests for twitch_bridge.py

Target: ≥85% coverage, 15+ test methods
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))


class TestTwitchChatBridge:
    """Test suite for TwitchChatBridge."""

    @pytest.fixture
    def bridge_config(self):
        """Create bridge configuration."""
        return {
            "username": "test_bot",
            "oauth_token": "oauth:test_token",
            "channel": "test_channel"
        }

    @patch('src.services.chat_presence.twitch_bridge.IRC_AVAILABLE', True)
    def test_bridge_initialization(self, bridge_config):
        """Test bridge initializes correctly."""
        with patch('src.services.chat_presence.twitch_bridge.TwitchIRCBot'):
            from src.services.chat_presence.twitch_bridge import TwitchChatBridge
            bridge = TwitchChatBridge(**bridge_config)
            
            assert bridge.username == "test_bot"
            assert bridge.channel == "#test_channel"

    @patch('src.services.chat_presence.twitch_bridge.IRC_AVAILABLE', False)
    def test_bridge_initialization_no_irc(self, bridge_config):
        """Test bridge raises error when IRC not available."""
        with pytest.raises(ImportError):
            from src.services.chat_presence.twitch_bridge import TwitchChatBridge
            TwitchChatBridge(**bridge_config)

