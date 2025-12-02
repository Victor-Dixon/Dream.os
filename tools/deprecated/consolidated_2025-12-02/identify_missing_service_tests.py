#!/usr/bin/env python3
"""
Identify Missing Service Test Files
===================================

Compares src/services/ with tests/unit/services/ to find services without tests.

Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2025-11-30
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def get_service_files():
    """Get all Python service files."""
    services_dir = project_root / "src" / "services"
    service_files = []
    
    for py_file in services_dir.rglob("*.py"):
        if py_file.name == "__init__.py":
            continue
        if py_file.name.startswith("_"):
            continue
        # Get relative path from services dir
        rel_path = py_file.relative_to(services_dir)
        service_files.append(rel_path)
    
    return sorted(service_files)


def get_test_files():
    """Get all test files."""
    tests_dir = project_root / "tests" / "unit" / "services"
    test_files = []
    
    if not tests_dir.exists():
        return test_files
    
    for test_file in tests_dir.glob("test_*.py"):
        # Remove test_ prefix and .py extension
        service_name = test_file.stem[5:]  # Remove "test_" prefix
        test_files.append(service_name)
    
    return sorted(test_files)


def map_service_to_test(service_path):
    """Map service file path to expected test file name."""
    # Convert path to test name
    # e.g., "messaging_cli.py" -> "messaging_cli"
    # e.g., "handlers/onboarding_handler.py" -> "onboarding_handler"
    service_name = service_path.stem
    
    # For nested files, use the file name, not the directory
    # e.g., "handlers/onboarding_handler.py" -> "onboarding_handler"
    return service_name


def main():
    """Identify missing test files."""
    print("=" * 70)
    print("🔍 IDENTIFYING MISSING SERVICE TEST FILES")
    print("=" * 70)
    
    service_files = get_service_files()
    test_files = get_test_files()
    
    print(f"\n📊 Statistics:")
    print(f"   Services: {len(service_files)}")
    print(f"   Test files: {len(test_files)}")
    
    # Find missing tests
    missing_tests = []
    has_tests = []
    
    for service_path in service_files:
        expected_test = map_service_to_test(service_path)
        if expected_test not in test_files:
            missing_tests.append((service_path, expected_test))
        else:
            has_tests.append((service_path, expected_test))
    
    print(f"\n✅ Services with tests: {len(has_tests)}")
    print(f"❌ Services missing tests: {len(missing_tests)}")
    
    if missing_tests:
        print(f"\n📋 MISSING TEST FILES ({len(missing_tests)}):")
        print("=" * 70)
        for i, (service_path, expected_test) in enumerate(missing_tests, 1):
            print(f"{i:2d}. {service_path}")
            print(f"    Expected test: test_{expected_test}.py")
    
    # Show top 11 missing (as per task requirement)
    if len(missing_tests) >= 11:
        print(f"\n🎯 TOP 11 PRIORITY MISSING TESTS:")
        print("=" * 70)
        for i, (service_path, expected_test) in enumerate(missing_tests[:11], 1):
            print(f"{i:2d}. test_{expected_test}.py")
    
    print("\n" + "=" * 70)
    return 0


if __name__ == "__main__":
    sys.exit(main())

