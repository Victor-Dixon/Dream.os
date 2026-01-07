"""
Setup Service - Agent Cellphone V2
==================================

SSOT Domain: core

Core service for system setup and configuration management.

Features:
- Environment variable management
- Service configuration
- Configuration validation
- Setup automation
- Configuration persistence

V2 Compliant: Yes (<300 lines)
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2026-01-07
"""

import os
import json
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict

try:
    from dotenv import load_dotenv, set_key
    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False

@dataclass
class ServiceConfig:
    """Service configuration settings."""
    enabled: bool = False
    auto_start: bool = False
    config_valid: bool = False
    dependencies: List[str] = None

    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []

@dataclass
class SetupConfig:
    """Complete setup configuration."""
    # Environment settings
    environment: str = "development"

    # Discord settings
    discord_bot_token: Optional[str] = None
    discord_guild_id: Optional[str] = None
    discord_channel_id: Optional[str] = None

    # Service configurations
    services: Dict[str, ServiceConfig] = None

    # Database settings
    database_url: Optional[str] = None
    database_enabled: bool = False

    # API settings
    api_port: int = 8001
    api_host: str = "localhost"

    # Logging settings
    log_level: str = "INFO"
    log_file: Optional[str] = None

    def __post_init__(self):
        if self.services is None:
            self.services = {
                "discord_bot": ServiceConfig(enabled=True, auto_start=True),
                "fastapi": ServiceConfig(enabled=True, auto_start=True),
                "message_queue": ServiceConfig(enabled=True, auto_start=True),
                "database": ServiceConfig(enabled=False, auto_start=False),
            }

class SetupService:
    """
    Service for managing system setup and configuration.
    """

    def __init__(self, project_root: Optional[Path] = None):
        self.project_root = project_root or Path(__file__).parent.parent.parent
        self.env_file = self.project_root / ".env"
        self.config_file = self.project_root / "config" / "setup_config.json"

        # Ensure config directory exists
        self.config_file.parent.mkdir(exist_ok=True)

        # Load dotenv if available
        if DOTENV_AVAILABLE:
            load_dotenv(dotenv_path=self.env_file)

    def load_config(self) -> SetupConfig:
        """
        Load setup configuration from file.

        Returns:
            Setup configuration object
        """
        if not self.config_file.exists():
            return SetupConfig()

        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return SetupConfig(**data)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Warning: Could not load config: {e}")
            return SetupConfig()

    def save_config(self, config: SetupConfig) -> None:
        """
        Save setup configuration to file.

        Args:
            config: Setup configuration to save
        """
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(asdict(config), f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving config: {e}")

    def validate_environment(self) -> Tuple[bool, List[str]]:
        """
        Validate current environment setup.

        Returns:
            Tuple of (is_valid, issues_list)
        """
        issues = []

        # Check required environment variables
        required_vars = [
            ("DISCORD_BOT_TOKEN", "Discord bot token"),
            ("DISCORD_GUILD_ID", "Discord guild/server ID"),
        ]

        for var_name, description in required_vars:
            value = os.getenv(var_name)
            if not value:
                issues.append(f"Missing {description} ({var_name})")
            elif var_name == "DISCORD_BOT_TOKEN" and len(value) < 50:
                issues.append(f"Discord bot token appears invalid (too short)")

        # Check file permissions
        config_dir = self.config_file.parent
        if not config_dir.exists():
            issues.append("Config directory does not exist")
        elif not os.access(config_dir, os.W_OK):
            issues.append("Config directory is not writable")

        # Check Python version
        import sys
        if sys.version_info < (3, 8):
            issues.append("Python 3.8+ required")

        return len(issues) == 0, issues

    def setup_environment_variables(self, config: SetupConfig) -> None:
        """
        Setup environment variables from configuration.

        Args:
            config: Setup configuration
        """
        if not DOTENV_AVAILABLE:
            print("Warning: python-dotenv not available, skipping .env setup")
            return

        env_vars = {
            "DISCORD_BOT_TOKEN": config.discord_bot_token,
            "DISCORD_GUILD_ID": config.discord_guild_id,
            "DISCORD_CHANNEL_ID": config.discord_channel_id,
            "DATABASE_URL": config.database_url,
            "API_PORT": str(config.api_port),
            "API_HOST": config.api_host,
            "LOG_LEVEL": config.log_level,
            "LOG_FILE": config.log_file,
        }

        for key, value in env_vars.items():
            if value is not None:
                set_key(self.env_file, key, str(value))
                os.environ[key] = str(value)

    def validate_service_dependencies(self, config: SetupConfig) -> Dict[str, List[str]]:
        """
        Validate service dependencies.

        Args:
            config: Setup configuration

        Returns:
            Dictionary mapping service names to missing dependencies
        """
        issues = {}

        for service_name, service_config in config.services.items():
            if not service_config.enabled:
                continue

            missing_deps = []

            # Check dependencies based on service type
            if service_name == "discord_bot":
                if not config.discord_bot_token:
                    missing_deps.append("Discord bot token")
                if not config.discord_guild_id:
                    missing_deps.append("Discord guild ID")

            elif service_name == "database":
                if not config.database_url:
                    missing_deps.append("Database URL")

            elif service_name == "fastapi":
                # Check if required ports are available
                import socket
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    result = sock.connect_ex((config.api_host, config.api_port))
                    sock.close()
                    if result == 0:
                        # Port is in use - this might be okay if service is already running
                        pass
                except Exception:
                    missing_deps.append(f"Cannot check port {config.api_port}")

            if missing_deps:
                issues[service_name] = missing_deps

        return issues

    def create_backup(self) -> Optional[Path]:
        """
        Create backup of current configuration.

        Returns:
            Path to backup file, or None if failed
        """
        if not self.config_file.exists():
            return None

        import time
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        backup_file = self.config_file.with_suffix(f".backup_{timestamp}.json")

        try:
            shutil.copy2(self.config_file, backup_file)
            return backup_file
        except Exception as e:
            print(f"Error creating backup: {e}")
            return None

    def reset_configuration(self) -> bool:
        """
        Reset configuration to defaults.

        Returns:
            True if successful
        """
        try:
            # Create backup first
            backup = self.create_backup()
            if backup:
                print(f"Backup created: {backup}")

            # Reset to defaults
            default_config = SetupConfig()
            self.save_config(default_config)

            # Clear environment variables
            if DOTENV_AVAILABLE and self.env_file.exists():
                # Remove .env file to reset
                self.env_file.unlink(missing_ok=True)

            return True

        except Exception as e:
            print(f"Error resetting configuration: {e}")
            return False

# Global service instance
setup_service = SetupService()

__all__ = [
    "SetupService",
    "SetupConfig",
    "ServiceConfig",
    "setup_service"
]