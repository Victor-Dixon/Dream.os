#!/usr/bin/env python3
"""
Analyze QA Validation Tools for Phase 2 Consolidation
=====================================================

Analyzes validation tools related to QA, testing, quality standards, and coverage.
Identifies consolidation patterns for Agent-8's Phase 2 assignment.

Author: Agent-8 (Testing & Quality Assurance Specialist)
Date: 2025-12-03
"""

import json
import sys
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Any

PROJECT_ROOT = Path(__file__).parent.parent


def load_consolidation_candidates() -> Dict[str, List[Dict[str, Any]]]:
    """Load consolidation candidates from JSON file."""
    candidates_file = PROJECT_ROOT / "agent_workspaces" / "Agent-8" / "CONSOLIDATION_CANDIDATES_PHASE2.json"
    
    if not candidates_file.exists():
        print(f"❌ Candidates file not found: {candidates_file}")
        sys.exit(1)
    
    with open(candidates_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    return data


def is_qa_validation_tool(tool: Dict[str, Any]) -> bool:
    """Check if tool is QA/validation related."""
    name = tool.get('name', '').lower()
    path = tool.get('path', '').lower()
    
    qa_keywords = [
        'valid', 'verify', 'check', 'test', 'qa', 'coverage', 
        'quality', 'ssot', 'import', 'chain', 'config'
    ]
    
    return any(keyword in name or keyword in path for keyword in qa_keywords)


def categorize_qa_tools(tools: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """Categorize QA validation tools by pattern."""
    categories = defaultdict(list)
    
    for tool in tools:
        name = tool.get('name', '').lower()
        path = tool.get('path', '').lower()
        
        # SSOT Validation
        if 'ssot' in name or 'ssot' in path:
            categories['ssot_validation'].append(tool)
        # Import/Chain Validation
        elif 'import' in name or 'chain' in name or 'import' in path:
            categories['import_validation'].append(tool)
        # Config Validation
        elif 'config' in name and 'valid' in name:
            categories['config_validation'].append(tool)
        # Test Coverage
        elif 'coverage' in name or 'test' in name and 'coverage' in path:
            categories['test_coverage'].append(tool)
        # Test Infrastructure
        elif 'test' in name and ('tracker' in name or 'analyzer' in name or 'prioritizer' in name):
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
        else:
            categories['other_qa'].append(tool)
    
    return dict(categories)


def analyze_qa_tools():
    """Main analysis function."""
    print("🔍 Analyzing QA Validation Tools for Phase 2 Consolidation\n")
    
    # Load candidates
    data = load_consolidation_candidates()
    validation_tools = data.get('validation', [])
    
    print(f"📊 Total validation tools: {len(validation_tools)}")
    
    # Filter QA-related tools
    qa_tools = [t for t in validation_tools if is_qa_validation_tool(t)]
    print(f"✅ QA-related validation tools: {len(qa_tools)}\n")
    
    # Categorize
    categories = categorize_qa_tools(qa_tools)
    
    # Print categories
    print("📋 QA Validation Tool Categories:\n")
    for category, tools in sorted(categories.items()):
        print(f"  {category.upper().replace('_', ' ')}: {len(tools)} tools")
        for tool in tools[:5]:  # Show first 5
            print(f"    - {tool['name']} ({tool.get('lines', 0)} lines)")
        if len(tools) > 5:
            print(f"    ... and {len(tools) - 5} more")
        print()
    
    # Consolidation recommendations
    print("\n🎯 Consolidation Recommendations:\n")
    
    core_tools = []
    
    # SSOT Validation → unified_ssot_validator.py
    if categories.get('ssot_validation'):
        core_tools.append({
            'name': 'unified_ssot_validator.py',
            'category': 'SSOT Validation',
            'consolidates': len(categories['ssot_validation']),
            'tools': [t['name'] for t in categories['ssot_validation']]
        })
    
    # Import Validation → unified_import_validator.py (already exists: import_chain_validator.py)
    if categories.get('import_validation'):
        core_tools.append({
            'name': 'import_chain_validator.py (enhance)',
            'category': 'Import Validation',
            'consolidates': len(categories['import_validation']),
            'tools': [t['name'] for t in categories['import_validation']]
        })
    
    # Config Validation → ssot_config_validator.py (already exists)
    if categories.get('config_validation'):
        core_tools.append({
            'name': 'ssot_config_validator.py (enhance)',
            'category': 'Config Validation',
            'consolidates': len(categories['config_validation']),
            'tools': [t['name'] for t in categories['config_validation']]
        })
    
    # Test Coverage → unified_test_coverage.py
    if categories.get('test_coverage'):
        core_tools.append({
            'name': 'unified_test_coverage.py',
            'category': 'Test Coverage',
            'consolidates': len(categories['test_coverage']),
            'tools': [t['name'] for t in categories['test_coverage']]
        })
    
    # Test Infrastructure → unified_test_infrastructure.py
    if categories.get('test_infrastructure'):
        core_tools.append({
            'name': 'unified_test_infrastructure.py',
            'category': 'Test Infrastructure',
            'consolidates': len(categories['test_infrastructure']),
            'tools': [t['name'] for t in categories['test_infrastructure']]
        })
    
    # General Validation → unified_validator.py (already exists)
    if categories.get('general_validation'):
        core_tools.append({
            'name': 'unified_validator.py (enhance)',
            'category': 'General Validation',
            'consolidates': len(categories['general_validation']),
            'tools': [t['name'] for t in categories['general_validation']]
        })
    
    print("  Core Tools to Create/Enhance:\n")
    for tool in core_tools:
        print(f"  ✅ {tool['name']}")
        print(f"     Category: {tool['category']}")
        print(f"     Consolidates: {tool['consolidates']} tools")
        print(f"     Sample tools: {', '.join(tool['tools'][:3])}")
        if len(tool['tools']) > 3:
            print(f"     ... and {len(tool['tools']) - 3} more")
        print()
    
    total_consolidated = sum(t['consolidates'] for t in core_tools)
    print(f"📊 Total tools to consolidate: {total_consolidated}")
    print(f"📊 Target core tools: {len(core_tools)}")
    print(f"📊 Reduction: {total_consolidated} → {len(core_tools)} ({100 * (1 - len(core_tools) / total_consolidated):.1f}% reduction)\n")
    
    # Save analysis
    output_file = PROJECT_ROOT / "agent_workspaces" / "Agent-8" / "QA_VALIDATION_TOOLS_ANALYSIS.json"
    analysis = {
        'total_validation_tools': len(validation_tools),
        'qa_validation_tools': len(qa_tools),
        'categories': {
            cat: [{'name': t['name'], 'path': t['path'], 'lines': t.get('lines', 0)} 
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
    
    print(f"✅ Analysis saved to: {output_file}")
    
    return analysis


if __name__ == '__main__':
    analyze_qa_tools()

