"""
Unit tests for core_configuration_manager.py - MEDIUM PRIORITY

Tests CoreConfigurationManager class and configuration operations.
"""

import pytest
from unittest.mock import Mock, MagicMock, patch, mock_open
from datetime import datetime
import sys
import json
import tempfile
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.managers.contracts import ManagerContext, ManagerResult
from src.core.managers.core_configuration_manager import CoreConfigurationManager


class TestCoreConfigurationManager:
    """Test suite for CoreConfigurationManager class."""

    @pytest.fixture
    def mock_context(self):
        """Create mock manager context."""
        return ManagerContext(
            config={"test": "config"},
            logger=lambda msg: None,
            metrics={},
            timestamp=datetime.now()
        )

    @pytest.fixture
    def manager(self):
        """Create CoreConfigurationManager instance."""
        with patch('src.core.managers.core_configuration_manager.get_default_discord_config') as mock_discord, \
             patch('src.core.managers.core_configuration_manager.get_default_app_config') as mock_app, \
             patch('src.core.managers.core_configuration_manager.get_default_db_config') as mock_db, \
             patch('src.core.managers.core_configuration_manager.get_validation_rules') as mock_rules:
            
            mock_discord.return_value = {"discord": "config"}
            mock_app.return_value = {"app": "config"}
            mock_db.return_value = {"db": "config"}
            mock_rules.return_value = {"type1": {"field1": {"required": True}}}
            
            manager = CoreConfigurationManager()
            return manager

    def test_manager_initialization(self, manager):
        """Test manager initialization."""
        assert manager is not None
        assert hasattr(manager, 'configs')
        assert hasattr(manager, 'config_files')
        assert hasattr(manager, 'environment_vars')
        assert hasattr(manager, 'validation_rules')

    def test_initialize(self, manager, mock_context):
        """Test manager initialization with context."""
        result = manager.initialize(mock_context)
        assert result is True

    def test_load_config_from_memory(self, manager, mock_context):
        """Test load_config from memory."""
        manager.configs["test_config"] = {"key": "value"}
        result = manager.load_config(mock_context, "test_config")
        assert result.success is True
        assert result.data["config_key"] == "test_config"
        assert result.data["config"] == {"key": "value"}

    def test_load_config_not_found(self, manager, mock_context):
        """Test load_config when config not found."""
        result = manager.load_config(mock_context, "nonexistent")
        assert result.success is False
        assert "not found" in result.error.lower()

    def test_save_config(self, manager, mock_context):
        """Test save_config operation."""
        config_data = {"key": "value", "type": "test"}
        result = manager.save_config(mock_context, "test_config", config_data)
        assert result.success is True
        assert "test_config" in manager.configs
        assert manager.configs["test_config"] == config_data

    def test_save_config_with_file_path(self, manager, mock_context):
        """Test save_config with file path."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "config.json"
            config_data = {"key": "value", "file_path": str(file_path)}
            result = manager.save_config(mock_context, "test_config", config_data)
            assert result.success is True
            assert file_path.exists()
            assert "test_config" in manager.config_files

    def test_validate_config_success(self, manager, mock_context):
        """Test validate_config with valid config."""
        config_data = {"type": "type1", "field1": "value"}
        result = manager.validate_config(mock_context, config_data)
        assert result.success is True
        assert result.data["valid"] is True

    def test_validate_config_failure(self, manager, mock_context):
        """Test validate_config with invalid config."""
        # Ensure validation rules are set up
        manager.validation_rules = {"type1": {"field1": {"required": True}}}
        config_data = {"type": "type1"}  # Missing required field1
        result = manager.validate_config(mock_context, config_data)
        assert result.success is False
        assert "validation_errors" in result.data or "error" in result.error.lower()

    def test_execute_load_config(self, manager, mock_context):
        """Test execute load_config operation."""
        manager.configs["test"] = {"key": "value"}
        result = manager.execute(mock_context, "load_config", {"config_key": "test"})
        assert result.success is True
        assert result.data["config_key"] == "test"

    def test_execute_save_config(self, manager, mock_context):
        """Test execute save_config operation."""
        config_data = {"key": "value"}
        result = manager.execute(mock_context, "save_config", {
            "config_key": "test",
            "config_data": config_data
        })
        assert result.success is True

    def test_execute_validate_config(self, manager, mock_context):
        """Test execute validate_config operation."""
        config_data = {"key": "value"}
        result = manager.execute(mock_context, "validate_config", {"config_data": config_data})
        assert result.success is True

    def test_execute_get_all_configs(self, manager, mock_context):
        """Test execute get_all_configs operation."""
        manager.configs["config1"] = {"key": "value1"}
        manager.configs["config2"] = {"key": "value2"}
        result = manager.execute(mock_context, "get_all_configs", {})
        assert result.success is True
        assert len(result.data["configs"]) == 2

    def test_execute_unknown_operation(self, manager, mock_context):
        """Test execute with unknown operation."""
        result = manager.execute(mock_context, "unknown_operation", {})
        assert result.success is False
        assert "Unknown operation" in result.error

    def test_cleanup(self, manager, mock_context):
        """Test cleanup operation."""
        manager.configs["test"] = {"key": "value"}
        manager.config_files["test"] = "/tmp/test.json"
        result = manager.cleanup(mock_context)
        assert result is True
        assert len(manager.configs) == 0
        assert len(manager.config_files) == 0

    def test_get_status(self, manager):
        """Test get_status operation."""
        manager.configs["config1"] = {}
        manager.config_files["config1"] = "/tmp/config1.json"
        manager.environment_vars["VAR1"] = "value1"
        manager.validation_rules["type1"] = {}
        
        status = manager.get_status()
        assert status["total_configs"] == 1
        assert status["file_configs"] == 1
        assert status["environment_vars"] == 1
        assert status["validation_rules"] == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

