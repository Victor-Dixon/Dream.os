#!/usr/bin/env python3
"""
Chat Presence Orchestrator V2 - Agent Cellphone V2
=================================================

SSOT Domain: integration

Refactored chat presence orchestrator using extracted coordinators.
Replaces the original 840-line monolithic implementation.

Features:
- Modular architecture with separated concerns
- Twitch, OBS, and agent coordination via dedicated coordinators
- V2 compliance: <400 lines, single responsibility
- Maintains all original functionality through coordinator delegation

V2 Compliant: <400 lines, modular architecture
Author: Agent-6 (Coordination & Communication Specialist)
Date: 2026-01-08
"""

import asyncio
import logging
from typing import Optional, Dict, Any, List
from datetime import datetime

from src.core.base.base_service import BaseService
from .chat_config_manager import ChatConfigManager
from .twitch_coordinator import TwitchCoordinator
from .obs_coordinator import OBSCoordinator
from .agent_coordinator import AgentCoordinator

logger = logging.getLogger(__name__)


class ChatPresenceOrchestratorV2(BaseService):
    """
    V2 Refactored Chat Presence Orchestrator.

    Coordinates between specialized coordinators:
    - ChatConfigManager: Configuration management
    - TwitchCoordinator: Twitch chat operations
    - OBSCoordinator: OBS caption integration
    - AgentCoordinator: Agent response coordination
    """

    def __init__(
        self,
        twitch_config: Optional[Dict[str, Any]] = None,
        obs_config: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize chat presence orchestrator V2.

        Args:
            twitch_config: Twitch configuration dict
            obs_config: OBS configuration dict
        """
        super().__init__("ChatPresenceOrchestratorV2")

        # Initialize system components
        self._initialize_components(twitch_config, obs_config)

    def _initialize_components(self, twitch_config: Optional[Dict[str, Any]], obs_config: Optional[Dict[str, Any]]) -> None:
        """Initialize all system components."""
        # Initialize configuration manager
        self.config_manager = ChatConfigManager()

        # Load and validate configurations
        if twitch_config is None:
            twitch_config = self.config_manager.load_twitch_config_from_env()
        if obs_config is None:
            obs_config = self.config_manager.load_obs_config_from_env()

        self.twitch_config = twitch_config if self.config_manager.validate_twitch_config(twitch_config) else {}
        self.obs_config = obs_config if self.config_manager.validate_obs_config(obs_config) else {}

        # Initialize coordinators
        self.twitch_coordinator = TwitchCoordinator(self.twitch_config)
        self.obs_coordinator = OBSCoordinator(self.obs_config)
        self.agent_coordinator = AgentCoordinator()

        # System state
        self.running = False
        self._status_update_task: Optional[asyncio.Task] = None
        self._message_processing_task: Optional[asyncio.Task] = None

        # Initialize legacy compatibility attributes
        self._initialize_admin_users()

    def _initialize_admin_users(self) -> None:
        """Initialize admin users from configuration."""
        self.admin_users = set()
        channel_owner = self.twitch_config.get("channel", "").lstrip("#").lower()
        if channel_owner:
            self.admin_users.add(channel_owner)
        admin_list = self.twitch_config.get("admin_users", [])
        if isinstance(admin_list, str):
            admin_list = [a.strip().lower() for a in admin_list.split(",") if a.strip()]
        self.admin_users.update(admin_list)

    async def start(self) -> bool:
        """
        Start the chat presence system.

        Returns:
            True if started successfully, False otherwise
        """
        logger.info("🚀 Starting Chat Presence Orchestrator V2...")

        try:
            # Initialize coordinator components
            success = await self._initialize_coordinators()
            if not success:
                logger.error("❌ Failed to initialize coordinators")
                return False

            # Start coordinators
            await self._start_coordinators()

            # Start background tasks
            await self._start_background_tasks()

            self.running = True
            logger.info("✅ Chat Presence Orchestrator V2 started successfully")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to start Chat Presence Orchestrator V2: {e}")
            await self._emergency_shutdown()
            return False

    async def _initialize_coordinators(self) -> bool:
        """
        Initialize all coordinator components.

        Returns:
            True if all coordinators initialized successfully
        """
        try:
            # Initialize agent coordinator components
            agent_success = self.agent_coordinator.initialize_agent_components()
            if not agent_success:
                logger.warning("⚠️ Agent coordinator initialization failed")

            # Initialize OBS coordinator components
            obs_success = self.obs_coordinator.initialize_obs_components()
            if not obs_success:
                logger.warning("⚠️ OBS coordinator initialization failed")

            logger.info("✅ Coordinator components initialized")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to initialize coordinators: {e}")
            return False

    async def _start_coordinators(self) -> None:
        """Start all coordinators."""
        # Initialize Twitch connection
        if self.twitch_config:
            await self.twitch_coordinator.initialize_twitch_connection()

        # Start OBS caption listening
        if self.obs_config:
            await self.obs_coordinator.start_caption_listening()

        # Set up OBS caption callback to broadcast to Twitch
        if self.obs_config and self.twitch_config:
            async def caption_callback(caption_text: str) -> None:
                await self.obs_coordinator.broadcast_caption_to_chat(caption_text, self.twitch_coordinator)

            self.obs_coordinator.register_caption_callback(caption_callback)

    async def _start_background_tasks(self) -> None:
        """Start background processing tasks."""
        # Status update task
        self._status_update_task = asyncio.create_task(self._status_update_loop())

        # Message processing task
        self._message_processing_task = asyncio.create_task(self._message_processing_loop())

        logger.info("✅ Background tasks started")

    async def _status_update_loop(self) -> None:
        """Background task for periodic status updates."""
        while self.running:
            try:
                # Update agent statuses
                await self.agent_coordinator.check_agent_statuses()

                # Check stream status
                if self.twitch_config:
                    stream_status = await self.twitch_coordinator.check_stream_status()
                    logger.debug(f"Stream status: {stream_status}")

                await asyncio.sleep(60)  # Update every minute

            except Exception as e:
                logger.error(f"Error in status update loop: {e}")
                await asyncio.sleep(30)

    async def _message_processing_loop(self) -> None:
        """Background task for processing incoming messages."""
        while self.running:
            try:
                # Process Twitch messages
                if self.twitch_coordinator.is_connected:
                    messages = await self.twitch_coordinator.process_incoming_messages()

                    for message_data in messages:
                        await self._handle_incoming_message(message_data)

                # Process pending agent responses
                pending_responses = await self.agent_coordinator.get_pending_responses()
                for response_data in pending_responses:
                    await self._send_agent_response(response_data)

                await asyncio.sleep(1)  # Process every second

            except Exception as e:
                logger.error(f"Error in message processing loop: {e}")
                await asyncio.sleep(5)

    async def _handle_incoming_message(self, message_data: Dict[str, Any]) -> None:
        """
        Handle incoming chat message.

        Args:
            message_data: Message data from chat platform
        """
        try:
            # Interpret message
            interpretation = await self.agent_coordinator.interpret_chat_message(message_data)

            # Check if response is needed
            if interpretation.get('response_needed', False):
                # Generate agent response
                response = await self.agent_coordinator.generate_agent_response(message_data, interpretation)

                if response and self.twitch_coordinator.is_connected:
                    await self.twitch_coordinator.send_chat_message(response)

            # Handle special message types
            await self._handle_special_messages(message_data)

        except Exception as e:
            logger.error(f"Failed to handle incoming message: {e}")

    async def _handle_special_messages(self, message_data: Dict[str, Any]) -> None:
        """
        Handle special message types (rewards, commands, etc.).

        Args:
            message_data: Message data
        """
        try:
            message_text = message_data.get('message', '').lower()

            # Handle quote redemptions
            if 'quote' in message_text and message_data.get('is_redemption'):
                await self.twitch_coordinator._handle_quote_redemption(message_data.get('username', ''))

            # Handle personality changes
            elif 'personality' in message_text and message_data.get('is_redemption'):
                await self.twitch_coordinator._handle_personality_redemption(message_data.get('username', ''))

            # Handle channel point redemptions
            if message_data.get('reward_data'):
                await self.twitch_coordinator.handle_channel_points_redemption(message_data['reward_data'])

        except Exception as e:
            logger.error(f"Failed to handle special message: {e}")

    async def _send_agent_response(self, response_data: Dict[str, Any]) -> None:
        """
        Send agent response to chat.

        Args:
            response_data: Response data from agent coordinator
        """
        try:
            response_text = response_data.get('response', '')
            if response_text and self.twitch_coordinator.is_connected:
                await self.twitch_coordinator.send_chat_message(response_text)

        except Exception as e:
            logger.error(f"Failed to send agent response: {e}")

    async def stop(self) -> None:
        """Stop the chat presence system."""
        logger.info("🛑 Stopping Chat Presence Orchestrator V2...")

        self.running = False

        # Cancel background tasks
        if self._status_update_task:
            self._status_update_task.cancel()
        if self._message_processing_task:
            self._message_processing_task.cancel()

        # Shutdown coordinators
        await self.twitch_coordinator.shutdown()
        await self.obs_coordinator.shutdown()
        await self.agent_coordinator.shutdown()

        logger.info("✅ Chat Presence Orchestrator V2 stopped")

    async def _emergency_shutdown(self) -> None:
        """Emergency shutdown in case of critical errors."""
        logger.error("🚨 Emergency shutdown initiated")

        self.running = False

        # Cancel tasks
        if self._status_update_task and not self._status_update_task.done():
            self._status_update_task.cancel()
        if self._message_processing_task and not self._message_processing_task.done():
            self._message_processing_task.cancel()

    def get_system_status(self) -> Dict[str, Any]:
        """
        Get comprehensive system status.

        Returns:
            Dict with system status information
        """
        return {
            'running': self.running,
            'twitch_status': self.twitch_coordinator.get_connection_status(),
            'obs_status': self.obs_coordinator.get_connection_status(),
            'agent_status': self.agent_coordinator.get_coordination_status(),
            'config_valid': bool(self.twitch_config or self.obs_config),
            'admin_users': list(self.admin_users)
        }

    # Legacy compatibility methods
    async def send_message(self, message: str, priority: str = "normal") -> bool:
        """Legacy method for sending messages."""
        return await self.twitch_coordinator.send_chat_message(message, priority)

    def get_status(self) -> Dict[str, Any]:
        """Legacy method for getting status."""
        return self.get_system_status()