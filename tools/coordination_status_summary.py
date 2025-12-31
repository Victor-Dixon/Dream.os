#!/usr/bin/env python3
"""
Coordination Status Summary Tool
================================
Generates a quick summary of active coordinations from Agent-4 status.json
for rapid coordination visibility.

Migrated to use unified agent status library (Phase 6).

<!-- SSOT Domain: tools -->
"""

from pathlib import Path
from typing import Optional

# Try to use unified library, fallback to direct reading
try:
    from src.core.agent_status import read_agent_status
    USE_UNIFIED_LIBRARY = True
except ImportError:
    USE_UNIFIED_LIBRARY = False
    import json


def get_coordination_summary() -> None:
    """Extract active coordination summary from Agent-4 status.json."""
    workspace_root = Path(__file__).parent.parent
    
    # Use unified library if available
    if USE_UNIFIED_LIBRARY:
        status = read_agent_status("Agent-4", workspace_root=workspace_root)
    else:
        # Fallback to direct reading
        status_path = workspace_root / "agent_workspaces" / "Agent-4" / "status.json"
        if not status_path.exists():
            print("❌ status.json not found")
            return
        with open(status_path, 'r', encoding='utf-8') as f:
            status = json.load(f)
    
    if not status:
        print("❌ Could not read Agent-4 status")
        return
    
    active = [
        c for c in status.get("active_coordinations", [])
        if c.get("status") in ["ACTIVE", "IN_PROGRESS"]
    ]
    
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

