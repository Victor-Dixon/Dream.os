#!/usr/bin/env python3
"""
Count V2 Compliance Violations
==============================

Scans the codebase to count actual V2 compliance violations (files over 300 lines).

Agent-6: Coordination & Communication Specialist
Task: Monitor V2 compliance refactoring progress - verify dashboard numbers
"""

import os
from pathlib import Path
from typing import List, Dict

def count_lines(file_path: Path) -> int:
    """Count lines in a file."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return sum(1 for _ in f)
    except Exception:
        return 0

def scan_v2_violations(root_dir: Path, exclude_dirs: List[str] = None) -> Dict:
    """Scan for V2 compliance violations."""
    if exclude_dirs is None:
        exclude_dirs = ['.git', '__pycache__', 'node_modules', '.pytest_cache', 
                       'venv', 'env', '.venv', 'dist', 'build', '.benchmarks',
                       'temp_repos', 'dream', 'quarantine', 'backup']
    
    violations = []
    total_files = 0
    compliant_files = 0
    
    # File extensions to check
    extensions = ['.py', '.js', '.ts', '.tsx', '.jsx']
    
    for ext in extensions:
        for file_path in root_dir.rglob(f'*{ext}'):
            # Skip excluded directories
            if any(excluded in str(file_path) for excluded in exclude_dirs):
                continue
            
            # Skip if in excluded subdirectories
            parts = file_path.parts
            if any(part in exclude_dirs for part in parts):
                continue
            
            total_files += 1
            line_count = count_lines(file_path)
            
            if line_count > 300:
                violations.append({
                    'file': str(file_path.relative_to(root_dir)),
                    'lines': line_count,
                    'over_limit': line_count - 300
                })
            else:
                compliant_files += 1
    
    compliance_percent = (compliant_files / total_files * 100) if total_files > 0 else 0
    
    return {
        'total_files': total_files,
        'compliant_files': compliant_files,
        'violations': violations,
        'violation_count': len(violations),
        'compliance_percent': round(compliance_percent, 1)
    }

def main():
    """Main execution."""
    print("=" * 70)
    print("V2 COMPLIANCE VIOLATION COUNT")
    print("=" * 70)
    print()
    
    project_root = Path(__file__).parent.parent
    
    print(f"Scanning: {project_root}")
    print("Checking files: .py, .js, .ts, .tsx, .jsx")
    print("Limit: 300 lines per file")
    print()
    print("Scanning...")
    
    results = scan_v2_violations(project_root)
    
    print()
    print("=" * 70)
    print("RESULTS")
    print("=" * 70)
    print(f"Total files scanned: {results['total_files']}")
    print(f"Compliant files: {results['compliant_files']}")
    print(f"Violations: {results['violation_count']}")
    print(f"Compliance: {results['compliance_percent']}%")
    print()
    
    if results['violation_count'] > 0:
        print(f"Top 20 violations (by line count):")
        print("-" * 70)
        sorted_violations = sorted(results['violations'], key=lambda x: x['lines'], reverse=True)
        for i, v in enumerate(sorted_violations[:20], 1):
            print(f"{i:2}. {v['file']}: {v['lines']} lines (+{v['over_limit']})")
    
    print()
    print("=" * 70)
    print("DASHBOARD NUMBERS")
    print("=" * 70)
    print(f"Violations: {results['violation_count']}")
    print(f"Compliance: {results['compliance_percent']}%")
    print()
    
    # Check against expected numbers
    expected_violations = 110
    expected_compliance = 87.6
    
    print("Expected (from MASTER_TASK_LOG):")
    print(f"  Violations: {expected_violations}")
    print(f"  Compliance: {expected_compliance}%")
    print()
    
    if results['violation_count'] == expected_violations and abs(results['compliance_percent'] - expected_compliance) < 0.5:
        print("✅ Numbers match expected values!")
    else:
        print("⚠️  Numbers differ from expected:")
        print(f"   Violations: {results['violation_count']} (expected {expected_violations})")
        print(f"   Compliance: {results['compliance_percent']}% (expected {expected_compliance}%)")
    
    # Save results
    import json
    output_path = project_root / "agent_workspaces" / "Agent-6" / "v2_violations_count.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✅ Results saved to: {output_path}")

if __name__ == "__main__":
    main()

