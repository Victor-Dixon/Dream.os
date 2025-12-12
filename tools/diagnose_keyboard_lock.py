#!/usr/bin/env python3
"""
Keyboard Lock Diagnostics Tool
==============================

Diagnoses and fixes keyboard lock issues.

Usage:
    python tools/diagnose_keyboard_lock.py          # Check status
    python tools/diagnose_keyboard_lock.py --force  # Force release if stuck
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.core.keyboard_control_lock import (
    is_locked,
    get_current_holder,
    get_lock_status,
    force_release_lock,
)


def main():
    """Diagnose and optionally fix keyboard lock issues."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Diagnose and fix keyboard lock issues"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force release lock if stuck"
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Show detailed lock status"
    )
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("🔍 KEYBOARD LOCK DIAGNOSTICS")
    print("=" * 70)
    print()
    
    # Get lock status
    status = get_lock_status()
    
    print("📊 Lock Status:")
    print(f"   Locked: {'🔒 YES' if status['locked'] else '🔓 NO'}")
    print(f"   Current Holder: {status['current_holder'] or 'None'}")
    print(f"   Timeout: {status['timeout_seconds']}s")
    print()
    
    if status['locked']:
        print("⚠️  Lock is currently held!")
        if status['current_holder']:
            print(f"   Holder: {status['current_holder']}")
            print("   This may be normal if:")
            print("   - Queue processor is delivering a message")
            print("   - Soft onboarding is in progress")
            print("   - Discord bot is sending a message")
        else:
            print("   ⚠️  WARNING: Lock is held but holder is None!")
            print("   This indicates a potential stuck lock.")
        
        print()
        
        if args.force:
            print("🔧 Force releasing lock...")
            if force_release_lock():
                print("✅ Lock force released successfully!")
                print()
                # Re-check status
                new_status = get_lock_status()
                print("📊 New Status:")
                print(f"   Locked: {'🔒 YES' if new_status['locked'] else '🔓 NO'}")
                return 0
            else:
                print("❌ Failed to force release lock")
                print("   You may need to restart the queue processor or Discord bot")
                return 1
        else:
            print("💡 To force release stuck lock, run:")
            print("   python tools/diagnose_keyboard_lock.py --force")
            return 1
    else:
        print("✅ Lock is free - no issues detected")
        return 0


if __name__ == "__main__":
    sys.exit(main())

