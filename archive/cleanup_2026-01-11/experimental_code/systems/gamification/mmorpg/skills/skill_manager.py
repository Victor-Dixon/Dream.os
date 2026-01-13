"""
Skill Manager - MMORPG Skill Progression
=======================================

This module handles skill progression, XP calculations, and
skill management for the MMORPG system.
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from dataclasses import dataclass
from enum import Enum

from ..core.base_system import MMORPGComponent, ValidationError

logger = logging.getLogger(__name__)


class SkillType(Enum):
    """Core skills in the Dreamscape MMORPG."""
    SYSTEM_CONVERGENCE = "system_convergence"
    EXECUTION_VELOCITY = "execution_velocity"
    STRATEGIC_INTELLIGENCE = "strategic_intelligence"
    AI_SELF_ORGANIZATION = "ai_self_organization"
    DOMAIN_STABILIZATION = "domain_stabilization"
    PROGRAMMING = "programming"
    DEBUGGING = "debugging"
    ARCHITECTURE = "architecture"
    TESTING = "testing"
    ANALYTICS = "analytics"


@dataclass
class Skill:
    """Represents a player skill."""
    name: str
    skill_type: SkillType
    current_level: int = 0
    experience_points: int = 0
    max_level: int = 100
    last_updated: datetime = None
    bonus_multiplier: float = 1.0
    
    def __post_init__(self):
        if self.last_updated is None:
            self.last_updated = datetime.now()


@dataclass
class SkillProgress:
    """Represents skill progression data."""
    skill_name: str
    xp_gained: int
    levels_gained: int
    source: str
    timestamp: datetime
    details: Dict[str, Any] = None


class SkillManager(MMORPGComponent):
    """Manages skill progression and XP calculations."""
    
    def __init__(self, db_path: str = "dreamos_resume.db"):
        """Initialize the skill manager."""
        super().__init__(db_path, "SkillManager")
        self.skills = {}
        self.skill_progress_history = []
        
        # Load existing skills
        self._load_skills()
    
    def _create_schema(self):
        """Create skills database schema."""
        try:
            # Skills table
            skills_schema = """
                CREATE TABLE IF NOT EXISTS skills (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    skill_type TEXT NOT NULL,
                    current_level INTEGER DEFAULT 0,
                    experience_points INTEGER DEFAULT 0,
                    max_level INTEGER DEFAULT 100,
                    bonus_multiplier REAL DEFAULT 1.0,
                    last_updated TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """
            
            # Skill progress history table
            progress_schema = """
                CREATE TABLE IF NOT EXISTS skill_progress (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    skill_name TEXT NOT NULL,
                    xp_gained INTEGER NOT NULL,
                    levels_gained INTEGER DEFAULT 0,
                    source TEXT,
                    details TEXT,
                    timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (skill_name) REFERENCES skills (name)
                )
            """
            
            self.execute_update(skills_schema)
            self.execute_update(progress_schema)
            
            logger.info("Skills database schema created successfully")
            
        except Exception as e:
            logger.error(f"Failed to create skills schema: {e}")
            raise
    
    def _load_skills(self):
        """Load skills from database."""
        try:
            if not self.table_exists("skills"):
                self._create_schema()
                self._create_default_skills()
                return
            
            # Load skills from database
            skills_data = self.execute_query("SELECT * FROM skills")
            
            for skill_data in skills_data:
                skill = Skill(
                    name=skill_data["name"],
                    skill_type=SkillType(skill_data["skill_type"]),
                    current_level=skill_data["current_level"],
                    experience_points=skill_data["experience_points"],
                    max_level=skill_data["max_level"],
                    bonus_multiplier=skill_data["bonus_multiplier"],
                    last_updated=datetime.fromisoformat(skill_data["last_updated"]) if skill_data["last_updated"] else datetime.now()
                )
                self.skills[skill.name] = skill
            
            logger.info(f"Loaded {len(self.skills)} skills from database")
            
        except Exception as e:
            logger.error(f"Failed to load skills: {e}")
            self._create_default_skills()
    
    def _create_default_skills(self):
        """Create default skills for new players."""
        default_skills = [
            ("System Convergence", SkillType.SYSTEM_CONVERGENCE),
            ("Execution Velocity", SkillType.EXECUTION_VELOCITY),
            ("Strategic Intelligence", SkillType.STRATEGIC_INTELLIGENCE),
            ("AI Self-Organization", SkillType.AI_SELF_ORGANIZATION),
            ("Domain Stabilization", SkillType.DOMAIN_STABILIZATION),
            ("Programming", SkillType.PROGRAMMING),
            ("Debugging", SkillType.DEBUGGING),
            ("Architecture", SkillType.ARCHITECTURE),
            ("Testing", SkillType.TESTING),
            ("Analytics", SkillType.ANALYTICS)
        ]
        
        for skill_name, skill_type in default_skills:
            self.create_skill(skill_name, skill_type)
        
        logger.info(f"Created {len(default_skills)} default skills")
    
    def create_skill(self, name: str, skill_type: SkillType, max_level: int = 100) -> bool:
        """Create a new skill."""
        try:
            if name in self.skills:
                logger.warning(f"Skill already exists: {name}")
                return False
            
            # Create skill object
            skill = Skill(
                name=name,
                skill_type=skill_type,
                max_level=max_level,
                last_updated=datetime.now()
            )
            
            # Save to database
            query = """
                INSERT INTO skills (name, skill_type, current_level, experience_points, max_level, bonus_multiplier, last_updated)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            
            success = self.execute_update(query, (
                skill.name,
                skill.skill_type.value,
                skill.current_level,
                skill.experience_points,
                skill.max_level,
                skill.bonus_multiplier,
                skill.last_updated.isoformat()
            ))
            
            if success:
                self.skills[name] = skill
                self.log_activity(f"Created skill: {name}")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Failed to create skill {name}: {e}")
            return False
    
    def add_experience(self, skill_name: str, xp_amount: int, source: str = "manual") -> Dict[str, Any]:
        """Add experience to a skill."""
        try:
            if skill_name not in self.skills:
                logger.warning(f"Skill not found: {skill_name}")
                return {"success": False, "error": "Skill not found"}
            
            skill = self.skills[skill_name]
            old_level = skill.current_level
            
            # Calculate effective XP with bonuses
            effective_xp = int(xp_amount * skill.bonus_multiplier)
            
            # Add XP
            skill.experience_points += effective_xp
            
            # Calculate new level
            new_level = self._calculate_level(skill.experience_points)
            levels_gained = new_level - old_level
            
            # Update skill level
            if new_level != old_level:
                skill.current_level = min(new_level, skill.max_level)
            
            skill.last_updated = datetime.now()
            
            # Save to database
            self._save_skill(skill)
            
            # Record progress
            progress = SkillProgress(
                skill_name=skill_name,
                xp_gained=effective_xp,
                levels_gained=levels_gained,
                source=source,
                timestamp=datetime.now(),
                details={"original_xp": xp_amount, "bonus_multiplier": skill.bonus_multiplier}
            )
            
            self._record_progress(progress)
            
            result = {
                "success": True,
                "skill_name": skill_name,
                "xp_gained": effective_xp,
                "levels_gained": levels_gained,
                "new_level": skill.current_level,
                "total_xp": skill.experience_points
            }
            
            if levels_gained > 0:
                self.log_activity(f"Level up! {skill_name} reached level {skill.current_level}")
            else:
                self.log_activity(f"Gained {effective_xp} XP in {skill_name}")
            
            return result
            
        except Exception as e:
            logger.error(f"Failed to add experience to {skill_name}: {e}")
            return {"success": False, "error": str(e)}
    
    def _calculate_level(self, experience_points: int) -> int:
        """Calculate level based on experience points."""
        # Use a square root progression: level = sqrt(xp / 100)
        import math
        if experience_points <= 0:
            return 0
        
        level = int(math.sqrt(experience_points / 100))
        return level
    
    def _xp_for_level(self, level: int) -> int:
        """Calculate XP required for a specific level."""
        if level <= 0:
            return 0
        return level * level * 100
    
    def _save_skill(self, skill: Skill) -> bool:
        """Save skill to database."""
        try:
            query = """
                UPDATE skills 
                SET current_level = ?, experience_points = ?, bonus_multiplier = ?, last_updated = ?
                WHERE name = ?
            """
            
            return self.execute_update(query, (
                skill.current_level,
                skill.experience_points,
                skill.bonus_multiplier,
                skill.last_updated.isoformat(),
                skill.name
            ))
            
        except Exception as e:
            logger.error(f"Failed to save skill {skill.name}: {e}")
            return False
    
    def _record_progress(self, progress: SkillProgress):
        """Record skill progress in history."""
        try:
            # Add to memory
            self.skill_progress_history.append(progress)
            
            # Keep only last 1000 entries in memory
            if len(self.skill_progress_history) > 1000:
                self.skill_progress_history.pop(0)
            
            # Save to database
            query = """
                INSERT INTO skill_progress (skill_name, xp_gained, levels_gained, source, details, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            """
            
            import json
            self.execute_update(query, (
                progress.skill_name,
                progress.xp_gained,
                progress.levels_gained,
                progress.source,
                json.dumps(progress.details or {}),
                progress.timestamp.isoformat()
            ))
            
        except Exception as e:
            logger.error(f"Failed to record progress: {e}")
    
    def get_skill(self, skill_name: str) -> Optional[Skill]:
        """Get a skill by name."""
        return self.skills.get(skill_name)
    
    def get_all_skills(self) -> Dict[str, Skill]:
        """Get all skills."""
        return self.skills.copy()
    
    def get_skills_by_type(self, skill_type: SkillType) -> List[Skill]:
        """Get skills of a specific type."""
        return [skill for skill in self.skills.values() if skill.skill_type == skill_type]
    
    def get_top_skills(self, limit: int = 5) -> List[Skill]:
        """Get top skills by level."""
        sorted_skills = sorted(
            self.skills.values(),
            key=lambda s: (s.current_level, s.experience_points),
            reverse=True
        )
        return sorted_skills[:limit]
    
    def get_recent_progress(self, limit: int = 10) -> List[SkillProgress]:
        """Get recent skill progress."""
        return self.skill_progress_history[-limit:] if self.skill_progress_history else []
    
    def set_skill_bonus(self, skill_name: str, bonus_multiplier: float) -> bool:
        """Set skill bonus multiplier."""
        try:
            if skill_name not in self.skills:
                return False
            
            skill = self.skills[skill_name]
            skill.bonus_multiplier = bonus_multiplier
            skill.last_updated = datetime.now()
            
            return self._save_skill(skill)
            
        except Exception as e:
            logger.error(f"Failed to set skill bonus for {skill_name}: {e}")
            return False
    
    def validate_data(self, data: Dict[str, Any]) -> bool:
        """Validate skill data."""
        required_fields = ["name", "skill_type"]
        for field in required_fields:
            if field not in data:
                return False
        
        # Validate skill type
        try:
            SkillType(data["skill_type"])
        except ValueError:
            return False
        
        return True
    
    def get_stats(self) -> Dict[str, Any]:
        """Get skill system statistics."""
        if not self.skills:
            return {"total_skills": 0}
        
        total_level = sum(skill.current_level for skill in self.skills.values())
        total_xp = sum(skill.experience_points for skill in self.skills.values())
        max_level_skill = max(self.skills.values(), key=lambda s: s.current_level)
        
        return {
            "total_skills": len(self.skills),
            "total_level": total_level,
            "total_xp": total_xp,
            "average_level": total_level / len(self.skills) if self.skills else 0,
            "highest_skill": {
                "name": max_level_skill.name,
                "level": max_level_skill.current_level,
                "xp": max_level_skill.experience_points
            },
            "recent_progress_count": len(self.skill_progress_history)
        } 