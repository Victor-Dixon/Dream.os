"""
Daily Cycle Tracker - Track cycles by day for productivity metrics
<!-- SSOT Domain: infrastructure -->


Tracks daily cycles to measure productivity and prepare for end-of-day pushes
before autonomous overnight runs.

Author: Agent-1 (Integration & Core Systems)
Date: 2025-01-27
"""

import json
from pathlib import Path
from datetime import datetime, timezone, date
from typing import Dict, Any, List, Optional


class DailyCycleTracker:
    """
    Tracks cycles by day for productivity measurement.
    
    Each day = 1 cycle for tracking purposes.
    Tracks what gets done each day and prepares for end-of-day push.
    """
    
    def __init__(self, agent_id: str):
        """
        Initialize daily cycle tracker.
        
        Args:
            agent_id: Agent identifier (e.g., "Agent-1")
        """
        self.agent_id = agent_id
        self.workspace = Path(f"agent_workspaces/{agent_id}")
        self.cycle_file = self.workspace / "daily_cycles.json"
        
        # Ensure workspace exists
        self.workspace.mkdir(parents=True, exist_ok=True)
        
        # Load or create cycle data
        self._load_cycles()
    
    def _load_cycles(self) -> None:
        """Load daily cycle data or create default."""
        if self.cycle_file.exists():
            with open(self.cycle_file) as f:
                self.cycles = json.load(f)
        else:
            self.cycles = {
                "agent_id": self.agent_id,
                "current_day": None,
                "current_cycle_date": None,
                "daily_cycles": {},
                "total_days": 0,
                "last_updated": datetime.now(timezone.utc).isoformat()
            }
            self._save_cycles()
    
    def _save_cycles(self) -> None:
        """Save daily cycle data."""
        self.cycles["last_updated"] = datetime.now(timezone.utc).isoformat()
        
        with open(self.cycle_file, 'w') as f:
            json.dump(self.cycles, f, indent=2)
    
    def start_new_day(self) -> Dict[str, Any]:
        """
        Start a new day cycle.
        
        Returns:
            Dictionary with day cycle information
        """
        today = date.today().isoformat()
        
        # Check if this is a new day
        if self.cycles["current_cycle_date"] != today:
            # End previous day if exists
            if self.cycles["current_cycle_date"]:
                self._end_day()
            
            # Start new day
            self.cycles["current_cycle_date"] = today
            self.cycles["current_day"] = today
            
            if today not in self.cycles["daily_cycles"]:
                self.cycles["daily_cycles"][today] = {
                    "date": today,
                    "start_time": datetime.now(timezone.utc).isoformat(),
                    "end_time": None,
                    "tasks_completed": [],
                    "points_earned": 0,
                    "interaction_count": 0,
                    "commits_made": 0,
                    "status_updates": 0,
                    "messages_sent": 0,
                    "messages_received": 0,
                    "blockers": [],
                    "achievements": [],
                    "ready_for_push": False,
                    "pushed": False
                }
                self.cycles["total_days"] = len(self.cycles["daily_cycles"])
            
            self._save_cycles()
        
        return self.cycles["daily_cycles"][today]
    
    def _end_day(self) -> None:
        """End the current day cycle."""
        if not self.cycles["current_cycle_date"]:
            return
        
        day_data = self.cycles["daily_cycles"][self.cycles["current_cycle_date"]]
        day_data["end_time"] = datetime.now(timezone.utc).isoformat()
        day_data["ready_for_push"] = True
        
        self._save_cycles()
    
    def record_interaction(self) -> None:
        """Record an interaction (Captain prompt + Agent response)."""
        today = date.today().isoformat()
        self.start_new_day()
        
        if today in self.cycles["daily_cycles"]:
            self.cycles["daily_cycles"][today]["interaction_count"] += 1
            self._save_cycles()
    
    def record_task_completed(self, task_name: str, points: int = 0) -> None:
        """
        Record a completed task.
        
        Args:
            task_name: Name of completed task
            points: Points earned for task
        """
        today = date.today().isoformat()
        self.start_new_day()
        
        if today in self.cycles["daily_cycles"]:
            day_data = self.cycles["daily_cycles"][today]
            day_data["tasks_completed"].append({
                "task": task_name,
                "points": points,
                "timestamp": datetime.now(timezone.utc).isoformat()
            })
            day_data["points_earned"] += points
            self._save_cycles()
    
    def record_commit(self) -> None:
        """Record a git commit."""
        today = date.today().isoformat()
        self.start_new_day()
        
        if today in self.cycles["daily_cycles"]:
            self.cycles["daily_cycles"][today]["commits_made"] += 1
            self._save_cycles()
    
    def record_status_update(self) -> None:
        """Record a status.json update."""
        today = date.today().isoformat()
        self.start_new_day()
        
        if today in self.cycles["daily_cycles"]:
            self.cycles["daily_cycles"][today]["status_updates"] += 1
            self._save_cycles()
    
    def record_message_sent(self) -> None:
        """Record a message sent."""
        today = date.today().isoformat()
        self.start_new_day()
        
        if today in self.cycles["daily_cycles"]:
            self.cycles["daily_cycles"][today]["messages_sent"] += 1
            self._save_cycles()
    
    def record_message_received(self) -> None:
        """Record a message received."""
        today = date.today().isoformat()
        self.start_new_day()
        
        if today in self.cycles["daily_cycles"]:
            self.cycles["daily_cycles"][today]["messages_received"] += 1
            self._save_cycles()
    
    def add_blocker(self, blocker: str) -> None:
        """
        Add a blocker for the day.
        
        Args:
            blocker: Description of blocker
        """
        today = date.today().isoformat()
        self.start_new_day()
        
        if today in self.cycles["daily_cycles"]:
            self.cycles["daily_cycles"][today]["blockers"].append({
                "blocker": blocker,
                "timestamp": datetime.now(timezone.utc).isoformat()
            })
            self._save_cycles()
    
    def add_achievement(self, achievement: str) -> None:
        """
        Add an achievement for the day.
        
        Args:
            achievement: Description of achievement
        """
        today = date.today().isoformat()
        self.start_new_day()
        
        if today in self.cycles["daily_cycles"]:
            self.cycles["daily_cycles"][today]["achievements"].append({
                "achievement": achievement,
                "timestamp": datetime.now(timezone.utc).isoformat()
            })
            self._save_cycles()
    
    def mark_ready_for_push(self) -> None:
        """Mark current day as ready for end-of-cycle push."""
        today = date.today().isoformat()
        self.start_new_day()
        
        if today in self.cycles["daily_cycles"]:
            self.cycles["daily_cycles"][today]["ready_for_push"] = True
            self._save_cycles()
    
    def mark_pushed(self) -> None:
        """Mark current day as pushed to git."""
        today = date.today().isoformat()
        self.start_new_day()
        
        if today in self.cycles["daily_cycles"]:
            self.cycles["daily_cycles"][today]["pushed"] = True
            self._save_cycles()
    
    def get_today_summary(self) -> Dict[str, Any]:
        """
        Get summary of today's cycle.
        
        Returns:
            Dictionary with today's cycle summary
        """
        today = date.today().isoformat()
        self.start_new_day()
        
        if today in self.cycles["daily_cycles"]:
            day_data = self.cycles["daily_cycles"][today]
            return {
                "date": today,
                "tasks_completed": len(day_data["tasks_completed"]),
                "points_earned": day_data["points_earned"],
                "interactions": day_data["interaction_count"],
                "commits": day_data["commits_made"],
                "status_updates": day_data["status_updates"],
                "messages_sent": day_data["messages_sent"],
                "messages_received": day_data["messages_received"],
                "blockers": len(day_data["blockers"]),
                "achievements": len(day_data["achievements"]),
                "ready_for_push": day_data["ready_for_push"],
                "pushed": day_data["pushed"]
            }
        return {}
    
    def get_all_days_summary(self) -> List[Dict[str, Any]]:
        """
        Get summary of all days.
        
        Returns:
            List of day summaries
        """
        summaries = []
        for day_date, day_data in sorted(self.cycles["daily_cycles"].items()):
            summaries.append({
                "date": day_date,
                "tasks_completed": len(day_data["tasks_completed"]),
                "points_earned": day_data["points_earned"],
                "interactions": day_data["interaction_count"],
                "commits": day_data["commits_made"],
                "ready_for_push": day_data["ready_for_push"],
                "pushed": day_data["pushed"]
            })
        return summaries

