#!/usr/bin/env python3
"""
MMORPG Skills System
====================

This module contains ONLY skill system management logic.
Following the Single Responsibility Principle - this module only handles skill operations.
"""

import math
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from .mmorpg_system import SkillLevel
from .models import Skill, SkillType, SkillDefinition

class SkillSystem:
    """
    Core skill system responsible for:
    - Skill XP calculation
    - Level progression
    - Skill unlocks
    - Skill categories
    """
    
    XP_TABLE = [0]
    COMBAT_SKILLS = ["debugging", "error_handling", "security"]
    PRODUCTION_SKILLS = ["coding", "refactoring", "optimization"]
    GATHERING_SKILLS = ["research", "analysis", "documentation"]
    SUPPORT_SKILLS = ["architecture", "design_patterns", "testing"]
    
    def __init__(self):
        """Initialize the skill system."""
        self._generate_xp_table()
        self.skills = self._initialize_skills()
        self.unlocks = self._initialize_unlocks()
        
    def _generate_xp_table(self):
        """Generate XP table for skill levels."""
        self.XP_TABLE = [0]
        for level in range(1, 100):
            xp_needed = int(level ** 1.5 * 100)
            self.XP_TABLE.append(xp_needed)
            
    def _initialize_skills(self) -> Dict[str, Skill]:
        """Initialize default skills."""
        skills = {}
        skill_definitions = {
            "python": SkillDefinition("python", "Python programming", "technical", ["programming", "backend"], 99),
            "javascript": SkillDefinition("javascript", "JavaScript programming", "technical", ["programming", "frontend"], 99),
            "architecture": SkillDefinition("architecture", "System architecture", "technical", ["design", "planning"], 99),
            "testing": SkillDefinition("testing", "Software testing", "technical", ["quality", "validation"], 99),
            "debugging": SkillDefinition("debugging", "Debugging and troubleshooting", "technical", ["problem_solving"], 99),
            "optimization": SkillDefinition("optimization", "Performance optimization", "technical", ["efficiency"], 99),
            "documentation": SkillDefinition("documentation", "Technical documentation", "technical", ["communication"], 99),
            "research": SkillDefinition("research", "Technical research", "technical", ["analysis"], 99),
            "analysis": SkillDefinition("analysis", "Data analysis", "technical", ["research"], 99),
            "security": SkillDefinition("security", "Security practices", "technical", ["protection"], 99),
        }
        
        for skill_name, definition in skill_definitions.items():
            skills[skill_name] = Skill(
                name=skill_name,
                current_level=0,
                experience_points=0,
                max_level=definition.max_level,
                last_updated=datetime.now()
            )
            
        return skills
        
    def _initialize_unlocks(self) -> Dict[str, Dict[int, List[str]]]:
        """Initialize skill unlocks."""
        unlocks = {}
        for skill_name in self.skills.keys():
            unlocks[skill_name] = {}
            for level in range(5, 100, 5):  # Every 5 levels
                unlocks[skill_name][level] = [f"{skill_name}_ability_{level}"]
        return unlocks
        
    def calculate_level(self, xp: int) -> int:
        """Calculate skill level from XP."""
        for level, required_xp in enumerate(self.XP_TABLE):
            if xp < required_xp:
                return max(1, level - 1)
        return 99
        
    def get_xp_for_level(self, level: int) -> int:
        """Get XP required for a specific level."""
        if 0 <= level < len(self.XP_TABLE):
            return self.XP_TABLE[level]
        return 0
        
    def get_skill_info(self, skill_name: str, current_xp: int) -> SkillLevel:
        """Get detailed skill information."""
        level = self.calculate_level(current_xp)
        xp_to_next = self.get_xp_for_level(level + 1) - current_xp if level < 99 else 0
        unlocks = self.unlocks.get(skill_name, {}).get(level, [])
        
        return SkillLevel(
            level=level,
            current_xp=current_xp,
            xp_to_next=xp_to_next,
            unlocks=unlocks
        )
        
    def award_xp(self, current_xp: int, xp_award: int) -> Tuple[int, List[int]]:
        """Award XP and return new XP and levels gained."""
        old_level = self.calculate_level(current_xp)
        new_xp = current_xp + xp_award
        new_level = self.calculate_level(new_xp)
        
        levels_gained = []
        for level in range(old_level + 1, new_level + 1):
            levels_gained.append(level)
            
        return new_xp, levels_gained
        
    def get_skill_milestones(self, skill_name: str) -> List[Dict]:
        """Get skill milestones."""
        milestones = []
        skill = self.skills.get(skill_name)
        if skill:
            for level in range(5, 100, 5):
                xp_required = self.get_xp_for_level(level)
                milestones.append({
                    'level': level,
                    'xp_required': xp_required,
                    'unlocks': self.unlocks.get(skill_name, {}).get(level, [])
                })
        return milestones
        
    def get_total_level(self, skill_levels: Dict[str, int]) -> int:
        """Calculate total level from all skills."""
        return sum(skill_levels.values())
        
    def get_combat_level(self, combat_skills: Dict[str, int]) -> int:
        """Calculate combat level from combat skills."""
        combat_total = sum(combat_skills.get(skill, 0) for skill in self.COMBAT_SKILLS)
        return max(1, combat_total // len(self.COMBAT_SKILLS))
        
    def get_skill_category_levels(self, skill_levels: Dict[str, int]) -> Dict[str, float]:
        """Get average levels for each skill category."""
        categories = {
            'combat': self.COMBAT_SKILLS,
            'production': self.PRODUCTION_SKILLS,
            'gathering': self.GATHERING_SKILLS,
            'support': self.SUPPORT_SKILLS
        }
        
        category_levels = {}
        for category, skills in categories.items():
            category_skills = [skill_levels.get(skill, 0) for skill in skills]
            if category_skills:
                category_levels[category] = sum(category_skills) / len(category_skills)
            else:
                category_levels[category] = 0.0
                
        return category_levels
        
    def calculate_xp_bonus(self, skill_name: str, skill_levels: Dict[str, int]) -> float:
        """Calculate XP bonus based on related skills."""
        skill = self.skills.get(skill_name)
        if skill:
            related_skills = skill.related_skills if hasattr(skill, 'related_skills') else []
            bonus = 0.0
            for related_skill in related_skills:
                related_level = skill_levels.get(related_skill, 0)
                bonus += related_level * 0.01  # 1% bonus per level
            return min(bonus, 0.5)  # Cap at 50% bonus
        return 0.0
        
    def get_high_scores(self, all_player_skills: Dict[str, Dict[str, int]]) -> Dict[str, List[Tuple[str, int]]]:
        """Get high scores for each skill."""
        high_scores = {}
        
        # Get all unique skill names
        all_skills = set()
        for player_skills in all_player_skills.values():
            all_skills.update(player_skills.keys())
            
        for skill_name in all_skills:
            skill_scores = []
            for player_name, player_skills in all_player_skills.items():
                level = player_skills.get(skill_name, 0)
                skill_scores.append((player_name, level))
                
            # Sort by level (descending) and take top 10
            skill_scores.sort(key=lambda x: x[1], reverse=True)
            high_scores[skill_name] = skill_scores[:10]
            
        return high_scores

class SkillManager:
    """
    Skill manager responsible for:
    - Database operations for skills
    - Skill persistence
    - Skill queries
    """
    
    def __init__(self, db_connection):
        """Initialize skill manager with database connection."""
        self.db = db_connection
        self._initialize_default_skills()
        
    def _initialize_default_skills(self):
        """Initialize default skills in database."""
        default_skills = [
            ("python", "Python programming", "technical"),
            ("javascript", "JavaScript programming", "technical"),
            ("architecture", "System architecture", "technical"),
            ("testing", "Software testing", "technical"),
            ("debugging", "Debugging and troubleshooting", "technical"),
            ("optimization", "Performance optimization", "technical"),
            ("documentation", "Technical documentation", "technical"),
            ("research", "Technical research", "technical"),
            ("analysis", "Data analysis", "technical"),
            ("security", "Security practices", "technical"),
        ]
        
        cursor = self.db.cursor()
        for skill_name, description, category in default_skills:
            cursor.execute("""
                INSERT OR IGNORE INTO skills (name, description, category, current_level, current_xp, max_level)
                VALUES (?, ?, ?, 0, 0, 99)
            """, (skill_name, description, category))
        self.db.commit()
        
    def update_skills_from_achievement(self, achievement):
        """Update skills based on achievement completion."""
        # Map achievements to skill improvements
        skill_improvements = self._map_achievement_to_skills(achievement)
        
        cursor = self.db.cursor()
        for skill_name, xp_gain in skill_improvements.items():
            cursor.execute("""
                UPDATE skills 
                SET current_xp = current_xp + ?, 
                    current_level = ?, 
                    last_updated = ?
                WHERE name = ?
            """, (xp_gain, self._calculate_level_from_xp(xp_gain), datetime.now(), skill_name))
        self.db.commit()
        
    def _map_achievement_to_skills(self, achievement) -> List[str]:
        """Map achievement to relevant skills."""
        # This is a simplified mapping - can be enhanced
        skill_mapping = {
            "code_review": ["python", "javascript", "architecture"],
            "bug_fix": ["debugging", "testing"],
            "performance_improvement": ["optimization", "analysis"],
            "security_audit": ["security", "testing"],
            "documentation": ["documentation", "communication"],
            "research": ["research", "analysis"],
        }
        
        achievement_type = achievement.get('type', 'general')
        return skill_mapping.get(achievement_type, [])
        
    def get_skills(self) -> List[Any]:
        """Get all skills from database."""
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM skills ORDER BY current_level DESC")
        return cursor.fetchall()
        
    def get_skill_stats(self) -> Dict[str, Any]:
        """Get skill statistics."""
        cursor = self.db.cursor()
        cursor.execute("""
            SELECT 
                COUNT(*) as total_skills,
                AVG(current_level) as avg_level,
                MAX(current_level) as max_level,
                SUM(current_xp) as total_xp
            FROM skills
        """)
        stats = cursor.fetchone()
        
        return {
            'total_skills': stats[0],
            'average_level': round(stats[1], 2) if stats[1] else 0,
            'max_level': stats[2] or 0,
            'total_xp': stats[3] or 0
        } 