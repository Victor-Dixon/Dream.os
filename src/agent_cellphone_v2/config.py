"""
Configuration management for Agent Cellphone V2.
"""

import os
from pathlib import Path
from typing import List, Optional
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings with environment variable support.

    All settings can be configured via environment variables or .env file.
    """

    # Application settings
    app_name: str = "Agent Cellphone V2"
    app_version: str = "2.0.0"
    debug: bool = Field(default=False, env="DEBUG")

    # Project paths (no hardcoded paths!)
    project_root: Path = Field(default_factory=lambda: Path(__file__).parent.parent.parent.parent)
    data_dir: Path = Field(default_factory=lambda: Path(__file__).parent.parent.parent.parent / "data")
    logs_dir: Path = Field(default_factory=lambda: Path(__file__).parent.parent.parent.parent / "logs")
    agent_workspaces_dir: Path = Field(default_factory=lambda: Path(__file__).parent.parent.parent.parent / "agent_workspaces")

    # API settings
    api_host: str = Field(default="0.0.0.0", env="API_HOST")
    api_port: int = Field(default=8001, env="API_PORT")
    api_workers: int = Field(default=1, env="API_WORKERS")

    # Discord settings
    discord_token: Optional[str] = Field(default=None, env="DISCORD_TOKEN")
    discord_channel_id: Optional[str] = Field(default=None, env="DISCORD_CHANNEL_ID")

    # Database settings
    database_url: str = Field(default="sqlite:///agent_cellphone.db", env="DATABASE_URL")

    # Agent settings
    max_agents: int = Field(default=8, env="MAX_AGENTS")
    agent_timeout: int = Field(default=30, env="AGENT_TIMEOUT")  # seconds

    # Security settings
    secret_key: str = Field(default_factory=lambda: os.urandom(32).hex(), env="SECRET_KEY")
    allowed_hosts: List[str] = Field(default_factory=lambda: ["localhost", "127.0.0.1"], env="ALLOWED_HOSTS")

    # Logging settings
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_format: str = Field(default="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # GUI/Automation settings
    enable_gui: bool = Field(default=True, env="ENABLE_GUI")
    screenshot_dir: Path = Field(default_factory=lambda: Path(__file__).parent.parent.parent.parent / "screenshots")

    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

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