#!/usr/bin/env python3
"""
Validation Integration Status Checker

Quick status check for validation integration pipeline completion.
Agent-6 can use this to verify integration pipeline has executed after validation.

Usage:
    python tools/check_validation_integration_status.py
"""

import json
from pathlib import Path
from datetime import datetime

# Paths
REPO_ROOT = Path(__file__).parent.parent
VALIDATION_REPORT_JSON = REPO_ROOT / "docs" / "SSOT" / "FINAL_PHASE3_VALIDATION_REPORT.json"
MILESTONE_OUTPUT = REPO_ROOT / "docs" / "SSOT" / "PHASE1_THROUGH_PHASE3_COMPLETION_MILESTONE.md"
MASTER_TASK_LOG = REPO_ROOT / "MASTER_TASK_LOG.md"


def check_validation_report():
    """Check if validation report exists and is valid."""
    if not VALIDATION_REPORT_JSON.exists():
        return False, "Validation report not found"
    
    try:
        with open(VALIDATION_REPORT_JSON, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if 'total_files' not in data or 'valid_files' not in data:
            return False, "Validation report incomplete"
        
        return True, f"Validation complete: {data.get('valid_files', 0)}/{data.get('total_files', 0)} files valid"
    except Exception as e:
        return False, f"Error reading validation report: {e}"


def check_milestone_generated():
    """Check if milestone document was generated."""
    if not MILESTONE_OUTPUT.exists():
        return False, "Milestone document not generated"
    
    # Check if it's populated (not just template)
    content = MILESTONE_OUTPUT.read_text(encoding='utf-8')
    if '[TO BE POPULATED]' in content:
        return False, "Milestone document exists but not populated"
    
    return True, "Milestone document generated and populated"


def check_task_log_updated():
    """Check if MASTER_TASK_LOG was updated with Phase 3 completion."""
    if not MASTER_TASK_LOG.exists():
        return False, "MASTER_TASK_LOG not found"
    
    content = MASTER_TASK_LOG.read_text(encoding='utf-8')
    
    # Look for Phase 3 completion markers
    phase3_complete_markers = [
        'SSOT Phase 3 - COMPLETE',
        'Phase 3 - COMPLETE',
        'Phase 3 completion',
        '100% SSOT compliance'
    ]
    
    for marker in phase3_complete_markers:
        if marker in content:
            return True, f"MASTER_TASK_LOG updated (found: {marker})"
    
    return False, "MASTER_TASK_LOG not updated with Phase 3 completion"


def main():
    """Main status check."""
    print("🔍 Validation Integration Status Check")
    print("=" * 60)
    print()
    
    # Check validation report
    print("1️⃣  Validation Report:")
    valid, message = check_validation_report()
    status_icon = "✅" if valid else "❌"
    print(f"   {status_icon} {message}")
    print()
    
    # Check milestone
    print("2️⃣  Milestone Document:")
    valid, message = check_milestone_generated()
    status_icon = "✅" if valid else "❌"
    print(f"   {status_icon} {message}")
    print()
    
    # Check task log
    print("3️⃣  MASTER_TASK_LOG Update:")
    valid, message = check_task_log_updated()
    status_icon = "✅" if valid else "❌"
    print(f"   {status_icon} {message}")
    print()
    
    # Overall status
    print("=" * 60)
    all_checks = [
        check_validation_report()[0],
        check_milestone_generated()[0],
        check_task_log_updated()[0]
    ]
    
    if all(all_checks):
        print("✅ Integration Pipeline: COMPLETE")
        print("\n🎯 All integration steps completed successfully!")
        print("   - Validation report generated")
        print("   - Milestone document populated")
        print("   - MASTER_TASK_LOG updated")
    else:
        print("🟡 Integration Pipeline: IN PROGRESS or INCOMPLETE")
        print("\n💡 Next Steps:")
        if not all_checks[0]:
            print("   - Run validation: python tools/execute_phase3_final_validation.py")
        if not all_checks[1] or not all_checks[2]:
            print("   - Run integration pipeline: python tools/validation_result_integration_pipeline.py")


if __name__ == '__main__':
    main()

