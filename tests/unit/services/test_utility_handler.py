"""
Unit tests for utility_handler.py

Target: ≥85% coverage, 15+ test methods
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from src.services.handlers.utility_handler import UtilityHandler


class TestUtilityHandler:
    """Test suite for UtilityHandler."""

    @pytest.fixture
    def handler(self):
        """Create UtilityHandler instance."""
        return UtilityHandler()

    def test_handler_initialization(self, handler):
        """Test handler initializes correctly."""
        assert handler is not None
        assert handler.logger is not None

    @patch('src.services.handlers.utility_handler.OnboardingHandler')
    def test_check_status_specific_agent(self, mock_handler_class, handler):
        """Test check_status for specific agent."""
        mock_handler = Mock()
        mock_handler_class.return_value = mock_handler
        mock_handler.get_onboarding_status.return_value = {
            "status": "onboarded",
            "role": "Specialist",
            "onboarded_at": "2025-01-01",
            "workspace_path": "/path",
            "capabilities": ["test"],
            "vector_db_enabled": True
        }
        
        result = handler.check_status("Agent-1")
        
        assert result["agent_id"] == "Agent-1"
        assert result["status"] == "onboarded"
        assert result["role"] == "Specialist"

    @patch('src.services.handlers.utility_handler.OnboardingHandler')
    def test_check_status_agent_not_found(self, mock_handler_class, handler):
        """Test check_status for non-existent agent."""
        mock_handler = Mock()
        mock_handler_class.return_value = mock_handler
        mock_handler.get_onboarding_status.return_value = None
        
        result = handler.check_status("Agent-999")
        
        assert result["agent_id"] == "Agent-999"
        assert result["status"] == "not_found"

    @patch('src.services.handlers.utility_handler.OnboardingHandler')
    @patch('src.services.handlers.utility_handler.get_vector_database_service')
    def test_check_status_all_agents(self, mock_vector_db_func, mock_handler_class, handler):
        """Test check_status for all agents."""
        mock_handler = Mock()
        mock_handler_class.return_value = mock_handler
        mock_handler.list_onboarded_agents.return_value = ["Agent-1", "Agent-2"]
        
        # Mock vector database service
        mock_vector_db_instance = Mock()
        mock_stats = Mock()
        mock_stats.total_documents = 100
        mock_stats.total_collections = 5
        mock_vector_db_instance.get_stats.return_value = mock_stats
        mock_vector_db_func.return_value = mock_vector_db_instance
        
        result = handler.check_status(None)
        
        assert result["total_agents"] == 2
        assert result["active_agents"] == 2

