#!/usr/bin/env python3
"""
Tag Analyzer Score Comparison Tool
Compares tag analyzer reports to track improvement between runs.

<!-- SSOT Domain: tools -->

Author: Agent-5 (Business Intelligence Specialist)
Created: 2025-12-28
Purpose: Compare tag analyzer reports to validate SSOT tagging remediation progress
"""

import argparse
import json
import re
from pathlib import Path
from typing import Dict, Optional


def extract_summary_from_report(report_path: Path) -> Optional[Dict[str, float]]:
    """Extract summary statistics from tag analyzer markdown report."""
    try:
        content = report_path.read_text(encoding='utf-8')
        
        # Extract average score
        avg_match = re.search(r'Average Tag Score:\*\* ([\d.]+)/5\.0', content)
        avg_score = float(avg_match.group(1)) if avg_match else None
        
        # Extract perfect files count
        perfect_match = re.search(r'Perfect Files \(5/5\):\*\* (\d+)', content)
        perfect_count = int(perfect_match.group(1)) if perfect_match else None
        
        # Extract needs work count
        needs_match = re.search(r'Needs Work \(<3/5\):\*\* (\d+)', content)
        needs_count = int(needs_match.group(1)) if needs_match else None
        
        if avg_score is not None:
            return {
                'average_score': avg_score,
                'perfect_files': perfect_count or 0,
                'needs_work': needs_count or 0
            }
        return None
    except Exception as e:
        print(f"Error reading report: {e}")
        return None


def compare_reports(before_path: Path, after_path: Path) -> Dict[str, any]:
    """Compare two tag analyzer reports."""
    before = extract_summary_from_report(before_path)
    after = extract_summary_from_report(after_path)
    
    if not before or not after:
        return {"success": False, "error": "Could not extract summary from one or both reports"}
    
    avg_delta = after['average_score'] - before['average_score']
    perfect_delta = after['perfect_files'] - before['perfect_files']
    needs_delta = before['needs_work'] - after['needs_work']
    
    return {
        "success": True,
        "before": before,
        "after": after,
        "improvements": {
            "average_score_delta": round(avg_delta, 2),
            "perfect_files_delta": perfect_delta,
            "needs_work_delta": needs_delta
        },
        "summary": f"Average score: {before['average_score']:.1f} → {after['average_score']:.1f} ({'+' if avg_delta >= 0 else ''}{avg_delta:.2f}). Perfect files: {before['perfect_files']} → {after['perfect_files']} ({'+' if perfect_delta >= 0 else ''}{perfect_delta}). Needs work: {before['needs_work']} → {after['needs_work']} ({'+' if needs_delta >= 0 else ''}{needs_delta})."
    }


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Compare tag analyzer reports to track SSOT tagging progress"
    )
    parser.add_argument("before", help="Path to earlier report")
    parser.add_argument("after", help="Path to later report")
    parser.add_argument("--json", action="store_true", help="Output JSON format")
    
    args = parser.parse_args()
    
    before_path = Path(args.before)
    after_path = Path(args.after)
    
    if not before_path.exists():
        print(f"Error: {before_path} not found")
        return 1
    
    if not after_path.exists():
        print(f"Error: {after_path} not found")
        return 1
    
    result = compare_reports(before_path, after_path)
    
    if not result.get("success"):
        print(f"Error: {result.get('error')}")
        return 1
    
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(result["summary"])
        print(f"\nDetailed comparison:")
        print(f"  Average score: {result['before']['average_score']:.2f} → {result['after']['average_score']:.2f} (Δ {result['improvements']['average_score_delta']:+.2f})")
        print(f"  Perfect files: {result['before']['perfect_files']} → {result['after']['perfect_files']} (Δ {result['improvements']['perfect_files_delta']:+d})")
        print(f"  Needs work: {result['before']['needs_work']} → {result['after']['needs_work']} (Δ {result['improvements']['needs_work_delta']:+d})")
    
    return 0


if __name__ == "__main__":
    exit(main())

