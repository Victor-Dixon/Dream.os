"""
MMORPG Player Models
Contains player-related data models for the Dreamscape MMORPG system.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List
from .enums import TIER_DEFINITIONS


@dataclass
class Player:
    """Represents a player in the Dreamscape MMORPG."""
    name: str
    architect_tier: str = "Tier 1 - Novice"
    xp: int = 0
    total_conversations: int = 0
    total_messages: int = 0
    total_words: int = 0
    created_at: datetime = None
    last_active: datetime = None

    def __post_init__(self):
        """Initialize default values after object creation."""
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.last_active is None:
            self.last_active = datetime.now()

    def get_next_level_xp(self) -> int:
        """Get XP required for next architect tier."""
        try:
            tier_parts = self.architect_tier.split()
            if len(tier_parts) >= 2:
                current_tier = int(tier_parts[1])
            else:
                current_tier = 1
            
            for tier_level, tier_name, xp_required in TIER_DEFINITIONS:
                if tier_level > current_tier:
                    return xp_required
            return self.xp
        except (ValueError, IndexError):
            return 100

    def add_xp(self, xp_amount: int) -> bool:
        """Add experience points to the player."""
        if xp_amount > 0:
            self.xp += xp_amount
            self.last_active = datetime.now()
            return True
        return False

    def get_current_tier_level(self) -> int:
        """Get the current tier level as an integer."""
        try:
            tier_parts = self.architect_tier.split()
            if len(tier_parts) >= 2:
                return int(tier_parts[1])
            return 1
        except (ValueError, IndexError):
            return 1

    def can_advance_tier(self) -> bool:
        """Check if the player can advance to the next tier."""
        next_tier_xp = self.get_next_level_xp()
        return self.xp >= next_tier_xp

    def advance_tier(self) -> bool:
        """Advance to the next architect tier if possible."""
        if self.can_advance_tier():
            current_tier = self.get_current_tier_level()
            for tier_level, tier_name, xp_required in TIER_DEFINITIONS:
                if tier_level == current_tier + 1:
                    self.architect_tier = f"Tier {tier_level} - {tier_name}"
                    return True
        return False

    def update_stats(self, conversations: int = 0, messages: int = 0, words: int = 0) -> None:
        """Update player statistics."""
        self.total_conversations += conversations
        self.total_messages += messages
        self.total_words += words
        self.last_active = datetime.now()

    def get_stats_summary(self) -> Dict:
        """Get a summary of player statistics."""
        return {
            'name': self.name,
            'architect_tier': self.architect_tier,
            'xp': self.xp,
            'next_level_xp': self.get_next_level_xp(),
            'total_conversations': self.total_conversations,
            'total_messages': self.total_messages,
            'total_words': self.total_words,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_active': self.last_active.isoformat() if self.last_active else None
        }

    def to_dict(self) -> Dict:
        """Convert player to dictionary representation."""
        return {
            'name': self.name,
            'architect_tier': self.architect_tier,
            'xp': self.xp,
            'total_conversations': self.total_conversations,
            'total_messages': self.total_messages,
            'total_words': self.total_words,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_active': self.last_active.isoformat() if self.last_active else None
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Player':
        """Create player from dictionary representation."""
        return cls(
            name=data['name'],
            architect_tier=data['architect_tier'],
            xp=data['xp'],
            total_conversations=data['total_conversations'],
            total_messages=data['total_messages'],
            total_words=data['total_words'],
            created_at=datetime.fromisoformat(data['created_at']) if data.get('created_at') else None,
            last_active=datetime.fromisoformat(data['last_active']) if data.get('last_active') else None
        )


@dataclass
class ArchitectTier:
    """Represents an architect tier with requirements and abilities."""
    tier_level: int
    tier_name: str
    experience_required: int
    abilities_unlocked: List[str]
    achieved_at: datetime = None

    def __post_init__(self):
        """Initialize default values after object creation."""
        if self.achieved_at is None:
            self.achieved_at = datetime.now()

    def to_dict(self) -> Dict:
        """Convert architect tier to dictionary representation."""
        return {
            'tier_level': self.tier_level,
            'tier_name': self.tier_name,
            'experience_required': self.experience_required,
            'abilities_unlocked': self.abilities_unlocked,
            'achieved_at': self.achieved_at.isoformat() if self.achieved_at else None
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'ArchitectTier':
        """Create architect tier from dictionary representation."""
        return cls(
            tier_level=data['tier_level'],
            tier_name=data['tier_name'],
            experience_required=data['experience_required'],
            abilities_unlocked=data['abilities_unlocked'],
            achieved_at=datetime.fromisoformat(data['achieved_at']) if data.get('achieved_at') else None
        )


@dataclass
class Guild:
    """Represents a guild in the Dreamscape MMORPG."""
    id: str
    name: str
    description: str = ""
    leader_id: str = ""
    members: List[str] = None
    created_at: datetime = None

    def __post_init__(self):
        """Initialize default values after object creation."""
        if self.members is None:
            self.members = []
        if self.created_at is None:
            self.created_at = datetime.now()

    def add_member(self, member_id: str) -> bool:
        """Add a member to the guild."""
        if member_id not in self.members:
            self.members.append(member_id)
            return True
        return False

    def remove_member(self, member_id: str) -> bool:
        """Remove a member from the guild."""
        if member_id in self.members:
            self.members.remove(member_id)
            return True
        return False

    def is_member(self, member_id: str) -> bool:
        """Check if a player is a member of the guild."""
        return member_id in self.members

    def get_member_count(self) -> int:
        """Get the number of members in the guild."""
        return len(self.members)

    def to_dict(self) -> Dict:
        """Convert guild to dictionary representation."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'leader_id': self.leader_id,
            'members': self.members,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Guild':
        """Create guild from dictionary representation."""
        return cls(
            id=data['id'],
            name=data['name'],
            description=data['description'],
            leader_id=data['leader_id'],
            members=data['members'],
            created_at=datetime.fromisoformat(data['created_at']) if data.get('created_at') else None
        ) 