#!/usr/bin/env python3
"""
Unit Tests for Chat Presence Orchestrator
==========================================

Tests for chat presence orchestration system.
"""

import pytest
from unittest.mock import Mock, patch, AsyncMock, MagicMock
from typing import Optional

try:
    from src.services.chat_presence.chat_presence_orchestrator import ChatPresenceOrchestrator
    CHAT_PRESENCE_AVAILABLE = True
except ImportError:
    CHAT_PRESENCE_AVAILABLE = False


@pytest.mark.skipif(not CHAT_PRESENCE_AVAILABLE, reason="Chat presence orchestrator not available")
class TestChatPresenceOrchestrator:
    """Unit tests for Chat Presence Orchestrator."""

    def test_initialization(self):
        """Test orchestrator initialization."""
        orchestrator = ChatPresenceOrchestrator()
        
        assert orchestrator.message_interpreter is not None
        assert orchestrator.chat_scheduler is not None
        assert orchestrator.caption_interpreter is not None
        assert orchestrator.speech_log_manager is not None
        assert orchestrator.twitch_bridge is None
        assert orchestrator.obs_listener is None
        assert not orchestrator.running

    def test_initialization_with_config(self):
        """Test initialization with configuration."""
        twitch_config = {"channel": "test_channel", "token": "test_token"}
        obs_config = {"host": "localhost", "port": 4455}
        
        orchestrator = ChatPresenceOrchestrator(
            twitch_config=twitch_config,
            obs_config=obs_config
        )
        
        assert orchestrator.twitch_config == twitch_config
        assert orchestrator.obs_config == obs_config

    @pytest.mark.asyncio
    async def test_start_success(self):
        """Test successful start."""
        orchestrator = ChatPresenceOrchestrator()
        
        with patch('src.services.chat_presence.chat_presence_orchestrator.TwitchChatBridge') as mock_bridge_class:
            with patch('src.services.chat_presence.chat_presence_orchestrator.OBSCaptionListener') as mock_obs_class:
                mock_bridge = AsyncMock()
                mock_bridge.connect = AsyncMock(return_value=True)
                mock_bridge_class.return_value = mock_bridge
                
                mock_obs = AsyncMock()
                mock_obs_class.return_value = mock_obs
                
                result = await orchestrator.start()
                
                assert result is True
                assert orchestrator.running

    @pytest.mark.asyncio
    async def test_stop(self):
        """Test stop functionality."""
        orchestrator = ChatPresenceOrchestrator()
        orchestrator.running = True
        orchestrator.twitch_bridge = Mock()
        orchestrator.twitch_bridge.stop = Mock()
        orchestrator.obs_listener = AsyncMock()
        orchestrator.obs_listener.disconnect = AsyncMock()
        
        await orchestrator.stop()
        
        assert not orchestrator.running
        orchestrator.twitch_bridge.stop.assert_called_once()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

