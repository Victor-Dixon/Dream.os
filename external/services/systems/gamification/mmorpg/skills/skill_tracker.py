"""
Skill Tracker - Skill Progress Tracking
======================================

This module handles skill progress tracking and statistics.
"""

from typing import Dict, Any, List
from datetime import datetime


class SkillTracker:
    """Tracks skill progress and statistics."""
    
    def __init__(self):
        """Initialize skill tracker."""
        self.progress_history = []
    
    def record_progress(self, skill_name: str, xp_gained: int, source: str = "manual"):
        """Record skill progress."""
        entry = {
            "skill_name": skill_name,
            "xp_gained": xp_gained,
            "source": source,
            "timestamp": datetime.now().isoformat()
        }
        self.progress_history.append(entry)
    
    def get_recent_progress(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent skill progress."""
        return self.progress_history[-limit:] if self.progress_history else []
    
    def get_stats(self) -> Dict[str, Any]:
        """Get tracker statistics."""
        return {
            "total_progress_entries": len(self.progress_history),
            "recent_activity": len(self.get_recent_progress(5))
        } 