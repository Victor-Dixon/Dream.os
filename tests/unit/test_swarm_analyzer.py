#!/usr/bin/env python3
"""
Unit Tests for Swarm Analyzer
=============================

Comprehensive tests for swarm_analyzer.py targeting ≥85% coverage.

Author: Agent-5 (Business Intelligence Specialist)
Date: 2025-01-28
"""

import pytest
from datetime import datetime
from src.core.vector_strategic_oversight.unified_strategic_oversight.analyzers.swarm_analyzer import (
    SwarmCoordinationAnalyzer
)
from src.core.vector_strategic_oversight.unified_strategic_oversight.enums import (
    ConfidenceLevel,
    ImpactLevel,
    InsightType
)
# Note: swarm_analyzer imports from ..data_models, but actual model is in ..models
# We'll use models directly for testing
try:
    from src.core.vector_strategic_oversight.unified_strategic_oversight.models import (
        SwarmCoordinationInsight
    )
except ImportError:
    # Fallback if import path differs
    from src.core.vector_strategic_oversight.unified_strategic_oversight.analyzers.swarm_analyzer import (
        SwarmCoordinationInsight
    )


class TestSwarmCoordinationAnalyzer:
    """Tests for SwarmCoordinationAnalyzer."""

    @pytest.fixture
    def analyzer(self):
        """Create analyzer instance."""
        return SwarmCoordinationAnalyzer()

    @pytest.fixture
    def sample_agent_data(self):
        """Sample agent data for testing."""
        return [
            {"agent_id": "Agent-1", "status": "ACTIVE_AGENT_MODE"},
            {"agent_id": "Agent-2", "status": "ACTIVE_AGENT_MODE"},
            {"agent_id": "Agent-3", "status": "ACTIVE_AGENT_MODE"},
        ]

    @pytest.fixture
    def sample_mission_data(self):
        """Sample mission data for testing."""
        return [
            {"mission_id": "M001", "status": "completed", "assigned_agent_id": "Agent-1"},
            {"mission_id": "M002", "status": "in_progress", "assigned_agent_id": "Agent-2"},
        ]

    @pytest.mark.asyncio
    async def test_initialization(self, analyzer):
        """Test analyzer initialization."""
        assert analyzer.analysis_history == []

    @pytest.mark.asyncio
    async def test_analyze_swarm_coordination(self, analyzer, sample_agent_data, sample_mission_data):
        """Test analyze_swarm_coordination method."""
        insights = await analyzer.analyze_swarm_coordination(
            sample_agent_data,
            sample_mission_data,
            time_window_hours=24
        )
        assert isinstance(insights, list)
        # Should store analysis history
        assert len(analyzer.analysis_history) > 0

    @pytest.mark.asyncio
    async def test_analyze_swarm_coordination_empty_data(self, analyzer):
        """Test with empty data."""
        insights = await analyzer.analyze_swarm_coordination([], [], 24)
        assert isinstance(insights, list)

    @pytest.mark.asyncio
    async def test_analyze_swarm_coordination_exception_handling(self, analyzer):
        """Test exception handling."""
        # Should handle exceptions gracefully
        insights = await analyzer.analyze_swarm_coordination(None, None, 24)
        assert isinstance(insights, list)

    @pytest.mark.asyncio
    async def test_analyze_collaboration_patterns(self, analyzer, sample_agent_data):
        """Test _analyze_collaboration_patterns method."""
        insights = await analyzer._analyze_collaboration_patterns(sample_agent_data)
        assert isinstance(insights, list)

    @pytest.mark.asyncio
    async def test_analyze_collaboration_patterns_empty(self, analyzer):
        """Test collaboration patterns with empty data."""
        insights = await analyzer._analyze_collaboration_patterns([])
        assert isinstance(insights, list)

    @pytest.mark.asyncio
    async def test_analyze_collaboration_patterns_insufficient_data(self, analyzer):
        """Test with insufficient agent data."""
        insights = await analyzer._analyze_collaboration_patterns([{"agent_id": "Agent-1"}])
        assert isinstance(insights, list)

    @pytest.mark.asyncio
    async def test_analyze_mission_coordination(self, analyzer, sample_mission_data):
        """Test _analyze_mission_coordination method."""
        insights = await analyzer._analyze_mission_coordination(sample_mission_data)
        assert isinstance(insights, list)

    @pytest.mark.asyncio
    async def test_analyze_mission_coordination_empty(self, analyzer):
        """Test mission coordination with empty data."""
        insights = await analyzer._analyze_mission_coordination([])
        assert isinstance(insights, list)

    def test_analyze_mission_data_directly(self, analyzer):
        """Test _analyze_mission_data_directly fallback method."""
        mission_data = [
            {"status": "completed"},
            {"status": "in_progress"},
        ]
        insights = analyzer._analyze_mission_data_directly(mission_data)
        assert isinstance(insights, list)
        assert len(insights) > 0

    def test_analyze_mission_data_directly_empty(self, analyzer):
        """Test mission data directly with empty data."""
        insights = analyzer._analyze_mission_data_directly([])
        assert isinstance(insights, list)

    @pytest.mark.asyncio
    async def test_analyze_performance_trends(self, analyzer, sample_agent_data):
        """Test _analyze_performance_trends method."""
        insights = await analyzer._analyze_performance_trends(sample_agent_data, 24)
        assert isinstance(insights, list)

    @pytest.mark.asyncio
    async def test_analyze_performance_trends_insufficient_data(self, analyzer):
        """Test performance trends with insufficient data."""
        insights = await analyzer._analyze_performance_trends([{"agent_id": "Agent-1"}], 24)
        assert isinstance(insights, list)

    def test_analyze_agent_performance_directly(self, analyzer, sample_agent_data):
        """Test _analyze_agent_performance_directly fallback method."""
        insights = analyzer._analyze_agent_performance_directly(sample_agent_data, 24)
        assert isinstance(insights, list)
        assert len(insights) > 0

    def test_analyze_agent_performance_directly_empty(self, analyzer):
        """Test agent performance directly with empty data."""
        insights = analyzer._analyze_agent_performance_directly([], 24)
        assert isinstance(insights, list)

    def test_analyze_agent_performance_directly_with_status(self, analyzer):
        """Test agent performance with status data."""
        agent_data = [
            {"agent_id": "Agent-1", "status": "ACTIVE_AGENT_MODE"},
            {"agent_id": "Agent-2", "status": "IDLE"},
        ]
        insights = analyzer._analyze_agent_performance_directly(agent_data, 24)
        assert len(insights) > 0
        insight = insights[0]
        assert isinstance(insight, SwarmCoordinationInsight)
        assert insight.insight_type == InsightType.PERFORMANCE


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=src.core.vector_strategic_oversight.unified_strategic_oversight.analyzers.swarm_analyzer", "--cov-report=term-missing"])

