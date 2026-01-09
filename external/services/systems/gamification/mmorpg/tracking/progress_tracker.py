"""
MMORPG Progress Tracking
Contains the progress tracking system for the Dreamscape MMORPG.
"""

from typing import Dict, List, Any, Optional
import json
import os
from datetime import datetime, timedelta

from ..models import Quest, Skill, Achievement, GameState


class TrackMMORPGProgress:
    """Tracks MMORPG progress and generates reports."""
    
    def __init__(self, save_file: str = "mmorpg_progress.json"):
        """Initialize the progress tracker."""
        self.save_file = save_file
        self.progress_data = self._load_progress()
        
    def _load_progress(self) -> Dict[str, Any]:
        """Load progress data from file."""
        try:
            if os.path.exists(self.save_file):
                with open(self.save_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading progress: {e}")
            
        return self._initialize_progress()
        
    def _initialize_progress(self) -> Dict[str, Any]:
        """Initialize default progress structure."""
        return {
            "player": {
                "name": "Dreamscape Player",
                "level": 1,
                "total_xp": 0,
                "architect_tier": "Tier 1 - Novice",
                "created_at": datetime.now().isoformat(),
                "last_active": datetime.now().isoformat()
            },
            "quests": {
                "total_started": 0,
                "total_completed": 0,
                "total_failed": 0,
                "active_quests": [],
                "completed_quests": [],
                "failed_quests": []
            },
            "skills": {
                "total_skills": 0,
                "skill_levels": {},
                "total_skill_xp": 0,
                "highest_skill": None,
                "skill_progress": {}
            },
            "achievements": {
                "total_earned": 0,
                "achievement_list": [],
                "recent_achievements": []
            },
            "game_state": {
                "current_tier": 1,
                "total_xp": 0,
                "last_updated": datetime.now().isoformat()
            },
            "play_time": {
                "total_hours": 0.0,
                "sessions": [],
                "average_session_length": 0.0
            },
            "activity_log": []
        }
        
    def save_progress(self) -> bool:
        """Save progress data to file."""
        try:
            # Update last active timestamp
            self.progress_data["player"]["last_active"] = datetime.now().isoformat()
            self.progress_data["game_state"]["last_updated"] = datetime.now().isoformat()
            
            with open(self.save_file, 'w') as f:
                json.dump(self.progress_data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving progress: {e}")
            return False
            
    def update_player_level(self, new_level: int, total_xp: int) -> bool:
        """Update player level and XP."""
        try:
            self.progress_data["player"]["level"] = new_level
            self.progress_data["player"]["total_xp"] = total_xp
            self.progress_data["game_state"]["total_xp"] = total_xp
            
            # Update architect tier based on level
            if new_level >= 5:
                self.progress_data["player"]["architect_tier"] = "Tier 2 - Apprentice"
            if new_level >= 15:
                self.progress_data["player"]["architect_tier"] = "Tier 3 - Architect"
            if new_level >= 30:
                self.progress_data["player"]["architect_tier"] = "Tier 4 - Master Architect"
            if new_level >= 50:
                self.progress_data["player"]["architect_tier"] = "Tier 5 - Grandmaster Architect"
                
            return self.save_progress()
        except Exception as e:
            print(f"Error updating player level: {e}")
            return False
            
    def complete_quest(self, quest: Any) -> bool:
        """Record quest completion."""
        try:
            quest_data = {
                "id": quest.id,
                "title": quest.title,
                "quest_type": quest.quest_type.value if hasattr(quest.quest_type, 'value') else str(quest.quest_type),
                "difficulty": quest.difficulty,
                "xp_reward": quest.xp_reward,
                "completed_at": datetime.now().isoformat()
            }
            
            # Add to completed quests
            self.progress_data["quests"]["completed_quests"].append(quest_data)
            self.progress_data["quests"]["total_completed"] += 1
            
            # Remove from active quests if present
            self.progress_data["quests"]["active_quests"] = [
                q for q in self.progress_data["quests"]["active_quests"] 
                if q.get("id") != quest.id
            ]
            
            # Add to activity log
            self._add_activity_log("quest_completed", quest_data)
            
            return self.save_progress()
        except Exception as e:
            print(f"Error completing quest: {e}")
            return False
            
    def start_quest(self, quest: Any) -> bool:
        """Record quest start."""
        try:
            quest_data = {
                "id": quest.id,
                "title": quest.title,
                "quest_type": quest.quest_type.value if hasattr(quest.quest_type, 'value') else str(quest.quest_type),
                "difficulty": quest.difficulty,
                "started_at": datetime.now().isoformat()
            }
            
            # Add to active quests
            self.progress_data["quests"]["active_quests"].append(quest_data)
            self.progress_data["quests"]["total_started"] += 1
            
            # Add to activity log
            self._add_activity_log("quest_started", quest_data)
            
            return self.save_progress()
        except Exception as e:
            print(f"Error starting quest: {e}")
            return False
            
    def fail_quest(self, quest: Any, reason: str = "Unknown") -> bool:
        """Record quest failure."""
        try:
            quest_data = {
                "id": quest.id,
                "title": quest.title,
                "quest_type": quest.quest_type.value if hasattr(quest.quest_type, 'value') else str(quest.quest_type),
                "difficulty": quest.difficulty,
                "failed_at": datetime.now().isoformat(),
                "failure_reason": reason
            }
            
            # Add to failed quests
            self.progress_data["quests"]["failed_quests"].append(quest_data)
            self.progress_data["quests"]["total_failed"] += 1
            
            # Remove from active quests if present
            self.progress_data["quests"]["active_quests"] = [
                q for q in self.progress_data["quests"]["active_quests"] 
                if q.get("id") != quest.id
            ]
            
            # Add to activity log
            self._add_activity_log("quest_failed", quest_data)
            
            return self.save_progress()
        except Exception as e:
            print(f"Error failing quest: {e}")
            return False
            
    def update_skill(self, skill: Any) -> bool:
        """Update skill progress."""
        try:
            skill_name = skill.name
            skill_data = {
                "name": skill_name,
                "level": skill.get_level(),
                "xp": skill.experience_points,
                "max_level": skill.max_level,
                "last_updated": datetime.now().isoformat()
            }
            
            # Update skill levels
            self.progress_data["skills"]["skill_levels"][skill_name] = skill_data
            
            # Update total skill XP
            total_skill_xp = sum(s.get("xp", 0) for s in self.progress_data["skills"]["skill_levels"].values())
            self.progress_data["skills"]["total_skill_xp"] = total_skill_xp
            
            # Update highest skill
            highest_skill = max(
                self.progress_data["skills"]["skill_levels"].values(),
                key=lambda s: s.get("level", 0)
            )
            self.progress_data["skills"]["highest_skill"] = highest_skill["name"]
            
            # Update total skills count
            self.progress_data["skills"]["total_skills"] = len(self.progress_data["skills"]["skill_levels"])
            
            return self.save_progress()
        except Exception as e:
            print(f"Error updating skill: {e}")
            return False
            
    def earn_achievement(self, achievement: Any) -> bool:
        """Record achievement earned."""
        try:
            achievement_data = {
                "id": achievement.id,
                "name": achievement.name,
                "category": achievement.category,
                "difficulty": achievement.difficulty,
                "xp_reward": achievement.xp_reward,
                "earned_at": datetime.now().isoformat()
            }
            
            # Add to achievements
            self.progress_data["achievements"]["achievement_list"].append(achievement_data)
            self.progress_data["achievements"]["total_earned"] += 1
            
            # Add to recent achievements
            self.progress_data["achievements"]["recent_achievements"].append(achievement_data)
            
            # Keep only last 10 recent achievements
            self.progress_data["achievements"]["recent_achievements"] = \
                self.progress_data["achievements"]["recent_achievements"][-10:]
                
            # Add to activity log
            self._add_activity_log("achievement_earned", achievement_data)
            
            return self.save_progress()
        except Exception as e:
            print(f"Error earning achievement: {e}")
            return False
            
    def update_game_state(self, game_state: Any) -> bool:
        """Update game state."""
        try:
            self.progress_data["game_state"]["current_tier"] = game_state.current_tier
            self.progress_data["game_state"]["total_xp"] = game_state.total_xp
            self.progress_data["game_state"]["last_updated"] = datetime.now().isoformat()
            
            return self.save_progress()
        except Exception as e:
            print(f"Error updating game state: {e}")
            return False
            
    def update_play_time(self, session_hours: float) -> bool:
        """Update play time tracking."""
        try:
            session_data = {
                "start_time": (datetime.now() - timedelta(hours=session_hours)).isoformat(),
                "end_time": datetime.now().isoformat(),
                "duration_hours": session_hours
            }
            
            # Add session
            self.progress_data["play_time"]["sessions"].append(session_data)
            self.progress_data["play_time"]["total_hours"] += session_hours
            
            # Calculate average session length
            total_sessions = len(self.progress_data["play_time"]["sessions"])
            if total_sessions > 0:
                self.progress_data["play_time"]["average_session_length"] = \
                    self.progress_data["play_time"]["total_hours"] / total_sessions
                    
            return self.save_progress()
        except Exception as e:
            print(f"Error updating play time: {e}")
            return False
            
    def get_progress_summary(self) -> Dict[str, Any]:
        """Get a comprehensive progress summary."""
        try:
            summary = {
                "player_info": {
                    "name": self.progress_data["player"]["name"],
                    "level": self.progress_data["player"]["level"],
                    "total_xp": self.progress_data["player"]["total_xp"],
                    "architect_tier": self.progress_data["player"]["architect_tier"],
                    "created_at": self.progress_data["player"]["created_at"],
                    "last_active": self.progress_data["player"]["last_active"]
                },
                "quest_stats": {
                    "total_started": self.progress_data["quests"]["total_started"],
                    "total_completed": self.progress_data["quests"]["total_completed"],
                    "total_failed": self.progress_data["quests"]["total_failed"],
                    "completion_rate": self._calculate_completion_rate(),
                    "active_quests_count": len(self.progress_data["quests"]["active_quests"])
                },
                "skill_stats": {
                    "total_skills": self.progress_data["skills"]["total_skills"],
                    "total_skill_xp": self.progress_data["skills"]["total_skill_xp"],
                    "highest_skill": self.progress_data["skills"]["highest_skill"],
                    "average_skill_level": self._calculate_average_skill_level()
                },
                "achievement_stats": {
                    "total_earned": self.progress_data["achievements"]["total_earned"],
                    "recent_achievements": len(self.progress_data["achievements"]["recent_achievements"])
                },
                "play_time_stats": {
                    "total_hours": self.progress_data["play_time"]["total_hours"],
                    "average_session_length": self.progress_data["play_time"]["average_session_length"],
                    "total_sessions": len(self.progress_data["play_time"]["sessions"])
                }
            }
            
            return summary
        except Exception as e:
            print(f"Error getting progress summary: {e}")
            return {}
            
    def get_recent_activity(self, days: int = 7) -> List[Dict[str, Any]]:
        """Get recent activity from the last N days."""
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            recent_activities = []
            
            for activity in self.progress_data["activity_log"]:
                activity_time = datetime.fromisoformat(activity["timestamp"])
                if activity_time >= cutoff_date:
                    recent_activities.append(activity)
                    
            return recent_activities
        except Exception as e:
            print(f"Error getting recent activity: {e}")
            return []
            
    def export_progress_report(self, output_path: str) -> bool:
        """Export a detailed progress report."""
        try:
            report_content = self._generate_progress_report()
            
            with open(output_path, 'w') as f:
                f.write(report_content)
            return True
        except Exception as e:
            print(f"Error exporting progress report: {e}")
            return False
            
    def _add_activity_log(self, activity_type: str, data: Dict[str, Any]) -> None:
        """Add an activity to the log."""
        activity = {
            "type": activity_type,
            "data": data,
            "timestamp": datetime.now().isoformat()
        }
        
        self.progress_data["activity_log"].append(activity)
        
        # Keep only last 1000 activities
        if len(self.progress_data["activity_log"]) > 1000:
            self.progress_data["activity_log"] = self.progress_data["activity_log"][-1000:]
            
    def _calculate_completion_rate(self) -> float:
        """Calculate quest completion rate."""
        total_quests = self.progress_data["quests"]["total_started"]
        completed_quests = self.progress_data["quests"]["total_completed"]
        
        if total_quests == 0:
            return 0.0
        return round(completed_quests / total_quests * 100, 2)
        
    def _calculate_average_skill_level(self) -> float:
        """Calculate average skill level."""
        skill_levels = self.progress_data["skills"]["skill_levels"].values()
        if not skill_levels:
            return 0.0
            
        total_level = sum(skill.get("level", 0) for skill in skill_levels)
        return round(total_level / len(skill_levels), 2)
        
    def _generate_progress_report(self) -> str:
        """Generate a detailed progress report."""
        summary = self.get_progress_summary()
        
        report = []
        report.append("# Dreamscape MMORPG Progress Report")
        report.append("")
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Player Info
        report.append("## Player Information")
        report.append(f"- **Name**: {summary['player_info']['name']}")
        report.append(f"- **Level**: {summary['player_info']['level']}")
        report.append(f"- **Total XP**: {summary['player_info']['total_xp']:,}")
        report.append(f"- **Architect Tier**: {summary['player_info']['architect_tier']}")
        report.append(f"- **Created**: {summary['player_info']['created_at']}")
        report.append(f"- **Last Active**: {summary['player_info']['last_active']}")
        report.append("")
        
        # Quest Stats
        report.append("## Quest Statistics")
        report.append(f"- **Total Started**: {summary['quest_stats']['total_started']}")
        report.append(f"- **Total Completed**: {summary['quest_stats']['total_completed']}")
        report.append(f"- **Total Failed**: {summary['quest_stats']['total_failed']}")
        report.append(f"- **Completion Rate**: {summary['quest_stats']['completion_rate']}%")
        report.append(f"- **Active Quests**: {summary['quest_stats']['active_quests_count']}")
        report.append("")
        
        # Skill Stats
        report.append("## Skill Statistics")
        report.append(f"- **Total Skills**: {summary['skill_stats']['total_skills']}")
        report.append(f"- **Total Skill XP**: {summary['skill_stats']['total_skill_xp']:,}")
        report.append(f"- **Highest Skill**: {summary['skill_stats']['highest_skill']}")
        report.append(f"- **Average Skill Level**: {summary['skill_stats']['average_skill_level']}")
        report.append("")
        
        # Achievement Stats
        report.append("## Achievement Statistics")
        report.append(f"- **Total Earned**: {summary['achievement_stats']['total_earned']}")
        report.append(f"- **Recent Achievements**: {summary['achievement_stats']['recent_achievements']}")
        report.append("")
        
        # Play Time Stats
        report.append("## Play Time Statistics")
        report.append(f"- **Total Hours**: {summary['play_time_stats']['total_hours']:.1f}")
        report.append(f"- **Average Session**: {summary['play_time_stats']['average_session_length']:.1f} hours")
        report.append(f"- **Total Sessions**: {summary['play_time_stats']['total_sessions']}")
        report.append("")
        
        return "\n".join(report) 