#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path

src_dir = Path('src')
syntax_errors = []

for py_file in src_dir.rglob('*.py'):
    try:
        result = subprocess.run([sys.executable, '-m', 'py_compile', str(py_file)],
                              capture_output=True, text=True, timeout=10)
        if result.returncode != 0:
            syntax_errors.append({
                'file': str(py_file),
                'error': result.stderr.strip()
            })
    except Exception as e:
        syntax_errors.append({
            'file': str(py_file),
            'error': str(e)
        })

print(f'Found {len(syntax_errors)} Python syntax errors:')
for error in syntax_errors[:10]:  # Show first 10
    print(f'  {error["file"]}: {error["error"][:100]}...')