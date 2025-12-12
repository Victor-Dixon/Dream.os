#!/usr/bin/env python3
"""
CI/CD Failure Diagnostic Tool
=============================
Identifies common CI/CD failure points before pushing.
"""

import subprocess
import sys
from pathlib import Path

def check_python_syntax():
    """Check for Python syntax errors."""
    print("=" * 60)
    print("1. Checking Python Syntax")
    print("=" * 60)
    
    errors = []
    for py_file in Path(".").rglob("*.py"):
        if any(skip in str(py_file) for skip in [".git", "__pycache__", "venv", ".venv", "node_modules"]):
            continue
        try:
            compile(open(py_file, encoding='utf-8').read(), str(py_file), 'exec')
        except SyntaxError as e:
            errors.append(f"{py_file}:{e.lineno}: {e.msg}")
    
    if errors:
        print(f"❌ Found {len(errors)} syntax errors:")
        for err in errors[:10]:
            print(f"   {err}")
        return False
    else:
        print("✅ No syntax errors found")
        return True

def check_imports():
    """Check for import errors."""
    print("\n" + "=" * 60)
    print("2. Checking Critical Imports")
    print("=" * 60)
    
    critical_modules = [
        "pytest",
        "ruff",
        "black",
        "isort",
    ]
    
    missing = []
    for module in critical_modules:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError:
            print(f"❌ {module} - NOT INSTALLED")
            missing.append(module)
    
    if missing:
        print(f"\n⚠️  Missing modules: {', '.join(missing)}")
        print("   Install with: pip install " + " ".join(missing))
        return False
    return True

def check_requirements():
    """Check if requirements files exist."""
    print("\n" + "=" * 60)
    print("3. Checking Requirements Files")
    print("=" * 60)
    
    required_files = ["requirements.txt"]
    optional_files = ["requirements-dev.txt", "requirements-testing.txt"]
    
    for req_file in required_files:
        if Path(req_file).exists():
            print(f"✅ {req_file} exists")
        else:
            print(f"❌ {req_file} MISSING")
            return False
    
    for req_file in optional_files:
        if Path(req_file).exists():
            print(f"✅ {req_file} exists")
        else:
            print(f"⚠️  {req_file} not found (optional)")
    
    return True

def check_test_structure():
    """Check test directory structure."""
    print("\n" + "=" * 60)
    print("4. Checking Test Structure")
    print("=" * 60)
    
    tests_dir = Path("tests")
    if not tests_dir.exists():
        print("⚠️  tests/ directory not found")
        return True  # Not a failure, just a warning
    
    test_files = list(tests_dir.rglob("test_*.py"))
    if test_files:
        print(f"✅ Found {len(test_files)} test files")
        return True
    else:
        print("⚠️  No test_*.py files found in tests/")
        return True  # Not a failure

def check_v2_tools():
    """Check if V2 compliance tools exist."""
    print("\n" + "=" * 60)
    print("5. Checking V2 Compliance Tools")
    print("=" * 60)
    
    v2_tools = [
        "tests/v2_standards_checker.py",
        "tools/v2_compliance_checker.py",
        "scripts/validate_v2_compliance.py",
        "config/v2_rules.yaml",
    ]
    
    found = []
    missing = []
    for tool in v2_tools:
        if Path(tool).exists():
            print(f"✅ {tool}")
            found.append(tool)
        else:
            print(f"⚠️  {tool} not found")
            missing.append(tool)
    
    if not found:
        print("\n⚠️  No V2 compliance tools found - CI will skip V2 checks")
    return True  # Not a failure, just informational

def check_linting():
    """Check for linting errors."""
    print("\n" + "=" * 60)
    print("6. Checking Linting (ruff)")
    print("=" * 60)
    
    try:
        result = subprocess.run(
            ["ruff", "check", ".", "--select", "E,F"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print("✅ No critical linting errors (E, F codes)")
            return True
        else:
            lines = result.stdout.split('\n')[:20]
            print(f"⚠️  Found linting issues:")
            for line in lines:
                if line.strip():
                    print(f"   {line}")
            return False
    except FileNotFoundError:
        print("⚠️  ruff not installed - skipping lint check")
        return True
    except Exception as e:
        print(f"⚠️  Lint check failed: {e}")
        return True

def main():
    """Run all diagnostic checks."""
    print("🔍 CI/CD Failure Diagnostic")
    print("=" * 60)
    print()
    
    checks = [
        ("Python Syntax", check_python_syntax),
        ("Critical Imports", check_imports),
        ("Requirements Files", check_requirements),
        ("Test Structure", check_test_structure),
        ("V2 Tools", check_v2_tools),
        ("Linting", check_linting),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ {name} check failed with error: {e}")
            results.append((name, False))
    
    print("\n" + "=" * 60)
    print("📊 Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")
    
    print(f"\nResults: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n✅ All checks passed! CI should work.")
        return 0
    else:
        print("\n⚠️  Some checks failed. Review issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

