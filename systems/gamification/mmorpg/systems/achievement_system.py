#!/usr/bin/env python3
"""
MMORPG Achievement System
=========================

This module contains ONLY achievement tracking and management logic.
Following the Single Responsibility Principle - this module only handles achievements.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
from ..models import Achievement, Player

class AchievementSystem:
    """
    Manages achievements, badges, and milestone tracking.
    """
    
    def __init__(self):
        """Initialize the achievement system."""
        self.achievements = {}
        self.badges = {}
        self.milestones = {}
        self._initialize_default_achievements()
        
    def _initialize_default_achievements(self):
        """Initialize default achievements."""
        default_achievements = [
            {
                "id": "first_conversation",
                "name": "First Conversation",
                "description": "Complete your first conversation",
                "category": "milestone",
                "difficulty": 1,
                "xp_reward": 10,
                "requirement": {"conversations": 1}
            },
            {
                "id": "conversation_master",
                "name": "Conversation Master",
                "description": "Complete 100 conversations",
                "category": "milestone",
                "difficulty": 5,
                "xp_reward": 100,
                "requirement": {"conversations": 100}
            },
            {
                "id": "skill_novice",
                "name": "Skill Novice",
                "description": "Reach level 10 in any skill",
                "category": "skill",
                "difficulty": 3,
                "xp_reward": 50,
                "requirement": {"skill_level": 10}
            },
            {
                "id": "skill_expert",
                "name": "Skill Expert",
                "description": "Reach level 50 in any skill",
                "category": "skill",
                "difficulty": 7,
                "xp_reward": 200,
                "requirement": {"skill_level": 50}
            },
            {
                "id": "quest_completer",
                "name": "Quest Completer",
                "description": "Complete your first quest",
                "category": "quest",
                "difficulty": 2,
                "xp_reward": 25,
                "requirement": {"quests_completed": 1}
            },
            {
                "id": "quest_master",
                "name": "Quest Master",
                "description": "Complete 50 quests",
                "category": "quest",
                "difficulty": 8,
                "xp_reward": 500,
                "requirement": {"quests_completed": 50}
            }
        ]
        
        for achievement_data in default_achievements:
            achievement = Achievement(
                id=achievement_data["id"],
                name=achievement_data["name"],
                description=achievement_data["description"],
                category=achievement_data["category"],
                difficulty=achievement_data["difficulty"],
                xp_reward=achievement_data["xp_reward"],
                completed_at="",
                evidence="",
                tags=[],
                impact_score=achievement_data["difficulty"]
            )
            self.achievements[achievement.id] = achievement
            
    def check_achievements(self, player: Player, game_state: Dict[str, Any]) -> List[Achievement]:
        """
        Check if player has earned any new achievements.
        Returns list of newly earned achievements.
        """
        newly_earned = []
        
        for achievement in self.achievements.values():
            if achievement.completed_at:  # Already completed
                continue
                
            if self._check_achievement_requirement(achievement, player, game_state):
                achievement.completed_at = datetime.now().isoformat()
                newly_earned.append(achievement)
                
        return newly_earned
        
    def _check_achievement_requirement(self, achievement: Achievement, player: Player, game_state: Dict[str, Any]) -> bool:
        """Check if a specific achievement requirement is met."""
        # This is a simplified check - in a real implementation, you'd have more complex logic
        if "conversations" in achievement.description.lower():
            return player.total_conversations >= 1
        elif "skill" in achievement.description.lower():
            # Check if any skill has reached the required level
            for skill in game_state.get("skills", {}).values():
                if hasattr(skill, 'current_level') and skill.current_level >= 10:
                    return True
        elif "quest" in achievement.description.lower():
            # Check quest completion
            completed_quests = sum(1 for quest in game_state.get("quests", {}).values() 
                                 if hasattr(quest, 'status') and quest.status == "completed")
            return completed_quests >= 1
            
        return False
        
    def get_achievements(self, category: str = None, difficulty: int = None) -> List[Achievement]:
        """Get achievements filtered by category and/or difficulty."""
        filtered = []
        
        for achievement in self.achievements.values():
            if category and achievement.category != category:
                continue
            if difficulty and achievement.difficulty != difficulty:
                continue
            filtered.append(achievement)
            
        return filtered
        
    def get_completed_achievements(self) -> List[Achievement]:
        """Get all completed achievements."""
        return [a for a in self.achievements.values() if a.completed_at]
        
    def get_pending_achievements(self) -> List[Achievement]:
        """Get all pending (uncompleted) achievements."""
        return [a for a in self.achievements.values() if not a.completed_at]
        
    def add_achievement(self, achievement: Achievement) -> bool:
        """Add a new achievement to the system."""
        if achievement.id in self.achievements:
            return False
            
        self.achievements[achievement.id] = achievement
        return True
        
    def remove_achievement(self, achievement_id: str) -> bool:
        """Remove an achievement from the system."""
        if achievement_id in self.achievements:
            del self.achievements[achievement_id]
            return True
        return False
        
    def get_achievement_stats(self) -> Dict[str, Any]:
        """Get comprehensive achievement statistics."""
        total_achievements = len(self.achievements)
        completed_achievements = len(self.get_completed_achievements())
        completion_rate = (completed_achievements / total_achievements * 100) if total_achievements > 0 else 0
        
        # Stats by category
        category_stats = {}
        for achievement in self.achievements.values():
            category = achievement.category
            if category not in category_stats:
                category_stats[category] = {"total": 0, "completed": 0}
            category_stats[category]["total"] += 1
            if achievement.completed_at:
                category_stats[category]["completed"] += 1
                
        # Stats by difficulty
        difficulty_stats = {}
        for achievement in self.achievements.values():
            difficulty = achievement.difficulty
            if difficulty not in difficulty_stats:
                difficulty_stats[difficulty] = {"total": 0, "completed": 0}
            difficulty_stats[difficulty]["total"] += 1
            if achievement.completed_at:
                difficulty_stats[difficulty]["completed"] += 1
                
        return {
            "total_achievements": total_achievements,
            "completed_achievements": completed_achievements,
            "completion_rate": round(completion_rate, 2),
            "category_stats": category_stats,
            "difficulty_stats": difficulty_stats
        }
        
    def get_recent_achievements(self, limit: int = 10) -> List[Achievement]:
        """Get recently completed achievements."""
        completed = self.get_completed_achievements()
        # Sort by completion date (most recent first)
        completed.sort(key=lambda x: x.completed_at, reverse=True)
        return completed[:limit]
        
    def get_achievement_progress(self, player: Player, game_state: Dict[str, Any]) -> Dict[str, Any]:
        """Get progress towards all achievements."""
        progress = {}
        
        for achievement in self.achievements.values():
            if achievement.completed_at:
                progress[achievement.id] = {
                    "completed": True,
                    "progress": 100,
                    "completed_at": achievement.completed_at
                }
            else:
                progress_value = self._calculate_achievement_progress(achievement, player, game_state)
                progress[achievement.id] = {
                    "completed": False,
                    "progress": progress_value,
                    "completed_at": None
                }
                
        return progress
        
    def _calculate_achievement_progress(self, achievement: Achievement, player: Player, game_state: Dict[str, Any]) -> float:
        """Calculate progress percentage for an achievement."""
        # Simplified progress calculation
        if "conversations" in achievement.description.lower():
            if "100" in achievement.description:
                return min(100, (player.total_conversations / 100) * 100)
            else:
                return min(100, (player.total_conversations / 1) * 100)
        elif "skill" in achievement.description.lower():
            # Check highest skill level
            max_skill_level = 0
            for skill in game_state.get("skills", {}).values():
                if hasattr(skill, 'current_level'):
                    max_skill_level = max(max_skill_level, skill.current_level)
            if "50" in achievement.description:
                return min(100, (max_skill_level / 50) * 100)
            else:
                return min(100, (max_skill_level / 10) * 100)
        elif "quest" in achievement.description.lower():
            completed_quests = sum(1 for quest in game_state.get("quests", {}).values() 
                                 if hasattr(quest, 'status') and quest.status == "completed")
            if "50" in achievement.description:
                return min(100, (completed_quests / 50) * 100)
            else:
                return min(100, (completed_quests / 1) * 100)
                
        return 0.0 