#!/usr/bin/env python3
"""
Check Agent Statuses - Captain Pattern Execution
================================================

Quick script to check all agent status.json files for staleness.
Used by Captain to identify agents that need resume prompts.

<!-- SSOT Domain: infrastructure -->

Author: Agent-4 (Captain)
Date: 2025-12-05
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple

def check_agent_statuses() -> Tuple[List[Dict], List[Dict], List[Dict]]:
    """Check all agent statuses and categorize by staleness."""
    
    agents = ['Agent-1', 'Agent-2', 'Agent-3', 'Agent-5', 'Agent-6', 'Agent-7', 'Agent-8', 'Agent-4']
    workspace_root = Path("agent_workspaces")
    
    fresh_agents = []  # <2 hours
    warning_agents = []  # 2-6 hours
    critical_agents = []  # 6-12 hours
    auto_resume_agents = []  # >12 hours
    
    now = datetime.now()
    
    for agent_id in agents:
        status_file = workspace_root / agent_id / "status.json"
        
        if not status_file.exists():
            auto_resume_agents.append({
                "agent_id": agent_id,
                "status": "NO_STATUS_FILE",
                "hours_old": None,
                "last_updated": None
            })
            continue
        
        try:
            with open(status_file, 'r', encoding='utf-8') as f:
                status = json.load(f)
            
            last_updated_str = status.get('last_updated', '')
            agent_status = status.get('status', 'UNKNOWN')
            mission = status.get('current_mission', 'N/A')
            
            if not last_updated_str:
                auto_resume_agents.append({
                    "agent_id": agent_id,
                    "status": agent_status,
                    "hours_old": None,
                    "last_updated": None,
                    "mission": mission
                })
                continue
            
            # Parse timestamp
            try:
                # Handle different timestamp formats
                if 'T' in last_updated_str:
                    if last_updated_str.endswith('Z'):
                        last_updated = datetime.fromisoformat(last_updated_str.replace('Z', '+00:00'))
                    else:
                        last_updated = datetime.fromisoformat(last_updated_str)
                else:
                    # Format: "YYYY-MM-DD HH:MM:SS"
                    last_updated = datetime.strptime(last_updated_str, '%Y-%m-%d %H:%M:%S')
            except Exception as e:
                auto_resume_agents.append({
                    "agent_id": agent_id,
                    "status": agent_status,
                    "hours_old": None,
                    "last_updated": last_updated_str,
                    "mission": mission,
                    "error": f"Invalid timestamp: {e}"
                })
                continue
            
            # Calculate hours since update
            if last_updated.tzinfo:
                hours_old = (now - last_updated.replace(tzinfo=None)).total_seconds() / 3600
            else:
                hours_old = (now - last_updated).total_seconds() / 3600
            
            agent_info = {
                "agent_id": agent_id,
                "status": agent_status,
                "hours_old": round(hours_old, 1),
                "last_updated": last_updated_str,
                "mission": mission[:60]
            }
            
            # Categorize by staleness
            if hours_old < 2:
                fresh_agents.append(agent_info)
            elif hours_old < 6:
                warning_agents.append(agent_info)
            elif hours_old < 12:
                critical_agents.append(agent_info)
            else:
                auto_resume_agents.append(agent_info)
                
        except Exception as e:
            auto_resume_agents.append({
                "agent_id": agent_id,
                "status": "ERROR",
                "hours_old": None,
                "last_updated": None,
                "error": str(e)
            })
    
    return fresh_agents, warning_agents, critical_agents, auto_resume_agents


def main():
    """Print agent status summary."""
    fresh, warning, critical, auto_resume = check_agent_statuses()
    
    print("=" * 60)
    print("AGENT STATUS CHECK - Captain Pattern Execution")
    print("=" * 60)
    print()
    
    print(f"🟢 FRESH (<2 hours): {len(fresh)}")
    for agent in fresh:
        print(f"  - {agent['agent_id']}: {agent['status']} ({agent['hours_old']}h ago) - {agent['mission']}")
    
    print()
    print(f"🟡 WARNING (2-6 hours): {len(warning)}")
    for agent in warning:
        print(f"  - {agent['agent_id']}: {agent['status']} ({agent['hours_old']}h ago) - {agent['mission']}")
    
    print()
    print(f"🟠 CRITICAL (6-12 hours): {len(critical)}")
    for agent in critical:
        print(f"  - {agent['agent_id']}: {agent['status']} ({agent['hours_old']}h ago) - {agent['mission']}")
    
    print()
    print(f"🔴 AUTO-RESUME (>12 hours): {len(auto_resume)}")
    for agent in auto_resume:
        hours_str = f"{agent['hours_old']}h ago" if agent['hours_old'] else "UNKNOWN"
        print(f"  - {agent['agent_id']}: {agent['status']} ({hours_str}) - {agent.get('mission', 'N/A')}")
    
    print()
    print("=" * 60)
    print(f"Total Agents: {len(fresh) + len(warning) + len(critical) + len(auto_resume)}")
    print(f"Need Resume: {len(critical) + len(auto_resume)}")
    print("=" * 60)
    
    # Return exit code based on staleness
    if auto_resume:
        return 2  # Need immediate resume
    elif critical:
        return 1  # Need resume soon
    else:
        return 0  # All good


if __name__ == "__main__":
    sys.exit(main())

