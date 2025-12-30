"""
Comprehensive Audit Tool
========================
Scans tools for runtime errors and identifies those needing fixes.

<!-- SSOT Domain: tools -->
"""

import os
import subprocess
import sys
from pathlib import Path

def audit_tool(tool_path: Path):
    """Test a tool by running it."""
    try:
        # Convert path to module name if it's in a package
        cwd = Path.cwd().resolve()
        abs_tool_path = tool_path.resolve()
        
        try:
            rel_path = abs_tool_path.relative_to(cwd)
            module_name = str(rel_path).replace(os.sep, ".").replace(".py", "")
        except ValueError:
            # Fallback for paths that might be on different drives or something
            return f"❌ ERROR: Path issue for {tool_path}"
        
        # Try running as module first
        result = subprocess.run(
            [sys.executable, "-m", module_name, "--help"],
            capture_output=True,
            text=True,
            timeout=15,
            cwd=str(cwd)
        )
        
        if result.returncode == 0:
            return "✅ PASS"
        
        # Check if it failed because --help is not supported
        if "unrecognized arguments: --help" in result.stderr or "invalid choice: '--help'" in result.stderr:
            return "✅ PASS (No --help support)"
            
        # Fallback to direct execution if module run fails
        result = subprocess.run(
            [sys.executable, str(abs_tool_path), "--help"],
            capture_output=True,
            text=True,
            timeout=15,
            cwd=str(cwd)
        )
        if result.returncode == 0:
            return "✅ PASS"
        if "unrecognized arguments: --help" in result.stderr or "invalid choice: '--help'" in result.stderr:
            return "✅ PASS (No --help support)"

        error_msg = result.stderr[:200].replace('\n', ' ')
        return f"❌ FAIL ({result.returncode}): {error_msg}..."
        
    except subprocess.TimeoutExpired:
        return "⏳ TIMEOUT"
    except Exception as e:
        return f"❌ ERROR: {str(e)}"

def main():
    tools_dir = Path("tools")
    all_tools = list(tools_dir.rglob("*.py"))
    
    print(f"🔍 Auditing {len(all_tools)} tools in {tools_dir} recursively...")
    
    broken = []
    for tool in all_tools:
        if tool.name == "__init__.py" or "pycache" in str(tool) or "tests" in str(tool):
            continue
            
        status = audit_tool(tool)
        if "❌" in status:
            print(f"{str(tool):50} | {status}")
            broken.append((str(tool), status))
        else:
            # print(f"{str(tool):50} | {status}")
            pass
            
    print("\n" + "="*80)
    print(f"📊 SUMMARY: {len(broken)} broken tools found.")
    for path, status in broken:
        print(f"- {path}: {status}")

if __name__ == "__main__":
    main()
