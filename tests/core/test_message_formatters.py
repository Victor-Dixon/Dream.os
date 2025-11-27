"""
Unit tests for message_formatters.py - HIGH PRIORITY

Tests message formatting functions.
"""

import pytest
from datetime import datetime

# Import formatters
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.message_formatters import (
    format_message_full,
    format_message_compact,
    format_message_minimal,
    format_message
)


class TestMessageFormatters:
    """Test suite for message formatting functions."""

    def test_format_message_full(self):
        """Test formatting message with full details."""
        from src.core.messaging_models_core import UnifiedMessage, UnifiedMessageType, UnifiedMessagePriority
        
        message = UnifiedMessage(
            content="test message",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR
        )
        
        formatted = format_message_full(message)
        
        assert "Agent-1" in formatted or "test message" in formatted

    def test_format_message_compact(self):
        """Test formatting message in compact format."""
        from src.core.messaging_models_core import UnifiedMessage, UnifiedMessageType, UnifiedMessagePriority
        
        message = UnifiedMessage(
            content="test",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR
        )
        
        formatted = format_message_compact(message)
        
        assert message.content in formatted or message.sender in formatted

    def test_format_message_minimal(self):
        """Test formatting message in minimal format."""
        from src.core.messaging_models_core import UnifiedMessage, UnifiedMessageType, UnifiedMessagePriority
        
        message = UnifiedMessage(
            content="test",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR
        )
        
        formatted = format_message_minimal(message)
        
        assert message.content in formatted

    def test_format_message_with_template(self):
        """Test formatting message with template selection."""
        from src.core.messaging_models_core import UnifiedMessage, UnifiedMessageType, UnifiedMessagePriority
        
        message = UnifiedMessage(
            content="test",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR
        )
        
        # Test different templates
        full_formatted = format_message(message, template="full")
        compact_formatted = format_message(message, template="compact")
        minimal_formatted = format_message(message, template="minimal")
        
        assert message.content in full_formatted or message.content in compact_formatted or message.content in minimal_formatted


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

