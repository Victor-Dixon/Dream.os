#!/usr/bin/env python3
"""
Simple duplication checker for Agent Cellphone V2 closure.
Since the original duplication_audit.py was archived during cleanup.
"""

import os
from pathlib import Path
from collections import defaultdict
import hashlib


def get_file_hash(filepath):
    """Get MD5 hash of file content."""
    hash_md5 = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def find_duplicates(directory):
    """Find duplicate files in directory."""
    hashes = defaultdict(list)

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(('.py', '.md', '.txt', '.json')):
                filepath = Path(root) / file
                try:
                    file_hash = get_file_hash(filepath)
                    hashes[file_hash].append(filepath)
                except Exception as e:
                    print(f"Error reading {filepath}: {e}")

    duplicates = {k: v for k, v in hashes.items() if len(v) > 1}
    return duplicates


def main():
    """Main duplication check."""
    project_root = Path(__file__).parent.parent
    src_dir = project_root / "src"

    print("🔍 Checking for code duplication in src/ directory...")

    if not src_dir.exists():
        print("❌ src/ directory not found")
        return

    duplicates = find_duplicates(src_dir)

    if duplicates:
        print(f"⚠️  Found {len(duplicates)} duplicate file groups:")
        for hash_val, files in duplicates.items():
            print(f"\nDuplicate group ({len(files)} files):")
            for file in files:
                print(f"  - {file.relative_to(project_root)}")
    else:
        print("✅ No duplicate files found in src/ directory")

    # Check for incomplete implementations
    print("\n🔍 Checking for incomplete implementations...")
    incomplete_indicators = ["TODO", "FIXME", "NotImplemented", "pass  # TODO"]

    for root, dirs, files in os.walk(src_dir):
        for file in files:
            if file.endswith('.py'):
                filepath = Path(root) / file
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        for indicator in incomplete_indicators:
                            if indicator in content:
                                print(f"⚠️  Incomplete implementation in {filepath.relative_to(project_root)}: {indicator}")
                except Exception as e:
                    print(f"Error reading {filepath}: {e}")


if __name__ == "__main__":
    main()