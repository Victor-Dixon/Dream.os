#!/usr/bin/env python3
"""
Unit Tests for Mock Unified Messaging Core
==========================================
"""

import pytest
from unittest.mock import MagicMock, patch
from src.core.mock_unified_messaging_core import (
    MockDeliveryConfig,
    MockDeliveryResult,
    MockUnifiedMessagingCore,
    get_mock_messaging_core,
)


class TestMockDeliveryConfig:
    """Tests for MockDeliveryConfig dataclass."""

    def test_default_config(self):
        """Test default configuration values."""
        config = MockDeliveryConfig()
        assert config.min_latency_ms == 1
        assert config.max_latency_ms == 10
        assert config.success_rate == 0.95
        assert config.chaos_mode is False

    def test_custom_config(self):
        """Test custom configuration."""
        config = MockDeliveryConfig(
            min_latency_ms=5,
            max_latency_ms=20,
            success_rate=0.90,
            chaos_mode=True,
        )
        assert config.min_latency_ms == 5
        assert config.max_latency_ms == 20
        assert config.success_rate == 0.90
        assert config.chaos_mode is True


class TestMockDeliveryResult:
    """Tests for MockDeliveryResult dataclass."""

    def test_success_result(self):
        """Test successful delivery result."""
        from datetime import datetime
        result = MockDeliveryResult(
            success=True,
            latency_ms=5.0,
            timestamp=datetime.now(),
        )
        assert result.success is True
        assert result.latency_ms == 5.0

    def test_failure_result(self):
        """Test failed delivery result."""
        from datetime import datetime
        result = MockDeliveryResult(
            success=False,
            latency_ms=10.0,
            timestamp=datetime.now(),
            error_message="Test error",
        )
        assert result.success is False
        assert result.error_message == "Test error"


class TestMockUnifiedMessagingCore:
    """Tests for MockUnifiedMessagingCore."""

    def test_initialization(self):
        """Test core initialization."""
        core = MockUnifiedMessagingCore()
        assert core.config is not None
        assert core._delivery_stats["total_deliveries"] == 0

    def test_initialization_with_config(self):
        """Test initialization with custom config."""
        config = MockDeliveryConfig(success_rate=0.99)
        core = MockUnifiedMessagingCore(config)
        assert core.config.success_rate == 0.99

    def test_send_message_disabled(self):
        """Test sending when disabled."""
        config = MockDeliveryConfig(enabled=False)
        core = MockUnifiedMessagingCore(config)
        result = core.send_message("test", "sender", "recipient")
        assert result is False

    @patch('src.core.mock_unified_messaging_core.random.random')
    @patch('src.core.mock_unified_messaging_core.time.sleep')
    def test_send_message_success(self, mock_sleep, mock_random):
        """Test successful message send."""
        mock_random.return_value = 0.5  # Below success rate
        core = MockUnifiedMessagingCore()
        result = core.send_message("test", "sender", "recipient")
        assert result is True
        assert core._delivery_stats["total_deliveries"] == 1
        assert core._delivery_stats["successful_deliveries"] == 1

    @patch('src.core.mock_unified_messaging_core.random.random')
    @patch('src.core.mock_unified_messaging_core.time.sleep')
    def test_send_message_failure(self, mock_sleep, mock_random):
        """Test failed message send."""
        mock_random.side_effect = [0.5, 0.99]  # Success check fails
        core = MockUnifiedMessagingCore(MockDeliveryConfig(success_rate=0.5))
        result = core.send_message("test", "sender", "recipient")
        assert result is False
        assert core._delivery_stats["failed_deliveries"] == 1

    def test_get_stats_empty(self):
        """Test getting stats with no deliveries."""
        core = MockUnifiedMessagingCore()
        stats = core.get_stats()
        assert stats["total_deliveries"] == 0
        assert stats["success_rate"] == 0.0

    @patch('src.core.mock_unified_messaging_core.random.random')
    @patch('src.core.mock_unified_messaging_core.time.sleep')
    def test_get_stats_with_deliveries(self, mock_sleep, mock_random):
        """Test getting stats after deliveries."""
        mock_random.return_value = 0.5  # Always succeeds
        core = MockUnifiedMessagingCore()
        core.send_message("test1", "sender", "recipient")
        core.send_message("test2", "sender", "recipient")
        stats = core.get_stats()
        assert stats["total_deliveries"] == 2
        assert stats["successful_deliveries"] == 2

    def test_reset_stats(self):
        """Test resetting statistics."""
        core = MockUnifiedMessagingCore()
        core._delivery_stats["total_deliveries"] = 10
        core.reset_stats()
        assert core._delivery_stats["total_deliveries"] == 0

    def test_configure(self):
        """Test configuration update."""
        core = MockUnifiedMessagingCore()
        core.configure(success_rate=0.99, min_latency_ms=5)
        assert core.config.success_rate == 0.99
        assert core.config.min_latency_ms == 5

    def test_send_message_object(self):
        """Test sending message object."""
        core = MockUnifiedMessagingCore()
        mock_message = MagicMock()
        mock_message.content = "test"
        mock_message.sender = "sender"
        mock_message.recipient = "recipient"
        with patch.object(core, 'send_message', return_value=True) as mock_send:
            result = core.send_message_object(mock_message)
            assert result is True
            mock_send.assert_called_once()


class TestGetMockMessagingCore:
    """Tests for get_mock_messaging_core function."""

    def test_get_mock_core_singleton(self):
        """Test that function returns singleton instance."""
        # Reset global instance
        import src.core.mock_unified_messaging_core as mock_module
        mock_module._mock_core_instance = None
        
        core1 = get_mock_messaging_core()
        core2 = get_mock_messaging_core()
        assert core1 is core2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

