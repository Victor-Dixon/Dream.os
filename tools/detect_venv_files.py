#!/usr/bin/env python3
"""
Virtual Environment File Detector

Detects virtual environment files that should NOT be in repositories.
Following Agent-2's findings: venv files found in DigitalDreamscape/lib/python3.11/site-packages/

Author: Agent-5 (Business Intelligence Specialist)
Date: 2025-11-26
"""

import os
import sys
from pathlib import Path
from typing import List, Dict


VENV_PATTERNS = [
    'venv/',
    '.venv/',
    'env/',
    '.env/',
    'lib/python3.11/site-packages/',
    'lib/python3.10/site-packages/',
    'lib/python3.9/site-packages/',
    'lib/python3.8/site-packages/',
    'site-packages/',
    '__pycache__/',
    '*.pyc',
    '*.pyo',
    '*.pyd',
]


def detect_venv_files(root_path: str) -> Dict[str, List[str]]:
    """
    Detect virtual environment files in repository.
    
    Args:
        root_path: Root directory to scan
        
    Returns:
        Dictionary with pattern matches and file paths
    """
    root = Path(root_path)
    findings = {pattern: [] for pattern in VENV_PATTERNS}
    
    for root_dir, dirs, files in os.walk(root):
        # Skip .git directories
        if '.git' in root_dir:
            continue
            
        rel_path = os.path.relpath(root_dir, root)
        
        # Check directory names
        for pattern in VENV_PATTERNS:
            if pattern.rstrip('/') in rel_path or pattern.rstrip('/') in root_dir:
                findings[pattern].append(rel_path)
        
        # Check files
        for file in files:
            file_path = os.path.join(rel_path, file)
            for pattern in VENV_PATTERNS:
                if pattern.startswith('*') and file.endswith(pattern[1:]):
                    findings[pattern].append(file_path)
    
    return findings


def print_report(findings: Dict[str, List[str]]):
    """Print detection report."""
    total = sum(len(paths) for paths in findings.values())
    
    print("=" * 60)
    print("VIRTUAL ENVIRONMENT FILE DETECTION REPORT")
    print("=" * 60)
    print(f"\nTotal matches found: {total}\n")
    
    for pattern, paths in findings.items():
        if paths:
            print(f"\nPattern: {pattern}")
            print(f"  Matches: {len(paths)}")
            for path in paths[:10]:  # Show first 10
                print(f"    - {path}")
            if len(paths) > 10:
                print(f"    ... and {len(paths) - 10} more")
    
    if total > 0:
        print("\n⚠️  WARNING: Virtual environment files detected!")
        print("   These should NOT be in repositories.")
        print("   Action: Remove these files/directories.")
    else:
        print("\n✅ No virtual environment files detected.")


def main():
    """Main entry point."""
    if len(sys.argv) > 1:
        root_path = sys.argv[1]
    else:
        root_path = os.getcwd()
    
    print(f"Scanning: {root_path}")
    findings = detect_venv_files(root_path)
    print_report(findings)
    
    return 0 if sum(len(p) for p in findings.values()) == 0 else 1


if __name__ == '__main__':
    sys.exit(main())



