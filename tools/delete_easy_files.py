#!/usr/bin/env python3
"""
Delete easy deletion candidates safely.
"""

import os
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
DELETION_LIST = REPO_ROOT / 'DELETION_CANDIDATES_EASY.txt'

def main():
    """Delete files from deletion list."""
    if not DELETION_LIST.exists():
        print("❌ Deletion list not found. Run find_easy_deletions.py first.")
        return
    
    deletions = []
    with open(DELETION_LIST, 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if line and not line.startswith('=') and not line.startswith('Reason:') and not line.startswith('Easy Deletions'):
                if line and not line.startswith('  '):  # File path (not indented)
                    deletions.append(REPO_ROOT / line)
    
    print(f"🗑️  Deleting {len(deletions)} files...\n")
    
    deleted = 0
    failed = 0
    
    for filepath in deletions:
        try:
            if filepath.exists():
                filepath.unlink()
                print(f"  ✅ Deleted: {filepath.relative_to(REPO_ROOT)}")
                deleted += 1
            else:
                print(f"  ⚠️  Not found: {filepath.relative_to(REPO_ROOT)}")
        except Exception as e:
            print(f"  ❌ Failed: {filepath.relative_to(REPO_ROOT)} - {e}")
            failed += 1
    
    print(f"\n✅ Deleted: {deleted}")
    if failed > 0:
        print(f"❌ Failed: {failed}")
    
    # Delete the deletion list
    if DELETION_LIST.exists():
        DELETION_LIST.unlink()
        print(f"✅ Cleaned up deletion list")

if __name__ == '__main__':
    main()

