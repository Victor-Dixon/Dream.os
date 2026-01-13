#!/usr/bin/env python3
"""
Consolidated Discord Bot Entrypoint
===================================

Single entrypoint for the unified Discord bot system.
All Discord functionality consolidated into one bot instance.

Agent-3 (Infrastructure & DevOps) - 2026-01-10
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

def main():
    """Main entrypoint for consolidated Discord bot."""
    try:
        from src.discord_commander.unified_discord_bot import main as discord_main
        discord_main()
    except ImportError as e:
        print(f"❌ Failed to import unified Discord bot: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n🛑 Discord bot shutdown requested")
        sys.exit(0)
    except Exception as e:
        print(f"💥 Discord bot crashed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
