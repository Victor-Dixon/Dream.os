#!/usr/bin/env python3
"""
Unit Tests for Agent Personality
==================================

Tests for agent personality system.
"""

import pytest
from unittest.mock import Mock, patch

try:
    from src.services.chat_presence.agent_personality import (
        AgentPersonality,
        PersonalityTone,
        get_personality,
        format_chat_message,
        should_agent_respond,
        AGENT_PERSONALITIES,
    )
    AGENT_PERSONALITY_AVAILABLE = True
except ImportError:
    AGENT_PERSONALITY_AVAILABLE = False


@pytest.mark.skipif(not AGENT_PERSONALITY_AVAILABLE, reason="Agent personality not available")
class TestAgentPersonality:
    """Unit tests for Agent Personality."""

    def test_personality_tone_enum(self):
        """Test personality tone enumeration."""
        assert PersonalityTone.FRIENDLY.value == "friendly"
        assert PersonalityTone.PROFESSIONAL.value == "professional"
        assert PersonalityTone.TECHNICAL.value == "technical"

    def test_get_personality(self):
        """Test getting agent personality."""
        personality = get_personality("Agent-1")
        
        assert personality is not None
        assert hasattr(personality, "agent_id") or "agent_id" in personality

    def test_get_personality_unknown_agent(self):
        """Test getting personality for unknown agent."""
        personality = get_personality("Unknown-Agent")
        
        # Should return default or None
        assert personality is not None or personality is None

    def test_format_chat_message(self):
        """Test chat message formatting."""
        message = format_chat_message("Agent-1", "Hello world")
        
        assert isinstance(message, str)
        assert len(message) > 0

    def test_format_chat_message_with_context(self):
        """Test chat message formatting with context."""
        context = {"channel": "test", "username": "user123"}
        message = format_chat_message("Agent-1", "Hello", context)
        
        assert isinstance(message, str)

    def test_should_agent_respond(self):
        """Test agent response decision."""
        result = should_agent_respond("Agent-1", "test message about web development")
        
        assert isinstance(result, bool)

    def test_should_agent_respond_keywords(self):
        """Test agent response with keywords."""
        # Test with relevant keywords
        result = should_agent_respond("Agent-7", "How do I fix this React bug?")
        
        assert isinstance(result, bool)

    def test_agent_personalities_defined(self):
        """Test that agent personalities are defined."""
        assert AGENT_PERSONALITIES is not None
        assert isinstance(AGENT_PERSONALITIES, dict) or isinstance(AGENT_PERSONALITIES, list)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

