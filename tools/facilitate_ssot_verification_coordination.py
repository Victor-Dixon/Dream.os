#!/usr/bin/env python3
"""
Facilitate SSOT Verification Coordination for Batches 2-8
=========================================================

Coordinates SSOT validation between Agent-8 (SSOT validation) and Agent-3
(infrastructure) for duplicate consolidation batches. Tracks progress,
identifies blockers, facilitates bilateral coordination.

Agent-6: Coordination & Communication Specialist
Task: Facilitate SSOT verification coordination for Batches 2-8 (MEDIUM priority)
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

def analyze_ssot_coordination_status() -> Dict:
    """Analyze SSOT verification coordination status."""
    agents = ["Agent-8", "Agent-3", "Agent-5"]
    
    analysis = {
        "timestamp": datetime.now().isoformat(),
        "task": "SSOT Verification Coordination for Batches 2-8",
        "agents": {},
        "coordination_status": {},
        "blockers": [],
        "next_actions": []
    }
    
    for agent_id in agents:
        status = load_agent_status(agent_id)
        analysis["agents"][agent_id] = {
            "status": status.get("status", "UNKNOWN"),
            "current_tasks": status.get("current_tasks", []),
            "ssot_related": extract_ssot_info(status, agent_id)
        }
    
    # Analyze coordination status
    agent8_status = analysis["agents"]["Agent-8"]
    agent3_status = analysis["agents"]["Agent-3"]
    agent5_status = analysis["agents"]["Agent-5"]
    
    # Check Agent-8 SSOT verification status
    agent8_ssot = agent8_status["ssot_related"]
    if agent8_ssot.get("accepted"):
        analysis["coordination_status"]["agent8"] = {
            "status": "ACCEPTED",
            "current_step": agent8_ssot.get("current_step", "UNKNOWN"),
            "blockers": agent8_ssot.get("blockers", [])
        }
    else:
        analysis["coordination_status"]["agent8"] = {
            "status": "PENDING",
            "note": "SSOT verification not yet accepted"
        }
    
    # Check Agent-5 batch data status
    agent5_ssot = agent5_status["ssot_related"]
    if agent5_ssot.get("providing_data"):
        analysis["coordination_status"]["agent5"] = {
            "status": "PROVIDING_DATA",
            "note": "Agent-5 providing batch 2-8 data"
        }
    else:
        analysis["coordination_status"]["agent5"] = {
            "status": "UNKNOWN",
            "note": "Batch data status unclear"
        }
    
    # Check Agent-3 infrastructure support
    agent3_ssot = agent3_status["ssot_related"]
    if agent3_ssot.get("ready"):
        analysis["coordination_status"]["agent3"] = {
            "status": "READY",
            "note": "Agent-3 ready for infrastructure support"
        }
    else:
        analysis["coordination_status"]["agent3"] = {
            "status": "UNKNOWN",
            "note": "Infrastructure support status unclear"
        }
    
    # Identify blockers
    if agent8_ssot.get("waiting_for_data"):
        analysis["blockers"].append({
            "type": "data_dependency",
            "agent": "Agent-8",
            "description": "Waiting for batch 2-8 data from Agent-5",
            "blocking": "SSOT verification execution"
        })
    
    # Identify next actions
    if agent8_ssot.get("accepted") and agent8_ssot.get("waiting_for_data"):
        analysis["next_actions"].append({
            "action": "Coordinate with Agent-5 to provide batch 2-8 data",
            "priority": "HIGH",
            "agents": ["Agent-5", "Agent-8"]
        })
    
    if agent8_ssot.get("ready_to_execute"):
        analysis["next_actions"].append({
            "action": "Coordinate SSOT verification execution between Agent-8 and Agent-3",
            "priority": "MEDIUM",
            "agents": ["Agent-8", "Agent-3"]
        })
    
    return analysis

def extract_ssot_info(status: Dict, agent_id: str) -> Dict:
    """Extract SSOT-related information from agent status."""
    ssot_info = {
        "accepted": False,
        "current_step": "UNKNOWN",
        "blockers": [],
        "waiting_for_data": False,
        "ready_to_execute": False,
        "providing_data": False,
        "ready": False
    }
    
    current_tasks = status.get("current_tasks", [])
    current_mission = status.get("current_mission", "")
    
    # Check for SSOT verification acceptance
    for task in current_tasks:
        task_str = str(task).lower()
        if "ssot verification" in task_str and "batches 2-8" in task_str:
            if "accepted" in task_str:
                ssot_info["accepted"] = True
            if "waiting" in task_str or "awaiting" in task_str:
                ssot_info["waiting_for_data"] = True
            if "ready" in task_str:
                ssot_info["ready_to_execute"] = True
    
    # Check mission
    if "ssot verification" in current_mission.lower() and "batches 2-8" in current_mission.lower():
        if "accepted" in current_mission.lower():
            ssot_info["accepted"] = True
    
    # Agent-specific extraction
    if agent_id == "Agent-8":
        for task in current_tasks:
            task_str = str(task).lower()
            if "request batch" in task_str and "agent-5" in task_str:
                ssot_info["waiting_for_data"] = True
                ssot_info["current_step"] = "Waiting for batch data from Agent-5"
            if "execute ssot" in task_str and "ready" in task_str:
                ssot_info["ready_to_execute"] = True
                ssot_info["current_step"] = "Ready to execute SSOT verification"
    
    elif agent_id == "Agent-5":
        for task in current_tasks:
            task_str = str(task).lower()
            if "batch" in task_str and ("2-8" in task_str or "duplicate" in task_str):
                if "provide" in task_str or "data" in task_str:
                    ssot_info["providing_data"] = True
                    ssot_info["current_step"] = "Providing batch 2-8 data"
    
    elif agent_id == "Agent-3":
        for task in current_tasks:
            task_str = str(task).lower()
            if "ssot" in task_str or "infrastructure" in task_str:
                if "ready" in task_str or "support" in task_str:
                    ssot_info["ready"] = True
                    ssot_info["current_step"] = "Ready for infrastructure support"
    
    return ssot_info

def main():
    """Main execution."""
    print("=" * 70)
    print("SSOT VERIFICATION COORDINATION - Batches 2-8")
    print("=" * 70)
    print()
    
    analysis = analyze_ssot_coordination_status()
    
    print("AGENT STATUS:")
    print("-" * 70)
    for agent_id, agent_data in analysis["agents"].items():
        print(f"\n{agent_id}:")
        print(f"  Status: {agent_data['status']}")
        ssot = agent_data["ssot_related"]
        if ssot["accepted"]:
            print(f"  SSOT Verification: ✅ ACCEPTED")
        if ssot["current_step"] != "UNKNOWN":
            print(f"  Current Step: {ssot['current_step']}")
        if ssot["waiting_for_data"]:
            print(f"  ⏳ Waiting for batch data")
        if ssot["ready_to_execute"]:
            print(f"  ✅ Ready to execute")
    
    print()
    print("=" * 70)
    print("COORDINATION STATUS:")
    print("-" * 70)
    for agent, coord_status in analysis["coordination_status"].items():
        print(f"  {agent}: {coord_status['status']}")
        if "note" in coord_status:
            print(f"    {coord_status['note']}")
    
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
    print("NEXT ACTIONS:")
    print("-" * 70)
    if analysis["next_actions"]:
        for action in analysis["next_actions"]:
            print(f"  • {action['action']}")
            print(f"    Priority: {action['priority']}")
            print(f"    Agents: {', '.join(action['agents'])}")
    else:
        print("  No immediate actions identified")
    
    # Save results
    output_path = Path("agent_workspaces/Agent-6/ssot_verification_coordination.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(analysis, f, indent=2)
    
    print()
    print(f"✅ Coordination analysis saved to: {output_path}")

if __name__ == "__main__":
    main()

