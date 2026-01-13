#!/usr/bin/env python3
"""
<!-- SSOT Domain: discord -->

Service Integration Manager
===========================

Manages integration with external services (Thea browser, messaging, GUI).

V2 Compliance | Author: Agent-1 | Date: 2025-12-14
"""

import json
import logging
import os
import time
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.discord_commander.unified_discord_bot import UnifiedDiscordBot

from src.infrastructure.browser.thea_browser_service import TheaBrowserService
from src.core.config.config_dataclasses import BrowserConfig
from src.infrastructure.browser.browser_models import TheaConfig

logger = logging.getLogger(__name__)


class ServiceIntegrationManager:
    """Manages integration with external services."""

    def __init__(self, bot: "UnifiedDiscordBot"):
        """Initialize service integration manager."""
        self.bot = bot
        self.logger = logging.getLogger(__name__)
        self._thea_browser_service: TheaBrowserService | None = None
        self.thea_last_refresh_path = Path("data/thea_last_refresh.json")
        try:
            self.thea_min_interval_minutes = int(
                os.getenv("THEA_MIN_INTERVAL_MINUTES", "60"))
        except ValueError:
            self.thea_min_interval_minutes = 60

    def get_thea_service(self, headless: bool = True) -> TheaBrowserService:
        """Get or create Thea browser service."""
        if self._thea_browser_service:
            return self._thea_browser_service
        browser_cfg = BrowserConfig(headless=headless)
        thea_cfg = TheaConfig()
        self._thea_browser_service = TheaBrowserService(
            config=browser_cfg, thea_config=thea_cfg)
        return self._thea_browser_service

    async def ensure_thea_session(
        self, allow_interactive: bool, min_interval_minutes: int | None = None
    ) -> bool:
        """Self-throttling Thea session ensure."""
        min_interval = min_interval_minutes or self.thea_min_interval_minutes
        last = self._read_last_thea_refresh()
        now = time.time()

        if last and (now - last) < (min_interval * 60):
            self.logger.info(
                f"⏭️  Thea refresh skipped (age {(now - last)/60:.1f}m < {min_interval}m)")
            return True

        # Try headless first
        if await self._try_headless_refresh(now):
            return True

        # Fallback to interactive if allowed
        if allow_interactive:
            return await self._try_interactive_refresh(now)

        return False

    async def _try_headless_refresh(self, now: float) -> bool:
        """Try headless Thea refresh."""
        try:
            svc = self.get_thea_service(headless=True)
            if not svc.initialize():
                self.logger.error("Thea refresh: initialize failed")
                return False
            ok = svc.ensure_thea_authenticated(allow_manual=False)
            svc.close()
            if ok:
                self.logger.info("✅ Thea session refreshed headlessly")
                self._write_last_thea_refresh(now)
                return True
            self.logger.warning("⚠️ Thea headless refresh failed")
        except Exception as e:
            self.logger.error(f"❌ Thea headless refresh error: {e}")
        return False

    async def _try_interactive_refresh(self, now: float) -> bool:
        """Try interactive Thea refresh."""
        try:
            svc = self.get_thea_service(headless=False)
            if not svc.initialize():
                self.logger.error("Thea interactive init failed")
                return False
            ok = svc.ensure_thea_authenticated(allow_manual=True)
            svc.close()
            if ok:
                self.logger.info("✅ Thea session refreshed interactively")
                self._write_last_thea_refresh(now)
                return True
            self.logger.error("❌ Thea interactive refresh failed")
        except Exception as e:
            self.logger.error(f"❌ Thea interactive refresh error: {e}")
        return False

    def _read_last_thea_refresh(self) -> float | None:
        """Read last Thea refresh timestamp."""
        try:
            if self.thea_last_refresh_path.exists():
                data = json.loads(
                    self.thea_last_refresh_path.read_text(encoding="utf-8"))
                return float(data.get("ts"))
        except Exception:
            return None
        return None

    def _write_last_thea_refresh(self, ts: float) -> None:
        """Write last Thea refresh timestamp."""
        try:
            self.thea_last_refresh_path.parent.mkdir(
                parents=True, exist_ok=True)
            self.thea_last_refresh_path.write_text(
                json.dumps({"ts": ts}, indent=2), encoding="utf-8")
        except Exception as e:
            self.logger.warning(f"Could not write Thea last refresh: {e}")
