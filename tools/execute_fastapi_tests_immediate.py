#!/usr/bin/env python3
"""
Immediate FastAPI Test Execution Script
Executes FastAPI integration tests when service is ready.

Usage:
    python tools/execute_fastapi_tests_immediate.py [--endpoint URL]
    
Default endpoint: http://localhost:8000
"""

import subprocess
import sys
import argparse
import json
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent
TEST_SUITE = "tests/integration/trading_robot/test_phase3_integration.py"


def check_service_health(endpoint: str = "http://localhost:8000") -> bool:
    """Check if FastAPI service is responding."""
    try:
        import requests
        response = requests.get(f"{endpoint}/health", timeout=5)
        return response.status_code == 200
    except Exception:
        return False


def execute_fastapi_tests(endpoint: str = "http://localhost:8000", verbose: bool = True) -> dict:
    """Execute FastAPI integration tests."""
    test_command = [
        "pytest",
        f"{TEST_SUITE}::TestFastAPIIntegration",
        "-v" if verbose else "",
        "--tb=short"
    ]
    test_command = [c for c in test_command if c]  # Remove empty strings
    
    print(f"🚀 Executing FastAPI integration tests...")
    print(f"   Endpoint: {endpoint}")
    print(f"   Test suite: {TEST_SUITE}")
    print()
    
    try:
        result = subprocess.run(
            test_command,
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        return {
            "success": result.returncode == 0,
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "endpoint": endpoint,
            "timestamp": datetime.now().isoformat()
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": "Test execution timed out (5 minutes)",
            "endpoint": endpoint,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "endpoint": endpoint,
            "timestamp": datetime.now().isoformat()
        }


def save_results(results: dict, output_file: str = None):
    """Save test results to file."""
    if output_file is None:
        output_file = f"agent_workspaces/Agent-1/trading_robot_phase3_fastapi_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    output_path = PROJECT_ROOT / output_file
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    
    return output_path


def main():
    parser = argparse.ArgumentParser(description="Execute FastAPI integration tests immediately")
    parser.add_argument("--endpoint", default="http://localhost:8001", help="FastAPI endpoint URL")
    parser.add_argument("--skip-health-check", action="store_true", help="Skip health check before tests")
    parser.add_argument("--output", help="Output file for results JSON")
    args = parser.parse_args()
    
    # Health check
    if not args.skip_health_check:
        print("🔍 Checking FastAPI service health...")
        if not check_service_health(args.endpoint):
            print(f"❌ Service not responding at {args.endpoint}/health")
            print("   Waiting for service to be ready...")
            sys.exit(1)
        print("✅ Service health check passed")
        print()
    
    # Execute tests
    results = execute_fastapi_tests(args.endpoint)
    
    # Save results
    output_path = save_results(results, args.output)
    print(f"\n📊 Results saved to: {output_path}")
    
    # Print summary
    print("\n" + "="*60)
    if results["success"]:
        print("✅ All FastAPI integration tests PASSED")
    else:
        print("❌ Some tests FAILED or ERRORED")
        if "error" in results:
            print(f"   Error: {results['error']}")
    print("="*60)
    
    # Print test output
    if "stdout" in results and results["stdout"]:
        print("\nTest Output:")
        print(results["stdout"])
    
    if "stderr" in results and results["stderr"]:
        print("\nTest Errors:")
        print(results["stderr"])
    
    sys.exit(0 if results["success"] else 1)


if __name__ == "__main__":
    main()

