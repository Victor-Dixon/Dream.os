#!/usr/bin/env python3
"""
Markdown File Analysis for Cleanup Strategy Development
======================================================

Analyzes 7000+ markdown files to develop cleanup strategy for:
- Categorization
- Deduplication
- Archive organization

Author: Agent-5 (Business Intelligence)
Date: 2026-01-11
"""

import os
from pathlib import Path
from collections import defaultdict
import hashlib

def analyze_markdown_files():
    """Analyze markdown files for cleanup strategy development."""
    repo_root = Path('.')
    md_files = []

    # Get all markdown files
    for root, dirs, files in os.walk(repo_root):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__', 'node_modules', '.git']]
        for file in files:
            if file.endswith('.md'):
                md_files.append(os.path.join(root, file))

    print(f'Analyzing {len(md_files)} markdown files for patterns and duplication...')

    # Analyze file sizes and patterns
    sizes = []
    file_types = defaultdict(int)
    first_lines = defaultdict(int)
    content_hashes = defaultdict(list)

    for md_file in md_files:
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
                sizes.append(len(content))

                # Calculate content hash for duplication detection
                content_hash = hashlib.md5(content.encode('utf-8')).hexdigest()
                content_hashes[content_hash].append(md_file)

                lines = content.split('\n')
                if lines:
                    first_line = lines[0].strip()
                    # Categorize by first line pattern
                    if first_line.startswith('# '):
                        file_types['heading_h1'] += 1
                    elif first_line.startswith('## '):
                        file_types['heading_h2'] += 1
                    elif first_line.startswith('### '):
                        file_types['heading_h3'] += 1
                    elif first_line.startswith('- '):
                        file_types['bullet_list'] += 1
                    elif first_line.startswith('|'):
                        file_types['table'] += 1
                    elif not first_line:
                        file_types['empty_first_line'] += 1
                    else:
                        file_types['other'] += 1

                    # Track common first line patterns (top 15)
                    if len([k for k in first_lines.keys() if k]) < 15 or first_line in first_lines:
                        first_lines[first_line] += 1

        except Exception as e:
            print(f'Error reading {md_file}: {e}')

    print(f'\nFile size analysis:')
    print(f'  Total content size: {sum(sizes):,} characters')
    print(f'  Average file size: {sum(sizes)//len(sizes):,} characters')
    print(f'  Largest file: {max(sizes):,} characters')
    print(f'  Smallest file: {min(sizes)} characters')

    print(f'\nFile type patterns:')
    for file_type, count in sorted(file_types.items(), key=lambda x: x[1], reverse=True):
        print(f'  {file_type}: {count} files')

    print(f'\nMost common first lines:')
    for line, count in sorted(first_lines.items(), key=lambda x: x[1], reverse=True)[:15]:
        if line:
            print(f'  "{line}": {count} files')
        else:
            print(f'  (empty): {count} files')

    # Analyze duplication
    duplicates = {k: v for k, v in content_hashes.items() if len(v) > 1}
    duplicate_files = sum(len(files) for files in duplicates.values())

    print(f'\nDuplication analysis:')
    print(f'  Unique content hashes: {len(content_hashes)}')
    print(f'  Duplicate groups: {len(duplicates)}')
    print(f'  Total duplicate files: {duplicate_files}')
    print(f'  Potential space savings: {duplicate_files - len(duplicates)} files')

    if duplicates:
        print(f'\nLargest duplicate groups:')
        for i, (hash_key, files) in enumerate(sorted(duplicates.items(), key=lambda x: len(x[1]), reverse=True)[:5]):
            print(f'  Group {i+1}: {len(files)} files')
            for j, file_path in enumerate(files[:3]):  # Show first 3 files
                print(f'    {file_path}')
            if len(files) > 3:
                print(f'    ... and {len(files) - 3} more')

    return {
        'total_files': len(md_files),
        'total_size': sum(sizes),
        'avg_size': sum(sizes)//len(sizes),
        'file_types': dict(file_types),
        'duplicates': len(duplicates),
        'duplicate_files': duplicate_files
    }

if __name__ == "__main__":
    analyze_markdown_files()