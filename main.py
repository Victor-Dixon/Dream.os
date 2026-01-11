#!/usr/bin/env python3
"""
Agent Cellphone V2 - Main Entry Point
====================================

Professional entry point for the Agent Cellphone V2 system.

Usage:
    python main.py                    # Start interactive mode
    python main.py --api-only         # Start API only
    python main.py --status           # Check system status
    python main.py --stop             # Stop running services
"""

import asyncio
import argparse
import logging
import signal
import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from agent_cellphone_v2 import AgentCoordinator
from agent_cellphone_v2.config import Settings

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class AgentCellphoneApp:
    """Main application class."""

    def __init__(self):
        self.coordinator: AgentCoordinator = None
        self.settings = Settings()

    async def start(self, api_only: bool = False):
        """Start the application."""
        logger.info("Starting Agent Cellphone V2...")

        # Setup directories
        self.settings.setup_directories()

        # Validate configuration
        validation_messages = self.settings.validate_config()
        for message in validation_messages:
            if message.startswith("❌"):
                logger.error(message)
            else:
                logger.warning(message)

        # Initialize coordinator
        self.coordinator = AgentCoordinator()

        # Setup signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

        try:
            await self.coordinator.start()
            logger.info("Agent Cellphone V2 started successfully")
            logger.info(f"API available at: http://{self.settings.api_host}:{self.settings.api_port}")
            logger.info("Press Ctrl+C to stop")

            # Keep running
            while self.coordinator.is_running():
                await asyncio.sleep(1)

        except KeyboardInterrupt:
            logger.info("Received shutdown signal")
        except Exception as e:
            logger.error(f"Error during startup: {e}")
            raise
        finally:
            if self.coordinator:
                await self.coordinator.stop()

    def _signal_handler(self, signum, frame):
        """Handle shutdown signals."""
        logger.info(f"Received signal {signum}, shutting down...")
        if self.coordinator:
            asyncio.create_task(self.coordinator.stop())

    async def status(self):
        """Get system status."""
        if not self.coordinator:
            self.coordinator = AgentCoordinator()

        status = await self.coordinator.get_status()
        print("Agent Cellphone V2 Status:")
        print(f"  Running: {status['running']}")
        print(f"  Version: {status['version']}")
        print("  Services:")
        for service, running in status['services'].items():
            print(f"    {service}: {'✅' if running else '❌'}")

    async def stop(self):
        """Stop running services."""
        logger.info("Stopping Agent Cellphone V2...")
        if self.coordinator:
            await self.coordinator.stop()
        logger.info("Agent Cellphone V2 stopped")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Agent Cellphone V2")
    parser.add_argument("--api-only", action="store_true", help="Start API service only")
    parser.add_argument("--status", action="store_true", help="Show system status")
    parser.add_argument("--stop", action="store_true", help="Stop running services")
    parser.add_argument("--config", help="Path to config file")

    args = parser.parse_args()

    # Override config if specified
    if args.config:
        Settings.Config.env_file = args.config

    app = AgentCellphoneApp()

    if args.status:
        asyncio.run(app.status())
    elif args.stop:
        asyncio.run(app.stop())
    else:
        # Start the application
        asyncio.run(app.start(api_only=args.api_only))


if __name__ == "__main__":
    main()