#!/usr/bin/env python3
"""
Quick utility to check agent onboarding status from status.json

Usage:
    python tools/check_agent_onboarding_status.py [agent_id]
    
If agent_id not provided, checks Agent-1 by default.
"""

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent


def check_onboarding_status(agent_id: str = "Agent-1") -> dict:
    """Check onboarding status from agent's status.json."""
    status_path = PROJECT_ROOT / "agent_workspaces" / agent_id / "status.json"
    
    if not status_path.exists():
        return {"error": f"Status file not found: {status_path}"}
    
    try:
        with open(status_path, 'r', encoding='utf-8') as f:
            status = json.load(f)
        
        return {
            "agent_id": status.get("agent_id"),
            "status": status.get("status"),
            "cycle_count": status.get("cycle_count"),
            "last_updated": status.get("last_updated"),
            "current_mission": status.get("current_mission"),
            "current_phase": status.get("current_phase"),
        }
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    agent_id = sys.argv[1] if len(sys.argv) > 1 else "Agent-1"
    result = check_onboarding_status(agent_id)
    
    if "error" in result:
        print(f"❌ Error: {result['error']}", file=sys.stderr)
        sys.exit(1)
    
    print(f"Agent: {result['agent_id']}")
    print(f"Status: {result['status']}")
    print(f"Cycle Count: {result['cycle_count']}")
    print(f"Last Updated: {result['last_updated']}")
    print(f"Current Mission: {result['current_mission']}")
    print(f"Current Phase: {result['current_phase']}")

