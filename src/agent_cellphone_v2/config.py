"""
Configuration management for Agent Cellphone V2.
"""

import os
from pathlib import Path
from typing import List, Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings with environment variable support.

    All settings can be configured via environment variables or .env file.
    """

    # Application settings
    app_name: str = "Agent Cellphone V2"
    app_version: str = "2.0.0"
    debug: bool = Field(default=False)

    # Project paths (no hardcoded paths!)
    project_root: Path = Field(default_factory=lambda: Path(__file__).parent.parent.parent.parent)
    data_dir: Path = Field(default_factory=lambda: Path(__file__).parent.parent.parent.parent / "data")
    logs_dir: Path = Field(default_factory=lambda: Path(__file__).parent.parent.parent.parent / "logs")
    agent_workspaces_dir: Path = Field(default_factory=lambda: Path(__file__).parent.parent.parent.parent / "agent_workspaces")

    # API settings
    api_host: str = Field(default="0.0.0.0")
    api_port: int = Field(default=8001)
    api_workers: int = Field(default=1)

    # Discord settings
    discord_token: Optional[str] = Field(default=None)
    discord_channel_id: Optional[str] = Field(default=None)

    # Database settings
    database_url: str = Field(default="sqlite:///agent_cellphone.db")

    # Agent settings
    max_agents: int = Field(default=8)
    agent_timeout: int = Field(default=30)  # seconds

    # Security settings
    secret_key: str = Field(default_factory=lambda: os.urandom(32).hex())
    allowed_hosts: List[str] = Field(default_factory=lambda: ["localhost", "127.0.0.1"])

    # Logging settings
    log_level: str = Field(default="INFO")
    log_format: str = Field(default="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # GUI/Automation settings
    enable_gui: bool = Field(default=True)
    screenshot_dir: Path = Field(default_factory=lambda: Path(__file__).parent.parent.parent.parent / "screenshots")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_prefix="",
    )

    def setup_directories(self) -> None:
        """Create necessary directories."""
        directories = [
            self.data_dir,
            self.logs_dir,
            self.agent_workspaces_dir,
            self.screenshot_dir,
        ]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

    def get_database_path(self) -> Path:
        """Get full database path."""
        if self.database_url.startswith("sqlite:///"):
            db_path = self.database_url.replace("sqlite:///", "")
            return Path(db_path)
        return Path(self.database_url)

    def validate_config(self) -> List[str]:
        """
        Validate configuration and return list of warnings/errors.

        Returns:
            List of validation messages (warnings/errors)
        """
        warnings = []
        errors = []

        # Check required directories exist or can be created
        for directory in [self.data_dir, self.logs_dir, self.agent_workspaces_dir]:
            if not directory.exists():
                try:
                    directory.mkdir(parents=True, exist_ok=True)
                except Exception as e:
                    errors.append(f"Cannot create directory {directory}: {e}")

        # Check Discord configuration
        if not self.discord_token:
            warnings.append("Discord token not configured - Discord features will be disabled")

        # Check database configuration
        if self.database_url.startswith("sqlite:///"):
            db_path = self.get_database_path()
            if not db_path.parent.exists():
                try:
                    db_path.parent.mkdir(parents=True, exist_ok=True)
                except Exception as e:
                    errors.append(f"Cannot create database directory {db_path.parent}: {e}")

        return errors + warnings