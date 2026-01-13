#!/usr/bin/env python3
"""Check queue status breakdown."""
import json
import sys
from pathlib import Path
from collections import Counter

sys.path.insert(0, str(Path(__file__).parent.parent))

qf = Path('message_queue/queue.json')
d = json.loads(qf.read_text()) if qf.exists() else {'entries': []}
entries = d.get('entries', []) if isinstance(d, dict) else d
statuses = Counter([e.get('status', 'UNKNOWN') for e in entries if isinstance(e, dict)])

print('Status breakdown:')
for status, count in statuses.items():
    print(f'  {status}: {count}')

