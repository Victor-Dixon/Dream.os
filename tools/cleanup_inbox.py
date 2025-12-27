#!/usr/bin/env python3
"""Clean up old inbox messages."""
import shutil
from pathlib import Path
from datetime import datetime

inbox = Path('agent_workspaces/Agent-5/inbox')
archive = inbox / 'archive' / f'processed_{datetime.now().strftime("%Y%m%d")}'
archive.mkdir(parents=True, exist_ok=True)

old_files = [f for f in inbox.glob('*.md') if f.is_file()]
for f in old_files:
    shutil.move(str(f), str(archive / f.name))

print(f'Archived {len(old_files)} inbox messages to {archive}')

