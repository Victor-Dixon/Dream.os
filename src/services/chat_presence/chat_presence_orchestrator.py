#!/usr/bin/env python3
"""
<!-- SSOT Domain: integration -->

Chat Presence Orchestrator
==========================

Unified orchestrator for chat presence system.
Coordinates Twitch, Discord, OBS caption integration.

V2 Compliance: <400 lines, single responsibility
Migrated to BaseService for consolidated initialization and error handling.
Author: Agent-7 (Web Development Specialist)
License: MIT
"""

from src.core.messaging_models_core import (
    UnifiedMessagePriority,
    UnifiedMessageTag,
    UnifiedMessageType,
)
from src.core.messaging_core import send_message
from src.core.base.base_service import BaseService
from src.core.agent_mode_manager import get_mode_manager, get_active_agents
<<<<<<< HEAD
from src.obs import InterpretedCaption
=======
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
import asyncio
import logging
from pathlib import Path
from typing import Optional, List

<<<<<<< HEAD
# Import extracted coordinators - V2 MODULARIZATION ENABLED
from .chat_config_manager import ChatConfigManager
from .twitch_coordinator import TwitchCoordinator
from .obs_coordinator import OBSCoordinator
from .agent_coordinator import AgentCoordinator

# Legacy imports for backward compatibility
from .twitch_bridge import TwitchChatBridge
from .quote_generator import get_random_quote, format_quote_for_chat

=======
# Use unified logging system
from src.core.unified_logging_system import get_logger, configure_logging

from .agent_personality import format_chat_message, get_personality
from .chat_scheduler import ChatScheduler
from .message_interpreter import MessageInterpreter
from .status_reader import AgentStatusReader
from .twitch_bridge import TwitchChatBridge
from .quote_generator import get_random_quote, format_quote_for_chat

# Configure logging for chat_presence with file handler
log_dir = Path(__file__).parent.parent.parent.parent / "logs"
log_dir.mkdir(parents=True, exist_ok=True)
log_file = log_dir / "chat_presence_orchestrator.log"
configure_logging(level="DEBUG", log_file=log_file)

logger = get_logger(__name__)
# OBS imports (optional - bot can run without OBS)
try:
    from src.obs.caption_interpreter import CaptionInterpreter, InterpretedCaption
    from src.obs.caption_listener import OBSCaptionListener
    from src.obs.speech_log_manager import SpeechLogManager
    OBS_AVAILABLE = True
except ImportError:
    OBS_AVAILABLE = False
    # Create stub classes for when OBS is not available

    class CaptionInterpreter:
        def __init__(self):
            pass

    class InterpretedCaption:
        pass

    class OBSCaptionListener:
        pass

    class SpeechLogManager:
        def __init__(self):
            pass

>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
logger = logging.getLogger(__name__)


class ChatPresenceOrchestrator(BaseService):
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
<<<<<<< HEAD
        Initialize chat presence orchestrator - V2 MODULAR ARCHITECTURE.

        Uses coordinator pattern for clean separation of concerns.

        Args:
            twitch_config: Twitch configuration dict (legacy support)
            obs_config: OBS configuration dict (legacy support)
        """
        super().__init__("ChatPresenceOrchestrator")

        # V2 MODULAR ARCHITECTURE: Initialize coordinators
        self.config_manager = ChatConfigManager()
        self.twitch_coordinator = TwitchCoordinator(self.config_manager)
        self.obs_coordinator = OBSCoordinator(self.config_manager)
        self.agent_coordinator = AgentCoordinator(self.config_manager)

        # Legacy support - load config from environment if not provided
        if twitch_config is None:
            twitch_config = self._load_twitch_config_from_env()

        self.twitch_config = twitch_config or {}
        self.obs_config = obs_config or {}

        # Legacy components for backward compatibility
=======
        Initialize chat presence orchestrator.

        Args:
            twitch_config: Twitch configuration dict
            obs_config: OBS configuration dict
        """
        super().__init__("ChatPresenceOrchestrator")
        self.twitch_config = twitch_config or {}
        self.obs_config = obs_config or {}

        # Initialize components
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
        self.message_interpreter = MessageInterpreter()
        self.chat_scheduler = ChatScheduler()
        self.status_reader = AgentStatusReader()
        # OBS components (only if OBS is available)
        if OBS_AVAILABLE:
            self.caption_interpreter = CaptionInterpreter()
            self.speech_log_manager = SpeechLogManager()
        else:
            self.caption_interpreter = None
            self.speech_log_manager = None

<<<<<<< HEAD
        # Bridges (initialized on start) - LEGACY
=======
        # Bridges (initialized on start)
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
        self.twitch_bridge: Optional[TwitchChatBridge] = None
        self.obs_listener: Optional[OBSCaptionListener] = None

        self.running = False
        self._status_update_task: Optional[asyncio.Task] = None

        # Admin users (channel owner + configured admins)
        self.admin_users = set()
        channel_owner = self.twitch_config.get(
            "channel", "").lstrip("#").lower()
        if channel_owner:
            self.admin_users.add(channel_owner)
        # Add configured admins from env/config if needed
        admin_list = self.twitch_config.get("admin_users", [])
        if isinstance(admin_list, str):
            admin_list = [a.strip().lower()
                          for a in admin_list.split(",") if a.strip()]
        self.admin_users.update(admin_list)

<<<<<<< HEAD
    def _load_twitch_config_from_env(self) -> dict:
        """
        Load Twitch configuration from environment variables with URL parsing.

        Returns:
            Dict containing Twitch configuration
        """
        import os

        config = {}

        # Get channel from environment
        channel = os.getenv("TWITCH_CHANNEL", "").strip()
        if channel:
            # Parse URL if present
            if channel.startswith("#"):
                channel = channel[1:]
                print("   ⚠️  Removed # prefix from channel")

            if "twitch.tv/" in channel.lower():
                # Extract channel name from URL
                parts = channel.lower().split("twitch.tv/")
                if len(parts) > 1:
                    channel = parts[-1].split("/")[0].split("?")[0].rstrip("/")
                    print(f"   ⚠️  Extracted channel name from URL: {channel}")

            # Normalize channel
            channel = channel.lower().strip()
            config["channel"] = channel

        # Get token from environment
        token = os.getenv("TWITCH_ACCESS_TOKEN", "").strip()
        if token:
            # Ensure it starts with oauth: prefix
            if not token.startswith("oauth:"):
                token = f"oauth:{token}"
            config["oauth_token"] = token

        # Get username from environment or use channel name
        username = os.getenv("TWITCH_BOT_USERNAME", "").strip() or channel
        if username:
            config["username"] = username.lower().strip()

        # Get admin users
        admin_users = os.getenv("TWITCH_ADMIN_USERS", "").strip()
        if admin_users:
            config["admin_users"] = [u.strip().lower() for u in admin_users.split(",") if u.strip()]

        return config

    async def start(self) -> bool:
        """
        Start chat presence system - V2 MODULAR ARCHITECTURE.

        Uses coordinators for clean separation of concerns.
=======
    async def start(self) -> bool:
        """
        Start chat presence system.
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console

        Returns:
            True if started successfully
        """
<<<<<<< HEAD
        logger.info("🚀 Starting Chat Presence Orchestrator (V2)...")

        # V2 MODULAR STARTUP: Start coordinators
        coordinator_results = []

        # Start Twitch coordinator
        twitch_success = await self.twitch_coordinator.start()
        coordinator_results.append(("Twitch", twitch_success))

        # Start OBS coordinator
        obs_success = await self.obs_coordinator.start()
        coordinator_results.append(("OBS", obs_success))

        # Start Agent coordinator
        agent_success = await self.agent_coordinator.start()
        coordinator_results.append(("Agent", agent_success))

        # Log coordinator startup results
        for name, success in coordinator_results:
            if success:
                logger.info(f"✅ {name} coordinator started")
            else:
                logger.warning(f"⚠️ {name} coordinator failed to start")

        # LEGACY SUPPORT: Start old bridges for backward compatibility
        if self.twitch_config:
            success = await self._start_twitch()
            if not success:
                logger.warning("⚠️ Legacy Twitch bridge failed to start")

        if self.obs_config:
            success = await self._start_obs()
            if not success:
                logger.warning("⚠️ Legacy OBS listener failed to start")

        self.running = True

        # Start periodic status updates using coordinators
        if self.twitch_coordinator.is_healthy():
=======
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

        # Start periodic status updates (every 5 minutes)
        if self.twitch_bridge:
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
            self._status_update_task = asyncio.create_task(
                self._periodic_status_updates()
            )
            logger.info("📊 Periodic status updates started (every 5 minutes)")

        logger.info("✅ Chat Presence Orchestrator started")
        return True

    async def _start_twitch(self) -> bool:
        """Start Twitch bridge."""
        try:
            logger.debug(
                "Creating TwitchChatBridge",
                extra={
                    "username": self.twitch_config.get('username', ''),
                    "channel": self.twitch_config.get('channel', ''),
                    "oauth_token_preview": self.twitch_config.get('oauth_token', '')[:15] + "...",
                    "has_callback": self._handle_twitch_message is not None,
                }
            )

            self.twitch_bridge = TwitchChatBridge(
                username=self.twitch_config.get("username", ""),
                oauth_token=self.twitch_config.get("oauth_token", ""),
                channel=self.twitch_config.get("channel", ""),
                on_message=self._handle_twitch_message,
            )

            logger.debug("TwitchChatBridge created, calling connect()...")
            result = await self.twitch_bridge.connect()
            logger.debug(f"connect() returned: {result}")
            return result

        except Exception as e:
            logger.error(
                "Failed to start Twitch bridge",
                extra={
                    "error_type": type(e).__name__,
                    "error_message": str(e),
                    "component": "ChatPresenceOrchestrator",
                    "operation": "_start_twitch",
                },
                exc_info=True
            )
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

        logger.info(
            "Twitch message received",
            extra={
                "username": username,
                "message_preview": message[:50],
                "message_keys": list(message_data.keys()),
            }
        )

        # Handle status commands first (special case - available to all users)
        is_status = self.message_interpreter.is_status_command(message)
        logger.debug(f"is_status_command returned: {is_status}")

        if is_status:
            logger.info(f"Status command detected: {message}")
            try:
                await self._handle_status_command(message)
                logger.debug("_handle_status_command completed")
            except Exception as e:
                logger.error(
                    "Error in _handle_status_command",
                    extra={
                        "error_type": type(e).__name__,
                        "error_message": str(e),
                        "component": "ChatPresenceOrchestrator",
                        "operation": "_handle_status_command",
                        "message": message,
                    },
                    exc_info=True
                )
            return

        # Handle quote commands (available to all users)
        is_quote = self.message_interpreter.is_quote_command(message)
        logger.debug(f"is_quote_command returned: {is_quote}")

        if is_quote:
            logger.info(f"Quote command detected: {message}")
            try:
                quote_response = self.message_interpreter.get_quote_response()
                await self.twitch_bridge.send_message(quote_response)
                logger.debug("Quote sent to chat")
            except Exception as e:
                logger.error(
                    "Error handling quote command",
                    extra={
                        "error_type": type(e).__name__,
                        "error_message": str(e),
                        "component": "ChatPresenceOrchestrator",
                        "operation": "_handle_quote_command",
                        "message": message,
                    },
                    exc_info=True
                )
            return

        # Check if user is admin for agent messaging commands
        is_admin = self._is_admin_user(username, message_data.get("tags", {}))

        # Determine which agent should respond
        agent_id = self.message_interpreter.determine_responder(
            message, username, "twitch"
        )

        logger.debug(f"Determined agent: {agent_id}")

        if not agent_id:
            logger.debug("No agent determined, returning")
            return

        # Handle broadcast (admin only)
        if agent_id == "BROADCAST":
            if not is_admin:
                await self.twitch_bridge.send_message(
                    "❌ Only admins can send broadcast messages to agents."
                )
                return
            await self._handle_broadcast(message, "twitch")
            # Also send confirmation to chat
            await self.twitch_bridge.send_message("✅ Message sent to all agents!")
            return

        # Check admin permission for agent messaging
        if message.lower().startswith("!agent") and not is_admin:
            await self.twitch_bridge.send_message(
                f"❌ Only admins can send messages to agents. Use !status to check agent status."
            )
            logger.warning(
                f"⚠️ Non-admin user {username} attempted to message agents")
            return

        # Extract message content (remove command prefix)
        message_content = message
        if message.lower().startswith("!agent"):
            # Remove !agent7, !agent-7, etc. and get the actual message
            parts = message.split(None, 1)
            if len(parts) > 1:
                message_content = parts[1]
            else:
                message_content = "Hello from Twitch chat!"

        logger.debug(f"Message content to send: '{message_content}'")

        # Send message to agent's inbox using messaging CLI (more reliable)
        logger.info(f"Sending message to {agent_id}: {message_content}")

        try:
            # Use messaging CLI for reliable delivery
            import subprocess
            import sys
            from pathlib import Path
            from src.core.config.timeout_constants import TimeoutConstants

            message_text = f"Twitch Chat Message from {username}: {message_content}"
            cmd = [
                sys.executable,
                "-m", "src.services.messaging_cli",
                "--agent", agent_id,
                "--message", message_text,
                "--priority", "normal"
            ]

            logger.debug(f"Running CLI command: {' '.join(cmd)}")
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=TimeoutConstants.HTTP_SHORT,
                cwd=str(Path(__file__).parent.parent.parent.parent)
            )

            logger.debug(
                "CLI command completed",
                extra={
                    "returncode": result.returncode,
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                }
            )

            if result.returncode == 0:
                logger.info(f"Message sent to {agent_id} inbox via CLI")
                # Also send confirmation to Twitch chat
                try:
                    await self.twitch_bridge.send_message(f"✅ Message sent to {agent_id}!")
                    logger.debug("Confirmation sent to Twitch chat")
                except Exception as e:
                    logger.warning(
                        "Failed to send Twitch confirmation",
                        extra={"error": str(e)}
                    )
            else:
                logger.warning(
                    "CLI message send failed",
                    extra={
                        "returncode": result.returncode,
                        "stderr": result.stderr,
                        "agent_id": agent_id,
                    }
                )

                # Fallback to direct send_message
                try:
                    send_message(
                        content=message_text,
                        sender=f"Twitch-{username}",
                        recipient=agent_id,
                        message_type=UnifiedMessageType.HUMAN_TO_AGENT,
                        priority=UnifiedMessagePriority.REGULAR,
                        tags=[UnifiedMessageTag.COORDINATION],
                    )
                    logger.debug("Fallback send_message called")
                    await self.twitch_bridge.send_message(f"✅ Message sent to {agent_id} (fallback method)")
                except Exception as e:
                    logger.error(
                        "Both CLI and fallback failed",
                        extra={
                            "error_type": type(e).__name__,
                            "error_message": str(e),
                            "agent_id": agent_id,
                        },
                        exc_info=True
                    )

        except Exception as e:
            logger.error(
                "Failed to send message",
                extra={
                    "error_type": type(e).__name__,
                    "error_message": str(e),
                    "agent_id": agent_id,
                    "component": "ChatPresenceOrchestrator",
                    "operation": "send_message_to_agent",
                },
                exc_info=True
            )

        # Check if agent can speak
        if not self.chat_scheduler.can_agent_speak(agent_id):
            logger.debug(f"⏸️ {agent_id} on cooldown, skipping chat response")
            # Still send confirmation
            await self.twitch_bridge.send_message(f"✅ Message sent to {agent_id}!")
            return

        # Generate response
        response = await self._generate_agent_response(agent_id, message_content)

        if response:
            # Send response to chat
            await self.twitch_bridge.send_as_agent(agent_id, response)

            # Record activity
            self.chat_scheduler.record_agent_response(agent_id)
        else:
            # Send confirmation even if no response generated
            await self.twitch_bridge.send_message(f"✅ Message sent to {agent_id}!")

    async def _handle_status_command(self, message: str) -> None:
        """
        Handle status command from Twitch chat.

        Args:
            message: Status command message (e.g., "!status" or "!status agent7")
        """
        logger.info(f"Status command received: {message}")

        # Parse command
        command_type, agent_id = self.message_interpreter.parse_status_command(
            message)
        logger.debug(
            "Parsed status command",
            extra={"command_type": command_type, "agent_id": agent_id}
        )

        try:
            if not self.status_reader:
                logger.error("status_reader is None!")
                await self.twitch_bridge.send_message("❌ Status reader not available")
                return

            logger.debug("status_reader available, proceeding...")

            # Single-agent status (e.g., "!status agent3")
            if command_type == "agent" and agent_id:
                status_text = self.status_reader.format_agent_status_compact(
                    agent_id)
                await self.twitch_bridge.send_message(status_text)
                return

            # Mode-aware multi-agent summary for Twitch
            mode_manager = get_mode_manager()
            current_mode = mode_manager.get_current_mode()
            active_agents: List[str] = mode_manager.get_active_agents()

            if not active_agents:
                await self.twitch_bridge.send_message(
                    f"📊 Swarm Status — {current_mode}: no active agents configured."
                )
                return

            header = f"📊 Swarm Status — {current_mode} ({len(active_agents)} active agents)"
            lines: List[str] = [header]
            for agent in active_agents:
                lines.append(
                    self.status_reader.format_agent_status_compact(agent))
            lines.append("Use !status agent3 for a single-agent view.")

            # Twitch has message length limits, so send in chunks (~450 chars max)
            chunk: List[str] = []
            current_length = 0
            for line in lines:
                if current_length + len(line) + 3 > 450 and chunk:
                    await self.twitch_bridge.send_message(" | ".join(chunk))
                    chunk = [line]
                    current_length = len(line)
                else:
                    chunk.append(line)
                    current_length += len(line) + 3

            if chunk:
                await self.twitch_bridge.send_message(" | ".join(chunk))

        except Exception as e:
            logger.error(
                f"❌ Error handling status command: {e}", exc_info=True)
            await self.twitch_bridge.send_message("❌ Error retrieving status")

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

    def _is_admin_user(self, username: str, tags: dict) -> bool:
        """
        Check if user is an admin.

        Args:
            username: Twitch username (lowercase)
            tags: Twitch IRC tags (may contain badges)

        Returns:
            True if user is admin
        """
        username_lower = username.lower()

        # Channel owner is always admin
        channel_owner = self.twitch_config.get(
            "channel", "").lstrip("#").lower()
        if channel_owner and username_lower == channel_owner:
            return True

        # Check configured admin list from config/env (explicit allow-list)
        if username_lower in self.admin_users:
            return True

        # Do NOT implicitly trust badges; only explicit owner/admin list
        return False

    async def _periodic_status_updates(self) -> None:
        """
        Background task to post periodic status updates to Twitch chat.
        Posts every 5 minutes.
        """
        # Wait for connection to be established before sending updates
        max_wait = 30  # Wait up to 30 seconds for connection
        wait_count = 0
        while wait_count < max_wait:
            if self.twitch_bridge and self.twitch_bridge.connected:
                break
            await asyncio.sleep(1)
            wait_count += 1

        if not self.twitch_bridge or not self.twitch_bridge.connected:
            logger.warning(
                "⚠️ Twitch bridge not connected, skipping periodic updates")
            return

        while self.running:
            try:
                await asyncio.sleep(300)  # 5 minutes

                if not self.running or not self.twitch_bridge or not self.twitch_bridge.connected:
                    break

                # Mode-aware periodic status update
                mode_manager = get_mode_manager()
                current_mode = mode_manager.get_current_mode()
                active_agents: List[str] = mode_manager.get_active_agents()

                if not active_agents:
                    await self.twitch_bridge.send_message(
                        f"📊 Swarm Status — {current_mode}: no active agents configured."
                    )
                    continue

                header = f"📊 Swarm Status Update — {current_mode} ({len(active_agents)} active agents)"
                lines: List[str] = [header]
                for agent in active_agents:
                    lines.append(
                        self.status_reader.format_agent_status_compact(agent))

                # Send in chunks under Twitch length limits
                chunk: List[str] = []
                current_length = 0
                for line in lines:
                    if current_length + len(line) + 3 > 450 and chunk:
                        await self.twitch_bridge.send_message(" | ".join(chunk))
                        chunk = [line]
                        current_length = len(line)
                    else:
                        chunk.append(line)
                        current_length += len(line) + 3

                if chunk:
                    await self.twitch_bridge.send_message(" | ".join(chunk))

                logger.info("📊 Periodic status update posted to Twitch")

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(
                    f"❌ Error in periodic status update: {e}", exc_info=True)
                # Continue running even if one update fails
                await asyncio.sleep(60)  # Wait 1 minute before retry

    async def stop(self) -> None:
<<<<<<< HEAD
        """Stop chat presence system - V2 MODULAR ARCHITECTURE."""
        logger.info("🛑 Stopping Chat Presence Orchestrator (V2)...")
=======
        """Stop chat presence system."""
        logger.info("🛑 Stopping Chat Presence Orchestrator...")
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
        self.running = False

        # Cancel periodic status updates
        if self._status_update_task:
            self._status_update_task.cancel()
            try:
                await self._status_update_task
            except asyncio.CancelledError:
                pass

<<<<<<< HEAD
        # V2 MODULAR SHUTDOWN: Stop coordinators
        await self.twitch_coordinator.stop()
        await self.obs_coordinator.stop()
        await self.agent_coordinator.stop()

        # LEGACY SUPPORT: Stop old bridges
=======
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
        if self.twitch_bridge:
            self.twitch_bridge.stop()

        if self.obs_listener:
            await self.obs_listener.disconnect()

<<<<<<< HEAD
        logger.info("✅ Chat Presence Orchestrator stopped (V2)")
=======
        logger.info("✅ Chat Presence Orchestrator stopped")
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console


__all__ = ["ChatPresenceOrchestrator"]
