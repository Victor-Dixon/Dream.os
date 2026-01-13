"""Social Models for Agent Interaction and Collaboration Tracking.
<!-- SSOT Domain: gaming -->

Data models for social features, agent relationships, and collaboration tracking.

Author: Agent-6 - Gaming & Entertainment Specialist
V2 Compliance: SOLID principles, type hints, comprehensive social metrics
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import uuid4


class RelationshipType(Enum):
    """Types of relationships between agents."""

    COLLABORATOR = "collaborator"
    COMPETITOR = "competitor"
    MENTOR = "mentor"
    MENTEE = "mentee"
    FRIEND = "friend"
    RIVAL = "rival"


class InteractionType(Enum):
    """Types of social interactions."""

    MESSAGE = "message"
    COORDINATION = "coordination"
    COLLABORATION = "collaboration"
    COMPETITION = "competition"
    HELP_REQUEST = "help_request"
    HELP_PROVIDED = "help_provided"
    QUEST_SHARED = "quest_shared"
    ACHIEVEMENT_SHARED = "achievement_shared"


class SocialAchievement(Enum):
    """Social achievements for agent interactions."""

    TEAM_PLAYER = "team_player"
    HELPFUL_AGENT = "helpful_agent"
    SOCIAL_BUTTERFLY = "social_butterfly"
    COORDINATION_MASTER = "coordination_master"
    MENTOR = "mentor"
    COLLABORATION_CHAMPION = "collaboration_champion"
    COMMUNITY_BUILDER = "community_builder"


@dataclass
class AgentRelationship:
    """Represents a relationship between two agents."""

    relationship_id: str
    agent_a: str
    agent_b: str
    relationship_type: RelationshipType
    strength: float  # 0.0 to 1.0
    trust_level: float  # 0.0 to 1.0
    created_at: datetime
    last_interaction: datetime
    interaction_count: int = 0
    shared_quests: int = 0
    collaborations_completed: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Generate relationship ID if not provided."""
        if not self.relationship_id:
            # Create consistent ID regardless of agent order
            agents = sorted([self.agent_a, self.agent_b])
            self.relationship_id = f"rel_{agents[0]}_{agents[1]}"

    def update_interaction(self, interaction_type: InteractionType):
        """Update relationship based on interaction."""
        self.last_interaction = datetime.now()
        self.interaction_count += 1

        # Adjust strength and trust based on interaction type
        if interaction_type in [InteractionType.COLLABORATION, InteractionType.HELP_PROVIDED]:
            self.strength = min(1.0, self.strength + 0.1)
            self.trust_level = min(1.0, self.trust_level + 0.05)
        elif interaction_type == InteractionType.QUEST_SHARED:
            self.strength = min(1.0, self.strength + 0.05)
        elif interaction_type == InteractionType.COMPETITION:
            # Healthy competition can strengthen relationships
            self.strength = min(1.0, self.strength + 0.02)

    def get_relationship_score(self) -> float:
        """Calculate overall relationship score."""
        return (self.strength * 0.6) + (self.trust_level * 0.4)

    def is_active(self) -> bool:
        """Check if relationship is still active."""
        days_since_last_interaction = (datetime.now() - self.last_interaction).days
        return days_since_last_interaction <= 30  # Consider inactive after 30 days

    def to_dict(self) -> Dict[str, Any]:
        """Convert relationship to dictionary."""
        return {
            "relationship_id": self.relationship_id,
            "agent_a": self.agent_a,
            "agent_b": self.agent_b,
            "relationship_type": self.relationship_type.value,
            "strength": self.strength,
            "trust_level": self.trust_level,
            "created_at": self.created_at.isoformat(),
            "last_interaction": self.last_interaction.isoformat(),
            "interaction_count": self.interaction_count,
            "shared_quests": self.shared_quests,
            "collaborations_completed": self.collaborations_completed,
            "relationship_score": self.get_relationship_score(),
            "is_active": self.is_active(),
            "metadata": self.metadata
        }


@dataclass
class SocialInteraction:
    """Represents a social interaction between agents."""

    interaction_id: str
    from_agent: str
    to_agent: str
    interaction_type: InteractionType
    timestamp: datetime
    context: str  # Brief description of the interaction
    impact_score: float  # -1.0 to 1.0 (negative to positive impact)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Generate interaction ID if not provided."""
        if not self.interaction_id:
            self.interaction_id = f"int_{uuid4().hex[:8]}"

    def to_dict(self) -> Dict[str, Any]:
        """Convert interaction to dictionary."""
        return {
            "interaction_id": self.interaction_id,
            "from_agent": self.from_agent,
            "to_agent": self.to_agent,
            "interaction_type": self.interaction_type.value,
            "timestamp": self.timestamp.isoformat(),
            "context": self.context,
            "impact_score": self.impact_score,
            "metadata": self.metadata
        }


@dataclass
class AgentSocialProfile:
    """Social profile for an agent."""

    agent_id: str
    reputation_score: float = 0.0
    social_achievements: List[SocialAchievement] = field(default_factory=list)
    relationships: List[AgentRelationship] = field(default_factory=list)
    interaction_history: List[SocialInteraction] = field(default_factory=list)
    collaboration_count: int = 0
    help_provided_count: int = 0
    help_received_count: int = 0
    quests_shared: int = 0
    last_social_activity: Optional[datetime] = None
    social_stats: Dict[str, Any] = field(default_factory=dict)

    def add_relationship(self, relationship: AgentRelationship):
        """Add or update a relationship."""
        # Remove existing relationship if it exists
        self.relationships = [r for r in self.relationships
                            if r.relationship_id != relationship.relationship_id]
        self.relationships.append(relationship)

    def add_interaction(self, interaction: SocialInteraction):
        """Add an interaction to history."""
        self.interaction_history.append(interaction)
        self.last_social_activity = interaction.timestamp

        # Update stats based on interaction
        if interaction.interaction_type == InteractionType.COLLABORATION:
            self.collaboration_count += 1
        elif interaction.interaction_type == InteractionType.HELP_PROVIDED:
            self.help_provided_count += 1
        elif interaction.interaction_type == InteractionType.HELP_REQUEST:
            self.help_received_count += 1
        elif interaction.interaction_type == InteractionType.QUEST_SHARED:
            self.quests_shared += 1

        # Update reputation based on positive interactions
        if interaction.impact_score > 0:
            self.reputation_score = min(100.0, self.reputation_score + interaction.impact_score)

    def get_active_relationships(self) -> List[AgentRelationship]:
        """Get currently active relationships."""
        return [r for r in self.relationships if r.is_active()]

    def get_relationship_with(self, other_agent: str) -> Optional[AgentRelationship]:
        """Get relationship with specific agent."""
        for rel in self.relationships:
            if rel.agent_a == other_agent or rel.agent_b == other_agent:
                return rel
        return None

    def get_social_score(self) -> float:
        """Calculate overall social score."""
        # Base score from reputation
        score = self.reputation_score

        # Bonus for relationships
        active_rels = len(self.get_active_relationships())
        score += active_rels * 5

        # Bonus for collaborations
        score += self.collaboration_count * 2

        # Bonus for helping others
        score += self.help_provided_count * 3

        # Bonus for social achievements
        score += len(self.social_achievements) * 10

        return min(100.0, score)

    def check_social_achievements(self):
        """Check and award social achievements."""
        new_achievements = []

        # Team Player: 5+ collaborations
        if self.collaboration_count >= 5 and SocialAchievement.TEAM_PLAYER not in self.social_achievements:
            self.social_achievements.append(SocialAchievement.TEAM_PLAYER)
            new_achievements.append(SocialAchievement.TEAM_PLAYER)

        # Helpful Agent: 10+ help interactions
        if self.help_provided_count >= 10 and SocialAchievement.HELPFUL_AGENT not in self.social_achievements:
            self.social_achievements.append(SocialAchievement.HELPFUL_AGENT)
            new_achievements.append(SocialAchievement.HELPFUL_AGENT)

        # Social Butterfly: 3+ active relationships
        if len(self.get_active_relationships()) >= 3 and SocialAchievement.SOCIAL_BUTTERFLY not in self.social_achievements:
            self.social_achievements.append(SocialAchievement.SOCIAL_BUTTERFLY)
            new_achievements.append(SocialAchievement.SOCIAL_BUTTERFLY)

        # Coordination Master: High reputation + many interactions
        if (self.reputation_score >= 50 and len(self.interaction_history) >= 20
            and SocialAchievement.COORDINATION_MASTER not in self.social_achievements):
            self.social_achievements.append(SocialAchievement.COORDINATION_MASTER)
            new_achievements.append(SocialAchievement.COORDINATION_MASTER)

        return new_achievements

    def to_dict(self) -> Dict[str, Any]:
        """Convert social profile to dictionary."""
        return {
            "agent_id": self.agent_id,
            "reputation_score": self.reputation_score,
            "social_achievements": [a.value for a in self.social_achievements],
            "relationships": [r.to_dict() for r in self.relationships],
            "interaction_history": [i.to_dict() for i in self.interaction_history[-20:]],  # Last 20 interactions
            "collaboration_count": self.collaboration_count,
            "help_provided_count": self.help_provided_count,
            "help_received_count": self.help_received_count,
            "quests_shared": self.quests_shared,
            "last_social_activity": self.last_social_activity.isoformat() if self.last_social_activity else None,
            "social_score": self.get_social_score(),
            "social_stats": self.social_stats
        }


# Interface definitions for dependency injection
class ISocialProfileManager:
    """Interface for social profile management."""

    def get_profile(self, agent_id: str) -> Optional[AgentSocialProfile]: ...

    def update_profile(self, profile: AgentSocialProfile) -> bool: ...

    def record_interaction(self, interaction: SocialInteraction) -> bool: ...

    def get_social_leaderboard(self, limit: int = 10) -> List[Dict[str, Any]]: ...


class ISocialRelationshipManager:
    """Interface for relationship management."""

    def create_relationship(self, agent_a: str, agent_b: str,
                          relationship_type: RelationshipType) -> Optional[AgentRelationship]: ...

    def update_relationship(self, relationship: AgentRelationship) -> bool: ...

    def get_relationships(self, agent_id: str) -> List[AgentRelationship]: ...