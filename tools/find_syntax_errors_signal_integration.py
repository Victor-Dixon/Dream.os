#!/usr/bin/env python3
"""
Find Syntax Errors in SIGNAL Integration Tools
==============================================

Finds syntax errors in SIGNAL integration tools for Phase 0 contract.

Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2025-12-21
Task: Phase 0 - Syntax Error Fixes (Integration Tools)
"""

import ast
import json
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))


def is_integration_tool(file_path: str) -> bool:
    """Check if a tool is integration-related."""
    integration_patterns = [
        "integration",
        "integrate",
        "validator",
        "verify",
        "check",
        "coordination",
        "communication",
        "messaging",
        "orchestrator",
        "functionality",
    ]
    
    file_str = file_path.lower()
    name_str = Path(file_path).stem.lower()
    
    # Check if it's in integration-related directories
    if "integration" in file_str or "communication" in file_str or "coordination" in file_str:
        return True
    
    # Check if name contains integration patterns
    for pattern in integration_patterns:
        if pattern in name_str:
            return True
    
    return False


def main():
    """Find syntax errors in SIGNAL integration tools."""
    # Load classification
    classification_file = project_root / "tools" / "TOOL_CLASSIFICATION.json"
    
    if not classification_file.exists():
        print("❌ ERROR: TOOL_CLASSIFICATION.json not found!")
        return 1

    with open(classification_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Get SIGNAL tools with errors
    signal_tools = data.get("signal", [])
    
    # Filter to integration tools with syntax errors
    integration_with_errors = []
    
    for tool in signal_tools:
        file_path = tool.get("file", "")
        error = tool.get("error")
        
        if not file_path:
            continue
        
        # Check if it's integration-related
        if not is_integration_tool(file_path):
            continue
        
        # Check if it has a syntax error
        if error and "syntax" in str(error).lower():
            integration_with_errors.append((file_path, error))
    
    print("🔍 Finding syntax errors in SIGNAL integration tools...")
    print()
    print(f"📊 Found {len(integration_with_errors)} SIGNAL integration tools with syntax errors")
    print()
    
    if integration_with_errors:
        print("🔧 Files needing fixes:")
        for file_path, error in integration_with_errors:
            print(f"   - {file_path}")
            print(f"     {error}")
        print()
        print("=" * 60)
        print("📋 Next Steps:")
        print("   1. Fix syntax errors in listed files")
        print("   2. Verify fixes with Python parser")
        print("   3. Update status in dashboard")
    else:
        print("✅ No syntax errors found in SIGNAL integration tools!")
        print()
        print("💡 Checking all SIGNAL tools for syntax errors...")
        
        # Check all SIGNAL tools with errors
        all_signal_errors = [t for t in signal_tools if t.get("error") and "syntax" in str(t.get("error")).lower()]
        
        if all_signal_errors:
            print(f"   Found {len(all_signal_errors)} SIGNAL tools with syntax errors (not just integration):")
            for tool in all_signal_errors[:10]:
                print(f"   - {tool.get('file')}: {tool.get('error')}")
        else:
            print("   ✅ No syntax errors in any SIGNAL tools!")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

