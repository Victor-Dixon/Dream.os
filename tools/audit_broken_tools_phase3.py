#!/usr/bin/env python3
"""
Phase 3 Broken Tools Audit

Scans all Python tools and identifies import failures and hard execution errors.
Timeouts are tracked separately as "slow" because many tools legitimately perform IO.
"""

import argparse
import importlib
import importlib.util
import subprocess
import sys
from pathlib import Path
from typing import Dict, List

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))


def _path_to_module_name(tool_path: Path) -> str | None:
    """
    Convert a repo-relative python file path into a module name.

    Example:
      tools/categories/system_tools.py -> tools.categories.system_tools
    """
    try:
        rel_path = tool_path.relative_to(project_root)
    except ValueError:
        return None

    if not rel_path.parts or rel_path.parts[0] != "tools":
        return None

    return ".".join(rel_path.with_suffix("").parts)


def test_tool_import(tool_path: Path) -> Dict:
    """Test if a tool can be imported without errors."""
    try:
        module_name = _path_to_module_name(tool_path)
        if module_name:
            importlib.import_module(module_name)
        else:
            spec = importlib.util.spec_from_file_location("tool", tool_path)
            if spec is None or spec.loader is None:
                return {"status": "error", "error": "Could not create spec"}

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
    """Test if a tool can execute quickly (with --help or no args)."""
    try:
        module_name = _path_to_module_name(tool_path)
        exec_cmd: List[str]
        if module_name and any(part in {"categories", "core", "adapters", "utils"} for part in tool_path.parts):
            exec_cmd = [sys.executable, "-m", module_name, "--help"]
        else:
            exec_cmd = [sys.executable, str(tool_path), "--help"]

        result = subprocess.run(exec_cmd, capture_output=True, timeout=5, cwd=project_root)
        if result.returncode == 0:
            return {"status": "working", "error": None}

        if module_name and any(part in {"categories", "core", "adapters", "utils"} for part in tool_path.parts):
            exec_cmd = [sys.executable, "-m", module_name]
        else:
            exec_cmd = [sys.executable, str(tool_path)]

        result = subprocess.run(exec_cmd, capture_output=True, timeout=5, cwd=project_root)
        if result.returncode in [0, 1, 2]:
            return {"status": "working", "error": None}

        return {
            "status": "execution_error",
            "error": result.stderr.decode()[:200] if result.stderr else "Unknown error",
        }
    except subprocess.TimeoutExpired:
        return {"status": "timeout", "error": "Execution timed out"}
    except Exception as e:
        return {"status": "exception", "error": str(e)}


def run_audit() -> int:
    print("🔧 Phase 3 Broken Tools Audit")
    print("=" * 60)

    tools_dir = project_root / "tools"
    all_tools = list(tools_dir.rglob("*.py"))
    tools = [t for t in all_tools if t.name != "__init__.py" and "__pycache__" not in str(t)]

    print(f"Scanning {len(tools)} tools...\n")

    broken_tools = []
    working_tools = []
    slow_tools = []

    for tool_path in sorted(tools):
        rel_path = tool_path.relative_to(project_root)

        import_result = test_tool_import(tool_path)
        if import_result["status"] != "working":
            broken_tools.append(
                {"tool": str(rel_path), "status": import_result["status"], "error": import_result["error"]}
            )
            print(f"❌ {rel_path}: {import_result['status']} - {import_result['error'][:60]}")
            continue

        exec_result = test_tool_execution(tool_path)
        if exec_result["status"] == "working":
            working_tools.append(str(rel_path))
            print(f"✅ {rel_path}")
            continue

        if exec_result["status"] == "timeout":
            slow_tools.append(str(rel_path))
            print(f"⏳ {rel_path}: timeout - {exec_result.get('error', '')[:60]}")
            continue

        broken_tools.append(
            {"tool": str(rel_path), "status": exec_result["status"], "error": exec_result["error"]}
        )
        print(f"❌ {rel_path}: {exec_result['status']} - {exec_result.get('error', 'Unknown')[:60]}")

    print("\n" + "=" * 60)
    print(f"Summary: {len(working_tools)} working, {len(slow_tools)} slow, {len(broken_tools)} broken")
    print("=" * 60)

    if broken_tools:
        print("\n🔧 Broken Tools to Fix:")
        for tool in broken_tools[:20]:
            print(f"  - {tool['tool']}: {tool['status']} - {tool['error'][:80]}")
        if len(broken_tools) > 20:
            print(f"  ... and {len(broken_tools) - 20} more")

    if slow_tools:
        print("\n⏳ Slow Tools (timed out during quick execution check):")
        for tool in slow_tools[:20]:
            print(f"  - {tool}")
        if len(slow_tools) > 20:
            print(f"  ... and {len(slow_tools) - 20} more")

    return 0 if len(broken_tools) == 0 else 1


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Phase 3 Broken Tools Audit - Scan tools for import/execution failures"
    )
    parser.add_argument("--run", action="store_true", help="Run the audit (default behavior)")
    _ = parser.parse_args()
    return run_audit()


if __name__ == "__main__":
    sys.exit(main())

