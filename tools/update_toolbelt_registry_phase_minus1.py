#!/usr/bin/env python3
"""
Phase -1: Update Toolbelt Registry - Remove NOISE Tools
========================================================

Updates toolbelt_registry.py to remove NOISE tools that have been moved to scripts/.
Documents any NOISE tools that were in the registry.

Author: Agent-4 (Captain - Strategic Oversight)
Date: 2025-12-21
"""

import json
import re
from pathlib import Path

# NOISE tools from Phase -1 classification
NOISE_TOOLS = [
    "activate_wordpress_theme.py",
    "captain_update_log.py",
    "check_dashboard_page.py",
    "check_keyboard_lock_status.py",
    "detect_comment_code_mismatches.py",
    "extract_freeride_error.py",
    "extract_integration_files.py",
    "thea/run_headless_refresh.py",
]

def check_noise_tools_in_registry():
    """Check which NOISE tools are referenced in toolbelt registry."""
    registry_path = Path("tools/toolbelt_registry.py")
    
    if not registry_path.exists():
        print(f"❌ Registry file not found: {registry_path}")
        return
    
    with open(registry_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check each NOISE tool
    found_in_registry = []
    for noise_tool in NOISE_TOOLS:
        # Check for module references (tools.filename or tools.path.filename)
        tool_name = Path(noise_tool).stem
        patterns = [
            rf'tools\.{re.escape(tool_name)}',
            rf'"module":\s*"tools\.{re.escape(tool_name)}"',
            rf"'module':\s*'tools\.{re.escape(tool_name)}'",
            rf'"{re.escape(tool_name)}"',
            rf"'{re.escape(tool_name)}'",
        ]
        
        for pattern in patterns:
            if re.search(pattern, content, re.IGNORECASE):
                found_in_registry.append(noise_tool)
                break
    
    # Also check for commented-out references
    commented_out = []
    for noise_tool in NOISE_TOOLS:
        tool_name = Path(noise_tool).stem
        # Check if commented out
        commented_pattern = rf'#.*{re.escape(tool_name)}'
        if re.search(commented_pattern, content, re.IGNORECASE):
            commented_out.append(noise_tool)
    
    print("=" * 60)
    print("NOISE Tools Registry Check - Phase -1")
    print("=" * 60)
    print(f"\n✅ Total NOISE tools identified: {len(NOISE_TOOLS)}")
    print(f"📋 Found in registry (active): {len(found_in_registry)}")
    print(f"💬 Found in registry (commented): {len(commented_out)}")
    
    if found_in_registry:
        print(f"\n⚠️  NOISE tools found in registry (should be removed):")
        for tool in found_in_registry:
            print(f"   - {tool}")
    else:
        print("\n✅ No NOISE tools found actively registered in toolbelt registry!")
    
    if commented_out:
        print(f"\n💬 NOISE tools already commented out (good):")
        for tool in commented_out:
            print(f"   - {tool}")
    
    # Check if tools exist in scripts/
    scripts_dir = Path("scripts")
    if scripts_dir.exists():
        moved_to_scripts = []
        for noise_tool in NOISE_TOOLS:
            tool_filename = Path(noise_tool).name
            script_path = scripts_dir / tool_filename
            if script_path.exists():
                moved_to_scripts.append(noise_tool)
        
        print(f"\n✅ NOISE tools moved to scripts/: {len(moved_to_scripts)}/{len(NOISE_TOOLS)}")
        if moved_to_scripts:
            for tool in moved_to_scripts:
                print(f"   - {tool} → scripts/{Path(tool).name}")
    
    print("\n" + "=" * 60)
    print("SUMMARY:")
    print("=" * 60)
    
    if found_in_registry:
        print("❌ ACTION REQUIRED: Remove NOISE tools from registry")
        print("   These tools should be removed or commented out.")
    else:
        print("✅ Registry is clean - No NOISE tools actively registered")
        print("   All NOISE tools have been moved to scripts/ and removed from registry.")
    
    print("\n✅ Phase -1 Toolbelt Registry Check: COMPLETE")
    print("   Next: Proceed with Phase 0 (Syntax Error Fixes)")

if __name__ == "__main__":
    check_noise_tools_in_registry()

