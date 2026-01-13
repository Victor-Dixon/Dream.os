#!/usr/bin/env python3
"""
PyPI Publishing Automation Script
================================

Automated PyPI publishing workflow for Agent Cellphone V2.

Usage:
    python scripts/publish_to_pypi.py --token YOUR_PYPI_TOKEN

Requirements:
    - Python 3.11+
    - twine>=4.0.0 (install with: pip install twine)
    - PyPI account with API token

Author: Agent-5 (Infrastructure Automation Specialist)
Date: 2026-01-12
"""

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Optional

import toml


class PyPIPublisher:
    """Automated PyPI publishing workflow."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.build_dir = project_root / "dist"
        self.pyproject_path = project_root / "pyproject.toml"

    def load_project_config(self) -> dict:
        """Load project configuration from pyproject.toml."""
        with open(self.pyproject_path, 'r', encoding='utf-8') as f:
            return toml.load(f)

    def clean_build_artifacts(self) -> None:
        """Clean previous build artifacts."""
        if self.build_dir.exists():
            print(f"🧹 Cleaning build directory: {self.build_dir}")
            shutil.rmtree(self.build_dir)

    def build_package(self) -> bool:
        """Build the package using setuptools."""
        print("🔨 Building package...")

        try:
            result = subprocess.run([
                sys.executable, "-m", "build",
                "--wheel", "--sdist",
                "--outdir", str(self.build_dir)
            ], cwd=self.project_root, capture_output=True, text=True)

            if result.returncode != 0:
                print(f"❌ Build failed:\n{result.stderr}")
                return False

            print("✅ Package built successfully")
            return True

        except Exception as e:
            print(f"❌ Build error: {e}")
            return False

    def verify_build_artifacts(self) -> bool:
        """Verify that build artifacts were created correctly."""
        if not self.build_dir.exists():
            print("❌ Build directory not found")
            return False

        artifacts = list(self.build_dir.glob("*"))
        if not artifacts:
            print("❌ No build artifacts found")
            return False

        print(f"📦 Build artifacts created:")
        for artifact in artifacts:
            print(f"  - {artifact.name}")

        # Check for both wheel and source distribution
        has_wheel = any(artifact.suffix == ".whl" for artifact in artifacts)
        has_sdist = any(artifact.suffix == ".tar.gz" for artifact in artifacts)

        if not (has_wheel and has_sdist):
            print("❌ Missing required artifacts (wheel and/or source distribution)")
            return False

        print("✅ Build artifacts verified")
        return True

    def test_install_locally(self) -> bool:
        """Test local installation of the built package."""
        print("🧪 Testing local installation...")

        try:
            # Find the wheel file
            wheel_files = list(self.build_dir.glob("*.whl"))
            if not wheel_files:
                print("❌ No wheel file found for testing")
                return False

            wheel_path = wheel_files[0]

            # Test installation in a temporary environment
            result = subprocess.run([
                sys.executable, "-m", "pip", "install",
                "--dry-run", "--quiet", str(wheel_path)
            ], capture_output=True, text=True)

            if result.returncode != 0:
                print(f"❌ Local install test failed:\n{result.stderr}")
                return False

            print("✅ Local installation test passed")
            return True

        except Exception as e:
            print(f"❌ Local install test error: {e}")
            return False

    def upload_to_pypi(self, token: str, test_pypi: bool = False) -> bool:
        """Upload package to PyPI using twine."""
        repository = "testpypi" if test_pypi else "pypi"
        repository_url = f"https://upload.{repository}.org/legacy/"

        print(f"📤 Uploading to {'Test PyPI' if test_pypi else 'PyPI'}...")

        try:
            # Set up environment with token
            env = os.environ.copy()
            env["TWINE_USERNAME"] = "__token__"
            env["TWINE_PASSWORD"] = token
            env["TWINE_REPOSITORY_URL"] = repository_url

            result = subprocess.run([
                sys.executable, "-m", "twine", "upload",
                "--repository-url", repository_url,
                "--username", "__token__",
                "--password", token,
                str(self.build_dir / "*")
            ], cwd=self.project_root, capture_output=True, text=True, env=env)

            if result.returncode != 0:
                print(f"❌ Upload failed:\n{result.stderr}")
                return False

            print(f"✅ Package uploaded to {'Test PyPI' if test_pypi else 'PyPI'} successfully")
            return True

        except Exception as e:
            print(f"❌ Upload error: {e}")
            return False

    def generate_publishing_report(self, config: dict, success: bool, test_pypi: bool = False) -> str:
        """Generate a publishing report."""
        package_name = config['project']['name']
        version = config['project']['version']

        report = f"""
# PyPI Publishing Report

## Package Information
- **Name**: {package_name}
- **Version**: {version}
- **Repository**: {'Test PyPI' if test_pypi else 'PyPI'}

## Publishing Status
- **Status**: {'✅ SUCCESS' if success else '❌ FAILED'}
- **Timestamp**: {self._get_timestamp()}

## Build Artifacts
"""

        if self.build_dir.exists():
            artifacts = list(self.build_dir.glob("*"))
            for artifact in artifacts:
                report += f"- {artifact.name}\n"

        if success and not test_pypi:
            report += f"""
## Installation
```bash
pip install {package_name}=={version}
```

## URLs
- [PyPI Project Page](https://pypi.org/project/{package_name}/)
- [PyPI Download](https://pypi.org/project/{package_name}/{version}/#files)
"""

        return report

    def _get_timestamp(self) -> str:
        """Get current timestamp."""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")

    def publish(self, token: str, test_pypi: bool = False, skip_tests: bool = False) -> bool:
        """
        Complete PyPI publishing workflow.

        Args:
            token: PyPI API token
            test_pypi: Whether to publish to Test PyPI first
            skip_tests: Whether to skip local testing

        Returns:
            True if publishing succeeded, False otherwise
        """
        print("🚀 Starting PyPI publishing workflow...")

        # Load configuration
        config = self.load_project_config()
        package_name = config['project']['name']
        version = config['project']['version']

        print(f"📦 Publishing {package_name} v{version}")

        # Clean previous builds
        self.clean_build_artifacts()

        # Build package
        if not self.build_package():
            return False

        # Verify build artifacts
        if not self.verify_build_artifacts():
            return False

        # Test installation (unless skipped)
        if not skip_tests:
            if not self.test_install_locally():
                return False

        # Upload to PyPI
        if not self.upload_to_pypi(token, test_pypi):
            return False

        print("🎉 Publishing workflow completed successfully!")
        return True


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Automated PyPI publishing for Agent Cellphone V2",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Publish to Test PyPI first (recommended)
  python scripts/publish_to_pypi.py --token YOUR_TOKEN --test-pypi

  # Publish to production PyPI
  python scripts/publish_to_pypi.py --token YOUR_TOKEN

  # Skip local tests (not recommended)
  python scripts/publish_to_pypi.py --token YOUR_TOKEN --skip-tests
        """
    )

    parser.add_argument(
        "--token",
        required=True,
        help="PyPI API token (get from https://pypi.org/manage/account/token/)"
    )

    parser.add_argument(
        "--test-pypi",
        action="store_true",
        help="Publish to Test PyPI instead of production PyPI"
    )

    parser.add_argument(
        "--skip-tests",
        action="store_true",
        help="Skip local installation testing (not recommended)"
    )

    parser.add_argument(
        "--report-file",
        help="Save publishing report to file"
    )

    args = parser.parse_args()

    # Initialize publisher
    project_root = Path(__file__).parent.parent
    publisher = PyPIPublisher(project_root)

    # Execute publishing workflow
    success = publisher.publish(args.token, args.test_pypi, args.skip_tests)

    # Generate and save report if requested
    if args.report_file:
        config = publisher.load_project_config()
        report = publisher.generate_publishing_report(config, success, args.test_pypi)

        with open(args.report_file, 'w', encoding='utf-8') as f:
            f.write(report)

        print(f"📄 Publishing report saved to: {args.report_file}")

    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()