#!/usr/bin/env python3
"""
Quick Validation Runner for FastAPI Refactoring
===============================================

Fast feedback validation for Agent-1's fastapi_app.py modularization.
Run immediately after commits to provide quality assurance.

Author: Agent-4 (Captain - Strategic Coordination)
Date: 2026-01-08
"""

import subprocess
import sys
from pathlib import Path

def run_validation():
    """Run fastapi validation and return results."""
    print("🚀 Running FastAPI Refactoring Validation...")

    try:
        result = subprocess.run([
            sys.executable, "validation_framework_fastapi_refactor.py"
        ], capture_output=True, text=True, timeout=30)

        print("📊 VALIDATION RESULTS:")
        print(result.stdout)

        if result.stderr:
            print("⚠️  WARNINGS/ERRORS:")
            print(result.stderr)

        # Return success/failure
        return result.returncode == 0

    except subprocess.TimeoutExpired:
        print("❌ VALIDATION TIMEOUT - Check for infinite loops or hangs")
        return False
    except Exception as e:
        print(f"❌ VALIDATION ERROR: {e}")
        return False

def check_git_status():
    """Check git status for recent commits."""
    try:
        result = subprocess.run([
            "git", "log", "--oneline", "-3"
        ], capture_output=True, text=True, cwd=Path(__file__).parent)

        if result.returncode == 0:
            print("📝 RECENT COMMITS:")
            print(result.stdout)
        else:
            print("⚠️  Could not check git status")

    except Exception as e:
        print(f"⚠️  Git check failed: {e}")

if __name__ == "__main__":
    print("🔍 FASTAPI REFACTORING QUICK VALIDATION")
    print("=" * 50)

    check_git_status()
    print()

    success = run_validation()

    print("=" * 50)
    if success:
        print("✅ VALIDATION PASSED - Modularization looks good!")
        print("🐝 Ready for next modularization phase")
    else:
        print("❌ VALIDATION FAILED - Review modularization")
        print("🔧 Agent-1: Check validation errors above")

    sys.exit(0 if success else 1)