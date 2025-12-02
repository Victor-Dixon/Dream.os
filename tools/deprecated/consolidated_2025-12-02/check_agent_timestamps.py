#!/usr/bin/env python3
"""Check agent status.json timestamps for sync issues."""

import json
from pathlib import Path
from datetime import datetime

AGENTS = ["Agent-1", "Agent-2", "Agent-3", "Agent-5", "Agent-6", "Agent-7", "Agent-8"]
PROJECT_ROOT = Path(__file__).parent.parent

def check_timestamps():
    """Check all agent timestamps."""
    now = datetime.now()
    print("=" * 60)
    print("AGENT TIMESTAMP CHECK")
    print("=" * 60)
    print(f"Current time: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    for agent in AGENTS:
        status_file = PROJECT_ROOT / "agent_workspaces" / agent / "status.json"
        if not status_file.exists():
            print(f"{agent}: ❌ NO STATUS FILE")
            continue
        
        try:
            data = json.loads(status_file.read_text(encoding="utf-8"))
            last_updated_str = data.get("last_updated", "MISSING")
            
            if last_updated_str == "MISSING":
                print(f"{agent}: ❌ MISSING TIMESTAMP")
                continue
            
            # Parse timestamp
            try:
                # Try ISO format
                if "T" in last_updated_str:
                    last_updated = datetime.fromisoformat(last_updated_str.replace("Z", "+00:00"))
                else:
                    # Try simple format
                    last_updated = datetime.strptime(last_updated_str, "%Y-%m-%d %H:%M:%S")
                
                # Calculate difference
                diff = (now.replace(tzinfo=None) - last_updated.replace(tzinfo=None)).total_seconds() / 3600
                
                if diff < 2:
                    status = "✅ RECENT"
                elif diff < 24:
                    status = "⚠️ STALE"
                else:
                    status = "❌ VERY STALE"
                
                print(f"{agent}: {status} - {last_updated_str} ({diff:.1f} hours ago)")
            except Exception as e:
                print(f"{agent}: ❌ PARSE ERROR - {last_updated_str} ({e})")
        except Exception as e:
            print(f"{agent}: ❌ ERROR - {e}")
    
    print()
    print("=" * 60)

if __name__ == "__main__":
    check_timestamps()


