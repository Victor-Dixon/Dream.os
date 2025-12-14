#!/usr/bin/env python3
"""
Core Domain Code Quality Scanner
Scans core domain files for code quality issues, complexity, and maintainability
"""

import os
import ast
from pathlib import Path
from typing import List, Dict, Tuple
from collections import defaultdict

REPO_ROOT = Path(__file__).parent.parent
CORE_DIR = REPO_ROOT / "src" / "core"


def count_lines(file_path: Path) -> int:
    """Count lines in file"""
    try:
        return len(file_path.read_text(encoding='utf-8').split('\n'))
    except:
        return 0


def analyze_complexity(file_path: Path) -> Dict:
    """Analyze code complexity"""
    try:
        content = file_path.read_text(encoding='utf-8')
        tree = ast.parse(content)

        complexity = {
            'functions': 0,
            'classes': 0,
            'max_function_lines': 0,
            'max_class_lines': 0,
            'imports': len(ast.walk(tree)) - sum(1 for _ in ast.walk(tree) if isinstance(_, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef))),
        }

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                complexity['functions'] += 1
                func_lines = node.end_lineno - \
                    node.lineno if hasattr(node, 'end_lineno') else 0
                complexity['max_function_lines'] = max(
                    complexity['max_function_lines'], func_lines)
            elif isinstance(node, ast.ClassDef):
                complexity['classes'] += 1
                class_lines = node.end_lineno - \
                    node.lineno if hasattr(node, 'end_lineno') else 0
                complexity['max_class_lines'] = max(
                    complexity['max_class_lines'], class_lines)

        return complexity
    except:
        return {'functions': 0, 'classes': 0, 'max_function_lines': 0, 'max_class_lines': 0, 'imports': 0}


def check_ssot_tag(file_path: Path) -> bool:
    """Check if file has SSOT tag"""
    try:
        content = file_path.read_text(encoding='utf-8')
        lines = content.split('\n')[:50]
        header = '\n'.join(lines)
        return 'SSOT Domain:' in header
    except:
        return False


def scan_core_files(limit: int = 10) -> List[Dict]:
    """Scan core domain files for quality issues"""
    results = []

    # Get Python files in core directory (excluding test files and __pycache__)
    core_files = []
    for root, dirs, files in os.walk(CORE_DIR):
        # Skip test directories and cache
        dirs[:] = [d for d in dirs if d not in ['__pycache__', 'test', 'tests']]

        for file in files:
            if file.endswith('.py') and not file.startswith('test_'):
                file_path = Path(root) / file
                core_files.append(file_path)

    # Sort by size (largest first) to prioritize important files
    core_files.sort(key=lambda f: count_lines(f), reverse=True)

    # Scan first N files
    for file_path in core_files[:limit]:
        rel_path = file_path.relative_to(REPO_ROOT)
        lines = count_lines(file_path)
        complexity = analyze_complexity(file_path)
        has_ssot = check_ssot_tag(file_path)

        # Calculate quality score (lower is better)
        issues = []
        score = 0

        if lines > 300:
            issues.append(f"V2 violation: {lines} lines (limit: 300)")
            score += 10

        if complexity['max_function_lines'] > 50:
            issues.append(
                f"Long function: {complexity['max_function_lines']} lines")
            score += 5

        if complexity['max_class_lines'] > 200:
            issues.append(
                f"Large class: {complexity['max_class_lines']} lines")
            score += 5

        if not has_ssot:
            issues.append("Missing SSOT tag")
            score += 3

        if complexity['functions'] > 20:
            issues.append(f"High function count: {complexity['functions']}")
            score += 2

        results.append({
            'file': str(rel_path),
            'lines': lines,
            'complexity': complexity,
            'has_ssot': has_ssot,
            'issues': issues,
            'score': score,
            'priority': 'HIGH' if score >= 10 else 'MEDIUM' if score >= 5 else 'LOW'
        })

    return sorted(results, key=lambda x: x['score'], reverse=True)


def generate_report(results: List[Dict]) -> str:
    """Generate markdown report"""
    report = []
    report.append("# Core Domain Code Quality Scan Report")
    report.append("")
    report.append("**Date**: 2025-12-13")
    report.append("**Agent**: Agent-8 (SSOT & System Integration Specialist)")
    report.append("**Task**: Core Domain Scanning - Code Quality Analysis")
    report.append("")
    report.append("---")
    report.append("")
    report.append("## Summary")
    report.append("")

    total = len(results)
    high_priority = sum(1 for r in results if r['priority'] == 'HIGH')
    medium_priority = sum(1 for r in results if r['priority'] == 'MEDIUM')
    low_priority = sum(1 for r in results if r['priority'] == 'LOW')
    missing_ssot = sum(1 for r in results if not r['has_ssot'])

    report.append(f"- **Total Files Scanned**: {total}")
    report.append(f"- **HIGH Priority Issues**: {high_priority}")
    report.append(f"- **MEDIUM Priority Issues**: {medium_priority}")
    report.append(f"- **LOW Priority Issues**: {low_priority}")
    report.append(f"- **Missing SSOT Tags**: {missing_ssot}")
    report.append("")
    report.append("---")
    report.append("")
    report.append("## Detailed Results")
    report.append("")
    report.append(
        "| File | Lines | Functions | Classes | SSOT | Issues | Priority |")
    report.append(
        "|------|-------|-----------|---------|------|--------|----------|")

    for r in results:
        ssot_status = "✅" if r['has_ssot'] else "❌"
        file_name = r['file'].split('/')[-1]
        issues_count = len(r['issues'])
        priority_emoji = "🔴" if r['priority'] == 'HIGH' else "🟡" if r['priority'] == 'MEDIUM' else "🟢"

        report.append(
            f"| `{file_name}` | {r['lines']} | {r['complexity']['functions']} | {r['complexity']['classes']} | {ssot_status} | {issues_count} | {priority_emoji} {r['priority']} |")

    report.append("")
    report.append("---")
    report.append("")
    report.append("## Files by Priority")
    report.append("")

    for priority in ['HIGH', 'MEDIUM', 'LOW']:
        priority_files = [r for r in results if r['priority'] == priority]
        if priority_files:
            report.append(
                f"### {priority} Priority ({len(priority_files)} files)")
            report.append("")
            for r in priority_files:
                file_name = r['file'].split('/')[-1]
                report.append(f"- **`{r['file']}`** ({r['lines']} lines)")
                if r['issues']:
                    for issue in r['issues']:
                        report.append(f"  - {issue}")
                report.append("")

    report.append("---")
    report.append("")
    report.append("## Recommendations")
    report.append("")

    v2_violations = [r for r in results if any(
        'V2 violation' in issue for issue in r['issues'])]
    if v2_violations:
        report.append("### V2 Compliance Issues")
        report.append("")
        for r in v2_violations:
            report.append(
                f"- `{r['file']}` - {r['lines']} lines (exceeds 300 line limit)")
        report.append("")

    missing_ssot_files = [r for r in results if not r['has_ssot']]
    if missing_ssot_files:
        report.append("### Missing SSOT Tags")
        report.append("")
        for r in missing_ssot_files:
            report.append(f"- `{r['file']}`")
        report.append("")

    report.append(
        "**Status**: Scan complete, ready for prioritization and remediation")
    report.append("")
    report.append("🐝 **WE. ARE. SWARM. ⚡🔥**")

    return "\n".join(report)


if __name__ == "__main__":
    print("Core Domain Code Quality Scan - Scanning files...")
    results = scan_core_files(limit=10)
    report = generate_report(results)

    # Save report
    report_path = REPO_ROOT / "docs" / "agent-8" / \
        "AGENT8_CORE_DOMAIN_SCAN_2025-12-13.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report, encoding='utf-8')

    print(f"\nReport generated: {report_path}")
    print(f"\nSummary: {len(results)} files scanned")
    print(
        f"High priority: {sum(1 for r in results if r['priority'] == 'HIGH')}")
    print(
        f"Medium priority: {sum(1 for r in results if r['priority'] == 'MEDIUM')}")

    # Print summary
    print("\n" + "="*60)
    print(report[:500])  # Print first 500 chars
    print("="*60)



