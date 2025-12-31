#!/usr/bin/env python3
"""
Validation Completion Signal Handler

Automatically triggers integration pipeline when validation completes.
Can be called by Agent-6's validation execution script or run manually.

Usage:
    python tools/validation_completion_signal_handler.py [--validation-report PATH]

This script:
1. Verifies validation report exists
2. Executes integration pipeline automatically
3. Sends completion notification to Agent-6
"""

import sys
import subprocess
from pathlib import Path
from datetime import datetime

# Paths
REPO_ROOT = Path(__file__).parent.parent
VALIDATION_REPORT_JSON = REPO_ROOT / "docs" / "SSOT" / "FINAL_PHASE3_VALIDATION_REPORT.json"
INTEGRATION_PIPELINE = REPO_ROOT / "tools" / "validation_result_integration_pipeline.py"


def verify_validation_complete(report_path: Path) -> bool:
    """Verify validation report exists and contains results."""
    if not report_path.exists():
        return False
    
    try:
        import json
        with open(report_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Check for required fields
        return all(key in data for key in ['total_files', 'valid_files', 'invalid_files'])
    except Exception:
        return False


def execute_integration_pipeline(report_path: Path) -> bool:
    """Execute the integration pipeline."""
    print("🔄 Executing integration pipeline...")
    
    try:
        result = subprocess.run(
            [sys.executable, str(INTEGRATION_PIPELINE), '--validation-report', str(report_path)],
            cwd=REPO_ROOT,
            capture_output=False,
            text=True
        )
        
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error executing integration pipeline: {e}")
        return False


def main():
    """Main execution function."""
    # Parse command line arguments
    validation_report = VALIDATION_REPORT_JSON
    if len(sys.argv) > 1 and sys.argv[1] == '--validation-report':
        if len(sys.argv) > 2:
            validation_report = Path(sys.argv[2])
        else:
            print("❌ ERROR: --validation-report requires a path")
            sys.exit(1)
    
    print("🚀 Validation Completion Signal Handler")
    print("=" * 60)
    print(f"📊 Checking validation report: {validation_report}")
    
    # Verify validation complete
    if not verify_validation_complete(validation_report):
        print("⚠️  Validation report not found or incomplete")
        print("💡 Run validation first: python tools/execute_phase3_final_validation.py")
        sys.exit(1)
    
    print("✅ Validation report verified")
    
    # Execute integration pipeline
    print(f"\n🔄 Triggering integration pipeline...")
    success = execute_integration_pipeline(validation_report)
    
    if success:
        print("\n" + "=" * 60)
        print("✅ Signal Handler Complete")
        print(f"   Integration pipeline executed successfully")
        print(f"   Milestone: docs/SSOT/PHASE1_THROUGH_PHASE3_COMPLETION_MILESTONE.md")
        print(f"   Task Log: MASTER_TASK_LOG.md")
        print("\n🎯 Next Steps:")
        print("   1. Review generated milestone document")
        print("   2. Commit integration updates")
        print("   3. Notify Agent-6 of completion")
    else:
        print("\n❌ Integration pipeline failed")
        sys.exit(1)


if __name__ == '__main__':
    main()

