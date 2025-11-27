#!/usr/bin/env python3
"""
Create Tools Debate - Rank Toolbelt Tools
==========================================

Creates a debate session to rank and compare tools on the toolbelt.
Uses the debate system to determine which tool is the best.

Author: Agent-6 (Coordination & Communication Specialist)
Date: 2025-11-24
Priority: HIGH
"""

import json
import sys
import time
from pathlib import Path
from typing import List, Dict, Any

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

# Import toolbelt registry - use direct import to avoid __init__.py issues
try:
    # Import directly from toolbelt_registry to avoid __init__.py dependencies
    import importlib.util
    registry_path = project_root / "tools" / "toolbelt_registry.py"
    spec = importlib.util.spec_from_file_location("toolbelt_registry", registry_path)
    toolbelt_registry_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(toolbelt_registry_module)
    TOOLS_REGISTRY = toolbelt_registry_module.TOOLS_REGISTRY
    ToolRegistry = toolbelt_registry_module.ToolRegistry
except Exception as e:
    print(f"⚠️ Could not import toolbelt_registry: {e}")
    TOOLS_REGISTRY = {}
    ToolRegistry = None


def get_all_toolbelt_tools() -> List[Dict[str, Any]]:
    """Get all tools from toolbelt registry."""
    if TOOLS_REGISTRY:
        # Direct access to TOOLS_REGISTRY
        return [{"id": tool_id, **config} for tool_id, config in TOOLS_REGISTRY.items()]
    elif ToolRegistry:
        registry = ToolRegistry()
        return registry.list_tools()
    else:
        return []


def create_tools_debate() -> Dict[str, Any]:
    """Create a debate to rank toolbelt tools."""
    tools = get_all_toolbelt_tools()
    
    if not tools:
        print("⚠️ No tools found in toolbelt registry")
        return {}
    
    # Create debate topic
    topic = "Rank Toolbelt Tools - Which tool is the best?"
    
    # Get all agents as participants
    participants = [
        "Agent-1", "Agent-2", "Agent-3", "Agent-5", 
        "Agent-6", "Agent-7", "Agent-8", "Agent-4"
    ]
    
    # Create debate session
    debate_data = {
        "ts": time.time(),
        "topic": topic,
        "participants": participants,
        "duration_hours": 48,  # 2 days for debate
        "tools_count": len(tools),
        "tools": [{"id": t["id"], "name": t["name"]} for t in tools]
    }
    
    # Save to debate sessions
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    debate_file = data_dir / "debate.sessions.jsonl"
    with open(debate_file, 'a', encoding='utf-8') as f:
        f.write(json.dumps(debate_data) + '\n')
    
    print(f"✅ Debate created: {topic}")
    print(f"📊 Tools to rank: {len(tools)}")
    print(f"👥 Participants: {', '.join(participants)}")
    print(f"⏰ Duration: 48 hours")
    print(f"\n📋 Tools in debate:")
    for i, tool in enumerate(tools[:10], 1):  # Show first 10
        print(f"   {i}. {tool['name']} ({tool['id']})")
    if len(tools) > 10:
        print(f"   ... and {len(tools) - 10} more tools")
    
    return debate_data


def main():
    """Main entry point."""
    print("🔍 Creating tools debate...")
    debate = create_tools_debate()
    
    if debate:
        print(f"\n✅ Debate created successfully!")
        print(f"📝 Topic: {debate['topic']}")
        print(f"🎯 Use 'debate.vote' to vote on tools")
        print(f"📊 Use 'debate.status' to check results")


if __name__ == "__main__":
    main()

