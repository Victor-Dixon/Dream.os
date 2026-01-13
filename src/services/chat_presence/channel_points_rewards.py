#!/usr/bin/env python3
"""
<!-- SSOT Domain: integration -->

Twitch Channel Points Rewards Configuration
===========================================

Defines channel point rewards and maps them to agent swarm actions.

V2 Compliance: <400 lines, single responsibility
Author: Agent-4 (Captain)
License: MIT
"""

from dataclasses import dataclass
from typing import Optional, Callable, Dict, Any
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class RewardCategory(Enum):
    """Categories for channel point rewards."""
    CONTROL = "control"           # Control & Influence
    VISIBILITY = "visibility"     # Visibility & Recognition
    CHAOS = "chaos"               # Chaos & Experimentation
    EDUCATION = "education"       # Education & Insight
    META = "meta"                 # Meta-Game / Progression


@dataclass
class ChannelPointReward:
    """
    Configuration for a channel point reward.
    
    Maps Twitch reward redemption to agent swarm actions.
    """
    reward_id: str                    # Twitch reward ID (from EventSub)
    name: str                         # Display name
    description: str                  # Reward description
    category: RewardCategory          # Reward category
    point_cost: int                   # Channel points cost (set on Twitch)
    handler_func: Callable            # Function to handle redemption
    requires_approval: bool = False   # Whether streamer approval needed
    rate_limit_seconds: int = 0       # Minimum seconds between redemptions (0 = no limit)
    
    def __post_init__(self):
        """Validate reward configuration."""
        if self.point_cost < 0:
            raise ValueError(f"Reward '{self.name}' cannot have negative point cost")
        if self.rate_limit_seconds < 0:
            raise ValueError(f"Reward '{self.name}' cannot have negative rate limit")


# MVP Reward Handlers
# These functions are called when a reward is redeemed

def handle_force_status_report(
    user_name: str,
    user_id: str,
    redemption_id: str,
    reward_data: Dict[str, Any]
) -> str:
    """
    Force an agent to provide a status report.
    
    Reward: Force Agent Status Report
    """
    import subprocess
    from src.core.agent_mode_manager import get_active_agents
    
    active_agents = get_active_agents()
    if not active_agents:
        return f"⚠️ No active agents to report. Requested by {user_name}."
    
    # For MVP: Send to first active agent
    # Future: Allow viewer to choose agent
    target_agent = active_agents[0]
    
    message = (
        f"🚨 **LIVE STATUS REQUEST**\n"
        f"Requested by: @{user_name}\n\n"
        f"Please provide current status update immediately."
    )
    
    try:
        result = subprocess.run(
            [
                "python", "-m", "src.services.messaging_cli",
                "--agent", target_agent,
                "--message", message,
                "--type", "text",
                "--category", "a2c",
                "--priority", "urgent"
            ],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            return f"✅ Status report requested from {target_agent} (requested by {user_name})"
        else:
            logger.error(f"Failed to request status: {result.stderr}")
            return f"⚠️ Failed to request status report. Error logged."
    except Exception as e:
        logger.error(f"Error handling force status report: {e}", exc_info=True)
        return f"⚠️ Error requesting status report: {str(e)}"


def handle_vote_next_task(
    user_name: str,
    user_id: str,
    redemption_id: str,
    reward_data: Dict[str, Any]
) -> str:
    """
    Vote on next task priority.
    
    Reward: Vote on Next Task
    """
    # MVP: Store vote, announce in chat
    # Future: Accumulate votes, trigger when threshold met
    return f"🗳️ Vote recorded from {user_name}. Voting system in development."


def handle_inject_constraint(
    user_name: str,
    user_id: str,
    redemption_id: str,
    reward_data: Dict[str, Any]
) -> str:
    """
    Inject a creative constraint for next agent task.
    
    Reward: Inject Constraint
    """
    # MVP: Store constraint, apply to next agent message
    return f"🧪 Constraint injection from {user_name} noted. Will apply to next agent task."


def handle_name_in_devlog(
    user_name: str,
    user_id: str,
    redemption_id: str,
    reward_data: Dict[str, Any]
) -> str:
    """
    Add viewer name to next devlog.
    
    Reward: Name in Devlog
    """
    # MVP: Store name, add to next devlog template
    return f"📜 {user_name} will be credited in next devlog!"


def handle_chaos_mode(
    user_name: str,
    user_id: str,
    redemption_id: str,
    reward_data: Dict[str, Any]
) -> str:
    """
    Trigger random/chaos mode for agent.
    
    Reward: Chaos Mode
    """
    import random
    import subprocess
    from src.core.agent_mode_manager import get_active_agents
    
    chaos_modes = [
        "Solve this creatively",
        "Explain like I'm 5",
        "Speed run mode (5 minute limit)",
        "No imports allowed",
        "Explain before coding"
    ]
    
    selected_mode = random.choice(chaos_modes)
    active_agents = get_active_agents()
    
    if not active_agents:
        return f"🎲 Chaos mode: {selected_mode} (no active agents)"
    
    target_agent = random.choice(active_agents)
    message = f"🎲 **CHAOS MODE ACTIVATED** by @{user_name}\n\nConstraint: {selected_mode}"
    
    try:
        subprocess.run(
            [
                "python", "-m", "src.services.messaging_cli",
                "--agent", target_agent,
                "--message", message,
                "--type", "text",
                "--category", "a2a",
                "--priority", "normal"
            ],
            timeout=10
        )
        return f"🎲 Chaos mode activated: {selected_mode} for {target_agent} (by {user_name})"
    except Exception as e:
        logger.error(f"Error in chaos mode: {e}")
        return f"🎲 Chaos mode: {selected_mode} (error sending to agent)"


def handle_explain_reasoning(
    user_name: str,
    user_id: str,
    redemption_id: str,
    reward_data: Dict[str, Any]
) -> str:
    """
    Request explanation of last agent decision.
    
    Reward: Explain Reasoning
    """
    # MVP: Trigger explanation request
    return f"🧠 Explanation request from {user_name}. Will provide reasoning breakdown."


def handle_unlock_operator_title(
    user_name: str,
    user_id: str,
    redemption_id: str,
    reward_data: Dict[str, Any]
) -> str:
    """
    Unlock operator title for viewer.
    
    Reward: Unlock Operator Title
    """
    # MVP: Track unlocked titles per user
    return f"🏆 {user_name} unlocked 'Junior Operator' title!"


# MVP Reward Definitions
# These map to rewards you'll create in Twitch dashboard
# Match by reward name or ID

MVP_REWARDS: Dict[str, ChannelPointReward] = {
    "force_status_report": ChannelPointReward(
        reward_id="force_status_report",  # Set this when creating reward on Twitch
        name="Force Agent Status Report",
        description="Issue a Swarm Directive: Force an agent to provide live status",
        category=RewardCategory.CONTROL,
        point_cost=100,  # Set actual cost on Twitch
        handler_func=handle_force_status_report,
        requires_approval=False,
        rate_limit_seconds=60  # Max once per minute
    ),
    "vote_next_task": ChannelPointReward(
        reward_id="vote_next_task",
        name="Vote on Next Task",
        description="Influence task prioritization",
        category=RewardCategory.CONTROL,
        point_cost=50,
        handler_func=handle_vote_next_task,
        requires_approval=False,
        rate_limit_seconds=30
    ),
    "inject_constraint": ChannelPointReward(
        reward_id="inject_constraint",
        name="Inject Constraint",
        description="Add creative constraint to next agent task",
        category=RewardCategory.CHAOS,
        point_cost=75,
        handler_func=handle_inject_constraint,
        requires_approval=False,
        rate_limit_seconds=45
    ),
    "name_in_devlog": ChannelPointReward(
        reward_id="name_in_devlog",
        name="Name in Devlog",
        description="Get credited in next devlog publication",
        category=RewardCategory.VISIBILITY,
        point_cost=200,
        handler_func=handle_name_in_devlog,
        requires_approval=False,
        rate_limit_seconds=0
    ),
    "chaos_mode": ChannelPointReward(
        reward_id="chaos_mode",
        name="Chaos Mode",
        description="Trigger random constraint mode for agent",
        category=RewardCategory.CHAOS,
        point_cost=150,
        handler_func=handle_chaos_mode,
        requires_approval=False,
        rate_limit_seconds=120
    ),
    "explain_reasoning": ChannelPointReward(
        reward_id="explain_reasoning",
        name="Explain Reasoning",
        description="Break down last agent decision",
        category=RewardCategory.EDUCATION,
        point_cost=100,
        handler_func=handle_explain_reasoning,
        requires_approval=False,
        rate_limit_seconds=60
    ),
    "unlock_operator_title": ChannelPointReward(
        reward_id="unlock_operator_title",
        name="Unlock Operator Title",
        description="Earn 'Junior Operator' swarm title",
        category=RewardCategory.META,
        point_cost=500,
        handler_func=handle_unlock_operator_title,
        requires_approval=False,
        rate_limit_seconds=0
    ),
}


def get_reward_by_id(reward_id: str) -> Optional[ChannelPointReward]:
    """Get reward configuration by Twitch reward ID."""
    return MVP_REWARDS.get(reward_id)


def get_reward_by_name(name: str) -> Optional[ChannelPointReward]:
    """Get reward configuration by name (case-insensitive)."""
    name_lower = name.lower()
    for reward in MVP_REWARDS.values():
        if reward.name.lower() == name_lower:
            return reward
    return None


def list_all_rewards() -> list[ChannelPointReward]:
    """Get all configured rewards."""
    return list(MVP_REWARDS.values())


__all__ = [
    "ChannelPointReward",
    "RewardCategory",
    "MVP_REWARDS",
    "get_reward_by_id",
    "get_reward_by_name",
    "list_all_rewards",
]

