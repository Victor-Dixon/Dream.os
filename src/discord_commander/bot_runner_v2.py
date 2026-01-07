"""
Bot Runner V2 - Agent Cellphone V2
==================================

SSOT Domain: discord

Refactored Discord bot runner using service architecture for V2 compliance.

Features:
- Bot lifecycle management
- Automatic reconnection with backoff
- Environment validation
- Logging and error handling

V2 Compliant: Yes (<300 lines)
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2026-01-07
"""

import asyncio
import sys
from pathlib import Path

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    # Prefer repo-root .env regardless of current working directory
    repo_root = Path(__file__).resolve().parents[2]
    load_dotenv(dotenv_path=repo_root / ".env")
except ImportError:
    print("⚠️  python-dotenv not installed. Install with: pip install python-dotenv")
    print("⚠️  Continuing without .env support...")
    repo_root = Path(__file__).resolve().parents[2]

# Import bot runner service
from .bot_runner_service import create_bot_runner_service

async def main() -> int:
    """
    Main entry point for running the Discord bot.

    This function handles:
    - Environment setup and validation
    - Bot initialization and configuration
    - Automatic reconnection with exponential backoff
    - Graceful shutdown handling
    - Comprehensive logging

    Returns:
        Exit code (0 for success, 1 for failure)
    """
    try:
        # Create and run the bot runner service
        bot_runner = create_bot_runner_service(repo_root)
        return await bot_runner.run()

    except KeyboardInterrupt:
        print("\n🛑 Bot shutdown requested by user")
        return 0

    except Exception as e:
        print(f"❌ Fatal error in main: {e}")
        return 1

def run_bot():
    """
    Synchronous wrapper to run the async main function.

    This is the entry point that should be called from external scripts.
    """
    try:
        return asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Bot shutdown requested")
        return 0

if __name__ == "__main__":
    """
    Direct execution entry point.

    Allows the bot runner to be executed directly:
    python src/discord_commander/bot_runner_v2.py
    """
    sys.exit(run_bot())