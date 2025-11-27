#!/usr/bin/env python3
"""
Enhanced CI/CD Verification Tool for Merged Repos
=================================================

Uses existing GitHub tools to verify CI/CD pipelines for merged repositories.
Combines GitHub API access with local verification capabilities.

Author: Agent-3 (Infrastructure & DevOps Specialist)
"""

import json
import logging
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import existing tools
try:
    from tools.fetch_repo_names import fetch_repo_info, get_github_token, get_github_owner
    from tools.analysis.audit_github_repos import audit_repository
    from src.tools.github_scanner import GitHubScanner
    TOOLS_AVAILABLE = True
except ImportError as e:
    logger.warning(f"⚠️ Some tools not available: {e}")
    TOOLS_AVAILABLE = False


class EnhancedCICDVerifier:
    """Enhanced CI/CD verification using existing GitHub tools."""

    def __init__(self, owner: Optional[str] = None, token: Optional[str] = None):
        """Initialize verifier with GitHub credentials."""
        self.token = token or get_github_token() if TOOLS_AVAILABLE else None
        self.owner = owner or get_github_owner() if TOOLS_AVAILABLE else "dadudekc"
        self.scanner = None
        if self.token and TOOLS_AVAILABLE:
            try:
                self.scanner = GitHubScanner(token=self.token)
            except Exception as e:
                logger.warning(f"⚠️ Could not initialize GitHubScanner: {e}")

    def verify_repo_via_api(self, repo_name: str) -> Dict[str, Any]:
        """
        Verify CI/CD via GitHub API (no cloning required).
        
        Args:
            repo_name: Repository name
            
        Returns:
            Verification results dictionary
        """
        results = {
            "repo": f"{self.owner}/{repo_name}",
            "verification_method": "github_api",
            "pipeline_exists": False,
            "pipeline_files": [],
            "dependencies": {},
            "testing_setup": {},
            "status": "unknown",
        }

        if not TOOLS_AVAILABLE:
            results["error"] = "Required tools not available"
            results["status"] = "error"
            return results

        logger.info(f"🔍 Verifying CI/CD via API for: {self.owner}/{repo_name}")

        # Get repo info
        repo_info = fetch_repo_info(self.owner, repo_name, self.token)
        if not repo_info:
            results["status"] = "repo_not_found"
            results["error"] = f"Repository {self.owner}/{repo_name} not found"
            return results

        results["repo_info"] = {
            "name": repo_info.get("name"),
            "full_name": repo_info.get("full_name"),
            "url": repo_info.get("html_url"),
            "clone_url": repo_info.get("clone_url"),
            "default_branch": repo_info.get("default_branch", "main"),
        }

        # Check for workflows via GitHub Contents API
        try:
            import requests
            headers = {
                "Accept": "application/vnd.github.v3+json",
            }
            if self.token:
                headers["Authorization"] = f"token {self.token}"

            # Check for .github/workflows directory
            workflows_url = f"https://api.github.com/repos/{self.owner}/{repo_name}/contents/.github/workflows"
            response = requests.get(workflows_url, headers=headers, timeout=10)

            if response.status_code == 200:
                workflow_files = response.json()
                if isinstance(workflow_files, list):
                    yml_files = [f for f in workflow_files if f.get("name", "").endswith((".yml", ".yaml"))]
                    results["pipeline_exists"] = len(yml_files) > 0
                    results["pipeline_files"] = [f.get("name") for f in yml_files]
                    logger.info(f"✅ Found {len(yml_files)} workflow file(s) via API")
            elif response.status_code == 404:
                logger.warning(f"⚠️ No .github/workflows directory found")
                results["pipeline_exists"] = False
            else:
                logger.warning(f"⚠️ Could not check workflows: {response.status_code}")

        except Exception as e:
            logger.warning(f"⚠️ Error checking workflows via API: {e}")

        # Check for dependency files via API
        dependency_files = ["requirements.txt", "requirements-dev.txt", "package.json", "pyproject.toml"]
        for dep_file in dependency_files:
            try:
                import requests
                headers = {
                    "Accept": "application/vnd.github.v3+json",
                }
                if self.token:
                    headers["Authorization"] = f"token {self.token}"

                file_url = f"https://api.github.com/repos/{self.owner}/{repo_name}/contents/{dep_file}"
                response = requests.get(file_url, headers=headers, timeout=10)

                if response.status_code == 200:
                    results["dependencies"][dep_file] = "exists"
                    logger.info(f"✅ Found {dep_file} via API")
            except Exception as e:
                logger.debug(f"Could not check {dep_file}: {e}")

        # Check for test directories (requires cloning or tree API)
        # For now, mark as "requires_clone"
        results["testing_setup"] = {
            "verification_method": "requires_clone",
            "note": "Test directories require cloning or tree API access",
        }

        # Determine status
        if results["pipeline_exists"]:
            if results["dependencies"]:
                results["status"] = "complete"
            else:
                results["status"] = "pipeline_only"
        else:
            if results["dependencies"]:
                results["status"] = "dependencies_only"
            else:
                results["status"] = "missing"

        return results

    def verify_repo_via_clone(self, repo_name: str, clone_dir: Optional[Path] = None) -> Dict[str, Any]:
        """
        Verify CI/CD by cloning repository (more comprehensive).
        
        Args:
            repo_name: Repository name
            clone_dir: Directory to clone into (default: temp_repos/)
            
        Returns:
            Verification results dictionary
        """
        if not TOOLS_AVAILABLE:
            return {"error": "Required tools not available", "status": "error"}

        logger.info(f"🔍 Verifying CI/CD via clone for: {self.owner}/{repo_name}")

        clone_dir = clone_dir or project_root / "temp_repos" / "cicd_verification"
        clone_dir.mkdir(parents=True, exist_ok=True)

        repo_path = clone_dir / repo_name
        clone_url = f"https://github.com/{self.owner}/{repo_name}.git"

        # Use existing audit function
        try:
            results = audit_repository(repo_name, clone_url, clone_dir)
            
            # Convert to our format
            verification_results = {
                "repo": f"{self.owner}/{repo_name}",
                "verification_method": "clone",
                "pipeline_exists": results.get("has_ci_cd", False),
                "pipeline_files": [],
                "workflow_count": results.get("workflow_count", 0),
                "dependencies": {
                    "requirements.txt": results.get("has_requirements", False),
                    "package.json": results.get("has_package_json", False),
                },
                "testing_setup": {
                    "has_tests": results.get("has_tests", False),
                    "test_count": results.get("test_count", 0),
                },
                "professional_setup": {
                    "has_readme": results.get("has_readme", False),
                    "has_license": results.get("has_license", False),
                    "has_gitignore": results.get("has_gitignore", False),
                },
                "recommendations": results.get("recommendations", []),
                "issues": results.get("issues", []),
                "status": "complete" if results.get("has_ci_cd") else "incomplete",
            }

            return verification_results

        except Exception as e:
            logger.error(f"❌ Error during clone verification: {e}")
            return {
                "repo": f"{self.owner}/{repo_name}",
                "verification_method": "clone",
                "status": "error",
                "error": str(e),
            }

    def verify_merge(self, merge_info: Dict[str, Any], method: str = "api") -> Dict[str, Any]:
        """
        Verify CI/CD for a specific merge.
        
        Args:
            merge_info: Dictionary with merge information
            method: "api" (fast, no clone) or "clone" (comprehensive)
            
        Returns:
            Verification results
        """
        target_repo = merge_info.get("target_repo") or merge_info.get("target")
        if not target_repo:
            logger.error("❌ No target_repo specified in merge_info")
            return {"error": "No target_repo specified", "status": "error"}

        # Extract repo name (handle various formats)
        if "/" in target_repo:
            parts = target_repo.split("/")
            repo_name = parts[-1].replace(".git", "")
        else:
            repo_name = target_repo

        logger.info(f"🔍 Verifying merge: {merge_info.get('source_repo')} → {repo_name}")

        if method == "clone":
            return self.verify_repo_via_clone(repo_name)
        else:
            return self.verify_repo_via_api(repo_name)

    def close(self):
        """Close scanner if open."""
        if self.scanner:
            try:
                self.scanner.close()
            except Exception:
                pass


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Enhanced CI/CD verification for merged repos"
    )
    parser.add_argument(
        "repo_name",
        help="Repository name to verify",
    )
    parser.add_argument(
        "--owner",
        "-o",
        help="Repository owner (default: auto-detect)",
    )
    parser.add_argument(
        "--method",
        "-m",
        choices=["api", "clone"],
        default="api",
        help="Verification method: api (fast) or clone (comprehensive)",
    )
    parser.add_argument(
        "--token",
        "-t",
        help="GitHub token (or set GITHUB_TOKEN env var)",
    )

    args = parser.parse_args()

    verifier = EnhancedCICDVerifier(owner=args.owner, token=args.token)

    try:
        if args.method == "clone":
            results = verifier.verify_repo_via_clone(args.repo_name)
        else:
            results = verifier.verify_repo_via_api(args.repo_name)

        print(json.dumps(results, indent=2))
    finally:
        verifier.close()


if __name__ == "__main__":
    main()

