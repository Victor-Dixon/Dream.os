#!/usr/bin/env python3
"""
Test Usage Analyzer - Identify Unused Functionality via Test Coverage
=====================================================================

Analyzes test files to identify methods/functions that are only tested
but never used in production code. Uses test coverage analysis to discover
potentially unused functionality.

Author: Agent-3 (Infrastructure & DevOps Specialist)
Date: 2025-11-27
License: MIT
"""

import ast
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple
import json
import re


def find_python_files(directory: Path, pattern: str = "*.py") -> List[Path]:
    """Find all Python files matching pattern."""
    files = []
    for path in directory.rglob(pattern):
        if any(skip in str(path) for skip in ["__pycache__", ".git", "venv", ".venv"]):
            continue
        files.append(path)
    return files


def parse_python_file(file_path: Path) -> Tuple[List[str], List[str], Dict[str, List[str]]]:
    """Parse Python file and extract functions, classes, and methods."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        tree = ast.parse(content, filename=str(file_path))
        
        functions = []
        classes = []
        class_methods = {}  # class_name -> [methods]
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Check if it's a method (inside a class)
                if any(isinstance(parent, ast.ClassDef) for parent in ast.walk(tree) if hasattr(parent, 'body') and node in parent.body):
                    # Find parent class
                    for parent in ast.walk(tree):
                        if isinstance(parent, ast.ClassDef):
                            if node in parent.body:
                                if parent.name not in class_methods:
                                    class_methods[parent.name] = []
                                class_methods[parent.name].append(node.name)
                                break
                else:
                    functions.append(node.name)
            elif isinstance(node, ast.ClassDef):
                classes.append(node.name)
        
        return functions, classes, class_methods
    except Exception as e:
        print(f"⚠️  Error parsing {file_path}: {e}")
        return [], [], {}


def find_test_files_for_module(module_path: Path) -> List[Path]:
    """Find test files that test this module."""
    module_name = module_path.stem
    test_files = []
    
    # Look in tests directory
    tests_dir = Path("tests")
    if not tests_dir.exists():
        return []
    
    # Find test files matching module name
    patterns = [
        f"test_{module_name}.py",
        f"test_{module_name.replace('_', '')}.py",
        f"test_{module_name.replace('_', '_')}.py"
    ]
    
    for pattern in patterns:
        for test_file in tests_dir.rglob(pattern):
            test_files.append(test_file)
    
    # Also check for test files in same directory structure
    test_path = tests_dir / module_path.relative_to(Path("src"))
    test_file = test_path.parent / f"test_{test_path.name}"
    if test_file.exists():
        test_files.append(test_file)
    
    return list(set(test_files))


def extract_tested_methods(test_file: Path) -> Set[str]:
    """Extract methods/functions tested in test file."""
    tested = set()
    
    try:
        with open(test_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        tree = ast.parse(content, filename=str(test_file))
        
        # Find all method calls and attribute accesses
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Attribute):
                    tested.add(node.func.attr)
                elif isinstance(node.func, ast.Name):
                    tested.add(node.func.id)
    except Exception as e:
        print(f"⚠️  Error parsing test file {test_file}: {e}")
    
    return tested


def search_codebase_usage(method_name: str, source_file: Path, search_dirs: List[Path]) -> bool:
    """Search codebase for actual usage of method (excluding test files)."""
    for search_dir in search_dirs:
        for py_file in search_dir.rglob("*.py"):
            # Skip test files and the source file itself
            if "test_" in str(py_file) or py_file == source_file:
                continue
            
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Simple pattern matching (could be enhanced with AST)
                if f".{method_name}(" in content or f" {method_name}(" in content:
                    return True
            except Exception:
                continue
    
    return False


def analyze_module(module_path: Path) -> Dict:
    """Analyze a module for unused functionality."""
    functions, classes, class_methods = parse_python_file(module_path)
    test_files = find_test_files_for_module(module_path)
    
    # Get tested methods from test files
    tested_methods = set()
    for test_file in test_files:
        tested_methods.update(extract_tested_methods(test_file))
    
    # Find methods only in tests
    unused_candidates = []
    
    # Check functions
    for func in functions:
        if func in tested_methods:
            # Check if used in production
            search_dirs = [Path("src"), Path("tools")]
            if not search_codebase_usage(func, module_path, search_dirs):
                unused_candidates.append({
                    "type": "function",
                    "name": func,
                    "file": str(module_path),
                    "tested": True,
                    "used_in_production": False
                })
    
    # Check class methods
    for class_name, methods in class_methods.items():
        for method in methods:
            if method in tested_methods:
                search_dirs = [Path("src"), Path("tools")]
                if not search_codebase_usage(method, module_path, search_dirs):
                    unused_candidates.append({
                        "type": "method",
                        "name": f"{class_name}.{method}",
                        "class": class_name,
                        "method": method,
                        "file": str(module_path),
                        "tested": True,
                        "used_in_production": False
                    })
    
    return {
        "module": str(module_path),
        "functions": len(functions),
        "classes": len(classes),
        "test_files": [str(tf) for tf in test_files],
        "unused_candidates": unused_candidates
    }


def main():
    """Main analysis function."""
    if len(sys.argv) > 1:
        target = Path(sys.argv[1])
    else:
        target = Path("src/core")
    
    if not target.exists():
        print(f"❌ Error: {target} does not exist")
        return 1
    
    print(f"🔍 Analyzing {target} for unused functionality...")
    print("=" * 60)
    
    python_files = find_python_files(target)
    results = []
    
    for py_file in python_files:
        if "test_" in str(py_file) or "__pycache__" in str(py_file):
            continue
        
        analysis = analyze_module(py_file)
        if analysis["unused_candidates"]:
            results.append(analysis)
    
    # Print results
    print(f"\n📊 Analysis Complete: {len(results)} modules with unused candidates\n")
    
    for result in results:
        print(f"📁 {result['module']}")
        print(f"   Functions: {result['functions']}, Classes: {result['classes']}")
        print(f"   Test Files: {len(result['test_files'])}")
        
        if result['unused_candidates']:
            print(f"   ⚠️  {len(result['unused_candidates'])} potentially unused items:")
            for candidate in result['unused_candidates']:
                print(f"      - {candidate['name']} ({candidate['type']})")
        else:
            print(f"   ✅ No unused candidates found")
        print()
    
    # Save results
    output_file = Path("agent_workspaces/Agent-3/unused_functionality_analysis.json")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"💾 Results saved to: {output_file}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())



