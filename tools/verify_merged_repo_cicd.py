#!/usr/bin/env python3
"""
CI/CD Verification Tool for Merged Repos
========================================

Verifies CI/CD pipeline status for merged repositories.
Checks for pipeline files, configuration, and dependencies.

Author: Agent-3 (Infrastructure & DevOps Specialist)
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CICDVerifier:
    """Verify CI/CD pipelines for merged repos."""

    def __init__(self, repo_path: Path):
        self.repo_path = Path(repo_path)
        self.results = {
            "repo_path": str(self.repo_path),
            "pipeline_exists": False,
            "pipeline_files": [],
            "dependencies": {},
            "testing_setup": {},
            "status": "unknown",
        }

    def verify(self) -> Dict:
        """Run complete CI/CD verification."""
        logger.info(f"🔍 Verifying CI/CD for: {self.repo_path}")

        # Check for pipeline files
        self._check_pipeline_files()

        # Check dependencies
        self._check_dependencies()

        # Check testing setup
        self._check_testing_setup()

        # Determine overall status
        self._determine_status()

        return self.results

    def _check_pipeline_files(self):
        """Check for CI/CD pipeline files."""
        workflows_dir = self.repo_path / ".github" / "workflows"
        if workflows_dir.exists():
            pipeline_files = list(workflows_dir.glob("*.yml")) + list(
                workflows_dir.glob("*.yaml")
            )
            self.results["pipeline_exists"] = len(pipeline_files) > 0
            self.results["pipeline_files"] = [
                str(f.relative_to(self.repo_path)) for f in pipeline_files
            ]
            logger.info(f"✅ Found {len(pipeline_files)} pipeline file(s)")
        else:
            logger.warning(f"⚠️ No .github/workflows directory found")

    def _check_dependencies(self):
        """Check for dependency files."""
        deps = {}

        # Check for requirements files
        req_files = ["requirements.txt", "requirements-dev.txt", "pyproject.toml"]
        for req_file in req_files:
            req_path = self.repo_path / req_file
            if req_path.exists():
                deps[req_file] = str(req_path.relative_to(self.repo_path))
                logger.info(f"✅ Found {req_file}")

        # Check for package.json (Node.js)
        package_json = self.repo_path / "package.json"
        if package_json.exists():
            deps["package.json"] = str(package_json.relative_to(self.repo_path))
            logger.info("✅ Found package.json")

        self.results["dependencies"] = deps

    def _check_testing_setup(self):
        """Check for testing setup."""
        testing = {}

        # Check for test directories
        test_dirs = ["tests", "test", "__tests__", "spec"]
        for test_dir in test_dirs:
            test_path = self.repo_path / test_dir
            if test_path.exists() and test_path.is_dir():
                test_files = list(test_path.rglob("*.py")) + list(
                    test_path.rglob("*.js")
                )
                if test_files:
                    testing[test_dir] = {
                        "exists": True,
                        "file_count": len(test_files),
                        "files": [str(f.name) for f in test_files[:5]],  # First 5
                    }
                    logger.info(f"✅ Found {test_dir} with {len(test_files)} test files")

        # Check for test config files
        test_configs = ["pytest.ini", ".pytestrc", "jest.config.js", "vitest.config.js"]
        for config in test_configs:
            config_path = self.repo_path / config
            if config_path.exists():
                testing[config] = str(config_path.relative_to(self.repo_path))
                logger.info(f"✅ Found {config}")

        self.results["testing_setup"] = testing

    def _determine_status(self):
        """Determine overall CI/CD status."""
        if self.results["pipeline_exists"]:
            if self.results["testing_setup"]:
                self.results["status"] = "complete"
            else:
                self.results["status"] = "pipeline_only"
        else:
            if self.results["testing_setup"]:
                self.results["status"] = "tests_only"
            else:
                self.results["status"] = "missing"


def verify_merge(merge_info: Dict) -> Dict:
    """Verify CI/CD for a specific merge."""
    target_repo = merge_info.get("target_repo")
    if not target_repo:
        logger.error("❌ No target_repo specified")
        return {}

    # Try to find the repo path
    # Note: This assumes repos are in a standard location
    # Adjust based on actual repo structure
    repo_path = Path(target_repo)
    if not repo_path.exists():
        logger.warning(f"⚠️ Repo path not found: {repo_path}")
        logger.info("💡 Note: Repo may need to be cloned first")
        return {
            "status": "repo_not_found",
            "message": f"Repo path not found: {repo_path}",
        }

    verifier = CICDVerifier(repo_path)
    return verifier.verify()


def main():
    """Main entry point."""
    import sys

    if len(sys.argv) > 1:
        repo_path = Path(sys.argv[1])
        verifier = CICDVerifier(repo_path)
        results = verifier.verify()
        print(json.dumps(results, indent=2))
    else:
        print("Usage: python verify_merged_repo_cicd.py <repo_path>")
        print("\nExample:")
        print("  python verify_merged_repo_cicd.py Streamertools")


if __name__ == "__main__":
    main()

