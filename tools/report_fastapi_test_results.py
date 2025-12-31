#!/usr/bin/env python3
"""
FastAPI Test Result Reporter
Formats and reports test results for coordination handoff.

Usage:
    python tools/report_fastapi_test_results.py <test_results.json>
    
Or pipe from test execution:
    python tools/execute_fastapi_tests_immediate.py | python tools/report_fastapi_test_results.py
"""

import json
import sys
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

PROJECT_ROOT = Path(__file__).parent.parent


def load_test_results(results_file: str) -> Dict[str, Any]:
    """Load test results from JSON file."""
    results_path = Path(results_file)
    if not results_path.exists():
        # Try relative to agent workspace
        results_path = PROJECT_ROOT / "agent_workspaces" / "Agent-1" / results_file
        if not results_path.exists():
            raise FileNotFoundError(f"Test results file not found: {results_file}")
    
    with open(results_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def format_results_for_coordination(results: Dict[str, Any]) -> str:
    """Format test results for Agent-4 and Agent-7 coordination."""
    report = []
    report.append("=" * 70)
    report.append("FASTAPI INTEGRATION TEST RESULTS")
    report.append("=" * 70)
    report.append(f"Timestamp: {results.get('timestamp', 'Unknown')}")
    report.append(f"Endpoint: {results.get('endpoint', 'Unknown')}")
    report.append()
    
    # Test execution status
    if results.get("success"):
        report.append("✅ TEST EXECUTION: PASSED")
    else:
        report.append("❌ TEST EXECUTION: FAILED")
        if "error" in results:
            report.append(f"   Error: {results['error']}")
    report.append()
    
    # Test output summary
    if "stdout" in results and results["stdout"]:
        report.append("TEST OUTPUT SUMMARY:")
        report.append("-" * 70)
        
        # Extract key metrics from pytest output
        stdout_lines = results["stdout"].split('\n')
        for line in stdout_lines:
            if any(keyword in line for keyword in ["passed", "failed", "error", "PASSED", "FAILED", "ERROR"]):
                report.append(f"  {line}")
        
        report.append()
    
    # WordPress endpoint status (for Agent-7)
    report.append("WORDPRESS ENDPOINT STATUS (for Agent-7 verification):")
    report.append("-" * 70)
    if results.get("success"):
        report.append("✅ FastAPI service is operational")
        report.append("✅ WordPress endpoints should now return 200 (account, positions)")
        report.append("   Agent-7 can verify: /wp-json/tradingrobotplug/v1/account")
        report.append("   Agent-7 can verify: /wp-json/tradingrobotplug/v1/positions")
    else:
        report.append("❌ FastAPI service not operational")
        report.append("   WordPress endpoints will return 500 until FastAPI is connected")
    report.append()
    
    # Coordination handoff
    report.append("COORDINATION HANDOFF:")
    report.append("-" * 70)
    report.append("Agent-4: FastAPI test execution complete")
    if results.get("success"):
        report.append("Agent-7: Ready for WordPress endpoint verification")
        report.append("   → Verify /wp-json/tradingrobotplug/v1/account returns 200")
        report.append("   → Verify /wp-json/tradingrobotplug/v1/positions returns 200")
    else:
        report.append("Agent-7: Wait for FastAPI service to be ready")
    report.append()
    
    report.append("=" * 70)
    
    return "\n".join(report)


def save_coordination_report(report: str, output_file: str = None):
    """Save coordination report to file."""
    if output_file is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"agent_workspaces/Agent-1/trading_robot_phase3_coordination_report_{timestamp}.md"
    
    output_path = PROJECT_ROOT / output_file
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    return output_path


def main():
    parser = argparse.ArgumentParser(description="Format and report FastAPI test results for coordination")
    parser.add_argument("results_file", nargs="?", help="Test results JSON file")
    parser.add_argument("--output", help="Output file for coordination report")
    parser.add_argument("--print", action="store_true", help="Print report to stdout")
    args = parser.parse_args()
    
    # Load results
    if args.results_file:
        results = load_test_results(args.results_file)
    else:
        # Try to find latest results file
        results_dir = PROJECT_ROOT / "agent_workspaces" / "Agent-1"
        result_files = sorted(results_dir.glob("trading_robot_phase3_fastapi_test_results_*.json"))
        if result_files:
            results = load_test_results(str(result_files[-1]))
            print(f"📄 Using latest results file: {result_files[-1].name}")
        else:
            print("❌ No test results file found. Run tests first or specify --results-file")
            sys.exit(1)
    
    # Format report
    report = format_results_for_coordination(results)
    
    # Save report
    output_path = save_coordination_report(report, args.output)
    print(f"📊 Coordination report saved to: {output_path}")
    
    # Print if requested
    if args.print:
        print("\n" + report)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

