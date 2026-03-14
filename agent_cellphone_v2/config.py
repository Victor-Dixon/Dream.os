"""Compatibility settings for top-level `agent_cellphone_v2` package."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Settings:
    agent_id: str = "default"
    mode: str = "NORMAL"
    timeout: float = 30.0

    def __init__(self, _env_file: str | None = None, **kwargs: object) -> None:
        self.agent_id = str(kwargs.get("agent_id", "default"))
        self.mode = str(kwargs.get("mode", "NORMAL"))
        self.timeout = float(kwargs.get("timeout", 30.0))
        _ = _env_file
