"""
Integration Tests for Gaming System
====================================

Comprehensive integration tests for the gaming system including:
- Leaderboards
- Quests
- Social features
- Analytics
- Performance metrics

Author: Agent-6 - Quality Assurance & Testing Lead
"""

import pytest
import asyncio
import random
from unittest.mock import Mock, patch, AsyncMock
from datetime import datetime, timedelta

# Import gaming system components
from src.gaming.models.gaming_models import GameType, GameSession, EntertainmentSystem
from src.gaming.models.quest_models import Quest, QuestType, QuestDifficulty, QuestStatus
from src.gaming.models.social_models import AgentSocialProfile, SocialInteraction, InteractionType
from src.gaming.quests.quest_generator import DynamicQuestGenerator
from src.gaming.quests.quest_manager import QuestManager
from src.gaming.social.social_profile_manager import SocialProfileManager
from src.gaming.social.social_integration_service import SocialIntegrationService
from src.gaming.analytics.performance_analytics import PerformanceAnalytics
from src.gaming.dreamos.ui_integration import gamification_bp


def test_gaming_system_imports():
    """Test that all gaming system components can be imported."""
    # All imports are done at module level above
    assert True, "All gaming system components imported successfully"


class TestQuestSystemIntegration:
    """Integration tests for the quest system."""

    def setup_method(self):
        """Set up test fixtures."""
        self.quest_manager = QuestManager()
        self.generator = DynamicQuestGenerator()

    def test_quest_creation_workflow(self):
        """Test complete quest creation workflow."""
        agent_id = "TestAgent"
        quest_type = QuestType.COLLABORATION
        difficulty = QuestDifficulty.MEDIUM

        # Create quest
        quest = self.quest_manager.create_quest(agent_id, quest_type, difficulty)

        assert quest is not None
        assert quest.assigned_agent == agent_id
        assert quest.quest_type == quest_type
        assert quest.difficulty == difficulty
        assert quest.status == QuestStatus.AVAILABLE
        assert len(quest.objectives) > 0

    def test_quest_lifecycle(self):
        """Test complete quest lifecycle from creation to completion."""
        agent_id = "TestAgent"

        # Create and start quest
        quest = self.quest_manager.create_quest(agent_id, QuestType.DEVELOPMENT, QuestDifficulty.EASY)
        assert quest is not None

        quest_id = quest.quest_id

        # Start quest
        success = self.quest_manager.start_quest(quest_id)
        assert success

        quest = self.quest_manager.get_quest(quest_id)
        assert quest.status == QuestStatus.ACTIVE
        assert quest.started_at is not None

        # Update progress (assume we complete all objectives)
        for objective in quest.objectives:
            self.quest_manager.update_quest_progress(quest_id, objective.objective_id, objective.target_value)

        # Complete quest
        success = self.quest_manager.complete_quest(quest_id)
        assert success

        quest = self.quest_manager.get_quest(quest_id)
        assert quest.status == QuestStatus.COMPLETED
        assert quest.completed_at is not None
        assert quest.progress_percentage == 100.0

    def test_quest_agent_filtering(self):
        """Test that quests are properly filtered by agent."""
        agent_a = "AgentA"
        agent_b = "AgentB"

        # Create quests for different agents
        quest_a = self.quest_manager.create_quest(agent_a, QuestType.COLLABORATION, QuestDifficulty.EASY)
        quest_b = self.quest_manager.create_quest(agent_b, QuestType.DEVELOPMENT, QuestDifficulty.MEDIUM)

        # Get quests for each agent
        quests_a = self.quest_manager.get_agent_quests(agent_a)
        quests_b = self.quest_manager.get_agent_quests(agent_b)

        # Verify correct filtering
        assert len(quests_a) == 1
        assert len(quests_b) == 1
        assert quests_a[0].assigned_agent == agent_a
        assert quests_b[0].assigned_agent == agent_b


class TestSocialSystemIntegration:
    """Integration tests for the social system."""

    def setup_method(self):
        """Set up test fixtures."""
        self.social_manager = SocialProfileManager()
        self.integration_service = SocialIntegrationService()

    def test_social_profile_creation(self):
        """Test social profile creation and basic functionality."""
        agent_id = "TestAgent"

        # Create profile
        profile = self.social_manager.get_or_create_profile(agent_id)

        assert profile.agent_id == agent_id
        assert profile.reputation_score == 0.0
        assert len(profile.relationships) == 0
        assert len(profile.interaction_history) == 0

    def test_social_interaction_recording(self):
        """Test recording social interactions between agents."""
        agent_a = "AgentA"
        agent_b = "AgentB"

        # Create profiles
        profile_a = self.social_manager.get_or_create_profile(agent_a)
        profile_b = self.social_manager.get_or_create_profile(agent_b)

        # Record interaction
        interaction = SocialInteraction(
            interaction_id="",
            from_agent=agent_a,
            to_agent=agent_b,
            interaction_type=InteractionType.COLLABORATION,
            timestamp=datetime.now(),
            context="Collaborated on project",
            impact_score=0.5
        )

        success = self.social_manager.record_interaction(interaction)
        assert success

        # Verify interaction was recorded
        profile_a_updated = self.social_manager.get_profile(agent_a)
        profile_b_updated = self.social_manager.get_profile(agent_b)

        assert len(profile_a_updated.interaction_history) == 1
        assert len(profile_b_updated.interaction_history) == 1

        # Check relationship was created
        assert len(profile_a_updated.relationships) == 1
        assert len(profile_b_updated.relationships) == 1

    def test_social_analytics(self):
        """Test social analytics calculations."""
        agent_id = "TestAgent"

        # Create profile and add interactions
        profile = self.social_manager.get_or_create_profile(agent_id)

        # Add multiple interactions
        interactions = [
            SocialInteraction("", agent_id, "OtherAgent1", InteractionType.COLLABORATION,
                            datetime.now(), "Collaboration 1", 0.3),
            SocialInteraction("", agent_id, "OtherAgent2", InteractionType.HELP_PROVIDED,
                            datetime.now(), "Help provided", 0.5),
            SocialInteraction("", "OtherAgent3", agent_id, InteractionType.QUEST_SHARED,
                            datetime.now(), "Quest shared", 0.2),
        ]

        for interaction in interactions:
            self.social_manager.record_interaction(interaction)

        # Test analytics
        insights = self.integration_service.get_agent_social_insights(agent_id)

        assert insights["agent_id"] == agent_id
        assert "social_score" in insights
        assert "relationship_network_size" in insights
        assert "recommendations" in insights

    def test_social_leaderboard(self):
        """Test social leaderboard generation."""
        # Create multiple profiles with different activity levels
        agents = ["Agent1", "Agent2", "Agent3"]

        for i, agent_id in enumerate(agents):
            profile = self.social_manager.get_or_create_profile(agent_id)
            # Simulate different activity levels
            profile.reputation_score = (i + 1) * 10
            profile.collaboration_count = (i + 1) * 2
            self.social_manager.update_profile(profile)

        # Get leaderboard
        leaderboard = self.social_manager.get_social_leaderboard(limit=5)

        assert len(leaderboard) == 3
        # Should be sorted by social score descending
        assert leaderboard[0]["social_score"] >= leaderboard[1]["social_score"]


class TestAnalyticsSystemIntegration:
    """Integration tests for the analytics system."""

    def setup_method(self):
        """Set up test fixtures."""
        self.analytics = PerformanceAnalytics()

    def test_metric_recording_and_analysis(self):
        """Test recording metrics and analyzing them."""
        metric_name = "test_response_time"

        # Record some metrics
        values = [150, 200, 120, 180, 160]
        for value in values:
            self.analytics.record_metric(metric_name, value)

        # Get statistics
        stats = self.analytics.calculate_metric_stats(metric_name)

        assert stats["metric"] == metric_name
        assert stats["count"] == len(values)
        assert stats["avg"] == sum(values) / len(values)
        assert stats["min"] == min(values)
        assert stats["max"] == max(values)

    def test_health_score_calculation(self):
        """Test system health score calculation."""
        # Record metrics for health calculation
        self.analytics.record_metric("response_time", 150)
        self.analytics.record_metric("engagement_rate", 85)
        self.analytics.record_metric("completion_rate", 92)
        self.analytics.record_metric("social_interaction_rate", 5)
        self.analytics.record_metric("error_rate", 1)

        health = self.analytics.get_system_health_score()

        assert "overall_score" in health
        assert "health_status" in health
        assert "components" in health
        assert isinstance(health["overall_score"], (int, float))

    def test_performance_report_generation(self):
        """Test comprehensive performance report generation."""
        # Add some test data
        self.analytics.record_metric("response_time", 145)
        self.analytics.record_metric("engagement_rate", 88)

        report = self.analytics.generate_performance_report(hours=1)

        assert "generated_at" in report
        assert "system_health" in report
        assert "metrics_summary" in report
        assert "insights" in report
        assert "recommendations" in report


class TestGamingAPIIntegration:
    """Integration tests for gaming API endpoints."""

    def setup_method(self):
        """Set up test fixtures."""
        from src.gaming.dreamos.ui_integration import gamification_bp
        self.app = None  # Would need Flask test client setup

    @pytest.mark.skip(reason="Requires Flask test client setup")
    def test_leaderboard_endpoint(self):
        """Test leaderboard API endpoint."""
        # This would test the actual API endpoint with Flask test client
        pass

    @pytest.mark.skip(reason="Requires Flask test client setup")
    def test_quest_creation_endpoint(self):
        """Test quest creation API endpoint."""
        # This would test quest creation via API
        pass

    @pytest.mark.skip(reason="Requires Flask test client setup")
    def test_social_profile_endpoint(self):
        """Test social profile API endpoint."""
        # This would test social profile retrieval
        pass


class TestEndToEndGamingWorkflow:
    """End-to-end tests for complete gaming workflows."""

    def setup_method(self):
        """Set up complete gaming system for end-to-end testing."""
        self.quest_manager = QuestManager()
        self.social_manager = SocialProfileManager()
        self.integration_service = SocialIntegrationService()
        self.analytics = PerformanceAnalytics()

    def test_complete_agent_gaming_journey(self):
        """Test complete agent journey through gaming system."""
        agent_id = "TestAgent"

        # 1. Create social profile
        profile = self.social_manager.get_or_create_profile(agent_id)
        assert profile.agent_id == agent_id

        # 2. Generate and accept quest
        quest = self.quest_manager.create_quest(agent_id, QuestType.DEVELOPMENT, QuestDifficulty.EASY)
        assert quest is not None

        # 3. Start quest
        success = self.quest_manager.start_quest(quest.quest_id)
        assert success

        # 4. Complete quest objectives
        for objective in quest.objectives:
            self.quest_manager.update_quest_progress(quest.quest_id, objective.objective_id, objective.target_value)

        # 5. Complete quest
        success = self.quest_manager.complete_quest(quest.quest_id)
        assert success

        # 6. Record completion as social interaction
        completion_interaction = SocialInteraction(
            "", agent_id, "System", InteractionType.HELP_PROVIDED,
            datetime.now(), f"Completed quest: {quest.title}", 0.3
        )
        self.social_manager.record_interaction(completion_interaction)

        # 7. Update analytics
        self.analytics.record_metric("quest_completion_rate", 100)
        self.analytics.record_metric("agent_engagement", 85)

        # 8. Verify final state
        updated_profile = self.social_manager.get_profile(agent_id)
        completed_quests = self.quest_manager.get_agent_quests(agent_id)

        assert len([q for q in completed_quests if q.status == QuestStatus.COMPLETED]) >= 1
        assert updated_profile.reputation_score > 0
        assert len(updated_profile.interaction_history) > 0

        # 9. Generate final analytics
        health = self.analytics.get_system_health_score()
        assert health["overall_score"] > 0

        print(f"✅ Complete gaming journey test passed for {agent_id}")
        print(f"   • Social score: {updated_profile.get_social_score():.1f}")
        print(f"   • Completed quests: {len([q for q in completed_quests if q.status == QuestStatus.COMPLETED])}")
        print(f"   • System health: {health['overall_score']:.1f}")


# Integration test utilities
def create_test_agent_context(agent_id: str) -> dict:
    """Create test agent context for gaming system testing."""
    return {
        "agent_id": agent_id,
        "capabilities": ["development", "collaboration", "communication"],
        "status": {
            "current_phase": "PHASE_5",
            "mission_priority": "HIGH",
            "current_mission": "Gaming system testing"
        }
    }


def simulate_agent_interactions(agent_network: list, interaction_count: int = 5):
    """Simulate interactions between agents in a network."""
    from src.gaming.social.social_profile_manager import SocialProfileManager

    social_manager = SocialProfileManager()

    for _ in range(interaction_count):
        agent_a, agent_b = random.sample(agent_network, 2)

        interaction = SocialInteraction(
            "", agent_a, agent_b,
            random.choice(list(InteractionType)),
            datetime.now(),
            f"Simulated interaction between {agent_a} and {agent_b}",
            random.uniform(0.1, 0.8)
        )

        social_manager.record_interaction(interaction)

    return social_manager