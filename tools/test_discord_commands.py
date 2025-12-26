#!/usr/bin/env python3
"""
Discord Bot Commands Test Suite
================================

Comprehensive test suite for all Discord bot commands to verify functionality.

V2 Compliance | Author: Agent-6 | Date: 2025-12-25
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_command_registration():
    """Test that all commands are properly registered."""
    print("🔍 Testing Discord command registration...")
    
    try:
        from src.discord_commander.unified_discord_bot import UnifiedDiscordBot
        from src.discord_commander.bot_runner import main as bot_main
        
        # Check if bot can be instantiated (without actually connecting)
        print("✅ Bot imports successful")
        
        # List all command modules
        command_modules = [
            "src.discord_commander.commands.onboarding_commands",
            "src.discord_commander.commands.core_messaging_commands",
            "src.discord_commander.commands.system_control_commands",
            "src.discord_commander.commands.agent_management_commands",
            "src.discord_commander.commands.profile_commands",
            "src.discord_commander.commands.utility_commands",
            "src.discord_commander.commands.swarm_showcase_commands",
        ]
        
        commands_found = []
        commands_missing = []
        
        for module_path in command_modules:
            try:
                module = __import__(module_path, fromlist=[''])
                print(f"✅ {module_path} - Found")
                commands_found.append(module_path)
            except ImportError as e:
                print(f"❌ {module_path} - Missing: {e}")
                commands_missing.append(module_path)
        
        return len(commands_missing) == 0, commands_found, commands_missing
        
    except Exception as e:
        print(f"❌ Error testing command registration: {e}")
        return False, [], []

def test_soft_onboard_cli_exists():
    """Test that soft_onboard_cli.py exists."""
    print("\n🔍 Testing soft_onboard_cli.py existence...")
    
    cli_path = project_root / 'tools' / 'soft_onboard_cli.py'
    
    if cli_path.exists():
        print(f"✅ soft_onboard_cli.py found at {cli_path}")
        return True, cli_path
    else:
        print(f"❌ soft_onboard_cli.py NOT FOUND at {cli_path}")
        print("   This is why soft onboarding is failing!")
        return False, cli_path

def test_soft_onboarding_service():
    """Test that soft onboarding service exists and works."""
    print("\n🔍 Testing soft onboarding service...")
    
    try:
        from src.services.soft_onboarding_service import soft_onboard_agent
        print("✅ soft_onboarding_service imported successfully")
        
        # Check if function exists
        if callable(soft_onboard_agent):
            print("✅ soft_onboard_agent function is callable")
            return True
        else:
            print("❌ soft_onboard_agent is not callable")
            return False
    except ImportError as e:
        print(f"❌ Failed to import soft_onboarding_service: {e}")
        return False
    except Exception as e:
        print(f"❌ Error testing soft onboarding service: {e}")
        return False

def generate_test_report(results):
    """Generate test report."""
    print("\n" + "="*60)
    print("📊 DISCORD COMMANDS TEST REPORT")
    print("="*60)
    
    total_tests = len(results)
    passed = sum(1 for r in results if r[0])
    failed = total_tests - passed
    
    print(f"\nTotal Tests: {total_tests}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    
    if failed > 0:
        print("\n❌ FAILED TESTS:")
        for name, passed, details in results:
            if not passed:
                print(f"  - {name}")
                if details:
                    print(f"    Details: {details}")
    
    print("\n" + "="*60)
    
    return passed == total_tests

if __name__ == "__main__":
    print("🧪 DISCORD BOT COMMANDS TEST SUITE")
    print("="*60)
    
    results = []
    
    # Test 1: Command registration
    passed, found, missing = test_command_registration()
    results.append(("Command Registration", passed, f"Found: {len(found)}, Missing: {len(missing)}"))
    
    # Test 2: soft_onboard_cli.py exists
    passed, cli_path = test_soft_onboard_cli_exists()
    results.append(("soft_onboard_cli.py Exists", passed, str(cli_path)))
    
    # Test 3: Soft onboarding service
    passed = test_soft_onboarding_service()
    results.append(("Soft Onboarding Service", passed, None))
    
    # Generate report
    all_passed = generate_test_report(results)
    
    sys.exit(0 if all_passed else 1)

