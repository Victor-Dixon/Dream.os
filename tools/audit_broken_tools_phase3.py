#!/usr/bin/env python3
"""
Phase 3 Broken Tools Audit - Scan all tools for runtime errors

Scans all Python tools and identifies runtime errors.
"""

import sys
import subprocess
import importlib.util
from pathlib import Path
from typing import List, Dict

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

def test_tool_import(tool_path: Path) -> Dict:
    """Test if a tool can be imported without errors."""
    try:
        spec = importlib.util.spec_from_file_location("tool", tool_path)
        if spec is None or spec.loader is None:
            return {"status": "error", "error": "Could not create spec"}
        
        # Try to load the module
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        return {"status": "working", "error": None}
    except SyntaxError as e:
        return {"status": "syntax_error", "error": f"Syntax error: {e}"}
    except ImportError as e:
        return {"status": "import_error", "error": f"Import error: {e}"}
    except Exception as e:
        return {"status": "runtime_error", "error": f"Runtime error: {e}"}

def test_tool_execution(tool_path: Path) -> Dict:
    """Test if a tool can execute (with --help or no args)."""
    try:
        # Try with --help first
        result = subprocess.run(
            [sys.executable, str(tool_path), "--help"],
            capture_output=True,
            timeout=3,
            cwd=project_root
        )
        
        if result.returncode == 0:
            return {"status": "working", "error": None}
        
        # If --help fails, try with no args (some tools don't have --help)
        result = subprocess.run(
            [sys.executable, str(tool_path)],
            capture_output=True,
            timeout=3,
            cwd=project_root
        )
        
        # If it exits with 0 or 1 (usage error), it's working
        if result.returncode in [0, 1, 2]:
            return {"status": "working", "error": None}
        
        return {
            "status": "execution_error",
            "error": result.stderr.decode()[:200] if result.stderr else "Unknown error"
        }
    except subprocess.TimeoutExpired:
        return {"status": "timeout", "error": "Execution timed out"}
    except Exception as e:
        return {"status": "exception", "error": str(e)}

def main():
    """Main entry point."""
    print("🔧 Phase 3 Broken Tools Audit")
    print("=" * 60)
    
    tools_dir = project_root / "tools"
    all_tools = list(tools_dir.rglob("*.py"))
    # Filter out __init__.py and __pycache__
    tools = [t for t in all_tools if t.name != "__init__.py" and "__pycache__" not in str(t)]
    
    print(f"Scanning {len(tools)} tools...\n")
    
    broken_tools = []
    working_tools = []
    
    for tool_path in sorted(tools):
        rel_path = tool_path.relative_to(project_root)
        
        # Test import first
        import_result = test_tool_import(tool_path)
        
        if import_result["status"] != "working":
            broken_tools.append({
                "tool": str(rel_path),
                "status": import_result["status"],
                "error": import_result["error"]
            })
            print(f"❌ {rel_path}: {import_result['status']} - {import_result['error'][:60]}")
            continue
        
        # Test execution
        exec_result = test_tool_execution(tool_path)
        
        if exec_result["status"] != "working":
            broken_tools.append({
                "tool": str(rel_path),
                "status": exec_result["status"],
                "error": exec_result["error"]
            })
            print(f"❌ {rel_path}: {exec_result['status']} - {exec_result.get('error', 'Unknown')[:60]}")
        else:
            working_tools.append(str(rel_path))
            print(f"✅ {rel_path}")
    
    print("\n" + "=" * 60)
    print(f"Summary: {len(working_tools)} working, {len(broken_tools)} broken")
    print("=" * 60)
    
    if broken_tools:
        print("\n🔧 Broken Tools to Fix:")
        for tool in broken_tools[:20]:  # Show first 20
            print(f"  - {tool['tool']}: {tool['status']} - {tool['error'][:80]}")
        if len(broken_tools) > 20:
            print(f"  ... and {len(broken_tools) - 20} more")
    
    return 0 if len(broken_tools) == 0 else 1

if __name__ == "__main__":
    sys.exit(main())

