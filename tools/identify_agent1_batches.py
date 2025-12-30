#!/usr/bin/env python3
"""Identify incomplete SSOT batches assigned to Agent-1."""

import json
from pathlib import Path

def main():
    assignments_file = Path("reports/ssot/ssot_batch_assignments_latest.json")
    
    with open(assignments_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    incomplete_batches = []
    total_files = 0
    
    # Check all priority levels
    for priority_level, batches in data.get('batches', {}).items():
        for batch in batches:
            if not isinstance(batch, dict):
                continue
                
            # Check if Agent-1 is assigned (primary or secondary)
            assigned_to_agent1 = (
                batch.get('primary_agent') == 'Agent-1' or 
                batch.get('secondary_agent') == 'Agent-1'
            )
            
            # Check if incomplete
            is_complete = batch.get('status') == 'complete'
            
            if assigned_to_agent1 and not is_complete:
                batch_info = {
                    'batch_id': batch.get('batch_id'),
                    'domain': batch.get('domain'),
                    'priority': batch.get('priority'),
                    'file_count': batch.get('file_count', 0),
                    'files': batch.get('files', [])
                }
                incomplete_batches.append(batch_info)
                total_files += batch_info['file_count']
    
    print(f"Agent-1 Incomplete Batches: {len(incomplete_batches)}")
    print(f"Total Files: {total_files}")
    print("\nBatch Details:")
    for batch in incomplete_batches:
        print(f"  {batch['batch_id']}: {batch['file_count']} files ({batch['domain']} domain, Priority {batch['priority']})")
    
    # Find batches that total ~81 files
    if total_files > 0:
        print(f"\n✅ Found {len(incomplete_batches)} incomplete batches with {total_files} total files")
        if total_files == 81:
            print("✅ This matches the 81 files assignment!")
        elif total_files > 81:
            print(f"⚠️  Total files ({total_files}) exceeds 81. May need to select specific batches.")
        else:
            print(f"⚠️  Total files ({total_files}) is less than 81. May need additional batches.")

if __name__ == "__main__":
    main()



