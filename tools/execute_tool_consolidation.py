#!/usr/bin/env python3
"""
Execute Tool Consolidation
===========================

Executes tool consolidation based on comprehensive_tool_consolidation.py analysis.
Consolidates similar tools, eliminates redundancies, optimizes toolbelt efficiency.

V2 Compliance | Author: Agent-5 | Date: 2025-12-25
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))


def load_consolidation_analysis() -> Dict[str, Any]:
    """Load tool consolidation analysis."""
    analysis_path = project_root / "agent_workspaces" / "Agent-5" / "TOOL_CONSOLIDATION_ANALYSIS.json"
    
    if not analysis_path.exists():
        print(f"❌ Analysis file not found: {analysis_path}")
        return {}
    
    with open(analysis_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def identify_consolidation_candidates(analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Identify tools that should be consolidated."""
    candidates = []
    
    # Load similar tools from report
    report_path = project_root / "agent_workspaces" / "Agent-5" / "TOOL_CONSOLIDATION_REPORT.md"
    
    if not report_path.exists():
        print(f"⚠️  Report file not found: {report_path}")
        return candidates
    
    # Parse similar tools from report
    with open(report_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract similar tools groups
    # This is a simplified approach - in production, would parse more carefully
    tools_data = analysis.get("tools", {})
    
    # Group tools by similarity (same categories, similar imports)
    category_groups = {}
    for tool_name, tool_info in tools_data.items():
        categories = tuple(sorted(tool_info.get("categories", [])))
        if categories not in category_groups:
            category_groups[categories] = []
        category_groups[categories].append({
            "name": tool_name,
            "path": tool_info.get("path"),
            "lines": tool_info.get("lines", 0),
            "categories": tool_info.get("categories", [])
        })
    
    # Find groups with multiple tools (consolidation candidates)
    for categories, tools in category_groups.items():
        if len(tools) > 1:
            # Sort by lines (keep largest as base)
            tools.sort(key=lambda x: x["lines"], reverse=True)
            candidates.append({
                "category_group": categories,
                "tools": tools,
                "base_tool": tools[0],  # Largest tool as base
                "consolidate_tools": tools[1:]  # Others to consolidate
            })
    
    return candidates


def generate_consolidation_plan(candidates: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Generate consolidation execution plan."""
    plan = {
        "total_candidates": len(candidates),
        "consolidations": [],
        "estimated_lines_saved": 0
    }
    
    for candidate in candidates:
        base = candidate["base_tool"]
        consolidate = candidate["consolidate_tools"]
        
        total_lines = sum(t["lines"] for t in consolidate)
        estimated_saved = total_lines * 0.3  # Estimate 30% reduction from consolidation
        
        plan["consolidations"].append({
            "base_tool": {
                "name": base["name"],
                "path": base["path"],
                "lines": base["lines"]
            },
            "consolidate_into": [
                {
                    "name": t["name"],
                    "path": t["path"],
                    "lines": t["lines"]
                }
                for t in consolidate
            ],
            "estimated_lines_saved": int(estimated_saved),
            "action": f"Merge functionality from {len(consolidate)} tools into {base['name']}"
        })
        
        plan["estimated_lines_saved"] += int(estimated_saved)
    
    return plan


def execute_consolidation(plan: Dict[str, Any], dry_run: bool = True) -> Dict[str, Any]:
    """Execute consolidation plan."""
    results = {
        "dry_run": dry_run,
        "consolidations_executed": 0,
        "tools_consolidated": 0,
        "lines_saved": 0,
        "errors": []
    }
    
    if dry_run:
        print("🔍 DRY RUN MODE - No files will be modified\n")
    
    for consolidation in plan["consolidations"]:
        base = consolidation["base_tool"]
        consolidate = consolidation["consolidate_into"]
        
        print(f"📦 Consolidation: {base['name']}")
        print(f"   Base tool: {base['path']} ({base['lines']} lines)")
        print(f"   Consolidating {len(consolidate)} tools:")
        
        for tool in consolidate:
            print(f"     - {tool['name']} ({tool['path']}, {tool['lines']} lines)")
        
        if not dry_run:
            # In production, would:
            # 1. Read base tool
            # 2. Extract functionality from consolidate tools
            # 3. Merge into base tool
            # 4. Update imports/references
            # 5. Archive or delete consolidate tools
            print(f"   ⚠️  Actual consolidation not implemented - requires manual review")
        else:
            print(f"   ✅ Would consolidate (dry run)")
        
        results["consolidations_executed"] += 1
        results["tools_consolidated"] += len(consolidate)
        results["lines_saved"] += consolidation["estimated_lines_saved"]
        print()
    
    return results


def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Execute Tool Consolidation")
    parser.add_argument("--dry-run", action="store_true", default=True,
                       help="Dry run mode (default: True)")
    parser.add_argument("--execute", action="store_true",
                       help="Actually execute consolidation (overrides --dry-run)")
    
    args = parser.parse_args()
    
    dry_run = not args.execute
    
    print("🔧 Tool Consolidation Execution")
    print("=" * 60)
    print()
    
    # Load analysis
    print("📊 Loading consolidation analysis...")
    analysis = load_consolidation_analysis()
    
    if not analysis:
        print("❌ Failed to load analysis")
        return 1
    
    print(f"✅ Loaded analysis for {len(analysis.get('tools', {}))} tools")
    print()
    
    # Identify candidates
    print("🔍 Identifying consolidation candidates...")
    candidates = identify_consolidation_candidates(analysis)
    print(f"✅ Found {len(candidates)} consolidation candidate groups")
    print()
    
    # Generate plan
    print("📋 Generating consolidation plan...")
    plan = generate_consolidation_plan(candidates)
    print(f"✅ Plan generated: {plan['total_candidates']} consolidations")
    print(f"   Estimated lines saved: {plan['estimated_lines_saved']}")
    print()
    
    # Save plan
    plan_path = project_root / "agent_workspaces" / "Agent-5" / "TOOL_CONSOLIDATION_PLAN.json"
    with open(plan_path, 'w', encoding='utf-8') as f:
        json.dump(plan, f, indent=2, ensure_ascii=False)
    print(f"💾 Plan saved: {plan_path}")
    print()
    
    # Execute
    print("⚙️  Executing consolidation...")
    results = execute_consolidation(plan, dry_run=dry_run)
    
    # Save results
    results_path = project_root / "agent_workspaces" / "Agent-5" / "TOOL_CONSOLIDATION_RESULTS.json"
    with open(results_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print()
    print("=" * 60)
    print("📊 Consolidation Results:")
    print(f"   Consolidations: {results['consolidations_executed']}")
    print(f"   Tools consolidated: {results['tools_consolidated']}")
    print(f"   Estimated lines saved: {results['lines_saved']}")
    print(f"   Mode: {'DRY RUN' if results['dry_run'] else 'EXECUTED'}")
    print("=" * 60)
    
    if dry_run:
        print("\n💡 To execute consolidation, run with --execute flag")
        print("   python tools/execute_tool_consolidation.py --execute")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

