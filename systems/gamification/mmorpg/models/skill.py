"""
MMORPG Skill Models
Contains skill-related data models for the Dreamscape MMORPG system.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Optional


@dataclass
class Skill:
    """Represents a skill in the Dreamscape MMORPG."""
    name: str
    current_level: int = 0
    experience_points: int = 0
    max_level: int = 100
    last_updated: datetime = None

    def __post_init__(self):
        """Initialize default values after object creation."""
        if self.last_updated is None:
            self.last_updated = datetime.now()

    def add_experience(self, xp_amount: int) -> bool:
        """Add experience points to the skill."""
        if xp_amount > 0:
            self.experience_points += xp_amount
            self.last_updated = datetime.now()
            return True
        return False

    def get_level(self) -> int:
        """Calculate current level based on experience points."""
        if self.experience_points <= 0:
            return 0
        
        # Simple level calculation: level = sqrt(xp / 100)
        import math
        level = int(math.sqrt(self.experience_points / 100))
        return min(level, self.max_level)

    def get_xp_for_next_level(self) -> int:
        """Calculate XP required for next level."""
        current_level = self.get_level()
        if current_level >= self.max_level:
            return 0
        
        next_level = current_level + 1
        required_xp = (next_level ** 2) * 100
        return required_xp - self.experience_points

    def get_progress_to_next_level(self) -> float:
        """Get progress percentage to next level."""
        current_level = self.get_level()
        if current_level >= self.max_level:
            return 1.0
        
        current_level_xp = (current_level ** 2) * 100
        next_level_xp = ((current_level + 1) ** 2) * 100
        level_xp_range = next_level_xp - current_level_xp
        current_level_progress = self.experience_points - current_level_xp
        
        return min(current_level_progress / level_xp_range, 1.0)

    def can_level_up(self) -> bool:
        """Check if the skill can level up."""
        return self.get_level() < self.max_level and self.get_xp_for_next_level() <= 0

    def level_up(self) -> bool:
        """Level up the skill if possible."""
        if self.can_level_up():
            self.current_level = self.get_level()
            return True
        return False

    def to_dict(self) -> Dict:
        """Convert skill to dictionary representation."""
        return {
            'name': self.name,
            'current_level': self.current_level,
            'experience_points': self.experience_points,
            'max_level': self.max_level,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Skill':
        """Create skill from dictionary representation."""
        return cls(
            name=data['name'],
            current_level=data['current_level'],
            experience_points=data['experience_points'],
            max_level=data['max_level'],
            last_updated=datetime.fromisoformat(data['last_updated']) if data.get('last_updated') else None
        )


@dataclass
class SkillLevel:
    """Represents a skill level with unlock information."""
    level: int
    current_xp: int
    xp_to_next: int
    unlocks: List[str]


@dataclass
class SkillDefinition:
    """Represents a skill definition with metadata."""
    name: str
    description: str
    category: str
    related_skills: List[str]
    max_level: int = 99


@dataclass
class SkillTreeNode:
    """Represents a node in the skill tree."""
    skill_name: str
    level: int
    xp: int
    category: str
    dependencies: List[str]
    unlocks: List[str]
    ai_confidence: float
    last_updated: datetime
    metadata: Dict = None

    def __post_init__(self):
        """Initialize default values after object creation."""
        if self.metadata is None:
            self.metadata = {} 