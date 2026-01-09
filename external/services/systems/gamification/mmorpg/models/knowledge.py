"""Knowledge models for Dreamscape MMORPG."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List


@dataclass
class KnowledgeNode:
    """Represents a knowledge area with progression metadata."""

    topic: str
    category: str
    level: int = 0
    xp: int = 0
    dependencies: List[str] = field(default_factory=list)
    last_updated: datetime | None = None

    def __post_init__(self) -> None:
        if self.last_updated is None:
            self.last_updated = datetime.now()
