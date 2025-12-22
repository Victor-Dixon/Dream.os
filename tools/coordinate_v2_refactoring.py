#!/usr/bin/env python3
"""
Coordinate V2 Compliance Refactoring Across Agents
===================================================

Facilitates parallel V2 refactoring coordination across Agent-1 (integration),
Agent-7 (web), Agent-8 (SSOT/QA). Tracks progress, identifies blockers,
ensures force multiplier efficiency.

Agent-6: Coordination & Communication Specialist
Task: Coordinate V2 compliance refactoring across agents (HIGH priority)
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List

def load_agent_status(agent_id: str) -> Dict:
    """Load agent status.json file."""
    project_root = Path(__file__).parent.parent
    status_file = project_root / "agent_workspaces" / agent_id / "status.json"
    
    if not status_file.exists():
        return {"agent_id": agent_id, "status": "UNKNOWN", "error": "status.json not found"}
    
    try:
        with open(status_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        return {"agent_id": agent_id, "status": "ERROR", "error": str(e)}

def analyze_v2_refactoring_progress() -> Dict:
    """Analyze V2 refactoring progress across all agents."""
    agents = ["Agent-1", "Agent-7", "Agent-8"]
    
    analysis = {
        "timestamp": datetime.now().isoformat(),
        "agents": {},
        "coordination_opportunities": [],
        "blockers": [],
        "progress_summary": {}
    }
    
    for agent_id in agents:
        status = load_agent_status(agent_id)
        analysis["agents"][agent_id] = {
            "status": status.get("status", "UNKNOWN"),
            "current_tasks": status.get("current_tasks", []),
            "v2_refactoring": extract_v2_refactoring_info(status, agent_id)
        }
    
    # Identify coordination opportunities
    analysis["coordination_opportunities"] = identify_coordination_opportunities(analysis["agents"])
    
    # Identify blockers
    analysis["blockers"] = identify_blockers(analysis["agents"])
    
    # Calculate progress summary
    analysis["progress_summary"] = calculate_progress_summary(analysis["agents"])
    
    return analysis

def extract_v2_refactoring_info(status: Dict, agent_id: str) -> Dict:
    """Extract V2 refactoring information from agent status."""
    v2_info = {
        "active": False,
        "details": {}
    }
    
    current_tasks = status.get("current_tasks", [])
    for task in current_tasks:
        task_str = str(task).lower()
        if "v2" in task_str or "refactor" in task_str or "compliance" in task_str:
            v2_info["active"] = True
            v2_info["details"]["task"] = task[:200] if len(task) > 200 else task
    
    # Agent-specific extraction
    if agent_id == "Agent-1":
        # Look for Phase 0 or Batch information
        for task in current_tasks:
            if "phase 0" in str(task).lower() or "batch" in str(task).lower():
                v2_info["details"]["phase_info"] = str(task)[:200]
    
    elif agent_id == "Agent-7":
        # Look for Batch 1 information
        for task in current_tasks:
            if "batch 1" in str(task).lower() or "unified_discord_bot" in str(task).lower():
                v2_info["details"]["batch_info"] = str(task)[:200]
    
    elif agent_id == "Agent-8":
        # Look for SSOT or import fixes
        for task in current_tasks:
            if "ssot" in str(task).lower() or "import" in str(task).lower():
                v2_info["details"]["ssot_info"] = str(task)[:200]
    
    return v2_info

def identify_coordination_opportunities(agents: Dict) -> List[Dict]:
    """Identify coordination opportunities between agents."""
    opportunities = []
    
    # Check if agents are working on related files
    agent1_files = extract_file_mentions(agents.get("Agent-1", {}).get("v2_refactoring", {}).get("details", {}))
    agent7_files = extract_file_mentions(agents.get("Agent-7", {}).get("v2_refactoring", {}).get("details", {}))
    agent8_files = extract_file_mentions(agents.get("Agent-8", {}).get("v2_refactoring", {}).get("details", {}))
    
    # Check for overlapping domains
    if agent1_files and agent7_files:
        opportunities.append({
            "type": "file_coordination",
            "agents": ["Agent-1", "Agent-7"],
            "description": "Potential file overlap between integration and web refactoring"
        })
    
    # Check for dependency chains
    if agents.get("Agent-8", {}).get("v2_refactoring", {}).get("active"):
        opportunities.append({
            "type": "dependency_coordination",
            "agents": ["Agent-8", "Agent-1", "Agent-7"],
            "description": "SSOT/QA validation should coordinate with integration and web refactoring"
        })
    
    return opportunities

def extract_file_mentions(details: Dict) -> List[str]:
    """Extract file mentions from details."""
    files = []
    for key, value in details.items():
        if isinstance(value, str):
            # Look for .py, .js, .ts file mentions
            import re
            file_matches = re.findall(r'\b[\w/]+\.(?:py|js|ts|tsx|jsx)\b', value)
            files.extend(file_matches)
    return files

def identify_blockers(agents: Dict) -> List[Dict]:
    """Identify blockers in V2 refactoring progress."""
    blockers = []
    
    for agent_id, agent_data in agents.items():
        status = agent_data.get("status", "UNKNOWN")
        v2_active = agent_data.get("v2_refactoring", {}).get("active", False)
        
        if status not in ["ACTIVE", "ACTIVE_AGENT_MODE"] and v2_active:
            blockers.append({
                "agent": agent_id,
                "type": "status_blocker",
                "description": f"{agent_id} has V2 refactoring work but status is {status}"
            })
        
        # Check for "blocker" or "waiting" in tasks
        tasks = agent_data.get("current_tasks", [])
        for task in tasks:
            task_str = str(task).lower()
            if "blocker" in task_str or "waiting" in task_str or "stuck" in task_str:
                blockers.append({
                    "agent": agent_id,
                    "type": "task_blocker",
                    "description": f"{agent_id} has blocker mentioned in tasks: {task[:100]}"
                })
    
    return blockers

def calculate_progress_summary(agents: Dict) -> Dict:
    """Calculate overall progress summary."""
    total_agents = len(agents)
    active_agents = sum(1 for a in agents.values() if a.get("status") in ["ACTIVE", "ACTIVE_AGENT_MODE"])
    v2_active_agents = sum(1 for a in agents.values() if a.get("v2_refactoring", {}).get("active", False))
    
    return {
        "total_agents": total_agents,
        "active_agents": active_agents,
        "v2_active_agents": v2_active_agents,
        "coordination_health": "GOOD" if active_agents == total_agents else "NEEDS_ATTENTION",
        "v2_progress": f"{v2_active_agents}/{total_agents} agents actively refactoring"
    }

def main():
    """Main execution."""
    print("=" * 70)
    print("V2 COMPLIANCE REFACTORING COORDINATION")
    print("=" * 70)
    print()
    
    analysis = analyze_v2_refactoring_progress()
    
    print("AGENT STATUS:")
    print("-" * 70)
    for agent_id, agent_data in analysis["agents"].items():
        print(f"\n{agent_id}:")
        print(f"  Status: {agent_data['status']}")
        v2_info = agent_data["v2_refactoring"]
        if v2_info["active"]:
            print(f"  V2 Refactoring: ✅ ACTIVE")
            for key, value in v2_info["details"].items():
                value_str = str(value)
                if len(value_str) > 100:
                    print(f"    {key}: {value_str[:100]}...")
                else:
                    print(f"    {key}: {value_str}")
        else:
            print(f"  V2 Refactoring: ⏸️  NOT ACTIVE")
    
    print()
    print("=" * 70)
    print("COORDINATION OPPORTUNITIES:")
    print("-" * 70)
    if analysis["coordination_opportunities"]:
        for opp in analysis["coordination_opportunities"]:
            print(f"  • {opp['type']}: {opp['description']}")
            print(f"    Agents: {', '.join(opp['agents'])}")
    else:
        print("  No coordination opportunities identified")
    
    print()
    print("=" * 70)
    print("BLOCKERS:")
    print("-" * 70)
    if analysis["blockers"]:
        for blocker in analysis["blockers"]:
            print(f"  ⚠️  {blocker['agent']}: {blocker['description']}")
    else:
        print("  ✅ No blockers identified")
    
    print()
    print("=" * 70)
    print("PROGRESS SUMMARY:")
    print("-" * 70)
    summary = analysis["progress_summary"]
    print(f"  Total agents: {summary['total_agents']}")
    print(f"  Active agents: {summary['active_agents']}")
    print(f"  V2 active agents: {summary['v2_active_agents']}")
    print(f"  Coordination health: {summary['coordination_health']}")
    print(f"  V2 progress: {summary['v2_progress']}")
    
    # Save results
    output_path = Path("agent_workspaces/Agent-6/v2_refactoring_coordination.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(analysis, f, indent=2)
    
    print()
    print(f"✅ Coordination analysis saved to: {output_path}")

if __name__ == "__main__":
    main()

