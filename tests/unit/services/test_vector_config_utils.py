"""
Tests for vector_config_utils.py

Author: Agent-3 (Infrastructure & DevOps Specialist)
Date: 2025-01-27
"""

import pytest
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(project_root))

from src.services.utils import vector_config_utils


class TestVectorConfigUtils:
    """Test vector configuration utility functions."""

    def test_load_simple_config_default_path(self):
        """Test load_simple_config with default config_path (None)."""
        agent_id = "Agent-1"
        config = vector_config_utils.load_simple_config(agent_id)
        
        assert isinstance(config, dict)
        assert "collection_name" in config
        assert "embedding_model" in config
        assert "max_results" in config

    def test_load_simple_config_custom_path(self):
        """Test load_simple_config with custom config_path."""
        agent_id = "Agent-2"
        config_path = "/custom/path/config.json"
        config = vector_config_utils.load_simple_config(agent_id, config_path)
        
        assert isinstance(config, dict)
        assert "collection_name" in config
        assert config["collection_name"] == f"agent_{agent_id}"

    def test_load_simple_config_collection_name_format(self):
        """Test collection_name format includes agent_id."""
        agent_id = "Agent-7"
        config = vector_config_utils.load_simple_config(agent_id)
        
        assert config["collection_name"] == f"agent_{agent_id}"
        assert config["collection_name"] == "agent_Agent-7"

    def test_load_simple_config_embedding_model_default(self):
        """Test embedding_model default value."""
        config = vector_config_utils.load_simple_config("Agent-1")
        
        assert config["embedding_model"] == "default"

    def test_load_simple_config_max_results_default(self):
        """Test max_results default value."""
        config = vector_config_utils.load_simple_config("Agent-1")
        
        assert config["max_results"] == 10
        assert isinstance(config["max_results"], int)

    def test_load_simple_config_returns_dict(self):
        """Test load_simple_config always returns a dictionary."""
        config = vector_config_utils.load_simple_config("TestAgent")
        
        assert isinstance(config, dict)
        assert len(config) == 3

    def test_load_simple_config_different_agent_ids(self):
        """Test load_simple_config with different agent IDs."""
        agent_ids = ["Agent-1", "Agent-2", "Agent-3", "test-agent", "custom_agent"]
        
        for agent_id in agent_ids:
            config = vector_config_utils.load_simple_config(agent_id)
            assert config["collection_name"] == f"agent_{agent_id}"

    def test_load_simple_config_config_path_ignored(self):
        """Test that config_path parameter is currently ignored but accepted."""
        agent_id = "Agent-1"
        config1 = vector_config_utils.load_simple_config(agent_id, None)
        config2 = vector_config_utils.load_simple_config(agent_id, "/path/to/config.json")
        
        # Should return same config regardless of path
        assert config1 == config2

    def test_load_simple_config_required_keys(self):
        """Test that config contains all required keys."""
        config = vector_config_utils.load_simple_config("Agent-1")
        
        required_keys = ["collection_name", "embedding_model", "max_results"]
        for key in required_keys:
            assert key in config

    def test_load_simple_config_value_types(self):
        """Test that config values have correct types."""
        config = vector_config_utils.load_simple_config("Agent-1")
        
        assert isinstance(config["collection_name"], str)
        assert isinstance(config["embedding_model"], str)
        assert isinstance(config["max_results"], int)

    def test_load_simple_config_immutable(self):
        """Test that modifying returned config doesn't affect future calls."""
        config1 = vector_config_utils.load_simple_config("Agent-1")
        config1["max_results"] = 999
        
        config2 = vector_config_utils.load_simple_config("Agent-1")
        
        assert config2["max_results"] == 10  # Should be default, not modified

    def test_load_simple_config_empty_agent_id(self):
        """Test load_simple_config with empty agent_id."""
        config = vector_config_utils.load_simple_config("")
        
        assert config["collection_name"] == "agent_"

    def test_load_simple_config_special_characters(self):
        """Test load_simple_config with special characters in agent_id."""
        config = vector_config_utils.load_simple_config("Agent-7_Test")
        
        assert config["collection_name"] == "agent_Agent-7_Test"

    def test_load_simple_config_numeric_agent_id(self):
        """Test load_simple_config with numeric agent_id."""
        config = vector_config_utils.load_simple_config("123")
        
        assert config["collection_name"] == "agent_123"

    def test_load_simple_config_function_signature(self):
        """Test function signature."""
        import inspect
        sig = inspect.signature(vector_config_utils.load_simple_config)
        
        assert 'agent_id' in sig.parameters
        assert 'config_path' in sig.parameters
        assert sig.parameters['config_path'].default is None

    def test_load_simple_config_unicode_agent_id(self):
        """Test load_simple_config with unicode characters in agent_id."""
        config = vector_config_utils.load_simple_config("Agent-测试")
        
        assert config["collection_name"] == "agent_Agent-测试"

    def test_load_simple_config_very_long_agent_id(self):
        """Test load_simple_config with very long agent_id."""
        long_id = "Agent-" + "X" * 100
        config = vector_config_utils.load_simple_config(long_id)
        
        assert config["collection_name"] == f"agent_{long_id}"

    def test_load_simple_config_whitespace_agent_id(self):
        """Test load_simple_config with whitespace in agent_id."""
        config = vector_config_utils.load_simple_config("Agent 7")
        
        assert config["collection_name"] == "agent_Agent 7"

    def test_load_simple_config_config_path_various_values(self):
        """Test load_simple_config with various config_path values."""
        agent_id = "Agent-1"
        paths = [None, "", "/path/to/config.json", "relative/path.json", "C:\\Windows\\path.json"]
        
        for path in paths:
            config = vector_config_utils.load_simple_config(agent_id, path)
            # All should return same config (path is ignored)
            assert config["collection_name"] == f"agent_{agent_id}"

    def test_load_simple_config_consistency(self):
        """Test that load_simple_config returns consistent results."""
        agent_id = "Agent-1"
        config1 = vector_config_utils.load_simple_config(agent_id)
        config2 = vector_config_utils.load_simple_config(agent_id)
        
        assert config1 == config2

    def test_load_simple_config_max_results_type(self):
        """Test that max_results is always an integer."""
        config = vector_config_utils.load_simple_config("Agent-1")
        
        assert isinstance(config["max_results"], int)
        assert config["max_results"] == 10

    def test_load_simple_config_embedding_model_type(self):
        """Test that embedding_model is always a string."""
        config = vector_config_utils.load_simple_config("Agent-1")
        
        assert isinstance(config["embedding_model"], str)
        assert config["embedding_model"] == "default"

