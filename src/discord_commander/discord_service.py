"""
Discord Service - Devlog Monitoring & Notifications
===================================================

SSOT-backed Discord webhook service for devlogs and status updates.

<!-- SSOT Domain: communication -->
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests

logger = logging.getLogger(__name__)
_discord_service_instance = None


@dataclass
class _AgentEngine:
    async def broadcast_to_all_agents(self, *args: Any, **kwargs: Any):  # pragma: no cover - simple stub
        class Result:
            success = True

        return Result()


class DiscordService:
    """Discord webhook service for devlog monitoring and notifications."""

    def __init__(self, webhook_url: Optional[str] = None) -> None:
        self.webhook_url = webhook_url or self._load_webhook_url()
        self.agent_engine = _AgentEngine()
        self.devlogs_path = Path("devlogs")
        self.last_check_time = datetime.utcnow()
        self.is_running = False
        self.session = requests.Session()
        self.logger = logging.getLogger(__name__)

    def _load_webhook_url(self) -> Optional[str]:
        env_url = os.environ.get("DISCORD_WEBHOOK_URL")
        if env_url:
            return env_url
        config_path = Path("config") / "discord_webhook.json"
        if config_path.exists():
            with open(config_path, "r", encoding="utf-8") as handle:
                data = json.load(handle)
                return data.get("webhook_url")
        return None

    async def start_devlog_monitoring(self, check_interval: float = 60.0) -> None:
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

    async def _check_for_new_devlogs(self) -> None:
        for devlog in self._find_new_devlogs():
            await self._process_devlog(devlog)

    def _find_new_devlogs(self) -> List[Path]:
        if not self.devlogs_path.exists():
            return []
        results = []
        for path in self.devlogs_path.rglob("*.md"):
            try:
                if path.stat().st_mtime > self.last_check_time.timestamp():
                    results.append(path)
            except FileNotFoundError:
                continue
        self.last_check_time = datetime.utcnow()
        return results

    async def _process_devlog(self, devlog_path: Path) -> None:
        with open(devlog_path, "r", encoding="utf-8") as handle:
            content = handle.read()
        metadata = self._parse_devlog_filename(devlog_path.name)
        devlog_data = {
            "title": metadata["title"],
            "description": self._extract_devlog_summary(content),
            "category": metadata["category"],
            "agent": metadata["agent"],
            "filepath": str(devlog_path),
            "timestamp": datetime.utcnow().isoformat(),
        }
        if self.send_devlog_notification(devlog_data):
            await self._notify_agents_of_devlog(devlog_data)

    async def _notify_agents_of_devlog(self, devlog_data: Dict[str, Any]) -> None:
        await self.agent_engine.broadcast_to_all_agents(devlog_data)

    def _parse_devlog_filename(self, filename: str) -> Dict[str, str]:
        stem = Path(filename).stem
        parts = stem.split("_")
        if len(parts) >= 4:
            return {
                "timestamp": f"{parts[0]}_{parts[1]}",
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
        text = (content or "").strip()
        if not text:
            return "V2_SWARM monitoring system - no content provided."
        lines = [line for line in text.splitlines() if line.strip()]
        summary = " ".join(lines[:3])
        return summary if summary else "V2_SWARM monitoring system - summary unavailable."

    def send_devlog_notification(self, devlog_data: Dict[str, Any]) -> bool:
        if not self.webhook_url:
            self.webhook_url = self._load_webhook_url()
        if not self.webhook_url:
            return False
        payload = {
            "embeds": [
                {
                    "title": devlog_data.get("title", "Devlog Update"),
                    "description": devlog_data.get("description", ""),
                    "fields": [
                        {"name": "Agent", "value": devlog_data.get("agent", "Unknown"), "inline": True},
                        {"name": "Category", "value": devlog_data.get("category", "general"), "inline": True},
                    ],
                    "timestamp": devlog_data.get("timestamp"),
                }
            ]
        }
        try:
            response = self.session.post(self.webhook_url, json=payload, timeout=10)
            return response.status_code == 204
        except Exception as exc:
            logger.warning("Devlog notification failed: %s", exc)
            return False

    def send_agent_status_notification(self, agent_status: Dict[str, Any]) -> bool:
        if not self.webhook_url:
            self.webhook_url = self._load_webhook_url()
        if not self.webhook_url:
            return False
        payload = {"content": f"Agent status update: {agent_status}"}
        try:
            response = self.session.post(self.webhook_url, json=payload, timeout=10)
            return response.status_code == 204
        except Exception as exc:
            logger.warning("Agent status notification failed: %s", exc)
            return False

    def send_swarm_coordination_notification(self, coordination_data: Dict[str, Any]) -> bool:
        if not self.webhook_url:
            self.webhook_url = self._load_webhook_url()
        if not self.webhook_url:
            return False
        payload = {"content": coordination_data.get("message", "")}
        try:
            response = self.session.post(self.webhook_url, json=payload, timeout=10)
            return response.status_code == 204
        except Exception as exc:
            logger.warning("Coordination notification failed: %s", exc)
            return False

    def test_webhook_connection(self) -> bool:
        if not self.webhook_url:
            self.webhook_url = self._load_webhook_url()
        if not self.webhook_url:
            return False
        payload = {"content": "Webhook connection test"}
        try:
            response = self.session.post(self.webhook_url, json=payload, timeout=10)
            return response.status_code == 204
        except Exception as exc:
            logger.warning("Webhook connection test failed: %s", exc)
            return False

    def stop_monitoring(self) -> None:
        self.is_running = False

    async def test_integration(self) -> bool:
        if not self.test_webhook_connection():
            return False
        devlog_ok = self.send_devlog_notification({"title": "Integration Test"})
        result = await self.agent_engine.broadcast_to_all_agents({"message": "Integration test broadcast"})
        return devlog_ok and bool(getattr(result, "success", False))


def get_discord_service(webhook_url: Optional[str] = None) -> DiscordService:
    global _discord_service_instance
    if _discord_service_instance is None:
        _discord_service_instance = DiscordService(webhook_url=webhook_url)
    return _discord_service_instance
