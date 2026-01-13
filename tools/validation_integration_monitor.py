#!/usr/bin/env python3
"""
Validation Integration Monitor

Real-time monitoring tool for validation integration pipeline execution.
Tracks pipeline status, logs integration events, and alerts on failures.

Protocol: CYCLE_ACCOMPLISHMENTS_REPORT_GENERATION v2.0
Author: Agent-8 (SSOT & System Integration Specialist)
Date: 2025-12-31
V2 Compliant: Yes

Usage:
    python tools/validation_integration_monitor.py [--watch] [--log-file PATH]

<!-- SSOT Domain: tools -->
"""

import json
import sys
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional

# Paths
REPO_ROOT = Path(__file__).parent.parent
VALIDATION_REPORT_JSON = REPO_ROOT / "docs" / "SSOT" / "FINAL_PHASE3_VALIDATION_REPORT.json"
MILESTONE_OUTPUT = REPO_ROOT / "docs" / "SSOT" / "PHASE1_THROUGH_PHASE3_COMPLETION_MILESTONE.md"
MASTER_TASK_LOG = REPO_ROOT / "MASTER_TASK_LOG.md"
SIGNAL_HANDLER = REPO_ROOT / "tools" / "validation_completion_signal_handler.py"
INTEGRATION_PIPELINE = REPO_ROOT / "tools" / "validation_result_integration_pipeline.py"


def check_validation_report() -> tuple[bool, str]:
    """Check if validation report exists and is valid."""
    if not VALIDATION_REPORT_JSON.exists():
        return False, "Validation report not found"
    
    try:
        with open(VALIDATION_REPORT_JSON, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if 'total_files' not in data or 'valid_files' not in data:
            return False, "Validation report incomplete"
        
        invalid = data.get('invalid_files', 0)
        total = data.get('total_files', 0)
        valid = data.get('valid_files', 0)
        
        if invalid == 0:
            return True, f"Validation complete: {valid}/{total} files valid (100% success)"
        else:
            return False, f"Validation incomplete: {invalid} invalid files remaining"
    except Exception as e:
        return False, f"Error reading validation report: {e}"


def check_milestone() -> tuple[bool, str]:
    """Check if milestone document was generated."""
    if not MILESTONE_OUTPUT.exists():
        return False, "Milestone document not generated"
    
    content = MILESTONE_OUTPUT.read_text(encoding='utf-8')
    if '[TO BE POPULATED]' in content:
        return False, "Milestone document exists but not populated"
    
    return True, "Milestone document generated and populated"


def check_task_log() -> tuple[bool, str]:
    """Check if MASTER_TASK_LOG was updated."""
    if not MASTER_TASK_LOG.exists():
        return False, "MASTER_TASK_LOG not found"
    
    content = MASTER_TASK_LOG.read_text(encoding='utf-8')
    
    phase3_markers = [
        'SSOT Phase 3 - COMPLETE',
        'Phase 3 - COMPLETE',
        'Phase 3 completion',
        '100% SSOT compliance'
    ]
    
    for marker in phase3_markers:
        if marker in content:
            return True, f"MASTER_TASK_LOG updated (found: {marker})"
    
    return False, "MASTER_TASK_LOG not updated with Phase 3 completion"


def check_integration_tools() -> tuple[bool, str]:
    """Check if integration tools exist."""
    tools_status = []
    
    if SIGNAL_HANDLER.exists():
        tools_status.append("✅ Signal handler")
    else:
        tools_status.append("❌ Signal handler missing")
    
    if INTEGRATION_PIPELINE.exists():
        tools_status.append("✅ Integration pipeline")
    else:
        tools_status.append("❌ Integration pipeline missing")
    
    all_exist = SIGNAL_HANDLER.exists() and INTEGRATION_PIPELINE.exists()
    status_msg = ", ".join(tools_status)
    
    return all_exist, status_msg


def log_event(event_type: str, message: str, log_file: Optional[Path] = None):
    """Log integration event."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{timestamp}] {event_type}: {message}\n"
    
    print(log_entry.strip())
    
    if log_file:
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry)


def monitor_integration(watch: bool = False, log_file: Optional[Path] = None):
    """Monitor integration pipeline status."""
    print("🔍 Validation Integration Monitor")
    print("=" * 60)
    print()
    
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        log_event("MONITOR_START", f"Monitoring started, log file: {log_file}", log_file)
    
    iteration = 0
    
    while True:
        iteration += 1
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        print(f"\n📊 Status Check #{iteration} - {timestamp}")
        print("-" * 60)
        
        # Check validation report
        report_valid, report_msg = check_validation_report()
        status_icon = "✅" if report_valid else "❌"
        print(f"1️⃣  Validation Report: {status_icon} {report_msg}")
        if log_file:
            log_event("VALIDATION_REPORT", report_msg, log_file)
        
        # Check milestone
        milestone_valid, milestone_msg = check_milestone()
        status_icon = "✅" if milestone_valid else "❌"
        print(f"2️⃣  Milestone Document: {status_icon} {milestone_msg}")
        if log_file:
            log_event("MILESTONE", milestone_msg, log_file)
        
        # Check task log
        task_log_valid, task_log_msg = check_task_log()
        status_icon = "✅" if task_log_valid else "❌"
        print(f"3️⃣  MASTER_TASK_LOG: {status_icon} {task_log_msg}")
        if log_file:
            log_event("TASK_LOG", task_log_msg, log_file)
        
        # Check integration tools
        tools_valid, tools_msg = check_integration_tools()
        status_icon = "✅" if tools_valid else "❌"
        print(f"4️⃣  Integration Tools: {status_icon} {tools_msg}")
        if log_file:
            log_event("INTEGRATION_TOOLS", tools_msg, log_file)
        
        # Overall status
        all_complete = report_valid and milestone_valid and task_log_valid
        
        print("\n" + "=" * 60)
        if all_complete:
            print("✅ Integration Pipeline: COMPLETE")
            print("\n🎯 All integration steps completed successfully!")
            if log_file:
                log_event("INTEGRATION_COMPLETE", "All checks passed", log_file)
            
            if not watch:
                break
        else:
            print("🟡 Integration Pipeline: IN PROGRESS or INCOMPLETE")
            if log_file:
                log_event("INTEGRATION_IN_PROGRESS", "Waiting for completion", log_file)
        
        if not watch:
            break
        
        # Wait before next check
        print("\n⏳ Waiting 30 seconds before next check...")
        time.sleep(30)


def main():
    """Main execution function."""
    watch_mode = '--watch' in sys.argv
    log_file = None
    
    if '--log-file' in sys.argv:
        idx = sys.argv.index('--log-file')
        if idx + 1 < len(sys.argv):
            log_file = Path(sys.argv[idx + 1])
    
    try:
        monitor_integration(watch=watch_mode, log_file=log_file)
    except KeyboardInterrupt:
        print("\n\n⚠️  Monitoring stopped by user")
        if log_file:
            log_event("MONITOR_STOPPED", "User interrupted", log_file)
        sys.exit(0)


if __name__ == '__main__':
    main()

