"""
Core Agent Cellphone V2 functionality.
"""

import asyncio
import logging
from typing import Optional, Dict, Any
from pathlib import Path

from .config import Settings
from .services.messaging import MessagingService
from .services.api import APIService

logger = logging.getLogger(__name__)


class AgentCoordinator:
    """
    Main coordinator for the Agent Cellphone V2 system.

    This class manages the lifecycle of all services and coordinates
    communication between agents.
    """

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the Agent Coordinator.

        Args:
            config_path: Path to configuration file (optional)
        """
        self.config_path = config_path or ".env"
        self.settings = Settings(_env_file=config_path)
        self.messaging_service: Optional[MessagingService] = None
        self.api_service: Optional[APIService] = None
        self._running = False

    async def start(self) -> None:
        """Start all services."""
        logger.info("Starting Agent Cellphone V2...")

        # Initialize services
        self.messaging_service = MessagingService(self.settings)
        self.api_service = APIService(self.settings)

        # Start services
        await asyncio.gather(
            self.messaging_service.start(),
            self.api_service.start()
        )

        self._running = True
        logger.info("Agent Cellphone V2 started successfully")

    async def stop(self) -> None:
        """Stop all services."""
        logger.info("Stopping Agent Cellphone V2...")

        if self.messaging_service:
            await self.messaging_service.stop()
        if self.api_service:
            await self.api_service.stop()

        self._running = False
        logger.info("Agent Cellphone V2 stopped")

    def is_running(self) -> bool:
        """Check if the system is running."""
        return self._running

    async def send_message(self, recipient: str, message: str, **kwargs) -> Dict[str, Any]:
        """
        Send a message to an agent.

        Args:
            recipient: Agent ID to send message to
            message: Message content
            **kwargs: Additional message parameters

        Returns:
            Message delivery status
        """
        if not self.messaging_service:
            raise RuntimeError("Messaging service not initialized")

        return await self.messaging_service.send_message(recipient, message, **kwargs)

    async def get_status(self) -> Dict[str, Any]:
        """
        Get system status.

        Returns:
            System status information
        """
        return {
            "running": self._running,
            "services": {
                "messaging": self.messaging_service.is_running() if self.messaging_service else False,
                "api": self.api_service.is_running() if self.api_service else False,
            },
            "version": __import__(__name__.split('.')[0]).__version__,
        }