#!/usr/bin/env python3
"""
Conversion Funnel Test Runner
=============================

Runs conversion funnel tests and generates test report.

Usage:
    python run_conversion_funnel_tests.py [--verbose] [--coverage]
"""

import sys
import os
import pytest
from datetime import datetime
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

def main():
    """Run conversion funnel tests."""
    print("🧪 Conversion Funnel Test Suite")
    print("=" * 60)
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Test file
    test_file = Path(__file__).parent / "test_conversion_funnel.py"
    
    # Pytest arguments
    pytest_args = [
        str(test_file),
        '-v',  # Verbose
        '--tb=short',  # Short traceback
        '-r', 'fE',  # Show failures and errors
    ]
    
    # Add coverage if requested
    if '--coverage' in sys.argv:
        pytest_args.extend(['--cov=trading_robot', '--cov-report=html'])
    
    # Run tests
    exit_code = pytest.main(pytest_args)
    
    print()
    print("=" * 60)
    if exit_code == 0:
        print("✅ All tests passed!")
    else:
        print(f"❌ Tests failed with exit code: {exit_code}")
    
    return exit_code

if __name__ == '__main__':
    sys.exit(main())

