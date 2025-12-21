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

# Channel points integration (optional - requires Flask)
try:
    from .channel_points_rewards import (
        ChannelPointReward,
        RewardCategory,
        MVP_REWARDS,
        get_reward_by_id,
        get_reward_by_name,
        list_all_rewards,
    )
    from .twitch_eventsub_handler import (
        TwitchEventSubHandler,
        create_eventsub_flask_app,
    )
    CHANNEL_POINTS_AVAILABLE = True
except ImportError:
    CHANNEL_POINTS_AVAILABLE = False

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
    "CHANNEL_POINTS_AVAILABLE",
]

# Add channel points exports if available
if CHANNEL_POINTS_AVAILABLE:
    __all__.extend([
        "ChannelPointReward",
        "RewardCategory",
        "MVP_REWARDS",
        "get_reward_by_id",
        "get_reward_by_name",
        "list_all_rewards",
        "TwitchEventSubHandler",
        "create_eventsub_flask_app",
    ])




