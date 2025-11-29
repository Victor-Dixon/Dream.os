#!/usr/bin/env python3
"""
Unit Tests for Message Interpreter
===================================

Tests for message interpretation and agent routing.
"""

import pytest
from unittest.mock import Mock, patch

try:
    from src.services.chat_presence.message_interpreter import MessageInterpreter
    MESSAGE_INTERPRETER_AVAILABLE = True
except ImportError:
    MESSAGE_INTERPRETER_AVAILABLE = False


@pytest.mark.skipif(not MESSAGE_INTERPRETER_AVAILABLE, reason="Message interpreter not available")
class TestMessageInterpreter:
    """Unit tests for Message Interpreter."""

    def test_initialization(self):
        """Test interpreter initialization."""
        interpreter = MessageInterpreter()
        
        assert interpreter.agent_activity == {}
        assert isinstance(interpreter.agent_activity, dict)

    def test_determine_responder_explicit_command(self):
        """Test explicit agent command detection."""
        interpreter = MessageInterpreter()
        
        result = interpreter.determine_responder("!agent1 hello", "user123", "channel")
        
        assert result == "Agent-1"

    def test_determine_responder_broadcast_command(self):
        """Test broadcast command detection."""
        interpreter = MessageInterpreter()
        
        result = interpreter.determine_responder("!team help", "user123", "channel")
        
        assert result == "BROADCAST"

    def test_determine_responder_content_match(self):
        """Test content-based agent matching."""
        interpreter = MessageInterpreter()
        
        # Test web development related message
        result = interpreter.determine_responder(
            "How do I fix this React component?", "user123", "channel"
        )
        
        # Result may be None, an agent ID, or BROADCAST
        assert result is None or result.startswith("Agent-") or result == "BROADCAST"

    def test_should_respond_empty_message(self):
        """Test response decision for empty message."""
        interpreter = MessageInterpreter()
        
        assert not interpreter.should_respond("")
        assert not interpreter.should_respond("   ")

    def test_should_respond_substantial_message(self):
        """Test response decision for substantial message."""
        interpreter = MessageInterpreter()
        
        assert interpreter.should_respond("This is a substantial message")
        assert interpreter.should_respond("Hello world!")

    def test_should_respond_command(self):
        """Test response decision for commands."""
        interpreter = MessageInterpreter()
        
        assert interpreter.should_respond("!agent1")
        assert interpreter.should_respond("!team")

    def test_get_response_count(self):
        """Test response count calculation."""
        interpreter = MessageInterpreter()
        
        count = interpreter.get_response_count("test message")
        
        assert count == 1
        assert isinstance(count, int)

    def test_activity_rotation(self):
        """Test activity rotation tracking."""
        interpreter = MessageInterpreter()
        
        agent = interpreter._apply_activity_rotation("Agent-1", "test message")
        
        assert agent == "Agent-1"
        assert "Agent-1" in interpreter.agent_activity
        assert interpreter.agent_activity["Agent-1"] > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

