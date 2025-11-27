#!/usr/bin/env python3
"""
Test All Discord Buttons
=======================

Quick test script to verify all Discord buttons have proper error handling.
"""

import ast
import sys
from pathlib import Path

def check_file_for_buttons(file_path: Path) -> list[str]:
    """Check if file has buttons and if callbacks have error handling."""
    issues = []
    try:
        content = file_path.read_text(encoding="utf-8")
        tree = ast.parse(content, filename=str(file_path))
        
        # Find all async functions that take interaction parameter
        async_funcs = []
        for node in ast.walk(tree):
            if isinstance(node, ast.AsyncFunctionDef):
                # Check if it takes interaction parameter
                params = [arg.arg for arg in node.args.args]
                if "interaction" in params:
                    async_funcs.append((node.name, node.lineno))
        
        # Check if these functions have try/except
        for func_name, lineno in async_funcs:
            func_node = None
            for node in ast.walk(tree):
                if isinstance(node, ast.AsyncFunctionDef) and node.name == func_name:
                    func_node = node
                    break
            
            if func_node:
                has_try = False
                for child in ast.walk(func_node):
                    if isinstance(child, ast.Try):
                        has_try = True
                        break
                
                if not has_try:
                    issues.append(f"Line {lineno}: {func_name}() missing try/except")
    
    except Exception as e:
        issues.append(f"Error parsing {file_path.name}: {e}")
    
    return issues

def main():
    """Check all Discord files for button error handling."""
    print("=" * 70)
    print("🔍 CHECKING ALL DISCORD BUTTONS FOR ERROR HANDLING")
    print("=" * 70 + "\n")
    
    project_root = Path(__file__).resolve().parent.parent
    discord_dir = project_root / "src" / "discord_commander"
    
    all_issues = {}
    for py_file in discord_dir.rglob("*.py"):
        if "deprecated" in str(py_file):
            continue
        issues = check_file_for_buttons(py_file)
        if issues:
            all_issues[str(py_file)] = issues
    
    if not all_issues:
        print("✅ ALL BUTTON CALLBACKS HAVE ERROR HANDLING!")
    else:
        print(f"❌ FOUND {len(all_issues)} FILE(S) WITH MISSING ERROR HANDLING:\n")
        for file_path, issues in all_issues.items():
            print(f"  {Path(file_path).name}:")
            for issue in issues:
                print(f"    - {issue}")
    
    print("\n" + "=" * 70)
    print("💡 NOTE: This checks for try/except blocks, not response.is_done() checks")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    main()

