#!/usr/bin/env python3
"""
Cleanup Agent-3 Inbox
Archives old messages (>7 days) to archive directory
"""

import os
import shutil
from pathlib import Path
from datetime import datetime, timedelta

INBOX_DIR = Path("agent_workspaces/Agent-3/inbox")
ARCHIVE_DIR = INBOX_DIR / "archive" / f"{datetime.now().strftime('%Y-%m-%d')}_processed"
ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)

def cleanup_inbox():
    """Archive messages older than 7 days."""
    cutoff_date = datetime.now() - timedelta(days=7)
    archived_count = 0
    
    for file_path in INBOX_DIR.glob("*.md"):
        if file_path.name == "Agent-3_inbox.txt":
            continue
            
        file_time = datetime.fromtimestamp(file_path.stat().st_mtime)
        
        if file_time < cutoff_date:
            dest = ARCHIVE_DIR / file_path.name
            shutil.move(str(file_path), str(dest))
            archived_count += 1
            print(f"✅ Archived: {file_path.name}")
    
    print(f"\n✅ Cleanup complete: {archived_count} files archived to {ARCHIVE_DIR}")
    return archived_count

if __name__ == "__main__":
    cleanup_inbox()

