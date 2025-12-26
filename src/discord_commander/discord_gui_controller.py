#!/usr/bin/env python3
"""
Discord GUI Controller - Facade Pattern
========================================

<!-- SSOT Domain: web -->

Lightweight facade for Discord GUI components.
Consolidates Discord GUI functionality into a clean, simple interface.

Author: Agent-7 (Repository Cloning Specialist) - V2 Compliance Refactor (Facade Pattern)
Original: Agent-3 (Infrastructure & DevOps)
License: MIT
"""

import asyncio
import logging
from typing import Any

from src.core.messaging_models_core import MessageCategory
from src.services.unified_messaging_service import UnifiedMessagingService

from .discord_gui_modals import AgentMessageModal, BroadcastMessageModal
from .views import (
    AgentMessagingGUIView,
    SwarmStatusGUIView,
    HelpGUIView,
    MainControlPanelView,
)

logger = logging.getLogger(__name__)


class DiscordGUIController:
    """
    Unified Discord GUI Controller for Agent Messaging System (Facade Pattern).

    Provides complete Discord-based access to:
    - Agent-to-agent messaging
    - Swarm status monitoring
    - Broadcast communications
    - Interactive GUI (views, modals, buttons)

    This is a lightweight facade that delegates to specialized components:
    - views/: UI views (AgentMessagingGUIView, SwarmStatusGUIView)
    - discord_gui_modals.py: UI modals (AgentMessageModal, BroadcastMessageModal)
    """

    def __init__(self, messaging_service: UnifiedMessagingService):
        """Initialize Discord GUI controller."""
        self.messaging_service = messaging_service
        self.logger = logging.getLogger(__name__)

    def create_main_gui(self) -> AgentMessagingGUIView:
        """Create main messaging GUI view."""
        return AgentMessagingGUIView(self.messaging_service)

    def create_status_gui(self) -> SwarmStatusGUIView:
        """Create status monitoring GUI view."""
        return SwarmStatusGUIView(self.messaging_service)

    def create_control_panel(self) -> MainControlPanelView:
        """Create main control panel view."""
        return MainControlPanelView(self.messaging_service)

    def create_agent_message_modal(self, agent_id: str) -> AgentMessageModal:
        """Create modal for messaging specific agent."""
        return AgentMessageModal(agent_id, self.messaging_service)

    def create_broadcast_modal(self) -> BroadcastMessageModal:
        """Create modal for broadcasting to all agents."""
        return BroadcastMessageModal(self.messaging_service)

    async def send_message(
        self,
        agent_id: str,
        message: str,
        priority: str = "regular",
        stalled: bool = False,
        discord_user=None,
    ) -> bool:
        """Send message to specific agent via PyAutoGUI chat input coordinates."""
        try:
            sender = (
                f"Discord User ({getattr(discord_user, 'name', '')})"
                if discord_user
                else "Discord GUI"
            )
            discord_user_id = str(getattr(discord_user, "id", "")) if discord_user else None

            result = self.messaging_service.send_message(
                agent=agent_id, 
                message=message, 
                priority=priority, 
                use_pyautogui=True,
                wait_for_delivery=False,  # Don't wait - queue processor will handle delivery
                stalled=stalled,
                discord_user_id=discord_user_id,
                apply_template=True,
                message_category=MessageCategory.D2A,
                sender=sender,
            )
            return result.get("success", False)
        except Exception as e:
            self.logger.error(f"Error sending message: {e}")
            return False

    async def broadcast_message(
        self,
        message: str,
        priority: str = "regular",
        discord_user=None,
    ) -> bool:
        """Broadcast message to all agents via PyAutoGUI chat input coordinates."""
        try:
            agents = [f"Agent-{i}" for i in range(1, 9)]
            success_count = 0
            sender = (
                f"Discord User ({getattr(discord_user, 'name', '')})"
                if discord_user
                else "Discord GUI"
            )
            discord_user_id = str(getattr(discord_user, "id", "")) if discord_user else None

            # Delay between agents to prevent race conditions and routing problems
            # Queue operations need time to process and prevent conflicts
            INTER_AGENT_QUEUE_DELAY = 0.5  # 500ms delay between queue operations

            for agent in agents:
                result = self.messaging_service.send_message(
                    agent=agent, 
                    message=message, 
                    priority=priority, 
                    use_pyautogui=True,
                    wait_for_delivery=False,  # Don't wait - queue processor will handle delivery
                    discord_user_id=discord_user_id,
                    apply_template=True,
                    message_category=MessageCategory.D2A,
                    sender=sender,
                )
                if result.get("success"):
                    success_count += 1
                
                # Add delay between agents to prevent race conditions in queue routing
                if agent != agents[-1]:  # Don't delay after the last agent
                    await asyncio.sleep(INTER_AGENT_QUEUE_DELAY)

            return success_count == len(agents)
        except Exception as e:
            self.logger.error(f"Error broadcasting: {e}")
            return False

    def get_agent_status(self) -> dict[str, Any]:
        """Get current swarm status."""
        from .status_reader import StatusReader

        try:
            status_reader = StatusReader()
            agents_status = {}

            for i in range(1, 9):
                agent_id = f"Agent-{i}"
                status = status_reader.get_agent_status(agent_id)
                if status:
                    agents_status[agent_id] = status

            return agents_status
        except Exception as e:
            self.logger.error(f"Error getting status: {e}")
            return {}


__all__ = [
    "DiscordGUIController",
    "AgentMessagingGUIView",
    "SwarmStatusGUIView",
    "HelpGUIView",
    "MainControlPanelView",
    "AgentMessageModal",
    "BroadcastMessageModal",
]
