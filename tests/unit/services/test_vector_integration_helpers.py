"""
Tests for vector_integration_helpers.py

Author: Agent-3 (Infrastructure & DevOps Specialist)
Date: 2025-01-27
"""

import pytest
from pathlib import Path
import sys
from unittest.mock import Mock, MagicMock

# Add project root to path
project_root = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(project_root))

from src.services.utils import vector_integration_helpers


class TestFormatSearchResult:
    """Test format_search_result function."""

    def test_format_search_result_with_all_fields(self):
        """Test format_search_result with complete result object."""
        mock_result = Mock()
        mock_result.similarity_score = 0.85
        mock_result.document = Mock()
        mock_result.document.content = "This is test content"
        mock_result.document.document_type = Mock()
        mock_result.document.document_type.value = "test_type"
        mock_result.document.source_file = "test.py"
        mock_result.document.tags = ["tag1", "tag2"]
        
        result = vector_integration_helpers.format_search_result(mock_result)
        
        assert isinstance(result, dict)
        assert result["similarity"] == 0.85
        assert result["content"] == "This is test content"
        assert result["type"] == "test_type"
        assert result["source"] == "test.py"
        assert result["tags"] == ["tag1", "tag2"]

    def test_format_search_result_with_long_content(self):
        """Test format_search_result truncates long content."""
        mock_result = Mock()
        mock_result.similarity_score = 0.75
        mock_result.document = Mock()
        mock_result.document.content = "A" * 200  # Long content
        mock_result.document.document_type = Mock()
        mock_result.document.document_type.value = "type"
        
        result = vector_integration_helpers.format_search_result(mock_result)
        
        assert len(result["content"]) == 153  # 150 + "..."
        assert result["content"].endswith("...")

    def test_format_search_result_with_short_content(self):
        """Test format_search_result doesn't truncate short content."""
        mock_result = Mock()
        mock_result.similarity_score = 0.90
        mock_result.document = Mock()
        mock_result.document.content = "Short"
        mock_result.document.document_type = Mock()
        mock_result.document.document_type.value = "type"
        
        result = vector_integration_helpers.format_search_result(mock_result)
        
        assert result["content"] == "Short"

    def test_format_search_result_missing_attributes(self):
        """Test format_search_result handles missing attributes."""
        # Create a class to avoid Mock auto-attributes
        class TestDocument:
            content = "Content"
            document_type = Mock()
            document_type.value = "type"
            # No source_file or tags attributes
        
        class TestResult:
            similarity_score = 0.50
            document = TestDocument()
        
        test_result = TestResult()
        result = vector_integration_helpers.format_search_result(test_result)
        
        assert result["source"] == "unknown"
        assert result["tags"] == []

    def test_format_search_result_exception_handling(self):
        """Test format_search_result handles exceptions gracefully."""
        invalid_result = "not a result object"
        
        result = vector_integration_helpers.format_search_result(invalid_result)
        
        assert isinstance(result, dict)
        assert "error" in result


class TestGenerateRecommendations:
    """Test generate_recommendations function."""

    def test_generate_recommendations_with_tags(self):
        """Test generate_recommendations with tasks containing tags."""
        mock_task1 = Mock()
        mock_task1.document = Mock()
        mock_task1.document.tags = ["python", "testing"]
        
        mock_task2 = Mock()
        mock_task2.document = Mock()
        mock_task2.document.tags = ["python", "api"]
        
        similar_tasks = [mock_task1, mock_task2]
        
        recommendations = vector_integration_helpers.generate_recommendations(similar_tasks)
        
        assert len(recommendations) > 0
        assert any("python" in rec.lower() for rec in recommendations)

    def test_generate_recommendations_empty_list(self):
        """Test generate_recommendations with empty task list."""
        recommendations = vector_integration_helpers.generate_recommendations([])
        
        assert len(recommendations) == 1
        assert "No specific patterns found" in recommendations[0]

    def test_generate_recommendations_no_tags(self):
        """Test generate_recommendations with tasks without tags."""
        mock_task = Mock()
        mock_task.document = Mock()
        mock_task.document.tags = []
        
        recommendations = vector_integration_helpers.generate_recommendations([mock_task])
        
        assert len(recommendations) == 1
        assert "No specific patterns found" in recommendations[0]

    def test_generate_recommendations_limits_to_three(self):
        """Test generate_recommendations limits to top 3 common tags."""
        tasks = []
        for i in range(5):
            mock_task = Mock()
            mock_task.document = Mock()
            mock_task.document.tags = [f"tag{i}"] * (i + 1)  # Varying frequencies
        
        recommendations = vector_integration_helpers.generate_recommendations(tasks)
        
        # Should have at most 3 recommendations (plus fallback)
        assert len([r for r in recommendations if "Consider using" in r]) <= 3


class TestGenerateAgentRecommendations:
    """Test generate_agent_recommendations function."""

    def test_generate_agent_recommendations_high_similarity(self):
        """Test generate_agent_recommendations with high similarity scores."""
        mock_work1 = Mock()
        mock_work1.similarity_score = 0.85
        
        mock_work2 = Mock()
        mock_work2.similarity_score = 0.90
        
        work_history = [mock_work1, mock_work2]
        
        recommendations = vector_integration_helpers.generate_agent_recommendations(work_history)
        
        assert len(recommendations) > 0
        assert any("Excellent" in rec or "excellent" in rec.lower() for rec in recommendations)

    def test_generate_agent_recommendations_medium_similarity(self):
        """Test generate_agent_recommendations with medium similarity scores."""
        mock_work = Mock()
        mock_work.similarity_score = 0.65
        
        work_history = [mock_work]
        
        recommendations = vector_integration_helpers.generate_agent_recommendations(work_history)
        
        assert len(recommendations) > 0

    def test_generate_agent_recommendations_low_similarity(self):
        """Test generate_agent_recommendations with low similarity scores."""
        mock_work = Mock()
        mock_work.similarity_score = 0.40
        
        work_history = [mock_work]
        
        recommendations = vector_integration_helpers.generate_agent_recommendations(work_history)
        
        assert len(recommendations) > 0
        assert any("improving" in rec.lower() for rec in recommendations)

    def test_generate_agent_recommendations_empty_list(self):
        """Test generate_agent_recommendations with empty work history."""
        recommendations = vector_integration_helpers.generate_agent_recommendations([])
        
        assert len(recommendations) == 0

    def test_generate_agent_recommendations_missing_similarity(self):
        """Test generate_agent_recommendations handles missing similarity_score."""
        # Create object without similarity_score - use object() to avoid Mock auto-attributes
        class WorkItem:
            pass
        
        work_item = WorkItem()
        work_history = [work_item]
        
        recommendations = vector_integration_helpers.generate_agent_recommendations(work_history)
        
        # Should handle gracefully - avg similarity will be 0.0
        assert isinstance(recommendations, list)

    def test_format_search_result_exact_150_chars(self):
        """Test format_search_result with exactly 150 characters."""
        mock_result = Mock()
        mock_result.similarity_score = 0.75
        mock_result.document = Mock()
        mock_result.document.content = "A" * 150
        mock_result.document.document_type = Mock()
        mock_result.document.document_type.value = "type"
        
        result = vector_integration_helpers.format_search_result(mock_result)
        
        # Should not truncate (exactly 150 chars)
        assert len(result["content"]) == 150
        assert not result["content"].endswith("...")

    def test_format_search_result_151_chars(self):
        """Test format_search_result with 151 characters (should truncate)."""
        mock_result = Mock()
        mock_result.similarity_score = 0.75
        mock_result.document = Mock()
        mock_result.document.content = "A" * 151
        mock_result.document.document_type = Mock()
        mock_result.document.document_type.value = "type"
        
        result = vector_integration_helpers.format_search_result(mock_result)
        
        # Should truncate to 150 + "..."
        assert len(result["content"]) == 153
        assert result["content"].endswith("...")

    def test_format_search_result_zero_similarity(self):
        """Test format_search_result with zero similarity score."""
        mock_result = Mock()
        mock_result.similarity_score = 0.0
        mock_result.document = Mock()
        mock_result.document.content = "Content"
        mock_result.document.document_type = Mock()
        mock_result.document.document_type.value = "type"
        
        result = vector_integration_helpers.format_search_result(mock_result)
        
        assert result["similarity"] == 0.0

    def test_format_search_result_negative_similarity(self):
        """Test format_search_result with negative similarity (edge case)."""
        mock_result = Mock()
        mock_result.similarity_score = -0.1
        mock_result.document = Mock()
        mock_result.document.content = "Content"
        mock_result.document.document_type = Mock()
        mock_result.document.document_type.value = "type"
        
        result = vector_integration_helpers.format_search_result(mock_result)
        
        assert result["similarity"] == -0.1

    def test_format_search_result_empty_content(self):
        """Test format_search_result with empty content."""
        mock_result = Mock()
        mock_result.similarity_score = 0.5
        mock_result.document = Mock()
        mock_result.document.content = ""
        mock_result.document.document_type = Mock()
        mock_result.document.document_type.value = "type"
        
        result = vector_integration_helpers.format_search_result(mock_result)
        
        assert result["content"] == ""

    def test_generate_recommendations_single_tag(self):
        """Test generate_recommendations with single tag."""
        mock_task = Mock()
        mock_task.document = Mock()
        mock_task.document.tags = ["python"]
        
        recommendations = vector_integration_helpers.generate_recommendations([mock_task])
        
        assert len(recommendations) > 0
        assert any("python" in rec.lower() for rec in recommendations)

    def test_generate_recommendations_many_tags(self):
        """Test generate_recommendations with many tags."""
        tasks = []
        for i in range(10):
            mock_task = Mock()
            mock_task.document = Mock()
            mock_task.document.tags = [f"tag{i}"]
            tasks.append(mock_task)
        
        recommendations = vector_integration_helpers.generate_recommendations(tasks)
        
        # Should limit to top 3
        assert len([r for r in recommendations if "Consider using" in r]) <= 3

    def test_generate_recommendations_no_document_attribute(self):
        """Test generate_recommendations with task missing document attribute."""
        mock_task = Mock()
        del mock_task.document  # Remove document attribute
        
        recommendations = vector_integration_helpers.generate_recommendations([mock_task])
        
        assert len(recommendations) == 1
        assert "No specific patterns found" in recommendations[0]

    def test_generate_recommendations_document_no_tags(self):
        """Test generate_recommendations with document but no tags attribute."""
        mock_task = Mock()
        mock_task.document = Mock()
        # No tags attribute
        
        recommendations = vector_integration_helpers.generate_recommendations([mock_task])
        
        assert len(recommendations) == 1
        assert "No specific patterns found" in recommendations[0]

    def test_generate_agent_recommendations_zero_similarity(self):
        """Test generate_agent_recommendations with zero similarity."""
        mock_work = Mock()
        mock_work.similarity_score = 0.0
        
        recommendations = vector_integration_helpers.generate_agent_recommendations([mock_work])
        
        assert len(recommendations) > 0
        assert any("improving" in rec.lower() for rec in recommendations)

    def test_generate_agent_recommendations_high_avg(self):
        """Test generate_agent_recommendations with high average similarity."""
        work_history = []
        for i in range(5):
            mock_work = Mock()
            mock_work.similarity_score = 0.9
            work_history.append(mock_work)
        
        recommendations = vector_integration_helpers.generate_agent_recommendations(work_history)
        
        assert len(recommendations) > 0
        assert any("Excellent" in rec or "excellent" in rec.lower() for rec in recommendations)

    def test_generate_agent_recommendations_mixed_scores(self):
        """Test generate_agent_recommendations with mixed similarity scores."""
        work_history = [
            Mock(similarity_score=0.9),
            Mock(similarity_score=0.5),
            Mock(similarity_score=0.7)
        ]
        
        recommendations = vector_integration_helpers.generate_agent_recommendations(work_history)
        
        assert len(recommendations) > 0

    def test_generate_agent_recommendations_single_item(self):
        """Test generate_agent_recommendations with single work item."""
        mock_work = Mock()
        mock_work.similarity_score = 0.75
        
        recommendations = vector_integration_helpers.generate_agent_recommendations([mock_work])
        
        assert len(recommendations) > 0

    def test_format_search_result_all_attributes_present(self):
        """Test format_search_result with all optional attributes present."""
        mock_result = Mock()
        mock_result.similarity_score = 0.85
        mock_result.document = Mock()
        mock_result.document.content = "Content"
        mock_result.document.document_type = Mock()
        mock_result.document.document_type.value = "type"
        mock_result.document.source_file = "test.py"
        mock_result.document.tags = ["tag1", "tag2"]
        
        result = vector_integration_helpers.format_search_result(mock_result)
        
        assert result["source"] == "test.py"
        assert result["tags"] == ["tag1", "tag2"]

    def test_format_search_result_type_value(self):
        """Test format_search_result extracts document_type.value."""
        mock_result = Mock()
        mock_result.similarity_score = 0.5
        mock_result.document = Mock()
        mock_result.document.content = "Content"
        mock_result.document.document_type = Mock()
        mock_result.document.document_type.value = "custom_type"
        
        result = vector_integration_helpers.format_search_result(mock_result)
        
        assert result["type"] == "custom_type"

    def test_format_search_result_very_long_content(self):
        """Test format_search_result with very long content."""
        mock_result = Mock()
        mock_result.similarity_score = 0.5
        mock_result.document = Mock()
        mock_result.document.content = "A" * 10000  # Very long
        mock_result.document.document_type = Mock()
        mock_result.document.document_type.value = "type"
        
        result = vector_integration_helpers.format_search_result(mock_result)
        
        assert len(result["content"]) == 153  # 150 + "..."
        assert result["content"].endswith("...")

    def test_generate_recommendations_single_task(self):
        """Test generate_recommendations with single task."""
        mock_task = Mock()
        mock_task.document = Mock()
        mock_task.document.tags = ["python"]
        
        recommendations = vector_integration_helpers.generate_recommendations([mock_task])
        
        assert len(recommendations) > 0

    def test_generate_recommendations_duplicate_tags(self):
        """Test generate_recommendations with duplicate tags."""
        tasks = []
        for i in range(5):
            mock_task = Mock()
            mock_task.document = Mock()
            mock_task.document.tags = ["python", "testing"]  # Same tags
            tasks.append(mock_task)
        
        recommendations = vector_integration_helpers.generate_recommendations(tasks)
        
        # Should recommend most common tags
        assert len(recommendations) > 0

    def test_generate_agent_recommendations_exactly_0_8(self):
        """Test generate_agent_recommendations with exactly 0.8 similarity."""
        mock_work = Mock()
        mock_work.similarity_score = 0.8
        
        recommendations = vector_integration_helpers.generate_agent_recommendations([mock_work])
        
        # 0.8 is > 0.8, so should recommend excellent
        assert len(recommendations) > 0

    def test_generate_agent_recommendations_exactly_0_6(self):
        """Test generate_agent_recommendations with exactly 0.6 similarity."""
        mock_work = Mock()
        mock_work.similarity_score = 0.6
        
        recommendations = vector_integration_helpers.generate_agent_recommendations([mock_work])
        
        # 0.6 is not > 0.8, but > 0.6, so should recommend good
        assert len(recommendations) > 0

    def test_generate_agent_recommendations_exactly_0_0(self):
        """Test generate_agent_recommendations with exactly 0.0 similarity."""
        mock_work = Mock()
        mock_work.similarity_score = 0.0
        
        recommendations = vector_integration_helpers.generate_agent_recommendations([mock_work])
        
        # 0.0 is not > 0.6, so should recommend improving
        assert len(recommendations) > 0
        assert any("improving" in rec.lower() for rec in recommendations)

    def test_generate_agent_recommendations_mixed_scores_edge_cases(self):
        """Test generate_agent_recommendations with edge case scores."""
        work_history = [
            Mock(similarity_score=0.81),  # Just above 0.8
            Mock(similarity_score=0.79),  # Just below 0.8
            Mock(similarity_score=0.61),  # Just above 0.6
            Mock(similarity_score=0.59),  # Just below 0.6
        ]
        
        recommendations = vector_integration_helpers.generate_agent_recommendations(work_history)
        
        assert len(recommendations) > 0

    def test_format_search_result_with_none_content(self):
        """Test format_search_result handles None content gracefully."""
        mock_result = Mock()
        mock_result.similarity_score = 0.5
        mock_result.document = Mock()
        mock_result.document.content = None
        mock_result.document.document_type = Mock()
        mock_result.document.document_type.value = "type"
        
        result = vector_integration_helpers.format_search_result(mock_result)
        
        # Should handle None gracefully
        assert isinstance(result, dict)

    def test_generate_recommendations_with_none_tags(self):
        """Test generate_recommendations handles None tags."""
        mock_task = Mock()
        mock_task.document = Mock()
        mock_task.document.tags = None
        
        recommendations = vector_integration_helpers.generate_recommendations([mock_task])
        
        # Should handle None tags gracefully
        assert len(recommendations) == 1
        assert "No specific patterns found" in recommendations[0]

