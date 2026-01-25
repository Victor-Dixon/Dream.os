#!/usr/bin/env python3
"""
Discord GUI Controller
======================

<!-- SSOT Domain: discord -->

Thin controller for GUI composition and messaging operations.
"""

from __future__ import annotations

import logging
from typing import Any

from src.core.messaging_models import MessageCategory

from .broadcast_modals import AgentMessageModal, BroadcastMessageModal
from .views.agent_messaging_view import AgentMessagingGUIView
from .views.main_control_panel_view import MainControlPanelView
from .views.swarm_status_view import SwarmStatusGUIView
from .status_reader import StatusReader

logger = logging.getLogger(__name__)


class DiscordGUIController:
    """Coordinator for Discord GUI views and messaging actions."""

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
                discord_user_id=None,
                apply_template=True,
                message_category=MessageCategory.S2A,
                sender="DISCORD",
            )
            return bool(result.get("success", False))
        except Exception:
            self.logger.exception("Failed to send message")
            return False

    async def broadcast_message(self, message: str, priority: str = "regular") -> bool:
        try:
            agents = [f"Agent-{i}" for i in range(1, 9)]
            results = []
            for agent_id in agents:
                result = self.messaging_service.send_message(
                    agent=agent_id,
                    message=message,
                    priority=priority,
                    use_pyautogui=True,
                    wait_for_delivery=False,
                    stalled=False,
                    discord_user_id=None,
                    apply_template=True,
                    message_category=MessageCategory.S2A,
                    sender="DISCORD",
                )
                results.append(bool(result.get("success", False)))
            return all(results)
        except Exception:
            self.logger.exception("Broadcast failed")
            return False

    def get_agent_status(self) -> dict[str, dict[str, Any]]:
        try:
            status_reader = StatusReader()
            statuses: dict[str, dict[str, Any]] = {}
            for i in range(1, 9):
                agent_id = f"Agent-{i}"
                status = status_reader.get_agent_status(agent_id)
                if status:
                    statuses[agent_id] = status
            return statuses
        except Exception:
            self.logger.exception("Failed to get agent status")
            return {}


__all__ = [
    "DiscordGUIController",
    "AgentMessageModal",
    "BroadcastMessageModal",
    "AgentMessagingGUIView",
    "SwarmStatusGUIView",
    "MainControlPanelView",
]
