"""
Unit tests for messaging_service_legacy (if exists) or legacy messaging patterns
Target: ≥85% coverage

Note: messaging_service_legacy.py doesn't exist in the codebase.
This test file covers legacy messaging patterns and compatibility functions.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock


class TestLegacyMessagingPatterns:
    """Tests for legacy messaging patterns and compatibility."""

    def test_unified_messaging_service_backward_compatibility(self):
        """Test UnifiedMessagingService provides backward compatibility."""
        from src.services.unified_messaging_service import UnifiedMessagingService, MessagingService
        
        # Verify alias exists
        assert MessagingService == UnifiedMessagingService

    def test_messaging_core_legacy_functions(self):
        """Test legacy compatibility functions in messaging_core."""
        from src.core.messaging_core import get_messaging_logger
        
        logger = get_messaging_logger()
        assert logger is not None

    def test_legacy_send_message_pattern(self):
        """Test legacy send_message pattern compatibility."""
        from src.core.messaging_core import send_message
        from src.core.messaging_models_core import UnifiedMessageType, UnifiedMessagePriority
        
        # Legacy pattern: send_message(content, sender, recipient, message_type)
        # Should still work
        with patch('src.core.messaging_core.messaging_core') as mock_core:
            mock_core.send_message.return_value = True
            result = send_message(
                content="test",
                sender="Agent-1",
                recipient="Agent-2",
                message_type=UnifiedMessageType.TEXT
            )
            assert isinstance(result, bool)

    def test_legacy_broadcast_pattern(self):
        """Test legacy broadcast pattern compatibility."""
        from src.core.messaging_core import broadcast_message
        from src.core.messaging_models_core import UnifiedMessagePriority
        
        # Legacy pattern: broadcast_message(content, sender)
        with patch('src.core.messaging_core.messaging_core') as mock_core:
            mock_core.broadcast_message.return_value = True
            result = broadcast_message(
                content="broadcast",
                sender="Agent-1"
            )
            assert isinstance(result, bool)

    def test_consolidated_messaging_service_legacy_interface(self):
        """Test ConsolidatedMessagingService maintains legacy interface."""
        from src.services.messaging_infrastructure import ConsolidatedMessagingService
        
        service = ConsolidatedMessagingService()
        
        # Legacy interface: send_message(agent, message, priority, use_pyautogui)
        assert hasattr(service, 'send_message')
        assert hasattr(service, 'broadcast_message')

    def test_discord_integration_legacy_functions(self):
        """Test Discord integration legacy functions."""
        from src.services.messaging_infrastructure import send_discord_message, broadcast_discord_message
        
        # Legacy functions should exist
        assert callable(send_discord_message)
        assert callable(broadcast_discord_message)

    def test_message_coordinator_legacy_methods(self):
        """Test MessageCoordinator legacy static methods."""
        from src.services.messaging_infrastructure import MessageCoordinator
        
        # Legacy static methods
        assert hasattr(MessageCoordinator, 'send_to_agent')
        assert hasattr(MessageCoordinator, 'broadcast_to_all')
        assert callable(MessageCoordinator.send_to_agent)
        assert callable(MessageCoordinator.broadcast_to_all)

    def test_legacy_message_handlers(self):
        """Test legacy message handler functions."""
        from src.services.messaging_handlers import handle_message, handle_broadcast
        
        # Legacy handlers should exist
        assert callable(handle_message)
        assert callable(handle_broadcast)

    def test_legacy_onboarding_message_generation(self):
        """Test legacy onboarding message generation."""
        from src.core.messaging_core import generate_onboarding_message
        
        # Legacy function should exist
        assert callable(generate_onboarding_message)
        
        with patch('src.core.messaging_core.messaging_core') as mock_core:
            mock_core.generate_onboarding_message.return_value = "Welcome"
            result = generate_onboarding_message("Agent-1", "standard")
            assert isinstance(result, str)

    def test_legacy_message_history(self):
        """Test legacy message history function."""
        from src.core.messaging_core import show_message_history
        
        # Legacy function should exist
        assert callable(show_message_history)
        
        with patch('src.core.messaging_core.messaging_core') as mock_core:
            # Should not raise exception
            show_message_history()

    def test_legacy_agent_listing(self):
        """Test legacy agent listing function."""
        from src.core.messaging_core import list_agents
        
        # Legacy function should exist
        assert callable(list_agents)
        
        with patch('src.core.messaging_core.messaging_core') as mock_core:
            # Should not raise exception
            list_agents()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

