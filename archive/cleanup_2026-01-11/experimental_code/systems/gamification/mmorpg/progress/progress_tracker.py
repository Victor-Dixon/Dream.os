#!/usr/bin/env python3
"""
MMORPG Progress Tracker
=======================

This module contains ONLY progress tracking and persistence logic.
Following the Single Responsibility Principle - this module only handles progress data management.
"""

import json
import os
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from ..models import Quest, Skill, Achievement, GameState

class TrackMMORPGProgress:
    """
    Tracks and persists MMORPG progress data.
    """
    
    def __init__(self, save_file: str = "mmorpg_progress.json"):
        """Initialize the progress tracker with save file path."""
        self.save_file = save_file
        self.progress_data = self._load_progress()
        
    def _load_progress(self) -> Dict[str, Any]:
        """Load progress data from file."""
        if os.path.exists(self.save_file):
            try:
                with open(self.save_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading progress file: {e}")
                return self._initialize_progress()
        else:
            return self._initialize_progress()
            
    def _initialize_progress(self) -> Dict[str, Any]:
        """Initialize default progress data."""
        return {
            "player": {
                "name": "Dreamscape Player",
                "level": 1,
                "xp": 0,
                "total_xp": 0,
                "architect_tier": "Tier 1 - Novice",
                "created_at": datetime.now().isoformat(),
                "last_active": datetime.now().isoformat()
            },
            "skills": {},
            "quests": {
                "active": {},
                "completed": {},
                "failed": {}
            },
            "achievements": [],
            "game_state": {
                "current_tier": 1,
                "total_xp": 0,
                "skills": {},
                "quests": {},
                "architect_tiers": {},
                "guilds": {},
                "last_updated": datetime.now().isoformat()
            },
            "play_time": {
                "total_hours": 0.0,
                "sessions": []
            },
            "recent_activity": []
        }
        
    def save_progress(self) -> bool:
        """Save progress data to file."""
        try:
            # Update last active timestamp
            self.progress_data["player"]["last_active"] = datetime.now().isoformat()
            self.progress_data["game_state"]["last_updated"] = datetime.now().isoformat()
            
            with open(self.save_file, 'w', encoding='utf-8') as f:
                json.dump(self.progress_data, f, indent=2, default=str)
            return True
        except IOError as e:
            print(f"Error saving progress: {e}")
            return False
            
    def update_player_level(self, new_level: int, total_xp: int) -> bool:
        """Update player level and XP."""
        try:
            self.progress_data["player"]["level"] = new_level
            self.progress_data["player"]["xp"] = total_xp
            self.progress_data["player"]["total_xp"] = total_xp
            self.progress_data["game_state"]["total_xp"] = total_xp
            
            # Update architect tier based on level
            if new_level >= 100:
                tier = "Tier 5 - Master"
            elif new_level >= 75:
                tier = "Tier 4 - Expert"
            elif new_level >= 50:
                tier = "Tier 3 - Journeyman"
            elif new_level >= 25:
                tier = "Tier 2 - Apprentice"
            else:
                tier = "Tier 1 - Novice"
                
            self.progress_data["player"]["architect_tier"] = tier
            self.progress_data["game_state"]["current_tier"] = new_level // 25 + 1
            
            return self.save_progress()
        except Exception as e:
            print(f"Error updating player level: {e}")
            return False
            
    def complete_quest(self, quest: Quest) -> bool:
        """Mark a quest as completed."""
        try:
            quest_id = quest.id
            
            # Move from active to completed
            if quest_id in self.progress_data["quests"]["active"]:
                quest_data = self.progress_data["quests"]["active"].pop(quest_id)
                quest_data["status"] = "completed"
                quest_data["completed_at"] = datetime.now().isoformat()
                self.progress_data["quests"]["completed"][quest_id] = quest_data
                
                # Update game state
                self.progress_data["game_state"]["quests"][quest_id] = quest_data
                
                # Add to recent activity
                self._add_recent_activity("quest_completed", {
                    "quest_id": quest_id,
                    "quest_name": quest.title,
                    "xp_reward": quest.xp_reward
                })
                
                return self.save_progress()
            return False
        except Exception as e:
            print(f"Error completing quest: {e}")
            return False
            
    def start_quest(self, quest: Quest) -> bool:
        """Start a new quest."""
        try:
            quest_data = {
                "id": quest.id,
                "title": quest.title,
                "description": quest.description,
                "quest_type": quest.quest_type.value,
                "difficulty": quest.difficulty,
                "xp_reward": quest.xp_reward,
                "skill_rewards": quest.skill_rewards,
                "status": "active",
                "started_at": datetime.now().isoformat()
            }
            
            self.progress_data["quests"]["active"][quest.id] = quest_data
            
            # Add to recent activity
            self._add_recent_activity("quest_started", {
                "quest_id": quest.id,
                "quest_name": quest.title
            })
            
            return self.save_progress()
        except Exception as e:
            print(f"Error starting quest: {e}")
            return False
            
    def fail_quest(self, quest: Quest, reason: str = "Unknown") -> bool:
        """Mark a quest as failed."""
        try:
            quest_id = quest.id
            
            # Move from active to failed
            if quest_id in self.progress_data["quests"]["active"]:
                quest_data = self.progress_data["quests"]["active"].pop(quest_id)
                quest_data["status"] = "failed"
                quest_data["failed_at"] = datetime.now().isoformat()
                quest_data["failure_reason"] = reason
                self.progress_data["quests"]["failed"][quest_id] = quest_data
                
                # Add to recent activity
                self._add_recent_activity("quest_failed", {
                    "quest_id": quest_id,
                    "quest_name": quest.title,
                    "reason": reason
                })
                
                return self.save_progress()
            return False
        except Exception as e:
            print(f"Error failing quest: {e}")
            return False
            
    def update_skill(self, skill: Skill) -> bool:
        """Update skill progress."""
        try:
            skill_data = {
                "name": skill.name,
                "current_level": skill.current_level,
                "experience_points": skill.experience_points,
                "max_level": skill.max_level,
                "last_updated": skill.last_updated.isoformat() if skill.last_updated else datetime.now().isoformat()
            }
            
            self.progress_data["skills"][skill.name] = skill_data
            self.progress_data["game_state"]["skills"][skill.name] = skill_data
            
            # Add to recent activity
            self._add_recent_activity("skill_updated", {
                "skill_name": skill.name,
                "new_level": skill.current_level,
                "xp": skill.experience_points
            })
            
            return self.save_progress()
        except Exception as e:
            print(f"Error updating skill: {e}")
            return False
            
    def earn_achievement(self, achievement: Achievement) -> bool:
        """Record an earned achievement."""
        try:
            achievement_data = {
                "id": achievement.id,
                "name": achievement.name,
                "description": achievement.description,
                "category": achievement.category,
                "difficulty": achievement.difficulty,
                "xp_reward": achievement.xp_reward,
                "completed_at": achievement.completed_at,
                "evidence": achievement.evidence,
                "tags": achievement.tags,
                "impact_score": achievement.impact_score,
                "earned_at": datetime.now().isoformat()
            }
            
            self.progress_data["achievements"].append(achievement_data)
            
            # Add to recent activity
            self._add_recent_activity("achievement_earned", {
                "achievement_id": achievement.id,
                "achievement_name": achievement.name,
                "xp_reward": achievement.xp_reward
            })
            
            return self.save_progress()
        except Exception as e:
            print(f"Error earning achievement: {e}")
            return False
            
    def update_game_state(self, game_state: GameState) -> bool:
        """Update the overall game state."""
        try:
            self.progress_data["game_state"] = {
                "current_tier": game_state.current_tier,
                "total_xp": game_state.total_xp,
                "skills": {name: {
                    "name": skill.name,
                    "current_level": skill.current_level,
                    "experience_points": skill.experience_points,
                    "max_level": skill.max_level,
                    "last_updated": skill.last_updated.isoformat() if skill.last_updated else datetime.now().isoformat()
                } for name, skill in game_state.skills.items()},
                "quests": {quest_id: {
                    "id": quest.id,
                    "title": quest.title,
                    "status": quest.status,
                    "created_at": quest.created_at.isoformat() if quest.created_at else None,
                    "completed_at": quest.completed_at.isoformat() if quest.completed_at else None
                } for quest_id, quest in game_state.quests.items()},
                "architect_tiers": {tier: {
                    "tier_level": arch_tier.tier_level,
                    "tier_name": arch_tier.tier_name,
                    "experience_required": arch_tier.experience_required,
                    "abilities_unlocked": arch_tier.abilities_unlocked,
                    "achieved_at": arch_tier.achieved_at.isoformat() if arch_tier.achieved_at else None
                } for tier, arch_tier in game_state.architect_tiers.items()},
                "guilds": {guild_id: {
                    "id": guild.id,
                    "name": guild.name,
                    "description": guild.description,
                    "leader_id": guild.leader_id,
                    "members": guild.members,
                    "created_at": guild.created_at.isoformat() if guild.created_at else None
                } for guild_id, guild in game_state.guilds.items()},
                "last_updated": datetime.now().isoformat()
            }
            
            return self.save_progress()
        except Exception as e:
            print(f"Error updating game state: {e}")
            return False
            
    def update_play_time(self, session_hours: float) -> bool:
        """Update total play time."""
        try:
            self.progress_data["play_time"]["total_hours"] += session_hours
            
            # Add session record
            session_data = {
                "date": datetime.now().isoformat(),
                "hours": session_hours
            }
            self.progress_data["play_time"]["sessions"].append(session_data)
            
            # Keep only last 100 sessions
            if len(self.progress_data["play_time"]["sessions"]) > 100:
                self.progress_data["play_time"]["sessions"] = self.progress_data["play_time"]["sessions"][-100:]
                
            return self.save_progress()
        except Exception as e:
            print(f"Error updating play time: {e}")
            return False
            
    def get_progress_summary(self) -> Dict[str, Any]:
        """Get a summary of current progress."""
        try:
            player = self.progress_data["player"]
            skills = self.progress_data["skills"]
            quests = self.progress_data["quests"]
            achievements = self.progress_data["achievements"]
            play_time = self.progress_data["play_time"]
            
            # Calculate skill statistics
            total_skills = len(skills)
            avg_skill_level = sum(skill["current_level"] for skill in skills.values()) / total_skills if total_skills > 0 else 0
            
            # Calculate quest statistics
            active_quests = len(quests["active"])
            completed_quests = len(quests["completed"])
            failed_quests = len(quests["failed"])
            total_quests = active_quests + completed_quests + failed_quests
            
            # Calculate achievement statistics
            total_achievements = len(achievements)
            total_achievement_xp = sum(achievement["xp_reward"] for achievement in achievements)
            
            return {
                "player": {
                    "name": player["name"],
                    "level": player["level"],
                    "xp": player["xp"],
                    "total_xp": player["total_xp"],
                    "architect_tier": player["architect_tier"],
                    "created_at": player["created_at"],
                    "last_active": player["last_active"]
                },
                "skills": {
                    "total": total_skills,
                    "average_level": round(avg_skill_level, 2),
                    "highest_level": max((skill["current_level"] for skill in skills.values()), default=0)
                },
                "quests": {
                    "active": active_quests,
                    "completed": completed_quests,
                    "failed": failed_quests,
                    "total": total_quests,
                    "completion_rate": (completed_quests / total_quests * 100) if total_quests > 0 else 0
                },
                "achievements": {
                    "total": total_achievements,
                    "total_xp_earned": total_achievement_xp
                },
                "play_time": {
                    "total_hours": play_time["total_hours"],
                    "recent_sessions": len(play_time["sessions"])
                }
            }
        except Exception as e:
            print(f"Error getting progress summary: {e}")
            return {}
            
    def get_recent_activity(self, days: int = 7) -> List[Dict[str, Any]]:
        """Get recent activity within the specified number of days."""
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            recent_activities = []
            
            for activity in self.progress_data["recent_activity"]:
                activity_date = datetime.fromisoformat(activity["timestamp"])
                if activity_date >= cutoff_date:
                    recent_activities.append(activity)
                    
            return recent_activities
        except Exception as e:
            print(f"Error getting recent activity: {e}")
            return []
            
    def _add_recent_activity(self, activity_type: str, data: Dict[str, Any]):
        """Add an activity to the recent activity log."""
        activity = {
            "type": activity_type,
            "data": data,
            "timestamp": datetime.now().isoformat()
        }
        
        self.progress_data["recent_activity"].append(activity)
        
        # Keep only last 100 activities
        if len(self.progress_data["recent_activity"]) > 100:
            self.progress_data["recent_activity"] = self.progress_data["recent_activity"][-100:]
            
    def export_progress_report(self, output_path: str) -> bool:
        """Export a detailed progress report to a file."""
        try:
            report_content = self._generate_progress_report()
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(report_content)
            return True
        except Exception as e:
            print(f"Error exporting progress report: {e}")
            return False
            
    def _generate_progress_report(self) -> str:
        """Generate a detailed progress report."""
        summary = self.get_progress_summary()
        recent_activity = self.get_recent_activity(7)
        
        report_lines = []
        report_lines.append("# MMORPG Progress Report")
        report_lines.append(f"Generated on: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}")
        report_lines.append("")
        
        # Player Information
        report_lines.append("## Player Information")
        player = summary["player"]
        report_lines.append(f"- **Name:** {player['name']}")
        report_lines.append(f"- **Level:** {player['level']}")
        report_lines.append(f"- **Total XP:** {player['total_xp']:,}")
        report_lines.append(f"- **Architect Tier:** {player['architect_tier']}")
        report_lines.append(f"- **Created:** {player['created_at']}")
        report_lines.append(f"- **Last Active:** {player['last_active']}")
        report_lines.append("")
        
        # Skills Summary
        report_lines.append("## Skills Summary")
        skills = summary["skills"]
        report_lines.append(f"- **Total Skills:** {skills['total']}")
        report_lines.append(f"- **Average Level:** {skills['average_level']}")
        report_lines.append(f"- **Highest Level:** {skills['highest_level']}")
        report_lines.append("")
        
        # Quests Summary
        report_lines.append("## Quests Summary")
        quests = summary["quests"]
        report_lines.append(f"- **Active Quests:** {quests['active']}")
        report_lines.append(f"- **Completed Quests:** {quests['completed']}")
        report_lines.append(f"- **Failed Quests:** {quests['failed']}")
        report_lines.append(f"- **Total Quests:** {quests['total']}")
        report_lines.append(f"- **Completion Rate:** {quests['completion_rate']:.1f}%")
        report_lines.append("")
        
        # Achievements Summary
        report_lines.append("## Achievements Summary")
        achievements = summary["achievements"]
        report_lines.append(f"- **Total Achievements:** {achievements['total']}")
        report_lines.append(f"- **Total XP Earned:** {achievements['total_xp_earned']:,}")
        report_lines.append("")
        
        # Play Time Summary
        report_lines.append("## Play Time Summary")
        play_time = summary["play_time"]
        report_lines.append(f"- **Total Hours:** {play_time['total_hours']:.1f}")
        report_lines.append(f"- **Recent Sessions:** {play_time['recent_sessions']}")
        report_lines.append("")
        
        # Recent Activity
        report_lines.append("## Recent Activity (Last 7 Days)")
        if recent_activity:
            for activity in recent_activity[-10:]:  # Last 10 activities
                timestamp = datetime.fromisoformat(activity["timestamp"]).strftime("%Y-%m-%d %H:%M")
                report_lines.append(f"- **{timestamp}:** {activity['type']} - {activity['data']}")
        else:
            report_lines.append("- No recent activity")
            
        return "\n".join(report_lines) 