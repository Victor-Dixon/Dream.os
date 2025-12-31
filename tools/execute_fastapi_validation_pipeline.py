#!/usr/bin/env python3
"""
FastAPI Validation Pipeline - Complete End-to-End Automation
Verifies service, executes tests, and formats results for coordination handoff.

Usage:
    python tools/execute_fastapi_validation_pipeline.py [--endpoint URL] [--skip-verify]
    
This script automates the complete validation workflow:
1. Verify FastAPI service is ready
2. Execute integration tests
3. Format results for coordination handoff
4. Generate coordination report
"""

import sys
import subprocess
import argparse
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent


def run_command(cmd: list, description: str) -> tuple[bool, str]:
    """Run a command and return success status and output."""
    print(f"\n{'='*70}")
    print(f"STEP: {description}")
    print(f"{'='*70}")
    print(f"Command: {' '.join(cmd)}")
    print()
    
    try:
        result = subprocess.run(
            cmd,
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            timeout=600  # 10 minute timeout
        )
        
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        
        return result.returncode == 0, result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        print(f"❌ Command timed out after 10 minutes")
        return False, "Command timed out"
    except Exception as e:
        print(f"❌ Error: {e}")
        return False, str(e)


def execute_pipeline(endpoint: str = "http://localhost:8001", skip_verify: bool = False):
    """Execute complete validation pipeline."""
    print("="*70)
    print("FASTAPI VALIDATION PIPELINE")
    print("="*70)
    print(f"Endpoint: {endpoint}")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print()
    
    pipeline_results = {
        "endpoint": endpoint,
        "timestamp": datetime.now().isoformat(),
        "steps": {}
    }
    
    # Step 1: Verify service (unless skipped)
    if not skip_verify:
        success, output = run_command(
            [sys.executable, "tools/verify_fastapi_service_ready.py", "--endpoint", endpoint],
            "Service Verification"
        )
        pipeline_results["steps"]["verification"] = {
            "success": success,
            "output": output
        }
        
        if not success:
            print("\n❌ Service verification failed. Pipeline stopped.")
            print("   Fix service issues before proceeding.")
            return False, pipeline_results
    
    # Step 2: Execute tests
    success, output = run_command(
        [sys.executable, "tools/execute_fastapi_tests_immediate.py", "--endpoint", endpoint],
        "Test Execution"
    )
    pipeline_results["steps"]["test_execution"] = {
        "success": success,
        "output": output
    }
    
    if not success:
        print("\n⚠️  Test execution completed with errors")
        print("   Continuing to result reporting...")
    
    # Step 3: Format results for coordination
    success, output = run_command(
        [sys.executable, "tools/report_fastapi_test_results.py", "--print"],
        "Result Formatting for Coordination"
    )
    pipeline_results["steps"]["result_reporting"] = {
        "success": success,
        "output": output
    }
    
    # Summary
    print("\n" + "="*70)
    print("PIPELINE SUMMARY")
    print("="*70)
    
    all_steps = list(pipeline_results["steps"].keys())
    passed_steps = [step for step, data in pipeline_results["steps"].items() if data["success"]]
    
    for step in all_steps:
        status = "✅ PASS" if pipeline_results["steps"][step]["success"] else "❌ FAIL"
        print(f"{status} - {step.replace('_', ' ').title()}")
    
    print()
    if len(passed_steps) == len(all_steps):
        print("✅ Complete pipeline executed successfully")
        print("   Results ready for Agent-4 coordination handoff")
    else:
        print(f"⚠️  Pipeline completed with {len(all_steps) - len(passed_steps)} failed step(s)")
        print("   Review output above for details")
    
    print("="*70)
    
    return len(passed_steps) == len(all_steps), pipeline_results


def main():
    parser = argparse.ArgumentParser(
        description="Execute complete FastAPI validation pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Complete automation workflow:
  1. Verify FastAPI service is ready
  2. Execute integration tests
  3. Format results for coordination handoff
  
All steps are automated. Results are saved and formatted for Agent-4/Agent-7 coordination.
        """
    )
    parser.add_argument("--endpoint", default="http://localhost:8001", help="FastAPI endpoint URL")
    parser.add_argument("--skip-verify", action="store_true", help="Skip service verification step")
    args = parser.parse_args()
    
    success, results = execute_pipeline(args.endpoint, args.skip_verify)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

