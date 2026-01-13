"""
MMORPG Skill System
Contains the skill system and skill manager for the Dreamscape MMORPG.
"""

import logging
import math
from typing import Dict, List, Any, Tuple
from ..models import SkillDefinition, SkillLevel

logger = logging.getLogger(__name__)


class SkillSystem:
    """Main skill system for the Dreamscape MMORPG."""
    
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
        """Generate the XP table for skill levels."""
        for level in range(1, 100):
            points = math.floor(sum(math.floor(level + 300 * (2 ** (level / 7.0))) for level in range(1, level)) / 4)
            self.XP_TABLE.append(points)

    def _initialize_skills(self) -> Dict[str, SkillDefinition]:
        """Initialize all available skills."""
        return {
            "debugging": SkillDefinition(
                name="Debugging",
                description="Combat bugs and errors in code",
                category="combat",
                related_skills=["error_handling", "analysis"]
            ),
            "error_handling": SkillDefinition(
                name="Error Handling",
                description="Defend against and manage errors",
                category="combat",
                related_skills=["debugging", "security"]
            ),
            "security": SkillDefinition(
                name="Security",
                description="Protect code and systems",
                category="combat",
                related_skills=["error_handling", "architecture"]
            ),
            "coding": SkillDefinition(
                name="Coding",
                description="Write efficient and clean code",
                category="production",
                related_skills=["refactoring", "design_patterns"]
            ),
            "refactoring": SkillDefinition(
                name="Refactoring",
                description="Improve existing code",
                category="production",
                related_skills=["coding", "optimization"]
            ),
            "optimization": SkillDefinition(
                name="Optimization",
                description="Enhance code performance",
                category="production",
                related_skills=["refactoring", "performance"]
            ),
            "research": SkillDefinition(
                name="Research",
                description="Gather information and solutions",
                category="gathering",
                related_skills=["analysis", "documentation"]
            ),
            "analysis": SkillDefinition(
                name="Analysis",
                description="Understand complex systems",
                category="gathering",
                related_skills=["research", "architecture"]
            ),
            "documentation": SkillDefinition(
                name="Documentation",
                description="Create and maintain documentation",
                category="gathering",
                related_skills=["research", "technical_writing"]
            ),
            "architecture": SkillDefinition(
                name="Architecture",
                description="Design system structures",
                category="support",
                related_skills=["design_patterns", "system_design"]
            ),
            "design_patterns": SkillDefinition(
                name="Design Patterns",
                description="Implement reusable solutions",
                category="support",
                related_skills=["architecture", "coding"]
            ),
            "testing": SkillDefinition(
                name="Testing",
                description="Verify code quality",
                category="support",
                related_skills=["debugging", "quality_assurance"]
            )
        }

    def _initialize_unlocks(self) -> Dict[str, Dict[int, List[str]]]:
        """Initialize skill unlocks for each level."""
        return {
            "debugging": {
                1: ["Basic error messages"],
                10: ["Stack trace analysis"],
                20: ["Debugger tools"],
                30: ["Advanced breakpoints"],
                40: ["Memory inspection"],
                50: ["Performance profiling"],
                60: ["Thread debugging"],
                70: ["Remote debugging"],
                80: ["Kernel debugging"],
                90: ["Time travel debugging"],
                99: ["Master debugger cape"]
            },
            "coding": {
                1: ["Basic syntax"],
                10: ["Functions and classes"],
                20: ["Design patterns"],
                30: ["APIs and interfaces"],
                40: ["System integration"],
                50: ["Microservices"],
                60: ["Distributed systems"],
                70: ["Cloud architecture"],
                80: ["System scaling"],
                90: ["Enterprise architecture"],
                99: ["Master coder cape"]
            },
        }

    def calculate_level(self, xp: int) -> int:
        """Calculate skill level from XP."""
        for level, requirement in enumerate(self.XP_TABLE):
            if xp < requirement:
                return max(1, level - 1)
        return 99

    def get_xp_for_level(self, level: int) -> int:
        """Get XP required for a specific level."""
        if level < 1 or level > 99:
            raise ValueError("Level must be between 1 and 99")
        return self.XP_TABLE[level]

    def get_skill_info(self, skill_name: str, current_xp: int) -> SkillLevel:
        """Get detailed information about a skill."""
        if skill_name not in self.skills:
            raise ValueError(f"Unknown skill: {skill_name}")
        
        current_level = self.calculate_level(current_xp)
        next_level = min(current_level + 1, 99)
        xp_to_next = self.XP_TABLE[next_level] - current_xp
        current_unlocks = self.unlocks.get(skill_name, {}).get(current_level, [])
        
        return SkillLevel(
            level=current_level,
            current_xp=current_xp,
            xp_to_next=xp_to_next,
            unlocks=current_unlocks
        )

    def award_xp(self, current_xp: int, xp_award: int) -> Tuple[int, List[int]]:
        """Award XP and return new total and levels gained."""
        old_level = self.calculate_level(current_xp)
        new_total = current_xp + xp_award
        new_level = self.calculate_level(new_total)
        levels_gained = []
        
        if new_level > old_level:
            levels_gained = list(range(old_level + 1, new_level + 1))
        
        return new_total, levels_gained

    def get_skill_milestones(self, skill_name: str) -> List[Dict]:
        """Get all milestones for a skill."""
        if skill_name not in self.skills:
            raise ValueError(f"Unknown skill: {skill_name}")
        
        milestones = []
        for level, unlocks in self.unlocks.get(skill_name, {}).items():
            milestones.append({
                "level": level,
                "xp_required": self.XP_TABLE[level],
                "unlocks": unlocks
            })
        return sorted(milestones, key=lambda x: x["level"])

    def get_total_level(self, skill_levels: Dict[str, int]) -> int:
        """Calculate total level from all skills."""
        return sum(skill_levels.values())

    def get_combat_level(self, combat_skills: Dict[str, int]) -> int:
        """Calculate combat level from combat skills."""
        debug_level = combat_skills.get("debugging", 1)
        error_level = combat_skills.get("error_handling", 1)
        security_level = combat_skills.get("security", 1)
        base = (debug_level + error_level + security_level) / 3
        return min(99, math.floor(base))

    def get_skill_category_levels(self, skill_levels: Dict[str, int]) -> Dict[str, float]:
        """Calculate average levels for each skill category."""
        categories = {
            "combat": self.COMBAT_SKILLS,
            "production": self.PRODUCTION_SKILLS,
            "gathering": self.GATHERING_SKILLS,
            "support": self.SUPPORT_SKILLS
        }
        averages = {}
        
        for category, skills in categories.items():
            levels = [skill_levels.get(skill, 1) for skill in skills]
            averages[category] = sum(levels) / len(levels)
        
        return averages

    def calculate_xp_bonus(self, skill_name: str, skill_levels: Dict[str, int]) -> float:
        """Calculate XP bonus from related skills."""
        if skill_name not in self.skills:
            return 1.0
        
        skill_def = self.skills[skill_name]
        related_levels = [skill_levels.get(skill, 1) for skill in skill_def.related_skills]
        bonus = sum(level / 99 for level in related_levels) / len(related_levels)
        return 1.0 + (bonus * 0.1)

    def get_high_scores(self, all_player_skills: Dict[str, Dict[str, int]]) -> Dict[str, List[Tuple[str, int]]]:
        """Get high scores for all skills."""
        high_scores = {skill: [] for skill in self.skills}
        high_scores["total"] = []
        
        for player_id, skills in all_player_skills.items():
            for skill, xp in skills.items():
                if skill in high_scores:
                    level = self.calculate_level(xp)
                    high_scores[skill].append((player_id, level))
            
            total = sum(self.calculate_level(xp) for xp in skills.values())
            high_scores["total"].append((player_id, total))
        
        for skill in high_scores:
            high_scores[skill] = sorted(high_scores[skill], key=lambda x: x[1], reverse=True)
        
        return high_scores


class SkillManager:
    """Manages skill operations and database interactions."""
    
    def __init__(self, db_connection):
        """Initialize the skill manager."""
        self.db_connection = db_connection
        self._initialize_default_skills()

    def _initialize_default_skills(self):
        """Initialize default skills in the database."""
        default_skills = [
            ("debugging", "Debugging", "Combat bugs and errors in code", "combat"),
            ("error_handling", "Error Handling", "Defend against and manage errors", "combat"),
            ("security", "Security", "Protect code and systems", "combat"),
            ("coding", "Coding", "Write efficient and clean code", "production"),
            ("refactoring", "Refactoring", "Improve existing code", "production"),
            ("optimization", "Optimization", "Enhance code performance", "production"),
            ("research", "Research", "Gather information and solutions", "gathering"),
            ("analysis", "Analysis", "Understand complex systems", "gathering"),
            ("documentation", "Documentation", "Create and maintain documentation", "gathering"),
            ("architecture", "Architecture", "Design system structures", "support"),
            ("design_patterns", "Design Patterns", "Implement reusable solutions", "support"),
            ("testing", "Testing", "Verify code quality", "support")
        ]

        cursor = self.db_connection.cursor()
        for skill_id, name, description, category in default_skills:
            cursor.execute("""
                INSERT OR IGNORE INTO skills (name, description, category, current_level, current_xp)
                VALUES (?, ?, ?, 0, 0)
            """, (name, description, category))
        self.db_connection.commit()

    def update_skills_from_achievement(self, achievement):
        """Update skills based on achievement completion."""
        skill_mapping = self._map_achievement_to_skills(achievement)
        
        cursor = self.db_connection.cursor()
        for skill_id in skill_mapping:
            cursor.execute("""
                UPDATE skills 
                SET current_xp = current_xp + ?, 
                    current_level = (SELECT level FROM skill_levels WHERE xp_required <= current_xp ORDER BY xp_required DESC LIMIT 1)
                WHERE name = ?
            """, (achievement.xp_reward, skill_id))
        
        self.db_connection.commit()

    def _map_achievement_to_skills(self, achievement) -> List[str]:
        """Map achievement to relevant skills."""
        # This is a simplified mapping - in a real system, this would be more sophisticated
        achievement_text = f"{achievement.name} {achievement.description}".lower()
        
        skill_mapping = {
            "debugging": ["debug", "error", "bug", "fix"],
            "error_handling": ["error", "exception", "handle"],
            "security": ["security", "vulnerability", "protect"],
            "coding": ["code", "program", "develop"],
            "refactoring": ["refactor", "improve", "clean"],
            "optimization": ["optimize", "performance", "efficiency"],
            "research": ["research", "investigate", "study"],
            "analysis": ["analyze", "understand", "examine"],
            "documentation": ["document", "write", "explain"],
            "architecture": ["architecture", "design", "structure"],
            "design_patterns": ["pattern", "design", "solution"],
            "testing": ["test", "verify", "validate"]
        }
        
        relevant_skills = []
        for skill_id, keywords in skill_mapping.items():
            if any(keyword in achievement_text for keyword in keywords):
                relevant_skills.append(skill_id)
        
        return relevant_skills

    def get_skills(self) -> List[Dict[str, Any]]:
        """Get all skills from the database."""
        cursor = self.db_connection.cursor()
        cursor.execute("""
            SELECT name, category, current_level, current_xp, description
            FROM skills
            ORDER BY category, name
        """)
        
        skills = []
        for row in cursor.fetchall():
            skills.append({
                'skill_id': row[0],  # Use name as skill_id since it's the primary key
                'name': row[0],
                'category': row[1],
                'current_level': row[2],
                'experience_points': row[3],
                'description': row[4]
            })
        
        return skills

    def get_skill_stats(self) -> Dict[str, Any]:
        """Get skill statistics."""
        cursor = self.db_connection.cursor()
        
        # Get total skills
        cursor.execute("SELECT COUNT(*) FROM skills")
        total_skills = cursor.fetchone()[0]
        
        # Get skills by category
        cursor.execute("""
            SELECT category, COUNT(*) as count, AVG(current_level) as avg_level
            FROM skills
            GROUP BY category
        """)
        
        category_stats = {}
        for row in cursor.fetchall():
            category_stats[row[0]] = {
                'count': row[1],
                'avg_level': row[2]
            }
        
        # Get highest level skills
        cursor.execute("""
            SELECT name, current_level
            FROM skills
            ORDER BY current_level DESC
            LIMIT 5
        """)
        
        top_skills = []
        for row in cursor.fetchall():
            top_skills.append({
                'skill_id': row[0],  # Use name as skill_id since it's the primary key
                'name': row[0],
                'level': row[1]
            })
        
        return {
            'total_skills': total_skills,
            'category_stats': category_stats,
            'top_skills': top_skills
        } 