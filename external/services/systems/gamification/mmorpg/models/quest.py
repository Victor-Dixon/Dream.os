"""
MMORPG Quest Models
Contains quest-related data models for the Dreamscape MMORPG system.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Dict
from .enums import QuestType


@dataclass
class Quest:
    """Represents a quest in the Dreamscape MMORPG."""
    id: str
    title: str
    description: str
    quest_type: QuestType
    difficulty: int  # 1-10
    xp_reward: int
    skill_rewards: Dict[str, int]
    status: str = "available"  # available, active, completed, failed
    created_at: datetime = None
    completed_at: datetime = None
    conversation_id: str = None

    def __post_init__(self):
        """Initialize default values after object creation."""
        if self.created_at is None:
            self.created_at = datetime.now()

    def is_available(self) -> bool:
        """Check if the quest is available for taking."""
        return self.status == "available"

    def is_active(self) -> bool:
        """Check if the quest is currently active."""
        return self.status == "active"

    def is_completed(self) -> bool:
        """Check if the quest has been completed."""
        return self.status == "completed"

    def is_failed(self) -> bool:
        """Check if the quest has failed."""
        return self.status == "failed"

    def start_quest(self) -> bool:
        """Start the quest if it's available."""
        if self.is_available():
            self.status = "active"
            return True
        return False

    def complete_quest(self) -> bool:
        """Complete the quest if it's active."""
        if self.is_active():
            self.status = "completed"
            self.completed_at = datetime.now()
            return True
        return False

    def fail_quest(self) -> bool:
        """Fail the quest if it's active."""
        if self.is_active():
            self.status = "failed"
            return True
        return False

    def get_total_reward_xp(self) -> int:
        """Get the total XP reward including skill bonuses."""
        total_xp = self.xp_reward
        # Add bonus XP for skill rewards
        for skill_name, skill_xp in self.skill_rewards.items():
            total_xp += skill_xp
        return total_xp

    def to_dict(self) -> Dict:
        """Convert quest to dictionary representation."""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'quest_type': self.quest_type.value,
            'difficulty': self.difficulty,
            'xp_reward': self.xp_reward,
            'skill_rewards': self.skill_rewards,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'conversation_id': self.conversation_id
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Quest':
        """Create quest from dictionary representation."""
        return cls(
            id=data['id'],
            title=data['title'],
            description=data['description'],
            quest_type=QuestType(data['quest_type']),
            difficulty=data['difficulty'],
            xp_reward=data['xp_reward'],
            skill_rewards=data['skill_rewards'],
            status=data['status'],
            created_at=datetime.fromisoformat(data['created_at']) if data.get('created_at') else None,
            completed_at=datetime.fromisoformat(data['completed_at']) if data.get('completed_at') else None,
            conversation_id=data.get('conversation_id')
        ) 