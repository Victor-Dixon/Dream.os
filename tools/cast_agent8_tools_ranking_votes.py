#!/usr/bin/env python3
"""
Cast Tools Ranking Debate Votes - Agent-8
===========================================

Casts votes on all 6 categories for the tools ranking debate.
Agent-8 (SSOT & System Integration Specialist) perspective.

Author: Agent-8
Date: 2025-12-02
Priority: CRITICAL
"""

import json
from pathlib import Path
from datetime import datetime

debate_id = "debate_tools_ranking_20251124"
agent_id = "Agent-8"

debate_file = Path("debates") / f"{debate_id}.json"

if not debate_file.exists():
    print(f"❌ Debate file not found: {debate_file}")
    exit(1)

# Load debate
with open(debate_file, 'r', encoding='utf-8') as f:
    debate_data = json.load(f)

# Agent-8's votes (SSOT & System Integration Specialist)
votes = [
    {
        "option": "Best Overall Tool (Most Useful)",
        "argument": (
            "As SSOT specialist, toolbelt_registry.py provides the foundation for all tool "
            "discovery and execution. It is the single source of truth for tool availability. "
            "Without it, we cannot organize, find, or use any other tools. SSOT foundation "
            "enables all other tools to function."
        ),
        "confidence": 9
    },
    {
        "option": "Best Monitoring Tool",
        "argument": (
            "workspace-health provides visibility into agent workspace status, enabling "
            "proactive coordination and swarm health monitoring. Essential for detecting "
            "stalled agents and maintaining swarm health. Monitoring is critical for SSOT "
            "compliance and coordination effectiveness."
        ),
        "confidence": 9
    },
    {
        "option": "Best Automation Tool",
        "argument": (
            "orchestrate (Swarm Orchestrator/Gas Station) automates coordination and reduces "
            "manual overhead by 90%. Enables continuous workflow through automated gas pipeline. "
            "Automation is fundamental to SSOT maintenance and coordination efficiency."
        ),
        "confidence": 9
    },
    {
        "option": "Best Analysis Tool",
        "argument": (
            "scan (Project Scanner) provides comprehensive project analysis essential for "
            "coordination decisions and understanding codebase structure. Foundation for SSOT "
            "verification and coordination analysis. Critical for identifying duplicates and "
            "maintaining single source of truth."
        ),
        "confidence": 9
    },
    {
        "option": "Best Quality Tool",
        "argument": (
            "v2-check (V2 Compliance Checker) enforces architectural standards critical for "
            "coordination and ensures code quality across the swarm. Quality tools ensure SSOT "
            "compliance and maintainability. Essential for maintaining architectural standards."
        ),
        "confidence": 9
    },
    {
        "option": "Most Critical Tool",
        "argument": (
            "toolbelt_registry.py is the most critical tool as it provides the SSOT foundation. "
            "Without it, we cannot organize, find, or use any other tools. It is the single "
            "source of truth for tool availability. Critical tools are the foundation - without "
            "them, monitoring, automation, analysis, and quality are meaningless. SSOT foundation "
            "enables all other tools to function."
        ),
        "confidence": 10
    }
]

print(f"🗳️ Casting All Votes for Tools Ranking Debate")
print(f"📋 Debate ID: {debate_id}")
print(f"🤖 Agent: {agent_id}")
print("=" * 60)

# Initialize votes and arguments if needed
if "votes" not in debate_data:
    debate_data["votes"] = {}
if "arguments" not in debate_data:
    debate_data["arguments"] = []

# Cast each vote
votes_cast = 0
for vote in votes:
    option = vote["option"]
    argument = vote["argument"]
    confidence = vote.get("confidence", 5)
    
    print(f"\n📊 Voting: {option}")
    
    # Record vote
    vote_data = {
        "option": option,
        "timestamp": datetime.now().isoformat(),
        "confidence": confidence,
        "argument": argument,
    }
    
    # Store vote (using option as key for multiple votes per agent)
    vote_key = f"{agent_id}_{option.replace(' ', '_').replace('(', '').replace(')', '')}"
    debate_data["votes"][vote_key] = vote_data
    
    # Add to arguments
    debate_data["arguments"].append({
        "agent_id": agent_id,
        "option": option,
        "argument": argument,
        "confidence": confidence,
        "timestamp": vote_data["timestamp"],
    })
    
    votes_cast += 1
    print(f"   ✅ Vote cast (Confidence: {confidence}/10)")

# Save updated debate
debate_file.write_text(json.dumps(debate_data, indent=2), encoding="utf-8")

print("\n" + "=" * 60)
print(f"✅ All {votes_cast} votes cast successfully!")
print(f"📝 Debate file updated: {debate_file}")
print("\n🐝 WE. ARE. SWARM. ⚡🔥")

