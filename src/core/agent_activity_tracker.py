"""
Agent Runtime Activity Tracker
==============================

<!-- SSOT Domain: infrastructure -->

Tracks when agents are actively working on message operations.
Provides SSOT for agent activity state across the system.

Author: Agent-1 (Integration & Core Systems)
Date: 2025-01-27
Priority: HIGH
"""

import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Optional

logger = logging.getLogger(__name__)


class AgentActivityTracker:
    """
    Tracks agent runtime activity for message operations.

    SSOT for agent activity state - all components should use this tracker.
    """

    def __init__(self, activity_file: str = "data/agent_activity.json"):
        """Initialize activity tracker."""
        self.activity_file = Path(activity_file)
        self.activity_file.parent.mkdir(parents=True, exist_ok=True)
        self._ensure_activity_file()

    def _ensure_activity_file(self) -> None:
        """Ensure activity file exists with proper structure."""
        if not self.activity_file.exists():
            self._save_activity({
                "agents": {},
                "metadata": {
                    "version": "1.0",
                    "created_at": datetime.now().isoformat()
                }
            })

    def _load_activity(self) -> dict[str, Any]:
        """Load activity data from file."""
        try:
            with open(self.activity_file, encoding="utf-8") as f:
                return json.load(f)
        except (OSError, json.JSONDecodeError):
            return {
                "agents": {},
                "metadata": {"version": "1.0"}
            }

    def _save_activity(self, data: dict[str, Any]) -> bool:
        """Save activity data to file."""
        try:
            with open(self.activity_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except OSError:
            return False

    def mark_active(self, agent_id: str, operation: str = "message_processing") -> bool:
        """
        Mark agent as actively working.

        Args:
            agent_id: Agent identifier (e.g., "Agent-1")
            operation: Type of operation (default: "message_processing")

        Returns:
            True if marked successfully
        """
        data = self._load_activity()
        agents = data.get("agents", {})

        agents[agent_id] = {
            "status": "active",
            "operation": operation,
            "last_active": datetime.now().isoformat(),
            "activity_count": agents.get(agent_id, {}).get("activity_count", 0) + 1
        }

        data["agents"] = agents
        return self._save_activity(data)

    def mark_delivering(self, agent_id: str, queue_id: str) -> bool:
        """
        Mark agent as delivering a message.

        Args:
            agent_id: Agent identifier
            queue_id: Queue ID of message being delivered

        Returns:
            True if marked successfully
        """
        data = self._load_activity()
        agents = data.get("agents", {})

        agents[agent_id] = {
            "status": "delivering",
            "queue_id": queue_id,
            "last_active": datetime.now().isoformat(),
            "operation": "message_delivery",
            "activity_count": agents.get(agent_id, {}).get("activity_count", 0) + 1
        }

        data["agents"] = agents
        return self._save_activity(data)

    def mark_inactive(self, agent_id: str) -> bool:
        """
        Mark agent as inactive (operation complete).

        Args:
            agent_id: Agent identifier

        Returns:
            True if marked successfully
        """
        data = self._load_activity()
        agents = data.get("agents", {})

        if agent_id in agents:
            agents[agent_id]["status"] = "inactive"
            agents[agent_id]["last_inactive"] = datetime.now().isoformat()

        data["agents"] = agents
        return self._save_activity(data)

    def is_agent_active(self, agent_id: str, timeout_minutes: int = 5) -> bool:
        """
        Check if agent is currently active.

        Args:
            agent_id: Agent identifier
            timeout_minutes: Minutes before considering inactive (default: 5)

        Returns:
            True if agent is active within timeout
        """
        data = self._load_activity()
        agents = data.get("agents", {})

        if agent_id not in agents:
            return False

        agent = agents[agent_id]
        status = agent.get("status", "inactive")

        if status == "inactive":
            return False

        # Check timeout
        last_active_str = agent.get("last_active", "")
        if not last_active_str:
            return False

        try:
            last_active = datetime.fromisoformat(last_active_str)
            timeout = timedelta(minutes=timeout_minutes)
            return datetime.now() - last_active < timeout
        except (ValueError, AttributeError):
            return False

    def get_agent_activity(self, agent_id: str) -> dict[str, Any]:
        """
        Get activity information for specific agent.

        Args:
            agent_id: Agent identifier

        Returns:
            Activity dictionary
        """
        data = self._load_activity()
        agents = data.get("agents", {})
        return agents.get(agent_id, {
            "status": "inactive",
            "last_active": None,
            "activity_count": 0
        })

    def get_all_agent_activity(self) -> dict[str, dict[str, Any]]:
        """
        Get activity information for all agents.

        Returns:
            Dictionary mapping agent_id to activity info
        """
        data = self._load_activity()
        return data.get("agents", {})

    def get_active_agents(self, timeout_minutes: int = 5) -> list[str]:
        """
        Get list of currently active agents.

        Args:
            timeout_minutes: Minutes before considering inactive

        Returns:
            List of active agent IDs
        """
        data = self._load_activity()
        agents = data.get("agents", {})
        active = []

        for agent_id in agents:
            if self.is_agent_active(agent_id, timeout_minutes):
                active.append(agent_id)

        return active


# Global instance for easy access
_activity_tracker: Optional[AgentActivityTracker] = None


def get_activity_tracker() -> AgentActivityTracker:
    """Get global activity tracker instance."""
    global _activity_tracker
    if _activity_tracker is None:
        _activity_tracker = AgentActivityTracker()
    return _activity_tracker
