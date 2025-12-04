#!/usr/bin/env python3
"""Archive processed inbox messages for Agent-4."""
from pathlib import Path
from datetime import datetime

inbox = Path('agent_workspaces/Agent-4/inbox')
archive = inbox / 'archive'
archive.mkdir(exist_ok=True)

# Archive all .md files except response files
messages = list(inbox.glob('*.md'))
archived = 0

for msg in messages:
    # Skip response files (keep them for now)
    if 'CAPTAIN_SUPPORT_RESPONSE' in msg.name or 'CAPTAIN_ACK' in msg.name:
        continue
    try:
        msg.rename(archive / msg.name)
        archived += 1
    except Exception as e:
        print(f"⚠️ Could not archive {msg.name}: {e}")

print(f"✅ Archived {archived} messages to {archive}")
print(f"📁 Remaining messages: {len(list(inbox.glob('*.md')))}")



