#!/usr/bin/env python3
"""
Captain Completion Processor - Automated Agent Completion Processing
Automatically processes agent completion messages, awards points, and sends recognition.

⚠️ DEPRECATED: This tool has been migrated to tools_v2.
Use 'python -m tools_v2.toolbelt captain.process_completion' instead.
This file will be removed in future version.

Migrated to: tools_v2/categories/captain_coordination_tools.py → CompletionProcessorTool
Registry: captain.process_completion

Author: Agent-4 (Captain)
Deprecated: 2025-01-27 (Agent-6 - V2 Tools Flattening)
"""

import warnings

warnings.warn(
    "⚠️ DEPRECATED: This tool has been migrated to tools_v2. "
    "Use 'python -m tools_v2.toolbelt captain.process_completion' instead. "
    "This file will be removed in future version.",
    DeprecationWarning,
    stacklevel=2
)

# Legacy compatibility - delegate to tools_v2
# For migration path, use: python -m tools_v2.toolbelt captain.process_completion

import sys
import re
from pathlib import Path
from datetime import datetime

repo_root = Path(__file__).parent.parent
sys.path.insert(0, str(repo_root))


def extract_completion_info(content: str) -> dict:
    """Extract completion information from message content."""
    info = {
        'task': 'Unknown',
        'points': 0,
        'roi': 0,
        'status': 'complete'
    }
    
    # Extract task name
    task_patterns = [
        r'Task[:\s]+([^\n]+)',
        r'Mission[:\s]+([^\n]+)',
        r'File[:\s]+([^\n]+\.py)',
        r'Phase\s+\d+[:\s]+([^\n]+)'
    ]
    for pattern in task_patterns:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            info['task'] = match.group(1).strip()
            break
    
    # Extract points
    points_patterns = [
        r'(\d+)\s*pts',
        r'(\d+)\s*points',
        r'Points[:\s]+(\d+)'
    ]
    for pattern in points_patterns:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            info['points'] = int(match.group(1))
            break
    
    # Extract ROI
    roi_patterns = [
        r'ROI[:\s]+([\d.]+)',
        r'roi[:\s]+([\d.]+)'
    ]
    for pattern in roi_patterns:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            info['roi'] = float(match.group(1))
            break
    
    return info


def process_completion(agent_id: str, message_content: str):
    """Process agent completion and award points."""
    # Delegate to tools_v2 adapter
    try:
        from tools_v2.categories.captain_coordination_tools import CompletionProcessorTool
        
        tool = CompletionProcessorTool()
        result = tool.execute({
            "agent_id": agent_id,
            "message_content": message_content
        }, None)
        
        if result.success:
            print(f"✅ Completion processed for {agent_id}")
            print(f"   Points awarded: {result.output.get('points', 0)}")
            print(f"   Task: {result.output.get('task', 'Unknown')}")
        else:
            print(f"❌ Error: {result.error_message}")
        
        return result.success
    except ImportError:
        # Fallback to original implementation
        info = extract_completion_info(message_content)
        
        # Update leaderboard
        leaderboard_file = Path("runtime/leaderboard.json")
        if leaderboard_file.exists():
            import json
            with open(leaderboard_file) as f:
                leaderboard = json.load(f)
        else:
            leaderboard = {}
        
        if agent_id not in leaderboard:
            leaderboard[agent_id] = {"total_points": 0, "tasks_completed": 0, "completions": []}
        
        leaderboard[agent_id]["total_points"] += info['points']
        leaderboard[agent_id]["tasks_completed"] += 1
        leaderboard[agent_id]["completions"].append({
            "task": info['task'],
            "points": info['points'],
            "roi": info['roi'],
            "timestamp": datetime.now().isoformat()
        })
        
        leaderboard_file.parent.mkdir(parents=True, exist_ok=True)
        with open(leaderboard_file, "w") as f:
            json.dump(leaderboard, f, indent=2)
        
        print(f"✅ Completion processed: {agent_id} - {info['task']} (+{info['points']} pts)")
        return True


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python captain_completion_processor.py <agent-id> <message-content>")
        sys.exit(1)
    
    agent_id = sys.argv[1]
    message_content = sys.argv[2]
    
    process_completion(agent_id, message_content)
