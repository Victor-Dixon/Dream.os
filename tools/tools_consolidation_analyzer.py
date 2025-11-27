#!/usr/bin/env python3
"""
Tools Consolidation Analyzer
============================

Analyzes tools directory to identify consolidation opportunities.
Groups tools by functionality and identifies duplicates/redundancies.

Author: Agent-8 (SSOT & System Integration Specialist)
Date: 2025-01-27
Priority: CRITICAL - Blocks Phase 1 execution
"""

import json
import re
from pathlib import Path
from typing import Any, Dict, List
from collections import defaultdict


def analyze_tool_file(tool_path: Path) -> Dict[str, Any]:
    """Analyze a single tool file."""
    try:
        content = tool_path.read_text(encoding="utf-8")
        lines = len(content.splitlines())
        
        # Extract docstring
        description = ""
        if '"""' in content:
            doc_start = content.find('"""')
            doc_end = content.find('"""', doc_start + 3)
            if doc_end > doc_start:
                description = content[doc_start + 3:doc_end].strip().split('\n')[0]
        
        # Extract key functions/classes
        functions = re.findall(r'def\s+(\w+)', content)
        classes = re.findall(r'class\s+(\w+)', content)
        
        # Categorize by keywords
        content_lower = content.lower()
        categories = []
        if any(kw in content_lower for kw in ['status', 'check', 'monitor', 'health']):
            categories.append('monitoring')
        if any(kw in content_lower for kw in ['analyze', 'scan', 'audit', 'report']):
            categories.append('analysis')
        if any(kw in content_lower for kw in ['validate', 'verify', 'check', 'test']):
            categories.append('validation')
        if any(kw in content_lower for kw in ['captain', 'coordinate', 'gas', 'fuel']):
            categories.append('captain')
        if any(kw in content_lower for kw in ['consolidation', 'merge', 'consolidate']):
            categories.append('consolidation')
        if any(kw in content_lower for kw in ['queue', 'message', 'delivery']):
            categories.append('messaging')
        if any(kw in content_lower for kw in ['automate', 'auto', 'scheduler']):
            categories.append('automation')
        
        return {
            "name": tool_path.stem,
            "path": str(tool_path),
            "lines": lines,
            "description": description[:200] if description else "No description",
            "categories": categories if categories else ["other"],
            "functions": functions[:5],  # First 5 functions
            "classes": classes,
        }
    except Exception as e:
        return {
            "name": tool_path.stem,
            "path": str(tool_path),
            "error": str(e),
        }


def group_tools_by_category(tools: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """Group tools by category."""
    grouped = defaultdict(list)
    
    for tool in tools:
        if "error" in tool:
            grouped["errors"].append(tool)
        elif "categories" in tool:
            for cat in tool["categories"]:
                grouped[cat].append(tool)
        else:
            grouped["other"].append(tool)
    
    return dict(grouped)


def identify_duplicates(tools: List[Dict[str, Any]]) -> List[List[Dict[str, Any]]]:
    """Identify potential duplicate tools."""
    duplicates = []
    seen_names = {}
    
    # Group by similar names
    name_groups = defaultdict(list)
    for tool in tools:
        if "error" in tool:
            continue
        name = tool["name"]
        # Normalize name (remove prefixes/suffixes)
        normalized = re.sub(r'^(agent_|captain_|check_|verify_|test_|validate_)', '', name.lower())
        name_groups[normalized].append(tool)
    
    # Find groups with multiple tools
    for normalized, group in name_groups.items():
        if len(group) > 1:
            duplicates.append(group)
    
    # Also check by description similarity
    desc_groups = defaultdict(list)
    for tool in tools:
        if "error" in tool or not tool.get("description"):
            continue
        desc_key = tool["description"].lower()[:50]  # First 50 chars
        desc_groups[desc_key].append(tool)
    
    for desc_key, group in desc_groups.items():
        if len(group) > 1 and group not in duplicates:
            # Check if descriptions are very similar
            if all(t.get("description", "")[:50].lower() == desc_key for t in group):
                duplicates.append(group)
    
    return duplicates


def generate_consolidation_plan(grouped: Dict[str, List], duplicates: List[List]) -> Dict[str, Any]:
    """Generate consolidation plan."""
    plan = {
        "total_tools": sum(len(tools) for tools in grouped.values()),
        "categories": {},
        "duplicates": [],
        "recommendations": [],
    }
    
    # Category analysis
    for category, tools in grouped.items():
        plan["categories"][category] = {
            "count": len(tools),
            "tools": [t["name"] for t in tools[:10]],  # First 10
            "total_lines": sum(t.get("lines", 0) for t in tools),
        }
    
    # Duplicate analysis
    for dup_group in duplicates:
        plan["duplicates"].append({
            "tools": [t["name"] for t in dup_group],
            "count": len(dup_group),
            "total_lines": sum(t.get("lines", 0) for t in dup_group),
        })
    
    # Recommendations
    for category, tools in grouped.items():
        if len(tools) > 5:
            plan["recommendations"].append({
                "category": category,
                "action": "consolidate",
                "tools_count": len(tools),
                "suggestion": f"Consider consolidating {len(tools)} {category} tools into unified implementation",
            })
    
    for dup_group in duplicates:
        if len(dup_group) > 1:
            plan["recommendations"].append({
                "action": "merge",
                "tools": [t["name"] for t in dup_group],
                "suggestion": f"Merge {len(dup_group)} duplicate tools: {', '.join([t['name'] for t in dup_group])}",
            })
    
    return plan


def main():
    """Main execution."""
    print("🔍 Tools Consolidation Analyzer - Agent-8")
    print("=" * 60)
    
    tools_dir = Path("tools")
    tools = []
    
    # Analyze all Python tools
    print("\n📋 Analyzing tools directory...")
    for tool_file in tools_dir.glob("*.py"):
        if tool_file.name.startswith("__"):
            continue
        tool_data = analyze_tool_file(tool_file)
        tools.append(tool_data)
    
    print(f"✅ Analyzed {len(tools)} tools")
    
    # Group by category
    print("\n📊 Grouping tools by category...")
    grouped = group_tools_by_category(tools)
    for category, category_tools in sorted(grouped.items()):
        print(f"  {category}: {len(category_tools)} tools")
    
    # Identify duplicates
    print("\n🔍 Identifying duplicates...")
    duplicates = identify_duplicates(tools)
    print(f"✅ Found {len(duplicates)} duplicate groups")
    for dup_group in duplicates[:5]:  # Show first 5
        print(f"  - {len(dup_group)} duplicates: {', '.join([t['name'] for t in dup_group[:3]])}")
    
    # Generate consolidation plan
    print("\n📝 Generating consolidation plan...")
    plan = generate_consolidation_plan(grouped, duplicates)
    
    # Save plan
    plan_path = Path("agent_workspaces/Agent-8/TOOLS_CONSOLIDATION_ANALYSIS.json")
    plan_path.parent.mkdir(parents=True, exist_ok=True)
    plan_path.write_text(json.dumps(plan, indent=2), encoding="utf-8")
    
    print(f"✅ Consolidation plan saved: {plan_path}")
    
    # Print summary
    print("\n📊 CONSOLIDATION SUMMARY:")
    print(f"  Total Tools: {plan['total_tools']}")
    print(f"  Categories: {len(plan['categories'])}")
    print(f"  Duplicate Groups: {len(plan['duplicates'])}")
    print(f"  Recommendations: {len(plan['recommendations'])}")
    
    print("\n🎯 TOP CONSOLIDATION OPPORTUNITIES:")
    for rec in plan["recommendations"][:10]:
        print(f"  - {rec['suggestion']}")
    
    print("\n🐝 WE. ARE. SWARM. ⚡🔥")


if __name__ == "__main__":
    main()


