#!/usr/bin/env python3
"""
Unified Discord Bot - Backward Compatibility Shim
==================================================

<!-- SSOT Domain: web -->

Backward compatibility shim for unified_discord_bot.py.
All functionality has been extracted to modular files for V2 compliance.

V2 Compliance | Author: Agent-1 | Date: 2025-12-14
"""

from __future__ import annotations

import asyncio
import logging
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING

# Add project root to path FIRST (before any src imports)
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

<<<<<<< HEAD
# Load environment variables from .env files
try:
    from dotenv import load_dotenv
    # Load main .env file first
    load_dotenv()
    # Then load Discord-specific configuration
    load_dotenv('.env.discord')
    print("✅ Environment variables loaded from .env and .env.discord")
=======
# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
except ImportError:
    print("⚠️  python-dotenv not installed. Install with: pip install python-dotenv")
    print("⚠️  Continuing without .env support...")

# Discord imports
<<<<<<< HEAD
import warnings
# Suppress the audioop deprecation warning from discord.py
warnings.filterwarnings("ignore", message="'audioop' is deprecated", category=DeprecationWarning)

=======
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
try:
    import discord
    from discord.ext import commands
    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False
    print("❌ discord.py not installed! Run: pip install discord.py")
    sys.exit(1)

# Import extracted managers
from src.services.unified_messaging_service import UnifiedMessagingService
from src.discord_commander.discord_gui_controller import DiscordGUIController
from src.discord_commander.handlers.discord_event_handlers import DiscordEventHandlers
from src.discord_commander.lifecycle.bot_lifecycle import BotLifecycleManager
from src.discord_commander.integrations.service_integration_manager import ServiceIntegrationManager
from src.discord_commander.config.bot_config import BotConfig

if TYPE_CHECKING:
    from src.infrastructure.browser.thea_browser_service import TheaBrowserService

logger = logging.getLogger(__name__)


class UnifiedDiscordBot(commands.Bot):
    """Single unified Discord bot - backward compatibility shim."""

<<<<<<< HEAD
    def __init__(self, token: str, channel_id: int | None = None, dry_run: bool = False):
        """Initialize unified Discord bot with modular components."""
        # Initialize logger first
        self.logger = logging.getLogger(__name__)

        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        intents.members = True  # Privileged intent - requires Discord app approval
        intents.voice_states = True

        # Validate intents configuration
        self._validate_intents(intents)

=======
    def __init__(self, token: str, channel_id: int | None = None):
        """Initialize unified Discord bot with modular components."""
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        intents.members = True
        intents.voice_states = True

>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
        super().__init__(command_prefix="!", intents=intents, help_command=None)

        # Store basic configuration
        self.token = token
        self.channel_id = channel_id
<<<<<<< HEAD
        self.dry_run = dry_run
=======
        self.logger = logging.getLogger(__name__)
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console

        # Initialize core services
        self.messaging_service = UnifiedMessagingService()
        self.gui_controller = DiscordGUIController(self.messaging_service)

        # Connection health tracking
        self.last_heartbeat = time.time()
        self.connection_healthy = False

        # Initialize modular components
        self.config = BotConfig(self)
        self.lifecycle = BotLifecycleManager(self)
        self.event_handlers = DiscordEventHandlers(self)
        self.services = ServiceIntegrationManager(self)

        # Preserve properties for backward compatibility
        self.discord_user_map = self.config.discord_user_map
        self.thea_min_interval_minutes = self.services.thea_min_interval_minutes

<<<<<<< HEAD
    def _validate_intents(self, intents: discord.Intents):
        """Validate Discord intents configuration and warn about privileged intents."""
        privileged_intents = []

        if intents.members:
            privileged_intents.append("members")
        if intents.message_content:
            privileged_intents.append("message_content")
        if intents.guilds and intents.members:  # members intent requires guilds
            pass  # This is expected

        if privileged_intents:
            self.logger.warning(f"⚠️  Bot is configured to use privileged intents: {', '.join(privileged_intents)}")
            self.logger.warning("   These must be enabled in your Discord application:")
            self.logger.warning("   https://discord.com/developers/applications/")
            self.logger.warning("   Bot Settings → Privileged Gateway Intents")
            self.logger.warning("   Enable: 'Server Members Intent' and 'Message Content Intent'")

    async def validate_connection(self) -> bool:
        """
        Validate Discord connection without starting the full bot.
        Returns True if connection test passes, False otherwise.
        """
        try:
            # Test token validity by attempting a minimal connection
            # This will fail with PrivilegedIntentsRequired if intents aren't enabled
            await self.login(self.token)

            # If login succeeds, logout immediately (dry-run success)
            await self.close()
            self.logger.info("✅ Discord connection validation successful (dry-run)")
            return True

        except discord.PrivilegedIntentsRequired as e:
            self.logger.error("❌ Privileged intents required but not enabled in Discord app")
            self.logger.error("   Required intents: members, message_content")
            self.logger.error("   Enable at: https://discord.com/developers/applications/")
            self.logger.error("   Bot Settings → Privileged Gateway Intents")
            return False

        except discord.LoginFailure as e:
            self.logger.error(f"❌ Invalid Discord token: {e}")
            return False

        except Exception as e:
            self.logger.error(f"❌ Discord connection validation failed: {e}")
            return False

=======
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
    # Event handler delegations
    async def on_ready(self):
        """Handle bot ready event."""
        print(f"🔍 DEBUG: Bot on_ready event triggered! Connected as {self.user}")
        await self.event_handlers.handle_on_ready()

    async def on_message(self, message: discord.Message):
        """Handle incoming messages."""
        await self.event_handlers.handle_on_message(message)

    async def on_disconnect(self):
        """Handle bot disconnection."""
        await self.event_handlers.handle_on_disconnect()

    async def on_resume(self):
        """Handle bot reconnection."""
        await self.event_handlers.handle_on_resume()

    async def on_socket_raw_receive(self, msg):
        """Track connection health."""
        await self.event_handlers.handle_on_socket_raw_receive(msg)

    async def on_error(self, event: str, *args, **kwargs):
        """Handle errors in event handlers."""
        await self.event_handlers.handle_on_error(event, *args, **kwargs)

    # Lifecycle delegations
    async def setup_hook(self):
        """Setup hook for bot initialization."""
        await self.lifecycle.setup_hook()

    async def send_startup_message(self):
        """Send startup message."""
        await self.lifecycle.send_startup_message()

    async def close(self):
        """Clean shutdown."""
        await self.lifecycle.close()
        await super().close()

    # Service delegations
    def _get_thea_service(self, headless: bool = True) -> "TheaBrowserService":
        """Get Thea browser service."""
        return self.services.get_thea_service(headless)

    async def ensure_thea_session(
        self, allow_interactive: bool, min_interval_minutes: int | None = None
    ) -> bool:
        """Ensure Thea session is active."""
        return await self.services.ensure_thea_session(allow_interactive, min_interval_minutes)

    # Configuration delegations
    def _get_developer_prefix(self, discord_user_id: str) -> str:
        """Get developer prefix from Discord user ID mapping."""
        return self.config.get_developer_prefix(discord_user_id)

    def _load_discord_user_map(self) -> dict[str, str]:
        """Load Discord user ID to developer name mapping (backward compatibility)."""
        return self.config.discord_user_map


<<<<<<< HEAD
# Main entry point for unified Discord bot
def main():
    """Main entry point for the unified Discord bot."""
    if not DISCORD_AVAILABLE:
        print("❌ discord.py not available. Install with: pip install discord.py")
        return

    import asyncio

    async def run_bot():
        """Run the Discord bot with proper async handling."""
        try:
            # Get Discord token from environment
            token = os.getenv('DISCORD_BOT_TOKEN')
            if not token:
                print("❌ DISCORD_BOT_TOKEN not found in environment variables")
                print("   Please set your Discord bot token: export DISCORD_BOT_TOKEN=your_token_here")
                return

            # Create bot instance
            bot = UnifiedDiscordBot(token)

            # Start the bot
            print("🤖 Starting unified Discord bot...")
            await bot.start(token)

        except KeyboardInterrupt:
            print("\n🛑 Bot shutdown requested by user")
        except Exception as e:
            print(f"💥 Bot crashed: {e}")

    # Run the bot
    asyncio.run(run_bot())

if __name__ == "__main__":
    main()
=======
# Main entry point moved to bot_runner.py for V2 compliance
if __name__ == "__main__":
    from src.discord_commander.bot_runner import main
    import asyncio
    import sys
    
    if not DISCORD_AVAILABLE:
        print("❌ discord.py not available. Install with: pip install discord.py")
        sys.exit(1)
    
    exit_code = asyncio.run(main())
    sys.exit(exit_code if exit_code is not None else 0)
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
