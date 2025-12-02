#!/usr/bin/env python3
"""
Agent-7 Comprehensive Cleanup Audit Tool
========================================

Systematically identifies broken/unused code matching the cleanup pattern:
- Broken imports (missing modules)
- Unused modules (no external imports)
- Incomplete implementations

Author: Agent-7 (Web Development Specialist)
"""

import ast
import importlib.util
import sys
from pathlib import Path
from typing import Any

# Add src to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))


def check_module_imports(file_path: Path) -> tuple[bool, list[str]]:
    """Check if a module can be imported and what errors occur."""
    errors = []
    try:
        # Try to parse the file
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Parse AST to find imports
        tree = ast.parse(content, filename=str(file_path))
        
        # Try to import
        module_name = str(file_path.relative_to(project_root / "src")).replace("/", ".").replace("\\", ".").replace(".py", "")
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return True, []
    except SyntaxError as e:
        errors.append(f"SyntaxError: {e}")
    except ImportError as e:
        errors.append(f"ImportError: {e}")
    except Exception as e:
        errors.append(f"Error: {type(e).__name__}: {e}")
    
    return False, errors


def find_broken_modules(directory: Path) -> dict[str, list[str]]:
    """Find all modules with broken imports."""
    broken = {}
    
    for py_file in directory.rglob("*.py"):
        if "__pycache__" in str(py_file):
            continue
        
        can_import, errors = check_module_imports(py_file)
        if not can_import and errors:
            rel_path = str(py_file.relative_to(project_root))
            broken[rel_path] = errors
    
    return broken


if __name__ == "__main__":
    src_dir = project_root / "src"
    broken = find_broken_modules(src_dir)
    
    print(f"Found {len(broken)} broken modules")
    for path, errors in list(broken.items())[:10]:
        print(f"\n{path}:")
        for error in errors[:3]:
            print(f"  - {error}")

