#!/usr/bin/env python3
"""Extract duplicate file information from analysis JSON."""

import json
from pathlib import Path

analysis_file = Path("agent_workspaces/Agent-5/unnecessary_files_analysis.json")

with open(analysis_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Extract duplicates
duplicates = data.get('duplicates', [])
deletion_markers = data.get('deletion_markers', [])
deprecated = data.get('deprecated', [])

print(f"=== DUPLICATES ({len(duplicates)}) ===")
for d in duplicates:
    file_path = d.get('file_path', d.get('file', 'N/A'))
    dup_of = d.get('duplicate_of', d.get('original', 'N/A'))
    print(f"{file_path} -> {dup_of}")

print(f"\n=== DELETION MARKERS ({len(deletion_markers)}) ===")
for d in deletion_markers:
    file_path = d.get('file_path', d.get('file', 'N/A'))
    print(f"{file_path}")

print(f"\n=== DEPRECATED ({len(deprecated)}) ===")
for d in deprecated:
    file_path = d.get('file_path', d.get('file', 'N/A'))
    print(f"{file_path}")

# Check config/ssot.py in unused files
unused = data.get('unused', [])
ssot_files = [f for f in unused if 'ssot.py' in f.get('file_path', '')]
print(f"\n=== SSOT FILES IN UNUSED ({len(ssot_files)}) ===")
for s in ssot_files:
    print(f"{s.get('file_path', 'N/A')}")

