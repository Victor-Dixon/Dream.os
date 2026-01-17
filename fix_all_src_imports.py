#!/usr/bin/env python3
"""
Comprehensive Import Fixer for Agent Cellphone V2
================================================

Fixes all absolute imports that reference 'src.' to use proper relative imports.
This addresses the 669 broken import paths identified in the repository audit.

Usage:
    python fix_all_src_imports.py

Author: Agent-3 (Infrastructure & DevOps Specialist)
"""

import os
import re
from pathlib import Path


def get_import_depth(file_path: Path, src_root: Path) -> int:
    """Calculate how many levels up to reach src/ from the file."""
    relative_path = file_path.relative_to(src_root)
    # Count directory levels (e.g., core/config/file.py needs 2 dots to reach src/)
    return len(relative_path.parts) - 1  # -1 because we don't count the file itself


def fix_import_line(line: str, depth: int) -> str:
    """Convert absolute src. import to relative import."""

    # Pattern: from src.X.Y import Z
    pattern = r'from src\.([^;]+)'

    def replace_import(match):
        import_path = match.group(1)
        # Add the correct number of dots for relative import
        dots = '.' * depth
        return f'from {dots}{import_path}'

    return re.sub(pattern, replace_import, line)


def fix_file_imports(file_path: Path, src_root: Path):
    """Fix all src. imports in a single file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content
        depth = get_import_depth(file_path, src_root)

        # Fix all lines that contain 'from src.'
        lines = content.split('\n')
        fixed_lines = []

        for line in lines:
            if 'from src.' in line:
                fixed_line = fix_import_line(line, depth)
                fixed_lines.append(fixed_line)
                if fixed_line != line:
                    print(f"  Fixed: {line.strip()} -> {fixed_line.strip()}")
            else:
                fixed_lines.append(line)

        new_content = '\n'.join(fixed_lines)

        if new_content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True

    except Exception as e:
        print(f"Error processing {file_path}: {e}")

    return False


def main():
    """Main function to fix all src. imports in the repository."""
    src_root = Path('src')

    if not src_root.exists():
        print("Error: src/ directory not found")
        return

    print("🔧 Starting comprehensive import fixes...")
    print("Converting absolute 'from src.X' imports to relative imports")

    total_files = 0
    fixed_files = 0

    # Find all Python files in src/
    for py_file in src_root.rglob('*.py'):
        total_files += 1
        print(f"Processing: {py_file.relative_to(src_root)}")

        if fix_file_imports(py_file, src_root):
            fixed_files += 1

    print("\n📊 Import Fix Summary:")
    print(f"  Total Python files processed: {total_files}")
    print(f"  Files with import fixes: {fixed_files}")
    print("\n✅ Import fixes completed!")
    print("\nNext steps:")
    print("1. Test imports: python -c 'from src.core.messaging_core import MessagingCoreOrchestrator'")
    print("2. Run existing tests to ensure no regressions")
    print("3. Commit changes: git add -A && git commit -m 'Fix absolute to relative imports'")


if __name__ == '__main__':
    main()