#!/usr/bin/env python3
"""
Extract Priority 2/3 invalid file lists from Phase 2 validation JSON for domain owner coordination.
"""
import json
import sys
from pathlib import Path
from collections import defaultdict

def extract_priority_files(json_path: str):
    """Extract Priority 2 (compilation errors) and Priority 3 (tag placement) file lists."""
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    validation_results = data.get('validation_results', [])
    
    # Priority 2: Compilation errors (Python files with compilation failures)
    priority2_files = []
    # Priority 3: Tag placement issues (tags outside first 50 lines)
    priority3_files = []
    
    for result in validation_results:
        if result.get('valid', True):
            continue  # Skip valid files
        
        file_path = result.get('file', '')
        domain = result.get('domain', 'unknown')
        compilation_result = result.get('compilation', [True, ''])
        tag_placement_result = result.get('tag_placement', [True, ''])
        
        # Priority 2: Compilation errors
        if not compilation_result[0] and file_path.endswith('.py'):
            priority2_files.append({
                'file_path': file_path,
                'domain': domain,
                'error': compilation_result[1] if len(compilation_result) > 1 else 'Compilation error'
            })
        
        # Priority 3: Tag placement issues
        if not tag_placement_result[0]:
            priority3_files.append({
                'file_path': file_path,
                'domain': domain,
                'error': tag_placement_result[1] if len(tag_placement_result) > 1 else 'Tag placement issue'
            })
    
    # Group by domain
    priority2_by_domain = defaultdict(list)
    priority3_by_domain = defaultdict(list)
    
    for file_info in priority2_files:
        priority2_by_domain[file_info['domain']].append(file_info)
    
    for file_info in priority3_files:
        priority3_by_domain[file_info['domain']].append(file_info)
    
    return priority2_files, priority3_files, priority2_by_domain, priority3_by_domain

def print_summary(priority2_files, priority3_files, priority2_by_domain, priority3_by_domain):
    """Print summary of extracted files."""
    print("=" * 80)
    print("PHASE 3 REMEDIATION FILE EXTRACTION SUMMARY")
    print("=" * 80)
    print()
    
    print(f"Priority 2 (Compilation Errors): {len(priority2_files)} files")
    print("-" * 80)
    for domain, files in sorted(priority2_by_domain.items()):
        print(f"  {domain}: {len(files)} files")
        for file_info in files[:3]:  # Show first 3 per domain
            rel_path = Path(file_info['file_path']).relative_to(Path.cwd()) if Path(file_info['file_path']).exists() else file_info['file_path']
            print(f"    - {rel_path}")
        if len(files) > 3:
            print(f"    ... and {len(files) - 3} more")
    print()
    
    print(f"Priority 3 (Tag Placement Issues): {len(priority3_files)} files")
    print("-" * 80)
    for domain, files in sorted(priority3_by_domain.items()):
        print(f"  {domain}: {len(files)} files")
        for file_info in files[:3]:  # Show first 3 per domain
            rel_path = Path(file_info['file_path']).relative_to(Path.cwd()) if Path(file_info['file_path']).exists() else file_info['file_path']
            print(f"    - {rel_path}")
        if len(files) > 3:
            print(f"    ... and {len(files) - 3} more")
    print()

if __name__ == '__main__':
    json_path = 'docs/SSOT/FINAL_VALIDATION_CHECKPOINT_20251230_175053.json'
    
    if not Path(json_path).exists():
        print(f"Error: JSON file not found: {json_path}")
        sys.exit(1)
    
    priority2_files, priority3_files, priority2_by_domain, priority3_by_domain = extract_priority_files(json_path)
    
    print_summary(priority2_files, priority3_files, priority2_by_domain, priority3_by_domain)
    
    # Export to JSON for further processing
    output = {
        'priority2_compilation_errors': {
            'total': len(priority2_files),
            'by_domain': {domain: len(files) for domain, files in priority2_by_domain.items()},
            'files': priority2_files
        },
        'priority3_tag_placement': {
            'total': len(priority3_files),
            'by_domain': {domain: len(files) for domain, files in priority3_by_domain.items()},
            'files': priority3_files
        }
    }
    
    output_path = 'docs/SSOT/PHASE3_PRIORITY23_FILE_LISTS.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2)
    
    print(f"✅ File lists exported to: {output_path}")

