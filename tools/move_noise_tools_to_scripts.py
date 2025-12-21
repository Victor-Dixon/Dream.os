#!/usr/bin/env python3
"""
Move NOISE Tools to Scripts Directory
======================================

Moves all NOISE tools (thin wrappers) from tools/ to scripts/ directory.

Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2025-12-21
Task: Phase -1 of V2 Compliance Refactoring Plan
"""

import json
import shutil
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))


def main():
    """Move NOISE tools to scripts directory."""
    # Load classification
    classification_file = project_root / "tools" / "TOOL_CLASSIFICATION.json"
    
    if not classification_file.exists():
        print("❌ ERROR: TOOL_CLASSIFICATION.json not found!")
        print("   Run classify_all_tools_phase1.py first")
        return 1

    with open(classification_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Get NOISE tools - handle different JSON structures
    noise_tools = []
    if "noise" in data:
        noise_tools = data["noise"]
    elif "by_classification" in data and "NOISE" in data["by_classification"]:
        noise_tools = data["by_classification"]["NOISE"]
    elif "classifications" in data:
        # Filter classifications for NOISE
        noise_tools = [
            {"file": k, **v} for k, v in data["classifications"].items()
            if v.get("classification") == "NOISE"
        ]
    
    if not noise_tools:
        print("⚠️  No NOISE tools found in classification")
        return 0

    print(f"🚀 Moving {len(noise_tools)} NOISE tools to scripts/...")
    print()

    scripts_dir = project_root / "scripts"
    scripts_dir.mkdir(exist_ok=True)

    moved = []
    skipped = []
    errors = []

    for tool in noise_tools:
        # Handle different tool object structures
        if isinstance(tool, str):
            tool_file = tool
        elif isinstance(tool, dict):
            tool_file = tool.get("file", "")
        else:
            continue
            
        if not tool_file:
            continue

        source_path = project_root / tool_file.replace("\\", "/")
        
        if not source_path.exists():
            skipped.append((tool_file, "File not found"))
            continue

        # Determine destination
        if tool_file.startswith("tools/"):
            dest_path = scripts_dir / source_path.name
        else:
            # Preserve subdirectory structure if any
            rel_path = source_path.relative_to(project_root / "tools")
            dest_path = scripts_dir / rel_path

        # Create parent directories if needed
        dest_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            # Move file
            shutil.move(str(source_path), str(dest_path))
            moved.append((tool_file, str(dest_path.relative_to(project_root))))
            
            if len(moved) % 10 == 0:
                print(f"   Moved {len(moved)}/{len(noise_tools)} tools...")

        except Exception as e:
            errors.append((tool_file, str(e)))

    print()
    print("=" * 60)
    print("📊 Move Summary")
    print("=" * 60)
    print(f"   ✅ Moved: {len(moved)}")
    print(f"   ⚠️  Skipped: {len(skipped)}")
    print(f"   ❌ Errors: {len(errors)}")
    print()

    if moved:
        print("✅ Successfully moved tools:")
        for source, dest in moved[:10]:  # Show first 10
            print(f"   {source} → {dest}")
        if len(moved) > 10:
            print(f"   ... and {len(moved) - 10} more")

    if skipped:
        print()
        print("⚠️  Skipped tools:")
        for tool, reason in skipped[:5]:
            print(f"   {tool}: {reason}")

    if errors:
        print()
        print("❌ Errors:")
        for tool, error in errors:
            print(f"   {tool}: {error}")

    print()
    print("📋 Next Steps:")
    print("   1. Update toolbelt registry (remove NOISE tools)")
    print("   2. Update compliance baseline (remove NOISE from denominator)")
    print("   3. Verify moved tools in scripts/")
    print()

    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())

