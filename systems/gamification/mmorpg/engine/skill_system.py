"""
MMORPG Skill System
Contains the skill management and progression system for the Dreamscape MMORPG.
"""

from typing import Dict, List, Any, Optional, Tuple
import math
import sqlite3
from datetime import datetime

from ..models import Skill, SkillLevel, SkillDefinition, SkillTreeNode


class SkillManager:
    """Manages skill data and operations."""
    
    def __init__(self, db_connection):
        """Initialize the skill manager."""
        self.db_connection = db_connection
        self._initialize_default_skills()
        
    def _initialize_default_skills(self):
        """Initialize default skills in the database."""
        try:
            cursor = self.db_connection.cursor()
            
            # Create skills table if it doesn't exist
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS skills (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    current_level INTEGER DEFAULT 0,
                    experience_points INTEGER DEFAULT 0,
                    max_level INTEGER DEFAULT 100,
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Default skills
            default_skills = [
                ('debugging', 0, 0, 100),
                ('error_handling', 0, 0, 100),
                ('security', 0, 0, 100),
                ('coding', 0, 0, 100),
                ('refactoring', 0, 0, 100),
                ('optimization', 0, 0, 100),
                ('research', 0, 0, 100),
                ('analysis', 0, 0, 100),
                ('documentation', 0, 0, 100),
                ('architecture', 0, 0, 100),
                ('design_patterns', 0, 0, 100),
                ('testing', 0, 0, 100),
                ('system_convergence', 0, 0, 100),
                ('execution_velocity', 0, 0, 100),
                ('strategic_intelligence', 0, 0, 100),
                ('ai_self_organization', 0, 0, 100),
                ('domain_stabilization', 0, 0, 100)
            ]
            
            # Insert default skills
            cursor.executemany('''
                INSERT OR IGNORE INTO skills (name, current_level, experience_points, max_level)
                VALUES (?, ?, ?, ?)
            ''', default_skills)
            
            self.db_connection.commit()
            
        except Exception as e:
            print(f"Error initializing default skills: {e}")
            
    def update_skills_from_achievement(self, achievement):
        """Update skills based on an achievement."""
        try:
            cursor = self.db_connection.cursor()
            
            # Map achievement to skills
            skill_mappings = self._map_achievement_to_skills(achievement)
            
            for skill_name, xp_gain in skill_mappings.items():
                # Get current skill data
                cursor.execute('''
                    SELECT current_level, experience_points, max_level
                    FROM skills WHERE name = ?
                ''', (skill_name,))
                
                result = cursor.fetchone()
                if result:
                    current_level, current_xp, max_level = result
                    
                    # Add XP
                    new_xp = current_xp + xp_gain
                    
                    # Calculate new level
                    new_level = self._calculate_level(new_xp, max_level)
                    
                    # Update skill
                    cursor.execute('''
                        UPDATE skills 
                        SET current_level = ?, experience_points = ?, last_updated = CURRENT_TIMESTAMP
                        WHERE name = ?
                    ''', (new_level, new_xp, skill_name))
                    
            self.db_connection.commit()
            return True
            
        except Exception as e:
            print(f"Error updating skills from achievement: {e}")
            return False
            
    def _map_achievement_to_skills(self, achievement) -> List[str]:
        """Map an achievement to relevant skills."""
        skill_mappings = {}
        
        # Basic mapping based on achievement category
        if achievement.category == 'quest':
            skill_mappings['system_convergence'] = 50
            skill_mappings['execution_velocity'] = 30
        elif achievement.category == 'skill':
            skill_mappings[achievement.name.lower()] = 100
        elif achievement.category == 'project':
            skill_mappings['architecture'] = 75
            skill_mappings['coding'] = 50
            skill_mappings['documentation'] = 25
        elif achievement.category == 'milestone':
            skill_mappings['strategic_intelligence'] = 100
            skill_mappings['domain_stabilization'] = 75
        elif achievement.category == 'special':
            skill_mappings['ai_self_organization'] = 150
            
        return skill_mappings
        
    def get_skills(self) -> List[Any]:
        """Get all skills from the database."""
        try:
            cursor = self.db_connection.cursor()
            cursor.execute('''
                SELECT name, current_level, experience_points, max_level, last_updated
                FROM skills ORDER BY name
            ''')
            
            skills = []
            for row in cursor.fetchall():
                name, current_level, experience_points, max_level, last_updated = row
                
                skill = Skill(
                    name=name,
                    current_level=current_level,
                    experience_points=experience_points,
                    max_level=max_level,
                    last_updated=datetime.fromisoformat(last_updated) if last_updated else None
                )
                skills.append(skill)
                
            return skills
            
        except Exception as e:
            print(f"Error getting skills: {e}")
            return []
            
    def get_skill_stats(self) -> Dict[str, Any]:
        """Get comprehensive skill statistics."""
        try:
            skills = self.get_skills()
            
            if not skills:
                return {}
                
            total_levels = sum(skill.get_level() for skill in skills)
            total_xp = sum(skill.experience_points for skill in skills)
            max_level_skill = max(skills, key=lambda s: s.get_level())
            highest_xp_skill = max(skills, key=lambda s: s.experience_points)
            
            # Calculate average level
            avg_level = total_levels / len(skills) if skills else 0
            
            # Get skill categories
            combat_skills = [s for s in skills if s.name in ['debugging', 'error_handling', 'security']]
            production_skills = [s for s in skills if s.name in ['coding', 'refactoring', 'optimization']]
            gathering_skills = [s for s in skills if s.name in ['research', 'analysis', 'documentation']]
            support_skills = [s for s in skills if s.name in ['architecture', 'design_patterns', 'testing']]
            
            return {
                'total_skills': len(skills),
                'total_levels': total_levels,
                'total_xp': total_xp,
                'average_level': round(avg_level, 2),
                'max_level_skill': max_level_skill.name,
                'max_level': max_level_skill.get_level(),
                'highest_xp_skill': highest_xp_skill.name,
                'highest_xp': highest_xp_skill.experience_points,
                'combat_level': sum(s.get_level() for s in combat_skills),
                'production_level': sum(s.get_level() for s in production_skills),
                'gathering_level': sum(s.get_level() for s in gathering_skills),
                'support_level': sum(s.get_level() for s in support_skills)
            }
            
        except Exception as e:
            print(f"Error getting skill stats: {e}")
            return {}
            
    def _calculate_level(self, xp: int, max_level: int) -> int:
        """Calculate level based on XP."""
        if xp <= 0:
            return 0
            
        level = int(math.sqrt(xp / 100))
        return min(level, max_level)


class SkillSystem:
    """Core skill system for MMORPG progression."""
    
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
        """Generate XP table for level calculations."""
        for level in range(1, 100):
            xp_needed = int((level ** 2) * 100)
            self.XP_TABLE.append(xp_needed)
            
    def _initialize_skills(self) -> Dict[str, Any]:
        """Initialize all skills."""
        skills = {}
        
        # Combat skills
        for skill_name in self.COMBAT_SKILLS:
            skills[skill_name] = {
                'name': skill_name,
                'category': 'combat',
                'current_xp': 0,
                'level': 0,
                'max_level': 99
            }
            
        # Production skills
        for skill_name in self.PRODUCTION_SKILLS:
            skills[skill_name] = {
                'name': skill_name,
                'category': 'production',
                'current_xp': 0,
                'level': 0,
                'max_level': 99
            }
            
        # Gathering skills
        for skill_name in self.GATHERING_SKILLS:
            skills[skill_name] = {
                'name': skill_name,
                'category': 'gathering',
                'current_xp': 0,
                'level': 0,
                'max_level': 99
            }
            
        # Support skills
        for skill_name in self.SUPPORT_SKILLS:
            skills[skill_name] = {
                'name': skill_name,
                'category': 'support',
                'current_xp': 0,
                'level': 0,
                'max_level': 99
            }
            
        return skills
        
    def _initialize_unlocks(self) -> Dict[str, Dict[int, List[str]]]:
        """Initialize skill unlocks."""
        unlocks = {}
        
        # Debugging unlocks
        unlocks['debugging'] = {
            10: ['Basic error detection'],
            25: ['Advanced debugging tools'],
            50: ['Automated debugging'],
            75: ['Predictive debugging'],
            99: ['Master debugger']
        }
        
        # Coding unlocks
        unlocks['coding'] = {
            10: ['Code templates'],
            25: ['Auto-completion'],
            50: ['Code generation'],
            75: ['AI-assisted coding'],
            99: ['Master coder']
        }
        
        # Architecture unlocks
        unlocks['architecture'] = {
            10: ['Basic patterns'],
            25: ['System design'],
            50: ['Enterprise architecture'],
            75: ['Cloud architecture'],
            99: ['Master architect']
        }
        
        return unlocks
        
    def calculate_level(self, xp: int) -> int:
        """Calculate level from XP."""
        for level, required_xp in enumerate(self.XP_TABLE):
            if xp < required_xp:
                return level - 1
        return 99
        
    def get_xp_for_level(self, level: int) -> int:
        """Get XP required for a specific level."""
        if 0 <= level < len(self.XP_TABLE):
            return self.XP_TABLE[level]
        return 0
        
    def get_skill_info(self, skill_name: str, current_xp: int) -> Any:
        """Get comprehensive skill information."""
        if skill_name not in self.skills:
            return None
            
        skill = self.skills[skill_name]
        level = self.calculate_level(current_xp)
        xp_to_next = self.get_xp_for_level(level + 1) - current_xp if level < 99 else 0
        
        unlocks = []
        if skill_name in self.unlocks:
            for unlock_level, unlock_items in self.unlocks[skill_name].items():
                if level >= unlock_level:
                    unlocks.extend(unlock_items)
                    
        return SkillLevel(
            level=level,
            current_xp=current_xp,
            xp_to_next=xp_to_next,
            unlocks=unlocks
        )
        
    def award_xp(self, current_xp: int, xp_award: int) -> Tuple[int, List[int]]:
        """Award XP and return new XP and levels gained."""
        new_xp = current_xp + xp_award
        old_level = self.calculate_level(current_xp)
        new_level = self.calculate_level(new_xp)
        
        levels_gained = []
        for level in range(old_level + 1, new_level + 1):
            levels_gained.append(level)
            
        return new_xp, levels_gained
        
    def get_skill_milestones(self, skill_name: str) -> List[Dict]:
        """Get milestone levels for a skill."""
        milestones = []
        
        if skill_name in self.unlocks:
            for level, unlock_items in self.unlocks[skill_name].items():
                milestones.append({
                    'level': level,
                    'unlocks': unlock_items,
                    'xp_required': self.get_xp_for_level(level)
                })
                
        return milestones
        
    def get_total_level(self, skill_levels: Dict[str, int]) -> int:
        """Calculate total level across all skills."""
        return sum(skill_levels.values())
        
    def get_combat_level(self, combat_skills: Dict[str, int]) -> int:
        """Calculate combat level."""
        combat_xp = sum(combat_skills.get(skill, 0) for skill in self.COMBAT_SKILLS)
        return self.calculate_level(combat_xp)
        
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
            category_xp = sum(skill_levels.get(skill, 0) for skill in skills)
            category_levels[category] = self.calculate_level(category_xp)
            
        return category_levels
        
    def calculate_xp_bonus(self, skill_name: str, skill_levels: Dict[str, int]) -> float:
        """Calculate XP bonus based on skill levels."""
        base_bonus = 0.1
        
        # Add bonus for related skills
        if skill_name in self.COMBAT_SKILLS:
            combat_level = self.get_combat_level(skill_levels)
            base_bonus += combat_level * 0.01
            
        return min(base_bonus, 0.5)  # Cap at 50% bonus
        
    def get_high_scores(self, all_player_skills: Dict[str, Dict[str, int]]) -> Dict[str, List[Tuple[str, int]]]:
        """Get high scores for each skill."""
        high_scores = {}
        
        # Get all skill names
        all_skills = set()
        for player_skills in all_player_skills.values():
            all_skills.update(player_skills.keys())
            
        # Calculate high scores for each skill
        for skill_name in all_skills:
            skill_scores = []
            for player_name, player_skills in all_player_skills.items():
                if skill_name in player_skills:
                    skill_scores.append((player_name, player_skills[skill_name]))
                    
            # Sort by XP (descending) and take top 10
            skill_scores.sort(key=lambda x: x[1], reverse=True)
            high_scores[skill_name] = skill_scores[:10]
            
        return high_scores 