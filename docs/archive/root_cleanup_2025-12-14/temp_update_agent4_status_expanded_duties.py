#!/usr/bin/env python3
"""Update Agent-4 status.json with expanded duties from downsizing."""

import json
import sys
from pathlib import Path
from datetime import datetime

project_root = Path(__file__).resolve().parent
status_file = project_root / "agent_workspaces/Agent-4/status.json"

# Load current status
with open(status_file, 'r', encoding='utf-8') as f:
    status = json.load(f)

# Update with expanded duties
status["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
status["current_mission"] = "Captain Operations - Strategic oversight, swarm coordination, progress monitoring, 4-agent mode gatekeeping + Expanded duties (Agent-6/8/5 coordination)"

# Add expanded duties to current tasks
expanded_duties_tasks = [
    "🚨 4-AGENT MODE GATEKEEPING (A4-CAPTAIN-GATES-001): Enforce dependency chain, test gates, status hygiene",
    "📊 FORCE MULTIPLIER MONITORING (FROM Agent-6): Track 4-agent parallel execution, acceleration metrics",
    "🔄 LOOP CLOSURE COORDINATION (FROM Agent-6): Track incomplete loops, coordinate closure campaigns",
    "💬 SWARM COMMUNICATION (FROM Agent-6): Manage inter-agent communication, monitor bottlenecks",
    "✅ QA VALIDATION COORDINATION (FROM Agent-8): Coordinate QA for Agent-1 refactors, Agent-3 infrastructure",
    "🎯 QUALITY OVERSIGHT (FROM Agent-8): Monitor code quality, enforce V2 compliance, review quality gates",
    "🔗 CROSS-DOMAIN COORDINATION (FROM Agent-5): Monitor cross-domain work, coordinate boundaries",
    "📋 AUDIT COORDINATION (FROM Agent-5): Manage audit activities, track completion"
]

# Merge with existing tasks (avoid duplicates)
existing_tasks = status.get("current_tasks", [])
new_tasks = []
for task in expanded_duties_tasks:
    if not any(task.split(":")[0] in existing_task for existing_task in existing_tasks):
        new_tasks.append(task)

status["current_tasks"] = existing_tasks[:5] + new_tasks  # Keep first 5 existing, add new

# Add expanded duties section
status["expanded_duties"] = {
    "from_agent_6": {
        "force_multiplier_monitoring": "Track parallel execution across 4-agent system",
        "loop_closure_coordination": "Coordinate loop closure campaigns",
        "swarm_communication": "Manage inter-agent communication"
    },
    "from_agent_8": {
        "qa_validation_coordination": "Coordinate QA validation for other agents' work",
        "quality_oversight": "Monitor code quality across all agents"
    },
    "from_agent_5": {
        "cross_domain_coordination": "Oversee cross-domain coordination",
        "audit_coordination": "Manage audit coordination activities"
    }
}

# Save updated status
with open(status_file, 'w', encoding='utf-8') as f:
    json.dump(status, f, indent=2, ensure_ascii=False)

print("✅ Agent-4 status.json updated with expanded duties")
print(f"   Last updated: {status['last_updated']}")
print(f"   Total current tasks: {len(status['current_tasks'])}")

