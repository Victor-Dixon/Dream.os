#!/usr/bin/env python3
"""Validate all agent status.json files for correctness and completeness."""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple

AGENTS = ["Agent-1", "Agent-2", "Agent-3", "Agent-5", "Agent-6", "Agent-7", "Agent-8"]
PROJECT_ROOT = Path(__file__).parent.parent

REQUIRED_FIELDS = [
    "agent_id",
    "agent_name",
    "status",
    "last_updated",
    "current_mission",
    "mission_priority",
    "current_tasks",
    "completed_tasks",
]

def validate_status_file(agent: str) -> Tuple[bool, List[str]]:
    """Validate a single agent's status.json file."""
    status_file = PROJECT_ROOT / "agent_workspaces" / agent / "status.json"
    issues = []
    
    if not status_file.exists():
        return False, [f"❌ Status file does not exist"]
    
    try:
        content = status_file.read_text(encoding="utf-8")
        data = json.loads(content)
    except json.JSONDecodeError as e:
        return False, [f"❌ JSON parse error: {e}"]
    except Exception as e:
        return False, [f"❌ File read error: {e}"]
    
    # Check required fields
    for field in REQUIRED_FIELDS:
        if field not in data:
            issues.append(f"⚠️ Missing required field: {field}")
    
    # Check timestamp format
    last_updated = data.get("last_updated", "")
    if not last_updated:
        issues.append("⚠️ Missing or empty 'last_updated' field")
    else:
        try:
            # Try to parse timestamp
            if "T" in last_updated:
                parsed_time = datetime.fromisoformat(last_updated.replace("Z", "+00:00"))
            else:
                parsed_time = datetime.strptime(last_updated, "%Y-%m-%d %H:%M:%S")
            
            # Check if recent (within 2 hours)
            now = datetime.now()
            diff_hours = (now.replace(tzinfo=None) - parsed_time.replace(tzinfo=None)).total_seconds() / 3600
            if diff_hours > 2:
                issues.append(f"⚠️ Timestamp stale: {diff_hours:.1f} hours ago")
        except Exception as e:
            issues.append(f"⚠️ Timestamp parse error: {e}")
    
    # Check data types
    if not isinstance(data.get("current_tasks", []), list):
        issues.append("⚠️ 'current_tasks' should be a list")
    if not isinstance(data.get("completed_tasks", []), list):
        issues.append("⚠️ 'completed_tasks' should be a list")
    
    return len(issues) == 0, issues

def validate_all():
    """Validate all agent status files."""
    print("=" * 60)
    print("AGENT STATUS.JSON VALIDATION")
    print("=" * 60)
    print()
    
    now = datetime.now()
    print(f"Current time: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    all_valid = True
    results = {}
    
    for agent in AGENTS:
        is_valid, issues = validate_status_file(agent)
        results[agent] = (is_valid, issues)
        if not is_valid:
            all_valid = False
        
        status_icon = "✅" if is_valid else "❌"
        print(f"{status_icon} {agent}:")
        if is_valid:
            # Show timestamp
            status_file = PROJECT_ROOT / "agent_workspaces" / agent / "status.json"
            try:
                data = json.loads(status_file.read_text(encoding="utf-8"))
                last_updated = data.get("last_updated", "MISSING")
                print(f"   ✅ Valid - Last updated: {last_updated}")
            except:
                print(f"   ✅ Valid")
        else:
            for issue in issues:
                print(f"   {issue}")
        print()
    
    print("=" * 60)
    if all_valid:
        print("✅ ALL STATUS FILES VALID")
    else:
        print("❌ SOME STATUS FILES HAVE ISSUES")
    print("=" * 60)
    
    return results

if __name__ == "__main__":
    validate_all()


