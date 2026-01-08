#!/usr/bin/env python3
"""
V2 Compliance Checker Tool - Agent-7
=====================================

Quick utility to check V2 compliance for Python files.
Checks file size (≤400 lines) and function sizes (≤30 lines).

Usage: python tools/v2_compliance_checker.py <file_path>

Returns exit code 0 if compliant, 1 if violations found.
"""

import sys
import os
from pathlib import Path

def check_file_size(filepath: Path, max_lines: int = 400) -> tuple[bool, str]:
    """Check if file size is within V2 limits."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        line_count = len(lines)
        if line_count > max_lines:
            return False, f"File exceeds {max_lines} line limit: {line_count} lines"
        return True, f"File size OK: {line_count} lines"
    except Exception as e:
        return False, f"Error reading file: {e}"

def check_function_sizes(filepath: Path, max_lines: int = 30) -> tuple[bool, list[str]]:
    """Check if all functions are within size limits."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        lines = content.split('\n')
        violations = []
        current_function = None
        function_start = 0

        for i, line in enumerate(lines, 1):
            # Check for function definition
            if line.strip().startswith('def ') or line.strip().startswith('    def '):
                # If we were tracking a function, check its size
                if current_function and (i - 1 - function_start) > max_lines:
                    violations.append(f"Function '{current_function}' exceeds {max_lines} line limit: {i - 1 - function_start} lines")

                # Start tracking new function
                func_name = line.strip().split('def ')[1].split('(')[0]
                current_function = func_name
                function_start = i

        # Check the last function
        if current_function and (len(lines) - function_start) > max_lines:
            violations.append(f"Function '{current_function}' exceeds {max_lines} line limit: {len(lines) - function_start} lines")

        return len(violations) == 0, violations

    except Exception as e:
        return False, [f"Error analyzing functions: {e}"]

def main():
    """Main entry point."""
    if len(sys.argv) != 2:
        print("Usage: python tools/v2_compliance_checker.py <file_path>")
        sys.exit(1)

    filepath = Path(sys.argv[1])

    if not filepath.exists():
        print(f"❌ File not found: {filepath}")
        sys.exit(1)

    if not filepath.suffix == '.py':
        print(f"❌ Not a Python file: {filepath}")
        sys.exit(1)

    print(f"🔍 Checking V2 compliance for: {filepath}")
    print("=" * 50)

    # Check file size
    file_ok, file_msg = check_file_size(filepath)
    status_icon = "✅" if file_ok else "❌"
    print(f"{status_icon} File Size: {file_msg}")

    # Check function sizes
    func_ok, func_violations = check_function_sizes(filepath)
    if func_ok:
        print("✅ Function Sizes: All functions within 30-line limit")
    else:
        print("❌ Function Sizes: Violations found")
        for violation in func_violations:
            print(f"   • {violation}")

    # Overall result
    overall_ok = file_ok and func_ok
    print("=" * 50)
    if overall_ok:
        print("🎉 V2 COMPLIANT: File passes all checks")
        sys.exit(0)
    else:
        print("⚠️ V2 VIOLATIONS: File needs refactoring")
        sys.exit(1)

if __name__ == "__main__":
    main()