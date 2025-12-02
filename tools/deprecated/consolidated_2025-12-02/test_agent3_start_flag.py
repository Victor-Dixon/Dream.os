#!/usr/bin/env python3
"""
Test Script: Agent-3 Onboarding Coordinates via --start Flag
============================================================

Temporary script to test Agent-3's onboarding coordinates using --start flag.
This script will be deleted after confirmation that coordinates are correct.

Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2025-11-30
"""

import sys
import subprocess
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))


def test_agent3_with_start_flag():
    """Test sending message to Agent-3 using --start flag."""
    print("="*60)
    print("🧪 TESTING AGENT-3 ONBOARDING COORDINATES")
    print("="*60)
    print("\n📍 Agent-3 Onboarding Coordinates: [-1276, 680]")
    print("📝 Using --start flag to send message")
    print("\n⚠️  NOTE: --start flag may route to chat coordinates instead of onboarding")
    print("   If message appears at wrong location, coordinates may need adjustment")
    print("\n🚀 Sending message via --start flag...\n")
    
    # Use the messaging CLI with --start flag for Agent-3
    result = subprocess.run(
        [
            sys.executable,
            "-m", "src.services.messaging_cli",
            "--start", "3"
        ],
        cwd=project_root,
        capture_output=False,
        text=True
    )
    
    print("\n" + "="*60)
    if result.returncode == 0:
        print("✅ Message sent successfully!")
        print("📋 Please verify Agent-3 received the message")
        print("   - Expected onboarding location: [-1276, 680]")
        print("   - If message appears elsewhere, coordinates may need adjustment")
    else:
        print("❌ Message send failed")
        print(f"Exit code: {result.returncode}")
    print("="*60)
    
    return result.returncode == 0


if __name__ == "__main__":
    success = test_agent3_with_start_flag()
    sys.exit(0 if success else 1)

