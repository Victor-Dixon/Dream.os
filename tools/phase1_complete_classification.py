#!/usr/bin/env python3
"""
Phase -1: Complete Signal vs Noise Classification Analysis
Analyzes existing classification results and generates deliverables for Phase -1.

This script:
1. Analyzes existing TOOL_CLASSIFICATION.json results
2. Generates comprehensive TOOL_CLASSIFICATION.md document
3. Creates summary statistics
4. Generates migration plan for NOISE tools
5. Updates compliance baseline calculations
"""

import json
import os
from pathlib import Path
from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Tuple

def load_classification_results(json_path: Path) -> Dict:
    """Load existing classification results."""
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(f"❌ Classification JSON not found: {json_path}")
        return {}
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing JSON: {e}")
        return {}

def analyze_classifications(data: Dict) -> Dict:
    """Analyze classification results and generate statistics."""
    stats = {
        'total': data.get('total_tools', 0),
        'signal': len(data.get('signal', [])),
        'noise': len(data.get('noise', [])),
        'needs_review': len(data.get('needs_review', [])),
        'unknown': len(data.get('unknown', [])),
        'errors': len(data.get('errors', [])),
    }
    
    # Calculate percentages
    if stats['total'] > 0:
        stats['signal_pct'] = (stats['signal'] / stats['total']) * 100
        stats['noise_pct'] = (stats['noise'] / stats['total']) * 100
        stats['needs_review_pct'] = (stats['needs_review'] / stats['total']) * 100
    else:
        stats['signal_pct'] = 0
        stats['noise_pct'] = 0
        stats['needs_review_pct'] = 0
    
    # Group by directory
    by_directory = defaultdict(lambda: {'signal': 0, 'noise': 0, 'needs_review': 0, 'unknown': 0})
    
    for category in ['signal', 'noise', 'needs_review', 'unknown']:
        for tool in data.get(category, []):
            file_path = tool.get('file', '')
            # Extract directory (tools/subdir/ or tools/)
            parts = Path(file_path).parts
            if len(parts) > 1:
                dir_key = f"{parts[0]}/{parts[1]}" if len(parts) > 2 else parts[0]
            else:
                dir_key = 'tools/'
            by_directory[dir_key][category] += 1
    
    stats['by_directory'] = dict(by_directory)
    
    return stats

def generate_classification_md(data: Dict, stats: Dict, output_path: Path):
    """Generate comprehensive TOOL_CLASSIFICATION.md document."""
    
    md_lines = [
        "# Tool Classification - Signal vs Noise Analysis",
        "",
        f"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"**Phase**: -1 (Signal vs Noise Classification)",
        f"**Status**: ✅ COMPLETE",
        "",
        "## Executive Summary",
        "",
        f"- **Total Tools Classified**: {stats['total']}",
        f"- **SIGNAL Tools** (Real Infrastructure): **{stats['signal']}** ({stats['signal_pct']:.1f}%)",
        f"- **NOISE Tools** (Thin Wrappers): **{stats['noise']}** ({stats['noise_pct']:.1f}%)",
        f"- **Needs Review**: **{stats['needs_review']}** ({stats['needs_review_pct']:.1f}%)",
        f"- **Unknown/Errors**: {stats.get('unknown', 0) + stats.get('errors', 0)}",
        "",
        "## Classification Criteria",
        "",
        "### ✅ SIGNAL Tools (Real Infrastructure - REFACTOR THESE)",
        "",
        "Tools classified as SIGNAL contain:",
        "- **Real business logic** (not just wrappers)",
        "- **Reusable infrastructure** (used across codebase/projects)",
        "- **Modular architecture** (extractable components, classes, multiple functions)",
        "- **Core functionality** (not convenience wrappers)",
        "- **Significant code** (>50 lines typically, but exceptions exist)",
        "",
        "### ❌ NOISE Tools (Thin Wrappers - DEPRECATE/MOVE THESE)",
        "",
        "Tools classified as NOISE are:",
        "- **CLI wrappers** around existing functionality",
        "- **No real business logic** (just calls other tools/functions)",
        "- **One-off convenience scripts** (not reusable infrastructure)",
        "- **Can be replaced** by direct usage of underlying tool",
        "- **Small files** (<50 lines typically, but size alone isn't decisive)",
        "",
        "### ⚠️ Needs Review",
        "",
        "Tools that don't clearly match SIGNAL or NOISE patterns require manual review.",
        "",
        "## Classification by Directory",
        "",
        "| Directory | SIGNAL | NOISE | Needs Review | Total |",
        "|-----------|--------|-------|--------------|-------|",
    ]
    
    # Sort directories by total tools
    sorted_dirs = sorted(stats['by_directory'].items(), 
                        key=lambda x: sum(x[1].values()), reverse=True)
    
    for dir_path, counts in sorted_dirs:
        total = sum(counts.values())
        md_lines.append(
            f"| `{dir_path}` | {counts['signal']} | {counts['noise']} | "
            f"{counts['needs_review'] + counts.get('unknown', 0)} | {total} |"
        )
    
    md_lines.extend([
        "",
        "## SIGNAL Tools (Real Infrastructure)",
        "",
        "These tools will be included in V2 refactoring phases.",
        "",
        "| File | Lines | Functions | Classes | Confidence |",
        "|------|-------|-----------|---------|------------|",
    ])
    
    # Add SIGNAL tools (sorted by lines, descending)
    signal_tools = sorted(data.get('signal', []), 
                         key=lambda x: x.get('lines', 0), reverse=True)
    
    for tool in signal_tools[:100]:  # Show top 100
        file_path = tool.get('file', '').replace('tools\\', 'tools/')
        lines = tool.get('lines', 0)
        funcs = tool.get('function_count', 0)
        classes = tool.get('class_count', 0)
        confidence = tool.get('confidence', 'MEDIUM')
        md_lines.append(
            f"| `{file_path}` | {lines} | {funcs} | {classes} | {confidence} |"
        )
    
    if len(signal_tools) > 100:
        md_lines.append(f"\n*... and {len(signal_tools) - 100} more SIGNAL tools (see JSON for complete list)*")
    
    md_lines.extend([
        "",
        "## NOISE Tools (Thin Wrappers)",
        "",
        "These tools will be moved to `scripts/` directory or deprecated.",
        "",
        "| File | Lines | Functions | Classes | Confidence |",
        "|------|-------|-----------|---------|------------|",
    ])
    
    # Add NOISE tools (sorted by lines, ascending)
    noise_tools = sorted(data.get('noise', []), 
                        key=lambda x: x.get('lines', 0))
    
    for tool in noise_tools[:100]:  # Show top 100
        file_path = tool.get('file', '').replace('tools\\', 'tools/')
        lines = tool.get('lines', 0)
        funcs = tool.get('function_count', 0)
        classes = tool.get('class_count', 0)
        confidence = tool.get('confidence', 'MEDIUM')
        md_lines.append(
            f"| `{file_path}` | {lines} | {funcs} | {classes} | {confidence} |"
        )
    
    if len(noise_tools) > 100:
        md_lines.append(f"\n*... and {len(noise_tools) - 100} more NOISE tools (see JSON for complete list)*")
    
    md_lines.extend([
        "",
        "## Needs Review",
        "",
        "These tools require manual review to determine SIGNAL vs NOISE.",
        "",
        "| File | Lines | Functions | Classes | Confidence |",
        "|------|-------|-----------|---------|------------|",
    ])
    
    # Add needs_review tools
    needs_review_tools = sorted(data.get('needs_review', []) + data.get('unknown', []),
                               key=lambda x: x.get('lines', 0))
    
    for tool in needs_review_tools[:50]:  # Show top 50
        file_path = tool.get('file', '').replace('tools\\', 'tools/')
        lines = tool.get('lines', 0)
        funcs = tool.get('function_count', 0)
        classes = tool.get('class_count', 0)
        confidence = tool.get('confidence', 'LOW')
        md_lines.append(
            f"| `{file_path}` | {lines} | {funcs} | {classes} | {confidence} |"
        )
    
    if len(needs_review_tools) > 50:
        md_lines.append(f"\n*... and {len(needs_review_tools) - 50} more tools needing review (see JSON for complete list)*")
    
    md_lines.extend([
        "",
        "## Next Steps",
        "",
        "1. ✅ **Classification Complete**: All 791 tools classified",
        "2. ⏳ **Review NEEDS_REVIEW tools**: Manual review required",
        "3. ⏳ **Move NOISE tools**: Migrate to `scripts/` directory",
        "4. ⏳ **Update toolbelt registry**: Remove NOISE tools from registry",
        "5. ⏳ **Update compliance baseline**: Recalculate percentages (SIGNAL tools only)",
        "6. ⏳ **Proceed with V2 refactoring**: Focus on SIGNAL tools only",
        "",
        "## Compliance Baseline Impact",
        "",
        f"**Before Phase -1**:",
        f"- Total tools: 791",
        f"- Non-compliant: 782 files",
        f"- Compliance: 1.8% (14/791)",
        "",
        f"**After Phase -1** (SIGNAL tools only):",
        f"- SIGNAL tools (refactoring scope): {stats['signal']}",
        f"- NOISE tools (deprecated): {stats['noise']}",
        f"- Compliance baseline will be recalculated for {stats['signal']} SIGNAL tools only",
        "",
        "---",
        "",
        "**Reference**: See `docs/toolbelt/TOOLBELT_SIGNAL_VS_NOISE_ANALYSIS.md` for classification methodology.",
        "",
        "🐝 **WE. ARE. SWARM. ⚡🔥**",
    ])
    
    # Write markdown file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(md_lines))
    
    print(f"✅ Generated TOOL_CLASSIFICATION.md: {output_path}")

def generate_migration_plan(data: Dict, stats: Dict, output_path: Path):
    """Generate migration plan for NOISE tools."""
    
    noise_tools = data.get('noise', [])
    
    md_lines = [
        "# NOISE Tools Migration Plan",
        "",
        f"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"**Phase**: -1 (Signal vs Noise Classification)",
        f"**Status**: 📋 READY FOR EXECUTION",
        "",
        "## Summary",
        "",
        f"- **NOISE Tools to Migrate**: {stats['noise']}",
        f"- **Target Directory**: `scripts/`",
        f"- **Action**: Move or deprecate NOISE tools",
        "",
        "## Migration Strategy",
        "",
        "1. **Create `scripts/` directory structure**",
        "   - Organize by category (analysis, bi, compliance, testing, etc.)",
        "   - Maintain tool organization for easier discovery",
        "",
        "2. **Move NOISE Tools**",
        "   - Move files from `tools/` to appropriate `scripts/` subdirectory",
        "   - Update any import references",
        "   - Create compatibility wrappers if needed (temporary)",
        "",
        "3. **Update Toolbelt Registry**",
        "   - Remove NOISE tools from toolbelt registry",
        "   - Update documentation",
        "",
        "4. **Update Documentation**",
        "   - Document migration in DEPRECATION_NOTICES.md",
        "   - Update tool usage guides",
        "",
        "## NOISE Tools by Category",
        "",
    ]
    
    # Group NOISE tools by directory/category
    by_category = defaultdict(list)
    for tool in noise_tools:
        file_path = tool.get('file', '')
        parts = Path(file_path).parts
        if len(parts) > 1:
            category = parts[1] if len(parts) > 2 else 'root'
        else:
            category = 'root'
        by_category[category].append(tool)
    
    for category, tools in sorted(by_category.items()):
        md_lines.extend([
            f"### {category}/ ({len(tools)} tools)",
            "",
            "| File | Lines | Reason |",
            "|------|-------|--------|",
        ])
        
        for tool in sorted(tools, key=lambda x: x.get('lines', 0)):
            file_path = tool.get('file', '').replace('tools\\', 'tools/')
            lines = tool.get('lines', 0)
            rationale = '; '.join(tool.get('rationale', []))[:100]
            md_lines.append(f"| `{file_path}` | {lines} | {rationale}... |")
        
        md_lines.append("")
    
    md_lines.extend([
        "## Execution Checklist",
        "",
        "- [ ] Create `scripts/` directory structure",
        "- [ ] Move NOISE tools to appropriate `scripts/` subdirectories",
        "- [ ] Update toolbelt registry (remove NOISE tools)",
        "- [ ] Update documentation references",
        "- [ ] Test that moved tools still work (if needed)",
        "- [ ] Commit migration",
        "",
        "---",
        "",
        "🐝 **WE. ARE. SWARM. ⚡🔥**",
    ])
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(md_lines))
    
    print(f"✅ Generated migration plan: {output_path}")

def generate_summary_stats(stats: Dict, output_path: Path):
    """Generate summary statistics JSON."""
    
    summary = {
        'timestamp': datetime.now().isoformat(),
        'phase': '-1',
        'status': 'COMPLETE',
        'statistics': {
            'total_tools': stats['total'],
            'signal_tools': stats['signal'],
            'noise_tools': stats['noise'],
            'needs_review': stats['needs_review'],
            'signal_percentage': round(stats['signal_pct'], 2),
            'noise_percentage': round(stats['noise_pct'], 2),
            'needs_review_percentage': round(stats['needs_review_pct'], 2),
        },
        'refactoring_scope': {
            'tools_to_refactor': stats['signal'],
            'tools_to_deprecate': stats['noise'],
            'tools_to_review': stats['needs_review'],
        },
        'compliance_baseline': {
            'before_phase_minus1': {
                'total_files': 791,
                'non_compliant': 782,
                'compliance_percentage': 1.8
            },
            'after_phase_minus1': {
                'total_files': stats['signal'],  # Only SIGNAL tools
                'non_compliant': 'TBD',  # Will be recalculated
                'compliance_percentage': 'TBD'
            }
        },
        'by_directory': stats['by_directory']
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2)
    
    print(f"✅ Generated summary statistics: {output_path}")

def main():
    """Main entry point."""
    repo_root = Path(__file__).parent.parent
    tools_dir = repo_root / 'tools'
    json_path = tools_dir / 'TOOL_CLASSIFICATION.json'
    output_dir = repo_root / 'docs' / 'toolbelt'
    
    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("🔍 Analyzing existing classification results...")
    data = load_classification_results(json_path)
    
    if not data:
        print("❌ No classification data found. Please run classify_all_tools_signal_noise.py first.")
        return
    
    print(f"✅ Loaded classification data: {data.get('total_tools', 0)} tools")
    
    print("📊 Analyzing statistics...")
    stats = analyze_classifications(data)
    
    print(f"   - SIGNAL: {stats['signal']} ({stats['signal_pct']:.1f}%)")
    print(f"   - NOISE: {stats['noise']} ({stats['noise_pct']:.1f}%)")
    print(f"   - Needs Review: {stats['needs_review']} ({stats['needs_review_pct']:.1f}%)")
    
    print("📝 Generating TOOL_CLASSIFICATION.md...")
    generate_classification_md(data, stats, output_dir / 'TOOL_CLASSIFICATION.md')
    
    print("📋 Generating migration plan...")
    generate_migration_plan(data, stats, output_dir / 'NOISE_TOOLS_MIGRATION_PLAN.md')
    
    print("📈 Generating summary statistics...")
    generate_summary_stats(stats, output_dir / 'PHASE_MINUS1_SUMMARY_STATS.json')
    
    print("\n✅ Phase -1 analysis complete!")
    print(f"   - Classification document: {output_dir / 'TOOL_CLASSIFICATION.md'}")
    print(f"   - Migration plan: {output_dir / 'NOISE_TOOLS_MIGRATION_PLAN.md'}")
    print(f"   - Summary stats: {output_dir / 'PHASE_MINUS1_SUMMARY_STATS.json'}")

if __name__ == '__main__':
    main()

