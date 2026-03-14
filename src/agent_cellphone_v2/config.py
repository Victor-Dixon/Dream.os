"""Settings model for Agent Cellphone V2."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Settings:
    """Application settings with a permissive constructor."""

    app_name: str = "Agent Cellphone V2"
    app_version: str = "2.0.0"
    debug: bool = False
    api_host: str = "127.0.0.1"
    api_port: int = 8000
    api_workers: int = 1
    log_level: str = "INFO"
    current_agent: str = "Agent-4"

    def __init__(self, _env_file: str | None = None, **kwargs: object) -> None:
        self.app_name = str(kwargs.get("app_name", "Agent Cellphone V2"))
        self.app_version = str(kwargs.get("app_version", "2.0.0"))
        self.debug = bool(kwargs.get("debug", False))
        self.api_host = str(kwargs.get("api_host", "127.0.0.1"))
        self.api_port = int(kwargs.get("api_port", 8000))
        self.api_workers = int(kwargs.get("api_workers", 1))
        self.log_level = str(kwargs.get("log_level", "INFO"))
        self.current_agent = str(kwargs.get("current_agent", "Agent-4"))
        _ = _env_file
