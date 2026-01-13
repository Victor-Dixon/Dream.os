"""Quest Models for Dynamic Quest System.
<!-- SSOT Domain: gaming -->

Data models and enums for the dynamic quest generation system.

Author: Agent-6 - Gaming & Entertainment Specialist
V2 Compliance: SOLID principles, type hints, comprehensive validation
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Protocol
from uuid import uuid4


class QuestType(Enum):
    """Types of quests available in the system."""

    COLLABORATION = "collaboration"
    PERFORMANCE = "performance"
    INNOVATION = "innovation"
    MAINTENANCE = "maintenance"
    COORDINATION = "coordination"
    DEVELOPMENT = "development"
    INTEGRATION = "integration"
    OPTIMIZATION = "optimization"


class QuestDifficulty(Enum):
    """Quest difficulty levels."""

    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    EPIC = "epic"
    LEGENDARY = "legendary"


class QuestStatus(Enum):
    """Quest status states."""

    AVAILABLE = "available"
    ACTIVE = "active"
    COMPLETED = "completed"
    FAILED = "failed"
    EXPIRED = "expired"


@dataclass
class QuestObjective:
    """Individual objective within a quest."""

    objective_id: str
    description: str
    target_value: int
    current_value: int = 0
    completed: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)

    def update_progress(self, increment: int = 1) -> bool:
        """Update objective progress. Returns True if completed."""
        self.current_value += increment
        if self.current_value >= self.target_value:
            self.completed = True
            return True
        return False

    def is_completed(self) -> bool:
        """Check if objective is completed."""
        return self.completed

    def get_progress_percentage(self) -> float:
        """Get completion percentage (0-100)."""
        if self.target_value == 0:
            return 100.0
        return min(100.0, (self.current_value / self.target_value) * 100.0)


@dataclass
class QuestReward:
    """Reward structure for quest completion."""

    xp_reward: int
    bonus_points: int = 0
    achievements: List[str] = field(default_factory=list)
    special_unlocks: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Quest:
    """Main quest data structure."""

    quest_id: str
    title: str
    description: str
    quest_type: QuestType
    difficulty: QuestDifficulty
    objectives: List[QuestObjective]
    rewards: QuestReward
    assigned_agent: str
    created_at: datetime
    expires_at: Optional[datetime] = None
    status: QuestStatus = QuestStatus.AVAILABLE
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    progress_percentage: float = 0.0
    tags: List[str] = field(default_factory=list)
    prerequisites: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Generate quest ID if not provided."""
        if not self.quest_id:
            self.quest_id = f"quest_{uuid4().hex[:8]}"
        self.update_progress()

    def start_quest(self) -> bool:
        """Start the quest. Returns True if successful."""
        if self.status != QuestStatus.AVAILABLE:
            return False

        self.status = QuestStatus.ACTIVE
        self.started_at = datetime.now()
        return True

    def update_progress(self) -> float:
        """Update overall quest progress. Returns completion percentage."""
        if not self.objectives:
            self.progress_percentage = 100.0
            return 100.0

        completed_objectives = sum(1 for obj in self.objectives if obj.is_completed())
        self.progress_percentage = (completed_objectives / len(self.objectives)) * 100.0

        # Check if quest is completed
        if self.progress_percentage >= 100.0 and self.status == QuestStatus.ACTIVE:
            self.complete_quest()

        return self.progress_percentage

    def complete_quest(self) -> bool:
        """Mark quest as completed. Returns True if successful."""
        if self.status != QuestStatus.ACTIVE:
            return False

        self.status = QuestStatus.COMPLETED
        self.completed_at = datetime.now()
        self.progress_percentage = 100.0
        return True

    def fail_quest(self) -> bool:
        """Mark quest as failed. Returns True if successful."""
        if self.status not in [QuestStatus.ACTIVE, QuestStatus.AVAILABLE]:
            return False

        self.status = QuestStatus.FAILED
        return True

    def is_expired(self) -> bool:
        """Check if quest has expired."""
        if not self.expires_at:
            return False
        return datetime.now() > self.expires_at

    def get_time_remaining(self) -> Optional[int]:
        """Get seconds remaining until expiration. None if no expiration."""
        if not self.expires_at:
            return None
        remaining = self.expires_at - datetime.now()
        return max(0, int(remaining.total_seconds()))

    def to_dict(self) -> Dict[str, Any]:
        """Convert quest to dictionary representation."""
        return {
            "quest_id": self.quest_id,
            "title": self.title,
            "description": self.description,
            "quest_type": self.quest_type.value,
            "difficulty": self.difficulty.value,
            "objectives": [
                {
                    "objective_id": obj.objective_id,
                    "description": obj.description,
                    "target_value": obj.target_value,
                    "current_value": obj.current_value,
                    "completed": obj.completed,
                    "progress_percentage": obj.get_progress_percentage(),
                    "metadata": obj.metadata
                }
                for obj in self.objectives
            ],
            "rewards": {
                "xp_reward": self.rewards.xp_reward,
                "bonus_points": self.rewards.bonus_points,
                "achievements": self.rewards.achievements,
                "special_unlocks": self.rewards.special_unlocks,
                "metadata": self.rewards.metadata
            },
            "assigned_agent": self.assigned_agent,
            "created_at": self.created_at.isoformat(),
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "status": self.status.value,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "progress_percentage": self.progress_percentage,
            "tags": self.tags,
            "prerequisites": self.prerequisites,
            "metadata": self.metadata
        }


class IQuestGenerator(Protocol):
    """Interface for quest generators."""

    def generate_quest(self, agent_id: str, agent_capabilities: List[str],
                      agent_status: Dict[str, Any]) -> Optional[Quest]: ...


class IQuestManager(Protocol):
    """Interface for quest management."""

    def create_quest(self, agent_id: str, quest_type: QuestType,
                    difficulty: QuestDifficulty) -> Optional[Quest]: ...

    def get_agent_quests(self, agent_id: str) -> List[Quest]: ...

    def update_quest_progress(self, quest_id: str, objective_id: str,
                            progress_increment: int) -> bool: ...

    def complete_quest(self, quest_id: str) -> bool: ...