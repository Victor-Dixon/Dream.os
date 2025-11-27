#!/usr/bin/env python3
"""
Chat Presence Orchestrator
==========================

Unified orchestrator for chat presence system.
Coordinates Twitch, Discord, OBS caption integration.

V2 Compliance: <400 lines, single responsibility
Author: Agent-7 (Web Development Specialist)
License: MIT
"""

import asyncio
import logging
from typing import Optional

from .agent_personality import format_chat_message, get_personality
from .chat_scheduler import ChatScheduler
from .message_interpreter import MessageInterpreter
from .twitch_bridge import TwitchChatBridge
from ...core.messaging_core import send_message
from ...core.messaging_models_core import (
    UnifiedMessagePriority,
    UnifiedMessageTag,
    UnifiedMessageType,
)
from ...obs.caption_interpreter import CaptionInterpreter, InterpretedCaption
from ...obs.caption_listener import OBSCaptionListener
from ...obs.speech_log_manager import SpeechLogManager

logger = logging.getLogger(__name__)


class ChatPresenceOrchestrator:
    """
    Orchestrates chat presence system.

    Manages:
    - Twitch chat connection
    - Discord chat connection (extended)
    - OBS caption listening
    - Agent response coordination
    """

    def __init__(
        self,
        twitch_config: Optional[dict] = None,
        obs_config: Optional[dict] = None,
    ):
        """
        Initialize chat presence orchestrator.

        Args:
            twitch_config: Twitch configuration dict
            obs_config: OBS configuration dict
        """
        self.twitch_config = twitch_config or {}
        self.obs_config = obs_config or {}

        # Initialize components
        self.message_interpreter = MessageInterpreter()
        self.chat_scheduler = ChatScheduler()
        self.caption_interpreter = CaptionInterpreter()
        self.speech_log_manager = SpeechLogManager()

        # Bridges (initialized on start)
        self.twitch_bridge: Optional[TwitchChatBridge] = None
        self.obs_listener: Optional[OBSCaptionListener] = None

        self.running = False

    async def start(self) -> bool:
        """
        Start chat presence system.

        Returns:
            True if started successfully
        """
        logger.info("🚀 Starting Chat Presence Orchestrator...")

        # Start Twitch bridge
        if self.twitch_config:
            success = await self._start_twitch()
            if not success:
                logger.warning("⚠️ Twitch bridge failed to start")

        # Start OBS listener
        if self.obs_config:
            success = await self._start_obs()
            if not success:
                logger.warning("⚠️ OBS listener failed to start")

        self.running = True
        logger.info("✅ Chat Presence Orchestrator started")
        return True

    async def _start_twitch(self) -> bool:
        """Start Twitch bridge."""
        try:
            self.twitch_bridge = TwitchChatBridge(
                username=self.twitch_config.get("username", ""),
                oauth_token=self.twitch_config.get("oauth_token", ""),
                channel=self.twitch_config.get("channel", ""),
                on_message=self._handle_twitch_message,
            )

            return await self.twitch_bridge.connect()

        except Exception as e:
            logger.error(f"❌ Failed to start Twitch bridge: {e}")
            return False

    async def _start_obs(self) -> bool:
        """Start OBS caption listener."""
        try:
            self.obs_listener = OBSCaptionListener(
                host=self.obs_config.get("host", "localhost"),
                port=self.obs_config.get("port", 4455),
                password=self.obs_config.get("password"),
                on_caption=self._handle_obs_caption,
            )

            # Start listener in background
            asyncio.create_task(self.obs_listener.listen())
            return True

        except Exception as e:
            logger.error(f"❌ Failed to start OBS listener: {e}")
            return False

    async def _handle_twitch_message(self, message_data: dict) -> None:
        """
        Handle incoming Twitch chat message.

        Args:
            message_data: Message data dictionary
        """
        message = message_data.get("message", "")
        username = message_data.get("username", "")

        logger.info(f"💬 Twitch message from {username}: {message[:50]}...")

        # Determine which agent should respond
        agent_id = self.message_interpreter.determine_responder(
            message, username, "twitch"
        )

        if not agent_id:
            return

        # Handle broadcast
        if agent_id == "BROADCAST":
            await self._handle_broadcast(message, "twitch")
            return

        # Check if agent can speak
        if not self.chat_scheduler.can_agent_speak(agent_id):
            logger.debug(f"⏸️ {agent_id} on cooldown, skipping response")
            return

        # Generate response
        response = await self._generate_agent_response(agent_id, message)

        if response:
            # Send response
            await self.twitch_bridge.send_as_agent(agent_id, response)

            # Record activity
            self.chat_scheduler.record_agent_response(agent_id)

    async def _handle_obs_caption(self, caption_data: dict) -> None:
        """
        Handle OBS caption event.

        Args:
            caption_data: Caption data dictionary
        """
        caption_text = caption_data.get("text", "")

        logger.info(f"🎤 OBS caption: {caption_text[:50]}...")

        # Interpret caption
        interpreted = self.caption_interpreter.interpret(caption_text)

        # Log caption
        self.speech_log_manager.log_caption(
            caption_text, interpreted.__dict__, destination="both"
        )

        # Route based on interpretation
        await self._route_interpreted_caption(interpreted)

    async def _route_interpreted_caption(self, interpreted: InterpretedCaption) -> None:
        """
        Route interpreted caption to appropriate handler.

        Args:
            interpreted: Interpreted caption
        """
        target_agents = interpreted.target_agents
        action_type = interpreted.action_type

        # If no target agents, broadcast
        if not target_agents:
            target_agents = [
                "Agent-1",
                "Agent-2",
                "Agent-3",
                "Agent-4",
                "Agent-5",
                "Agent-6",
                "Agent-7",
                "Agent-8",
            ]

        # Route based on action type
        if action_type == "message":
            await self._send_agent_messages(
                target_agents, interpreted.normalized_text
            )
        elif action_type == "task":
            await self._assign_task(target_agents, interpreted.normalized_text)
        elif action_type == "devlog":
            # Already logged by speech_log_manager
            pass
        elif action_type == "tool":
            await self._trigger_tool(interpreted.tool_name, target_agents)

    async def _generate_agent_response(
        self, agent_id: str, message: str
    ) -> Optional[str]:
        """
        Generate agent response.

        Args:
            agent_id: Agent identifier
            message: Original message

        Returns:
            Agent response text or None
        """
        # For now, simple echo with personality
        # Future: Integrate with LLM for intelligent responses
        personality = get_personality(agent_id)
        if not personality:
            return None

        # Simple response generation
        response = f"Received: {message[:100]}"

        # Apply personality formatting
        return format_chat_message(agent_id, response)

    async def _handle_broadcast(self, message: str, channel: str) -> None:
        """
        Handle broadcast message.

        Args:
            message: Message content
            channel: Channel name
        """
        # Send to all agents via messaging core
        for agent_id in [
            "Agent-1",
            "Agent-2",
            "Agent-3",
            "Agent-4",
            "Agent-5",
            "Agent-6",
            "Agent-7",
            "Agent-8",
        ]:
            send_message(
                content=message,
                sender="HUMAN",
                recipient=agent_id,
                message_type=UnifiedMessageType.HUMAN_TO_AGENT,
                priority=UnifiedMessagePriority.REGULAR,
                tags=[UnifiedMessageTag.COORDINATION],
            )

    async def _send_agent_messages(self, agent_ids: list[str], content: str) -> None:
        """Send messages to agents."""
        for agent_id in agent_ids:
            send_message(
                content=content,
                sender="HUMAN",
                recipient=agent_id,
                message_type=UnifiedMessageType.HUMAN_TO_AGENT,
                priority=UnifiedMessagePriority.REGULAR,
            )

    async def _assign_task(self, agent_ids: list[str], task_description: str) -> None:
        """Assign task to agents."""
        for agent_id in agent_ids:
            send_message(
                content=f"Task: {task_description}",
                sender="HUMAN",
                recipient=agent_id,
                message_type=UnifiedMessageType.HUMAN_TO_AGENT,
                priority=UnifiedMessagePriority.REGULAR,
            )

    async def _trigger_tool(
        self, tool_name: Optional[str], agent_ids: list[str]
    ) -> None:
        """Trigger tool execution."""
        if not tool_name:
            return

        # Notify agents about tool trigger
        for agent_id in agent_ids:
            send_message(
                content=f"Tool trigger: {tool_name}",
                sender="SYSTEM",
                recipient=agent_id,
                message_type=UnifiedMessageType.SYSTEM_TO_AGENT,
                priority=UnifiedMessagePriority.REGULAR,
            )

    async def stop(self) -> None:
        """Stop chat presence system."""
        self.running = False

        if self.twitch_bridge:
            self.twitch_bridge.stop()

        if self.obs_listener:
            await self.obs_listener.disconnect()

        logger.info("🛑 Chat Presence Orchestrator stopped")


__all__ = ["ChatPresenceOrchestrator"]

