#!/usr/bin/env python3
"""
Hard Onboard Any Agent - Quick Captain Tool
Generalized hard onboarding with custom messages.

⚠️ DEPRECATED: This tool has been migrated to tools_v2.
Use 'python -m tools_v2.toolbelt onboard.hard' instead.
This file will be removed in future version.

Migrated to: tools_v2/categories/onboarding_tools.py → HardOnboardTool
Registry: onboard.hard

Author: Agent-4 (Captain)
Deprecated: 2025-01-27 (Agent-6 - V2 Tools Flattening)
"""

import warnings

warnings.warn(
    "⚠️ DEPRECATED: This tool has been migrated to tools_v2. "
    "Use 'python -m tools_v2.toolbelt onboard.hard' instead. "
    "This file will be removed in future version.",
    DeprecationWarning,
    stacklevel=2
)

# Legacy compatibility - delegate to tools_v2
# For migration path, use: python -m tools_v2.toolbelt onboard.hard

import sys
from pathlib import Path

repo_root = Path(__file__).parent.parent
sys.path.insert(0, str(repo_root))

from src.services.hard_onboarding_service import hard_onboard_agent

def main():
    """Execute hard onboarding for specified agent."""
    
    if len(sys.argv) < 2:
        print("Usage: python captain_hard_onboard_agent.py <agent-id> [message-file]")
        print("\nExamples:")
        print("  python captain_hard_onboard_agent.py Agent-1")
        print("  python captain_hard_onboard_agent.py Agent-2 agent_workspaces/Agent-2/onboarding.md")
        print("\n⚠️  DEPRECATED: Use 'python -m tools_v2.toolbelt onboard.hard' instead")
        return 1
    
    agent_id = sys.argv[1]
    
    # Load message from file or use default
    if len(sys.argv) > 2:
        message_file = Path(sys.argv[2])
        if not message_file.exists():
            print(f"❌ Message file not found: {message_file}")
            return 1
        onboarding_message = message_file.read_text(encoding="utf-8")
        print(f"📄 Loaded message from {message_file} ({len(onboarding_message)} chars)")
    else:
        # Check for agent's default onboarding file
        default_file = repo_root / "agent_workspaces" / agent_id / "HARD_ONBOARDING_MESSAGE.md"
        if default_file.exists():
            onboarding_message = default_file.read_text(encoding="utf-8")
            print(f"📄 Loaded default message ({len(onboarding_message)} chars)")
        else:
            print(f"❌ No message file specified and no default found at {default_file}")
            return 1
    
    # Execute hard onboarding
    print(f"🚨 Starting HARD ONBOARDING for {agent_id}...")
    print("  Protocol: Clear chat → Execute → New window → Navigate → Send message")
    
    success = hard_onboard_agent(
        agent_id=agent_id,
        onboarding_message=onboarding_message,
        role=None
    )
    
    if success:
        print(f"✅ {agent_id} hard onboarding COMPLETE!")
        return 0
    else:
        print(f"❌ {agent_id} hard onboarding FAILED")
        return 1

if __name__ == "__main__":
    sys.exit(main())
