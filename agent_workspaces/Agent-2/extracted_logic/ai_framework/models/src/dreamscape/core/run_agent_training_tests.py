#!/usr/bin/env python3
"""
Agent Training Test Runner
==========================

Simple script to run agent training system tests with nice output formatting.
"""

import sys
import subprocess
from pathlib import Path

def main():
    """Run agent training tests with formatted output."""
    print("🧪 Running Agent Training System Tests")
    print("=" * 50)
    
    # Get the project root
    project_root = Path(__file__).parent.parent
    
    # Run the tests
    cmd = [
        sys.executable, "-m", "pytest",
        "tests/integration/test_agent_training_system.py",
        "-v",
        "--tb=short",
        "--color=yes"
    ]
    
    try:
        result = subprocess.run(cmd, cwd=project_root, capture_output=True, text=True)
        
        # Print output
        if result.stdout:
            print(result.stdout)
        
        if result.stderr:
            print("Warnings/Errors:")
            print(result.stderr)
        
        # Print summary
        print("\n" + "=" * 50)
        if result.returncode == 0:
            print("✅ All agent training tests passed!")
            print("🎉 The agent training system is working correctly.")
        else:
            print("❌ Some agent training tests failed.")
            print("🔧 Check the output above for details.")
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 