#!/usr/bin/env python3
"""
Identify Analytics Analysis Tools
=================================

Identifies analysis tools related to analytics, metrics, BI systems, and reporting.

Author: Agent-5 (Business Intelligence Specialist)
Date: 2025-12-03
"""

import json
import re
from pathlib import Path
from typing import List, Dict, Any

# Keywords for analytics/metrics/BI/reporting
ANALYTICS_KEYWORDS = [
    'metric', 'analytics', 'report', 'dashboard', 'tracker', 
    'bi', 'business intelligence', 'technical debt', 'debt',
    'coverage', 'analysis', 'analyze', 'insight', 'statistic',
    'measure', 'monitor', 'performance', 'trend', 'data'
]

def load_consolidation_analysis() -> Dict[str, Any]:
    """Load tools consolidation analysis."""
    analysis_path = Path("agent_workspaces/Agent-8/TOOLS_CONSOLIDATION_ANALYSIS.json")
    if not analysis_path.exists():
        return {}
    
    with open(analysis_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def analyze_tool_file(tool_path: Path) -> Dict[str, Any]:
    """Analyze a single tool file for analytics content."""
    try:
        content = tool_path.read_text(encoding='utf-8', errors='ignore')
        content_lower = content.lower()
        
        # Check for analytics keywords
        matches = []
        for keyword in ANALYTICS_KEYWORDS:
            if keyword in content_lower:
                matches.append(keyword)
        
        # Extract description
        description = ""
        if '"""' in content:
            doc_start = content.find('"""')
            doc_end = content.find('"""', doc_start + 3)
            if doc_end > doc_start:
                description = content[doc_start + 3:doc_end].strip().split('\n')[0]
        
        return {
            "name": tool_path.stem,
            "path": str(tool_path),
            "description": description[:200] if description else "",
            "analytics_keywords": matches,
            "is_analytics_tool": len(matches) >= 2,  # At least 2 keywords
        }
    except Exception as e:
        return {
            "name": tool_path.stem,
            "path": str(tool_path),
            "error": str(e),
            "is_analytics_tool": False
        }

def find_analytics_analysis_tools() -> List[Dict[str, Any]]:
    """Find all analytics-related analysis tools."""
    tools_dir = Path("tools")
    analytics_tools = []
    
    # Get all Python files in tools directory
    for tool_file in tools_dir.rglob("*.py"):
        # Skip deprecated and __pycache__
        if "deprecated" in str(tool_file) or "__pycache__" in str(tool_file):
            continue
        
        # Check if it's an analysis tool (has 'analyze' or 'analysis' in name/description)
        tool_name_lower = tool_file.stem.lower()
        if 'analyze' in tool_name_lower or 'analysis' in tool_name_lower:
            tool_info = analyze_tool_file(tool_file)
            if tool_info.get("is_analytics_tool", False):
                analytics_tools.append(tool_info)
    
    return analytics_tools

def main():
    """Main entry point."""
    print("🔍 Identifying Analytics Analysis Tools...")
    print("=" * 60)
    
    analytics_tools = find_analytics_analysis_tools()
    
    print(f"\n✅ Found {len(analytics_tools)} analytics-related analysis tools\n")
    
    # Group by keywords
    by_keyword = {}
    for tool in analytics_tools:
        for keyword in tool.get("analytics_keywords", []):
            if keyword not in by_keyword:
                by_keyword[keyword] = []
            by_keyword[keyword].append(tool["name"])
    
    print("📊 Tools by Keyword:")
    for keyword, tools in sorted(by_keyword.items(), key=lambda x: len(x[1]), reverse=True):
        print(f"  {keyword}: {len(tools)} tools")
    
    print("\n📋 Analytics Analysis Tools:")
    for tool in sorted(analytics_tools, key=lambda x: x["name"]):
        print(f"  - {tool['name']}")
        if tool.get("description"):
            print(f"    {tool['description'][:80]}")
        print(f"    Keywords: {', '.join(tool.get('analytics_keywords', [])[:5])}")
        print()
    
    # Save results
    output_path = Path("agent_workspaces/Agent-5/ANALYTICS_ANALYSIS_TOOLS.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump({
            "total_tools": len(analytics_tools),
            "tools": analytics_tools,
            "by_keyword": by_keyword
        }, f, indent=2)
    
    print(f"✅ Results saved to: {output_path}")

if __name__ == "__main__":
    main()


