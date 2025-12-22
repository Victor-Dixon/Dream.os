#!/usr/bin/env python3
"""
Refactored Files Validation Script
===================================

Validates refactored files against V2 compliance standards.
Designed for post-refactoring validation in bilateral coordination protocol.

Author: Agent-8 (SSOT & System Integration Specialist)
Date: 2025-12-12
V2 Compliant: Yes
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

try:
    import yaml
except ImportError:
    print("❌ ERROR: pyyaml not installed. Install with: pip install pyyaml")
    sys.exit(1)


def count_lines(file_path: Path) -> int:
    """Count lines in a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return len(f.readlines())
    except Exception:
        return 0


def count_functions(file_path: Path) -> int:
    """Count function definitions in a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Count function definitions (def and async def)
            func_count = content.count('\ndef ') + content.count('\n    def ')
            func_count += content.count('\nasync def ') + content.count('\n    async def ')
            return func_count
    except Exception:
        return 0


def count_classes(file_path: Path) -> int:
    """Count class definitions in a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            return content.count('\nclass ')
    except Exception:
        return 0


def validate_file(file_path: Path, loc_limit: int = 400, func_limit: int = 30, class_limit: int = 200) -> Dict:
    """Validate a single file against V2 compliance standards."""
    violations = []
    
    lines = count_lines(file_path)
    funcs = count_functions(file_path)
    classes = count_classes(file_path)
    
    if lines > loc_limit:
        violations.append(f"File size: {lines} lines (limit: {loc_limit})")
    
    # Note: Function and class size validation would require AST parsing
    # For now, we just count them
    
    return {
        "file": str(file_path),
        "lines": lines,
        "functions": funcs,
        "classes": classes,
        "violations": violations,
        "compliant": len(violations) == 0
    }


def validate_refactored_files(
    file_paths: List[Path],
    loc_limit: int = 400,
    output_format: str = "text"
) -> Tuple[int, int, List[Dict]]:
    """
    Validate multiple refactored files.
    
    Args:
        file_paths: List of file paths to validate
        loc_limit: Maximum lines of code allowed
        output_format: Output format (text, json)
        
    Returns:
        Tuple of (total_files, compliant_files, results)
    """
    results = []
    compliant_count = 0
    
    for file_path in file_paths:
        if not file_path.exists():
            print(f"⚠️  File not found: {file_path}")
            continue
            
        result = validate_file(file_path, loc_limit)
        results.append(result)
        
        if result["compliant"]:
            compliant_count += 1
    
    total_files = len(results)
    
    if output_format == "json":
        output = {
            "total_files": total_files,
            "compliant_files": compliant_count,
            "non_compliant_files": total_files - compliant_count,
            "compliance_rate": f"{(compliant_count / total_files * 100):.1f}%" if total_files > 0 else "0%",
            "results": results
        }
        print(json.dumps(output, indent=2))
    else:
        print(f"\n{'='*60}")
        print("REFACTORED FILES VALIDATION REPORT")
        print(f"{'='*60}\n")
        print(f"Total Files Validated: {total_files}")
        print(f"Compliant Files: {compliant_count}")
        print(f"Non-Compliant Files: {total_files - compliant_count}")
        if total_files > 0:
            print(f"Compliance Rate: {(compliant_count / total_files * 100):.1f}%")
        print(f"\n{'='*60}\n")
        
        for result in results:
            status = "✅" if result["compliant"] else "❌"
            print(f"{status} {result['file']}")
            print(f"   Lines: {result['lines']} | Functions: {result['functions']} | Classes: {result['classes']}")
            if result["violations"]:
                for violation in result["violations"]:
                    print(f"   ⚠️  {violation}")
            print()
    
    return total_files, compliant_count, results


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Validate refactored files against V2 compliance")
    parser.add_argument(
        "files",
        nargs="+",
        help="File paths to validate"
    )
    parser.add_argument(
        "--loc-limit",
        type=int,
        default=400,
        help="Guideline for lines of code (default: 400, clean code principles take precedence)"
    )
    parser.add_argument(
        "--output-format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)"
    )
    parser.add_argument(
        "--rules",
        type=Path,
        help="Path to V2 rules YAML file (optional)"
    )
    
    args = parser.parse_args()
    
    # Load rules if provided
    loc_limit = args.loc_limit
    if args.rules and args.rules.exists():
        try:
            with open(args.rules, 'r', encoding='utf-8') as f:
                rules = yaml.safe_load(f)
                if rules and 'loc_limit' in rules:
                    loc_limit = rules['loc_limit']
        except Exception as e:
            print(f"⚠️  Warning: Could not load rules file: {e}")
    
    # Convert file paths to Path objects
    file_paths = [Path(f) for f in args.files]
    
    # Validate files
    total, compliant, results = validate_refactored_files(
        file_paths,
        loc_limit=loc_limit,
        output_format=args.output_format
    )
    
    # Exit code: 0 if all compliant, 1 if any violations
    exit_code = 0 if compliant == total else 1
    sys.exit(exit_code)


if __name__ == "__main__":
    main()










