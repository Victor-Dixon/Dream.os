#!/usr/bin/env python3
"""
Check Agent Status Staleness
============================

Checks all agent status.json files for staleness and reports which agents need updates.

Author: Agent-4 (Captain)
Date: 2025-12-02
"""

import json
from pathlib import Path
from datetime import datetime, timedelta

AGENTS = ["Agent-1", "Agent-2", "Agent-3", "Agent-5", "Agent-6", "Agent-7", "Agent-8"]
STALE_THRESHOLD_HOURS = 6


def check_status_staleness():
    """Check all agent status files for staleness."""
    stale_agents = []
    current_agents = []
    
    for agent_id in AGENTS:
        status_file = Path(f"agent_workspaces/{agent_id}/status.json")
        
        if not status_file.exists():
            stale_agents.append({
                "agent_id": agent_id,
                "status": "MISSING",
                "last_updated": None,
                "hours_old": None
            })
            continue
        
        try:
            with open(status_file, 'r', encoding='utf-8') as f:
                status = json.load(f)
            
            last_updated_str = status.get("last_updated", "")
            if not last_updated_str:
                stale_agents.append({
                    "agent_id": agent_id,
                    "status": "NO_TIMESTAMP",
                    "last_updated": None,
                    "hours_old": None
                })
                continue
            
            # Parse timestamp
            try:
                last_updated = datetime.strptime(last_updated_str, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                try:
                    last_updated = datetime.strptime(last_updated_str, "%Y-%m-%dT%H:%M:%S")
                except ValueError:
                    stale_agents.append({
                        "agent_id": agent_id,
                        "status": "INVALID_TIMESTAMP",
                        "last_updated": last_updated_str,
                        "hours_old": None
                    })
                    continue
            
            hours_old = (datetime.now() - last_updated).total_seconds() / 3600
            
            if hours_old > STALE_THRESHOLD_HOURS:
                stale_agents.append({
                    "agent_id": agent_id,
                    "status": "STALE",
                    "last_updated": last_updated_str,
                    "hours_old": round(hours_old, 1)
                })
            else:
                current_agents.append({
                    "agent_id": agent_id,
                    "last_updated": last_updated_str,
                    "hours_old": round(hours_old, 1)
                })
        
        except Exception as e:
            stale_agents.append({
                "agent_id": agent_id,
                "status": "ERROR",
                "last_updated": None,
                "hours_old": None,
                "error": str(e)
            })
    
    return stale_agents, current_agents


def main():
    """Main entry point."""
    print("🔍 Checking agent status files for staleness...\n")
    
    stale_agents, current_agents = check_status_staleness()
    
    if stale_agents:
        print("⚠️  STALE AGENTS (need status.json updates):")
        print("=" * 60)
        for agent in stale_agents:
            status = agent["status"]
            hours = agent.get("hours_old", "N/A")
            last_up = agent.get("last_updated", "N/A")
            print(f"  {agent['agent_id']}: {status}")
            if hours != "N/A" and hours is not None:
                print(f"    Last updated: {last_up} ({hours} hours ago)")
            if "error" in agent:
                print(f"    Error: {agent['error']}")
        print()
    else:
        print("✅ All agents have current status files!\n")
    
    if current_agents:
        print("✅ CURRENT AGENTS:")
        print("=" * 60)
        for agent in current_agents:
            hours = agent["hours_old"]
            print(f"  {agent['agent_id']}: {agent['last_updated']} ({hours} hours ago)")
        print()
    
    return len(stale_agents)


if __name__ == "__main__":
    exit(main())


