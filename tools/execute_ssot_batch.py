#!/usr/bin/env python3
"""
Execute SSOT Batch Tagging
===========================

Automates SSOT domain tag addition for batch assignments.
Processes batches from ssot_batch_assignments_latest.json.

V2 Compliant: <300 lines
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2025-12-29
"""

import json
import sys
from pathlib import Path
from typing import List, Dict, Any

# SSOT tag format: <!-- SSOT Domain: domain_name -->
SSOT_TAG_FORMAT = "<!-- SSOT Domain: {domain} -->"


def load_batch_assignments(json_file: str = "ssot_batch_assignments_latest.json") -> Dict[str, Any]:
    """Load batch assignments from JSON file."""
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Batch assignments file not found: {json_file}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in {json_file}: {e}")
        sys.exit(1)


def file_has_ssot_tag(file_path: Path, domain: str) -> bool:
    """Check if file already has SSOT tag for the domain."""
    try:
        content = file_path.read_text(encoding='utf-8')
        tag = SSOT_TAG_FORMAT.format(domain=domain)
        # Check for both HTML comment format and Python comment format
        return tag in content or f"# {tag}" in content
    except Exception:
        return False


def add_ssot_tag_to_file(file_path: Path, domain: str) -> bool:
    """
    Add SSOT domain tag to file.
    Places tag at the top of the file, after shebang if present.
    For Python files, uses # comment format.
    """
    try:
        content = file_path.read_text(encoding='utf-8')
        
        # Check if tag already exists
        if file_has_ssot_tag(file_path, domain):
            return True  # Already tagged
        
        tag = SSOT_TAG_FORMAT.format(domain=domain)
        lines = content.splitlines(keepends=True)
        
        # For Python files, use # comment format
        is_python = file_path.suffix == '.py'
        if is_python:
            tag_line = f"# {tag}\n"
        else:
            tag_line = f"{tag}\n"
        
        # Find insertion point (after shebang and encoding, before docstring)
        insert_index = 0
        
        # Skip shebang
        if lines and lines[0].startswith('#!'):
            insert_index = 1
        
        # Skip encoding declaration
        if insert_index < len(lines) and ('coding:' in lines[insert_index] or 'encoding:' in lines[insert_index]):
            insert_index += 1
        
        # Skip blank lines at top
        while insert_index < len(lines) and lines[insert_index].strip() == '':
            insert_index += 1
        
        # For Python files, check if next line is a docstring - insert before it
        if is_python and insert_index < len(lines):
            # Check if next non-blank line is a docstring
            next_line_idx = insert_index
            while next_line_idx < len(lines) and lines[next_line_idx].strip() == '':
                next_line_idx += 1
            if next_line_idx < len(lines) and (lines[next_line_idx].strip().startswith('"""') or lines[next_line_idx].strip().startswith("'''")):
                insert_index = next_line_idx
        
        # Insert tag
        if insert_index == 0:
            lines.insert(0, tag_line)
        else:
            lines.insert(insert_index, tag_line)
        
        # Write back
        file_path.write_text(''.join(lines), encoding='utf-8')
        return True
        
    except Exception as e:
        print(f"  ❌ Error tagging {file_path}: {e}")
        return False


def process_batch(batch: Dict[str, Any], dry_run: bool = False) -> Dict[str, Any]:
    """Process a single batch of files."""
    batch_id = batch['batch_id']
    domain = batch['domain']
    files = batch['files']
    
    print(f"\n🎯 Processing {batch_id} ({domain} domain, {len(files)} files)...")
    
    results = {
        'batch_id': batch_id,
        'domain': domain,
        'total_files': len(files),
        'tagged': 0,
        'already_tagged': 0,
        'failed': 0,
        'files': []
    }
    
    for file_path_str in files:
        # Convert Windows path separators
        file_path = Path(file_path_str.replace('\\', '/'))
        
        if not file_path.exists():
            print(f"  ⚠️  File not found: {file_path}")
            results['failed'] += 1
            results['files'].append({
                'path': str(file_path),
                'status': 'not_found'
            })
            continue
        
        # Check if already tagged
        if file_has_ssot_tag(file_path, domain):
            print(f"  ✅ Already tagged: {file_path.name}")
            results['already_tagged'] += 1
            results['files'].append({
                'path': str(file_path),
                'status': 'already_tagged'
            })
            continue
        
        if dry_run:
            print(f"  🔍 Would tag: {file_path.name}")
            results['tagged'] += 1
            results['files'].append({
                'path': str(file_path),
                'status': 'would_tag'
            })
        else:
            if add_ssot_tag_to_file(file_path, domain):
                print(f"  ✅ Tagged: {file_path.name}")
                results['tagged'] += 1
                results['files'].append({
                    'path': str(file_path),
                    'status': 'tagged'
                })
            else:
                print(f"  ❌ Failed: {file_path.name}")
                results['failed'] += 1
                results['files'].append({
                    'path': str(file_path),
                    'status': 'failed'
                })
    
    return results


def main():
    """Main execution function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Execute SSOT batch tagging")
    parser.add_argument('--batch-id', help='Specific batch ID to process')
    parser.add_argument('--priority', type=int, help='Process all batches of this priority')
    parser.add_argument('--domain', help='Process all batches for this domain')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be tagged without making changes')
    parser.add_argument('--json-file', default='ssot_batch_assignments_latest.json', help='Batch assignments JSON file')
    
    args = parser.parse_args()
    
    assignments = load_batch_assignments(args.json_file)
    batches = assignments.get('batches', {})
    
    # Get priority 1 batches
    priority_1_batches = batches.get('priority_1', [])
    
    if args.batch_id:
        # Process specific batch
        batch = next((b for b in priority_1_batches if b['batch_id'] == args.batch_id), None)
        if not batch:
            print(f"❌ Batch not found: {args.batch_id}")
            sys.exit(1)
        results = process_batch(batch, dry_run=args.dry_run)
        print(f"\n📊 Results: {results['tagged']} tagged, {results['already_tagged']} already tagged, {results['failed']} failed")
    elif args.priority:
        # Process all batches of this priority
        batches_to_process = [b for b in priority_1_batches if b.get('priority') == args.priority]
        print(f"🎯 Processing {len(batches_to_process)} batches with priority {args.priority}...")
        for batch in batches_to_process:
            process_batch(batch, dry_run=args.dry_run)
    elif args.domain:
        # Process all batches for this domain
        batches_to_process = [b for b in priority_1_batches if b.get('domain') == args.domain]
        print(f"🎯 Processing {len(batches_to_process)} batches for domain '{args.domain}'...")
        for batch in batches_to_process:
            process_batch(batch, dry_run=args.dry_run)
    else:
        # Process first Priority 1 batch as example
        if priority_1_batches:
            print("🎯 Processing first Priority 1 batch (use --batch-id, --priority, or --domain for more)...")
            batch = priority_1_batches[0]
            results = process_batch(batch, dry_run=args.dry_run)
            print(f"\n📊 Results: {results['tagged']} tagged, {results['already_tagged']} already tagged, {results['failed']} failed")
        else:
            print("❌ No Priority 1 batches found")
            sys.exit(1)


if __name__ == "__main__":
    main()

