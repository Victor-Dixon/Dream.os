#!/usr/bin/env python3
"""
Identify Coordination Opportunities
===================================

Scans the codebase and task logs to identify coordination opportunities
that Agent-6 can facilitate.

Agent-6: Coordination & Communication Specialist
"""

import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict

def analyze_coordination_opportunities() -> Dict:
    """Analyze coordination opportunities from task log and status files."""
    project_root = Path(__file__).parent.parent
    master_task_log = project_root / "MASTER_TASK_LOG.md"
    
    opportunities = {
        "timestamp": datetime.now().isoformat(),
        "coordination_tasks": [],
        "blocker_resolution": [],
        "bilateral_coordination": [],
        "force_multiplier": [],
        "system_health": []
    }
    
    # Read master task log
    if master_task_log.exists():
        content = master_task_log.read_text(encoding='utf-8')
        
        # Find coordination blockers
        if "SSOT verification" in content and "Blocking" in content:
            opportunities["blocker_resolution"].append({
                "task": "SSOT verification for Batches 2-8",
                "agents": ["Agent-8", "Agent-3"],
                "priority": "MEDIUM",
                "action": "Facilitate SSOT validation coordination between Agent-8 and Agent-3"
            })
        
        if "Architecture review" in content and "Blocking" in content:
            opportunities["blocker_resolution"].append({
                "task": "Architecture review for Website SEO/UX",
                "agents": ["Agent-2", "Agent-7"],
                "priority": "MEDIUM",
                "action": "Coordinate architecture review handoff from Agent-2 to Agent-7"
            })
    
    # Check agent status files for coordination needs
    agent_workspaces = project_root / "agent_workspaces"
    if agent_workspaces.exists():
        for agent_dir in agent_workspaces.iterdir():
            if agent_dir.is_dir():
                status_file = agent_dir / "status.json"
                if status_file.exists():
                    try:
                        with open(status_file, 'r', encoding='utf-8') as f:
                            status = json.load(f)
                        
                        agent_id = status.get("agent_id", "")
                        current_tasks = status.get("current_tasks", [])
                        
                        # Look for coordination keywords
                        for task in current_tasks:
                            task_str = str(task).lower()
                            if any(keyword in task_str for keyword in ["coordination", "blocker", "waiting", "dependency"]):
                                opportunities["coordination_tasks"].append({
                                    "agent": agent_id,
                                    "task": task[:100] + "..." if len(task) > 100 else task,
                                    "priority": "MEDIUM"
                                })
                    except Exception:
                        pass
    
    # Add system health monitoring opportunity
    opportunities["system_health"].append({
        "task": "System health coordination dashboard",
        "priority": "MEDIUM",
        "action": "Create coordination dashboard showing: toolbelt health (100%), import health (0 issues), V2 compliance (87.7%), website audits (complete)"
    })
    
    # Add V2 compliance coordination
    opportunities["force_multiplier"].append({
        "task": "V2 compliance refactoring coordination",
        "agents": ["Agent-1", "Agent-7", "Agent-8"],
        "priority": "HIGH",
        "action": "Coordinate parallel V2 refactoring across multiple agents, track progress, identify blockers"
    })
    
    return opportunities

def main():
    """Main execution."""
    print("=" * 70)
    print("COORDINATION OPPORTUNITIES ANALYSIS")
    print("=" * 70)
    print()
    
    opportunities = analyze_coordination_opportunities()
    
    print("COORDINATION TASKS:")
    print("-" * 70)
    for task in opportunities["coordination_tasks"]:
        print(f"  • {task['agent']}: {task['task']}")
    
    print()
    print("BLOCKER RESOLUTION:")
    print("-" * 70)
    for blocker in opportunities["blocker_resolution"]:
        print(f"  • {blocker['task']}")
        print(f"    Agents: {', '.join(blocker['agents'])}")
        print(f"    Action: {blocker['action']}")
    
    print()
    print("BILATERAL COORDINATION:")
    print("-" * 70)
    for coord in opportunities["bilateral_coordination"]:
        print(f"  • {coord.get('task', 'N/A')}")
    
    print()
    print("FORCE MULTIPLIER:")
    print("-" * 70)
    for fm in opportunities["force_multiplier"]:
        print(f"  • {fm['task']}")
        print(f"    Agents: {', '.join(fm['agents'])}")
        print(f"    Action: {fm['action']}")
    
    print()
    print("SYSTEM HEALTH:")
    print("-" * 70)
    for health in opportunities["system_health"]:
        print(f"  • {health['task']}")
        print(f"    Action: {health['action']}")
    
    # Save results
    output_path = Path("agent_workspaces/Agent-6/coordination_opportunities.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(opportunities, f, indent=2)
    
    print()
    print(f"✅ Results saved to: {output_path}")

if __name__ == "__main__":
    main()

