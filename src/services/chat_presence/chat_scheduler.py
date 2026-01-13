#!/usr/bin/env python3
"""
<!-- SSOT Domain: integration -->

Agent Chat Scheduler
====================

Manages fair rotation and priority balancing for agent responses.
Ensures all agents get speaking time and handles priority messages.

V2 Compliance: <400 lines, single responsibility
Author: Agent-7 (Web Development Specialist)
License: MIT
"""

import logging
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Optional

logger = logging.getLogger(__name__)


class ChatScheduler:
    """
    Schedules agent responses with fair rotation.

    Features:
    - Activity tracking per agent
    - Priority message handling
    - Cooldown periods
    - Fair rotation algorithm
    """

    def __init__(self, cooldown_seconds: int = 30):
        """
        Initialize chat scheduler.

        Args:
            cooldown_seconds: Minimum seconds between agent responses
        """
        self.cooldown_seconds = cooldown_seconds
        self.agent_activity = defaultdict(list)  # Timestamps of responses
        self.agent_message_counts = defaultdict(int)  # Total message counts

    def can_agent_speak(self, agent_id: str) -> bool:
        """
        Check if agent can speak (cooldown check).

        Args:
            agent_id: Agent identifier

        Returns:
            True if agent can speak now
        """
        if agent_id not in self.agent_activity:
            return True

        recent_activity = self.agent_activity[agent_id]
        if not recent_activity:
            return True

        # Check if cooldown period has passed
        last_activity = max(recent_activity)
        time_since_last = (datetime.now() - last_activity).total_seconds()

        return time_since_last >= self.cooldown_seconds

    def record_agent_response(self, agent_id: str) -> None:
        """
        Record that an agent has responded.

        Args:
            agent_id: Agent identifier
        """
        now = datetime.now()
        self.agent_activity[agent_id].append(now)
        self.agent_message_counts[agent_id] += 1

        # Clean old activity (keep last hour)
        cutoff = now - timedelta(hours=1)
        self.agent_activity[agent_id] = [
            ts for ts in self.agent_activity[agent_id] if ts > cutoff
        ]

    def get_least_active_agent(self, candidate_agents: list[str]) -> Optional[str]:
        """
        Get least active agent from candidates.

        Args:
            candidate_agents: List of candidate agent IDs

        Returns:
            Least active agent ID or None
        """
        if not candidate_agents:
            return None

        # Find agent with lowest message count
        least_active = None
        min_count = float("inf")

        for agent_id in candidate_agents:
            count = self.agent_message_counts.get(agent_id, 0)
            if count < min_count:
                min_count = count
                least_active = agent_id

        return least_active

    def get_agent_activity_stats(self) -> dict[str, dict]:
        """
        Get activity statistics for all agents.

        Returns:
            Dictionary of agent activity stats
        """
        stats = {}

        for agent_id in [
            "Agent-1",
            "Agent-2",
            "Agent-3",
            "Agent-4",
            "Agent-5",
            "Agent-6",
            "Agent-7",
            "Agent-8",
        ]:
            recent_count = len(self.agent_activity.get(agent_id, []))
            total_count = self.agent_message_counts.get(agent_id, 0)

            stats[agent_id] = {
                "recent_responses": recent_count,
                "total_responses": total_count,
                "can_speak": self.can_agent_speak(agent_id),
            }

        return stats

    def select_agent_with_rotation(
        self, suggested_agent: str, all_candidates: list[str]
    ) -> str:
        """
        Select agent with rotation fairness applied.

        Args:
            suggested_agent: Initially suggested agent
            all_candidates: All candidate agents

        Returns:
            Final selected agent ID
        """
        # If suggested agent can speak, use them
        if suggested_agent in all_candidates and self.can_agent_speak(suggested_agent):
            return suggested_agent

        # Find alternative from candidates
        available = [
            agent for agent in all_candidates if self.can_agent_speak(agent)
        ]

        if not available:
            # If none available, use least active
            return self.get_least_active_agent(all_candidates) or suggested_agent

        # Use least active from available
        return self.get_least_active_agent(available) or available[0]

    def reset_activity(self, agent_id: Optional[str] = None) -> None:
        """
        Reset activity tracking.

        Args:
            agent_id: Specific agent to reset, or None for all
        """
        if agent_id:
            self.agent_activity[agent_id] = []
            self.agent_message_counts[agent_id] = 0
        else:
            self.agent_activity.clear()
            self.agent_message_counts.clear()


__all__ = ["ChatScheduler"]




