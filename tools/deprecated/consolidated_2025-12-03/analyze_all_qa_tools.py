#!/usr/bin/env python3
"""
Analyze ALL QA Tools for Phase 2 Consolidation
===============================================

Analyzes ALL tools (not just validation category) related to QA, testing, 
quality standards, and coverage. Identifies consolidation patterns.

Author: Agent-8 (Testing & Quality Assurance Specialist)
Date: 2025-12-03
"""

import json
import sys
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Any

PROJECT_ROOT = Path(__file__).parent.parent


def load_all_tools() -> List[Dict[str, Any]]:
    """Load all tools from consolidation candidates."""
    candidates_file = PROJECT_ROOT / "agent_workspaces" / "Agent-8" / "CONSOLIDATION_CANDIDATES_PHASE2.json"
    
    if not candidates_file.exists():
        print(f"❌ Candidates file not found: {candidates_file}")
        sys.exit(1)
    
    with open(candidates_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Get all tools from all categories
    all_tools = []
    for category in ['monitoring', 'validation', 'analysis']:
        all_tools.extend(data.get(category, []))
    
    return all_tools


def is_qa_tool(tool: Dict[str, Any]) -> bool:
    """Check if tool is QA/validation/testing related."""
    name = tool.get('name', '').lower()
    path = tool.get('path', '').lower()
    
    qa_keywords = [
        'valid', 'verify', 'check', 'test', 'qa', 'coverage', 
        'quality', 'ssot', 'import', 'chain', 'config',
        'tracker', 'analyzer', 'prioritizer', 'gap', 'infrastructure'
    ]
    
    # Check name and path
    name_match = any(keyword in name for keyword in qa_keywords)
    path_match = any(keyword in path for keyword in qa_keywords)
    
    # Also check if it's a test infrastructure tool
    test_infrastructure = (
        'test' in name and any(x in name for x in ['tracker', 'analyzer', 'prioritizer', 'coverage', 'gap']) or
        'coverage' in name or
        'quality' in name or
        'qa' in name
    )
    
    return name_match or path_match or test_infrastructure


def categorize_qa_tools(tools: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """Categorize QA tools by pattern."""
    categories = defaultdict(list)
    
    for tool in tools:
        name = tool.get('name', '').lower()
        path = tool.get('path', '').lower()
        category = tool.get('category', '')
        
        # SSOT Validation
        if 'ssot' in name and 'valid' in name:
            categories['ssot_validation'].append(tool)
        # Import/Chain Validation
        elif 'import' in name and ('valid' in name or 'chain' in name):
            categories['import_validation'].append(tool)
        # Config Validation
        elif 'config' in name and 'valid' in name:
            categories['config_validation'].append(tool)
        # Test Coverage Tools
        elif 'coverage' in name or ('test' in name and 'coverage' in path):
            categories['test_coverage'].append(tool)
        # Test Infrastructure (trackers, analyzers, prioritizers)
        elif 'test' in name and any(x in name for x in ['tracker', 'analyzer', 'prioritizer', 'gap']):
            categories['test_infrastructure'].append(tool)
        # Quality Standards
        elif 'quality' in name or 'qa' in name:
            categories['quality_standards'].append(tool)
        # General Validation
        elif 'valid' in name or 'verify' in name:
            categories['general_validation'].append(tool)
        # Health Checks
        elif 'check' in name or 'health' in name:
            categories['health_checks'].append(tool)
        # Test-related (but not infrastructure)
        elif 'test' in name and category == 'analysis':
            categories['test_analysis'].append(tool)
        else:
            categories['other_qa'].append(tool)
    
    return dict(categories)


def analyze_all_qa_tools():
    """Main analysis function."""
    print("🔍 Analyzing ALL QA Tools for Phase 2 Consolidation\n")
    
    # Load all tools
    all_tools = load_all_tools()
    print(f"📊 Total tools analyzed: {len(all_tools)}")
    
    # Filter QA-related tools
    qa_tools = [t for t in all_tools if is_qa_tool(t)]
    print(f"✅ QA-related tools found: {len(qa_tools)}\n")
    
    # Categorize
    categories = categorize_qa_tools(qa_tools)
    
    # Print categories
    print("📋 QA Tool Categories:\n")
    total_in_categories = 0
    for category, tools in sorted(categories.items()):
        print(f"  {category.upper().replace('_', ' ')}: {len(tools)} tools")
        for tool in tools[:5]:  # Show first 5
            print(f"    - {tool['name']} ({tool.get('lines', 0)} lines, {tool.get('category', 'unknown')})")
        if len(tools) > 5:
            print(f"    ... and {len(tools) - 5} more")
        print()
        total_in_categories += len(tools)
    
    print(f"📊 Total tools in categories: {total_in_categories}\n")
    
    # Consolidation recommendations
    print("\n🎯 Consolidation Recommendations:\n")
    
    core_tools = []
    
    # SSOT Validation → unified_ssot_validator.py
    if categories.get('ssot_validation'):
        core_tools.append({
            'name': 'unified_ssot_validator.py',
            'category': 'SSOT Validation',
            'consolidates': len(categories['ssot_validation']),
            'tools': [t['name'] for t in categories['ssot_validation']],
            'existing': 'ssot_validator.py, ssot_config_validator.py'
        })
    
    # Import Validation → import_chain_validator.py (enhance)
    if categories.get('import_validation'):
        core_tools.append({
            'name': 'import_chain_validator.py (enhance)',
            'category': 'Import Validation',
            'consolidates': len(categories['import_validation']),
            'tools': [t['name'] for t in categories['import_validation']],
            'existing': 'import_chain_validator.py, captain_import_validator.py'
        })
    
    # Config Validation → ssot_config_validator.py (enhance)
    if categories.get('config_validation'):
        core_tools.append({
            'name': 'ssot_config_validator.py (enhance)',
            'category': 'Config Validation',
            'consolidates': len(categories['config_validation']),
            'tools': [t['name'] for t in categories['config_validation']],
            'existing': 'ssot_config_validator.py'
        })
    
    # Test Coverage → unified_test_coverage.py
    if categories.get('test_coverage'):
        core_tools.append({
            'name': 'unified_test_coverage.py',
            'category': 'Test Coverage',
            'consolidates': len(categories['test_coverage']),
            'tools': [t['name'] for t in categories['test_coverage']],
            'existing': 'test_coverage_tracker.py, test_coverage_prioritizer.py, analyze_test_coverage_gaps_clean.py'
        })
    
    # Test Infrastructure → unified_test_infrastructure.py
    if categories.get('test_infrastructure'):
        core_tools.append({
            'name': 'unified_test_infrastructure.py',
            'category': 'Test Infrastructure',
            'consolidates': len(categories['test_infrastructure']),
            'tools': [t['name'] for t in categories['test_infrastructure']],
            'existing': 'test_coverage_tracker.py, test_coverage_prioritizer.py'
        })
    
    # General Validation → unified_validator.py (enhance)
    if categories.get('general_validation'):
        core_tools.append({
            'name': 'unified_validator.py (enhance)',
            'category': 'General Validation',
            'consolidates': len(categories['general_validation']),
            'tools': [t['name'] for t in categories['general_validation']],
            'existing': 'unified_validator.py'
        })
    
    # Test Analysis → unified_test_analysis.py
    if categories.get('test_analysis'):
        core_tools.append({
            'name': 'unified_test_analysis.py',
            'category': 'Test Analysis',
            'consolidates': len(categories['test_analysis']),
            'tools': [t['name'] for t in categories['test_analysis']],
            'existing': None
        })
    
    print("  Core Tools to Create/Enhance:\n")
    for tool in core_tools:
        print(f"  ✅ {tool['name']}")
        print(f"     Category: {tool['category']}")
        print(f"     Consolidates: {tool['consolidates']} tools")
        if tool['existing']:
            print(f"     Existing: {tool['existing']}")
        print(f"     Sample tools: {', '.join(tool['tools'][:3])}")
        if len(tool['tools']) > 3:
            print(f"     ... and {len(tool['tools']) - 3} more")
        print()
    
    total_consolidated = sum(t['consolidates'] for t in core_tools)
    print(f"📊 Total tools to consolidate: {total_consolidated}")
    print(f"📊 Target core tools: {len(core_tools)}")
    if total_consolidated > 0:
        reduction = 100 * (1 - len(core_tools) / total_consolidated)
        print(f"📊 Reduction: {total_consolidated} → {len(core_tools)} ({reduction:.1f}% reduction)\n")
    
    # Save analysis
    output_file = PROJECT_ROOT / "agent_workspaces" / "Agent-8" / "QA_TOOLS_COMPREHENSIVE_ANALYSIS.json"
    analysis = {
        'total_tools_analyzed': len(all_tools),
        'qa_tools_found': len(qa_tools),
        'categories': {
            cat: [{'name': t['name'], 'path': t['path'], 'lines': t.get('lines', 0), 'category': t.get('category', '')} 
                  for t in tools]
            for cat, tools in categories.items()
        },
        'core_tools': core_tools,
        'consolidation_summary': {
            'total_tools': total_consolidated,
            'target_core_tools': len(core_tools),
            'reduction_percentage': 100 * (1 - len(core_tools) / total_consolidated) if total_consolidated > 0 else 0
        }
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(analysis, f, indent=2)
    
    print(f"✅ Comprehensive analysis saved to: {output_file}")
    
    return analysis


if __name__ == '__main__':
    analyze_all_qa_tools()

