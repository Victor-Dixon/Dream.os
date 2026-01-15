"""
Bot Runner Service - Agent Cellphone V2
======================================

SSOT Domain: discord

Core service for managing Discord bot lifecycle, initialization, and reconnection.

Features:
- Bot initialization and configuration
- Automatic reconnection with exponential backoff
- Logging setup and management
- Environment validation
- Graceful shutdown handling

V2 Compliant: Yes (<300 lines)
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2026-01-07
"""

import asyncio
import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any

try:
    import discord
    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False

logger = logging.getLogger(__name__)

class BotRunnerService:
    """
    Service for managing Discord bot lifecycle and operations.
    """

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.bot: Optional[discord.Client] = None
        self.logger = logging.getLogger(__name__)

    def setup_logging(self) -> None:
        """Setup comprehensive logging configuration."""
        log_dir = self.repo_root / "runtime" / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)

        log_file = log_dir / f"discord_bot_{datetime.now().strftime('%Y%m%d')}.log"

        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s | %(name)s | %(levelname)s | %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler(sys.stdout)
            ]
        )

        # Set discord.py logging level
        logging.getLogger('discord').setLevel(logging.WARNING)
        logging.getLogger('discord.http').setLevel(logging.WARNING)
        logging.getLogger('discord.gateway').setLevel(logging.WARNING)

        self.logger.info(f"📝 Logging initialized - Log file: {log_file}")

    def validate_environment(self) -> bool:
        """
        Validate required environment variables and dependencies.

        Returns:
            True if environment is valid, False otherwise
        """
        issues = []

        # Check Discord availability
        if not DISCORD_AVAILABLE:
            issues.append("discord.py not installed - run: pip install discord.py")
            return False

        # Check Discord token
        token = os.getenv('DISCORD_BOT_TOKEN')
        if not token:
            issues.append("DISCORD_BOT_TOKEN environment variable not set")
        elif len(token) < 50:  # Basic token format check
            issues.append("DISCORD_BOT_TOKEN appears to be invalid (too short)")

        # Check other required environment variables
        required_vars = [
            'DISCORD_BOT_TOKEN',
            'DISCORD_GUILD_ID'
        ]

        for var in required_vars:
            if not os.getenv(var):
                issues.append(f"Missing required environment variable: {var}")

        if issues:
            self.logger.error("❌ Environment validation failed:")
            for issue in issues:
                self.logger.error(f"  • {issue}")
            return False

        self.logger.info("✅ Environment validation passed")
        return True

    def create_bot_instance(self) -> Optional[discord.Client]:
        """
        Create and configure the Discord bot instance.

        Returns:
            Configured bot instance or None if failed
        """
        try:
            # Import the unified bot
            from src.discord_commander.unified_discord_bot import UnifiedDiscordBot



            self.logger.info("✅ Bot instance created successfully")
            return bot

        except Exception as e:
            self.logger.error(f"❌ Failed to create bot instance: {e}")
            return None

    async def run_bot_with_reconnection(self, bot: discord.Client) -> int:
        """
        Run the bot with automatic reconnection logic.

        Args:
            bot: The Discord bot instance to run

        Returns:
            Exit code (0 for success, 1 for failure)
        """
        max_retries = 10
        base_delay = 5.0  # seconds
        max_delay = 300.0  # 5 minutes

        for attempt in range(max_retries):
            try:
                self.logger.info(f"🚀 Starting Discord bot (attempt {attempt + 1}/{max_retries})")

                token = os.getenv('DISCORD_BOT_TOKEN')
                if not token:
                    self.logger.error("❌ No Discord token found")
                    return 1

                # Run the bot
                await bot.start(token)

            except discord.LoginFailure:
                self.logger.error("❌ Invalid Discord token")
                return 1

            except discord.PrivilegedIntentsRequired:
                self.logger.error("❌ Privileged intents required but not enabled")
                self.logger.error("   Go to https://discord.com/developers/applications/")
                self.logger.error("   Enable 'Message Content Intent' in Bot settings")
                return 1

            except KeyboardInterrupt:
                self.logger.info("🛑 Bot shutdown requested by user")
                await self.graceful_shutdown(bot)
                return 0

            except Exception as e:
                self.logger.error(f"❌ Bot crashed (attempt {attempt + 1}): {e}")

                if attempt < max_retries - 1:
                    # Calculate delay with exponential backoff
                    delay = min(base_delay * (2 ** attempt), max_delay)
                    self.logger.info(f"⏳ Retrying in {delay} seconds...")

                    await asyncio.sleep(delay)
                    continue
                else:
                    self.logger.error("❌ Max retries exceeded, giving up")
                    return 1

        return 0

    async def graceful_shutdown(self, bot: discord.Client) -> None:
        """
        Perform graceful shutdown of the bot.

        Args:
            bot: The bot instance to shut down
        """
        try:
            self.logger.info("🛑 Initiating graceful shutdown...")

            # Close the bot connection
            await bot.close()

            # Cancel all running tasks
            tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
            if tasks:
                self.logger.info(f"🧹 Cancelling {len(tasks)} background tasks...")
                for task in tasks:
                    task.cancel()

                # Wait for tasks to cancel
                await asyncio.gather(*tasks, return_exceptions=True)

            self.logger.info("✅ Graceful shutdown completed")

        except Exception as e:
            self.logger.error(f"❌ Error during shutdown: {e}")

    def print_startup_banner(self) -> None:
        """Print the startup banner with system information."""
        banner = f"""
🐝 Agent Cellphone V2 - Discord Bot Runner
==========================================

📅 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
🏠 Repo: {self.repo_root}
📝 Log Level: INFO
🔄 Auto-reconnection: Enabled
⚡ Max Retries: 10

🌐 Discord Integration Status:
   • Token: {'✅ Set' if os.getenv('DISCORD_BOT_TOKEN') else '❌ Missing'}
   • Guild ID: {'✅ Set' if os.getenv('DISCORD_GUILD_ID') else '❌ Missing'}
   • Libraries: {'✅ discord.py available' if DISCORD_AVAILABLE else '❌ discord.py missing'}

⚙️ Bot Configuration:
   • Intents: All enabled
   • Message Content: Enabled
   • Auto-reconnection: Exponential backoff (5s to 5min)

==========================================
        """

        print(banner)

    async def run(self) -> int:
        """
        Main entry point to run the bot runner service.

        Returns:
            Exit code (0 for success, 1 for failure)
        """
        try:
            # Print startup banner
            self.print_startup_banner()

            # Setup logging
            self.setup_logging()

            # Validate environment
            if not self.validate_environment():
                return 1

            # Create bot instance
            bot = self.create_bot_instance()
            if not bot:
                return 1

            # Run bot with reconnection logic
            return await self.run_bot_with_reconnection(bot)

        except KeyboardInterrupt:
            self.logger.info("🛑 Shutdown requested")
            return 0

        except Exception as e:
            self.logger.error(f"❌ Fatal error: {e}")
            return 1

# Global service instance
def create_bot_runner_service(repo_root: Optional[Path] = None) -> BotRunnerService:
    """Create a bot runner service instance."""
    if repo_root is None:
        repo_root = Path(__file__).resolve().parents[2]
    return BotRunnerService(repo_root)

__all__ = [
    "BotRunnerService",
    "create_bot_runner_service"
]