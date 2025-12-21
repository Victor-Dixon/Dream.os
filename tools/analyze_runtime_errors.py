#!/usr/bin/env python3
"""
Analyze Runtime Errors from Tool Audit
=======================================

Systematically tests tools flagged with runtime errors to identify root causes.

Author: Agent-3
Date: 2025-12-20
"""

import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Tuple

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TOOLS_DIR = PROJECT_ROOT / "tools"
RESULTS_FILE = PROJECT_ROOT / "agent_workspaces" / "Agent-5" / "tool_audit_assignments" / "Agent-3_audit_results.json"


def test_tool_help(tool_path: Path) -> Tuple[bool, str, str]:
    """Test if tool can show help."""
    try:
        result = subprocess.run(
            [sys.executable, str(tool_path), "--help"],
            capture_output=True,
            text=True,
            timeout=10,
            cwd=PROJECT_ROOT
        )
        
        stdout = result.stdout.strip()
        stderr = result.stderr.strip()
        
        # Check if help worked
        if result.returncode == 0 or "usage:" in stdout.lower() or "--help" in stdout.lower():
            return True, stdout, stderr
        
        # Check for common errors
        if "ModuleNotFoundError" in stderr:
            return False, "IMPORT_ERROR", stderr
        elif "ImportError" in stderr:
            return False, "IMPORT_ERROR", stderr
        elif "SyntaxError" in stderr:
            return False, "SYNTAX_ERROR", stderr
        elif "Traceback" in stderr:
            return False, "RUNTIME_ERROR", stderr
        else:
            return False, "UNKNOWN_ERROR", stderr or stdout
            
    except subprocess.TimeoutExpired:
        return False, "TIMEOUT", "Tool timed out after 10 seconds"
    except Exception as e:
        return False, "EXCEPTION", str(e)


def analyze_runtime_errors():
    """Analyze runtime errors from audit results."""
    # Load audit results
    with open(RESULTS_FILE, 'r') as f:
        audit_data = json.load(f)
    
    runtime_errors = audit_data["results"]["runtime_errors"]
    
    print(f"🔍 Analyzing {len(runtime_errors)} tools with runtime errors...\n")
    
    categories = {
        "WORKING": [],
        "IMPORT_ERROR": [],
        "SYNTAX_ERROR": [],
        "NO_HELP_SUPPORT": [],
        "MISSING_DATA": [],
        "TIMEOUT": [],
        "OTHER_RUNTIME": []
    }
    
    for tool_rel in runtime_errors:
        tool_path = PROJECT_ROOT / tool_rel.replace("\\", "/")
        
        if not tool_path.exists():
            print(f"⚠️  {tool_path.name}: File not found")
            continue
        
        print(f"Testing {tool_path.name}...", end=" ")
        success, error_type, error_msg = test_tool_help(tool_path)
        
        if success:
            categories["WORKING"].append((tool_rel, "Works with --help"))
            print("✅ WORKING")
        elif error_type == "IMPORT_ERROR":
            categories["IMPORT_ERROR"].append((tool_rel, error_msg[:200]))
            print(f"❌ IMPORT_ERROR: {error_msg[:100]}")
        elif error_type == "SYNTAX_ERROR":
            categories["SYNTAX_ERROR"].append((tool_rel, error_msg[:200]))
            print(f"❌ SYNTAX_ERROR")
        elif "usage:" in error_msg.lower() or "Usage:" in error_msg:
            categories["NO_HELP_SUPPORT"].append((tool_rel, "Doesn't support --help but shows usage"))
            print("⚠️  NO_HELP_SUPPORT")
        else:
            categories["OTHER_RUNTIME"].append((tool_rel, error_msg[:200]))
            print(f"❌ {error_type}")
    
    # Print summary
    print("\n" + "="*70)
    print("📊 RUNTIME ERROR ANALYSIS SUMMARY")
    print("="*70)
    
    for category, items in categories.items():
        if items:
            print(f"\n{category} ({len(items)}):")
            for tool_rel, msg in items[:5]:  # Show first 5
                print(f"  - {Path(tool_rel).name}: {msg[:80]}")
            if len(items) > 5:
                print(f"  ... and {len(items) - 5} more")
    
    # Save detailed results
    output_file = PROJECT_ROOT / "agent_workspaces" / "Agent-3" / "runtime_errors_analysis.json"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w') as f:
        json.dump(categories, f, indent=2)
    
    print(f"\n📄 Detailed results saved to: {output_file}")
    
    return categories


if __name__ == "__main__":
    analyze_runtime_errors()
