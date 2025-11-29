"""
Unit tests for src/services/learning_recommender.py

Tests learning recommender functionality including:
- Initialization with/without vector DB
- Configuration loading
- Learning recommendations generation
- Work pattern analysis
- Skill gap identification
- Fallback recommendations
"""

import pytest
from unittest.mock import Mock, MagicMock, patch, mock_open
from pathlib import Path
import json
import yaml

from src.services.learning_recommender import LearningRecommender


class TestLearningRecommender:
    """Test learning recommender."""

    @pytest.fixture
    def recommender_with_vector_db(self):
        """Create recommender with vector DB available."""
        with patch('src.services.learning_recommender.get_vector_database_service') as mock_get, \
             patch('src.services.learning_recommender.search_vector_database') as mock_search:
            mock_vector_db = MagicMock()
            mock_get.return_value = mock_vector_db
            mock_search.return_value = []
            
            recommender = LearningRecommender("Agent-3")
            return recommender

    @pytest.fixture
    def recommender_without_vector_db(self):
        """Create recommender without vector DB."""
        with patch('src.services.learning_recommender.get_vector_database_service') as mock_get:
            mock_get.side_effect = ImportError("Vector DB not available")
            
            recommender = LearningRecommender("Agent-3")
            return recommender

    def test_init_with_vector_db(self, recommender_with_vector_db):
        """Test initialization with vector database."""
        assert recommender_with_vector_db.agent_id == "Agent-3"
        assert recommender_with_vector_db.vector_integration["status"] == "connected"
        assert recommender_with_vector_db.config is not None

    def test_init_without_vector_db(self, recommender_without_vector_db):
        """Test initialization without vector database."""
        assert recommender_without_vector_db.agent_id == "Agent-3"
        assert recommender_without_vector_db.vector_integration["status"] == "disconnected"
        assert recommender_without_vector_db.config is not None

    def test_default_config(self, recommender_with_vector_db):
        """Test default configuration values."""
        config = recommender_with_vector_db.config
        
        assert "learning_categories" in config
        assert "priority_weights" in config
        assert "max_recommendations" in config
        assert "min_confidence" in config
        assert config["max_recommendations"] == 5
        assert config["min_confidence"] == 0.6

    @patch('builtins.open', new_callable=mock_open, read_data='{"max_recommendations": 10}')
    @patch('pathlib.Path.exists')
    def test_load_config_from_json(self, mock_exists, mock_file):
        """Test loading configuration from JSON file."""
        mock_exists.return_value = True
        
        with patch('src.services.learning_recommender.get_vector_database_service') as mock_get:
            mock_get.return_value = MagicMock()
            
            recommender = LearningRecommender("Agent-3", config_path="test_config.json")
            
            assert recommender.config["max_recommendations"] == 10

    @patch('builtins.open', new_callable=mock_open, read_data='max_recommendations: 8')
    @patch('pathlib.Path.exists')
    @patch('yaml.safe_load')
    def test_load_config_from_yaml(self, mock_yaml, mock_exists, mock_file):
        """Test loading configuration from YAML file."""
        mock_exists.return_value = True
        mock_yaml.return_value = {"max_recommendations": 8}
        
        with patch('src.services.learning_recommender.get_vector_database_service') as mock_get:
            mock_get.return_value = MagicMock()
            
            recommender = LearningRecommender("Agent-3", config_path="test_config.yaml")
            
            assert recommender.config["max_recommendations"] == 8

    @patch('pathlib.Path.exists')
    def test_load_config_file_not_found(self, mock_exists):
        """Test loading configuration when file doesn't exist."""
        mock_exists.return_value = False
        
        with patch('src.services.learning_recommender.get_vector_database_service') as mock_get:
            mock_get.return_value = MagicMock()
            
            recommender = LearningRecommender("Agent-3", config_path="missing.json")
            
            # Should use default config
            assert recommender.config["max_recommendations"] == 5

    def test_get_learning_recommendations_with_vector_db(self, recommender_with_vector_db):
        """Test getting learning recommendations with vector DB."""
        with patch.object(recommender_with_vector_db, '_analyze_work_patterns') as mock_analyze, \
             patch.object(recommender_with_vector_db, '_identify_skill_gaps') as mock_gaps, \
             patch.object(recommender_with_vector_db, '_generate_learning_recommendations') as mock_gen:
            
            mock_analyze.return_value = {"work_types": [], "technologies": []}
            mock_gaps.return_value = ["python"]
            mock_gen.return_value = [{"recommendation_id": "test_1", "title": "Test"}]
            
            recommendations = recommender_with_vector_db.get_learning_recommendations()
            
            assert isinstance(recommendations, list)
            assert len(recommendations) <= recommender_with_vector_db.config["max_recommendations"]

    def test_get_learning_recommendations_without_vector_db(self, recommender_without_vector_db):
        """Test getting learning recommendations without vector DB (fallback)."""
        recommendations = recommender_without_vector_db.get_learning_recommendations()
        
        assert isinstance(recommendations, list)
        assert len(recommendations) > 0
        assert all("recommendation_id" in rec for rec in recommendations)

    def test_get_learning_recommendations_error_handling(self, recommender_with_vector_db):
        """Test error handling in get_learning_recommendations."""
        with patch.object(recommender_with_vector_db, '_analyze_work_patterns') as mock_analyze:
            mock_analyze.side_effect = Exception("Test error")
            
            recommendations = recommender_with_vector_db.get_learning_recommendations()
            
            # Should return fallback recommendations
            assert isinstance(recommendations, list)
            assert len(recommendations) > 0

    @patch('src.services.learning_recommender.search_vector_database')
    @patch('src.services.learning_recommender.SearchQuery')
    def test_analyze_work_patterns(self, mock_query_class, mock_search, recommender_with_vector_db):
        """Test work pattern analysis."""
        # Mock search result
        mock_result = MagicMock()
        mock_result.document.document_type.value = "code"
        mock_result.document.tags = ["python", "testing"]
        mock_search.return_value = [mock_result, mock_result]
        
        patterns = recommender_with_vector_db._analyze_work_patterns()
        
        assert "work_types" in patterns
        assert "technologies" in patterns
        assert "total_work_items" in patterns
        assert patterns["total_work_items"] == 2

    @patch('src.services.learning_recommender.search_vector_database')
    def test_analyze_work_patterns_error_handling(self, mock_search, recommender_with_vector_db):
        """Test work pattern analysis error handling."""
        mock_search.side_effect = Exception("Search error")
        
        patterns = recommender_with_vector_db._analyze_work_patterns()
        
        assert patterns == {"work_types": [], "technologies": [], "total_work_items": 0}

    def test_identify_skill_gaps_missing_tech(self, recommender_with_vector_db):
        """Test identifying skill gaps for missing technologies."""
        work_patterns = {
            "work_types": ["code"],
            "technologies": ["javascript"]
        }
        
        gaps = recommender_with_vector_db._identify_skill_gaps(work_patterns)
        
        assert isinstance(gaps, list)
        # Should identify missing python, vector_database, etc.
        assert len(gaps) > 0

    def test_identify_skill_gaps_missing_work_types(self, recommender_with_vector_db):
        """Test identifying skill gaps for missing work types."""
        work_patterns = {
            "work_types": ["code"],
            "technologies": ["python"]
        }
        
        gaps = recommender_with_vector_db._identify_skill_gaps(work_patterns)
        
        # Should identify missing documentation or testing
        assert isinstance(gaps, list)

    def test_identify_skill_gaps_no_gaps(self, recommender_with_vector_db):
        """Test identifying skill gaps when all skills present."""
        work_patterns = {
            "work_types": ["code", "documentation", "test"],
            "technologies": ["python", "vector_database", "coordination", "testing"]
        }
        
        gaps = recommender_with_vector_db._identify_skill_gaps(work_patterns)
        
        # Should have fewer gaps
        assert isinstance(gaps, list)

    def test_generate_learning_recommendations_python_gap(self, recommender_with_vector_db):
        """Test generating recommendations for Python skill gap."""
        gaps = ["python"]
        
        recommendations = recommender_with_vector_db._generate_learning_recommendations(gaps)
        
        assert len(recommendations) > 0
        assert any("python" in rec.get("recommendation_id", "").lower() or 
                  "python" in rec.get("title", "").lower() 
                  for rec in recommendations)

    def test_generate_learning_recommendations_vector_db_gap(self, recommender_with_vector_db):
        """Test generating recommendations for vector database gap."""
        gaps = ["vector_database"]
        
        recommendations = recommender_with_vector_db._generate_learning_recommendations(gaps)
        
        assert len(recommendations) > 0
        assert any("vector" in rec.get("recommendation_id", "").lower() or 
                  "vector" in rec.get("title", "").lower() 
                  for rec in recommendations)

    def test_generate_learning_recommendations_no_gaps(self, recommender_with_vector_db):
        """Test generating recommendations when no gaps (fallback)."""
        gaps = []
        
        recommendations = recommender_with_vector_db._generate_learning_recommendations(gaps)
        
        # Should return fallback recommendations
        assert len(recommendations) > 0
        assert all("recommendation_id" in rec for rec in recommendations)

    def test_get_fallback_recommendations(self, recommender_with_vector_db):
        """Test fallback recommendations."""
        recommendations = recommender_with_vector_db._get_fallback_recommendations()
        
        assert isinstance(recommendations, list)
        assert len(recommendations) == 2
        assert all("recommendation_id" in rec for rec in recommendations)
        assert all("type" in rec for rec in recommendations)
        assert all("title" in rec for rec in recommendations)
        assert all("description" in rec for rec in recommendations)
        assert all("priority" in rec for rec in recommendations)
        assert all("confidence" in rec for rec in recommendations)

    def test_max_recommendations_limit(self, recommender_with_vector_db):
        """Test that recommendations are limited by max_recommendations config."""
        recommender_with_vector_db.config["max_recommendations"] = 2
        
        with patch.object(recommender_with_vector_db, '_analyze_work_patterns') as mock_analyze, \
             patch.object(recommender_with_vector_db, '_identify_skill_gaps') as mock_gaps, \
             patch.object(recommender_with_vector_db, '_generate_learning_recommendations') as mock_gen:
            
            mock_analyze.return_value = {"work_types": [], "technologies": []}
            mock_gaps.return_value = ["python", "vector_database", "coordination"]
            mock_gen.return_value = [
                {"recommendation_id": "1"},
                {"recommendation_id": "2"},
                {"recommendation_id": "3"},
                {"recommendation_id": "4"}
            ]
            
            recommendations = recommender_with_vector_db.get_learning_recommendations()
            
            assert len(recommendations) == 2

