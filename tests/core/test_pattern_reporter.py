"""
Unit tests for pattern_analysis/pattern_reporter.py - HIGH PRIORITY

Tests PatternReporter class functionality.
Note: Maps to pattern_analysis_orchestrator.py PatternAnalysisSystem reporting methods.
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

# Import the pattern analysis system (has reporting functionality)
from src.core.pattern_analysis.pattern_analysis_orchestrator import PatternAnalysisSystem
from src.core.pattern_analysis.pattern_analysis_models import (
    PatternAnalysisConfig,
    MissionContext,
    MissionPattern,
    PatternType
)

# Alias for test purposes
PatternReporter = PatternAnalysisSystem


class TestPatternReporter:
    """Test suite for PatternReporter class."""

    @pytest.fixture
    def reporter(self):
        """Create a PatternReporter instance."""
        return PatternReporter()

    @pytest.fixture
    def mock_engine(self):
        """Create a mock engine."""
        engine = MagicMock()
        engine.mission_patterns = {}
        engine.analyze_mission_patterns = Mock(return_value=MagicMock(recommendations=[]))
        engine.add_pattern = Mock(return_value=True)
        engine.get_pattern = Mock(return_value=None)
        engine.get_metrics = Mock(return_value=MagicMock())
        engine.clear_old_patterns = Mock(return_value=0)
        return engine

    def test_initialization(self, reporter):
        """Test PatternReporter initialization."""
        assert reporter.config is not None
        assert reporter.engine is not None

    def test_get_pattern_summary_empty(self, reporter, mock_engine):
        """Test get_pattern_summary with no patterns."""
        reporter.engine = mock_engine
        mock_engine.mission_patterns = {}
        
        summary = reporter.get_pattern_summary()
        
        assert "message" in summary
        assert summary["message"] == "No patterns available"

    def test_get_pattern_summary_with_patterns(self, reporter, mock_engine):
        """Test get_pattern_summary with patterns."""
        reporter.engine = mock_engine
        
        # Create mock patterns
        pattern1 = MagicMock()
        pattern1.pattern_type = PatternType.SUCCESS
        pattern1.success_rate = 0.9
        pattern1.usage_count = 5
        
        pattern2 = MagicMock()
        pattern2.pattern_type = PatternType.FAILURE
        pattern2.success_rate = 0.3
        pattern2.usage_count = 2
        
        mock_engine.mission_patterns = {"p1": pattern1, "p2": pattern2}
        
        summary = reporter.get_pattern_summary()
        
        assert "total_patterns" in summary
        assert summary["total_patterns"] == 2

    def test_generate_strategic_insights(self, reporter, mock_engine):
        """Test generate_strategic_insights method."""
        reporter.engine = mock_engine
        
        insights = reporter.generate_strategic_insights(MagicMock())
        
        assert isinstance(insights, list)

    def test_get_pattern_summary_average_success_rate(self, reporter, mock_engine):
        """Test get_pattern_summary calculates average success rate."""
        reporter.engine = mock_engine
        
        pattern1 = MagicMock()
        pattern1.pattern_type = PatternType.SUCCESS
        pattern1.success_rate = 0.8
        pattern1.usage_count = 1
        
        pattern2 = MagicMock()
        pattern2.pattern_type = PatternType.SUCCESS
        pattern2.success_rate = 0.6
        pattern2.usage_count = 1
        
        mock_engine.mission_patterns = {"p1": pattern1, "p2": pattern2}
        
        summary = reporter.get_pattern_summary()
        
        assert "average_success_rate" in summary
        assert summary["average_success_rate"] == 0.7

    def test_get_pattern_summary_high_success_patterns(self, reporter, mock_engine):
        """Test get_pattern_summary counts high success patterns."""
        reporter.engine = mock_engine
        
        pattern1 = MagicMock()
        pattern1.pattern_type = PatternType.SUCCESS
        pattern1.success_rate = 0.9
        pattern1.usage_count = 1
        
        pattern2 = MagicMock()
        pattern2.pattern_type = PatternType.SUCCESS
        pattern2.success_rate = 0.5
        pattern2.usage_count = 1
        
        mock_engine.mission_patterns = {"p1": pattern1, "p2": pattern2}
        
        summary = reporter.get_pattern_summary()
        
        assert summary["high_success_patterns"] == 1

    def test_get_pattern_summary_pattern_types(self, reporter, mock_engine):
        """Test get_pattern_summary groups by pattern types."""
        reporter.engine = mock_engine
        
        pattern1 = MagicMock()
        pattern1.pattern_type = PatternType.SUCCESS
        
        pattern2 = MagicMock()
        pattern2.pattern_type = PatternType.SUCCESS
        
        pattern3 = MagicMock()
        pattern3.pattern_type = PatternType.FAILURE
        
        mock_engine.mission_patterns = {"p1": pattern1, "p2": pattern2, "p3": pattern3}
        
        summary = reporter.get_pattern_summary()
        
        assert "pattern_types" in summary
        assert PatternType.SUCCESS in summary["pattern_types"] or "success" in str(summary["pattern_types"])

    def test_analyze_success_patterns(self, reporter, mock_engine):
        """Test analyze_success_patterns method."""
        reporter.engine = mock_engine
        
        pattern1 = MagicMock()
        pattern1.success_rate = 0.9
        pattern1.usage_count = 1
        
        pattern2 = MagicMock()
        pattern2.success_rate = 0.5
        pattern2.usage_count = 1
        
        mock_engine.mission_patterns = {"p1": pattern1, "p2": pattern2}
        
        result = reporter.analyze_success_patterns(MagicMock())
        
        assert result is not None

    def test_analyze_risk_patterns(self, reporter, mock_engine):
        """Test analyze_risk_patterns method."""
        reporter.engine = mock_engine
        
        pattern1 = MagicMock()
        pattern1.risk_factors = ["risk1", "risk2", "risk3"]
        
        pattern2 = MagicMock()
        pattern2.risk_factors = ["risk1"]
        
        mock_engine.mission_patterns = {"p1": pattern1, "p2": pattern2}
        
        result = reporter.analyze_risk_patterns(MagicMock())
        
        assert result is not None

    def test_get_pattern_summary_recent_patterns(self, reporter, mock_engine):
        """Test get_pattern_summary counts recent patterns."""
        reporter.engine = mock_engine
        
        pattern1 = MagicMock()
        pattern1.usage_count = 5
        
        pattern2 = MagicMock()
        pattern2.usage_count = 0
        
        mock_engine.mission_patterns = {"p1": pattern1, "p2": pattern2}
        
        summary = reporter.get_pattern_summary()
        
        assert "recent_patterns" in summary
        assert summary["recent_patterns"] >= 1

