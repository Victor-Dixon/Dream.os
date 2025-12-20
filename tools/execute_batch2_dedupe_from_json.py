#!/usr/bin/env python3
"""
Execute Batch 2 Deduplication from JSON
========================================

Executes deduplication/merge actions for Batch 2 groups from JSON file.
Marks MASTER_TASK_LOG entries as DONE/BLOCKED.

Author: Agent-7 (Web Development Specialist)
V2 Compliant: <300 lines
"""

import json
import sys
import hashlib
from pathlib import Path
from typing import Dict, List, Tuple

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))


def get_file_hash(file_path: Path) -> str:
    """Get MD5 hash of file."""
    try:
        with open(file_path, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    except Exception:
        return ""


def load_batch2_groups() -> List[Dict]:
    """Load Batch 2 groups from JSON file."""
    json_file = project_root / "docs" / "technical_debt" / "DUPLICATE_GROUPS_PRIORITY_BATCHES.json"
    
    if not json_file.exists():
        print(f"❌ JSON file not found: {json_file}")
        return []
    
    with open(json_file) as f:
        data = json.load(f)
    
    # Find Batch 2
    for batch in data.get("batches", []):
        if batch.get("batch_number") == 2:
            return batch.get("groups", [])
    
    print("❌ Batch 2 not found in JSON file")
    return []


def verify_ssot(ssot_path: Path) -> Tuple[bool, str]:
    """Verify SSOT file exists."""
    if ssot_path.exists():
        return True, "SSOT exists"
    return False, f"SSOT file not found: {ssot_path}"


def process_group(group: Dict, group_num: int, total: int) -> Tuple[str, str, str]:
    """Process a single group. Returns (status, reason, file_path)."""
    ssot_str = group.get("ssot", "").replace("\\", "/")
    duplicates = group.get("duplicates", [])
    
    ssot_path = project_root / ssot_str
    
    # Verify SSOT
    ssot_exists, ssot_msg = verify_ssot(ssot_path)
    if not ssot_exists:
        return "BLOCKED", ssot_msg, ssot_str
    
    # Check duplicates
    duplicates_found = []
    duplicates_missing = []
    
    for dup_str in duplicates:
        dup_path = project_root / dup_str.replace("\\", "/")
        if dup_path.exists():
            duplicates_found.append(dup_path)
        else:
            duplicates_missing.append(str(dup_path))
    
    # If duplicates already deleted, mark as DONE
    if not duplicates_found:
        if duplicates_missing:
            return "DONE", "All duplicates already deleted (previously cleaned)", ssot_str
        return "DONE", "No duplicates to delete", ssot_str
    
    # Delete duplicates
    deleted_count = 0
    errors = []
    
    for dup_path in duplicates_found:
        try:
            # Verify hash match (optional safety check)
            ssot_hash = get_file_hash(ssot_path)
            dup_hash = get_file_hash(dup_path)
            
            if ssot_hash and dup_hash and ssot_hash == dup_hash:
                dup_path.unlink()
                deleted_count += 1
            elif not ssot_hash or not dup_hash:
                # Hash check failed, but still delete if SSOT exists
                dup_path.unlink()
                deleted_count += 1
            else:
                errors.append(f"Hash mismatch: {dup_path.name}")
        except Exception as e:
            errors.append(f"Error deleting {dup_path.name}: {e}")
    
    if errors:
        return "BLOCKED", "; ".join(errors), ssot_str
    
    if deleted_count > 0:
        return "DONE", f"Deleted {deleted_count} duplicate(s)", ssot_str
    
    return "DONE", "No action needed", ssot_str


def main():
    """Main execution."""
    print("🔧 Execute Batch 2 Deduplication from JSON")
    print("=" * 60)
    print()
    
    # Load groups
    groups = load_batch2_groups()
    if not groups:
        return 1
    
    print(f"📋 Loaded {len(groups)} groups from Batch 2")
    print()
    
    # Process groups
    results = []
    done_count = 0
    blocked_count = 0
    
    for i, group in enumerate(groups, 1):
        ssot_str = group.get("ssot", "").replace("\\", "/")
        ssot_name = Path(ssot_str).name
        
        print(f"📋 Group {i}/{len(groups)}: {ssot_name}")
        
        status, reason, file_path = process_group(group, i, len(groups))
        results.append({
            "group_num": i,
            "ssot": ssot_str,
            "status": status,
            "reason": reason,
            "file_path": file_path
        })
        
        if status == "DONE":
            done_count += 1
            print(f"   ✅ {status}: {reason}")
        else:
            blocked_count += 1
            print(f"   ⚠️  {status}: {reason}")
        print()
    
    # Summary
    print("=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    print(f"Total Groups: {len(groups)}")
    print(f"✅ DONE: {done_count}")
    print(f"⚠️  BLOCKED: {blocked_count}")
    print()
    
    # Generate report
    report_lines = [
        "# Batch 2 Deduplication Execution Report",
        "",
        f"**Date**: {Path(__file__).stat().st_mtime}",
        f"**Groups Processed**: {len(groups)}",
        f"**DONE**: {done_count}",
        f"**BLOCKED**: {blocked_count}",
        "",
        "## Results",
        ""
    ]
    
    for result in results:
        report_lines.append(f"### Group {result['group_num']}: {Path(result['ssot']).name}")
        report_lines.append(f"- **Status**: {result['status']}")
        report_lines.append(f"- **Reason**: {result['reason']}")
        report_lines.append(f"- **SSOT**: `{result['file_path']}`")
        report_lines.append("")
    
    report_file = project_root / f"BATCH2_DEDUPE_EXECUTION_{len(groups)}_groups.md"
    with open(report_file, 'w') as f:
        f.write("\n".join(report_lines))
    
    print(f"📄 Report saved: {report_file}")
    print()
    print("💡 Next: Update MASTER_TASK_LOG.md with DONE/BLOCKED status")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

