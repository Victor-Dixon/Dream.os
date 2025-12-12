#!/usr/bin/env python3
"""
Check for missing dependencies that might cause CI failures

<!-- SSOT Domain: infrastructure -->
"""

import ast
import os
from pathlib import Path
from typing import Set, List

# Standard library modules (don't need to be in requirements.txt)
STDLIB = {
    'os', 'sys', 'json', 'logging', 'datetime', 'time', 'threading',
    'subprocess', 'argparse', 'uuid', 'pathlib', 'collections', 'typing',
    'functools', 'itertools', 're', 'hashlib', 'base64', 'urllib',
    'http', 'email', 'csv', 'io', 'tempfile', 'shutil', 'glob',
    'pickle', 'copy', 'enum', 'dataclasses', 'abc', 'contextlib',
    'asyncio', 'multiprocessing', 'queue', 'socket', 'ssl', 'zipfile',
    'tarfile', 'gzip', 'bz2', 'lzma', 'zlib', 'struct', 'array',
    'ctypes', 'mmap', 'select', 'signal', 'errno', 'stat', 'fcntl',
    'pwd', 'grp', 'termios', 'tty', 'pty', 'resource', 'pipes',
    'posixpath', 'ntpath', 'genericpath', 'linecache', 'locale',
    'gettext', 'codecs', 'unicodedata', 'stringprep', 'readline',
    'rlcompleter', 'traceback', 'trace', 'tracemalloc', 'gc',
    'inspect', 'site', 'fpectl', 'warnings', 'contextvars',
    'dataclasses', 'typing_extensions', 'builtins', '__future__'
}

def extract_imports(file_path: Path) -> Set[str]:
    """Extract all import statements from a Python file."""
    imports = set()
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read(), filename=str(file_path))
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.add(alias.name.split('.')[0])
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.add(node.module.split('.')[0])
    except Exception as e:
        print(f"Error parsing {file_path}: {e}")
    
    return imports

def get_requirements() -> Set[str]:
    """Read requirements from requirements.txt."""
    reqs = set()
    req_file = Path("requirements.txt")
    if req_file.exists():
        with open(req_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    # Extract package name (before >=, ==, etc.)
                    pkg = line.split('>=')[0].split('==')[0].split('<')[0].split('[')[0].strip()
                    reqs.add(pkg.lower())
    return reqs

def check_dependencies():
    """Check for missing dependencies."""
    print("🔍 Checking for missing dependencies...\n")
    
    # Get all Python files in src/
    src_files = list(Path("src").rglob("*.py"))
    
    # Extract all imports
    all_imports = set()
    for file_path in src_files[:100]:  # Limit to first 100 files
        imports = extract_imports(file_path)
        all_imports.update(imports)
    
    # Filter out stdlib
    third_party = {imp for imp in all_imports if imp not in STDLIB and not imp.startswith('_')}
    
    # Get requirements
    requirements = get_requirements()
    
    # Check for missing dependencies
    missing = []
    for imp in sorted(third_party):
        # Check if it's in requirements (case-insensitive)
        if imp.lower() not in requirements:
            # Some packages have different import names
            mappings = {
                'PIL': 'pillow',
                'yaml': 'pyyaml',
                'dotenv': 'python-dotenv',
                'pydantic': 'pydantic',
                'discord': 'discord.py',
                'aiohttp': 'aiohttp',
            }
            if imp in mappings:
                mapped = mappings[imp]
                if mapped.lower() not in requirements:
                    missing.append(f"{imp} (install: {mapped})")
            else:
                missing.append(imp)
    
    print(f"📦 Found {len(third_party)} third-party imports")
    print(f"📋 Found {len(requirements)} packages in requirements.txt\n")
    
    if missing:
        print(f"❌ Missing dependencies ({len(missing)}):")
        for dep in missing[:20]:
            print(f"   - {dep}")
        if len(missing) > 20:
            print(f"   ... and {len(missing) - 20} more")
    else:
        print("✅ All dependencies appear to be in requirements.txt")
    
    return missing

if __name__ == "__main__":
    check_dependencies()

