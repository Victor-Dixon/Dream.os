#!/usr/bin/env python3
"""Check end-of-cycle push status."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from core.end_of_cycle_push import EndOfCyclePush

if __name__ == "__main__":
    agent_id = sys.argv[1] if len(sys.argv) > 1 else "Agent-1"
    pusher = EndOfCyclePush(agent_id)
    prep = pusher.prepare_for_push()
    
    print(f"📊 Push Status for {agent_id}:")
    print(f"  Uncommitted files: {len(prep['uncommitted_files'])}")
    print(f"  Unpushed commits: {len(prep['unpushed_commits'])}")
    print(f"  Has changes: {prep['has_changes']}")
    print(f"  Ready for push: {prep['ready_for_push']}")
    
    if prep['uncommitted_files']:
        print(f"\n  Uncommitted files:")
        for f in prep['uncommitted_files'][:10]:
            print(f"    - {f}")
        if len(prep['uncommitted_files']) > 10:
            print(f"    ... and {len(prep['uncommitted_files']) - 10} more")

