"""
MMORPG Achievement Models
Contains achievement-related data models for the Dreamscape MMORPG system.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Optional


@dataclass
class Achievement:
    """Represents an achievement in the Dreamscape MMORPG."""
    id: str
    name: str
    description: str
    category: str  # 'quest', 'skill', 'project', 'milestone', 'special'
    difficulty: int  # 1-10 scale
    xp_reward: int
    completed_at: str
    evidence: str  # URL, file path, or description of proof
    tags: List[str]
    impact_score: int  # 1-10 scale for resume impact

    def __post_init__(self):
        """Initialize default values after object creation."""
        if self.tags is None:
            self.tags = []

    def is_quest_achievement(self) -> bool:
        """Check if this is a quest-related achievement."""
        return self.category == 'quest'

    def is_skill_achievement(self) -> bool:
        """Check if this is a skill-related achievement."""
        return self.category == 'skill'

    def is_project_achievement(self) -> bool:
        """Check if this is a project-related achievement."""
        return self.category == 'project'

    def is_milestone_achievement(self) -> bool:
        """Check if this is a milestone achievement."""
        return self.category == 'milestone'

    def is_special_achievement(self) -> bool:
        """Check if this is a special achievement."""
        return self.category == 'special'

    def get_difficulty_label(self) -> str:
        """Get a human-readable difficulty label."""
        if self.difficulty <= 2:
            return "Easy"
        elif self.difficulty <= 4:
            return "Normal"
        elif self.difficulty <= 6:
            return "Hard"
        elif self.difficulty <= 8:
            return "Expert"
        else:
            return "Legendary"

    def get_impact_label(self) -> str:
        """Get a human-readable impact label."""
        if self.impact_score <= 2:
            return "Low"
        elif self.impact_score <= 4:
            return "Moderate"
        elif self.impact_score <= 6:
            return "High"
        elif self.impact_score <= 8:
            return "Very High"
        else:
            return "Critical"

    def has_tag(self, tag: str) -> bool:
        """Check if the achievement has a specific tag."""
        return tag.lower() in [t.lower() for t in self.tags]

    def add_tag(self, tag: str) -> bool:
        """Add a tag to the achievement."""
        if not self.has_tag(tag):
            self.tags.append(tag)
            return True
        return False

    def remove_tag(self, tag: str) -> bool:
        """Remove a tag from the achievement."""
        for i, existing_tag in enumerate(self.tags):
            if existing_tag.lower() == tag.lower():
                self.tags.pop(i)
                return True
        return False

    def to_dict(self) -> Dict:
        """Convert achievement to dictionary representation."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'difficulty': self.difficulty,
            'xp_reward': self.xp_reward,
            'completed_at': self.completed_at,
            'evidence': self.evidence,
            'tags': self.tags,
            'impact_score': self.impact_score
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Achievement':
        """Create achievement from dictionary representation."""
        return cls(
            id=data['id'],
            name=data['name'],
            description=data['description'],
            category=data['category'],
            difficulty=data['difficulty'],
            xp_reward=data['xp_reward'],
            completed_at=data['completed_at'],
            evidence=data['evidence'],
            tags=data['tags'],
            impact_score=data['impact_score']
        )


@dataclass
class ResumeSkill:
    """Represents a skill for resume generation."""
    name: str
    category: str  # 'technical', 'soft', 'domain', 'ai'
    current_level: int
    max_level: int
    current_xp: int
    next_level_xp: int
    description: str
    last_updated: str
    achievements: List[str]  # Achievement IDs that contributed

    def __post_init__(self):
        """Initialize default values after object creation."""
        if self.achievements is None:
            self.achievements = []

    def is_technical_skill(self) -> bool:
        """Check if this is a technical skill."""
        return self.category == 'technical'

    def is_soft_skill(self) -> bool:
        """Check if this is a soft skill."""
        return self.category == 'soft'

    def is_domain_skill(self) -> bool:
        """Check if this is a domain skill."""
        return self.category == 'domain'

    def is_ai_skill(self) -> bool:
        """Check if this is an AI-related skill."""
        return self.category == 'ai'

    def get_progress_percentage(self) -> float:
        """Get the progress percentage to next level."""
        if self.next_level_xp <= 0:
            return 1.0
        return min(self.current_xp / self.next_level_xp, 1.0)

    def add_achievement(self, achievement_id: str) -> bool:
        """Add an achievement that contributed to this skill."""
        if achievement_id not in self.achievements:
            self.achievements.append(achievement_id)
            return True
        return False

    def remove_achievement(self, achievement_id: str) -> bool:
        """Remove an achievement from this skill."""
        if achievement_id in self.achievements:
            self.achievements.remove(achievement_id)
            return True
        return False

    def to_dict(self) -> Dict:
        """Convert resume skill to dictionary representation."""
        return {
            'name': self.name,
            'category': self.category,
            'current_level': self.current_level,
            'max_level': self.max_level,
            'current_xp': self.current_xp,
            'next_level_xp': self.next_level_xp,
            'description': self.description,
            'last_updated': self.last_updated,
            'achievements': self.achievements
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'ResumeSkill':
        """Create resume skill from dictionary representation."""
        return cls(
            name=data['name'],
            category=data['category'],
            current_level=data['current_level'],
            max_level=data['max_level'],
            current_xp=data['current_xp'],
            next_level_xp=data['next_level_xp'],
            description=data['description'],
            last_updated=data['last_updated'],
            achievements=data['achievements']
        )


@dataclass
class Project:
    """Represents a project for resume generation."""
    id: str
    name: str
    description: str
    start_date: str
    end_date: Optional[str]
    status: str  # 'active', 'completed', 'paused', 'cancelled'
    technologies: List[str]
    achievements: List[str]
    impact_description: str
    team_size: int
    role: str

    def __post_init__(self):
        """Initialize default values after object creation."""
        if self.technologies is None:
            self.technologies = []
        if self.achievements is None:
            self.achievements = []

    def is_active(self) -> bool:
        """Check if the project is currently active."""
        return self.status == 'active'

    def is_completed(self) -> bool:
        """Check if the project is completed."""
        return self.status == 'completed'

    def is_paused(self) -> bool:
        """Check if the project is paused."""
        return self.status == 'paused'

    def is_cancelled(self) -> bool:
        """Check if the project is cancelled."""
        return self.status == 'cancelled'

    def add_technology(self, technology: str) -> bool:
        """Add a technology to the project."""
        if technology not in self.technologies:
            self.technologies.append(technology)
            return True
        return False

    def remove_technology(self, technology: str) -> bool:
        """Remove a technology from the project."""
        if technology in self.technologies:
            self.technologies.remove(technology)
            return True
        return False

    def add_achievement(self, achievement_id: str) -> bool:
        """Add an achievement related to this project."""
        if achievement_id not in self.achievements:
            self.achievements.append(achievement_id)
            return True
        return False

    def remove_achievement(self, achievement_id: str) -> bool:
        """Remove an achievement from this project."""
        if achievement_id in self.achievements:
            self.achievements.remove(achievement_id)
            return True
        return False

    def to_dict(self) -> Dict:
        """Convert project to dictionary representation."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'status': self.status,
            'technologies': self.technologies,
            'achievements': self.achievements,
            'impact_description': self.impact_description,
            'team_size': self.team_size,
            'role': self.role
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Project':
        """Create project from dictionary representation."""
        return cls(
            id=data['id'],
            name=data['name'],
            description=data['description'],
            start_date=data['start_date'],
            end_date=data.get('end_date'),
            status=data['status'],
            technologies=data['technologies'],
            achievements=data['achievements'],
            impact_description=data['impact_description'],
            team_size=data['team_size'],
            role=data['role']
        ) 