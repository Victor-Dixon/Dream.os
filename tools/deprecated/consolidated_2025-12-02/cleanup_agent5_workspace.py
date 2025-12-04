#!/usr/bin/env python3
"""
Agent-5 Workspace Cleanup Tool
==============================

Cleans up old/duplicate files from Agent-5 workspace, archives completed documents.
"""

import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import List

WORKSPACE_DIR = Path("agent_workspaces/Agent-5")
ARCHIVE_DIR = WORKSPACE_DIR / "archive"
KEEP_FILES = [
    "status.json",
    "technical_debt_markers_analysis.json",
    "22_duplicate_files_list.json",
    "unnecessary_files_analysis.json",
    "assignments_log.json",
    "loop_closure_report.json",
    "pattern_optimization.json",
    "production_monitoring_report.json",
    "CAPTAIN_SWARM_REPORT.json",
]

# Files to keep (recent/completed work)
IMPORTANT_FILES = [
    "TECHNICAL_DEBT_MONITORING_WORKFLOW_COMPLETE.md",
    "TECHNICAL_DEBT_TASKS_STATUS_REPORT.md",
    "CAPTAIN_LOOP_CLOSURE_ACTION_PLAN.md",
    "CAPTAIN_TASK_ASSIGNMENTS_COMPLETE.md",
    "FILE_DELETION_FINAL_SUMMARY.md",
    "AGENT1_TECHNICAL_DEBT_COORDINATION.md",
    "METRICS_EXPORTER_INTEGRATION_SUMMARY.md",
]

def archive_old_files():
    """Archive old coordination and summary files."""
    ARCHIVE_DIR.mkdir(exist_ok=True)
    
    files_to_archive = []
    
    for file in WORKSPACE_DIR.glob("*.md"):
        if file.name in KEEP_FILES + IMPORTANT_FILES:
            continue
        
        # Archive old captain/coordination documents
        if any(keyword in file.name for keyword in [
            "CAPTAIN_", "COORDINATION", "ACKNOWLEDGMENT", 
            "RESPONSE", "SUMMARY", "COMPLETE"
        ]):
            files_to_archive.append(file)
    
    archived = []
    for file in files_to_archive:
        archive_path = ARCHIVE_DIR / file.name
        if not archive_path.exists():
            shutil.move(str(file), str(archive_path))
            archived.append(file.name)
    
    return archived

if __name__ == "__main__":
    print("🧹 Cleaning Agent-5 workspace...")
    archived = archive_old_files()
    print(f"✅ Archived {len(archived)} files")
    for f in archived:
        print(f"  - {f}")


