"""Status change monitor (simplified)."""

from __future__ import annotations

import asyncio
import importlib
import importlib.util
import logging
import sys
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional

from src.core.messaging_core import MessageCategory
from src.core.messaging_models import UnifiedMessage, UnifiedMessagePriority, UnifiedMessageType
from src.core.messaging_templates import render_message

logger = logging.getLogger(__name__)


class _FallbackLoop:
    """Minimal loop shim for test environments without discord.ext.tasks."""

    def __init__(self, coro: Callable[..., object]) -> None:
        self._coro = coro
        self._running = False

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return _BoundFallbackLoop(self, instance)

    def _run(self, instance):
        return self._coro(instance)


class _BoundFallbackLoop:
    def __init__(self, loop_obj: _FallbackLoop, instance) -> None:
        self._loop_obj = loop_obj
        self._instance = instance

    def is_running(self) -> bool:
        return self._loop_obj._running

    def start(self) -> None:
        self._loop_obj._running = True

    def cancel(self) -> None:
        self._loop_obj._running = False

    async def __call__(self):
        await self._loop_obj._run(self._instance)


def _loop(seconds: int):
    """Resolve discord task loop decorator with fallback for tests."""
    tasks_mod = None
    discord_module_loaded = "discord" in sys.modules
    discord_spec = importlib.util.find_spec("discord") if not discord_module_loaded else True
    tasks_spec = (
        importlib.util.find_spec("discord.ext.tasks")
        if (not discord_module_loaded and discord_spec)
        else None
    )
    if discord_module_loaded and hasattr(sys.modules["discord"], "ext"):
        tasks_mod = getattr(sys.modules["discord"].ext, "tasks", None)
    elif discord_spec and tasks_spec:
        tasks_mod = importlib.import_module("discord.ext.tasks")
    if tasks_mod is not None and hasattr(tasks_mod, "loop"):
        return tasks_mod.loop(seconds=seconds)

    def decorator(coro: Callable[..., object]) -> _FallbackLoop:
        return _FallbackLoop(coro)

    return decorator


@dataclass
class _DeliveryMessage:
    recipient: str
    content: str
    metadata: dict


class StatusChangeMonitor:
    """Monitor agent status changes with periodic polling."""

    def __init__(
        self,
        workspace_path: Path | None = None,
        bot=None,
        channel_id: int | None = None,
        scheduler=None,
    ) -> None:
        self.workspace_path = workspace_path or Path(".")
        self.bot = bot
        self.channel_id = channel_id
        self.scheduler = scheduler
        self.last_modified: Dict[str, float] = {}
        self.last_status: Dict[str, dict] = {}
        self.dashboard_message: Optional[object] = None

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

    @_loop(seconds=5)
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

    async def _send_resume_message_to_agent(
        self,
        agent_id: str,
        prompt: str,
        summary,
        skip_wrapper: bool = False,
    ) -> bool:
        """Send a SWARM_PULSE resume prompt via PyAutoGUI delivery."""
        from src.core.messaging_pyautogui import PyAutoGUIMessagingDelivery

        inactivity = getattr(summary, "inactivity_duration_minutes", "unknown")
        context = f"Inactivity detected: {inactivity} minutes"
        template_message = UnifiedMessage(
            content=prompt,
            sender="SYSTEM",
            recipient=agent_id,
            message_type=UnifiedMessageType.SYSTEM_TO_AGENT,
            priority=UnifiedMessagePriority.URGENT,
            tags=[],
            metadata={},
            category=MessageCategory.S2A,
        )
        rendered = render_message(
            template_message,
            template_key="SWARM_PULSE",
            context=context,
            actions="Resume by producing an artifact.",
            fallback="Escalate if blocked.",
            fsm_state="UNKNOWN",
            current_mission="Resume execution",
            time_since_update=context,
            next_task="Check assigned inbox task",
            task_priority="urgent",
            task_points="0",
            task_status="assigned",
        )
        message = _DeliveryMessage(
            recipient=agent_id,
            content=rendered if not skip_wrapper else prompt,
            metadata={
                "use_pyautogui": True,
                "message_category": MessageCategory.S2A.value,
            },
        )
        delivery = PyAutoGUIMessagingDelivery()
        return await asyncio.to_thread(delivery.send_message, message)


__all__ = ["StatusChangeMonitor"]
