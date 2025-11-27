"""
Tests for Swarm Coordination Analyzer - Real Implementation
===========================================================

Tests the real collaboration, mission coordination, and performance trend analysis.

Author: Agent-5 (Business Intelligence Specialist)
Date: 2025-01-27
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, MagicMock

from src.core.vector_strategic_oversight.unified_strategic_oversight.analyzers.swarm_analyzer import (
    SwarmCoordinationAnalyzer,
)
from src.core.vector_strategic_oversight.unified_strategic_oversight.enums import (
    ConfidenceLevel,
    ImpactLevel,
    InsightType,
)


class TestSwarmCoordinationAnalyzer:
    """Test suite for SwarmCoordinationAnalyzer real implementation."""

    @pytest.fixture
    def analyzer(self):
        """Create SwarmCoordinationAnalyzer instance."""
        return SwarmCoordinationAnalyzer()

    @pytest.fixture
    def sample_agent_data(self):
        """Sample agent data for testing."""
        return [
            {"agent_id": "Agent-1", "status": "ACTIVE_AGENT_MODE"},
            {"agent_id": "Agent-2", "status": "ACTIVE_AGENT_MODE"},
            {"agent_id": "Agent-5", "status": "ACTIVE_AGENT_MODE"},
        ]

    @pytest.fixture
    def sample_mission_data(self):
        """Sample mission data for testing."""
        return [
            {
                "mission_id": "mission_1",
                "status": "completed",
                "completed_at": datetime.now().isoformat(),
                "assigned_agent_id": "Agent-1",
            },
            {
                "mission_id": "mission_2",
                "status": "in_progress",
                "assigned_agent_id": "Agent-2",
            },
        ]

    @pytest.mark.asyncio
    async def test_analyze_collaboration_patterns_with_message_data(self, analyzer, sample_agent_data):
        """Test collaboration analysis with real message history."""
        # Mock message history
        mock_messages = [
            {"from": "Agent-1", "to": "Agent-2", "timestamp": datetime.now().isoformat()},
            {"from": "Agent-2", "to": "Agent-1", "timestamp": datetime.now().isoformat()},
            {"from": "Agent-1", "to": "Agent-5", "timestamp": datetime.now().isoformat()},
            {"from": "Agent-5", "to": "Agent-1", "timestamp": datetime.now().isoformat()},
        ]
        
        with patch('src.core.vector_strategic_oversight.unified_strategic_oversight.analyzers.swarm_analyzer.MessageRepository') as mock_repo_class:
            mock_repo = Mock()
            mock_repo.get_message_history.return_value = mock_messages
            mock_repo_class.return_value = mock_repo
            
            insights = await analyzer._analyze_collaboration_patterns(sample_agent_data)
            
            assert len(insights) > 0
            insight = insights[0]
            assert insight.insight_type == InsightType.COLLABORATION
            assert insight.confidence_level in [
                ConfidenceLevel.VERY_HIGH,
                ConfidenceLevel.HIGH,
                ConfidenceLevel.MEDIUM,
                ConfidenceLevel.LOW,
            ]
            assert len(insight.key_findings) > 0
            assert len(insight.recommendations) > 0

    @pytest.mark.asyncio
    async def test_analyze_collaboration_patterns_no_data(self, analyzer, sample_agent_data):
        """Test collaboration analysis with no message data."""
        with patch('src.core.vector_strategic_oversight.unified_strategic_oversight.analyzers.swarm_analyzer.MessageRepository') as mock_repo_class:
            mock_repo = Mock()
            mock_repo.get_message_history.return_value = []
            mock_repo_class.return_value = mock_repo
            
            insights = await analyzer._analyze_collaboration_patterns(sample_agent_data)
            
            # Should return minimal insight or empty
            assert isinstance(insights, list)

    @pytest.mark.asyncio
    async def test_analyze_collaboration_patterns_import_error(self, analyzer, sample_agent_data):
        """Test collaboration analysis with import error."""
        with patch('src.core.vector_strategic_oversight.unified_strategic_oversight.analyzers.swarm_analyzer.MessageRepository', side_effect=ImportError("Repository not available")):
            insights = await analyzer._analyze_collaboration_patterns(sample_agent_data)
            # Should handle error gracefully
            assert isinstance(insights, list)

    @pytest.mark.asyncio
    async def test_analyze_mission_coordination_with_task_data(self, analyzer, sample_mission_data):
        """Test mission coordination analysis with real task data."""
        # Mock task data
        mock_task = Mock()
        mock_task.completed_at = datetime.now()
        mock_task.assigned_at = datetime.now() - timedelta(hours=2)
        mock_task.assigned_agent_id = "Agent-1"
        
        with patch('src.core.vector_strategic_oversight.unified_strategic_oversight.analyzers.swarm_analyzer.TaskRepository') as mock_repo_class, \
             patch('src.core.vector_strategic_oversight.unified_strategic_oversight.analyzers.swarm_analyzer.DatabaseConnection'):
            
            mock_repo = Mock()
            mock_repo.list_all.return_value = [mock_task, mock_task]
            mock_repo_class.return_value = mock_repo
            
            insights = await analyzer._analyze_mission_coordination(sample_mission_data)
            
            assert len(insights) > 0
            insight = insights[0]
            assert insight.insight_type == InsightType.MISSION_COORDINATION
            assert insight.confidence_level in [
                ConfidenceLevel.VERY_HIGH,
                ConfidenceLevel.HIGH,
                ConfidenceLevel.MEDIUM,
                ConfidenceLevel.LOW,
            ]
            assert len(insight.key_findings) > 0
            assert "completion rate" in " ".join(insight.key_findings).lower()

    @pytest.mark.asyncio
    async def test_analyze_mission_coordination_direct_fallback(self, analyzer, sample_mission_data):
        """Test mission coordination with direct data analysis fallback."""
        with patch('src.core.vector_strategic_oversight.unified_strategic_oversight.analyzers.swarm_analyzer.TaskRepository', side_effect=ImportError("Repository not available")):
            insights = await analyzer._analyze_mission_coordination(sample_mission_data)
            
            assert len(insights) > 0
            insight = insights[0]
            assert insight.insight_type == InsightType.MISSION_COORDINATION

    @pytest.mark.asyncio
    async def test_analyze_performance_trends_with_metrics(self, analyzer, sample_agent_data):
        """Test performance trend analysis with real metrics data."""
        # Mock metrics snapshots
        mock_snapshots = [
            {
                "timestamp": (datetime.now() - timedelta(hours=1)).isoformat(),
                "metrics": {"queue.processing": 1.5, "queue.depth": 10},
            },
            {
                "timestamp": (datetime.now() - timedelta(hours=2)).isoformat(),
                "metrics": {"queue.processing": 2.0, "queue.depth": 15},
            },
        ]
        
        with patch('src.core.vector_strategic_oversight.unified_strategic_oversight.analyzers.swarm_analyzer.MetricsRepository') as mock_repo_class:
            mock_repo = Mock()
            mock_repo.get_metrics_history.return_value = mock_snapshots
            mock_repo.get_metrics_trend.return_value = [1.5, 2.0, 1.8, 1.6]  # Improving trend
            mock_repo_class.return_value = mock_repo
            
            insights = await analyzer._analyze_performance_trends(sample_agent_data, time_window_hours=24)
            
            assert len(insights) > 0
            insight = insights[0]
            assert insight.insight_type == InsightType.PERFORMANCE
            assert insight.confidence_level in [
                ConfidenceLevel.VERY_HIGH,
                ConfidenceLevel.HIGH,
                ConfidenceLevel.MEDIUM,
                ConfidenceLevel.LOW,
            ]
            assert len(insight.key_findings) > 0
            assert "trend" in insight.description.lower()

    @pytest.mark.asyncio
    async def test_analyze_performance_trends_fallback(self, analyzer, sample_agent_data):
        """Test performance trend analysis fallback to agent data."""
        with patch('src.core.vector_strategic_oversight.unified_strategic_oversight.analyzers.swarm_analyzer.MetricsRepository', side_effect=ImportError("Repository not available")):
            insights = await analyzer._analyze_performance_trends(sample_agent_data, time_window_hours=24)
            
            assert len(insights) > 0
            insight = insights[0]
            assert insight.insight_type == InsightType.PERFORMANCE

    @pytest.mark.asyncio
    async def test_analyze_swarm_coordination_integration(self, analyzer, sample_agent_data, sample_mission_data):
        """Test full swarm coordination analysis integration."""
        with patch.object(analyzer, '_analyze_collaboration_patterns', return_value=[]), \
             patch.object(analyzer, '_analyze_mission_coordination', return_value=[]), \
             patch.object(analyzer, '_analyze_performance_trends', return_value=[]):
            
            insights = await analyzer.analyze_swarm_coordination(
                sample_agent_data, sample_mission_data, time_window_hours=24
            )
            
            assert isinstance(insights, list)
            # Should have analysis history entry
            assert len(analyzer.analysis_history) > 0

    def test_analyze_mission_data_directly(self, analyzer):
        """Test direct mission data analysis fallback."""
        mission_data = [
            {"status": "completed", "mission_id": "m1"},
            {"status": "in_progress", "mission_id": "m2"},
        ]
        
        insights = analyzer._analyze_mission_data_directly(mission_data)
        
        assert len(insights) > 0
        assert insights[0].insight_type == InsightType.MISSION_COORDINATION

    def test_analyze_agent_performance_directly(self, analyzer, sample_agent_data):
        """Test direct agent performance analysis fallback."""
        insights = analyzer._analyze_agent_performance_directly(sample_agent_data, time_window_hours=24)
        
        assert len(insights) > 0
        assert insights[0].insight_type == InsightType.PERFORMANCE


