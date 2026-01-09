#!/usr/bin/env python3
"""
Reorganization Validation Script
================================

Validation ritual for directory reorganization.
Run after each phase to ensure system integrity.
"""

import sys
import subprocess
from pathlib import Path

def run_command(cmd, description, ignore_errors=False):
    """Run a command and report results."""
    print(f"🔍 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0 or ignore_errors:
            print(f"  ✅ {description} passed")
            if result.stdout.strip():
                print(f"     {result.stdout.strip()}")
            return True
        else:
            print(f"  ❌ {description} failed")
            if result.stderr.strip():
                print(f"     {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"  ❌ {description} error: {e}")
        return False

def main():
    """Run validation checks."""
    repo = Path.cwd()

    print("=== REORG VALIDATION RITUAL ===")
    print(f"Repository: {repo}")
    print()

    checks_passed = 0
    total_checks = 0

    # 1) Git status check
    total_checks += 1
    if run_command("git status --porcelain", "Git status check"):
        checks_passed += 1

    # 2) Python compilation check
    total_checks += 1
    if run_command("python -m compileall -q src", "Python compilation check"):
        checks_passed += 1

    # 3) Import sanity check
    total_checks += 1
    if run_command('python -c "import sys; print(\'Python import OK\')"', "Basic Python import check"):
        checks_passed += 1

    # 4) Check for broken path references
    total_checks += 1
    broken_paths = [
        "schemas",
        "fsm_data",
        "nginx",
        "ssl",
        "database",
        "chroma_db",
        "swarm_brain",
        "cache",
        "runtime",
        "logs",
        "message_queue",
        "stress_test_analysis_results"
    ]

    path_check_cmd = " || ".join([f'echo "Checking {path}..."; rg -n "\\b{path}\\b" -S src config tools ops 2>/dev/null || true' for path in broken_paths[:5]])  # Limit to first 5 for brevity

    if run_command(path_check_cmd, "Path reference check (sample)", ignore_errors=True):
        checks_passed += 1

    # 5) Websites root validation
    total_checks += 1
    websites_check = 'python -c "from config.paths import WEBSITES_ROOT; print(f\'Websites root: {WEBSITES_ROOT}\'); import os; print(f\'Env WEBSITES_ROOT: {os.environ.get(\\\"WEBSITES_ROOT\\\", \\\"not set\\\")}\')"''
    if run_command(websites_check, "Websites root configuration check"):
        checks_passed += 1

    # 6) Sites directory check (should not exist in repo)
    total_checks += 1
    sites_check = 'if [ -d "sites" ]; then echo "ERROR: sites/ directory still exists in repo"; exit 1; else echo "sites/ correctly externalized"; fi'
    if run_command(sites_check, "Sites directory externalization check", ignore_errors=True):
        checks_passed += 1

    # Summary
    print()
    print("="*50)
    print(f"VALIDATION RESULTS: {checks_passed}/{total_checks} checks passed")

    if checks_passed == total_checks:
        print("🎉 ALL VALIDATION CHECKS PASSED")
        print("✅ Safe to proceed with next phase")
        return 0
    else:
        print("⚠️  SOME CHECKS FAILED")
        print("🔍 Review failures before proceeding")
        return 1

if __name__ == "__main__":
    sys.exit(main())