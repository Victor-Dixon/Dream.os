"""Social Integration Service for Automatic Social Interaction Tracking.
<!-- SSOT Domain: gaming -->

Automatically tracks and records social interactions based on agent activities.

Author: Agent-6 - Gaming & Entertainment Specialist
V2 Compliance: Observer pattern, automatic social interaction detection
"""

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

from .social_profile_manager import SocialProfileManager
from ..models.social_models import (
    SocialInteraction,
    InteractionType,
    RelationshipType
)

logger = logging.getLogger(__name__)


class SocialIntegrationService:
    """Automatically integrates social tracking into agent activities."""

    def __init__(self):
        """Initialize social integration service."""
        self.profile_manager = SocialProfileManager()

    def track_quest_collaboration(self, quest_id: str, participants: List[str], context: str = "Quest collaboration"):
        """Track quest-related collaboration between agents."""
        if len(participants) < 2:
            return

        # Record interactions between all participant pairs
        for i, agent_a in enumerate(participants):
            for agent_b in participants[i+1:]:
                self._record_interaction(
                    from_agent=agent_a,
                    to_agent=agent_b,
                    interaction_type=InteractionType.COLLABORATION,
                    context=f"{context}: {quest_id}",
                    impact_score=0.3,
                    metadata={"quest_id": quest_id, "collaboration_type": "quest"}
                )

        logger.info(f"Tracked quest collaboration for {len(participants)} agents on quest {quest_id}")

    def track_coordination_message(self, from_agent: str, to_agents: List[str],
                                 message_category: str, context: str = "Coordination message"):
        """Track coordination messages between agents."""
        for to_agent in to_agents:
            interaction_type = InteractionType.COORDINATION
            impact_score = 0.2

            # Adjust based on message category
            if message_category == "a2a":
                impact_score = 0.4  # Agent-to-agent coordination is more valuable
            elif message_category == "c2a":
                interaction_type = InteractionType.HELP_PROVIDED
                impact_score = 0.3

            self._record_interaction(
                from_agent=from_agent,
                to_agent=to_agent,
                interaction_type=interaction_type,
                context=context,
                impact_score=impact_score,
                metadata={"message_category": message_category}
            )

        logger.debug(f"Tracked coordination message from {from_agent} to {len(to_agents)} agents")

    def track_help_interaction(self, helper: str, helpee: str,
                             help_type: str, context: str = "Help provided"):
        """Track help interactions between agents."""
        # Record help provided (positive impact for helper)
        self._record_interaction(
            from_agent=helper,
            to_agent=helpee,
            interaction_type=InteractionType.HELP_PROVIDED,
            context=f"{context}: {help_type}",
            impact_score=0.5,
            metadata={"help_type": help_type, "role": "helper"}
        )

        # Record help received (positive impact for helpee)
        self._record_interaction(
            from_agent=helpee,
            to_agent=helper,
            interaction_type=InteractionType.HELP_REQUEST,
            context=f"Received help: {help_type}",
            impact_score=0.3,
            metadata={"help_type": help_type, "role": "helpee"}
        )

        logger.info(f"Tracked help interaction: {helper} -> {helpee} ({help_type})")

    def track_achievement_sharing(self, from_agent: str, to_agents: List[str],
                                achievement: str, context: str = "Achievement shared"):
        """Track achievement sharing between agents."""
        for to_agent in to_agents:
            self._record_interaction(
                from_agent=from_agent,
                to_agent=to_agent,
                interaction_type=InteractionType.ACHIEVEMENT_SHARED,
                context=f"{context}: {achievement}",
                impact_score=0.2,
                metadata={"achievement": achievement}
            )

        logger.debug(f"Tracked achievement sharing from {from_agent} to {len(to_agents)} agents")

    def track_quest_sharing(self, from_agent: str, to_agents: List[str],
                          quest_id: str, context: str = "Quest shared"):
        """Track quest sharing between agents."""
        for to_agent in to_agents:
            self._record_interaction(
                from_agent=from_agent,
                to_agent=to_agent,
                interaction_type=InteractionType.QUEST_SHARED,
                context=f"{context}: {quest_id}",
                impact_score=0.25,
                metadata={"quest_id": quest_id}
            )

        logger.debug(f"Tracked quest sharing from {from_agent} to {len(to_agents)} agents")

    def track_competition_result(self, winner: str, loser: str,
                               competition_type: str, context: str = "Competition result"):
        """Track competition results between agents."""
        # Winner gets positive interaction
        self._record_interaction(
            from_agent=winner,
            to_agent=loser,
            interaction_type=InteractionType.COMPETITION,
            context=f"Won {competition_type}: {context}",
            impact_score=0.4,
            metadata={"competition_type": competition_type, "result": "win"}
        )

        # Loser gets neutral/positive interaction (healthy competition)
        self._record_interaction(
            from_agent=loser,
            to_agent=winner,
            interaction_type=InteractionType.COMPETITION,
            context=f"Lost {competition_type}: {context}",
            impact_score=0.1,
            metadata={"competition_type": competition_type, "result": "loss"}
        )

        logger.info(f"Tracked competition result: {winner} defeated {loser} in {competition_type}")

    def analyze_agent_activity(self, agent_id: str, activity_data: Dict[str, Any]):
        """Analyze agent activity and extract social interactions."""
        activity_type = activity_data.get("type", "")
        metadata = activity_data.get("metadata", {})

        # Analyze different activity types
        if activity_type == "message_sent":
            self._analyze_message_activity(agent_id, activity_data)
        elif activity_type == "quest_completed":
            self._analyze_quest_activity(agent_id, activity_data)
        elif activity_type == "achievement_unlocked":
            self._analyze_achievement_activity(agent_id, activity_data)
        elif activity_type == "coordination_initiated":
            self._analyze_coordination_activity(agent_id, activity_data)

    def _analyze_message_activity(self, agent_id: str, activity_data: Dict[str, Any]):
        """Analyze message sending activity for social interactions."""
        recipients = activity_data.get("recipients", [])
        message_category = activity_data.get("category", "general")
        context = activity_data.get("context", "Message sent")

        if recipients:
            self.track_coordination_message(
                from_agent=agent_id,
                to_agents=recipients,
                message_category=message_category,
                context=context
            )

    def _analyze_quest_activity(self, agent_id: str, activity_data: Dict[str, Any]):
        """Analyze quest completion activity."""
        quest_id = activity_data.get("quest_id", "")
        collaborators = activity_data.get("collaborators", [])

        if collaborators:
            self.track_quest_collaboration(
                quest_id=quest_id,
                participants=[agent_id] + collaborators,
                context="Quest completion collaboration"
            )

    def _analyze_achievement_activity(self, agent_id: str, activity_data: Dict[str, Any]):
        """Analyze achievement unlocking activity."""
        achievement = activity_data.get("achievement", "")
        shared_with = activity_data.get("shared_with", [])

        if shared_with:
            self.track_achievement_sharing(
                from_agent=agent_id,
                to_agents=shared_with,
                achievement=achievement,
                context="Achievement unlocked and shared"
            )

    def _analyze_coordination_activity(self, agent_id: str, activity_data: Dict[str, Any]):
        """Analyze coordination initiation activity."""
        participants = activity_data.get("participants", [])
        coordination_type = activity_data.get("coordination_type", "general")

        if len(participants) > 1:
            # Record coordination interactions
            for participant in participants:
                if participant != agent_id:
                    self._record_interaction(
                        from_agent=agent_id,
                        to_agent=participant,
                        interaction_type=InteractionType.COORDINATION,
                        context=f"Coordinated {coordination_type}",
                        impact_score=0.3,
                        metadata={"coordination_type": coordination_type}
                    )

    def _record_interaction(self, from_agent: str, to_agent: str,
                          interaction_type: InteractionType, context: str,
                          impact_score: float, metadata: Optional[Dict[str, Any]] = None):
        """Record a social interaction."""
        interaction = SocialInteraction(
            interaction_id="",
            from_agent=from_agent,
            to_agent=to_agent,
            interaction_type=interaction_type,
            timestamp=datetime.now(),
            context=context,
            impact_score=impact_score,
            metadata=metadata or {}
        )

        self.profile_manager.record_interaction(interaction)

    def get_agent_social_insights(self, agent_id: str) -> Dict[str, Any]:
        """Get social insights for an agent."""
        profile = self.profile_manager.get_profile(agent_id)
        if not profile:
            return {"agent_id": agent_id, "insights": "No social data available"}

        # Calculate insights
        insights = {
            "agent_id": agent_id,
            "social_score": profile.get_social_score(),
            "relationship_network_size": len(profile.get_active_relationships()),
            "collaboration_frequency": profile.collaboration_count,
            "help_ratio": (profile.help_provided_count / max(1, profile.help_received_count)),
            "most_common_interaction": self._get_most_common_interaction(profile),
            "social_growth_trend": self._calculate_social_growth(profile),
            "recommendations": self._generate_social_recommendations(profile)
        }

        return insights

    def _get_most_common_interaction(self, profile) -> str:
        """Get the most common interaction type for an agent."""
        interaction_counts = {}
        for interaction in profile.interaction_history:
            interaction_type = interaction.interaction_type.value
            interaction_counts[interaction_type] = interaction_counts.get(interaction_type, 0) + 1

        if not interaction_counts:
            return "none"

        return max(interaction_counts, key=interaction_counts.get)

    def _calculate_social_growth(self, profile) -> str:
        """Calculate social growth trend."""
        recent_interactions = [i for i in profile.interaction_history
                             if (datetime.now() - i.timestamp).days <= 7]
        older_interactions = [i for i in profile.interaction_history
                            if (datetime.now() - i.timestamp).days > 7]

        recent_count = len(recent_interactions)
        older_count = len(older_interactions)

        if recent_count > older_count * 1.2:
            return "growing"
        elif recent_count < older_count * 0.8:
            return "declining"
        else:
            return "stable"

    def _generate_social_recommendations(self, profile) -> List[str]:
        """Generate social recommendations for an agent."""
        recommendations = []

        if len(profile.get_active_relationships()) < 3:
            recommendations.append("Consider reaching out to more agents for collaboration")

        if profile.collaboration_count < 5:
            recommendations.append("Try participating in more group quests or projects")

        if profile.help_provided_count < profile.help_received_count:
            recommendations.append("Consider offering help to other agents more often")

        if not profile.social_achievements:
            recommendations.append("Focus on building social achievements through interactions")

        most_common = self._get_most_common_interaction(profile)
        if most_common == "collaboration":
            recommendations.append("Great at collaboration! Consider mentoring others")
        elif most_common == "competition":
            recommendations.append("Consider balancing competition with more collaborative activities")

        return recommendations[:3]  # Limit to top 3 recommendations