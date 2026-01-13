#!/usr/bin/env python3
"""
Final Validation Readiness Verification Script

Verifies all prerequisites for final SSOT validation execution.
Checks Phase 3 completion, validation tool readiness, and documentation preparation.

Usage:
    python tools/verify_final_validation_readiness.py
"""

# SSOT Domain: tools

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Tuple

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent


def check_phase3_completion() -> Tuple[bool, List[str]]:
    """Check if Phase 3 remediation is complete."""
    issues = []
    
    progress_tracker = PROJECT_ROOT / "docs/SSOT/PHASE3_PROGRESS_TRACKER.md"
    if not progress_tracker.exists():
        issues.append("❌ Progress tracker not found")
        return False, issues
    
    # Read progress tracker
    content = progress_tracker.read_text(encoding="utf-8")
    
    # Check for completion indicators
    if "44/44 complete" in content or "100%" in content:
        print("✅ Phase 3 completion verified in progress tracker")
    else:
        # Extract current progress
        if "complete" in content.lower():
            # Try to extract numbers
            import re
            matches = re.findall(r'(\d+)/44.*complete', content, re.IGNORECASE)
            if matches:
                completed = int(matches[0])
                if completed < 44:
                    issues.append(f"⚠️  Phase 3 not complete: {completed}/44 files complete")
                else:
                    print("✅ Phase 3 completion verified")
            else:
                issues.append("⚠️  Cannot verify Phase 3 completion from progress tracker")
        else:
            issues.append("⚠️  Phase 3 completion status unclear")
    
    return len(issues) == 0, issues


def check_validation_tool() -> Tuple[bool, List[str]]:
    """Check if validation tool is ready."""
    issues = []
    
    validation_tool = PROJECT_ROOT / "tools/validate_all_ssot_files.py"
    if not validation_tool.exists():
        issues.append("❌ Validation tool not found")
        return False, issues
    
    # Check if tool is executable
    if not os.access(validation_tool, os.R_OK):
        issues.append("❌ Validation tool not readable")
    
    print("✅ Validation tool found and accessible")
    return True, issues


def check_report_script() -> Tuple[bool, List[str]]:
    """Check if report population script is ready."""
    issues = []
    
    report_script = PROJECT_ROOT / "tools/populate_validation_report.py"
    if not report_script.exists():
        issues.append("❌ Report population script not found")
        return False, issues
    
    # Check if script is executable
    if not os.access(report_script, os.R_OK):
        issues.append("❌ Report population script not readable")
    
    print("✅ Report population script found and accessible")
    return True, issues


def check_documentation_templates() -> Tuple[bool, List[str]]:
    """Check if documentation templates are ready."""
    issues = []
    
    templates = [
        "docs/SSOT/FINAL_PHASE3_VALIDATION_REPORT_TEMPLATE.md",
        "docs/SSOT/PHASE1_THROUGH_PHASE3_COMPLETION_MILESTONE_TEMPLATE.md",
        "docs/SSOT/FINAL_VALIDATION_EXECUTION_GUIDE.md",
    ]
    
    for template_path in templates:
        template = PROJECT_ROOT / template_path
        if not template.exists():
            issues.append(f"❌ Template not found: {template_path}")
        else:
            print(f"✅ Template found: {template_path}")
    
    return len(issues) == 0, issues


def check_output_directories() -> Tuple[bool, List[str]]:
    """Check if output directories exist and are writable."""
    issues = []
    
    output_dir = PROJECT_ROOT / "docs/SSOT"
    if not output_dir.exists():
        issues.append("❌ Output directory not found: docs/SSOT")
        return False, issues
    
    if not os.access(output_dir, os.W_OK):
        issues.append("❌ Output directory not writable: docs/SSOT")
    
    print("✅ Output directory exists and is writable")
    return True, issues


def main():
    """Main verification function."""
    print("=" * 60)
    print("Final Validation Readiness Verification")
    print("=" * 60)
    print()
    
    all_checks = []
    all_issues = []
    
    # Check Phase 3 completion
    print("Checking Phase 3 completion...")
    phase3_ok, phase3_issues = check_phase3_completion()
    all_checks.append(("Phase 3 Completion", phase3_ok))
    all_issues.extend(phase3_issues)
    print()
    
    # Check validation tool
    print("Checking validation tool...")
    tool_ok, tool_issues = check_validation_tool()
    all_checks.append(("Validation Tool", tool_ok))
    all_issues.extend(tool_issues)
    print()
    
    # Check report script
    print("Checking report population script...")
    script_ok, script_issues = check_report_script()
    all_checks.append(("Report Script", script_ok))
    all_issues.extend(script_issues)
    print()
    
    # Check documentation templates
    print("Checking documentation templates...")
    templates_ok, template_issues = check_documentation_templates()
    all_checks.append(("Documentation Templates", templates_ok))
    all_issues.extend(template_issues)
    print()
    
    # Check output directories
    print("Checking output directories...")
    dirs_ok, dir_issues = check_output_directories()
    all_checks.append(("Output Directories", dirs_ok))
    all_issues.extend(dir_issues)
    print()
    
    # Summary
    print("=" * 60)
    print("Verification Summary")
    print("=" * 60)
    
    for check_name, check_ok in all_checks:
        status = "✅ PASS" if check_ok else "❌ FAIL"
        print(f"{status}: {check_name}")
    
    print()
    
    if all_issues:
        print("Issues Found:")
        for issue in all_issues:
            print(f"  {issue}")
        print()
        print("❌ NOT READY: Please resolve issues before executing final validation")
        return 1
    else:
        print("✅ ALL CHECKS PASSED: Ready for final validation execution")
        print()
        print("Next Steps:")
        print("  1. Execute final validation:")
        print("     python tools/validate_all_ssot_files.py --output docs/SSOT/FINAL_PHASE3_VALIDATION_REPORT.json")
        print()
        print("  2. Populate validation report:")
        print("     python tools/populate_validation_report.py \\")
        print("       --json docs/SSOT/FINAL_PHASE3_VALIDATION_REPORT.json \\")
        print("       --template docs/SSOT/FINAL_PHASE3_VALIDATION_REPORT_TEMPLATE.md \\")
        print("       --output docs/SSOT/FINAL_PHASE3_VALIDATION_REPORT.md")
        print()
        print("  3. Generate completion milestone using:")
        print("     docs/SSOT/PHASE1_THROUGH_PHASE3_COMPLETION_MILESTONE_TEMPLATE.md")
        return 0


if __name__ == "__main__":
    sys.exit(main())

