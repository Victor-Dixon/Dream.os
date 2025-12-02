#!/usr/bin/env python3
"""
Reset All Agent Status Files
============================

Resets all agent status.json files to clean state.

Usage:
    python tools/reset_all_agent_status.py
"""

import json
import os
from pathlib import Path
from datetime import datetime

# Agent definitions
AGENTS = {
    "Agent-1": {
        "name": "Integration & Core Systems Specialist",
        "role": "Integration & Core Systems"
    },
    "Agent-2": {
        "name": "Architecture & Design Specialist",
        "role": "Architecture & Design"
    },
    "Agent-3": {
        "name": "Infrastructure & DevOps Specialist",
        "role": "Infrastructure & DevOps"
    },
    "Agent-4": {
        "name": "Captain (Strategic Oversight)",
        "role": "Strategic Oversight & Emergency Intervention"
    },
    "Agent-5": {
        "name": "Business Intelligence Specialist",
        "role": "Business Intelligence"
    },
    "Agent-6": {
        "name": "Coordination & Communication Specialist",
        "role": "Coordination & Communication"
    },
    "Agent-7": {
        "name": "Web Development Specialist",
        "role": "Web Development"
    },
    "Agent-8": {
        "name": "SSOT & System Integration Specialist",
        "role": "SSOT & System Integration"
    }
}

def create_clean_status(agent_id: str) -> dict:
    """Create clean status.json for an agent."""
    agent_info = AGENTS[agent_id]
    now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    
    return {
        "agent_id": agent_id,
        "agent_name": agent_info["name"],
        "status": "ACTIVE_AGENT_MODE",
        "current_phase": "TASK_EXECUTION",
        "last_updated": now,
        "current_mission": "V2 Compliance & Organization Phase",
        "mission_priority": "HIGH",
        "current_tasks": [],
        "completed_tasks": [],
        "achievements": [],
        "next_actions": []
    }

def reset_agent_status(agent_id: str) -> bool:
    """Reset an agent's status.json file."""
    workspace_path = Path(f"agent_workspaces/{agent_id}")
    status_file = workspace_path / "status.json"
    
    if not workspace_path.exists():
        print(f"⚠️  Workspace not found: {workspace_path}")
        return False
    
    try:
        clean_status = create_clean_status(agent_id)
        
        # Backup existing status if it exists
        if status_file.exists():
            backup_file = workspace_path / f"status_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(status_file, 'r') as f:
                backup_data = json.load(f)
            with open(backup_file, 'w') as f:
                json.dump(backup_data, f, indent=2)
            print(f"  📦 Backed up to: {backup_file.name}")
        
        # Write clean status
        with open(status_file, 'w') as f:
            json.dump(clean_status, f, indent=2)
        
        print(f"✅ {agent_id}: Status reset complete")
        return True
        
    except Exception as e:
        print(f"❌ {agent_id}: Error - {e}")
        return False

def main():
    """Reset all agent status files."""
    print("🔄 Resetting All Agent Status Files")
    print("=" * 50)
    print()
    
    results = {}
    for agent_id in AGENTS.keys():
        print(f"Processing {agent_id}...")
        results[agent_id] = reset_agent_status(agent_id)
        print()
    
    print("=" * 50)
    print("📊 Summary:")
    successful = sum(1 for v in results.values() if v)
    total = len(results)
    print(f"✅ Successful: {successful}/{total}")
    print(f"❌ Failed: {total - successful}/{total}")
    
    if successful == total:
        print("\n🎉 All agent status files reset successfully!")
    else:
        print("\n⚠️  Some agents failed to reset. Check errors above.")

if __name__ == "__main__":
    main()

