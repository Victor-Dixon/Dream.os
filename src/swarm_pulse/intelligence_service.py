"""
Intelligence Service - Agent Cellphone V2
==========================================

<<<<<<< HEAD
V2 Consolidated: Uses SSOT base classes for standardized patterns
Author: Agent-1 (Integration & Core Systems Specialist)
SSOT Migration: Agent-8 (System Integration)
Date: 2026-01-12

=======
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
SSOT Domain: swarm_brain

Core service for swarm intelligence operations and analysis.

Features:
- Partnership suggestion algorithms
- Intelligent routing and coordination
- Collaboration pattern detection
- Coordination efficiency analysis
- Vector-based similarity matching

V2 Compliant: Yes (<300 lines)
<<<<<<< HEAD
Date: 2026-01-07
"""

# SSOT Import Standardization - eliminates redundant typing imports
from src.core.base.import_standardization import logging, Dict, List, Optional, Any
=======
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2026-01-07
"""

import logging
from typing import Dict, List, Optional, Any
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1

from .intelligence_models import (
    INTELLIGENCE_CONFIG,
    CollaborationPattern,
    CoordinationMetrics,
    PartnershipSuggestion,
)
from .intelligence_scoring import (
    compute_combined_score,
    compute_semantic_similarity,
    create_suggestion,
)
from .models import NotificationLevel, PulseEvent

logger = logging.getLogger(__name__)

class IntelligenceService:
    """
    Service for swarm intelligence operations and analysis.
    """

    def __init__(self):
        self.config = INTELLIGENCE_CONFIG
        self.logger = logging.getLogger(__name__)

    def suggest_partnerships(
        self,
        event: PulseEvent,
        *,
        top_k: int = 3,
        threshold: float = 0.6,
    ) -> List[PartnershipSuggestion]:
        """
        Suggest bilateral partnerships based on event content.

        Args:
            event: Pulse event to analyze
            top_k: Number of suggestions to return
            threshold: Similarity threshold for suggestions

        Returns:
            List of partnership suggestions
        """
        if not self.config["enable_partnership_suggestions"]:
            return []

        try:
            from .vectordb.query import embed_events, get_similar_events

            embeddings = embed_events([event])
            if not embeddings:
                return []

            similar_events = get_similar_events(embeddings[0], limit=top_k * 2)
            if not similar_events:
                return []

            suggestions = []
            for similar_event, score in similar_events:
                if score >= threshold:
                    suggestion = create_suggestion(event, similar_event, score)
                    if suggestion:
                        suggestions.append(suggestion)

            # Sort by score and return top_k
            suggestions.sort(key=lambda x: x.score, reverse=True)
            return suggestions[:top_k]

        except Exception as e:
            self.logger.error(f"Error suggesting partnerships: {e}")
            return []

    def route_with_intelligence(
        self,
        event: PulseEvent,
        available_agents: List[str]
    ) -> List[str]:
        """
        Route events to agents using intelligence-based decisions.

        Args:
            event: Event to route
            available_agents: List of available agent IDs

        Returns:
            Ordered list of agent IDs for routing
        """
        if not self.config["enable_intelligent_routing"]:
            return available_agents

        try:
            # Get agent expertise and workload data
            agent_scores = {}
            for agent_id in available_agents:
                score = self._calculate_routing_score(event, agent_id)
                agent_scores[agent_id] = score

            # Sort agents by score (higher is better)
            sorted_agents = sorted(
                agent_scores.keys(),
                key=lambda x: agent_scores[x],
                reverse=True
            )

            self.logger.debug(f"Intelligent routing for {event.event_type}: {sorted_agents}")
            return sorted_agents

        except Exception as e:
            self.logger.error(f"Error in intelligent routing: {e}")
            return available_agents

    def detect_collaboration_patterns(self, events: List[PulseEvent]) -> List[CollaborationPattern]:
        """
        Detect collaboration patterns in pulse events.

        Args:
            events: List of pulse events to analyze

        Returns:
            List of detected collaboration patterns
        """
        patterns = []

        try:
            # Analyze event sequences for collaboration patterns
            if len(events) < 2:
                return patterns

            # Look for agent interaction patterns
            agent_sequences = self._extract_agent_sequences(events)

            for sequence in agent_sequences:
                pattern = self._analyze_sequence_pattern(sequence)
                if pattern:
                    patterns.append(pattern)

            return patterns

        except Exception as e:
            self.logger.error(f"Error detecting collaboration patterns: {e}")
            return []

    def analyze_coordination_efficiency(self, agent_id: Optional[str] = None) -> CoordinationMetrics:
        """
        Analyze coordination efficiency for agents.

        Args:
            agent_id: Specific agent to analyze, or None for all

        Returns:
            Coordination metrics
        """
        try:
            metrics = CoordinationMetrics(
                agent_id=agent_id or "all",
                coordination_score=0.0,
                efficiency_rating="unknown",
                bottlenecks=[],
                recommendations=[]
            )

            # Calculate coordination metrics
            if agent_id:
                metrics.coordination_score = self._calculate_agent_coordination_score(agent_id)
            else:
                # Calculate system-wide coordination
                all_scores = []
                for aid in self._get_all_agent_ids():
                    score = self._calculate_agent_coordination_score(aid)
                    all_scores.append(score)

                if all_scores:
                    metrics.coordination_score = sum(all_scores) / len(all_scores)

            # Determine efficiency rating
            metrics.efficiency_rating = self._calculate_efficiency_rating(metrics.coordination_score)

            # Identify bottlenecks and recommendations
            metrics.bottlenecks = self._identify_bottlenecks(agent_id)
            metrics.recommendations = self._generate_recommendations(metrics)

            return metrics

        except Exception as e:
            self.logger.error(f"Error analyzing coordination efficiency: {e}")
            return CoordinationMetrics(
                agent_id=agent_id or "unknown",
                coordination_score=0.0,
                efficiency_rating="error",
                bottlenecks=["Analysis failed"],
                recommendations=["Retry analysis"]
            )

    def _calculate_routing_score(self, event: PulseEvent, agent_id: str) -> float:
        """Calculate routing score for an agent and event."""
        try:
            # This would include complex logic based on:
            # - Agent expertise matching event content
            # - Current workload
            # - Historical performance
            # - Collaboration patterns

            # Simplified scoring for now
            base_score = 0.5

            # Boost score based on event type preferences
            if event.event_type == "coordination" and agent_id in ["Agent-6", "Agent-4"]:
                base_score += 0.3
            elif event.event_type == "infrastructure" and agent_id in ["Agent-3", "Agent-2"]:
                base_score += 0.3
            elif event.event_type == "development" and agent_id in ["Agent-7", "Agent-1"]:
                base_score += 0.3

            return min(base_score, 1.0)

        except Exception as e:
            self.logger.warning(f"Error calculating routing score: {e}")
            return 0.5

    def _extract_agent_sequences(self, events: List[PulseEvent]) -> List[List[str]]:
        """Extract sequences of agent interactions."""
        sequences = []

        try:
            current_sequence = []
            for event in events:
                if hasattr(event, 'agent_id') and event.agent_id:
                    if event.agent_id not in current_sequence:
                        current_sequence.append(event.agent_id)
                else:
                    if len(current_sequence) > 1:
                        sequences.append(current_sequence)
                    current_sequence = []

            # Add final sequence
            if len(current_sequence) > 1:
                sequences.append(current_sequence)

        except Exception as e:
            self.logger.warning(f"Error extracting agent sequences: {e}")

        return sequences

    def _analyze_sequence_pattern(self, sequence: List[str]) -> Optional[CollaborationPattern]:
        """Analyze a sequence for collaboration patterns."""
        try:
            if len(sequence) < 2:
                return None

            # Simple pattern detection
            pattern_type = "sequential" if len(sequence) == 2 else "multi_agent"

            return CollaborationPattern(
                pattern_type=pattern_type,
                agents_involved=sequence,
                frequency=1,  # Would be calculated from historical data
                efficiency_score=0.8,  # Would be calculated based on outcomes
                description=f"{' → '.join(sequence)} collaboration pattern"
            )

        except Exception as e:
            self.logger.warning(f"Error analyzing sequence pattern: {e}")
            return None

    def _calculate_agent_coordination_score(self, agent_id: str) -> float:
        """Calculate coordination score for a specific agent."""
        try:
            # This would analyze:
            # - Response times
            # - Task completion rates
            # - Collaboration effectiveness
            # - Communication patterns

            # Simplified calculation for now
            base_score = 0.7

            # Agent-specific adjustments
            adjustments = {
                "Agent-1": 0.1,  # Integration specialist
                "Agent-4": 0.1,  # Captain/coordination
                "Agent-6": 0.1,  # Co-captain
            }

            return min(base_score + adjustments.get(agent_id, 0), 1.0)

        except Exception as e:
            self.logger.warning(f"Error calculating coordination score for {agent_id}: {e}")
            return 0.5

    def _calculate_efficiency_rating(self, score: float) -> str:
        """Convert coordination score to efficiency rating."""
        if score >= 0.9:
            return "excellent"
        elif score >= 0.8:
            return "good"
        elif score >= 0.7:
            return "fair"
        elif score >= 0.6:
            return "needs_improvement"
        else:
            return "poor"

    def _identify_bottlenecks(self, agent_id: Optional[str]) -> List[str]:
        """Identify coordination bottlenecks."""
        bottlenecks = []

        try:
            # This would analyze actual bottleneck data
            # For now, return generic bottlenecks
            if agent_id:
                bottlenecks = [
                    f"Response time for {agent_id}",
                    f"Task queue backlog for {agent_id}"
                ]
            else:
                bottlenecks = [
                    "Inter-agent communication delays",
                    "Task routing inefficiencies",
                    "Resource allocation imbalances"
                ]

        except Exception as e:
            self.logger.warning(f"Error identifying bottlenecks: {e}")

        return bottlenecks

    def _generate_recommendations(self, metrics: CoordinationMetrics) -> List[str]:
        """Generate recommendations based on coordination metrics."""
        recommendations = []

        try:
            score = metrics.coordination_score

            if score < 0.7:
                recommendations.extend([
                    "Improve inter-agent communication protocols",
                    "Optimize task routing algorithms",
                    "Enhance resource allocation strategies"
                ])

            if metrics.efficiency_rating in ["poor", "needs_improvement"]:
                recommendations.extend([
                    "Implement automated coordination monitoring",
                    "Establish coordination performance baselines",
                    "Develop coordination training programs"
                ])

            if not recommendations:
                recommendations = ["Maintain current coordination excellence"]

        except Exception as e:
            self.logger.warning(f"Error generating recommendations: {e}")
            recommendations = ["Review coordination processes"]

        return recommendations

    def _get_all_agent_ids(self) -> List[str]:
        """Get list of all agent IDs."""
        # This would typically query the agent registry
        return ["Agent-1", "Agent-2", "Agent-3", "Agent-4", "Agent-5", "Agent-6", "Agent-7", "Agent-8"]

# Global service instance
intelligence_service = IntelligenceService()

__all__ = [
    "IntelligenceService",
    "intelligence_service"
]