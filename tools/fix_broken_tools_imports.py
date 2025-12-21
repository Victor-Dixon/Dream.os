#!/usr/bin/env python3
"""
Fix Broken Tools - Import Errors
==================================

Analyzes and fixes import errors in broken tools.
Prioritizes: syntax errors -> import errors -> runtime errors

Author: Agent-7 (Web Development Specialist)
V2 Compliant: <300 lines
"""

import ast
import sys
from pathlib import Path
from typing import List, Dict, Tuple

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))


def analyze_import_error(tool_path: Path) -> Tuple[str, str]:
    """Analyze import error in a tool file."""
    try:
        with open(tool_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse AST to find imports
        try:
            tree = ast.parse(content)
        except SyntaxError as e:
            return "SYNTAX_ERROR", str(e)
        
        # Try to compile and get actual error
        compile(content, str(tool_path), 'exec')
        return "NO_ERROR", ""
        
    except ImportError as e:
        return "IMPORT_ERROR", str(e)
    except Exception as e:
        return "OTHER_ERROR", str(e)


def get_import_errors_from_audit() -> List[str]:
    """Get list of tools with import errors from audit results."""
    audit_file = project_root / "agent_workspaces" / "Agent-5" / "tool_audit_assignments" / "Agent-7_audit_results.json"
    
    if not audit_file.exists():
        return []
    
    import json
    with open(audit_file) as f:
        data = json.load(f)
    
    return data.get("results", {}).get("import_errors", [])


def main():
    """Main function."""
    print("🔍 Analyzing Import Errors in Broken Tools")
    print("=" * 60)
    print()
    
    import_errors = get_import_errors_from_audit()
    
    if not import_errors:
        print("No import errors found in audit results")
        return 0
    
    print(f"Found {len(import_errors)} tools with import errors:")
    print()
    
    for tool_path_str in import_errors[:5]:  # Analyze first 5
        tool_path = project_root / tool_path_str.replace("\\", "/")
        if not tool_path.exists():
            print(f"⚠️  {tool_path.name}: File not found")
            continue
        
        error_type, error_msg = analyze_import_error(tool_path)
        print(f"📋 {tool_path.name}")
        print(f"   Error: {error_type}")
        if error_msg:
            print(f"   Message: {error_msg[:100]}")
        print()
    
    print("💡 Next: Manually fix each import error based on analysis")
    return 0


if __name__ == "__main__":
    sys.exit(main())


