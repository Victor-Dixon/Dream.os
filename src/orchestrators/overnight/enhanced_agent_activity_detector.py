#!/usr/bin/env python3
"""
<!-- SSOT Domain: core -->

Enhanced Agent Activity Detector - Main Entry Point
===================================================

Main entry point for enhanced agent activity detection.
Uses modular checkers for comprehensive activity monitoring.

V2 Compliant: <200 lines, modular architecture
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2026-01-08
"""

import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
import logging

from .activity_file_checkers import FileSystemActivityChecker
from .activity_git_checkers import GitActivityChecker
from .activity_message_checkers import MessageActivityChecker

logger = logging.getLogger(__name__)


class EnhancedAgentActivityDetector:
    """
    Detects agent activity through multiple modular indicators.

    Tracks:
    - File modifications (status.json, inbox, devlogs, reports)
    - Message operations (queue, inbox processing)
    - Code operations (git commits, file changes)
    - Tool executions
    - Discord activity
    - Inter-agent communications
    """

    def __init__(self, workspace_root: Optional[Path] = None):
        """Initialize activity detector with modular checkers."""
        self.workspace_root = workspace_root or Path(".")
        self.agent_workspaces = self.workspace_root / "agent_workspaces"
        self.devlogs_dir = self.workspace_root / "devlogs"

        # Initialize modular checkers
        self.file_checker = FileSystemActivityChecker(self.workspace_root)
        self.git_checker = GitActivityChecker(self.workspace_root)
        self.message_checker = MessageActivityChecker(self.workspace_root)

    def detect_agent_activity(self, agent_id: str) -> Dict[str, Any]:
        """
        Detect all activity indicators for an agent using modular checkers.

        Returns dict with activity indicators and metadata.
        """
        activity_data = {
            "agent_id": agent_id,
            "detection_timestamp": datetime.now().isoformat(),
            "activity_indicators": {},
            "overall_activity_score": 0,
            "is_active": False,
            "last_activity_timestamp": None
        }

        # File system activity checks
        activity_data["activity_indicators"]["status_json"] = self.file_checker.check_status_json(agent_id)
        activity_data["activity_indicators"]["inbox_files"] = self.file_checker.check_inbox_files(agent_id)
        activity_data["activity_indicators"]["devlogs"] = self.file_checker.check_devlogs(agent_id)
        activity_data["activity_indicators"]["reports"] = self.file_checker.check_reports(agent_id)
        activity_data["activity_indicators"]["workspace_files"] = self.file_checker.check_workspace_files(agent_id)

        # Git activity checks
        activity_data["activity_indicators"]["git_commits"] = self.git_checker.check_git_commits(agent_id)
        activity_data["activity_indicators"]["git_status"] = self.git_checker.check_git_status(agent_id)

        # Message and communication checks
        activity_data["activity_indicators"]["message_queue"] = self.message_checker.check_message_queue(agent_id)
        activity_data["activity_indicators"]["discord_posts"] = self.message_checker.check_discord_posts(agent_id)
        activity_data["activity_indicators"]["agent_communications"] = self.message_checker.check_agent_communications(agent_id)

        # Calculate overall activity score and status
        self._calculate_activity_score(activity_data)

        return activity_data

    def _calculate_activity_score(self, activity_data: Dict[str, Any]) -> None:
        """Calculate overall activity score from indicators."""
        indicators = activity_data["activity_indicators"]
        score = 0
        latest_timestamp = None

        # Weight different activity types
        weights = {
            "status_json": 3,  # High weight for status updates
            "git_commits": 4,  # Very high weight for commits
            "inbox_files": 2,  # Medium weight for messages
            "devlogs": 2,      # Medium weight for documentation
            "reports": 2,      # Medium weight for reporting
            "workspace_files": 1,  # Low weight for file changes
            "message_queue": 2,   # Medium weight for messaging
            "discord_posts": 2,   # Medium weight for Discord activity
            "agent_communications": 2,  # Medium weight for inter-agent comms
            "git_status": 1     # Low weight for uncommitted changes
        }

        for indicator_name, indicator_data in indicators.items():
            if indicator_data:
                score += weights.get(indicator_name, 1)

                # Track latest activity timestamp
                if "latest_modification" in indicator_data:
                    timestamp_str = indicator_data["latest_modification"]
                elif "latest_communication" in indicator_data:
                    timestamp_str = indicator_data["latest_communication"]
                elif "last_updated" in indicator_data:
                    timestamp_str = indicator_data["last_updated"]
                else:
                    timestamp_str = None

                if timestamp_str:
                    try:
                        timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                        if latest_timestamp is None or timestamp > latest_timestamp:
                            latest_timestamp = timestamp
                    except:
                        pass

        # Determine if agent is currently active
        is_active = score > 0
        if latest_timestamp:
            time_diff = datetime.now() - latest_timestamp
            # Consider active if activity within last 24 hours
            is_active = is_active and time_diff < timedelta(hours=24)

        activity_data["overall_activity_score"] = score
        activity_data["is_active"] = is_active
        activity_data["last_activity_timestamp"] = latest_timestamp.isoformat() if latest_timestamp else None

    def get_activity_summary(self, agent_ids: List[str]) -> Dict[str, Any]:
        """Get activity summary for multiple agents."""
        summary = {
            "total_agents": len(agent_ids),
            "active_agents": 0,
            "inactive_agents": 0,
            "agent_activities": {},
            "generated_at": datetime.now().isoformat()
        }

        for agent_id in agent_ids:
            activity = self.detect_agent_activity(agent_id)
            summary["agent_activities"][agent_id] = activity

            if activity["is_active"]:
                summary["active_agents"] += 1
            else:
                summary["inactive_agents"] += 1

        return summary

    def detect_recent_activity(self, agent_id: str, hours: int = 24) -> List[Dict[str, Any]]:
        """Detect activity within specified time window."""
        activity = self.detect_agent_activity(agent_id)
        recent_activities = []

        cutoff_time = datetime.now() - timedelta(hours=hours)

        for indicator_name, indicator_data in activity["activity_indicators"].items():
            if indicator_data and "latest_modification" in indicator_data:
                try:
                    activity_time = datetime.fromisoformat(indicator_data["latest_modification"])
                    if activity_time > cutoff_time:
                        recent_activities.append({
                            "indicator": indicator_name,
                            "timestamp": indicator_data["latest_modification"],
                            "details": indicator_data
                        })
                except:
                    pass

        return sorted(recent_activities, key=lambda x: x["timestamp"], reverse=True)


__all__ = ["EnhancedAgentActivityDetector"]