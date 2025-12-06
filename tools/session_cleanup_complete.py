#!/usr/bin/env python3
"""
Session Cleanup Complete Tool
==============================

Automates session cleanup tasks:
1. Create/Update passdown.json
2. Create Final Devlog
3. Post Devlog to Discord
4. Update Swarm Brain Database
5. Create a Tool You Wished You Had

Author: Agent-3 (Infrastructure & DevOps Specialist)
Date: 2025-12-05
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from src.utils.swarm_time import get_swarm_time, format_swarm_timestamp_readable


def get_agent_info():
    """Get agent information from status.json."""
    agent_workspace = Path("agent_workspaces")
    agents = {}
    
    for agent_dir in agent_workspace.iterdir():
        if agent_dir.is_dir() and agent_dir.name.startswith("Agent-"):
            status_file = agent_dir / "status.json"
            if status_file.exists():
                try:
                    with open(status_file, 'r', encoding='utf-8') as f:
                        status = json.load(f)
                        agents[status_file.parent.name] = {
                            "id": status.get("agent_id", ""),
                            "name": status.get("agent_name", ""),
                            "status": status.get("status", ""),
                            "last_updated": status.get("last_updated", ""),
                            "current_tasks": status.get("current_tasks", []),
                            "completed_tasks": status.get("completed_tasks", [])
                        }
                except Exception as e:
                    print(f"⚠️  Error reading {status_file}: {e}")
    
    return agents


def check_session_cleanup_status(agent_id: str = None):
    """Check session cleanup status for agent(s)."""
    agents = get_agent_info()
    
    if agent_id:
        agents = {k: v for k, v in agents.items() if v["id"] == agent_id}
    
    print(f"\n{'='*60}")
    print(f"SESSION CLEANUP STATUS CHECK")
    print(f"{'='*60}\n")
    
    current_time = get_swarm_time()
    
    for agent_name, info in agents.items():
        print(f"📋 {info['name']} ({info['id']})")
        print(f"   Status: {info['status']}")
        print(f"   Last Updated: {info['last_updated']}")
        
        # Check passdown.json
        passdown_file = Path(f"agent_workspaces/{agent_name}/passdown.json")
        if passdown_file.exists():
            print(f"   ✅ passdown.json: EXISTS")
        else:
            print(f"   ❌ passdown.json: MISSING")
        
        # Check devlogs
        devlog_dir = Path(f"agent_workspaces/{agent_name}/devlogs")
        if devlog_dir.exists():
            devlogs = list(devlog_dir.glob("*.md"))
            if devlogs:
                latest = max(devlogs, key=lambda p: p.stat().st_mtime)
                print(f"   ✅ Latest Devlog: {latest.name}")
            else:
                print(f"   ⚠️  Devlogs: NONE FOUND")
        else:
            print(f"   ⚠️  Devlogs Directory: MISSING")
        
        # Check recent activity
        if info['last_updated']:
            print(f"   📊 Current Tasks: {len(info['current_tasks'])}")
            print(f"   ✅ Completed Tasks: {len(info['completed_tasks'])}")
        
        print()
    
    print(f"{'='*60}\n")


def generate_cleanup_checklist(agent_id: str):
    """Generate session cleanup checklist for agent."""
    agents = get_agent_info()
    agent_info = None
    
    for agent_name, info in agents.items():
        if info["id"] == agent_id:
            agent_info = info
            agent_workspace_name = agent_name
            break
    
    if not agent_info:
        print(f"❌ Agent {agent_id} not found")
        return
    
    checklist = {
        "agent_id": agent_id,
        "agent_name": agent_info["name"],
        "checklist_date": get_swarm_time(),
        "tasks": [
            {
                "task": "Create/Update passdown.json",
                "status": "pending",
                "file": f"agent_workspaces/{agent_workspace_name}/passdown.json"
            },
            {
                "task": "Create Final Devlog",
                "status": "pending",
                "directory": f"agent_workspaces/{agent_workspace_name}/devlogs"
            },
            {
                "task": "Post Devlog to Discord",
                "status": "pending",
                "command": f"python tools/devlog_manager.py post --agent {agent_id.lower()} --file <devlog_file.md>"
            },
            {
                "task": "Update Swarm Brain Database",
                "status": "pending",
                "note": "Automatic via devlog_manager.py"
            },
            {
                "task": "Create a Tool You Wished You Had",
                "status": "pending",
                "directory": "tools/"
            }
        ]
    }
    
    # Check status
    passdown_file = Path(checklist["tasks"][0]["file"])
    if passdown_file.exists():
        checklist["tasks"][0]["status"] = "complete"
    
    devlog_dir = Path(checklist["tasks"][1]["directory"])
    if devlog_dir.exists() and list(devlog_dir.glob("*.md")):
        checklist["tasks"][1]["status"] = "complete"
    
    return checklist


def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Session Cleanup Complete Tool")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check session cleanup status"
    )
    parser.add_argument(
        "--agent",
        type=str,
        help="Agent ID to check (e.g., Agent-3)"
    )
    parser.add_argument(
        "--checklist",
        type=str,
        help="Generate checklist for agent ID"
    )
    
    args = parser.parse_args()
    
    if args.check:
        check_session_cleanup_status(args.agent)
    elif args.checklist:
        checklist = generate_cleanup_checklist(args.checklist)
        if checklist:
            print(json.dumps(checklist, indent=2))
    else:
        print("Session Cleanup Complete Tool")
        print("\nUsage:")
        print("  python tools/session_cleanup_complete.py --check [--agent Agent-X]")
        print("  python tools/session_cleanup_complete.py --checklist Agent-X")
        print("\nThis tool helps verify session cleanup tasks are complete.")


if __name__ == "__main__":
    main()
