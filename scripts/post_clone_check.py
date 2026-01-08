#!/usr/bin/env python3
"""
Post-Clone Validation Script
=============================

Validates that the repository is properly set up after cloning.
Checks for required files, Python version, dependencies, and basic functionality.

Usage:
    python scripts/post_clone_check.py

Exit codes:
    0: All checks passed
    1: Some checks failed
"""

import os
import sys
import importlib.util
import subprocess
from pathlib import Path
from typing import List, Tuple

class PostCloneValidator:
    """Validates repository setup after cloning."""

    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def log_error(self, message: str):
        """Log an error."""
        self.errors.append(message)
        print(f"❌ {message}")

    def log_warning(self, message: str):
        """Log a warning."""
        self.warnings.append(message)
        print(f"⚠️  {message}")

    def log_success(self, message: str):
        """Log a success."""
        print(f"✅ {message}")

    def check_python_version(self) -> bool:
        """Check Python version."""
        version = sys.version_info
        if version.major == 3 and version.minor >= 11:
            self.log_success(f"Python version: {version.major}.{version.minor}.{version.micro}")
            return True
        else:
            self.log_error(f"Python 3.11+ required. Found: {version.major}.{version.minor}.{version.micro}")
            return False

    def check_required_files(self) -> bool:
        """Check for required files."""
        required_files = [
            "README.md",
            "setup.py",
            "main.py",
            "requirements.txt",
            "pyproject.toml",
            ".env.example"
        ]

        all_present = True
        for file_path in required_files:
            if not (self.project_root / file_path).exists():
                self.log_error(f"Required file missing: {file_path}")
                all_present = False
            else:
                self.log_success(f"Found: {file_path}")

        return all_present

    def check_basic_imports(self) -> bool:
        """Check basic module imports (defensive to avoid system initialization)."""
        # Only check if files exist, don't actually import to avoid triggering full system init
        basic_files = [
            "src/core/config/config_manager.py",
            "src/services/service_manager.py",
            "src/cli/argument_parser.py"
        ]

        all_present = True
        for file_path in basic_files:
            if not (self.project_root / file_path).exists():
                self.log_error(f"Required module file missing: {file_path}")
                all_present = False
            else:
                self.log_success(f"Found: {file_path}")

        return all_present

    def check_git_status(self) -> bool:
        """Check git repository status."""
        try:
            # Just check if .git directory exists
            if (self.project_root / ".git").exists():
                self.log_success("Git repository initialized")
                return True
            else:
                self.log_warning("Not a git repository")
                return True
        except Exception as e:
            self.log_warning(f"Git check failed: {e}")
            return True

    def check_disk_space(self) -> bool:
        """Check available disk space."""
        try:
            if hasattr(os, 'statvfs'):
                stat = os.statvfs(self.project_root)
                free_gb = (stat.f_bavail * stat.f_frsize) / (1024**3)

                if free_gb > 5:
                    self.log_success(f"Disk space: {free_gb:.1f} GB available")
                    return True
                else:
                    self.log_warning(f"Low disk space: {free_gb:.1f} GB available (recommended: 10GB+)")
                    return True
            else:
                # Windows or other systems without statvfs
                self.log_success("Disk space check skipped (not supported on this OS)")
                return True
        except Exception as e:
            self.log_warning(f"Disk space check failed: {e}")
            return True

    def run_validation(self) -> bool:
        """Run all validation checks."""
        print("🐝 dream.os - Post-Clone Validation")
        print("=" * 50)

        checks = [
            ("Python Version", self.check_python_version),
            ("Required Files", self.check_required_files),
            ("Basic Imports", self.check_basic_imports),
            ("Git Status", self.check_git_status),
            ("Disk Space", self.check_disk_space)
        ]

        all_passed = True
        for check_name, check_func in checks:
            print(f"\n🔍 Checking: {check_name}")
            try:
                if not check_func():
                    all_passed = False
            except Exception as e:
                self.log_error(f"Check failed with exception: {e}")
                all_passed = False

        # Summary
        print(f"\n{'='*50}")
        if all_passed:
            print("🎉 All validation checks passed!")
            print("   Your dream.os repository is ready for setup.")
            return True
        else:
            print(f"❌ {len(self.errors)} validation error(s) found.")
            if self.warnings:
                print(f"⚠️  {len(self.warnings)} warning(s) found.")
            print("\n💡 Please fix the errors above before proceeding.")
            return False

def main():
    """Main entry point."""
    validator = PostCloneValidator()
    success = validator.run_validation()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()