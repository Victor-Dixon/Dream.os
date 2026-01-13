#!/usr/bin/env python3
"""
Final Validation Workflow Automation Script

Executes the complete final validation workflow:
1. Verify readiness (optional but recommended)
2. Execute final validation
3. Populate validation report
4. Generate completion milestone template

Usage:
    python tools/execute_final_validation_workflow.py [--skip-verification]
"""

# SSOT Domain: tools

import argparse
import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent


def run_command(cmd: list, description: str) -> bool:
    """Run a command and return success status."""
    print(f"\n{'='*60}")
    print(f"Step: {description}")
    print(f"{'='*60}")
    print(f"Command: {' '.join(cmd)}")
    print()
    
    try:
        result = subprocess.run(
            cmd,
            cwd=PROJECT_ROOT,
            check=True,
            capture_output=True,
            text=True
        )
        print(result.stdout)
        if result.stderr:
            print("Warnings/Errors:", result.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        print(f"Output: {e.stdout}")
        print(f"Error: {e.stderr}")
        return False


def verify_readiness() -> bool:
    """Run readiness verification script."""
    cmd = [
        sys.executable,
        str(PROJECT_ROOT / "tools" / "verify_final_validation_readiness.py")
    ]
    return run_command(cmd, "Verify Readiness")


def execute_validation() -> bool:
    """Execute final validation."""
    output_file = PROJECT_ROOT / "docs" / "SSOT" / "FINAL_PHASE3_VALIDATION_REPORT.json"
    cmd = [
        sys.executable,
        str(PROJECT_ROOT / "tools" / "validate_all_ssot_files.py"),
        "--output",
        str(output_file)
    ]
    return run_command(cmd, "Execute Final Validation")


def populate_report() -> bool:
    """Populate validation report from JSON results."""
    json_file = PROJECT_ROOT / "docs" / "SSOT" / "FINAL_PHASE3_VALIDATION_REPORT.json"
    template_file = PROJECT_ROOT / "docs" / "SSOT" / "FINAL_PHASE3_VALIDATION_REPORT_TEMPLATE.md"
    output_file = PROJECT_ROOT / "docs" / "SSOT" / "FINAL_PHASE3_VALIDATION_REPORT.md"
    
    cmd = [
        sys.executable,
        str(PROJECT_ROOT / "tools" / "populate_validation_report.py"),
        "--json",
        str(json_file),
        "--template",
        str(template_file),
        "--output",
        str(output_file)
    ]
    return run_command(cmd, "Populate Validation Report")


def generate_milestone_template() -> bool:
    """Generate completion milestone template with timestamp."""
    template_file = PROJECT_ROOT / "docs" / "SSOT" / "PHASE1_THROUGH_PHASE3_COMPLETION_MILESTONE_TEMPLATE.md"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = PROJECT_ROOT / "docs" / "SSOT" / f"PHASE1_THROUGH_PHASE3_COMPLETION_MILESTONE_{timestamp}.md"
    
    if not template_file.exists():
        print(f"❌ Template not found: {template_file}")
        return False
    
    # Copy template to output file
    content = template_file.read_text(encoding="utf-8")
    
    # Add timestamp to header
    content = content.replace(
        "# Phase 1-3 Completion Milestone",
        f"# Phase 1-3 Completion Milestone\n\n**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )
    
    output_file.write_text(content, encoding="utf-8")
    print(f"✅ Milestone template generated: {output_file}")
    print(f"   Next: Populate with validation results from {PROJECT_ROOT / 'docs' / 'SSOT' / 'FINAL_PHASE3_VALIDATION_REPORT.md'}")
    return True


def main():
    """Main workflow execution."""
    parser = argparse.ArgumentParser(
        description="Execute complete final validation workflow"
    )
    parser.add_argument(
        "--skip-verification",
        action="store_true",
        help="Skip readiness verification step"
    )
    args = parser.parse_args()
    
    print("=" * 60)
    print("Final Validation Workflow Automation")
    print("=" * 60)
    print()
    print("This script will execute:")
    print("  1. Verify readiness (optional)")
    print("  2. Execute final validation")
    print("  3. Populate validation report")
    print("  4. Generate completion milestone template")
    print()
    
    if not args.skip_verification:
        print("Starting with readiness verification...")
        if not verify_readiness():
            print("\n❌ Readiness verification failed. Use --skip-verification to proceed anyway.")
            response = input("Continue anyway? (y/N): ")
            if response.lower() != 'y':
                print("Aborted.")
                return 1
    else:
        print("Skipping readiness verification (--skip-verification flag set)")
    
    # Execute validation
    if not execute_validation():
        print("\n❌ Validation execution failed. Aborting workflow.")
        return 1
    
    # Populate report
    if not populate_report():
        print("\n❌ Report population failed. Aborting workflow.")
        return 1
    
    # Generate milestone template
    if not generate_milestone_template():
        print("\n⚠️  Milestone template generation failed (non-critical)")
    
    print("\n" + "=" * 60)
    print("✅ Workflow Complete!")
    print("=" * 60)
    print()
    print("Next Steps:")
    print("  1. Review validation report:")
    print(f"     {PROJECT_ROOT / 'docs' / 'SSOT' / 'FINAL_PHASE3_VALIDATION_REPORT.md'}")
    print()
    print("  2. Populate completion milestone with results")
    print()
    print("  3. Update MASTER_TASK_LOG with completion milestone")
    print()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

