#!/usr/bin/env python3
"""
Discord Service
===============

<!-- SSOT Domain: discord -->

Lightweight Discord webhook + devlog monitoring service used by tests and
legacy integrations.
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import requests

logger = logging.getLogger(__name__)


@dataclass
class _BroadcastResult:
    success: bool


class _AgentEngine:
    async def broadcast_to_all_agents(self, message: str) -> _BroadcastResult:
        return _BroadcastResult(success=True)


class DiscordService:
    """Service for posting devlog and status notifications via webhook."""

    def __init__(self, webhook_url: str | None = None) -> None:
        self.webhook_url = webhook_url or self._load_webhook_url()
        self.agent_engine = _AgentEngine()
        self.devlogs_path = Path("devlogs")
        self.is_running = False
        self.session = requests.Session()
        self.last_check_time = datetime.utcnow()

    def _load_webhook_url(self) -> str | None:
        env_url = os.getenv("DISCORD_WEBHOOK_URL")
        if env_url:
            return env_url

        config_path = Path("config") / "discord_webhook.json"
        if config_path.exists():
            try:
                with config_path.open("r", encoding="utf-8") as handle:
                    payload = json.load(handle)
                return payload.get("webhook_url")
            except Exception:
                logger.exception("Failed to load webhook config")
        return None

    async def start_devlog_monitoring(self, check_interval: float = 5.0) -> None:
        if not self.devlogs_path.exists():
            self.is_running = False
            return

        if not self.test_webhook_connection():
            self.is_running = False
            return

        self.is_running = True
        while self.is_running:
            await self._check_for_new_devlogs()
            await asyncio.sleep(check_interval)

    def stop_monitoring(self) -> None:
        self.is_running = False

    async def _check_for_new_devlogs(self) -> None:
        devlogs = self._find_new_devlogs()
        for devlog in devlogs:
            await self._process_devlog(devlog)
        if devlogs:
            self.last_check_time = datetime.utcnow()

    def _find_new_devlogs(self) -> list[Path]:
        if not self.devlogs_path.exists():
            return []
        new_logs = []
        for path in self.devlogs_path.rglob("*.md"):
            try:
                if path.stat().st_mtime > self.last_check_time.timestamp():
                    new_logs.append(path)
            except FileNotFoundError:
                continue
        return new_logs

    async def _process_devlog(self, devlog_path: Path) -> None:
        try:
            content = devlog_path.read_text(encoding="utf-8")
        except Exception:
            logger.exception("Failed to read devlog")
            return

        data = self._parse_devlog_filename(devlog_path.name)
        data.update(
            {
                "title": data.get("title", devlog_path.stem),
                "description": self._extract_devlog_summary(content),
                "filepath": str(devlog_path),
                "timestamp": datetime.utcnow().isoformat(),
            }
        )

        if self.send_devlog_notification(data):
            await self._notify_agents_of_devlog(data)

    async def _notify_agents_of_devlog(self, devlog_data: dict[str, Any]) -> None:
        try:
            result = await self.agent_engine.broadcast_to_all_agents(
                f"Devlog update: {devlog_data.get('title', 'Devlog')}"
            )
            return result
        except Exception:
            logger.exception("Failed to notify agents")

    def _parse_devlog_filename(self, filename: str) -> dict[str, str]:
        stem = Path(filename).stem
        parts = stem.split("_")
        if len(parts) >= 4:
            return {
                "timestamp": "_".join(parts[:2]),
                "category": parts[2],
                "agent": parts[3],
                "title": "_".join(parts[4:]) or stem,
            }
        return {
            "timestamp": "unknown",
            "category": "general",
            "agent": "Unknown",
            "title": stem,
        }

    def _extract_devlog_summary(self, content: str) -> str:
        if not content:
            return "V2_SWARM monitoring system: No summary available."
        cleaned = content.strip().replace("\n", " ")
        summary = cleaned[:200]
        return f"Summary: {summary}"

    def send_devlog_notification(self, devlog_data: dict[str, Any]) -> bool:
        if not self.webhook_url:
            self.webhook_url = self._load_webhook_url()
        if not self.webhook_url:
            return False

        payload = {
            "content": f"New DevLog: {devlog_data.get('title', 'Devlog')}",
            "embeds": [
                {
                    "title": devlog_data.get("title", "Devlog"),
                    "description": devlog_data.get("description", ""),
                    "fields": [
                        {"name": "Agent", "value": devlog_data.get("agent", "Unknown"), "inline": True},
                        {"name": "Category", "value": devlog_data.get("category", "general"), "inline": True},
                        {"name": "File", "value": devlog_data.get("filepath", ""), "inline": False},
                    ],
                }
            ],
        }

        try:
            response = self.session.post(self.webhook_url, json=payload, timeout=10)
            return response.status_code == 204
        except Exception:
            logger.exception("Failed to send devlog notification")
            return False

    def send_agent_status_notification(self, agent_status: dict[str, Any]) -> bool:
        if not self.webhook_url:
            self.webhook_url = self._load_webhook_url()
        if not self.webhook_url:
            return False

        payload = {
            "content": "Agent Status Update",
            "embeds": [
                {
                    "title": f"Status: {agent_status.get('agent_id', 'Agent')}",
                    "description": json.dumps(agent_status, indent=2),
                }
            ],
        }
        try:
            response = self.session.post(self.webhook_url, json=payload, timeout=10)
            return response.status_code == 204
        except Exception:
            logger.exception("Failed to send agent status notification")
            return False

    def send_swarm_coordination_notification(self, coordination_data: dict[str, Any]) -> bool:
        if not self.webhook_url:
            self.webhook_url = self._load_webhook_url()
        if not self.webhook_url:
            return False

        payload = {
            "content": "Swarm Coordination Update",
            "embeds": [
                {
                    "title": "Coordination",
                    "description": json.dumps(coordination_data, indent=2),
                }
            ],
        }
        try:
            response = self.session.post(self.webhook_url, json=payload, timeout=10)
            return response.status_code == 204
        except Exception:
            logger.exception("Failed to send coordination notification")
            return False

    def test_webhook_connection(self) -> bool:
        if not self.webhook_url:
            self.webhook_url = self._load_webhook_url()
        if not self.webhook_url:
            return False

        payload = {"content": "Webhook test"}
        try:
            response = self.session.post(self.webhook_url, json=payload, timeout=10)
            return response.status_code == 204
        except Exception:
            logger.exception("Webhook test failed")
            return False

    async def test_integration(self) -> bool:
        if not self.test_webhook_connection():
            return False
        test_result = await self.agent_engine.broadcast_to_all_agents("Integration test")
        return bool(getattr(test_result, "success", False))


_discord_service_instance: DiscordService | None = None


def get_discord_service(webhook_url: str | None = None) -> DiscordService:
    global _discord_service_instance
    if _discord_service_instance is None:
        _discord_service_instance = DiscordService(webhook_url=webhook_url)
    elif webhook_url:
        _discord_service_instance.webhook_url = webhook_url
    return _discord_service_instance


__all__ = ["DiscordService", "get_discord_service"]
