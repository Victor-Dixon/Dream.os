#!/usr/bin/env python3
import os
import re
from pathlib import Path

# Check for dead code patterns
dead_patterns = [
    r'def \w+\([^)]*\):?\s*\n\s*pass\s*$',  # Empty function definitions
    r'# TODO.*REMOVE|# FIXME.*REMOVE|# DEPRECATED',  # Marked for removal
    r'^\s*#\s*Dead code|^\s*#\s*Unused',  # Explicitly marked dead
]

src_dir = Path('src')
total_files = 0
findings = []

for py_file in src_dir.rglob('*.py'):
    total_files += 1
    try:
        with open(py_file, 'r', encoding='utf-8') as f:
            content = f.read()

        for pattern in dead_patterns:
            matches = re.findall(pattern, content, re.MULTILINE)
            if matches:
                findings.append({
                    'file': str(py_file),
                    'pattern': pattern,
                    'matches': len(matches)
                })
    except Exception as e:
        findings.append({
            'file': str(py_file),
            'pattern': 'READ_ERROR',
            'error': str(e)
        })

print(f'Checked {total_files} Python files')
print(f'Found {len(findings)} potential dead code issues:')
for finding in findings[:10]:  # Show first 10
    if 'error' not in finding:
        print(f'  {finding["file"]}: {finding["matches"]} matches')
    else:
        print(f'  {finding["file"]}: ERROR - {finding["error"]}')