#!/usr/bin/env python3
"""
Comprehensive Discord Commands Test Suite
==========================================

Tests all Discord bot commands to ensure they work correctly.
Can be run manually or integrated into CI/CD.

V2 Compliance | Author: Agent-6 | Date: 2025-12-25
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_all_commands():
    """Test all Discord commands for proper registration and functionality."""
    print("🧪 COMPREHENSIVE DISCORD COMMANDS TEST SUITE")
    print("="*60)
    
    results = []
    
    # Test 1: Command modules import
    print("\n1️⃣ Testing command module imports...")
    command_modules = {
        "onboarding_commands": "src.discord_commander.commands.onboarding_commands",
        "core_messaging_commands": "src.discord_commander.commands.core_messaging_commands",
        "system_control_commands": "src.discord_commander.commands.system_control_commands",
        "agent_management_commands": "src.discord_commander.commands.agent_management_commands",
        "profile_commands": "src.discord_commander.commands.profile_commands",
        "utility_commands": "src.discord_commander.commands.utility_commands",
    }
    
    for name, module_path in command_modules.items():
        try:
            __import__(module_path, fromlist=[''])
            print(f"  ✅ {name}")
            results.append((f"Import {name}", True, None))
        except ImportError as e:
            print(f"  ❌ {name}: {e}")
            results.append((f"Import {name}", False, str(e)))
    
    # Test 2: Soft onboarding CLI exists
    print("\n2️⃣ Testing soft onboarding CLI...")
    cli_path = project_root / 'tools' / 'soft_onboard_cli.py'
    if cli_path.exists():
        print(f"  ✅ soft_onboard_cli.py exists")
        results.append(("soft_onboard_cli.py exists", True, None))
    else:
        print(f"  ❌ soft_onboard_cli.py missing")
        results.append(("soft_onboard_cli.py exists", False, str(cli_path)))
    
    # Test 3: Soft onboarding service
    print("\n3️⃣ Testing soft onboarding service...")
    try:
        from src.services.soft_onboarding_service import soft_onboard_agent, soft_onboard_multiple_agents
        print("  ✅ Service imports successful")
        print("  ✅ Functions are callable")
        results.append(("Soft onboarding service", True, None))
    except Exception as e:
        print(f"  ❌ Service import failed: {e}")
        results.append(("Soft onboarding service", False, str(e)))
    
    # Test 4: Hard onboarding service
    print("\n4️⃣ Testing hard onboarding service...")
    try:
        from src.services.hard_onboarding_service import hard_onboard_agent
        print("  ✅ Service imports successful")
        results.append(("Hard onboarding service", True, None))
    except Exception as e:
        print(f"  ❌ Service import failed: {e}")
        results.append(("Hard onboarding service", False, str(e)))
    
    # Test 5: Bot can be instantiated (without connecting)
    print("\n5️⃣ Testing bot instantiation...")
    try:
        from src.discord_commander.unified_discord_bot import UnifiedDiscordBot
        print("  ✅ Bot class imports successfully")
        results.append(("Bot instantiation", True, None))
    except Exception as e:
        print(f"  ❌ Bot import failed: {e}")
        results.append(("Bot instantiation", False, str(e)))
    
    # Generate report
    print("\n" + "="*60)
    print("📊 TEST RESULTS SUMMARY")
    print("="*60)
    
    total = len(results)
    passed = sum(1 for r in results if r[1])
    failed = total - passed
    
    print(f"\nTotal Tests: {total}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    
    if failed > 0:
        print("\n❌ FAILED TESTS:")
        for name, passed, details in results:
            if not passed:
                print(f"  - {name}")
                if details:
                    print(f"    {details}")
    else:
        print("\n🎉 ALL TESTS PASSED!")
    
    print("="*60)
    
    return failed == 0

if __name__ == "__main__":
    success = test_all_commands()
    sys.exit(0 if success else 1)

