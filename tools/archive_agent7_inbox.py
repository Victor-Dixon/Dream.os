#!/usr/bin/env python3
"""Archive old Agent-7 inbox messages."""
import shutil
from pathlib import Path
from datetime import datetime

inbox = Path('agent_workspaces/Agent-7/inbox')
archive = inbox / 'archive' / f'{datetime.now().strftime("%Y-%m-%d")}_processed'
archive.mkdir(parents=True, exist_ok=True)

archived = 0
for f in inbox.glob('*.md'):
    if any(date in f.name for date in ['2025-12-18', '2025-12-19', '2025-12-20']):
        shutil.move(str(f), str(archive / f.name))
        archived += 1

print(f'✅ Archived {archived} old messages to {archive}')

