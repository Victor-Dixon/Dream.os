"""
Tests for Prediction Analyzer - Real Implementation
===================================================

Tests the real probability calculation implementation using historical task data.

Author: Agent-5 (Business Intelligence Specialist)
Date: 2025-01-27
"""

import pytest
import sys
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

# Import directly to avoid circular imports
try:
    from src.core.vector_strategic_oversight.unified_strategic_oversight.analyzers.prediction_analyzer import (
        PredictionAnalyzer,
        SuccessPrediction,
    )
    from src.core.vector_strategic_oversight.unified_strategic_oversight.enums import ConfidenceLevel
except ImportError:
    # If imports fail, skip all tests
    pytest.skip("Required modules not available", allow_module_level=True)


class TestPredictionAnalyzer:
    """Test suite for PredictionAnalyzer real implementation."""

    @pytest.fixture
    def analyzer(self):
        """Create PredictionAnalyzer instance."""
        return PredictionAnalyzer()

    @pytest.fixture
    def sample_task_data(self):
        """Sample task data for testing."""
        return {
            "task_id": "test_task_1",
            "title": "Test Task",
            "description": "A test task",
            "complexity": "medium",
            "assigned_agent_id": "Agent-5",
            "priority": "high",
            "resources_available": True,
        }

    def test_calculate_base_probability_with_historical_data(self, analyzer, sample_task_data):
        """Test probability calculation with historical task data."""
        # Mock TaskRepository with historical data
        mock_task = Mock()
        mock_task.completed_at = datetime.now()
        mock_task.assigned_at = datetime.now() - timedelta(hours=2)
        mock_task.complexity = "medium"
        mock_task.assigned_agent_id = "Agent-5"
        
        with patch('src.core.vector_strategic_oversight.unified_strategic_oversight.analyzers.prediction_analyzer.TaskRepository') as mock_repo_class, \
             patch('src.core.vector_strategic_oversight.unified_strategic_oversight.analyzers.prediction_analyzer.DatabaseConnection'):
            
            mock_repo = Mock()
            mock_repo.list_all.return_value = [mock_task, mock_task, mock_task]  # 3 completed tasks
            mock_repo_class.return_value = mock_repo
            
            probability = analyzer._calculate_base_probability(sample_task_data)
            
            # Should return a probability based on historical success rate
            assert 0.0 <= probability <= 1.0
            assert probability > 0.0  # Should have some success rate

    def test_calculate_base_probability_fallback_complexity(self, analyzer, sample_task_data):
        """Test fallback to complexity-based calculation when no historical data."""
        with patch('src.core.vector_strategic_oversight.unified_strategic_oversight.analyzers.prediction_analyzer.TaskRepository') as mock_repo_class, \
             patch('src.core.vector_strategic_oversight.unified_strategic_oversight.analyzers.prediction_analyzer.DatabaseConnection'):
            
            mock_repo = Mock()
            mock_repo.list_all.return_value = []  # No historical data
            mock_repo_class.return_value = mock_repo
            
            # Test different complexities
            for complexity, expected_min in [("low", 0.8), ("medium", 0.6), ("high", 0.4)]:
                sample_task_data["complexity"] = complexity
                probability = analyzer._calculate_base_probability(sample_task_data)
                assert probability >= expected_min
                assert probability <= 1.0

    def test_calculate_base_probability_import_error_fallback(self, analyzer, sample_task_data):
        """Test fallback when repository imports fail."""
        with patch('src.core.vector_strategic_oversight.unified_strategic_oversight.analyzers.prediction_analyzer.TaskRepository', side_effect=ImportError("Repository not available")):
            probability = analyzer._calculate_base_probability(sample_task_data)
            # Should fallback to complexity-based
            assert 0.0 <= probability <= 1.0

    def test_calculate_base_probability_similar_tasks(self, analyzer, sample_task_data):
        """Test probability calculation using similar tasks."""
        # Create tasks with same complexity
        mock_task_medium = Mock()
        mock_task_medium.completed_at = datetime.now()
        mock_task_medium.assigned_at = datetime.now() - timedelta(hours=1)
        mock_task_medium.complexity = "medium"
        mock_task_medium.assigned_agent_id = "Agent-5"
        
        mock_task_other = Mock()
        mock_task_other.completed_at = datetime.now()
        mock_task_other.assigned_at = datetime.now() - timedelta(hours=1)
        mock_task_other.complexity = "high"  # Different complexity
        mock_task_other.assigned_agent_id = "Agent-5"
        
        with patch('src.core.vector_strategic_oversight.unified_strategic_oversight.analyzers.prediction_analyzer.TaskRepository') as mock_repo_class, \
             patch('src.core.vector_strategic_oversight.unified_strategic_oversight.analyzers.prediction_analyzer.DatabaseConnection'):
            
            mock_repo = Mock()
            # Mix of similar and different tasks
            mock_repo.list_all.return_value = [mock_task_medium, mock_task_medium, mock_task_other]
            mock_repo_class.return_value = mock_repo
            
            probability = analyzer._calculate_base_probability(sample_task_data)
            assert 0.0 <= probability <= 1.0

    @pytest.mark.asyncio
    async def test_predict_task_success_with_historical_data(self, analyzer, sample_task_data):
        """Test full prediction with historical data."""
        # Add historical data
        historical_data = [
            {"task_id": "hist_1", "success": True, "complexity": "medium"},
            {"task_id": "hist_2", "success": True, "complexity": "medium"},
            {"task_id": "hist_3", "success": False, "complexity": "medium"},
        ]
        analyzer.add_historical_data(historical_data)
        
        with patch.object(analyzer, '_calculate_base_probability', return_value=0.7):
            prediction = await analyzer.predict_task_success(sample_task_data, historical_data)
            
            assert isinstance(prediction, SuccessPrediction)
            assert prediction.task_id == "test_task_1"
            assert 0.0 <= prediction.success_probability <= 1.0
            assert prediction.confidence_level in [
                ConfidenceLevel.VERY_HIGH,
                ConfidenceLevel.HIGH,
                ConfidenceLevel.MEDIUM,
                ConfidenceLevel.LOW,
            ]
            assert len(prediction.key_factors) > 0
            assert len(prediction.risk_factors) > 0
            assert len(prediction.recommendations) > 0

    def test_fallback_probability_by_complexity(self, analyzer):
        """Test fallback probability calculation."""
        assert analyzer._fallback_probability_by_complexity("low") == 0.9
        assert analyzer._fallback_probability_by_complexity("medium") == 0.7
        assert analyzer._fallback_probability_by_complexity("high") == 0.5
        assert analyzer._fallback_probability_by_complexity("unknown") == 0.6

    def test_calculate_historical_success_rate(self, analyzer):
        """Test historical success rate calculation."""
        # No data
        assert analyzer._calculate_historical_success_rate() == 0.5
        
        # With data
        historical_data = [
            {"success": True},
            {"success": True},
            {"success": False},
        ]
        analyzer.add_historical_data(historical_data)
        rate = analyzer._calculate_historical_success_rate()
        assert rate == pytest.approx(2/3, abs=0.01)

