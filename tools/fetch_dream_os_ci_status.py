#!/usr/bin/env python3
"""
Fetch Dream.os CI Status from GitHub API
Agent-3 (Infrastructure & DevOps)

Fetches the latest CI/CD workflow run status for Dream.os repository.

<!-- SSOT Domain: infrastructure -->
"""

import os
import sys
import json
import requests
from typing import Optional, Dict, List
from datetime import datetime

# Color output
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
RESET = "\033[0m"

REPO_OWNER = "Victor-Dixon"
REPO_NAME = "Dream.os"
GITHUB_API_BASE = "https://api.github.com"


def get_github_token() -> Optional[str]:
    """Get GitHub token from environment."""
    return os.getenv(
        "GITHUB_TOKEN"
    ) or os.getenv(
        "FG_PROFESSIONAL_DEVELOPMENT_ACCOUNT_GITHUB_TOKEN"
    )


def fetch_workflow_runs(limit: int = 5) -> Optional[List[Dict]]:
    """Fetch recent workflow runs from GitHub API."""
    token = get_github_token()
    
    if not token:
        print(f"{YELLOW}⚠{RESET} No GitHub token found in environment")
        print(f"   Set GITHUB_TOKEN or FG_PROFESSIONAL_DEVELOPMENT_ACCOUNT_GITHUB_TOKEN")
        return None
    
    url = f"{GITHUB_API_BASE}/repos/{REPO_OWNER}/{REPO_NAME}/actions/runs"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }
    
    try:
        response = requests.get(url, headers=headers, params={"per_page": limit})
        response.raise_for_status()
        data = response.json()
        return data.get("workflow_runs", [])
    except requests.exceptions.RequestException as e:
        print(f"{RED}✗{RESET} Failed to fetch workflow runs: {e}")
        return None


def fetch_workflow_run_details(run_id: int) -> Optional[Dict]:
    """Fetch detailed information about a specific workflow run."""
    token = get_github_token()
    
    if not token:
        return None
    
    url = f"{GITHUB_API_BASE}/repos/{REPO_OWNER}/{REPO_NAME}/actions/runs/{run_id}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"{RED}✗{RESET} Failed to fetch run details: {e}")
        return None


def fetch_job_details(run_id: int) -> Optional[List[Dict]]:
    """Fetch job details for a workflow run."""
    token = get_github_token()
    
    if not token:
        return None
    
    url = f"{GITHUB_API_BASE}/repos/{REPO_OWNER}/{REPO_NAME}/actions/runs/{run_id}/jobs"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data.get("jobs", [])
    except requests.exceptions.RequestException as e:
        print(f"{RED}✗{RESET} Failed to fetch job details: {e}")
        return None


def get_status_icon(status: str, conclusion: Optional[str]) -> str:
    """Get status icon based on workflow status."""
    if status == "completed":
        if conclusion == "success":
            return f"{GREEN}✓{RESET}"
        elif conclusion == "failure":
            return f"{RED}✗{RESET}"
        elif conclusion == "cancelled":
            return f"{YELLOW}⊘{RESET}"
        else:
            return f"{YELLOW}?{RESET}"
    elif status == "in_progress":
        return f"{BLUE}⟳{RESET}"
    elif status == "queued":
        return f"{YELLOW}⏳{RESET}"
    else:
        return f"{YELLOW}?{RESET}"


def format_timestamp(timestamp: str) -> str:
    """Format ISO timestamp to readable format."""
    try:
        dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except:
        return timestamp


def display_workflow_runs(runs: List[Dict]):
    """Display workflow runs in a readable format."""
    print(f"\n{BLUE}📊 Recent Workflow Runs{RESET}")
    print("=" * 80)
    
    for run in runs:
        status = run.get("status", "unknown")
        conclusion = run.get("conclusion")
        icon = get_status_icon(status, conclusion)
        
        workflow_name = run.get("name", "Unknown")
        branch = run.get("head_branch", "unknown")
        commit_sha = run.get("head_sha", "")[:7]
        created_at = format_timestamp(run.get("created_at", ""))
        run_id = run.get("id")
        
        print(f"\n{icon} {workflow_name}")
        print(f"   Branch: {branch}")
        print(f"   Commit: {commit_sha}")
        print(f"   Status: {status} ({conclusion or 'N/A'})")
        print(f"   Created: {created_at}")
        print(f"   Run ID: {run_id}")
        print(f"   URL: {run.get('html_url', 'N/A')}")
        
        # Fetch and display job details for failed runs
        if conclusion == "failure" and run_id:
            jobs = fetch_job_details(run_id)
            if jobs:
                print(f"\n   {RED}Failed Jobs:{RESET}")
                for job in jobs:
                    job_conclusion = job.get("conclusion")
                    if job_conclusion == "failure":
                        job_name = job.get("name", "Unknown")
                        print(f"     {RED}✗{RESET} {job_name}")
                        print(f"        URL: {job.get('html_url', 'N/A')}")


def main():
    """Main function."""
    print(f"\n{BLUE}{'='*80}{RESET}")
    print(f"{BLUE}🔍 Dream.os CI Status Checker{RESET}")
    print(f"{BLUE}{'='*80}{RESET}")
    
    print(f"\n{BLUE}Repository:{RESET} {REPO_OWNER}/{REPO_NAME}")
    print(f"{BLUE}API Endpoint:{RESET} {GITHUB_API_BASE}/repos/{REPO_OWNER}/{REPO_NAME}/actions")
    
    runs = fetch_workflow_runs(limit=5)
    
    if runs is None:
        print(f"\n{YELLOW}⚠{RESET} Could not fetch workflow runs")
        print(f"   Make sure you have a GitHub token set in your environment")
        print(f"   Or visit: https://github.com/{REPO_OWNER}/{REPO_NAME}/actions")
        return
    
    if not runs:
        print(f"\n{YELLOW}⚠{RESET} No workflow runs found")
        print(f"   This might mean:")
        print(f"   1. No workflows have been triggered yet")
        print(f"   2. The repository doesn't have CI/CD configured")
        print(f"   3. The repository is private and requires authentication")
        return
    
    display_workflow_runs(runs)
    
    # Check for failures
    failed_runs = [r for r in runs if r.get("conclusion") == "failure"]
    if failed_runs:
        print(f"\n{RED}❌ Found {len(failed_runs)} failed workflow run(s){RESET}")
        print(f"\n{BLUE}💡 Next Steps:{RESET}")
        print(f"   1. Click on the workflow run URL to see detailed logs")
        print(f"   2. Check the failed job logs for error messages")
        print(f"   3. Run the diagnostic tool: python tools/diagnose_dream_os_ci_failure.py")
        print(f"   4. Fix the issues and push a new commit to trigger CI again")
    else:
        print(f"\n{GREEN}✓{RESET} No failed runs in recent workflow history")
    
    print(f"\n{BLUE}{'='*80}{RESET}\n")


if __name__ == "__main__":
    try:
        import requests
    except ImportError:
        print(f"{RED}✗{RESET} Missing dependency: requests")
        print(f"   Install with: pip install requests")
        sys.exit(1)
    
    main()

