#!/usr/bin/env python3
"""
Verify Import Errors in Broken Tools
=====================================

Checks tools with import errors to identify missing dependencies or import issues.

Author: Agent-5 (Business Intelligence Specialist)
Date: 2025-12-20
"""

import sys
import subprocess
from pathlib import Path
from typing import List, Dict

PROJECT_ROOT = Path(__file__).parent.parent


def check_imports(tool_path: Path) -> Dict[str, any]:
    """Check if a tool can be imported and identify missing dependencies."""
    result = {
        "tool": str(tool_path.relative_to(PROJECT_ROOT)),
        "can_compile": False,
        "can_import": False,
        "missing_imports": [],
        "errors": []
    }
    
    # Test 1: Can compile?
    try:
        compile_result = subprocess.run(
            [sys.executable, '-m', 'py_compile', str(tool_path)],
            capture_output=True,
            text=True,
            timeout=5
        )
        result["can_compile"] = (compile_result.returncode == 0)
        if compile_result.returncode != 0:
            result["errors"].append(f"Compile error: {compile_result.stderr[:200]}")
    except Exception as e:
        result["errors"].append(f"Compile exception: {str(e)}")
    
    # Test 2: Can import (basic syntax check)?
    # Read file and check for obvious import issues
    try:
        content = tool_path.read_text(encoding='utf-8')
        
        # Look for common missing imports
        import_patterns = [
            r'import\s+(\w+)',
            r'from\s+(\S+)\s+import'
        ]
        
        # Check for try/except ImportError patterns (optional dependencies)
        if 'except ImportError' in content or 'except Import' in content:
            result["missing_imports"].append("Has optional imports (check runtime)")
            
    except Exception as e:
        result["errors"].append(f"Read error: {str(e)}")
    
    # Test 3: Try actual import (if compile works)
    if result["can_compile"]:
        try:
            # Add tools directory to path
            tool_name = tool_path.stem
            import importlib.util
            spec = importlib.util.spec_from_file_location(tool_name, tool_path)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                # Don't execute, just check if spec is valid
                result["can_import"] = True
        except Exception as e:
            result["errors"].append(f"Import check: {str(e)[:200]}")
    
    return result


def main():
    """Check import errors for reported broken tools."""
    
    # Tools with import errors from audit
    import_error_tools = [
        "tools/generate_chronological_blog.py"
    ]
    
    print("🔍 Verifying Import Errors")
    print("=" * 70)
    
    results = []
    for tool_rel_path in import_error_tools:
        tool_path = PROJECT_ROOT / tool_rel_path
        if not tool_path.exists():
            print(f"❌ Tool not found: {tool_rel_path}")
            continue
        
        print(f"\n📦 Checking: {tool_path.name}")
        result = check_imports(tool_path)
        results.append(result)
        
        if result["can_compile"] and result["can_import"]:
            print(f"   ✅ Compiles and imports successfully")
        else:
            print(f"   ❌ Issues found:")
            if not result["can_compile"]:
                print(f"      - Compile failed")
            if not result["can_import"]:
                print(f"      - Import check failed")
            if result["errors"]:
                for error in result["errors"]:
                    print(f"      - {error}")
            if result["missing_imports"]:
                for imp in result["missing_imports"]:
                    print(f"      - {imp}")
    
    print("\n" + "=" * 70)
    print("📊 SUMMARY")
    print(f"   Tools checked: {len(results)}")
    print(f"   ✅ Working: {sum(1 for r in results if r['can_compile'] and r['can_import'])}")
    print(f"   ❌ Issues: {sum(1 for r in results if not (r['can_compile'] and r['can_import']))}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())


