#!/usr/bin/env python3
"""
Start Tools Ranking Debate - Proper Format
==========================================

Creates a proper debate using the debate.start tool to rank toolbelt tools.

Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2025-11-24
Priority: CRITICAL
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

# Import debate tools directly to avoid circular import
import importlib.util
debate_tools_path = project_root / "tools_v2" / "categories" / "debate_tools.py"
spec = importlib.util.spec_from_file_location("debate_tools", debate_tools_path)
debate_tools_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(debate_tools_module)
DebateStartTool = debate_tools_module.DebateStartTool


def main():
    """Start tools ranking debate."""
    print("🗳️ Starting tools ranking debate...\n")
    
    # Create debate tool
    debate_tool = DebateStartTool()
    
    # Debate parameters
    params = {
        "topic": "Rank Toolbelt Tools - Which tool is the best on the toolbelt?",
        "description": "Ranking 60 tools in consolidated tools directory to identify best tool on toolbelt. This debate will help us clean our own project by identifying the most valuable tools.",
        "options": [
            "Best Overall Tool (Most Useful)",
            "Best Monitoring Tool",
            "Best Automation Tool",
            "Best Analysis Tool",
            "Best Quality Tool",
            "Most Critical Tool"
        ],
        "deadline": None  # No deadline - open until all agents vote
    }
    
    # Start debate
    result = debate_tool.execute(params)
    
    if result.success:
        debate_id = result.output["debate_id"]
        print(f"✅ Debate started successfully!")
        print(f"📋 Debate ID: {debate_id}")
        print(f"📝 Topic: {result.output['topic']}")
        print(f"🎯 Options: {len(result.output['options'])} options")
        print(f"\n🗳️ Next steps:")
        print(f"   1. Notify all agents to vote")
        print(f"   2. Use: debate.vote --debate-id {debate_id} --agent-id Agent-X --option 'Best Overall Tool (Most Useful)'")
        print(f"   3. Check status: debate.status --debate-id {debate_id}")
        return 0
    else:
        print(f"❌ Failed to start debate: {result.output}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

