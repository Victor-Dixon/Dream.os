#!/usr/bin/env python3
"""
Extract batches 2-8 consolidation data for Agent-8 SSOT verification.

This script extracts batch 2-8 data from DUPLICATE_GROUPS_PRIORITY_BATCHES.json
and formats it for Agent-8's SSOT validation tool.
"""

import json
import os
from pathlib import Path

def extract_batches_2_8():
    """Extract batches 2-8 from duplicate groups file."""
    # File paths
    repo_root = Path(__file__).parent.parent
    input_file = repo_root / "docs" / "technical_debt" / "DUPLICATE_GROUPS_PRIORITY_BATCHES.json"
    output_file = repo_root / "agent_workspaces" / "Agent-8" / "batches_2_8_for_ssot.json"
    
    # Ensure output directory exists
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Load batch data
    print(f"Loading batch data from: {input_file}")
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Extract batches 2-8
    batches_2_8 = []
    if 'batches' in data:
        for batch in data['batches']:
            batch_num = batch.get('batch_number', 0)
            if 2 <= batch_num <= 8:
                batches_2_8.append(batch)
                print(f"Found batch {batch_num}: {batch.get('size', 0)} groups, priority: {batch.get('priority', 'UNKNOWN')}")
    
    # Create output structure
    output_data = {
        "extraction_date": "2025-12-22T11:10:00",
        "source_file": str(input_file),
        "total_batches": len(batches_2_8),
        "batches": batches_2_8,
        "file_list": extract_file_list(batches_2_8),
        "consolidation_context": {
            "purpose": "SSOT domain validation for batches 2-8",
            "tool": "validate_ssot_domains.py",
            "coordinator": "Agent-5",
            "executor": "Agent-8"
        }
    }
    
    # Save output
    print(f"\nSaving extracted data to: {output_file}")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Extraction complete:")
    print(f"   - Batches extracted: {len(batches_2_8)}")
    print(f"   - Total groups: {sum(b.get('size', 0) for b in batches_2_8)}")
    print(f"   - Total files: {len(output_data['file_list'])}")
    print(f"   - Output file: {output_file}")
    
    return output_file

def extract_file_list(batches):
    """Extract all file paths from batches for SSOT validation."""
    file_list = []
    for batch in batches:
        batch_num = batch.get('batch_number', 0)
        for group in batch.get('groups', []):
            # Add SSOT file
            ssot = group.get('ssot', '')
            if ssot:
                file_list.append({
                    "batch": batch_num,
                    "file": ssot,
                    "type": "ssot",
                    "group_index": batch['groups'].index(group)
                })
            # Add duplicate files
            for dup in group.get('duplicates', []):
                file_list.append({
                    "batch": batch_num,
                    "file": dup,
                    "type": "duplicate",
                    "group_index": batch['groups'].index(group)
                })
    return file_list

if __name__ == "__main__":
    extract_batches_2_8()

