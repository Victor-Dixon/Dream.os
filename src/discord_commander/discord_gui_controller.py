#!/usr/bin/env python3
"""
Discord GUI Controller
======================

SSOT-compatible GUI controller for Discord views/modals.

<!-- SSOT Domain: communication -->
"""

from __future__ import annotations

import logging
from typing import Any

from src.core.messaging_models import MessageCategory

try:
    from .broadcast_modals import AgentMessageModal, BroadcastMessageModal
    from .views.agent_messaging_view import AgentMessagingGUIView
    from .views.main_control_panel_view import MainControlPanelView
    from .views.swarm_status_view import SwarmStatusGUIView
except Exception:  # pragma: no cover - import-safe fallback for non-Discord environments
    class _FallbackView:
        def __init__(self, *_args: Any, **_kwargs: Any) -> None:
            pass

    AgentMessageModal = _FallbackView
    BroadcastMessageModal = _FallbackView
    AgentMessagingGUIView = _FallbackView
    MainControlPanelView = _FallbackView
    SwarmStatusGUIView = _FallbackView

logger = logging.getLogger(__name__)


class DiscordGUIController:
    """Controller for Discord GUI components."""

    def __init__(self, messaging_service: Any) -> None:
        self.messaging_service = messaging_service
        self.logger = logger

    def create_main_gui(self) -> AgentMessagingGUIView:
        return AgentMessagingGUIView(self.messaging_service)

    def create_status_gui(self) -> SwarmStatusGUIView:
        return SwarmStatusGUIView(self.messaging_service)

    def create_control_panel(self) -> MainControlPanelView:
        return MainControlPanelView(self.messaging_service)

    def create_agent_message_modal(self, agent_id: str) -> AgentMessageModal:
        return AgentMessageModal(agent_id, self.messaging_service)

    def create_broadcast_modal(self) -> BroadcastMessageModal:
        return BroadcastMessageModal(self.messaging_service)

    async def send_message(
        self,
        agent_id: str,
        message: str,
        priority: str = "regular",
        stalled: bool = False,
    ) -> bool:
        try:
            result = self.messaging_service.send_message(
                agent=agent_id,
                message=message,
                priority=priority,
                use_pyautogui=True,
                wait_for_delivery=False,
                stalled=stalled,
                discord_user_id="discord",
                apply_template=True,
                message_category=MessageCategory.S2A,
                sender="DISCORD",
            )
            if isinstance(result, dict):
                return bool(result.get("success", False))
            return bool(result)
        except Exception as exc:
            self.logger.exception("Error sending message: %s", exc)
            return False

    async def broadcast_message(self, message: str, priority: str = "regular") -> bool:
        try:
            results = []
            for idx in range(1, 9):
                agent_id = f"Agent-{idx}"
                result = self.messaging_service.send_message(
                    agent=agent_id,
                    message=message,
                    priority=priority,
                    use_pyautogui=True,
                    wait_for_delivery=False,
                    stalled=False,
                    discord_user_id="discord",
                    apply_template=True,
                    message_category=MessageCategory.S2A,
                    sender="DISCORD",
                )
                if isinstance(result, dict):
                    results.append(bool(result.get("success", False)))
                else:
                    results.append(bool(result))
            return all(results)
        except Exception as exc:
            self.logger.exception("Error broadcasting message: %s", exc)
            return False

    def get_agent_status(self) -> dict[str, dict[str, Any]]:
        try:
            from .status_reader import StatusReader

            reader = StatusReader()
            statuses: dict[str, dict[str, Any]] = {}
            for idx in range(1, 9):
                agent_id = f"Agent-{idx}"
                data = reader.get_agent_status(agent_id)
                if data:
                    statuses[agent_id] = data
            return statuses
        except Exception as exc:
            self.logger.exception("Error reading agent status: %s", exc)
            return {}


__all__ = [
    "DiscordGUIController",
    "create_discord_gui_controller",
    "get_discord_gui_controller",
    "AgentMessageModal",
    "BroadcastMessageModal",
    "AgentMessagingGUIView",
    "SwarmStatusGUIView",
    "MainControlPanelView",
]


def create_discord_gui_controller(messaging_service: Any) -> DiscordGUIController:
    """Legacy factory wrapper for GUI controller creation."""
    return DiscordGUIController(messaging_service)


def get_discord_gui_controller(messaging_service: Any) -> DiscordGUIController:
    """Alias kept for older import paths."""
    return create_discord_gui_controller(messaging_service)