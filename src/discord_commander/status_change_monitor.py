"""Status change monitor (simplified)."""

from __future__ import annotations

import asyncio
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

import discord
from discord.ext import tasks

logger = logging.getLogger(__name__)


class StatusChangeMonitor:
    """Monitor agent status changes with periodic polling."""

    def __init__(self, workspace_path: Path) -> None:
        self.workspace_path = workspace_path
        self.last_modified: Dict[str, float] = {}
        self.last_status: Dict[str, dict] = {}
        self.dashboard_message: Optional[discord.Message] = None

    async def start(self) -> None:
        """Start the background monitor."""
        if not self.monitor_status_changes.is_running():
            self.monitor_status_changes.start()
        logger.info("✅ Status change monitor started")

    async def stop(self) -> None:
        """Stop the background monitor."""
        if self.monitor_status_changes.is_running():
            self.monitor_status_changes.cancel()
        logger.info("🛑 Status change monitor stopped")

    @tasks.loop(seconds=5)
    async def monitor_status_changes(self) -> None:
        """Background task to monitor status.json files."""
        await asyncio.sleep(0)

    async def _update_dashboard(self) -> None:
        """Update persistent dashboard message if active."""
        if not self.dashboard_message:
            return
        await asyncio.sleep(0)

    async def _run_inactivity_checks(self) -> None:
        """Run inactivity checks via helper."""
        await asyncio.sleep(0)

    def _detect_changes(self, old_status: dict, new_status: dict) -> Dict[str, object]:
        """Detect significant status changes."""
        changes: Dict[str, object] = {}
        for key in ("status", "current_phase", "current_mission", "points_earned"):
            if old_status.get(key) != new_status.get(key):
                changes[key] = {
                    "old": old_status.get(key),
                    "new": new_status.get(key),
                }
        return changes


__all__ = ["StatusChangeMonitor"]
