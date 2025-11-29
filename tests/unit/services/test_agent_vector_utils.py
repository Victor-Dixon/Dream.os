"""
Tests for agent_vector_utils.py

Author: Agent-3 (Infrastructure & DevOps Specialist)
Date: 2025-01-27
"""

import pytest
from unittest.mock import Mock
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(project_root))

from src.services.agent_vector_utils import format_search_result, generate_recommendations


class TestFormatSearchResult:
    """Test format_search_result function."""

    def test_format_with_document_and_score(self):
        """Test formatting result with document and similarity_score."""
        result = Mock()
        result.document = Mock()
        result.document.content = "This is a test document content"
        result.similarity_score = 0.95
        
        output = format_search_result(result)
        
        assert "Score: 0.950" in output
        assert "This is a test document content" in output

    def test_format_with_long_content(self):
        """Test formatting result with content longer than 200 chars."""
        result = Mock()
        result.document = Mock()
        result.document.content = "A" * 250
        result.similarity_score = 0.85
        
        output = format_search_result(result)
        
        assert len(output) < 250  # Should be truncated
        assert "..." in output
        assert "Score: 0.850" in output

    def test_format_with_short_content(self):
        """Test formatting result with content shorter than 200 chars."""
        result = Mock()
        result.document = Mock()
        result.document.content = "Short content"
        result.similarity_score = 0.75
        
        output = format_search_result(result)
        
        assert "Short content" in output
        assert "..." not in output
        assert "Score: 0.750" in output

    def test_format_without_document_attr(self):
        """Test formatting result without document attribute."""
        result = Mock()
        result.similarity_score = 0.90
        del result.document
        
        output = format_search_result(result)
        
        # Should fall back to str(result)
        assert output == str(result)

    def test_format_without_similarity_score(self):
        """Test formatting result without similarity_score attribute."""
        result = Mock()
        result.document = Mock()
        result.document.content = "Test content"
        del result.similarity_score
        
        output = format_search_result(result)
        
        # Should fall back to str(result)
        assert output == str(result)

    def test_format_with_exception(self):
        """Test formatting result that raises exception."""
        result = Mock()
        result.document = Mock()
        result.document.content = "Test"
        result.similarity_score = 0.90
        
        # Make accessing content raise exception
        type(result.document).content = property(lambda self: (_ for _ in ()).throw(Exception("Error")))
        
        output = format_search_result(result)
        
        # Should fall back to str(result) on exception
        assert output == str(result)

    def test_format_with_string_input(self):
        """Test formatting string input (fallback case)."""
        result = "simple string"
        
        output = format_search_result(result)
        
        assert output == "simple string"

    def test_format_with_none_input(self):
        """Test formatting None input (fallback case)."""
        result = None
        
        output = format_search_result(result)
        
        assert output == "None"


class TestGenerateRecommendations:
    """Test generate_recommendations function."""

    def test_generate_with_empty_results(self):
        """Test generating recommendations from empty results."""
        results = []
        
        recommendations = generate_recommendations(results)
        
        assert len(recommendations) == 1
        assert recommendations[0] == "No relevant information found"

    def test_generate_with_none_results(self):
        """Test generating recommendations from None input."""
        results = None
        
        # None is falsy, so it should be treated like empty list
        recommendations = generate_recommendations(results)
        
        assert len(recommendations) == 1
        assert recommendations[0] == "No relevant information found"

    def test_generate_with_single_result(self):
        """Test generating recommendations from single result."""
        result = Mock()
        result.document = Mock()
        result.document.content = "This is test content for recommendation"
        
        recommendations = generate_recommendations([result])
        
        assert len(recommendations) == 1
        assert "1. This is test content for recommendation" in recommendations[0]
        assert "..." in recommendations[0]

    def test_generate_with_multiple_results(self):
        """Test generating recommendations from multiple results."""
        results = []
        for i in range(3):
            result = Mock()
            result.document = Mock()
            result.document.content = f"Content {i+1}"
            results.append(result)
        
        recommendations = generate_recommendations(results)
        
        assert len(recommendations) == 3
        assert "1. Content 1" in recommendations[0]
        assert "2. Content 2" in recommendations[1]
        assert "3. Content 3" in recommendations[2]

    def test_generate_limits_to_five_results(self):
        """Test that recommendations are limited to top 5 results."""
        results = []
        for i in range(7):
            result = Mock()
            result.document = Mock()
            result.document.content = f"Content {i+1}"
            results.append(result)
        
        recommendations = generate_recommendations(results)
        
        assert len(recommendations) == 5
        assert "1. Content 1" in recommendations[0]
        assert "5. Content 5" in recommendations[4]

    def test_generate_with_long_content(self):
        """Test generating recommendations with long content (truncation)."""
        result = Mock()
        result.document = Mock()
        result.document.content = "A" * 150  # Longer than 100 chars
        
        recommendations = generate_recommendations([result])
        
        assert len(recommendations[0]) < 150  # Should be truncated
        assert "..." in recommendations[0]

    def test_generate_with_result_without_document(self):
        """Test generating recommendations from result without document."""
        result = Mock()
        del result.document
        
        recommendations = generate_recommendations([result])
        
        # Should skip result without document
        assert len(recommendations) == 0

    def test_generate_with_mixed_results(self):
        """Test generating recommendations from mixed valid/invalid results."""
        valid_result = Mock()
        valid_result.document = Mock()
        valid_result.document.content = "Valid content"
        
        invalid_result = Mock()
        del invalid_result.document
        
        recommendations = generate_recommendations([valid_result, invalid_result])
        
        assert len(recommendations) == 1
        assert "Valid content" in recommendations[0]

    def test_generate_with_exception_on_content_access(self):
        """Test generating recommendations when accessing content raises exception."""
        result = Mock()
        result.document = Mock()
        # Make accessing content raise exception
        type(result.document).content = property(lambda self: (_ for _ in ()).throw(Exception("Error")))
        
        recommendations = generate_recommendations([result])
        
        # Should skip result that raises exception
        assert len(recommendations) == 0

    def test_generate_numbering_starts_at_one(self):
        """Test that recommendation numbering starts at 1."""
        results = []
        for i in range(3):
            result = Mock()
            result.document = Mock()
            result.document.content = f"Content {i+1}"
            results.append(result)
        
        recommendations = generate_recommendations(results)
        
        assert recommendations[0].startswith("1.")
        assert recommendations[1].startswith("2.")
        assert recommendations[2].startswith("3.")

