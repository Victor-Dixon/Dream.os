#!/usr/bin/env python3
"""
V2 Compliance Validation Script
===============================

Validates code against V2 compliance rules.

Author: Agent-2 (Architecture & Design Specialist)
Date: 2025-12-11
V2 Compliant: Yes
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

try:
    import yaml
except ImportError:
    print("❌ ERROR: pyyaml not installed. Install with: pip install pyyaml")
    sys.exit(1)


def validate_v2_compliance(rules_file: Optional[Path] = None) -> int:
    """
    Validate V2 compliance.
    
    Args:
        rules_file: Path to V2 rules YAML file (optional)
        
    Returns:
        Exit code (0 = success, 1 = failure)
    """
    project_root = Path(__file__).parent.parent
    
    # Load rules if provided
    if rules_file and rules_file.exists():
        try:
            with open(rules_file, 'r', encoding='utf-8') as f:
                rules = yaml.safe_load(f)
            print(f"✅ Loaded V2 rules from {rules_file}")
        except Exception as e:
            print(f"⚠️  Warning: Could not load rules file: {e}")
            rules = None
    else:
        rules = None
        if rules_file:
            print(f"⚠️  Warning: Rules file not found: {rules_file}")
    
    # Basic V2 compliance checks
    issues = []
    
    # Check for files exceeding LOC limits
    src_dir = project_root / "src"
    if src_dir.exists():
        for py_file in src_dir.rglob("*.py"):
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    line_count = len(lines)
                    
                    # V2 limits: 300 lines per file
                    if line_count > 300:
                        issues.append(
                            f"⚠️  {py_file.relative_to(project_root)}: "
                            f"{line_count} lines (limit: 300)"
                        )
            except Exception:
                continue
    
    # Report results
    if issues:
        print(f"\n⚠️  Found {len(issues)} V2 compliance issues:")
        for issue in issues[:10]:  # Show first 10
            print(f"  {issue}")
        if len(issues) > 10:
            print(f"  ... and {len(issues) - 10} more")
        print("\n💡 Consider refactoring large files to meet V2 standards")
        return 1
    else:
        print("✅ V2 compliance validation passed")
        return 0


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Validate V2 compliance"
    )
    parser.add_argument(
        "--rules",
        type=Path,
        help="Path to V2 rules YAML file",
        default=Path("config/v2_rules.yaml")
    )
    
    args = parser.parse_args()
    
    exit_code = validate_v2_compliance(args.rules)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()



