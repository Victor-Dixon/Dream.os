#!/usr/bin/env python3
"""
Start Tools Ranking Debate - Direct Import
===========================================

Bypasses circular import issues to start tools ranking debate.

Author: Agent-8 (SSOT & System Integration Specialist)
Date: 2025-01-27
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timedelta

# Direct import to avoid circular import
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import debate tools directly
from tools_v2.categories.debate_tools import DebateStartTool, DebateNotifyTool


def start_tools_ranking_debate():
    """Start debate to rank tools."""
    debate_tool = DebateStartTool()
    
    result = debate_tool.execute({
        "topic": "Rank Tools in Consolidated Tools Directory - Which is the Best Tool on the Toolbelt?",
        "description": "Ranking 229 tools in consolidated tools directory to identify the best tool on the toolbelt. This debate will help us consolidate and organize our toolbelt foundation.",
        "options": [
            "Best Overall Tool (Most Useful)",
            "Best Monitoring Tool",
            "Best Automation Tool",
            "Best Analysis Tool",
            "Best Quality Tool",
            "Most Critical Tool",
        ],
        "deadline": (datetime.now() + timedelta(hours=48)).isoformat(),
    })
    
    if result.success:
        debate_id = result.output["debate_id"]
        print(f"✅ Debate started: {debate_id}")
        print(f"📋 Topic: {result.output['topic']}")
        print(f"🗳️ Options: {len(result.output['options'])} options")
        
        # Notify all agents
        notify_tool = DebateNotifyTool()
        notify_result = notify_tool.execute({
            "debate_id": debate_id,
            "urgency": "high",
        })
        
        if notify_result.success:
            print(f"✅ Notified {notify_result.output['notifications_sent']} agents")
        
        return debate_id
    else:
        print(f"❌ Failed to start debate: {result.output}")
        return None


if __name__ == "__main__":
    debate_id = start_tools_ranking_debate()
    if debate_id:
        print(f"\n📝 Next steps:")
        print(f"   1. Agents vote using: python -m tools_v2.toolbelt debate.vote --debate-id {debate_id} --agent Agent-X --option 'Best Overall Tool' --argument 'Your reasoning'")
        print(f"   2. Check status: python -m tools_v2.toolbelt debate.status --debate-id {debate_id}")
        print(f"\n🐝 WE. ARE. SWARM. ⚡🔥")


