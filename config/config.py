#!/usr/bin/env python3
"""
Agent Cellphone V2 - Configuration Management
=============================================

Environment-aware configuration management system.
Supports multiple deployment environments with secure secret handling.

V2 Compliance: <300 lines, SOLID principles
Author: Agent-2 (Architecture & Design Specialist)
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, field
from dotenv import load_dotenv


@dataclass
class DatabaseConfig:
    """Database configuration."""
    host: str = "localhost"
    port: int = 5432
    database: str = "agent_cellphone"
    user: str = "agent"
    password: str = ""
    ssl_mode: str = "require"

    @property
    def connection_string(self) -> str:
        """Get database connection string."""
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"


@dataclass
class DiscordConfig:
    """Discord bot configuration."""
    token: str = ""
    command_prefix: str = "!"
    status_channel_id: Optional[int] = None
    log_channel_id: Optional[int] = None


@dataclass
class TwitchConfig:
    """Twitch bot configuration."""
    channel: str = ""
    access_token: str = ""
    client_id: str = ""
    client_secret: str = ""


@dataclass
class WebConfig:
    """Web interface configuration."""
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    secret_key: str = ""
    cors_origins: list[str] = field(default_factory=lambda: ["*"])


@dataclass
class AgentConfig:
    """Agent system configuration."""
    mode: str = "4-agent"
    active_agents: list[str] = field(default_factory=lambda: ["Agent-1", "Agent-2", "Agent-3", "Agent-4"])
    workspace_root: str = "agent_workspaces"
    max_concurrent_tasks: int = 3


@dataclass
class SystemConfig:
    """Main system configuration."""
    environment: str = "development"
    log_level: str = "INFO"
    data_dir: str = "data"
    temp_dir: str = "temp"
    cache_dir: str = "cache"
    log_dir: str = "logs"

    # Sub-configurations
    database: DatabaseConfig = field(default_factory=DatabaseConfig)
    discord: DiscordConfig = field(default_factory=DiscordConfig)
    twitch: TwitchConfig = field(default_factory=TwitchConfig)
    web: WebConfig = field(default_factory=WebConfig)
    agent: AgentConfig = field(default_factory=AgentConfig)


class ConfigManager:
    """Centralized configuration management."""

    def __init__(self, config_dir: Optional[Path] = None):
        """Initialize configuration manager.

        Args:
            config_dir: Configuration directory (default: project_root/config)
        """
        if config_dir is None:
            project_root = Path(__file__).parent.parent
            config_dir = project_root / "config"

        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(exist_ok=True)

        # Load environment variables
        load_dotenv()

        # Determine environment
        self.environment = os.getenv("AGENT_CELLPHONE_ENV", "development")

        # Load configuration
        self.config = self._load_config()

    def _load_config(self) -> SystemConfig:
        """Load configuration from environment and config files."""
        config = SystemConfig(environment=self.environment)

        # Load base configuration
        base_config = self._load_json_config("base.json")
        if base_config:
            self._merge_config(config, base_config)

        # Load environment-specific configuration
        env_config = self._load_json_config(f"{self.environment}.json")
        if env_config:
            self._merge_config(config, env_config)

        # Override with environment variables
        self._load_from_env(config)

        return config

    def _load_json_config(self, filename: str) -> Optional[Dict[str, Any]]:
        """Load JSON configuration file."""
        config_file = self.config_dir / filename
        if config_file.exists():
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                return None
        return None

    def _merge_config(self, config: SystemConfig, data: Dict[str, Any]) -> None:
        """Merge dictionary data into configuration object."""
        for key, value in data.items():
            if hasattr(config, key):
                attr = getattr(config, key)
                if isinstance(attr, (DatabaseConfig, DiscordConfig, TwitchConfig, WebConfig, AgentConfig)):
                    self._merge_subconfig(attr, value)
                else:
                    setattr(config, key, value)

    def _merge_subconfig(self, subconfig: Any, data: Dict[str, Any]) -> None:
        """Merge data into sub-configuration object."""
        for key, value in data.items():
            if hasattr(subconfig, key):
                setattr(subconfig, key, value)

    def _load_from_env(self, config: SystemConfig) -> None:
        """Load configuration from environment variables."""
        # Database
        config.database.host = os.getenv("DB_HOST", config.database.host)
        config.database.port = int(os.getenv("DB_PORT", config.database.port))
        config.database.database = os.getenv("DB_NAME", config.database.database)
        config.database.user = os.getenv("DB_USER", config.database.user)
        config.database.password = os.getenv("DB_PASSWORD", config.database.password)

        # Discord
        config.discord.token = os.getenv("DISCORD_BOT_TOKEN", config.discord.token)

        # Twitch
        config.twitch.channel = os.getenv("TWITCH_CHANNEL", config.twitch.channel)
        config.twitch.access_token = os.getenv("TWITCH_ACCESS_TOKEN", config.twitch.access_token)

        # Web
        config.web.secret_key = os.getenv("SECRET_KEY", config.web.secret_key)
        config.web.debug = os.getenv("DEBUG", "false").lower() == "true"

        # System
        config.log_level = os.getenv("LOG_LEVEL", config.log_level)

    def save_config(self) -> None:
        """Save current configuration to file."""
        env_config = self._config_to_dict(self.config)
        config_file = self.config_dir / f"{self.environment}.json"

        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(env_config, f, indent=2, default=str)

    def _config_to_dict(self, config: SystemConfig) -> Dict[str, Any]:
        """Convert configuration object to dictionary."""
        return {
            "environment": config.environment,
            "log_level": config.log_level,
            "data_dir": config.data_dir,
            "temp_dir": config.temp_dir,
            "cache_dir": config.cache_dir,
            "log_dir": config.log_dir,
            "database": {
                "host": config.database.host,
                "port": config.database.port,
                "database": config.database.database,
                "user": config.database.user,
                "ssl_mode": config.database.ssl_mode
            },
            "discord": {
                "command_prefix": config.discord.command_prefix,
                "status_channel_id": config.discord.status_channel_id,
                "log_channel_id": config.discord.log_channel_id
            },
            "twitch": {
                "channel": config.twitch.channel
            },
            "web": {
                "host": config.web.host,
                "port": config.web.port,
                "debug": config.web.debug,
                "cors_origins": config.web.cors_origins
            },
            "agent": {
                "mode": config.agent.mode,
                "active_agents": config.agent.active_agents,
                "workspace_root": config.agent.workspace_root,
                "max_concurrent_tasks": config.agent.max_concurrent_tasks
            }
        }

    def get_config(self) -> SystemConfig:
        """Get current configuration."""
        return self.config


# Global configuration instance
_config_manager: Optional[ConfigManager] = None


def get_config() -> SystemConfig:
    """Get global configuration instance."""
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager()
    return _config_manager.get_config()


def reload_config() -> SystemConfig:
    """Reload configuration from files and environment."""
    global _config_manager
    _config_manager = ConfigManager()
    return _config_manager.get_config()


# Convenience functions
def is_development() -> bool:
    """Check if running in development environment."""
    return get_config().environment == "development"


def is_production() -> bool:
    """Check if running in production environment."""
    return get_config().environment == "production"


def is_docker() -> bool:
    """Check if running in Docker environment."""
    return os.getenv("DOCKER_COMPOSE", "false").lower() == "true"