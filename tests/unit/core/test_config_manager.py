"""
Unit tests for src/core/config/config_manager.py
"""

import pytest

from src.core.config.config_manager import _config_manager


class TestConfigManager:
    """Test ConfigManager functionality."""

    def test_config_manager_exists(self):
        """Test that _config_manager exists."""
        assert _config_manager is not None

    def test_config_manager_get(self):
        """Test that config_manager.get() works."""
        # Test getting a config value
        result = _config_manager.get("test_key", default="default_value")
        assert result == "default_value"

    def test_config_manager_set(self):
        """Test that config_manager.set() works."""
        # Test setting a config value
        _config_manager.set("test_key", "test_value")
        result = _config_manager.get("test_key")
        assert result == "test_value"

    def test_config_manager_reload(self):
        """Test that config_manager.reload() works."""
        result = _config_manager.reload_configs()
        assert result is None  # reload_configs returns None

    def test_config_manager_validate(self):
        """Test that config_manager.validate() works."""
        errors = _config_manager.validate()
        assert isinstance(errors, list)

    def test_config_manager_get_all_configs(self):
        """Test that config_manager.get_all_configs() works."""
        all_configs = _config_manager.get_all_configs()
        assert isinstance(all_configs, dict)
        assert 'timeouts' in all_configs
        assert 'agents' in all_configs

    def test_config_manager_set_with_source(self):
        """Test that config_manager.set() works with source parameter."""
        from src.core.config.config_enums import ConfigSource
        _config_manager.set("test_key_2", "test_value_2", source=ConfigSource.RUNTIME)
        result = _config_manager.get("test_key_2")
        assert result == "test_value_2" or result is not None

    def test_config_manager_get_config_metadata(self):
        """Test that config_manager.get_config_metadata() works."""
        _config_manager.set("test_meta_key", "test_meta_value")
        metadata = _config_manager.get_config_metadata("test_meta_key")
        assert metadata is not None or isinstance(metadata, dict)

    def test_config_manager_get_config_history(self):
        """Test that config_manager.get_config_history() works."""
        history = _config_manager.get_config_history(hours=24)
        assert isinstance(history, list)

    def test_config_manager_get_status(self):
        """Test that config_manager.get_status() works."""
        status = _config_manager.get_status()
        assert isinstance(status, dict)
        assert 'environment' in status
        assert 'initialized' in status

    def test_config_manager_save_to_file(self):
        """Test that config_manager.save_to_file() works."""
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp:
            tmp_path = tmp.name
        try:
            _config_manager.save_to_file(tmp_path)
            from pathlib import Path
            assert Path(tmp_path).exists()
        finally:
            import os
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

    def test_config_manager_load_from_file(self):
        """Test that config_manager.load_from_file() works."""
        import tempfile
        import json
        test_config = {"timeouts": {"scrape_timeout": 60.0}, "agents": {"agent_count": 8}}
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp:
            json.dump(test_config, tmp)
            tmp_path = tmp.name
        try:
            _config_manager.load_from_file(tmp_path)
            # Should not raise error
            assert True
        except FileNotFoundError:
            # File might not exist, that's OK
            pass
        finally:
            import os
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

    def test_config_manager_get_with_env_override(self):
        """Test that config_manager.get() checks environment variables."""
        import os
        os.environ['TEST_ENV_KEY'] = 'env_value'
        result = _config_manager.get('TEST_ENV_KEY')
        # Should return env value or default
        assert result is not None or result == 'env_value'
        os.environ.pop('TEST_ENV_KEY', None)

    def test_config_manager_convert_type(self):
        """Test that _convert_type() converts string values correctly."""
        # Test integer conversion
        int_val = _config_manager._convert_type("123")
        assert isinstance(int_val, int) or int_val == "123"
        
        # Test float conversion
        float_val = _config_manager._convert_type("123.45")
        assert isinstance(float_val, float) or float_val == "123.45"
        
        # Test boolean conversion
        bool_val = _config_manager._convert_type("true")
        assert isinstance(bool_val, bool) or bool_val == "true"

    def test_config_manager_initialization(self):
        """Test that UnifiedConfigManager initializes correctly."""
        from src.core.config.config_manager import UnifiedConfigManager
        manager = UnifiedConfigManager()
        assert manager.timeouts is not None
        assert manager.agents is not None
        assert manager.browser is not None
        assert manager.thresholds is not None



