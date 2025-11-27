"""
Chat Presence System
===================

Agent chat presence for Twitch and Discord.
"""

from .agent_personality import (
    AGENT_PERSONALITIES,
    AgentPersonality,
    PersonalityTone,
    format_chat_message,
    get_personality,
    should_agent_respond,
)
from .chat_presence_orchestrator import ChatPresenceOrchestrator
from .chat_scheduler import ChatScheduler
from .message_interpreter import MessageInterpreter
from .twitch_bridge import TwitchChatBridge, TwitchIRCBot

__all__ = [
    "ChatPresenceOrchestrator",
    "TwitchChatBridge",
    "TwitchIRCBot",
    "MessageInterpreter",
    "ChatScheduler",
    "AgentPersonality",
    "PersonalityTone",
    "AGENT_PERSONALITIES",
    "get_personality",
    "format_chat_message",
    "should_agent_respond",
]


