#!/usr/bin/env python3
"""
Cleanup Captain Workspace - Archives old files from Agent-4 workspace
"""

import argparse
from pathlib import Path
from datetime import datetime, timedelta
import shutil

def cleanup_workspace(workspace_path: Path, days_old: int = 30, dry_run: bool = False):
    """Archive files older than specified days"""
    workspace = Path(workspace_path)
    if not workspace.exists():
        print(f"❌ Workspace not found: {workspace}")
        return
    
    # Create archive directory
    archive_dir = workspace / "archive" / datetime.now().strftime("%Y-%m-%d")
    cutoff_date = datetime.now() - timedelta(days=days_old)
    
    # Files to keep (always)
    keep_patterns = [
        "status.json",
        "inbox",
        "devlogs",
        "captain_logs",
        "captain_handbook",
        "archive",
        "passdown.json"
    ]
    
    archived = 0
    kept = 0
    
    for file_path in workspace.iterdir():
        if file_path.is_file() and file_path.suffix == ".md":
            # Check if should keep
            should_keep = any(pattern in file_path.name for pattern in keep_patterns)
            
            if should_keep:
                kept += 1
                continue
            
            # Check age
            file_time = datetime.fromtimestamp(file_path.stat().st_mtime)
            if file_time < cutoff_date:
                if not dry_run:
                    archive_dir.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(file_path), str(archive_dir / file_path.name))
                archived += 1
                print(f"{'[DRY RUN] ' if dry_run else ''}📦 Archived: {file_path.name} ({file_time.strftime('%Y-%m-%d')})")
            else:
                kept += 1
    
    print(f"\n📊 Summary:")
    print(f"   Archived: {archived} files")
    print(f"   Kept: {kept} files")
    if not dry_run and archived > 0:
        print(f"   Archive location: {archive_dir}")

def main():
    parser = argparse.ArgumentParser(description="Cleanup Captain workspace - Archive old files")
    parser.add_argument("--workspace", type=str, default="agent_workspaces/Agent-4",
                       help="Path to Captain workspace")
    parser.add_argument("--days", type=int, default=30,
                       help="Archive files older than this many days")
    parser.add_argument("--dry-run", action="store_true",
                       help="Show what would be archived without actually doing it")
    args = parser.parse_args()
    
    cleanup_workspace(Path(args.workspace), days_old=args.days, dry_run=args.dry_run)

if __name__ == "__main__":
    main()


