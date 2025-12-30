#!/usr/bin/env python3
"""
Check Audit Evidence Utility
Quick utility to verify audit evidence exists and is fresh for closure validation.

<!-- SSOT Domain: tools -->
"""
import json
import glob
import sys
from pathlib import Path
from datetime import datetime

def check_latest_audit_evidence():
    """Check if latest audit evidence exists and is fresh."""
    reports_dir = Path("reports")
    if not reports_dir.exists():
        print("❌ Reports directory not found")
        return 1
    
    audit_files = sorted(glob.glob(str(reports_dir / "working_tree_audit_*.json")), reverse=True)
    if not audit_files:
        print("⚠️  No audit evidence found (this is OK if no audit has been run yet)")
        print("   Run: python tools/working_tree_audit.py --agent Agent-X")
        return 0  # Not an error - just informational
    
    latest = Path(audit_files[0])
    try:
        with open(latest, 'r') as f:
            data = json.load(f)
        
        ts_str = data.get("ts", "")
        if not ts_str:
            print("❌ Audit evidence missing timestamp")
            return 1
        
        audit_time = datetime.strptime(ts_str, "%Y%m%d_%H%M%S")
        age_hours = (datetime.now() - audit_time).total_seconds() / 3600
        
        if age_hours > 1:
            print(f"⚠️  Audit evidence stale ({age_hours:.1f} hours old)")
            return 1
        
        foreign = data.get("foreign_paths", {})
        task_ids = data.get("task_ids", {})
        broadcast = data.get("broadcast_sent", False)
        
        if foreign:
            missing = [k for k in foreign.keys() if k not in task_ids]
            if missing:
                print(f"❌ Missing task IDs for: {', '.join(missing)}")
                return 1
            if not broadcast:
                print("❌ Broadcast not sent")
                return 1
        
        print(f"✅ Audit evidence valid: {latest.name} ({age_hours:.1f}h old)")
        return 0
    except Exception as e:
        print(f"❌ Error reading audit evidence: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(check_latest_audit_evidence())

