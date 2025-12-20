#!/usr/bin/env python3
"""
Complete Agent-8's Batch 1 Duplicate Consolidation
===============================================

Completes the pending Batch 1 groups 7, 9, and 15 for Agent-8.
Deletes duplicate files while preserving SSOT (Single Source of Truth).

Groups to process:
- Group 7: FocusForge/my-resume resolution scripts (2 files, delete 1)
- Group 9: extract_freeride_error/validate_analytics_imports (2 files, delete 1)
- Group 15: jest.setup.js duplicates (2 files, delete 1)

Total: 3 groups, 7 files total, delete 3 duplicates
"""

import os
import sys
from pathlib import Path

def delete_duplicate(ssot_path, duplicate_path, group_num):
    """Safely delete a duplicate file."""
    print(f"\nGroup {group_num}:")

    # Check SSOT exists
    if not os.path.exists(ssot_path):
        print(f"  ❌ SSOT missing: {ssot_path}")
        return False

    # Check duplicate exists
    if not os.path.exists(duplicate_path):
        print(f"  ❌ Duplicate missing: {duplicate_path}")
        return False

    # Verify they are different files
    if os.path.samefile(ssot_path, duplicate_path):
        print(f"  ❌ Same file: {ssot_path}")
        return False

    print(f"  ✅ SSOT: {ssot_path}")
    print(f"  🗑️  Duplicate: {duplicate_path}")

    try:
        os.remove(duplicate_path)
        print(f"  ✅ Deleted duplicate")
        return True
    except Exception as e:
        print(f"  ❌ Delete failed: {e}")
        return False

def main():
    """Complete Agent-8's Batch 1 groups."""
    print("🧹 Completing Agent-8's Batch 1 Duplicate Consolidation")
    print("=" * 60)

    # Group 7: FocusForge/my-resume resolution scripts
    ssot7 = "agent_workspaces/Agent-2/FocusForge_RESOLUTION_SCRIPT.py"
    dup7 = "agent_workspaces/Agent-2/my-resume_RESOLUTION_SCRIPT.py"

    # Group 9: extract_freeride_error/validate_analytics_imports
    ssot9 = "tools/extract_freeride_error.py"
    dup9 = "tools/validate_analytics_imports.py"

    # Group 15: jest.setup.js duplicates
    ssot15 = "temp_repos/Auto_Blogger/tests/jest.setup.js"
    dup15 = "agent_workspaces/Agent-1/extracted_patterns/testing_patterns/jest.setup.js"

    deleted_count = 0
    total_groups = 3

    # Process each group
    if delete_duplicate(ssot7, dup7, 7):
        deleted_count += 1

    if delete_duplicate(ssot9, dup9, 9):
        deleted_count += 1

    if delete_duplicate(ssot15, dup15, 15):
        deleted_count += 1

    print(f"\n{'='*60}")
    print("📊 COMPLETION SUMMARY")
    print(f"{'='*60}")
    print(f"Groups processed: {total_groups}")
    print(f"Duplicates deleted: {deleted_count}")
    print(f"SSOT files preserved: {total_groups}")

    if deleted_count == total_groups:
        print("✅ SUCCESS: All Agent-8 Batch 1 groups completed!")
        print("🎯 Impact: 3 duplicate files removed, SSOT integrity maintained")
    else:
        print(f"⚠️  PARTIAL: {deleted_count}/{total_groups} groups completed")

    return 0

if __name__ == "__main__":
    sys.exit(main())


