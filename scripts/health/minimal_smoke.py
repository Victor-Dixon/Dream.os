#!/usr/bin/env python3
"""
Minimal Smoke Test - Import validation for core systems
=======================================================

Tests basic imports for the three core systems during recovery.
Used for git bisect to identify when systems broke.

Exit codes:
0 = All imports successful
1 = One or more imports failed

Author: Agent-3 (Infrastructure & DevOps Recovery)
Date: 2026-01-09
"""

import sys
import importlib
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

def test_import(module_name: str) -> bool:
    """Test if a module can be imported."""
    try:
        importlib.import_module(module_name)
        print(f"✅ {module_name}")
        return True
    except ImportError as e:
        print(f"❌ {module_name}: {e}")
        return False
    except Exception as e:
        print(f"❌ {module_name}: {e}")
        return False

def main():
    """Run minimal import tests."""
    print("🔍 Minimal import smoke test...")

    systems = [
        'src.discord_commander.unified_discord_bot',
        'src.services.twitch.twitch_bot',  # Assuming this is the twitch module
        'src.services.messaging.unified_messaging'  # Assuming this is the agent messaging module
    ]

    failed_systems = []

    for system in systems:
        if not test_import(system):
            failed_systems.append(system)

    if failed_systems:
        print(f"\n💥 FAILED SYSTEMS: {len(failed_systems)}")
        for system in failed_systems:
            print(f"  - {system}")
        return 1
    else:
        print("\n🎉 ALL IMPORTS SUCCESSFUL")
        return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)