#!/usr/bin/env python3
"""
Check System Updates

Simple script for agents to check for system-wide updates and announcements.

Usage:
    python scripts/check_system_updates.py
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def check_system_updates():
    """Check for system updates in agent_workspaces."""
    updates_file = project_root / "agent_workspaces" / "SYSTEM_UPDATES.md"
    
    if not updates_file.exists():
        print("ℹ️  No system updates file found.")
        return
    
    print("=" * 70)
    print("📢 SYSTEM UPDATES")
    print("=" * 70)
    print()
    
    with open(updates_file, 'r', encoding='utf-8') as f:
        content = f.read()
        print(content)
    
    print()
    print("=" * 70)
    print(f"📄 Full file: {updates_file}")
    print("=" * 70)

if __name__ == "__main__":
    check_system_updates()

