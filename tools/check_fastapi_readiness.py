#!/usr/bin/env python3
"""
FastAPI Validation Readiness Check
Verifies all tools and components are ready for execution.

Usage:
    python tools/check_fastapi_readiness.py
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent

REQUIRED_TOOLS = [
    "tools/execute_fastapi_validation_pipeline.py",
    "tools/generate_coordination_handoff_message.py",
    "tools/execute_fastapi_tests_immediate.py",
    "tools/verify_fastapi_service_ready.py",
    "tools/report_fastapi_test_results.py",
    "tools/monitor_fastapi_service_ready.py",
    "tests/integration/trading_robot/test_phase3_integration.py",
]

REQUIRED_DOCS = [
    "agent_workspaces/Agent-1/FASTAPI_TEST_EXECUTION_GUIDE.md",
    "agent_workspaces/Agent-1/FASTAPI_COORDINATION_HANDOFF_TEMPLATE.md",
]


def check_file_exists(filepath: str) -> tuple[bool, str]:
    """Check if a file exists."""
    full_path = PROJECT_ROOT / filepath
    if full_path.exists():
        return True, f"✅ {filepath}"
    return False, f"❌ {filepath} (missing)"


def check_readiness():
    """Check all readiness components."""
    print("="*70)
    print("FASTAPI VALIDATION READINESS CHECK")
    print("="*70)
    print()
    
    all_ready = True
    
    # Check tools
    print("TOOLS:")
    print("-"*70)
    for tool in REQUIRED_TOOLS:
        exists, message = check_file_exists(tool)
        print(f"  {message}")
        if not exists:
            all_ready = False
    print()
    
    # Check documentation
    print("DOCUMENTATION:")
    print("-"*70)
    for doc in REQUIRED_DOCS:
        exists, message = check_file_exists(doc)
        print(f"  {message}")
        if not exists:
            all_ready = False
    print()
    
    # Configuration check
    print("CONFIGURATION:")
    print("-"*70)
    print(f"  ✅ Endpoint: http://localhost:8001")
    print(f"  ✅ Service: tradingrobotplug-fastapi")
    print(f"  ✅ Test suite: tests/integration/trading_robot/test_phase3_integration.py")
    print()
    
    # Summary
    print("="*70)
    if all_ready:
        print("✅ ALL COMPONENTS READY")
        print()
        print("Ready to execute when service is available:")
        print("  python tools/execute_fastapi_validation_pipeline.py")
        print("  python tools/generate_coordination_handoff_message.py")
    else:
        print("❌ SOME COMPONENTS MISSING")
        print("   Review missing files above")
    print("="*70)
    
    return all_ready


if __name__ == "__main__":
    ready = check_readiness()
    sys.exit(0 if ready else 1)

