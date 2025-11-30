"""
Tests for Discord Core Configuration
====================================

Comprehensive tests for src/discord_commander/core.py

Author: Agent-7 (Web Development Specialist)
Date: 2025-11-29
Target: 80%+ coverage
"""

import os
import pytest
from unittest.mock import patch, MagicMock


class TestDiscordConfig:
    """Test DiscordConfig dataclass."""

    def test_config_initialization_defaults(self):
        """Test config initialization with default values."""
        from src.discord_commander.core import DiscordConfig

        config = DiscordConfig()
        assert config.command_prefix == "!"
        assert config.bot_token is None or isinstance(config.bot_token, str)
        assert config.channel_id is None or isinstance(config.channel_id, str)

    def test_config_initialization_custom_values(self):
        """Test config initialization with custom values."""
        from src.discord_commander.core import DiscordConfig

        config = DiscordConfig(
            bot_token="test_token",
            command_prefix="?",
            channel_id="123456789"
        )
        assert config.bot_token == "test_token"
        assert config.command_prefix == "?"
        assert config.channel_id == "123456789"

    @patch.dict(os.environ, {"DISCORD_BOT_TOKEN": "env_token", "DISCORD_CHANNEL_ID": "env_channel"})
    def test_config_loads_from_environment(self):
        """Test config loads from environment variables."""
        from src.discord_commander.core import DiscordConfig

        config = DiscordConfig()
        assert config.bot_token == "env_token"
        assert config.channel_id == "env_channel"

    @patch.dict(os.environ, {}, clear=True)
    def test_config_handles_missing_environment(self):
        """Test config handles missing environment variables."""
        from src.discord_commander.core import DiscordConfig

        config = DiscordConfig()
        assert config.bot_token is None
        assert config.channel_id is None

    def test_config_validate_with_valid_data(self):
        """Test validation with valid configuration."""
        from src.discord_commander.core import DiscordConfig

        config = DiscordConfig(
            bot_token="valid_token",
            channel_id="123456789"
        )
        issues = config.validate()
        assert len(issues) == 0

    def test_config_validate_missing_bot_token(self):
        """Test validation detects missing bot token."""
        from src.discord_commander.core import DiscordConfig

        config = DiscordConfig(bot_token=None, channel_id="123456789")
        issues = config.validate()
        assert len(issues) > 0
        assert any("DISCORD_BOT_TOKEN" in issue for issue in issues)

    def test_config_validate_missing_channel_id(self):
        """Test validation handles missing channel ID (warning only)."""
        from src.discord_commander.core import DiscordConfig

        config = DiscordConfig(bot_token="valid_token", channel_id=None)
        issues = config.validate()
        # Channel ID is optional, so no error, just warning
        assert len(issues) == 0

    def test_config_is_valid_with_valid_data(self):
        """Test is_valid returns True for valid config."""
        from src.discord_commander.core import DiscordConfig

        config = DiscordConfig(
            bot_token="valid_token",
            channel_id="123456789"
        )
        assert config.is_valid() is True

    def test_config_is_valid_with_missing_token(self):
        """Test is_valid returns False for missing token."""
        from src.discord_commander.core import DiscordConfig

        config = DiscordConfig(bot_token=None, channel_id="123456789")
        assert config.is_valid() is False

    def test_config_is_valid_with_empty_token(self):
        """Test is_valid returns False for empty token."""
        from src.discord_commander.core import DiscordConfig

        config = DiscordConfig(bot_token="", channel_id="123456789")
        assert config.is_valid() is False

    @patch.dict(os.environ, {"DISCORD_BOT_TOKEN": "env_token"})
    def test_config_post_init_loads_token_from_env(self):
        """Test __post_init__ loads token from environment."""
        from src.discord_commander.core import DiscordConfig

        config = DiscordConfig(bot_token=None)
        assert config.bot_token == "env_token"

    @patch.dict(os.environ, {"DISCORD_CHANNEL_ID": "env_channel"})
    def test_config_post_init_loads_channel_from_env(self):
        """Test __post_init__ loads channel from environment."""
        from src.discord_commander.core import DiscordConfig

        config = DiscordConfig(channel_id=None)
        assert config.channel_id == "env_channel"

    def test_config_post_init_preserves_explicit_values(self):
        """Test __post_init__ preserves explicitly set values."""
        from src.discord_commander.core import DiscordConfig

        with patch.dict(os.environ, {"DISCORD_BOT_TOKEN": "env_token"}):
            config = DiscordConfig(bot_token="explicit_token")
            assert config.bot_token == "explicit_token"  # Explicit takes precedence

    def test_config_dataclass_fields(self):
        """Test dataclass fields are properly defined."""
        from src.discord_commander.core import DiscordConfig

        config = DiscordConfig()
        # Verify all fields exist
        assert hasattr(config, 'bot_token')
        assert hasattr(config, 'command_prefix')
        assert hasattr(config, 'channel_id')
        assert hasattr(config, 'validate')
        assert hasattr(config, 'is_valid')

