#!/usr/bin/env python3
"""
Categorize Review Files for Swarm Assignment
===========================================

Categorizes 306 review files by domain expertise for swarm assignment.
Uses Force Multiplier Mode to break down large task.

Author: Agent-5 (Business Intelligence Specialist)
Date: 2025-12-03
"""

import json
from collections import defaultdict
from pathlib import Path

# Load markers data
markers_file = Path("systems/technical_debt/data/markers_tracking.json")
with open(markers_file, "r", encoding="utf-8") as f:
    markers_data = json.load(f)

# Agent domain mappings
AGENT_DOMAINS = {
    "Agent-1": ["src/core/", "src/services/", "integration", "coordination", "messaging"],
    "Agent-2": ["architecture", "design", "pattern", "manager"],
    "Agent-3": ["infrastructure", "devops", "test", "validation", "deployment", "ci/cd"],
    "Agent-5": ["analytics", "metrics", "bi", "reporting", "technical_debt", "output_flywheel"],
    "Agent-6": ["communication", "coordination", "messaging", "discord"],
    "Agent-7": ["web", "frontend", "api", "discord", "ui"],
    "Agent-8": ["test", "qa", "validation", "testing"],
}

# Categorize files
file_assignments = defaultdict(list)
uncategorized = []

for marker_key, marker in markers_data.get("markers", {}).items():
    file_path = marker.get("file_path", "")
    if not file_path:
        continue
    
    # Check if file needs review (simplified - all markers need review)
    assigned = False
    file_lower = file_path.lower()
    
    for agent, domains in AGENT_DOMAINS.items():
        if any(domain.lower() in file_lower for domain in domains):
            file_assignments[agent].append({
                "file": file_path,
                "marker": marker_key,
                "type": marker.get("marker_type", "UNKNOWN"),
                "priority": marker.get("priority", "P3 - Low")
            })
            assigned = True
            break
    
    if not assigned:
        uncategorized.append(file_path)

# Generate assignment summary
summary = {
    "total_files": sum(len(files) for files in file_assignments.values()) + len(uncategorized),
    "by_agent": {agent: len(files) for agent, files in file_assignments.items()},
    "uncategorized": len(uncategorized),
    "assignments": {agent: files[:20] for agent, files in file_assignments.items()}  # Limit for display
}

# Save results
output_file = Path("agent_workspaces/Agent-5/REVIEW_FILE_ASSIGNMENTS.json")
with open(output_file, "w", encoding="utf-8") as f:
    json.dump({
        "summary": summary,
        "full_assignments": {agent: files for agent, files in file_assignments.items()},
        "uncategorized": uncategorized
    }, f, indent=2)

print(f"✅ Categorized files for swarm assignment")
print(f"   Total: {summary['total_files']} files")
for agent, count in summary['by_agent'].items():
    print(f"   {agent}: {count} files")
print(f"   Uncategorized: {summary['uncategorized']} files")
print(f"   Results saved to: {output_file}")


