#!/usr/bin/env python3
"""
V2 Refactoring Progress Tracker
================================

Tracks V2 compliance refactoring progress and generates progress reports.

Author: Agent-2 (Architecture & Design Specialist)
Date: 2025-12-12
V2 Compliant: Yes
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

try:
    import yaml
except ImportError:
    print("❌ ERROR: pyyaml not installed. Install with: pip install pyyaml")
    sys.exit(1)


def get_file_line_count(file_path: Path) -> int:
    """Get line count for a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return len(f.readlines())
    except Exception:
        return 0


def scan_violations(src_dir: Path, limit: int = 300) -> List[Tuple[Path, int]]:
    """
    Scan for V2 compliance violations.
    
    Args:
        src_dir: Source directory to scan
        limit: Maximum lines allowed per file
        
    Returns:
        List of (file_path, line_count) tuples for violations
    """
    violations = []
    
    for py_file in src_dir.rglob("*.py"):
        line_count = get_file_line_count(py_file)
        if line_count > limit:
            violations.append((py_file, line_count))
    
    return sorted(violations, key=lambda x: x[1], reverse=True)


def categorize_violations(violations: List[Tuple[Path, int]]) -> Dict[str, List[Tuple[Path, int]]]:
    """
    Categorize violations by severity.
    
    Args:
        violations: List of (file_path, line_count) tuples
        
    Returns:
        Dictionary with categorized violations
    """
    categories = {
        "critical": [],  # >1000 lines
        "high": [],      # 500-1000 lines
        "medium": []     # 300-500 lines
    }
    
    for file_path, line_count in violations:
        if line_count > 1000:
            categories["critical"].append((file_path, line_count))
        elif line_count > 500:
            categories["high"].append((file_path, line_count))
        else:
            categories["medium"].append((file_path, line_count))
    
    return categories


def generate_progress_report(
    violations: List[Tuple[Path, int]],
    baseline_file: Path = None
) -> Dict:
    """
    Generate progress report comparing to baseline.
    
    Args:
        violations: Current violations
        baseline_file: Path to baseline violations JSON file
        
    Returns:
        Progress report dictionary
    """
    project_root = Path(__file__).parent.parent
    
    # Load baseline if provided
    baseline = {}
    if baseline_file and baseline_file.exists():
        try:
            with open(baseline_file, 'r', encoding='utf-8') as f:
                baseline = json.load(f)
        except Exception:
            pass
    
    # Categorize current violations
    categories = categorize_violations(violations)
    
    # Calculate totals
    total_violations = len(violations)
    total_lines_over = sum(max(0, lines - 300) for _, lines in violations)
    
    # Compare to baseline
    baseline_total = baseline.get("total_violations", total_violations)
    improvement = baseline_total - total_violations
    improvement_pct = (improvement / baseline_total * 100) if baseline_total > 0 else 0
    
    report = {
        "timestamp": datetime.now().isoformat(),
        "total_violations": total_violations,
        "total_lines_over": total_lines_over,
        "baseline_violations": baseline_total,
        "improvement": improvement,
        "improvement_percentage": round(improvement_pct, 2),
        "categories": {
            "critical": {
                "count": len(categories["critical"]),
                "files": [
                    {
                        "path": str(f.relative_to(project_root)),
                        "lines": lines,
                        "over_limit": lines - 300
                    }
                    for f, lines in categories["critical"][:10]
                ]
            },
            "high": {
                "count": len(categories["high"]),
                "files": [
                    {
                        "path": str(f.relative_to(project_root)),
                        "lines": lines,
                        "over_limit": lines - 300
                    }
                    for f, lines in categories["high"][:10]
                ]
            },
            "medium": {
                "count": len(categories["medium"]),
                "files": [
                    {
                        "path": str(f.relative_to(project_root)),
                        "lines": lines,
                        "over_limit": lines - 300
                    }
                    for f, lines in categories["medium"][:10]
                ]
            }
        }
    }
    
    return report


def print_progress_report(report: Dict):
    """Print formatted progress report."""
    print("=" * 60)
    print("V2 COMPLIANCE REFACTORING PROGRESS REPORT")
    print("=" * 60)
    print(f"\n📊 Current Status:")
    print(f"   Total Violations: {report['total_violations']}")
    print(f"   Total Lines Over Limit: {report['total_lines_over']:,}")
    
    if report['baseline_violations'] > 0:
        print(f"\n📈 Progress:")
        print(f"   Baseline: {report['baseline_violations']} violations")
        print(f"   Current: {report['total_violations']} violations")
        print(f"   Improvement: {report['improvement']} violations ({report['improvement_percentage']}%)")
    
    print(f"\n📋 Violations by Category:")
    print(f"   Critical (>1000 lines): {report['categories']['critical']['count']}")
    print(f"   High (500-1000 lines): {report['categories']['high']['count']}")
    print(f"   Medium (300-500 lines): {report['categories']['medium']['count']}")
    
    # Print top violations
    for category_name, category_data in report['categories'].items():
        if category_data['files']:
            print(f"\n🔴 Top {category_name.upper()} Violations:")
            for file_info in category_data['files'][:5]:
                print(f"   {file_info['path']}: {file_info['lines']} lines (+{file_info['over_limit']})")


def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Track V2 compliance refactoring progress"
    )
    parser.add_argument(
        "--baseline",
        type=Path,
        help="Path to baseline violations JSON file",
        default=Path("docs/v2_baseline_violations.json")
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Path to save progress report JSON",
        default=None
    )
    parser.add_argument(
        "--src-dir",
        type=Path,
        help="Source directory to scan",
        default=Path("src")
    )
    parser.add_argument(
        "--limit",
        type=int,
        help="Maximum lines allowed per file",
        default=300
    )
    
    args = parser.parse_args()
    
    project_root = Path(__file__).parent.parent
    src_dir = project_root / args.src_dir if not args.src_dir.is_absolute() else args.src_dir
    
    if not src_dir.exists():
        print(f"❌ ERROR: Source directory not found: {src_dir}")
        sys.exit(1)
    
    # Scan for violations
    print(f"🔍 Scanning {src_dir} for V2 compliance violations...")
    violations = scan_violations(src_dir, args.limit)
    
    # Generate report
    baseline_file = project_root / args.baseline if not args.baseline.is_absolute() else args.baseline
    report = generate_progress_report(violations, baseline_file)
    
    # Print report
    print_progress_report(report)
    
    # Save report if requested
    if args.output:
        output_path = project_root / args.output if not args.output.is_absolute() else args.output
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        print(f"\n💾 Progress report saved to: {output_path}")
    
    # Exit with error code if violations exist
    sys.exit(1 if report['total_violations'] > 0 else 0)


if __name__ == "__main__":
    main()



