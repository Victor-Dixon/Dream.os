#!/usr/bin/env python3
"""
Audit Broken Tools Phase 3
==========================
Scans tools for runtime errors and identifies those needing fixes.

<!-- SSOT Domain: tools -->
"""

import os
import subprocess
import sys
from pathlib import Path

def audit_tool(tool_path: Path):
    """Test a tool by running it with --help."""
    try:
        # Some tools might not support --help, but it's a good first test
        result = subprocess.run(
            [sys.executable, str(tool_path), "--help"],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            return "✅ PASS"
        else:
            # Check if it failed because --help is not supported
            if "unrecognized arguments: --help" in result.stderr or "invalid choice: '--help'" in result.stderr:
                return "⚠️  WARN (No --help)"
            error_msg = result.stderr[:100].replace('\n', ' ')
            return f"❌ FAIL ({result.returncode}): {error_msg}..."
    except subprocess.TimeoutExpired:
        return "⏳ TIMEOUT"
    except Exception as e:
        return f"❌ ERROR: {str(e)}"

def main():
    tools_dir = Path("tools")
    if not tools_dir.exists():
        print("❌ tools directory not found")
        return

    tools = list(tools_dir.glob("*.py"))
    print(f"🔍 Auditing {len(tools)} tools in {tools_dir}...")
    
    broken_tools = []
    
    for tool in tools:
        if tool.name == "__init__.py":
            continue
            
        status = audit_tool(tool)
        print(f"{tool.name:40} | {status}")
        
        if "❌" in status:
            broken_tools.append((tool.name, status))
            
    print("\n" + "="*50)
    print(f"📊 SUMMARY: {len(broken_tools)} broken tools found.")
    for name, status in broken_tools:
        print(f"- {name}: {status}")

if __name__ == "__main__":
    main()

