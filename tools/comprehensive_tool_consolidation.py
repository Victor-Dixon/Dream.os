#!/usr/bin/env python3
"""
Comprehensive Tool Consolidation
=================================

Analyzes and consolidates tools in the repository:
- Identifies duplicate/similar tools
- Consolidates functionality
- Updates references
- Generates consolidation report

Author: Agent-5 (Business Intelligence Specialist)
V2 Compliant: <400 lines
"""

import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Set, Tuple


def analyze_tools() -> Dict:
    """Analyze all tools in the tools directory."""
    repo_root = Path(__file__).parent.parent
    tools_dir = repo_root / "tools"
    
    tools = {}
    duplicates = defaultdict(list)
    similar_tools = defaultdict(list)
    
    # Pattern matching for similar functionality
    patterns = {
        'audit': ['audit', 'check', 'verify', 'validate'],
        'consolidate': ['consolidate', 'merge', 'combine'],
        'website': ['website', 'site', 'web'],
        'pr': ['pr', 'pull', 'merge'],
        'queue': ['queue', 'message'],
        'discord': ['discord', 'bot'],
        'twitch': ['twitch', 'chat'],
    }
    
    print("🔍 Analyzing tools...")
    print("=" * 70)
    
    for tool_file in sorted(tools_dir.rglob("*.py")):
        if tool_file.name.startswith("__") or tool_file.name.startswith("test_"):
            continue
        
        rel_path = tool_file.relative_to(tools_dir)
        tool_name = tool_file.stem
        
        # Read file to analyze
        try:
            content = tool_file.read_text(encoding='utf-8')
            
            # Extract docstring
            doc_match = re.search(r'"""(.*?)"""', content, re.DOTALL)
            docstring = doc_match.group(1).strip() if doc_match else ""
            
            # Extract imports
            imports = re.findall(r'^(?:from|import)\s+(\S+)', content, re.MULTILINE)
            
            # Categorize by patterns
            categories = []
            content_lower = content.lower()
            for category, keywords in patterns.items():
                if any(kw in content_lower for kw in keywords):
                    categories.append(category)
            
            tools[tool_name] = {
                'path': str(rel_path),
                'full_path': str(tool_file),
                'docstring': docstring[:200] if docstring else "",
                'imports': imports[:10],  # Limit imports
                'categories': categories,
                'size': len(content),
                'lines': len(content.splitlines()),
            }
            
            # Check for duplicate names (different locations)
            if tool_name in tools and tools[tool_name]['path'] != str(rel_path):
                duplicates[tool_name].append(str(rel_path))
            
        except Exception as e:
            print(f"   ⚠️  Error reading {tool_file}: {e}")
    
    # Find similar tools by category overlap
    for tool_name, tool_data in tools.items():
        for other_name, other_data in tools.items():
            if tool_name == other_name:
                continue
            
            # Check category overlap
            common_categories = set(tool_data['categories']) & set(other_data['categories'])
            if len(common_categories) >= 2:
                similar_tools[tool_name].append({
                    'name': other_name,
                    'common_categories': list(common_categories),
                })
    
    return {
        'tools': tools,
        'duplicates': dict(duplicates),
        'similar_tools': dict(similar_tools),
        'total_tools': len(tools),
    }


def generate_consolidation_report(analysis: Dict) -> str:
    """Generate consolidation report."""
    report = []
    report.append("=" * 70)
    report.append("📊 COMPREHENSIVE TOOL CONSOLIDATION REPORT")
    report.append("=" * 70)
    report.append("")
    
    report.append(f"Total Tools Analyzed: {analysis['total_tools']}")
    report.append("")
    
    # Duplicates section
    if analysis['duplicates']:
        report.append("🔴 DUPLICATE TOOLS FOUND:")
        report.append("-" * 70)
        for name, paths in analysis['duplicates'].items():
            report.append(f"  {name}:")
            for path in paths:
                report.append(f"    - {path}")
        report.append("")
    else:
        report.append("✅ No duplicate tool names found")
        report.append("")
    
    # Similar tools section
    if analysis['similar_tools']:
        report.append("⚠️  SIMILAR TOOLS (Potential Consolidation Candidates):")
        report.append("-" * 70)
        for tool_name, similar in list(analysis['similar_tools'].items())[:20]:  # Limit output
            if similar:
                report.append(f"  {tool_name}:")
                for sim in similar[:3]:  # Limit per tool
                    report.append(f"    - {sim['name']} (common: {', '.join(sim['common_categories'])})")
        report.append("")
    
    # Category breakdown
    category_count = defaultdict(int)
    for tool_data in analysis['tools'].values():
        for cat in tool_data['categories']:
            category_count[cat] += 1
    
    if category_count:
        report.append("📁 TOOLS BY CATEGORY:")
        report.append("-" * 70)
        for cat, count in sorted(category_count.items(), key=lambda x: -x[1]):
            report.append(f"  {cat}: {count} tools")
        report.append("")
    
    # Large tools (potential refactoring candidates)
    large_tools = sorted(
        [(name, data['lines']) for name, data in analysis['tools'].items()],
        key=lambda x: -x[1]
    )[:10]
    
    if large_tools:
        report.append("📏 LARGEST TOOLS (V2 Compliance Check):")
        report.append("-" * 70)
        for name, lines in large_tools:
            if lines > 400:
                report.append(f"  ⚠️  {name}: {lines} lines (exceeds 400 line limit)")
            else:
                report.append(f"  ✅ {name}: {lines} lines")
        report.append("")
    
    report.append("=" * 70)
    report.append("💡 RECOMMENDATIONS:")
    report.append("-" * 70)
    report.append("1. Review similar tools for consolidation opportunities")
    report.append("2. Refactor tools exceeding 400 lines (V2 compliance)")
    report.append("3. Update documentation for consolidated tools")
    report.append("4. Remove deprecated/duplicate tools")
    report.append("=" * 70)
    
    return "\n".join(report)


def save_analysis(analysis: Dict, output_path: Path):
    """Save analysis to JSON file."""
    # Convert Path objects to strings for JSON serialization
    json_data = {
        'tools': {
            name: {
                k: v for k, v in data.items() if k != 'full_path'
            }
            for name, data in analysis['tools'].items()
        },
        'duplicates': analysis['duplicates'],
        'similar_tools': analysis['similar_tools'],
        'total_tools': analysis['total_tools'],
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)


def main():
    """Main consolidation analysis."""
    repo_root = Path(__file__).parent.parent
    output_dir = repo_root / "agent_workspaces" / "Agent-5"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("🔧 COMPREHENSIVE TOOL CONSOLIDATION")
    print("=" * 70)
    print()
    
    # Analyze tools
    analysis = analyze_tools()
    
    # Generate report
    report = generate_consolidation_report(analysis)
    print(report)
    
    # Save results
    report_file = output_dir / "TOOL_CONSOLIDATION_REPORT.md"
    analysis_file = output_dir / "TOOL_CONSOLIDATION_ANALYSIS.json"
    
    report_file.write_text(report, encoding='utf-8')
    save_analysis(analysis, analysis_file)
    
    print()
    print(f"✅ Report saved: {report_file}")
    print(f"✅ Analysis saved: {analysis_file}")
    print()
    print("💡 Next steps:")
    print("   1. Review the consolidation report")
    print("   2. Identify tools to consolidate")
    print("   3. Create consolidation plan")
    print("   4. Execute consolidation")


if __name__ == "__main__":
    main()

