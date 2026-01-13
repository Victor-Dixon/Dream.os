#!/usr/bin/env python3
"""Execute end-of-cycle push for an agent."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from core.end_of_cycle_push import EndOfCyclePush
from core.daily_cycle_tracker import DailyCycleTracker

if __name__ == "__main__":
    agent_id = sys.argv[1] if len(sys.argv) > 1 else "Agent-1"
    
    # Get today's summary
    tracker = DailyCycleTracker(agent_id)
    summary = tracker.get_today_summary()
    
    # Create commit message
    commit_msg = (
        f"Cycle {summary['date']}: {summary['tasks_completed']} tasks, "
        f"{summary['interactions']} interactions, "
        f"{summary.get('points_earned', 0)} pts"
    )
    
    # Execute push
    pusher = EndOfCyclePush(agent_id)
    result = pusher.execute_push(commit_msg)
    
    # Mark as pushed if successful
    if result['success']:
        tracker.mark_pushed()
        tracker.record_commit()
        print(f"✅ Push successful for {agent_id}")
        print(f"   Committed: {result.get('committed', False)}")
        print(f"   Pushed: {result.get('pushed', False)}")
    else:
        print(f"❌ Push failed: {result.get('error', 'Unknown error')}")
        sys.exit(1)

