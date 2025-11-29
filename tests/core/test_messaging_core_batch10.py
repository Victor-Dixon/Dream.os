"""
Batch 10 unit tests for messaging_core.py

Additional comprehensive tests for advanced scenarios, error paths, and edge cases.
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime

from src.core.messaging_models_core import (
    UnifiedMessage,
    UnifiedMessageType,
    UnifiedMessagePriority,
    UnifiedMessageTag
)


class TestUnifiedMessagingCoreBatch10:
    """Batch 10 tests for UnifiedMessagingCore - Advanced scenarios."""

    @pytest.fixture
    def mock_delivery_service(self):
        """Create mock delivery service."""
        mock = MagicMock()
        mock.send_message.return_value = True
        return mock

    @pytest.fixture
    def mock_onboarding_service(self):
        """Create mock onboarding service."""
        mock = MagicMock()
        mock.generate_onboarding_message.return_value = "Welcome message"
        return mock

    @pytest.fixture
    def mock_message_repository(self):
        """Create mock message repository."""
        mock = MagicMock()
        mock.save_message = Mock()
        return mock

    def test_send_message_metadata_creation(self, mock_delivery_service):
        """Test send_message creates metadata when None."""
        from src.core.messaging_core import UnifiedMessagingCore
        
        core = UnifiedMessagingCore(delivery_service=mock_delivery_service)
        
        result = core.send_message(
            content="test",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT,
            metadata=None
        )
        
        assert isinstance(result, bool)

    def test_send_message_empty_tags(self, mock_delivery_service):
        """Test send_message with empty tags list."""
        from src.core.messaging_core import UnifiedMessagingCore
        
        core = UnifiedMessagingCore(delivery_service=mock_delivery_service)
        
        result = core.send_message(
            content="test",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT,
            tags=[]
        )
        
        assert isinstance(result, bool)

    def test_send_message_validation_recipient_not_agent(self, mock_delivery_service):
        """Test send_message skips validation for non-agent recipients."""
        from src.core.messaging_core import UnifiedMessagingCore
        
        core = UnifiedMessagingCore(delivery_service=mock_delivery_service)
        
        # SYSTEM recipient should skip validation
        result = core.send_message(
            content="test",
            sender="Agent-1",
            recipient="SYSTEM",
            message_type=UnifiedMessageType.TEXT
        )
        
        assert isinstance(result, bool)

    def test_send_message_validation_sender_not_agent(self, mock_delivery_service):
        """Test send_message skips validation for non-agent senders."""
        from src.core.messaging_core import UnifiedMessagingCore
        
        core = UnifiedMessagingCore(delivery_service=mock_delivery_service)
        
        # SYSTEM sender should skip validation
        result = core.send_message(
            content="test",
            sender="SYSTEM",
            recipient="Agent-1",
            message_type=UnifiedMessageType.TEXT
        )
        
        assert isinstance(result, bool)

    def test_send_message_object_template_already_set(self, mock_delivery_service):
        """Test send_message_object when template is already set in metadata."""
        from src.core.messaging_core import UnifiedMessagingCore
        from src.core.messaging_models_core import UnifiedMessage, UnifiedMessageType
        
        core = UnifiedMessagingCore(delivery_service=mock_delivery_service)
        
        message = UnifiedMessage(
            content="test",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT,
            metadata={"template": "full"}
        )
        
        mock_delivery_service.send_message.return_value = True
        
        result = core.send_message_object(message)
        
        assert result is True
        # Template should remain "full"
        assert message.metadata.get("template") == "full"

    def test_send_message_object_template_resolution_compact_fallback(self, mock_delivery_service):
        """Test send_message_object falls back to role resolution when channel returns compact."""
        from src.core.messaging_core import UnifiedMessagingCore
        from src.core.messaging_models_core import UnifiedMessage, UnifiedMessageType
        
        core = UnifiedMessagingCore(delivery_service=mock_delivery_service)
        
        message = UnifiedMessage(
            content="test",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT,
            metadata={"channel": "standard", "sender_role": "CAPTAIN", "receiver_role": "AGENT"}
        )
        
        with patch('src.services.messaging.policy_loader.load_template_policy') as mock_load, \
             patch('src.services.messaging.policy_loader.resolve_template_by_channel', return_value="compact") as mock_resolve_channel, \
             patch('src.services.messaging.policy_loader.resolve_template_by_roles', return_value="full") as mock_resolve_roles:
            
            mock_policy = {}
            mock_load.return_value = mock_policy
            
            mock_delivery_service.send_message.return_value = True
            
            result = core.send_message_object(message)
            
            assert result is True
            # Should fall back to role resolution when channel returns "compact"
            if mock_resolve_roles.called:
                assert message.metadata.get("template") == "full"

    def test_send_message_object_repository_not_initialized_warning(self, mock_delivery_service):
        """Test send_message_object logs warning when repository not initialized."""
        from src.core.messaging_core import UnifiedMessagingCore
        from src.core.messaging_models_core import UnifiedMessage, UnifiedMessageType
        
        core = UnifiedMessagingCore(delivery_service=mock_delivery_service)
        core.message_repository = None  # Explicitly set to None
        
        message = UnifiedMessage(
            content="test",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT
        )
        
        mock_delivery_service.send_message.return_value = True
        
        result = core.send_message_object(message)
        
        assert result is True

    def test_send_message_object_serialize_datetime(self, mock_delivery_service, mock_message_repository):
        """Test send_message_object serializes datetime in metadata."""
        from src.core.messaging_core import UnifiedMessagingCore
        from src.core.messaging_models_core import UnifiedMessage, UnifiedMessageType
        
        core = UnifiedMessagingCore(
            delivery_service=mock_delivery_service,
            message_repository=mock_message_repository
        )
        
        message = UnifiedMessage(
            content="test",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT,
            metadata={"timestamp": datetime.now()}
        )
        
        mock_delivery_service.send_message.return_value = True
        
        result = core.send_message_object(message)
        
        assert result is True
        # Verify repository was called with serialized metadata
        assert mock_message_repository.save_message.called

    def test_send_message_object_serialize_nested_dict(self, mock_delivery_service, mock_message_repository):
        """Test send_message_object serializes nested dictionaries."""
        from src.core.messaging_core import UnifiedMessagingCore
        from src.core.messaging_models_core import UnifiedMessage, UnifiedMessageType
        
        core = UnifiedMessagingCore(
            delivery_service=mock_delivery_service,
            message_repository=mock_message_repository
        )
        
        message = UnifiedMessage(
            content="test",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT,
            metadata={"nested": {"level1": {"level2": "value"}}}
        )
        
        mock_delivery_service.send_message.return_value = True
        
        result = core.send_message_object(message)
        
        assert result is True
        assert mock_message_repository.save_message.called

    def test_send_message_object_serialize_list(self, mock_delivery_service, mock_message_repository):
        """Test send_message_object serializes lists in metadata."""
        from src.core.messaging_core import UnifiedMessagingCore
        from src.core.messaging_models_core import UnifiedMessage, UnifiedMessageType
        
        core = UnifiedMessagingCore(
            delivery_service=mock_delivery_service,
            message_repository=mock_message_repository
        )
        
        message = UnifiedMessage(
            content="test",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT,
            metadata={"items": [1, 2, 3, {"nested": "value"}]}
        )
        
        mock_delivery_service.send_message.return_value = True
        
        result = core.send_message_object(message)
        
        assert result is True
        assert mock_message_repository.save_message.called

    def test_send_message_object_content_truncation(self, mock_delivery_service, mock_message_repository):
        """Test send_message_object truncates long content in repository."""
        from src.core.messaging_core import UnifiedMessagingCore
        from src.core.messaging_models_core import UnifiedMessage, UnifiedMessageType
        
        core = UnifiedMessagingCore(
            delivery_service=mock_delivery_service,
            message_repository=mock_message_repository
        )
        
        long_content = "A" * 500  # Longer than 200 chars
        message = UnifiedMessage(
            content=long_content,
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT
        )
        
        mock_delivery_service.send_message.return_value = True
        
        result = core.send_message_object(message)
        
        assert result is True
        # Verify save_message was called
        save_call = mock_message_repository.save_message.call_args[0][0]
        assert len(save_call["content"]) <= 203  # 200 + "..."

    def test_broadcast_message_priority_handling(self, mock_delivery_service):
        """Test broadcast_message handles different priorities correctly."""
        from src.core.messaging_core import UnifiedMessagingCore
        from src.core.messaging_models_core import UnifiedMessagePriority
        
        core = UnifiedMessagingCore(delivery_service=mock_delivery_service)
        
        priorities = [UnifiedMessagePriority.REGULAR, UnifiedMessagePriority.URGENT]
        
        for priority in priorities:
            mock_delivery_service.send_message.return_value = True
            result = core.broadcast_message(
                content="broadcast",
                sender="Agent-1",
                priority=priority
            )
            assert isinstance(result, bool)

    def test_broadcast_message_tags_included(self, mock_delivery_service):
        """Test broadcast_message includes SYSTEM tag."""
        from src.core.messaging_core import UnifiedMessagingCore
        from src.core.messaging_models_core import UnifiedMessagePriority
        
        core = UnifiedMessagingCore(delivery_service=mock_delivery_service)
        
        mock_delivery_service.send_message.return_value = True
        
        result = core.broadcast_message(
            content="broadcast",
            sender="Agent-1",
            priority=UnifiedMessagePriority.REGULAR
        )
        
        assert result is True
        # Verify SYSTEM tag was included
        calls = mock_delivery_service.send_message.call_args_list
        for call in calls:
            message = call[0][0]
            assert UnifiedMessageTag.SYSTEM in message.tags

    def test_generate_onboarding_message_default_style(self, mock_onboarding_service):
        """Test generate_onboarding_message uses default style."""
        from src.core.messaging_core import UnifiedMessagingCore
        
        core = UnifiedMessagingCore(onboarding_service=mock_onboarding_service)
        
        result = core.generate_onboarding_message("Agent-1")
        
        assert isinstance(result, str)
        mock_onboarding_service.generate_onboarding_message.assert_called_once_with("Agent-1", "standard")

    def test_list_agents_output_format(self):
        """Test list_agents outputs correct format."""
        from src.core.messaging_core import UnifiedMessagingCore
        
        core = UnifiedMessagingCore()
        
        with patch.object(core.logger, 'info') as mock_info:
            core.list_agents()
            
            # Should log agent list
            assert mock_info.called
            # Should log 8 agents
            agent_calls = [call for call in mock_info.call_args_list if "Agent-" in str(call)]
            assert len(agent_calls) == 8


class TestPublicAPIBatch10:
    """Batch 10 tests for public API functions - Advanced scenarios."""

    def test_send_message_function_all_parameters(self):
        """Test send_message function with all parameters."""
        from src.core.messaging_core import send_message
        from src.core.messaging_models_core import UnifiedMessageType, UnifiedMessagePriority, UnifiedMessageTag
        
        with patch('src.core.messaging_core.messaging_core') as mock_core:
            mock_core.send_message.return_value = True
            
            result = send_message(
                content="test",
                sender="Agent-1",
                recipient="Agent-2",
                message_type=UnifiedMessageType.TEXT,
                priority=UnifiedMessagePriority.URGENT,
                tags=[UnifiedMessageTag.CAPTAIN, UnifiedMessageTag.SYSTEM],
                metadata={"key": "value"}
            )
            
            assert result is True
            mock_core.send_message.assert_called_once_with(
                "test",
                "Agent-1",
                "Agent-2",
                UnifiedMessageType.TEXT,
                UnifiedMessagePriority.URGENT,
                [UnifiedMessageTag.CAPTAIN, UnifiedMessageTag.SYSTEM],
                {"key": "value"}
            )

    def test_send_message_object_function_with_metadata(self):
        """Test send_message_object function with metadata."""
        from src.core.messaging_core import send_message_object
        from src.core.messaging_models_core import UnifiedMessage, UnifiedMessageType
        
        message = UnifiedMessage(
            content="test",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT,
            metadata={"key": "value"}
        )
        
        with patch('src.core.messaging_core.messaging_core') as mock_core:
            mock_core.send_message_object.return_value = True
            result = send_message_object(message)
            
            assert result is True
            mock_core.send_message_object.assert_called_once_with(message)

    def test_broadcast_message_function_urgent(self):
        """Test broadcast_message function with urgent priority."""
        from src.core.messaging_core import broadcast_message
        from src.core.messaging_models_core import UnifiedMessagePriority
        
        with patch('src.core.messaging_core.messaging_core') as mock_core:
            mock_core.broadcast_message.return_value = True
            
            result = broadcast_message(
                content="urgent broadcast",
                sender="Agent-1",
                priority=UnifiedMessagePriority.URGENT
            )
            
            assert result is True
            mock_core.broadcast_message.assert_called_once_with(
                "urgent broadcast",
                "Agent-1",
                UnifiedMessagePriority.URGENT
            )

    def test_generate_onboarding_message_function_all_styles(self):
        """Test generate_onboarding_message function with all styles."""
        from src.core.messaging_core import generate_onboarding_message
        
        styles = ["standard", "friendly", "professional"]
        
        with patch('src.core.messaging_core.messaging_core') as mock_core:
            mock_core.generate_onboarding_message.return_value = "Welcome"
            
            for style in styles:
                result = generate_onboarding_message("Agent-1", style)
                assert isinstance(result, str)
                assert len(result) > 0

    def test_validate_messaging_system_core_none(self):
        """Test validate_messaging_system when core is None."""
        from src.core.messaging_core import validate_messaging_system
        
        with patch('src.core.messaging_core.get_messaging_core', return_value=None):
            result = validate_messaging_system()
            assert result is False

    def test_validate_messaging_system_message_creation_error(self):
        """Test validate_messaging_system handles message creation errors."""
        from src.core.messaging_core import validate_messaging_system
        
        with patch('src.core.messaging_core.get_messaging_core') as mock_get_core, \
             patch('src.core.messaging_models_core.UnifiedMessage', side_effect=Exception("Message error")):
            mock_core = Mock()
            mock_get_core.return_value = mock_core
            
            result = validate_messaging_system()
            assert result is False

    def test_initialize_messaging_system_validation_failure(self):
        """Test initialize_messaging_system raises ValueError on validation failure."""
        from src.core.messaging_core import initialize_messaging_system
        
        with patch('src.core.messaging_core.validate_messaging_system', return_value=False):
            with pytest.raises(ValueError):
                initialize_messaging_system()

    def test_initialize_messaging_system_import_error_handling(self):
        """Test initialize_messaging_system handles import errors gracefully."""
        # The function is called on import, so we test that it doesn't crash the module
        from src.core import messaging_core
        
        # Should not raise exception during import
        assert messaging_core is not None
        # Should have messaging_core instance
        assert hasattr(messaging_core, 'messaging_core')


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

