#!/usr/bin/env python3
"""Initialize daily cycle for an agent."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from core.daily_cycle_tracker import DailyCycleTracker

if __name__ == "__main__":
    agent_id = sys.argv[1] if len(sys.argv) > 1 else "Agent-1"
    tracker = DailyCycleTracker(agent_id)
    day = tracker.start_new_day()
    print(f"✅ Daily cycle started for {agent_id}")
    print(f"   Date: {day['date']}")
    print(f"   Start time: {day['start_time']}")

