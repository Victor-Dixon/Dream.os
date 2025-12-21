#!/usr/bin/env python3
"""
Find Syntax Errors in Integration Tools
=======================================

Finds syntax errors in integration-related tools for Phase 0 contract.

Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2025-12-21
Task: Phase 0 - Syntax Error Fixes (Integration Tools)
"""

import ast
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))


def check_syntax(file_path: Path) -> tuple[bool, str | None]:
    """Check if a Python file has syntax errors."""
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        
        # Try to parse the file
        ast.parse(content, filename=str(file_path))
        return True, None
    except SyntaxError as e:
        return False, f"Syntax error: {e.msg} at line {e.lineno}"
    except Exception as e:
        return False, f"Error: {str(e)}"


def is_integration_tool(file_path: Path) -> bool:
    """Check if a tool is integration-related."""
    # Integration-related patterns
    integration_patterns = [
        "integration",
        "integrate",
        "validator",
        "verify",
        "check",
        "test",
        "coordination",
        "communication",
        "messaging",
        "orchestrator",
        "functionality",
    ]
    
    file_str = str(file_path).lower()
    name_str = file_path.stem.lower()
    
    # Check if it's in integration-related directories
    if "integration" in file_str or "communication" in file_str or "coordination" in file_str:
        return True
    
    # Check if name contains integration patterns
    for pattern in integration_patterns:
        if pattern in name_str:
            return True
    
    return False


def main():
    """Find syntax errors in integration tools."""
    tools_dir = project_root / "tools"
    
    print("🔍 Finding syntax errors in integration tools...")
    print()
    
    # Get all Python files in tools directory
    python_files = list(tools_dir.rglob("*.py"))
    python_files = [
        f for f in python_files
        if "__pycache__" not in str(f)
        and not f.name.startswith("test_")
        and not f.name.endswith("_test.py")
    ]
    
    # Filter to integration tools
    integration_files = [f for f in python_files if is_integration_tool(f)]
    
    print(f"📊 Found {len(integration_files)} integration-related tools")
    print()
    
    # Check for syntax errors
    syntax_errors = []
    
    for file_path in integration_files:
        is_valid, error = check_syntax(file_path)
        if not is_valid:
            rel_path = file_path.relative_to(project_root)
            syntax_errors.append((rel_path, error))
            print(f"❌ {rel_path}: {error}")
    
    print()
    print("=" * 60)
    print("📊 Results")
    print("=" * 60)
    print(f"   Total integration tools checked: {len(integration_files)}")
    print(f"   Syntax errors found: {len(syntax_errors)}")
    print()
    
    if syntax_errors:
        print("🔧 Files needing fixes:")
        for file_path, error in syntax_errors:
            print(f"   - {file_path}")
            print(f"     {error}")
    else:
        print("✅ No syntax errors found in integration tools!")
    
    return 0 if not syntax_errors else 1


if __name__ == "__main__":
    sys.exit(main())

