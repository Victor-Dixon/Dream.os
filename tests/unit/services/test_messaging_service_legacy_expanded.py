"""
Expanded unit tests for messaging_service_legacy patterns - Batch 9

Additional tests for legacy messaging patterns and compatibility.
"""

import pytest
from unittest.mock import Mock, patch


class TestLegacyMessagingPatternsExpanded:
    """Expanded tests for legacy messaging patterns."""

    def test_legacy_send_message_all_message_types(self):
        """Test legacy send_message with all message types."""
        from src.core.messaging_core import send_message
        from src.core.messaging_models_core import UnifiedMessageType, UnifiedMessagePriority
        
        message_types = [
            UnifiedMessageType.TEXT,
            UnifiedMessageType.BROADCAST,
            UnifiedMessageType.ONBOARDING,
            UnifiedMessageType.AGENT_TO_AGENT,
            UnifiedMessageType.CAPTAIN_TO_AGENT,
            UnifiedMessageType.SYSTEM_TO_AGENT,
            UnifiedMessageType.HUMAN_TO_AGENT,
        ]
        
        with patch('src.core.messaging_core.messaging_core') as mock_core:
            mock_core.send_message.return_value = True
            
            for msg_type in message_types:
                result = send_message(
                    content="test",
                    sender="Agent-1",
                    recipient="Agent-2",
                    message_type=msg_type
                )
                assert isinstance(result, bool)

    def test_legacy_broadcast_all_priorities(self):
        """Test legacy broadcast with all priorities."""
        from src.core.messaging_core import broadcast_message
        from src.core.messaging_models_core import UnifiedMessagePriority
        
        priorities = [UnifiedMessagePriority.REGULAR, UnifiedMessagePriority.URGENT]
        
        with patch('src.core.messaging_core.messaging_core') as mock_core:
            mock_core.broadcast_message.return_value = True
            
            for priority in priorities:
                result = broadcast_message(
                    content="broadcast",
                    sender="Agent-1",
                    priority=priority
                )
                assert isinstance(result, bool)

    def test_legacy_generate_onboarding_all_styles(self):
        """Test legacy generate_onboarding_message with all styles."""
        from src.core.messaging_core import generate_onboarding_message
        
        styles = ["standard", "friendly", "professional"]
        
        with patch('src.core.messaging_core.messaging_core') as mock_core:
            mock_core.generate_onboarding_message.return_value = "Welcome"
            
            for style in styles:
                result = generate_onboarding_message("Agent-1", style)
                assert isinstance(result, str)
                assert len(result) > 0

    def test_legacy_send_message_with_all_tags(self):
        """Test legacy send_message with all tag combinations."""
        from src.core.messaging_core import send_message
        from src.core.messaging_models_core import UnifiedMessageType, UnifiedMessagePriority, UnifiedMessageTag
        
        tag_combinations = [
            [UnifiedMessageTag.CAPTAIN],
            [UnifiedMessageTag.ONBOARDING],
            [UnifiedMessageTag.WRAPUP],
            [UnifiedMessageTag.COORDINATION],
            [UnifiedMessageTag.SYSTEM],
            [UnifiedMessageTag.CAPTAIN, UnifiedMessageTag.SYSTEM],
        ]
        
        with patch('src.core.messaging_core.messaging_core') as mock_core:
            mock_core.send_message.return_value = True
            
            for tags in tag_combinations:
                result = send_message(
                    content="test",
                    sender="Agent-1",
                    recipient="Agent-2",
                    message_type=UnifiedMessageType.TEXT,
                    tags=tags
                )
                assert isinstance(result, bool)

    def test_legacy_send_message_with_metadata(self):
        """Test legacy send_message with various metadata."""
        from src.core.messaging_core import send_message
        from src.core.messaging_models_core import UnifiedMessageType
        
        metadata_variants = [
            {"key": "value"},
            {"channel": "onboarding"},
            {"sender_role": "CAPTAIN", "receiver_role": "AGENT"},
            {"template": "full"},
            {"nested": {"key": "value"}},
            {},
        ]
        
        with patch('src.core.messaging_core.messaging_core') as mock_core:
            mock_core.send_message.return_value = True
            
            for metadata in metadata_variants:
                result = send_message(
                    content="test",
                    sender="Agent-1",
                    recipient="Agent-2",
                    message_type=UnifiedMessageType.TEXT,
                    metadata=metadata
                )
                assert isinstance(result, bool)

    def test_consolidated_messaging_service_legacy_interface_methods(self):
        """Test ConsolidatedMessagingService has all legacy interface methods."""
        from src.services.messaging_infrastructure import ConsolidatedMessagingService
        
        service = ConsolidatedMessagingService()
        
        # Legacy interface methods
        assert hasattr(service, 'send_message')
        assert hasattr(service, 'broadcast_message')
        assert callable(service.send_message)
        assert callable(service.broadcast_message)

    def test_message_coordinator_legacy_static_methods(self):
        """Test MessageCoordinator has all legacy static methods."""
        from src.services.messaging_infrastructure import MessageCoordinator
        
        # Legacy static methods
        assert hasattr(MessageCoordinator, 'send_to_agent')
        assert hasattr(MessageCoordinator, 'broadcast_to_all')
        assert hasattr(MessageCoordinator, 'coordinate_survey')
        assert hasattr(MessageCoordinator, 'coordinate_consolidation')
        assert hasattr(MessageCoordinator, 'send_multi_agent_request')
        assert callable(MessageCoordinator.send_to_agent)
        assert callable(MessageCoordinator.broadcast_to_all)
        assert callable(MessageCoordinator.coordinate_survey)
        assert callable(MessageCoordinator.coordinate_consolidation)
        assert callable(MessageCoordinator.send_multi_agent_request)

    def test_legacy_message_handlers_all_functions(self):
        """Test all legacy message handler functions exist."""
        from src.services.messaging_handlers import handle_message, handle_broadcast
        
        # Legacy handlers should exist
        assert callable(handle_message)
        assert callable(handle_broadcast)

    def test_legacy_discord_integration_functions(self):
        """Test all legacy Discord integration functions exist."""
        from src.services.messaging_infrastructure import send_discord_message, broadcast_discord_message
        
        # Legacy functions should exist
        assert callable(send_discord_message)
        assert callable(broadcast_discord_message)

    def test_legacy_onboarding_message_generation_all_agents(self):
        """Test legacy onboarding message generation for all agents."""
        from src.core.messaging_core import generate_onboarding_message
        
        agents = ["Agent-1", "Agent-2", "Agent-3", "Agent-4", "Agent-5", "Agent-6", "Agent-7", "Agent-8"]
        
        with patch('src.core.messaging_core.messaging_core') as mock_core:
            mock_core.generate_onboarding_message.return_value = "Welcome"
            
            for agent in agents:
                result = generate_onboarding_message(agent, "standard")
                assert isinstance(result, str)
                assert len(result) > 0

    def test_legacy_message_history_function(self):
        """Test legacy message history function exists and works."""
        from src.core.messaging_core import show_message_history
        
        # Legacy function should exist
        assert callable(show_message_history)
        
        with patch('src.core.messaging_core.messaging_core') as mock_core:
            # Should not raise exception
            show_message_history()

    def test_legacy_agent_listing_function(self):
        """Test legacy agent listing function exists and works."""
        from src.core.messaging_core import list_agents
        
        # Legacy function should exist
        assert callable(list_agents)
        
        with patch('src.core.messaging_core.messaging_core') as mock_core:
            # Should not raise exception
            list_agents()

    def test_legacy_get_messaging_logger(self):
        """Test legacy get_messaging_logger function."""
        from src.core.messaging_core import get_messaging_logger
        
        logger = get_messaging_logger()
        assert logger is not None
        assert hasattr(logger, 'info')
        assert hasattr(logger, 'error')
        assert hasattr(logger, 'warning')

    def test_legacy_send_message_object_function(self):
        """Test legacy send_message_object function."""
        from src.core.messaging_core import send_message_object
        from src.core.messaging_models_core import UnifiedMessage, UnifiedMessageType
        
        message = UnifiedMessage(
            content="test",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT
        )
        
        with patch('src.core.messaging_core.messaging_core') as mock_core:
            mock_core.send_message_object.return_value = True
            result = send_message_object(message)
            assert isinstance(result, bool)

    def test_legacy_get_messaging_core_function(self):
        """Test legacy get_messaging_core function."""
        from src.core.messaging_core import get_messaging_core
        
        core = get_messaging_core()
        assert core is not None
        assert hasattr(core, 'send_message')
        assert hasattr(core, 'broadcast_message')
        assert hasattr(core, 'generate_onboarding_message')


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

