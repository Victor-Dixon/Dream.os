#!/usr/bin/env python3
"""
Discord Bot Runner
==================

Entry point for running the Discord bot with automatic reconnection.

V2 Compliance | Author: Agent-1 | Date: 2025-12-14
"""

import asyncio
import logging
import os
import sys
from datetime import datetime
from pathlib import Path

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("⚠️  python-dotenv not installed. Install with: pip install python-dotenv")
    print("⚠️  Continuing without .env support...")

try:
    import discord
    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False
    print("❌ discord.py not installed! Run: pip install discord.py")
    sys.exit(1)

from src.discord_commander.unified_discord_bot import UnifiedDiscordBot

logger = logging.getLogger(__name__)


async def main() -> int:
    """Main function to run the unified Discord bot with automatic reconnection."""
    # Setup logging with file output for debugging
    log_dir = Path("runtime/logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / f"discord_bot_{datetime.now().strftime('%Y%m%d')}.log"

    # Configure logging with both console and file handlers
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(log_file, encoding='utf-8')
        ]
    )

    logger.info(f"📝 Logging to file: {log_file}")

    # Get token from environment
    token = os.getenv("DISCORD_BOT_TOKEN")
    print(f"🔍 DEBUG: Checking for DISCORD_BOT_TOKEN...")
    print(f"🔍 DEBUG: Token found: {'YES' if token else 'NO'}")
    if token:
        print(f"🔍 DEBUG: Token length: {len(token)} characters")
        print(f"🔍 DEBUG: Token starts with: {token[:20]}..." if len(token) > 20 else f"🔍 DEBUG: Token: {token}")

    if not token:
        print("❌ DISCORD_BOT_TOKEN not set in environment!")
        print("   Set it with: $env:DISCORD_BOT_TOKEN='your_token' (Windows)")
        print("   Or add to .env file")
        sys.exit(1)

    # Get channel ID (optional)
    channel_id = os.getenv("DISCORD_CHANNEL_ID")
    if channel_id:
        try:
            channel_id = int(channel_id)
        except ValueError:
            print(f"⚠️  Invalid DISCORD_CHANNEL_ID: {channel_id}")
            channel_id = None

    # Create bot instance
    print(f"🔍 DEBUG: Creating UnifiedDiscordBot instance...")
    bot = UnifiedDiscordBot(token=token, channel_id=channel_id)
    print(f"🔍 DEBUG: Bot instance created successfully")

    # Enhanced reconnection settings for network stability
    max_reconnect_attempts = 999999
    base_delay = 5
    max_delay = 300
    reconnect_delay = base_delay
    reconnect_count = 0
    consecutive_failures = 0
    max_consecutive_failures = 10

    # Network health tracking
    network_failures = 0
    max_network_failures = 5
    last_successful_connection = None

    print("🚀 Starting Discord Commander...")
    print("🐝 WE. ARE. SWARM.")
    print("🔄 Auto-reconnect enabled - bot will automatically reconnect on internet outage\n")

    while reconnect_count < max_reconnect_attempts:
        try:
            if reconnect_count > 0:
                logger.info(f"🔄 Reconnection attempt {reconnect_count} (delay: {reconnect_delay}s)")
                await asyncio.sleep(reconnect_delay)

            logger.info("🔌 Connecting to Discord...")
            print(f"🔍 DEBUG: About to call bot.start(token)...")
            try:
                await bot.start(token)
            except Exception as runtime_error:
                logger.error(
                    f"❌ Runtime error during bot operation: {runtime_error}\n"
                    f"   Attempt {reconnect_count + 1}, consecutive failures: {consecutive_failures + 1}\n"
                    f"   Retrying in {reconnect_delay} seconds...",
                    exc_info=True
                )
                consecutive_failures += 1
                reconnect_count += 1

                # Special handling for rate limiting
                if "429" in str(runtime_error) or "rate limit" in str(runtime_error).lower():
                    logger.warning("🚦 Rate limiting detected - implementing backoff strategy...")
                    reconnect_delay = min(max_delay, reconnect_delay * 3)  # More aggressive backoff for rate limits
                    consecutive_failures = max_consecutive_failures  # Force longer delay

                    # Add rate limit recovery delay
                    import time
                    logger.info("⏳ Waiting 30 seconds for rate limit recovery...")
                    time.sleep(30)
                else:
                    if consecutive_failures >= max_consecutive_failures:
                        reconnect_delay = min(max_delay, reconnect_delay * 2)
                    else:
                        reconnect_delay = min(max_delay, reconnect_delay * 1.5)

                import random
                jitter = random.uniform(0.8, 1.2)
                reconnect_delay = int(reconnect_delay * jitter)

                try:
                    await bot.close()
                except Exception as close_error:
                    logger.error(f"Error closing bot after runtime error: {close_error}", exc_info=True)

                continue

            # Check if intentional shutdown
            if hasattr(bot, '_intentional_shutdown') and bot._intentional_shutdown:
                logger.info("✅ Bot shutdown requested - exiting cleanly")
                return 0

            # Reset network failure counter on successful connection
            if last_successful_connection is None:
                last_successful_connection = datetime.now()
                logger.info(f"🎉 First successful connection at {last_successful_connection}")
            else:
                last_successful_connection = datetime.now()
                network_failures = 0  # Reset on successful connection

            logger.warning("⚠️ Bot disconnected - will reconnect in next iteration")
            reconnect_count += 1
            consecutive_failures = 0
            reconnect_delay = base_delay

        except KeyboardInterrupt:
            print("\n🛑 Bot stopped by user")
            logger.info("🛑 Bot stopped by user (KeyboardInterrupt)")
            bot._intentional_shutdown = True
            try:
                await bot.close()
            except Exception as e:
                logger.error(f"Error closing bot on KeyboardInterrupt: {e}", exc_info=True)
            return 0

        except discord.LoginFailure as e:
            print(f"❌ Invalid Discord token: {e}")
            logger.error(f"Login failure: {e}")
            try:
                await bot.close()
            except Exception as e:
                logger.error(f"Error closing bot on login failure: {e}", exc_info=True)
            return 1

        except discord.PrivilegedIntentsRequired as e:
            print(f"❌ Missing required intents: {e}")
            logger.error(f"Intents error: {e}")
            try:
                await bot.close()
            except Exception as e:
                logger.error(f"Error closing bot on intents error: {e}", exc_info=True)
            return 1

        except discord.errors.ConnectionClosed as e:
            logger.warning(
                f"⚠️ Discord connection closed (code: {e.code}): {e}\n"
                f"   Attempt {reconnect_count + 1}, will reconnect..."
            )
            reconnect_count += 1
            consecutive_failures = 0

            try:
                await bot.close()
            except Exception as close_error:
                logger.error(f"Error closing bot after ConnectionClosed: {close_error}", exc_info=True)

            continue

        except (ConnectionError, OSError, asyncio.TimeoutError) as e:
            consecutive_failures += 1
            reconnect_count += 1
            network_failures += 1

            error_type = type(e).__name__
            logger.warning(
                f"⚠️ Network error ({error_type}): {e}\n"
                f"   Attempt {reconnect_count}, consecutive failures: {consecutive_failures}\n"
                f"   Network failures: {network_failures}/{max_network_failures}\n"
                f"   Retrying in {reconnect_delay} seconds..."
            )

            # If too many network failures, try a longer delay and reset
            if network_failures >= max_network_failures:
                logger.warning(f"🔄 Too many network failures ({network_failures}), resetting connection strategy...")
                reconnect_delay = max_delay  # Use maximum delay
                network_failures = 0
                consecutive_failures = 0

                # Add extra delay for network recovery
                import time
                logger.info("⏳ Waiting 60 seconds for network recovery...")
                time.sleep(60)
            else:
                if consecutive_failures >= max_consecutive_failures:
                    reconnect_delay = min(max_delay, reconnect_delay * 2)
                else:
                    reconnect_delay = min(max_delay, reconnect_delay * 1.5)

            import random
            jitter = random.uniform(0.8, 1.2)
            reconnect_delay = int(reconnect_delay * jitter)

            try:
                await bot.close()
            except Exception as e:
                logger.error(f"Error closing bot after network error: {e}", exc_info=True)

            continue

        except Exception as e:
            consecutive_failures += 1
            reconnect_count += 1

            logger.error(
                f"❌ Bot error: {e}\n"
                f"   Attempt {reconnect_count}, consecutive failures: {consecutive_failures}\n"
                f"   Retrying in {reconnect_delay} seconds...",
                exc_info=True
            )

            if consecutive_failures >= max_consecutive_failures:
                reconnect_delay = min(max_delay, reconnect_delay * 2)
            else:
                reconnect_delay = min(max_delay, reconnect_delay * 1.5)

            import random
            jitter = random.uniform(0.8, 1.2)
            reconnect_delay = int(reconnect_delay * jitter)

            try:
                await bot.close()
            except Exception as e:
                logger.error(f"Error closing bot after network error: {e}", exc_info=True)

            continue

    logger.error("❌ Max reconnection attempts reached")
    try:
        await bot.close()
    except Exception as e:
        logger.error(f"Error closing bot after max attempts: {e}", exc_info=True)
    return 1


if __name__ == "__main__":
    if not DISCORD_AVAILABLE:
        print("❌ discord.py not available. Install with: pip install discord.py")
        sys.exit(1)

    exit_code = asyncio.run(main())
    sys.exit(exit_code if exit_code is not None else 0)

