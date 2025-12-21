#!/usr/bin/env python3
"""
Execute Consolidation Deprecations
===================================

Moves duplicate tools to deprecated directory based on consolidation recommendations.

Author: Agent-5 (Business Intelligence Specialist)
Date: 2025-12-20
V2 Compliant: Yes
"""

import shutil
from pathlib import Path
from datetime import datetime
from typing import List, Dict
import json

PROJECT_ROOT = Path(__file__).parent.parent
TOOLS_DIR = PROJECT_ROOT / "tools"
DEPRECATED_DIR = TOOLS_DIR / "deprecated"
CONSOLIDATION_DATA = PROJECT_ROOT / "agent_workspaces" / "Agent-2" / "TOOLS_CONSOLIDATION_AND_RANKING_DATA.json"


def load_consolidation_plan() -> List[Dict]:
    """Load consolidation plan from JSON data."""
    if not CONSOLIDATION_DATA.exists():
        print(f"❌ Consolidation data not found: {CONSOLIDATION_DATA}")
        return []
    
    with open(CONSOLIDATION_DATA, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    return data.get("plan", {}).get("duplicates", [])


def move_to_deprecated(tool_name: str, reason: str) -> Dict:
    """Move tool to deprecated directory."""
    source = TOOLS_DIR / f"{tool_name}.py"
    
    if not source.exists():
        return {
            "success": False,
            "error": f"Tool not found: {source}",
            "tool": tool_name
        }
    
    # Create deprecated directory if it doesn't exist
    DEPRECATED_DIR.mkdir(parents=True, exist_ok=True)
    
    # Move file
    dest = DEPRECATED_DIR / source.name
    
    try:
        # Add deprecation notice at top of file
        content = source.read_text(encoding='utf-8')
        deprecation_notice = f'''"""
⚠️  DEPRECATED TOOL ⚠️

This tool has been deprecated as part of tool consolidation.
Reason: {reason}
Deprecated: {datetime.now().strftime("%Y-%m-%d")}

DO NOT USE - Use the recommended alternative instead.
"""

'''
        # Check if already has deprecation notice
        if "DEPRECATED" not in content[:500]:
            content = deprecation_notice + content
            dest.write_text(content, encoding='utf-8')
        else:
            shutil.copy2(source, dest)
        
        # Remove original
        source.unlink()
        
        return {
            "success": True,
            "tool": tool_name,
            "source": str(source.relative_to(PROJECT_ROOT)),
            "destination": str(dest.relative_to(PROJECT_ROOT)),
            "reason": reason
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "tool": tool_name
        }


def main():
    """Main execution."""
    print("🔧 Executing Tool Consolidation Deprecations")
    print("=" * 60)
    
    # Load consolidation plan
    duplicates = load_consolidation_plan()
    
    if not duplicates:
        print("❌ No consolidation plan found")
        return 1
    
    print(f"\n📋 Found {len(duplicates)} duplicate groups to process\n")
    
    results = []
    
    for group in duplicates:
        base_name = group.get("base_name", "unknown")
        keep_tool = group.get("keep")
        deprecate_tools = group.get("deprecate", [])
        reason = group.get("reason", "Duplicate tool")
        
        print(f"📦 Processing: {base_name}")
        print(f"   Keep: {keep_tool}")
        print(f"   Deprecate: {', '.join(deprecate_tools)}")
        
        for tool_name in deprecate_tools:
            print(f"\n   Moving {tool_name} to deprecated...")
            result = move_to_deprecated(tool_name, reason)
            results.append(result)
            
            if result["success"]:
                print(f"   ✅ Moved {tool_name} to deprecated/")
            else:
                print(f"   ❌ Failed: {result.get('error', 'Unknown error')}")
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 SUMMARY:")
    successful = [r for r in results if r["success"]]
    failed = [r for r in results if not r["success"]]
    
    print(f"   ✅ Successfully deprecated: {len(successful)}")
    print(f"   ❌ Failed: {len(failed)}")
    
    if successful:
        print("\n   Deprecated tools:")
        for r in successful:
            print(f"      - {r['tool']}")
    
    if failed:
        print("\n   Failed tools:")
        for r in failed:
            print(f"      - {r['tool']}: {r.get('error', 'Unknown error')}")
    
    print("\n✅ Consolidation deprecations complete!")
    print("🐝 WE. ARE. SWARM. ⚡🔥")
    
    return 0 if len(failed) == 0 else 1


if __name__ == "__main__":
    import sys
    sys.exit(main())


