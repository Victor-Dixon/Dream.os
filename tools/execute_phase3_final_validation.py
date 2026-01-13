#!/usr/bin/env python3
"""
Phase 3 Final Validation Execution Script

Automates the complete validation process after all Phase 3 files are fixed.
Run this script when Agent-2 completes (or all 44 files are fixed).

Usage:
    python tools/execute_phase3_final_validation.py

Output:
    - docs/SSOT/FINAL_PHASE3_VALIDATION_REPORT.json (raw validation results)
    - docs/SSOT/FINAL_PHASE3_VALIDATION_REPORT.md (formatted report)
    - Console output with success/failure status
"""

import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime

# Paths
REPO_ROOT = Path(__file__).parent.parent
VALIDATION_TOOL = REPO_ROOT / "tools" / "validate_all_ssot_files.py"
OUTPUT_DIR = REPO_ROOT / "docs" / "SSOT"
JSON_REPORT = OUTPUT_DIR / "FINAL_PHASE3_VALIDATION_REPORT.json"
MARKDOWN_REPORT = OUTPUT_DIR / "FINAL_PHASE3_VALIDATION_REPORT.md"
TEMPLATE = OUTPUT_DIR / "FINAL_PHASE3_VALIDATION_REPORT_TEMPLATE.md"

# Phase 2 baseline
PHASE2_VALID = 1309
PHASE2_TOTAL = 1369
PHASE2_SUCCESS_RATE = 95.62

def run_validation():
    """Run comprehensive validation and find the generated JSON report."""
    print("🔍 Running comprehensive SSOT validation...")
    
    try:
        result = subprocess.run(
            [sys.executable, str(VALIDATION_TOOL)],
            capture_output=True,
            text=True,
            cwd=REPO_ROOT
        )
        
        # Validation tool writes JSON to timestamped file - find the latest one
        report_dir = REPO_ROOT / "docs" / "SSOT"
        json_files = sorted(report_dir.glob("FINAL_VALIDATION_CHECKPOINT_*.json"), reverse=True)
        
        if not json_files:
            print("❌ No validation report JSON file found")
            if result.returncode != 0:
                print(f"⚠️  Validation tool returned exit code {result.returncode}")
            return None
        
        # Use the latest report file
        latest_report = json_files[0]
        
        # Copy to our expected location
        import shutil
        shutil.copy2(latest_report, JSON_REPORT)
        
        print(f"✅ Validation complete. Report: {latest_report.name}")
        print(f"📄 Copied to: {JSON_REPORT.name}")
        
        # Read and return the JSON data
        with open(JSON_REPORT, 'r', encoding='utf-8') as f:
            return json.load(f)
        
    except Exception as e:
        print(f"❌ Error running validation: {e}")
        return None

def parse_validation_results(data):
    """Parse validation JSON data to extract key metrics."""
    try:
        if isinstance(data, dict):
            return {
                'total': data.get('total_files', 0),
                'valid': data.get('valid_files', 0),
                'invalid': data.get('invalid_files', 0),
                'success_rate': data.get('success_rate', 0.0)
            }
        return None
    except Exception as e:
        print(f"⚠️  Error parsing results: {e}")
        return None

def generate_report(metrics):
    """Generate formatted markdown report from metrics."""
    if not metrics:
        print("⚠️  Cannot generate report: metrics unavailable")
        return False
    
    total = metrics.get('total', 0)
    valid = metrics.get('valid', 0)
    invalid = metrics.get('invalid', 0)
    success_rate = metrics.get('success_rate', 0.0)
    
    improvement = success_rate - PHASE2_SUCCESS_RATE
    overall_improvement = success_rate - 57.75  # Baseline from Phase 1
    
    # Pre-compute values to avoid backslashes in f-string expressions
    generated_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
    status_text = '✅ PASS' if invalid == 0 else '⚠️  PARTIAL'
    success_text = '✅ **SUCCESS:** All files valid. Phase 3 remediation complete.' if invalid == 0 else f'⚠️  **PARTIAL:** {invalid} files still need attention.'
    next_steps_text = '✅ Phase 3 complete. Ready for milestone closure.' if invalid == 0 else f'1. Review invalid files in {JSON_REPORT.name}\n2. Assign remaining files to domain owners\n3. Re-run validation after fixes'
    generated_iso = datetime.utcnow().isoformat()
    
    report = f"""# Final Phase 3 Validation Report

**Generated:** {generated_time}  
**Validation Tool:** `tools/validate_all_ssot_files.py`  
**Status:** {status_text}

---

## Executive Summary

**Total Files Scanned:** {total}  
**Valid Files:** {valid} ({success_rate:.2f}%)  
**Invalid Files:** {invalid} ({100-success_rate:.2f}%)  
**Success Rate:** {success_rate:.2f}%

---

## Phase Comparison

| Phase | Valid Files | Total Files | Success Rate | Improvement |
|-------|-----------|-------------|--------------|-------------|
| Phase 1 (Baseline) | 1,040 | 1,801 | 57.75% | - |
| Phase 2 (After Registry Update) | {PHASE2_VALID} | {PHASE2_TOTAL} | {PHASE2_SUCCESS_RATE:.2f}% | +37.87% |
| Phase 3 (After Remediation) | {valid} | {total} | {success_rate:.2f}% | {improvement:+.2f}% |

**Overall Improvement from Baseline:** {overall_improvement:+.2f}%

---

## Validation Results

{success_text}

### Next Steps

{next_steps_text}

---

## Detailed Results

**Full validation report:** `{JSON_REPORT.name}`  
**Generated:** {generated_iso}
"""
    
    with open(MARKDOWN_REPORT, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"✅ Report generated: {MARKDOWN_REPORT}")
    return True

def main():
    """Main execution flow."""
    print("=" * 70)
    print("Phase 3 Final Validation Execution")
    print("=" * 70)
    print()
    
    # Step 1: Run validation
    validation_data = run_validation()
    if not validation_data:
        print("❌ Validation failed. Check output above.")
        return 1
    
    # Step 2: Parse results
    print("\n📊 Parsing validation results...")
    metrics = parse_validation_results(validation_data)
    
    if not metrics:
        print("⚠️  Could not parse metrics. Check JSON report manually.")
        return 1
    
    # Step 3: Generate report
    print("\n📝 Generating validation report...")
    if not generate_report(metrics):
        return 1
    
    # Step 4: Summary
    print("\n" + "=" * 70)
    print("VALIDATION SUMMARY")
    print("=" * 70)
    print(f"Total Files: {metrics.get('total', 0)}")
    print(f"Valid Files: {metrics.get('valid', 0)} ({metrics.get('success_rate', 0):.2f}%)")
    print(f"Invalid Files: {metrics.get('invalid', 0)}")
    
    # Step 5: Auto-trigger integration pipeline (Agent-8 coordination)
    if metrics.get('invalid', 0) == 0:
        print("\n✅ SUCCESS: All files valid. Phase 3 complete!")
        print("\n🔄 Triggering integration pipeline (Agent-8 coordination)...")
        
        SIGNAL_HANDLER = REPO_ROOT / "tools" / "validation_completion_signal_handler.py"
        if SIGNAL_HANDLER.exists():
            try:
                result = subprocess.run(
                    [sys.executable, str(SIGNAL_HANDLER), '--validation-report', str(JSON_REPORT)],
                    cwd=REPO_ROOT,
                    capture_output=False,
                    text=True
                )
                if result.returncode == 0:
                    print("✅ Integration pipeline complete: milestone generated, MASTER_TASK_LOG updated")
                else:
                    print("⚠️  Integration pipeline completed with warnings (check output above)")
            except Exception as e:
                print(f"⚠️  Integration pipeline error: {e}")
                print("💡 Run manually: python tools/validation_completion_signal_handler.py")
        else:
            print("⚠️  Signal handler not found. Run integration manually:")
            print(f"   python tools/validation_result_integration_pipeline.py --validation-report {JSON_REPORT}")
        
        return 0
    else:
        print(f"\n⚠️  {metrics.get('invalid', 0)} files still need attention.")
        print(f"📄 See {JSON_REPORT.name} for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

