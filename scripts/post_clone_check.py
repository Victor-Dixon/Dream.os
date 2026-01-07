#!/usr/bin/env python3
"""
Post-Clone Validation Script - dream.os
=======================================

This script validates that a fresh clone is ready for setup and use.
Run this immediately after cloning to ensure your environment is properly configured.

Usage:
    python scripts/post_clone_check.py

V2 Compliance: <300 lines
Author: Agent-3 (Infrastructure & DevOps Specialist)
"""

import os
import sys
import platform
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple
import json

class PostCloneValidator:
    """Validates system readiness after cloning."""

    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.results = {
            "system_requirements": {},
            "file_structure": {},
            "configuration": {},
            "dependencies": {},
            "recommendations": []
        }
        self.errors = []
        self.warnings = []

    def log_success(self, message: str):
        """Log a successful check."""
        print(f"✅ {message}")

    def log_error(self, message: str):
        """Log an error."""
        print(f"❌ {message}")
        self.errors.append(message)

    def log_warning(self, message: str):
        """Log a warning."""
        print(f"⚠️  {message}")
        self.warnings.append(message)

    def log_info(self, message: str):
        """Log an informational message."""
        print(f"ℹ️  {message}")

    def check_python_version(self) -> bool:
        """Check Python version compatibility."""
        version = sys.version_info
        version_str = f"{version.major}.{version.minor}.{version.micro}"

        if version.major == 3 and version.minor >= 11:
            self.log_success(f"Python {version_str} - Compatible")
            self.results["system_requirements"]["python"] = True
            return True
        else:
            self.log_error(f"Python {version_str} - Requires Python 3.11+")
            self.results["system_requirements"]["python"] = False
            return False

    def check_operating_system(self) -> bool:
        """Check OS compatibility."""
        system = platform.system().lower()

        supported_systems = ["windows", "linux", "darwin"]
        if system in supported_systems:
            os_name = system.title()
            if system == "darwin":
                os_name = "macOS"
            self.log_success(f"Operating System: {os_name} - Supported")
            self.results["system_requirements"]["os"] = True
            return True
        else:
            self.log_error(f"Operating System: {system} - Not officially supported")
            self.results["system_requirements"]["os"] = False
            return False

    def check_docker_availability(self) -> bool:
        """Check if Docker is available (optional but recommended)."""
        try:
            result = subprocess.run(
                ["docker", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                version = result.stdout.strip()
                self.log_success(f"Docker available: {version}")
                self.results["system_requirements"]["docker"] = True
                return True
            else:
                self.log_warning("Docker not found - will use native Python installation")
                self.results["system_requirements"]["docker"] = False
                return False
        except (subprocess.TimeoutExpired, FileNotFoundError):
            self.log_warning("Docker not found - will use native Python installation")
            self.results["system_requirements"]["docker"] = False
            return False

    def check_git_repository(self) -> bool:
        """Check if this is a valid git repository."""
        git_dir = self.project_root / ".git"
        if git_dir.exists():
            self.log_success("Git repository detected")
            self.results["file_structure"]["git_repo"] = True
            return True
        else:
            self.log_error("Not a git repository - please clone properly")
            self.results["file_structure"]["git_repo"] = False
            return False

    def check_required_files(self) -> bool:
        """Check for required configuration and setup files."""
        required_files = [
            "README.md",
            "QUICKSTART.md",
            "install.sh",
            "install.bat",
            "setup_wizard.py",
            "requirements.txt",
            "env.example",
            "docker-compose.yml",
            "main.py"
        ]

        missing_files = []
        for file in required_files:
            if not (self.project_root / file).exists():
                missing_files.append(file)

        if not missing_files:
            self.log_success("All required setup files present")
            self.results["file_structure"]["required_files"] = True
            return True
        else:
            self.log_error(f"Missing required files: {', '.join(missing_files)}")
            self.results["file_structure"]["required_files"] = False
            return False

    def check_directory_structure(self) -> bool:
        """Check for required directory structure."""
        required_dirs = [
            "src",
            "scripts",
            "config",
            "agent_workspaces"
        ]

        missing_dirs = []
        for dir_name in required_dirs:
            if not (self.project_root / dir_name).exists():
                missing_dirs.append(dir_name)

        if not missing_dirs:
            self.log_success("Required directory structure present")
            self.results["file_structure"]["directories"] = True
            return True
        else:
            self.log_error(f"Missing required directories: {', '.join(missing_dirs)}")
            self.results["file_structure"]["directories"] = False
            return False

    def check_configuration_files(self) -> bool:
        """Check configuration file status."""
        env_file = self.project_root / ".env"
        env_example = self.project_root / "env.example"

        if env_file.exists():
            self.log_success("Environment file (.env) exists")
            self.results["configuration"]["env_file"] = True
        else:
            self.log_warning("Environment file (.env) not found - will be created during setup")
            self.results["configuration"]["env_file"] = False

        if env_example.exists():
            self.log_success("Environment template (env.example) available")
            self.results["configuration"]["env_template"] = True
        else:
            self.log_error("Environment template (env.example) missing")
            self.results["configuration"]["env_template"] = False

        return self.results["configuration"].get("env_template", False)

    def check_disk_space(self) -> bool:
        """Check available disk space."""
        try:
            stat = os.statvfs(self.project_root)
            # Get available space in GB
            available_gb = (stat.f_bavail * stat.f_frsize) / (1024**3)

            if available_gb > 10:
                self.log_success(".2f")
                self.results["system_requirements"]["disk_space"] = True
                return True
            else:
                self.log_error(".2f")
                self.results["system_requirements"]["disk_space"] = False
                return False
        except:
            self.log_warning("Could not check disk space")
            self.results["system_requirements"]["disk_space"] = None
            return True

    def generate_recommendations(self):
        """Generate setup recommendations based on findings."""
        recommendations = []

        # Docker recommendations
        if not self.results["system_requirements"].get("docker", False):
            recommendations.append("Install Docker Desktop for the easiest setup experience")

        # Configuration recommendations
        if not self.results["configuration"].get("env_file", False):
            recommendations.append("Run setup wizard: python setup_wizard.py")

        # Python recommendations
        if not self.results["system_requirements"].get("python", False):
            recommendations.append("Upgrade to Python 3.11+ for full compatibility")

        # General recommendations
        recommendations.extend([
            "Review QUICKSTART.md for detailed setup instructions",
            "Join our Discord for community support",
            "Check docs/ for comprehensive documentation"
        ])

        self.results["recommendations"] = recommendations

    def run_validation(self) -> Dict:
        """Run all validation checks."""
        print("🚀 dream.os - Post-Clone Validation")
        print("=" * 50)
        print()

        # System Requirements
        print("🔧 System Requirements:")
        self.check_operating_system()
        self.check_python_version()
        self.check_docker_availability()
        self.check_disk_space()
        print()

        # File Structure
        print("📁 File Structure:")
        self.check_git_repository()
        self.check_required_files()
        self.check_directory_structure()
        print()

        # Configuration
        print("⚙️  Configuration:")
        self.check_configuration_files()
        print()

        # Generate recommendations
        self.generate_recommendations()

        # Summary
        print("📊 Validation Summary:")
        print("=" * 30)

        # Calculate totals safely (handle None values)
        def safe_sum(values):
            return sum(1 for v in values if v is True)

        sys_reqs = safe_sum(self.results["system_requirements"].values())
        file_struct = safe_sum(self.results["file_structure"].values())
        config_checks = safe_sum(self.results["configuration"].values())

        total_checks = len(self.results["system_requirements"]) + len(self.results["file_structure"]) + len(self.results["configuration"])
        passed_checks = sys_reqs + file_struct + config_checks

        if self.errors:
            print(f"❌ Critical Issues: {len(self.errors)}")
            for error in self.errors:
                print(f"   - {error}")

        if self.warnings:
            print(f"⚠️  Warnings: {len(self.warnings)}")
            for warning in self.warnings:
                print(f"   - {warning}")

        print(f"✅ Passed Checks: {passed_checks}/{total_checks}")

        if not self.errors:
            print()
            print("🎉 Your clone is ready for setup!")
            print()
            print("Next steps:")
            print("1. Run: python setup_wizard.py")
            print("2. Or: ./install.sh --docker  (if Docker available)")
            print("3. Review: QUICKSTART.md")
        else:
            print()
            print("⚠️  Please address the critical issues above before proceeding.")

        print()
        print("💡 Recommendations:")
        for rec in self.results["recommendations"]:
            print(f"   • {rec}")

        return self.results

def main():
    """Main entry point."""
    validator = PostCloneValidator()
    results = validator.run_validation()

    # Exit with appropriate code
    if validator.errors:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()