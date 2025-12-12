#!/usr/bin/env python3
"""
Dream.os CI Failure Diagnostic Tool
Agent-3 (Infrastructure & DevOps)

Diagnoses common CI/CD failure patterns for the Dream.os repository.
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# Color output
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
RESET = "\033[0m"


def check_file_exists(filepath: str) -> Tuple[bool, str]:
    """Check if a file exists and return status."""
    exists = Path(filepath).exists()
    status = f"{GREEN}✓{RESET}" if exists else f"{RED}✗{RESET}"
    return exists, status


def check_requirements_files() -> Dict[str, any]:
    """Check for required dependency files."""
    print(f"\n{BLUE}📦 Checking Requirements Files{RESET}")
    print("=" * 60)
    
    results = {
        "requirements.txt": check_file_exists("requirements.txt"),
        "requirements-dev.txt": check_file_exists("requirements-dev.txt"),
        "pyproject.toml": check_file_exists("pyproject.toml"),
        "setup.py": check_file_exists("setup.py"),
        "Pipfile": check_file_exists("Pipfile"),
        "poetry.lock": check_file_exists("poetry.lock"),
    }
    
    for file, (exists, status) in results.items():
        print(f"  {status} {file}")
    
    return results


def check_ci_configuration() -> Dict[str, any]:
    """Check for CI/CD configuration files."""
    print(f"\n{BLUE}🔧 Checking CI/CD Configuration{RESET}")
    print("=" * 60)
    
    ci_files = {
        ".github/workflows/ci.yml": check_file_exists(".github/workflows/ci.yml"),
        ".github/workflows/ci-cd.yml": check_file_exists(".github/workflows/ci-cd.yml"),
        ".github/workflows/ci-optimized.yml": check_file_exists(".github/workflows/ci-optimized.yml"),
        ".gitlab-ci.yml": check_file_exists(".gitlab-ci.yml"),
        ".circleci/config.yml": check_file_exists(".circleci/config.yml"),
        ".travis.yml": check_file_exists(".travis.yml"),
    }
    
    for file, (exists, status) in ci_files.items():
        print(f"  {status} {file}")
    
    return ci_files


def check_test_structure() -> Dict[str, any]:
    """Check for test directories and files."""
    print(f"\n{BLUE}🧪 Checking Test Structure{RESET}")
    print("=" * 60)
    
    test_paths = {
        "tests/": check_file_exists("tests"),
        "test/": check_file_exists("test"),
        "pytest.ini": check_file_exists("pytest.ini"),
        "pytest.ini": check_file_exists("pytest.ini"),
        ".coveragerc": check_file_exists(".coveragerc"),
        "coverage.ini": check_file_exists("coverage.ini"),
    }
    
    for path, (exists, status) in test_paths.items():
        print(f"  {status} {path}")
    
    return test_paths


def check_python_syntax() -> Tuple[bool, List[str]]:
    """Check Python files for syntax errors."""
    print(f"\n{BLUE}🐍 Checking Python Syntax{RESET}")
    print("=" * 60)
    
    errors = []
    python_files = list(Path(".").rglob("*.py"))
    python_files = [f for f in python_files if not any(
        part.startswith(".") or part in ["__pycache__", "node_modules", ".git"]
        for part in f.parts
    )]
    
    # Limit to first 20 files for speed
    python_files = python_files[:20]
    
    for py_file in python_files:
        try:
            result = subprocess.run(
                [sys.executable, "-m", "py_compile", str(py_file)],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode != 0:
                errors.append(f"{py_file}: {result.stderr}")
                print(f"  {RED}✗{RESET} {py_file}")
        except Exception as e:
            errors.append(f"{py_file}: {str(e)}")
    
    if not errors:
        print(f"  {GREEN}✓{RESET} No syntax errors found in checked files")
    
    return len(errors) == 0, errors


def check_imports() -> Tuple[bool, List[str]]:
    """Check for common import issues."""
    print(f"\n{BLUE}📥 Checking Import Issues{RESET}")
    print("=" * 60)
    
    errors = []
    
    # Check if src/ exists and has __init__.py
    src_init = Path("src/__init__.py")
    if src_init.exists():
        print(f"  {GREEN}✓{RESET} src/__init__.py exists")
    else:
        print(f"  {YELLOW}⚠{RESET} src/__init__.py missing (may be intentional)")
    
    # Try importing main modules
    try:
        import sys
        if Path("src").exists():
            sys.path.insert(0, str(Path("src").absolute()))
        
        # Try common imports
        common_imports = [
            "config",
            "core",
        ]
        
        for module in common_imports:
            try:
                __import__(module)
                print(f"  {GREEN}✓{RESET} Can import {module}")
            except ImportError as e:
                print(f"  {YELLOW}⚠{RESET} Cannot import {module}: {e}")
    except Exception as e:
        errors.append(f"Import check failed: {e}")
    
    return len(errors) == 0, errors


def check_linting_config() -> Dict[str, any]:
    """Check for linting configuration files."""
    print(f"\n{BLUE}🔍 Checking Linting Configuration{RESET}")
    print("=" * 60)
    
    lint_files = {
        ".ruff.toml": check_file_exists(".ruff.toml"),
        "ruff.toml": check_file_exists("ruff.toml"),
        ".flake8": check_file_exists(".flake8"),
        "setup.cfg": check_file_exists("setup.cfg"),
        ".pylintrc": check_file_exists(".pylintrc"),
        ".pre-commit-config.yaml": check_file_exists(".pre-commit-config.yaml"),
    }
    
    for file, (exists, status) in lint_files.items():
        print(f"  {status} {file}")
    
    return lint_files


def check_environment_variables() -> Dict[str, any]:
    """Check for required environment variables in CI."""
    print(f"\n{BLUE}🔐 Checking Environment Variables{RESET}")
    print("=" * 60)
    
    # Common CI env vars that might be needed
    env_vars = {
        "GITHUB_TOKEN": os.getenv("GITHUB_TOKEN"),
        "PYTHON_VERSION": os.getenv("PYTHON_VERSION"),
        "COVERAGE_THRESHOLD": os.getenv("COVERAGE_THRESHOLD"),
    }
    
    for var, value in env_vars.items():
        if value:
            print(f"  {GREEN}✓{RESET} {var} is set")
        else:
            print(f"  {YELLOW}⚠{RESET} {var} not set (may be set in CI)")
    
    return env_vars


def check_github_workflow_syntax() -> Tuple[bool, List[str]]:
    """Check GitHub Actions workflow files for syntax errors."""
    print(f"\n{BLUE}⚙️  Checking GitHub Workflow Syntax{RESET}")
    print("=" * 60)
    
    errors = []
    workflow_dir = Path(".github/workflows")
    
    if not workflow_dir.exists():
        print(f"  {YELLOW}⚠{RESET} .github/workflows/ directory not found")
        return True, []
    
    workflow_files = list(workflow_dir.glob("*.yml")) + list(workflow_dir.glob("*.yaml"))
    
    for workflow_file in workflow_files:
        try:
            import yaml
            with open(workflow_file, 'r') as f:
                yaml.safe_load(f)
            print(f"  {GREEN}✓{RESET} {workflow_file.name} - Valid YAML")
        except ImportError:
            print(f"  {YELLOW}⚠{RESET} PyYAML not installed, skipping YAML validation")
            break
        except Exception as e:
            errors.append(f"{workflow_file}: {str(e)}")
            print(f"  {RED}✗{RESET} {workflow_file.name} - {str(e)}")
    
    return len(errors) == 0, errors


def generate_recommendations(results: Dict) -> List[str]:
    """Generate recommendations based on diagnostic results."""
    recommendations = []
    
    # Check requirements
    req_results = results.get("requirements", {})
    if not req_results.get("requirements.txt", (False,))[0]:
        recommendations.append(
            "❌ Missing requirements.txt - CI needs this to install dependencies"
        )
    
    # Check CI config
    ci_results = results.get("ci_config", {})
    has_ci = any(exists for exists, _ in ci_results.values())
    if not has_ci:
        recommendations.append(
            "❌ No CI/CD configuration found - Add .github/workflows/ci.yml"
        )
    
    # Check tests
    test_results = results.get("tests", {})
    has_tests = test_results.get("tests/", (False,))[0] or test_results.get("test/", (False,))[0]
    if not has_tests:
        recommendations.append(
            "⚠️  No test directory found - CI may fail if tests are required"
        )
    
    # Check syntax
    syntax_ok = results.get("syntax", {}).get("ok", False)
    if not syntax_ok:
        recommendations.append(
            "❌ Python syntax errors found - Fix before CI can pass"
        )
    
    return recommendations


def main():
    """Run full diagnostic."""
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}🔍 Dream.os CI Failure Diagnostic Tool{RESET}")
    print(f"{BLUE}{'='*60}{RESET}")
    
    results = {}
    
    # Run checks
    results["requirements"] = check_requirements_files()
    results["ci_config"] = check_ci_configuration()
    results["tests"] = check_test_structure()
    results["linting"] = check_linting_config()
    
    syntax_ok, syntax_errors = check_python_syntax()
    results["syntax"] = {"ok": syntax_ok, "errors": syntax_errors}
    
    import_ok, import_errors = check_imports()
    results["imports"] = {"ok": import_ok, "errors": import_errors}
    
    workflow_ok, workflow_errors = check_github_workflow_syntax()
    results["workflows"] = {"ok": workflow_ok, "errors": workflow_errors}
    
    results["environment"] = check_environment_variables()
    
    # Generate recommendations
    print(f"\n{BLUE}💡 Recommendations{RESET}")
    print("=" * 60)
    
    recommendations = generate_recommendations(results)
    
    if recommendations:
        for rec in recommendations:
            print(f"  {rec}")
    else:
        print(f"  {GREEN}✓{RESET} No obvious issues found")
        print(f"  {YELLOW}⚠{RESET} Check GitHub Actions logs for specific error messages")
    
    # Common CI failure patterns
    print(f"\n{BLUE}🔍 Common CI Failure Patterns to Check{RESET}")
    print("=" * 60)
    print("  1. Missing dependencies in requirements.txt")
    print("  2. Test failures (run: pytest -v)")
    print("  3. Linting errors (run: ruff check .)")
    print("  4. Coverage below threshold (check .coveragerc)")
    print("  5. Missing environment variables in workflow")
    print("  6. Python version mismatch (check workflow matrix)")
    print("  7. Import errors (check PYTHONPATH)")
    print("  8. Missing __init__.py files in packages")
    
    print(f"\n{BLUE}📋 Next Steps{RESET}")
    print("=" * 60)
    print("  1. Check GitHub Actions logs: https://github.com/Victor-Dixon/Dream.os/actions")
    print("  2. Run tests locally: pytest -v")
    print("  3. Run linters: ruff check . && black --check .")
    print("  4. Check workflow file syntax")
    print("  5. Verify all dependencies are in requirements.txt")
    
    # Save results
    output_file = Path("dream_os_ci_diagnostic.json")
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n{GREEN}✓{RESET} Diagnostic results saved to: {output_file}")
    print(f"\n{BLUE}{'='*60}{RESET}\n")


if __name__ == "__main__":
    main()

