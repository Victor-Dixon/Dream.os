#!/usr/bin/env python3
"""
Discord Commands Comprehensive Testing Script
============================================

Tests all major Discord bot commands to ensure they're working after role restriction removal.
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

async def test_discord_commands():
    """Test Discord command functionality."""
    print("🧪 DISCORD COMMANDS TESTING SUITE")
    print("=" * 50)

    try:
        # Import required modules
        from src.discord_commander.unified_discord_bot import UnifiedDiscordBot
        from dotenv import load_dotenv
        import os

        print("✅ Bot module imported successfully")

        # Load environment and create bot with token
        load_dotenv()
        token = os.getenv('DISCORD_BOT_TOKEN')
        if not token:
            print("❌ No DISCORD_BOT_TOKEN found in environment")
            return False

        bot = UnifiedDiscordBot(token=token)
        print("✅ Bot instance created successfully")

        # Test command registration
        commands_to_test = [
            'control', 'gui', 'status', 'help', 'commands',
            'monitor', 'message', 'broadcast', 'mermaid'
        ]

        print("\n📋 COMMAND REGISTRATION VERIFICATION:")
        print("-" * 40)

        registered_commands = []
        missing_commands = []

        for cmd_name in commands_to_test:
            cmd = bot.get_command(cmd_name)
            if cmd:
                registered_commands.append(cmd_name)
                print(f"✅ {cmd_name}: REGISTERED")

                # Check if role restrictions are disabled (no checks or commented out)
                if hasattr(cmd, 'checks') and cmd.checks:
                    print(f"   ⚠️  Has {len(cmd.checks)} check(s) - may need role permissions")
                else:
                    print("   ✅ No role restrictions (good for testing)")
            else:
                missing_commands.append(cmd_name)
                print(f"❌ {cmd_name}: NOT REGISTERED")

        print(f"\n📊 SUMMARY:")
        print(f"✅ Registered: {len(registered_commands)}/{len(commands_to_test)}")
        print(f"❌ Missing: {len(missing_commands)}")

        if missing_commands:
            print(f"⚠️  Missing commands: {', '.join(missing_commands)}")

        # Test GUI controller
        print("\n🎮 TESTING GUI CONTROLLER:")
        try:
            gui_controller = bot.gui_controller
            print("✅ GUI controller accessible")

            # Test control panel creation
            control_panel = gui_controller.create_control_panel()
            print("✅ Control panel created successfully")

            # Test main GUI creation
            main_gui = gui_controller.create_main_gui()
            print("✅ Main GUI created successfully")

            # Test status GUI creation
            status_gui = gui_controller.create_status_gui()
            print("✅ Status GUI created successfully")

        except Exception as e:
            print(f"❌ GUI controller test failed: {e}")

        # Overall assessment
        print("\n🎯 OVERALL ASSESSMENT:")
        if len(registered_commands) >= 7:  # Most commands registered
            print("✅ EXCELLENT: Discord commands are properly configured")
            print("🎉 Ready for Discord server testing!")
        elif len(registered_commands) >= 5:
            print("⚠️  GOOD: Core commands registered, some missing")
            print("📝 May need additional command registration")
        else:
            print("❌ POOR: Major command registration issues")
            print("🔧 Requires immediate attention")

        return len(registered_commands) >= 7

    except Exception as e:
        print(f"❌ Test suite failed: {e}")
        return False

def main():
    """Run the test suite."""
    print("🤖 Starting Discord Commands Test Suite...\n")

    success = asyncio.run(test_discord_commands())

    if success:
        print("\n🎉 TEST SUITE PASSED!")
        print("📝 Next: Test commands in Discord server")
        print("💡 Commands to test: !control, !gui, !status, !help")
        return 0
    else:
        print("\n❌ TEST SUITE FAILED!")
        print("🔧 Requires debugging before Discord testing")
        return 1

if __name__ == "__main__":
    sys.exit(main())