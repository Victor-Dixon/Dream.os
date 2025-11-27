#!/usr/bin/env python3
"""
Run Discord Bot with Auto-Restart Support
==========================================

Enhanced runner script that supports !restart command.
When !restart is used, bot gracefully shuts down and automatically restarts.

Author: Agent-6 (Co-Captain) - Implementation
Spec: Agent-2 (Architecture LEAD)
Date: 2025-10-15
"""

import os
import sys
import time
from pathlib import Path

def main():
    """Main loop with auto-restart support."""
    print("🚀 Discord Bot Runner with Auto-Restart")
    print("🐝 WE. ARE. SWARM.\n")
    
    restart_flag = Path('.discord_bot_restart')
    crash_count = 0
    max_crashes = 3
    crash_cooldown = 10  # seconds
    
    while True:
        # Run bot
        print("▶️  Starting Discord bot...")
        exit_code = run_bot()
        
        # Check for restart flag (intentional restart via !restart command)
        if restart_flag.exists():
            # Restart requested via !restart command
            restart_flag.unlink()  # Remove flag file
            crash_count = 0  # Reset crash count on intentional restart
            print("\n🔄 Restart requested - restarting in 3 seconds...")
            time.sleep(3)
            continue  # Restart loop
        
        # Check if bot crashed (non-zero exit code)
        if exit_code != 0:
            crash_count += 1
            print(f"\n⚠️  Bot crashed (exit code: {exit_code})")
            print(f"   Crash count: {crash_count}/{max_crashes}")
            
            if crash_count >= max_crashes:
                print(f"\n❌ Bot crashed {max_crashes} times in a row!")
                print("   Stopping auto-restart to prevent infinite loop.")
                print("   Please investigate the issue before restarting manually.")
                break
            
            print(f"   Waiting {crash_cooldown} seconds before restart...")
            time.sleep(crash_cooldown)
            continue  # Restart after cooldown
        
        # Normal exit (from !shutdown or clean exit)
        print("\n👋 Bot shutdown complete")
        break


def run_bot():
    """Run the Discord bot and return exit code."""
    try:
        import sys
        from pathlib import Path
        
        # CRITICAL: Import discord package BEFORE adding project root to path
        # This prevents local tools/discord/ from shadowing the discord.py package
        try:
            import discord
            import discord.ext
            # Verify it's the installed package, not local
            assert hasattr(discord, 'Client'), "discord module is not the installed package"
        except (ImportError, AssertionError):
            # If import fails, we'll try again after path setup
            pass
        
        # Add project root to Python path
        # Insert at position 1 (after current directory) to prioritize installed packages
        project_root = Path(__file__).parent.parent
        project_root_str = str(project_root)
        if project_root_str not in sys.path:
            # Insert at position 1 to prioritize installed packages over local directories
            sys.path.insert(1, project_root_str)
        
        import asyncio
        from src.discord_commander.unified_discord_bot import main as bot_main
        
        # Run bot (will block until shutdown or restart)
        asyncio.run(bot_main())
        
        return 0  # Clean exit
        
    except KeyboardInterrupt:
        print("\n⚠️  Bot interrupted by user (Ctrl+C)")
        return 1
        
    except ImportError as e:
        print(f"\n❌ Import error: {e}")
        print("💡 Make sure discord.py is installed: pip install discord.py")
        import traceback
        traceback.print_exc()
        return 1
        
    except Exception as e:
        print(f"\n❌ Bot error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Runner shutdown by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n💥 Fatal error in runner: {e}")
        sys.exit(1)

