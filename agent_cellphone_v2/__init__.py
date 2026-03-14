"""Compatibility package for tests expecting `agent_cellphone_v2` at repo root."""

from __future__ import annotations

from typing import Any

from .config import Settings


class AgentCoordinator:
    """Lightweight coordinator used by unit tests."""

    def __init__(self, config_path: str | None = None) -> None:
        self.config_path = config_path
        self.settings = Settings(_env_file=config_path)
        self.coordinator: Any = None
        self._running = False

    async def start(self) -> None:
        self._running = True

    async def stop(self) -> None:
        self._running = False

    def is_running(self) -> bool:
        return self._running

    async def send_message(self, recipient: str, message: str, **kwargs: Any) -> dict[str, Any]:
        _ = (message, kwargs)
        return {"status": "sent", "recipient": recipient}

    async def get_status(self) -> dict[str, Any]:
        return {
            "running": self._running,
            "services": {"messaging": self._running, "api": self._running},
            "version": "2.0.0",
        }


__all__ = ["AgentCoordinator", "Settings"]
