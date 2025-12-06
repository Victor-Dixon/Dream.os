"""
Activity Repository - SSOT for Agent Activity Data
==================================================

Persistent storage for agent activity data from AgentActivityTracker.
Provides SSOT for all activity history and monitoring.

<!-- SSOT Domain: data -->

Author: Agent-5 (Business Intelligence Specialist)
Date: 2025-01-27
JET FUEL: Autonomous creation
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

try:
    from src.core.agent_activity_tracker import AgentActivityState
    ACTIVITY_AVAILABLE = True
except ImportError:
    ACTIVITY_AVAILABLE = False
    AgentActivityState = None


class ActivityRepository:
    """
    Repository for agent activity data persistence.
    
    Provides SSOT for activity history and monitoring.
    """

    def __init__(
        self,
        activity_history_file: str = "data/agent_activity_history.json",
    ):
        """
        Initialize activity repository.

        Args:
            activity_history_file: Path to activity history storage
        """
        self.activity_history_file = Path(activity_history_file)
        self._ensure_history_file()

    def _ensure_history_file(self) -> None:
        """Ensure activity history file exists."""
        if not self.activity_history_file.exists():
            self.activity_history_file.parent.mkdir(parents=True, exist_ok=True)
            self._save_history({
                "activity_logs": [],
                "metadata": {"version": "1.0", "created_at": datetime.now().isoformat()},
            })

    def _load_history(self) -> dict[str, Any]:
        """Load activity history from file."""
        try:
            with open(self.activity_history_file, encoding="utf-8") as f:
                return json.load(f)
        except (OSError, json.JSONDecodeError):
            return {"activity_logs": [], "metadata": {"version": "1.0"}}

    def _save_history(self, data: dict[str, Any]) -> bool:
        """Save activity history to file."""
        try:
            with open(self.activity_history_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except OSError:
            return False

    def save_activity_change(
        self,
        agent_id: str,
        state: str,
        message_id: Optional[str] = None,
        queue_id: Optional[str] = None,
    ) -> bool:
        """
        Save activity state change to history.

        Args:
            agent_id: Agent identifier
            state: Activity state (idle, producing, queued, delivering, complete)
            message_id: Optional message ID
            queue_id: Optional queue ID

        Returns:
            True if save successful, False otherwise
        """
        data = self._load_history()
        logs = data.get("activity_logs", [])

        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "agent_id": agent_id,
            "state": state,
            "message_id": message_id,
            "queue_id": queue_id,
        }

        logs.append(log_entry)
        data["activity_logs"] = logs
        return self._save_history(data)

    def get_activity_history(
        self, agent_id: Optional[str] = None, limit: Optional[int] = None
    ) -> list[dict[str, Any]]:
        """
        Get activity history, optionally filtered by agent.

        Args:
            agent_id: Optional agent ID to filter by
            limit: Optional maximum number of logs to return

        Returns:
            List of activity log dictionaries
        """
        data = self._load_history()
        logs = data.get("activity_logs", [])

        if agent_id:
            logs = [l for l in logs if l.get("agent_id") == agent_id]

        logs.sort(key=lambda x: x.get("timestamp", ""), reverse=True)

        if limit:
            logs = logs[:limit]

        return logs

    def get_agent_activity_summary(self, agent_id: str, hours: int = 24) -> dict[str, Any]:
        """
        Get activity summary for agent.

        Args:
            agent_id: Agent identifier
            hours: Hours of history to analyze

        Returns:
            Dictionary with activity summary
        """
        from datetime import timedelta

        cutoff = datetime.now() - timedelta(hours=hours)
        history = self.get_activity_history(agent_id=agent_id)

        recent_logs = [
            log for log in history
            if datetime.fromisoformat(log.get("timestamp", "").replace("Z", "+00:00")).replace(tzinfo=None) >= cutoff
        ]

        state_counts = {}
        for log in recent_logs:
            state = log.get("state", "unknown")
            state_counts[state] = state_counts.get(state, 0) + 1

        return {
            "agent_id": agent_id,
            "period_hours": hours,
            "total_activity_changes": len(recent_logs),
            "by_state": state_counts,
            "last_activity": recent_logs[0] if recent_logs else None,
        }


