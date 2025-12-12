#!/usr/bin/env python3
"""Identify old and redundant files for easy deletion."""
from pathlib import Path
from datetime import datetime

# Old devlogs (2025-01-27 is way old)
old_devlogs = list(Path("devlogs").glob("2025-01-27_*.md"))

# Redundant artifacts
redundant_artifacts = [
    # Agent-5 duplicate/redundant reports
    "artifacts/2025-12-12_agent-5_audit-quick-reference.md",
    "artifacts/2025-12-12_agent-5_audit-quick-reference-guide.md",  # duplicate
    "artifacts/2025-12-12_agent-5_complete-delta-report.md",  # redundant
    "artifacts/2025-12-12_agent-5_final-handoff-document.md",  # redundant
    "artifacts/2025-12-12_agent-5_final-session-summary.md",  # redundant
    "artifacts/2025-12-12_agent-5_session-metrics-summary.md",  # redundant
    "artifacts/2025-12-12_agent-5_session-artifact-index.md",  # redundant
    
    # Agent-7 redundant validation files
    "artifacts/2025-12-12_agent-7_ci_cd_validation.json",
    "artifacts/2025-12-12_agent-7_validation_record.txt",
    "artifacts/AGENT7_CI_CD_WORK_COMPLETE_2025-12-12.txt",
    "artifacts/AGENT7_CODE_COMMENT_REVIEW_VALIDATION_2025-12-12.txt",
    "artifacts/AGENT7_COMMENT_CODE_ANALYZER_VALIDATION_2025-12-12.txt",
    "artifacts/DELETION_CANDIDATES_AGENT7_CI_CD.txt",
    "artifacts/REDUNDANT_DOCS_ANALYSIS_2025-12-12.md",
    "artifacts/VALIDATION_RESULT_2025-12-12.json",
]

# Tools redundant reports
redundant_tools = [
    "tools/COORDINATION_RESULTS_REPORT.md",  # redundant with validation report
    "tools/COORDINATION_FINAL_VALIDATION_REPORT.md",  # redundant
    "tools/COORDINATION_EFFECTIVENESS_ANALYSIS.md",  # redundant
    "tools/COORDINATION_METRICS_SNAPSHOT.md",  # redundant
    "tools/COORDINATION_TOOLS_SUMMARY.md",  # redundant
    "tools/COORDINATION_TOOLS_VALIDATION_REPORT.md",  # redundant
    "tools/COORDINATION_INFRASTRUCTURE_SUMMARY.md",  # redundant
    "tools/COORDINATION_ACTIVITY_LOG.md",  # redundant
]

all_files_to_delete = []
for f in old_devlogs:
    if f.exists():
        all_files_to_delete.append(f)

for f_path in redundant_artifacts + redundant_tools:
    f = Path(f_path)
    if f.exists():
        all_files_to_delete.append(f)

print(f"Found {len(all_files_to_delete)} files to delete:\n")
total_size = 0
for f in all_files_to_delete:
    size = f.stat().st_size
    total_size += size
    print(f"  {f} ({size:,} bytes)")

print(f"\nTotal: {len(all_files_to_delete)} files, {total_size:,} bytes ({total_size/1024:.1f} KB)")

