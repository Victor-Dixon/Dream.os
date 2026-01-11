"""
API service for Agent Cellphone V2.
"""

import asyncio
import logging
from typing import Dict, Any
from fastapi import FastAPI
from uvicorn import Server, Config
import uvicorn

from ..config import Settings

logger = logging.getLogger(__name__)


class APIService:
    """
    FastAPI-based REST API service for Agent Cellphone V2.
    """

    def __init__(self, settings: Settings):
        """
        Initialize API service.

        Args:
            settings: Application settings
        """
        self.settings = settings
        self.app = FastAPI(
            title=self.settings.app_name,
            version=self.settings.app_version,
            debug=self.settings.debug,
        )
        self.server: Optional[Server] = None
        self._running = False

        self._setup_routes()

    def _setup_routes(self) -> None:
        """Setup API routes."""

        @self.app.get("/")
        async def root():
            """Root endpoint."""
            return {"message": f"{self.settings.app_name} API", "version": self.settings.app_version}

        @self.app.get("/health")
        async def health():
            """Health check endpoint."""
            return {"status": "healthy", "timestamp": asyncio.get_event_loop().time()}

        @self.app.get("/status")
        async def status():
            """System status endpoint."""
            return {
                "status": "running" if self._running else "stopped",
                "version": self.settings.app_version,
                "debug": self.settings.debug,
            }

    async def start(self) -> None:
        """Start the API service."""
        logger.info(f"Starting API service on {self.settings.api_host}:{self.settings.api_port}...")

        config = Config(
            app=self.app,
            host=self.settings.api_host,
            port=self.settings.api_port,
            workers=self.settings.api_workers,
            log_level=self.settings.log_level.lower(),
        )

        self.server = Server(config)

        # Run server in background
        asyncio.create_task(self.server.serve())
        self._running = True

        logger.info("API service started")

    async def stop(self) -> None:
        """Stop the API service."""
        logger.info("Stopping API service...")

        if self.server:
            self.server.should_exit = True

        self._running = False
        logger.info("API service stopped")

    def is_running(self) -> bool:
        """Check if service is running."""
        return self._running