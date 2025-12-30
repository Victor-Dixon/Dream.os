#!/usr/bin/env python3
"""
Coordination Status Summary Tool
================================
Generates a quick summary of active coordinations from Agent-4 status.json
for rapid coordination visibility.

<!-- SSOT Domain: tools -->
"""

import json
from pathlib import Path

def get_coordination_summary():
    """Extract active coordination summary from Agent-4 status.json."""
    status_path = Path(__file__).parent.parent / "agent_workspaces" / "Agent-4" / "status.json"
    
    if not status_path.exists():
        print("❌ status.json not found")
        return
    
    with open(status_path, 'r', encoding='utf-8') as f:
        status = json.load(f)
    
    active = [c for c in status.get("active_coordinations", []) if c.get("status") in ["ACTIVE", "IN_PROGRESS"]]
    
    print(f"Active Coordinations: {len(active)}\n")
    for coord in active:
        task = coord.get("task", "Unknown")
        agents = ", ".join(coord.get("agents", []))
        progress = coord.get("progress", "No progress")
        print(f"• {task}")
        print(f"  Agents: {agents}")
        print(f"  Progress: {progress}\n")

if __name__ == "__main__":
    get_coordination_summary()

