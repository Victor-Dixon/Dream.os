#!/usr/bin/env python3
"""
Quick status checker for Agent-1's SSOT tagging batch assignments.

Usage:
    python tools/check_agent1_ssot_batch_status.py
"""

import json
import os
from pathlib import Path

def check_agent1_batch_status():
    """Check Agent-1's SSOT batch assignment status."""
    repo_root = Path(__file__).parent.parent
    assignments_file = repo_root / "ssot_batch_assignments_latest.json"
    
    if not assignments_file.exists():
        print(f"❌ Assignment file not found: {assignments_file}")
        return
    
    with open(assignments_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    agent1_batches = []
    total_files = 0
    
    for priority_level in ['priority_1', 'priority_2', 'priority_3']:
        if priority_level not in data.get('batches', {}):
            continue
        
        for batch in data['batches'][priority_level]:
            if batch.get('secondary_agent') == 'Agent-1' or batch.get('primary_agent') == 'Agent-1':
                agent1_batches.append(batch)
                total_files += batch.get('file_count', 0)
    
    print(f"📊 Agent-1 SSOT Batch Assignment Status")
    print(f"{'='*50}")
    print(f"Total batches: {len(agent1_batches)}")
    print(f"Total files: {total_files}")
    print(f"\nPriority breakdown:")
    
    priority_counts = {}
    for batch in agent1_batches:
        priority = batch.get('priority', 'unknown')
        priority_counts[priority] = priority_counts.get(priority, 0) + 1
    
    for priority, count in sorted(priority_counts.items()):
        print(f"  Priority {priority}: {count} batches")
    
    print(f"\nDomain breakdown:")
    domain_counts = {}
    for batch in agent1_batches:
        domain = batch.get('domain', 'unknown')
        domain_counts[domain] = domain_counts.get(domain, 0) + 1
    
    for domain, count in sorted(domain_counts.items()):
        print(f"  {domain}: {count} batches")

if __name__ == '__main__':
    check_agent1_ssot_batch_status()

