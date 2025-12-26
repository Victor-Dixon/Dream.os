#!/usr/bin/env python3
"""
Cleanup Agent-1 Inbox
====================

Archives old messages from Agent-1 inbox, keeping only recent/active messages.

V2 Compliance | Author: Agent-1 | Date: 2025-12-26
"""

import shutil
from pathlib import Path
from datetime import datetime, timedelta

def cleanup_inbox():
    """Archive old messages from inbox."""
    inbox_file = Path("agent_workspaces/Agent-1/inbox/Agent-1_inbox.txt")
    archive_dir = Path("agent_workspaces/Agent-1/inbox/archive")
    archive_dir.mkdir(parents=True, exist_ok=True)
    
    if not inbox_file.exists():
        print("No inbox file found")
        return
    
    # Read current inbox
    with open(inbox_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Archive old file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_file = archive_dir / f"Agent-1_inbox_archived_{timestamp}.txt"
    
    with open(archive_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    # Clear inbox (keep it empty for new messages)
    with open(inbox_file, 'w', encoding='utf-8') as f:
        f.write("# Agent-1 Inbox\n")
        f.write(f"# Last cleaned: {datetime.now().isoformat()}\n")
        f.write("# Old messages archived to archive/ directory\n\n")
    
    print(f"✅ Inbox cleaned. Archived to: {archive_file}")
    print(f"   Original messages: {len(content.split('==================================================')) - 1} messages")
    print(f"   Archive file: {archive_file}")

if __name__ == "__main__":
    cleanup_inbox()

