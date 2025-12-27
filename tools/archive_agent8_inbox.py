#!/usr/bin/env python3
"""Archive old Agent-8 inbox messages."""
import shutil
from pathlib import Path
from datetime import datetime

inbox = Path('agent_workspaces/Agent-8/inbox')
archive = inbox / 'archive' / f'{datetime.now().strftime("%Y-%m-%d")}_processed'
archive.mkdir(parents=True, exist_ok=True)

# Archive messages older than 7 days (before 2025-12-19)
archived = 0
for f in inbox.glob('*.md'):
    # Archive messages from Dec 6-18 (old messages)
    if any(date in f.name for date in ['20251206', '20251207', '20251208', '20251210', '20251211', '20251212', '20251213', '20251217', '20251218']):
        shutil.move(str(f), str(archive / f.name))
        archived += 1

print(f'✅ Archived {archived} old messages to {archive}')

