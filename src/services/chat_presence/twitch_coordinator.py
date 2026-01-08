"""
Twitch Coordinator - V2 Coordinator Module
==========================================

SSOT Domain: integration

V2 Compliant: <150 lines, single responsibility
Twitch chat coordination and management.

Author: Agent-2 (dream.os)
Date: 2026-01-08
"""

import asyncio
import logging
from typing import Optional, Dict, Any, List, Callable
from datetime import datetime

from .chat_config_manager import ChatConfigManager


class TwitchCoordinator:
    """
    V2 Compliant Twitch Coordinator

    Manages Twitch chat integration including:
    - Connection lifecycle
    - Message handling
    - Event subscription
    - Status monitoring
    """

    def __init__(self, config_manager: ChatConfigManager):
        self.config_manager = config_manager
        self.logger = logging.getLogger("TwitchCoordinator")

        # Connection state
        self.connected = False
        self.last_message_time = None
        self.message_count = 0
        self.reconnect_count = 0

        # Callbacks
        self.message_handlers: List[Callable] = []
        self.connection_handlers: List[Callable] = []

        # Import twitch bridge when needed
        self._twitch_bridge = None

    async def start(self) -> bool:
        """Start Twitch coordination"""
        if not self.config_manager.is_twitch_enabled():
            self.logger.info("Twitch coordination disabled in config")
            return True

        try:
            # Import twitch bridge
            from .twitch_bridge import TwitchChatBridge

            # Create bridge instance
            self._twitch_bridge = TwitchChatBridge()

            # Connect to Twitch
            success = await self._twitch_bridge.connect()
            if success:
                self.connected = True
                self.logger.info("✅ Twitch coordinator started successfully")

                # Notify connection handlers
                for handler in self.connection_handlers:
                    try:
                        await handler(True)
                    except Exception as e:
                        self.logger.error(f"Connection handler error: {e}")

                return True
            else:
                self.logger.error("❌ Failed to start Twitch coordinator")
                return False

        except Exception as e:
            self.logger.error(f"❌ Twitch coordinator startup error: {e}")
            return False

    async def stop(self) -> None:
        """Stop Twitch coordination"""
        if self._twitch_bridge:
            await self._twitch_bridge.disconnect()

        self.connected = False
        self.logger.info("🛑 Twitch coordinator stopped")

        # Notify connection handlers
        for handler in self.connection_handlers:
            try:
                await handler(False)
            except Exception as e:
                self.logger.error(f"Disconnection handler error: {e}")

    async def send_message(self, message: str) -> bool:
        """Send message to Twitch chat"""
        if not self.connected or not self._twitch_bridge:
            return False

        try:
            success = await self._twitch_bridge.send_message(message)
            if success:
                self.last_message_time = datetime.now()
                self.message_count += 1
            return success
        except Exception as e:
            self.logger.error(f"Message send error: {e}")
            return False

    def add_message_handler(self, handler: Callable) -> None:
        """Add message handler callback"""
        self.message_handlers.append(handler)

    def add_connection_handler(self, handler: Callable) -> None:
        """Add connection handler callback"""
        self.connection_handlers.append(handler)

    def get_status(self) -> Dict[str, Any]:
        """Get current Twitch coordination status"""
        return {
            "connected": self.connected,
            "last_message_time": self.last_message_time.isoformat() if self.last_message_time else None,
            "message_count": self.message_count,
            "reconnect_count": self.reconnect_count,
            "config_valid": self.config_manager.validate_config()["valid"]
        }

    async def reconnect(self) -> bool:
        """Attempt to reconnect to Twitch"""
        self.logger.info("🔄 Attempting Twitch reconnection...")
        self.reconnect_count += 1

        # Stop current connection
        await self.stop()

        # Wait before reconnecting
        await asyncio.sleep(min(self.reconnect_count * 5, 30))

        # Start new connection
        return await self.start()

    def is_healthy(self) -> bool:
        """Check if Twitch coordinator is healthy"""
        if not self.config_manager.is_twitch_enabled():
            return True  # Disabled is considered healthy

        config_valid = self.config_manager.validate_config()["valid"]
        return config_valid and self.connected

    async def handle_incoming_message(self, message: Dict[str, Any]) -> None:
        """Handle incoming Twitch message"""
        self.last_message_time = datetime.now()

        # Notify message handlers
        for handler in self.message_handlers:
            try:
                await handler(message)
            except Exception as e:
                self.logger.error(f"Message handler error: {e}")