#!/usr/bin/env python3
"""Check failed messages and their errors."""
import json
import sys
from pathlib import Path
from collections import Counter

sys.path.insert(0, str(Path(__file__).parent.parent))

qf = Path('message_queue/queue.json')
d = json.loads(qf.read_text()) if qf.exists() else {'entries': []}
entries = d.get('entries', []) if isinstance(d, dict) else d
failed = [e for e in entries if isinstance(e, dict) and e.get('status') == 'FAILED']

print(f'Total failed messages: {len(failed)}')
print('\nError breakdown:')
errors = Counter([e.get('error', 'No error') for e in failed])
for error, count in errors.most_common(10):
    print(f'  {error}: {count}')

print('\nRecent failed messages:')
for e in failed[-5:]:
    print(f"  Queue ID: {e.get('queue_id', 'unknown')[:8]}")
    print(f"  Error: {e.get('error', 'No error')}")
    print(f"  Recipient: {e.get('message', {}).get('recipient', 'unknown')}")
    print()

