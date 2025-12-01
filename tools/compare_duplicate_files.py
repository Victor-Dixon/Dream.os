#!/usr/bin/env python3
"""
Duplicate File Content Comparison Tool
Compares file contents to identify truly identical duplicates
"""

import filecmp
import hashlib
from pathlib import Path
from typing import List, Tuple, Dict


def calculate_file_hash(file_path: Path) -> str:
    """Calculate SHA256 hash of file content."""
    with open(file_path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()


def compare_files(file1: Path, file2: Path) -> Dict:
    """Compare two files and return comparison results."""
    result = {
        'file1': str(file1),
        'file2': str(file2),
        'both_exist': file1.exists() and file2.exists(),
        'identical': False,
        'same_size': False,
        'same_hash': False,
        'filecmp_match': False,
    }
    
    if not result['both_exist']:
        return result
    
    # Size comparison
    result['same_size'] = file1.stat().st_size == file2.stat().st_size
    
    if result['same_size']:
        # Hash comparison
        hash1 = calculate_file_hash(file1)
        hash2 = calculate_file_hash(file2)
        result['same_hash'] = hash1 == hash2
        
        # Filecmp comparison (byte-by-byte)
        result['filecmp_match'] = filecmp.cmp(str(file1), str(file2), shallow=False)
        result['identical'] = result['filecmp_match']
    
    return result


def compare_duplicate_groups(duplicate_groups: List[List[str]]) -> List[Dict]:
    """Compare files within duplicate groups."""
    results = []
    
    for group in duplicate_groups:
        if len(group) < 2:
            continue
        
        # Compare all pairs in the group
        for i in range(len(group)):
            for j in range(i + 1, len(group)):
                file1 = Path(group[i])
                file2 = Path(group[j])
                
                comparison = compare_files(file1, file2)
                results.append(comparison)
    
    return results


if __name__ == '__main__':
    # Example duplicate groups from the investigation
    duplicate_groups = [
        # Models files
        [
            'src/core/intelligent_context/unified_intelligent_context/models.py',
            'src/core/performance/unified_dashboard/models.py',
            'src/core/ssot/unified_ssot/models.py',
            'src/core/vector_strategic_oversight/unified_strategic_oversight/models.py',
        ],
        # Core files
        [
            'src/core/error_handling/circuit_breaker/core.py',
            'src/discord_commander/core.py',
            'src/gaming/integration/core.py',
        ],
        # Config files
        [
            'src/ai_training/dreamvault/config.py',
            'src/infrastructure/browser/unified/config.py',
            'src/services/config.py',
            'src/shared_utils/config.py',
        ],
        # Other specific duplicates
        [
            'src/core/constants/fsm_models.py',
            'src/gaming/dreamos/fsm_models.py',
        ],
        [
            'src/core/messaging_protocol_models.py',
            'src/services/protocol/messaging_protocol_models.py',
        ],
    ]
    
    print("🔍 Comparing duplicate files...\n")
    results = compare_duplicate_groups(duplicate_groups)
    
    identical_count = sum(1 for r in results if r['identical'])
    total_count = len(results)
    
    print(f"📊 Comparison Results:")
    print(f"   Total comparisons: {total_count}")
    print(f"   Identical files: {identical_count}")
    print(f"   Different files: {total_count - identical_count}\n")
    
    print("✅ Identical Files (Safe to delete one):")
    for r in results:
        if r['identical']:
            print(f"   {r['file1']}")
            print(f"   {r['file2']}")
            print()
    
    print("⚠️ Different Files (Need merge or keep both):")
    for r in results:
        if not r['identical'] and r['both_exist']:
            print(f"   {r['file1']} vs {r['file2']}")
            print(f"   Same size: {r['same_size']}, Same hash: {r['same_hash']}")
            print()

