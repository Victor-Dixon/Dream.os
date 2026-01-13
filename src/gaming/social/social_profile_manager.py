"""Social Profile Manager for Agent Social Features.
<!-- SSOT Domain: gaming -->

Manages agent social profiles, relationships, and interaction tracking.

Author: Agent-6 - Gaming & Entertainment Specialist
V2 Compliance: SOLID principles, comprehensive social analytics
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from ..models.social_models import (
    AgentSocialProfile,
    AgentRelationship,
    SocialInteraction,
    RelationshipType,
    InteractionType,
    SocialAchievement,
    ISocialProfileManager,
    ISocialRelationshipManager
)

logger = logging.getLogger(__name__)


class SocialProfileManager(ISocialProfileManager):
    """Manages social profiles for all agents."""

    def __init__(self, data_dir: Path = None):
        """Initialize social profile manager."""
        self.data_dir = data_dir or Path(__file__).parent.parent.parent / "data" / "social"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.profiles: Dict[str, AgentSocialProfile] = {}
        self._load_all_profiles()

    def _get_profile_path(self, agent_id: str) -> Path:
        """Get file path for agent's social profile."""
        return self.data_dir / f"{agent_id}_social_profile.json"

    def _load_all_profiles(self):
        """Load all existing social profiles."""
        if not self.data_dir.exists():
            return

        for profile_file in self.data_dir.glob("*_social_profile.json"):
            try:
                agent_id = profile_file.stem.replace("_social_profile", "")
                profile_data = json.loads(profile_file.read_text())

                # Reconstruct social profile from data
                profile = AgentSocialProfile(
                    agent_id=agent_id,
                    reputation_score=profile_data.get("reputation_score", 0.0),
                    social_achievements=[
                        SocialAchievement(a) for a in profile_data.get("social_achievements", [])
                    ],
                    collaboration_count=profile_data.get("collaboration_count", 0),
                    help_provided_count=profile_data.get("help_provided_count", 0),
                    help_received_count=profile_data.get("help_received_count", 0),
                    quests_shared=profile_data.get("quests_shared", 0),
                    social_stats=profile_data.get("social_stats", {})
                )

                # Load relationships
                for rel_data in profile_data.get("relationships", []):
                    relationship = AgentRelationship(
                        relationship_id=rel_data["relationship_id"],
                        agent_a=rel_data["agent_a"],
                        agent_b=rel_data["agent_b"],
                        relationship_type=RelationshipType(rel_data["relationship_type"]),
                        strength=rel_data["strength"],
                        trust_level=rel_data["trust_level"],
                        created_at=datetime.fromisoformat(rel_data["created_at"]),
                        last_interaction=datetime.fromisoformat(rel_data["last_interaction"]),
                        interaction_count=rel_data.get("interaction_count", 0),
                        shared_quests=rel_data.get("shared_quests", 0),
                        collaborations_completed=rel_data.get("collaborations_completed", 0),
                        metadata=rel_data.get("metadata", {})
                    )
                    profile.add_relationship(relationship)

                self.profiles[agent_id] = profile
                logger.debug(f"Loaded social profile for {agent_id}")

            except Exception as e:
                logger.error(f"Error loading social profile {profile_file}: {e}")

    def _save_profile(self, profile: AgentSocialProfile):
        """Save social profile to disk."""
        try:
            profile_path = self._get_profile_path(profile.agent_id)
            profile_data = profile.to_dict()
            profile_path.write_text(json.dumps(profile_data, indent=2, default=str))
        except Exception as e:
            logger.error(f"Error saving social profile for {profile.agent_id}: {e}")

    def get_profile(self, agent_id: str) -> Optional[AgentSocialProfile]:
        """Get social profile for an agent."""
        return self.profiles.get(agent_id)

    def get_or_create_profile(self, agent_id: str) -> AgentSocialProfile:
        """Get existing profile or create new one."""
        if agent_id not in self.profiles:
            self.profiles[agent_id] = AgentSocialProfile(agent_id=agent_id)
            self._save_profile(self.profiles[agent_id])
        return self.profiles[agent_id]

    def update_profile(self, profile: AgentSocialProfile) -> bool:
        """Update and save social profile."""
        try:
            self.profiles[profile.agent_id] = profile

            # Check for new social achievements
            new_achievements = profile.check_social_achievements()
            if new_achievements:
                logger.info(f"New social achievements for {profile.agent_id}: {[a.value for a in new_achievements]}")

            self._save_profile(profile)
            return True
        except Exception as e:
            logger.error(f"Error updating social profile for {profile.agent_id}: {e}")
            return False

    def record_interaction(self, interaction: SocialInteraction) -> bool:
        """Record a social interaction between agents."""
        try:
            # Update sender's profile
            sender_profile = self.get_or_create_profile(interaction.from_agent)
            sender_profile.add_interaction(interaction)
            self.update_profile(sender_profile)

            # Update receiver's profile (as received interaction)
            receiver_profile = self.get_or_create_profile(interaction.to_agent)
            # For receiver, create a mirrored interaction record
            receiver_interaction = SocialInteraction(
                interaction_id=f"recv_{interaction.interaction_id}",
                from_agent=interaction.to_agent,  # Reverse direction for receiver
                to_agent=interaction.from_agent,
                interaction_type=interaction.interaction_type,
                timestamp=interaction.timestamp,
                context=f"Received: {interaction.context}",
                impact_score=interaction.impact_score * 0.8,  # Slightly reduced impact for receiver
                metadata={**interaction.metadata, "original_interaction": interaction.interaction_id}
            )
            receiver_profile.add_interaction(receiver_interaction)
            self.update_profile(receiver_profile)

            # Update relationship between agents
            self._update_relationship_from_interaction(interaction)

            logger.debug(f"Recorded social interaction: {interaction.from_agent} -> {interaction.to_agent}")
            return True

        except Exception as e:
            logger.error(f"Error recording social interaction: {e}")
            return False

    def _update_relationship_from_interaction(self, interaction: SocialInteraction):
        """Update relationship based on interaction."""
        # Get or create relationship
        relationship = self._get_or_create_relationship(
            interaction.from_agent,
            interaction.to_agent,
            RelationshipType.COLLABORATOR  # Default type, can be updated later
        )

        if relationship:
            relationship.update_interaction(interaction.interaction_type)

            # Update both agents' profiles with the updated relationship
            sender_profile = self.profiles[interaction.from_agent]
            receiver_profile = self.profiles[interaction.to_agent]

            sender_profile.add_relationship(relationship)
            receiver_profile.add_relationship(relationship)

            self.update_profile(sender_profile)
            self.update_profile(receiver_profile)

    def _get_or_create_relationship(self, agent_a: str, agent_b: str,
                                  relationship_type: RelationshipType) -> Optional[AgentRelationship]:
        """Get existing relationship or create new one."""
        # Check if relationship exists in either agent's profile
        profile_a = self.profiles.get(agent_a)
        if profile_a:
            existing_rel = profile_a.get_relationship_with(agent_b)
            if existing_rel:
                return existing_rel

        # Create new relationship
        relationship = AgentRelationship(
            relationship_id="",
            agent_a=agent_a,
            agent_b=agent_b,
            relationship_type=relationship_type,
            strength=0.1,  # Start with low strength
            trust_level=0.5,  # Start with neutral trust
            created_at=datetime.now(),
            last_interaction=datetime.now(),
            interaction_count=0
        )

        return relationship

    def get_social_leaderboard(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get social leaderboard ranked by social scores."""
        leaderboard = []

        for profile in self.profiles.values():
            leaderboard.append({
                "agent_id": profile.agent_id,
                "social_score": profile.get_social_score(),
                "reputation_score": profile.reputation_score,
                "relationships": len(profile.get_active_relationships()),
                "collaborations": profile.collaboration_count,
                "achievements": len(profile.social_achievements),
                "last_activity": profile.last_social_activity.isoformat() if profile.last_social_activity else None
            })

        # Sort by social score descending
        leaderboard.sort(key=lambda x: x["social_score"], reverse=True)

        return leaderboard[:limit]

    def get_most_social_agents(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Get agents with highest social engagement."""
        social_stats = []

        for profile in self.profiles.values():
            social_stats.append({
                "agent_id": profile.agent_id,
                "total_interactions": len(profile.interaction_history),
                "relationships": len(profile.get_active_relationships()),
                "social_score": profile.get_social_score(),
                "last_activity": profile.last_social_activity
            })

        # Sort by total interactions descending
        social_stats.sort(key=lambda x: x["total_interactions"], reverse=True)

        return social_stats[:limit]

    def get_collaboration_network(self) -> Dict[str, Any]:
        """Get the collaboration network data for visualization."""
        nodes = []
        links = []

        # Create nodes for all agents with social profiles
        for agent_id, profile in self.profiles.items():
            nodes.append({
                "id": agent_id,
                "social_score": profile.get_social_score(),
                "relationships": len(profile.get_active_relationships()),
                "group": 1  # Could categorize by role or department
            })

        # Create links for relationships
        processed_relationships = set()
        for profile in self.profiles.values():
            for relationship in profile.get_active_relationships():
                # Avoid duplicate links
                rel_key = tuple(sorted([relationship.agent_a, relationship.agent_b]))
                if rel_key not in processed_relationships:
                    processed_relationships.add(rel_key)
                    links.append({
                        "source": relationship.agent_a,
                        "target": relationship.agent_b,
                        "strength": relationship.strength,
                        "trust": relationship.trust_level,
                        "interactions": relationship.interaction_count
                    })

        return {
            "nodes": nodes,
            "links": links,
            "metadata": {
                "total_agents": len(nodes),
                "total_relationships": len(links),
                "generated_at": datetime.now().isoformat()
            }
        }