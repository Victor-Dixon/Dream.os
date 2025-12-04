#!/usr/bin/env python3
"""
GitHub Rate Limit Handler
=========================

Provides rate limit checking, retry logic, and fallback options for GitHub operations.

Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2025-01-27
Priority: HIGH
"""

import os
import time
import subprocess
from pathlib import Path
from typing import Optional, Dict, Any, Tuple, Callable
import sys

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))


def get_github_token() -> Optional[str]:
    """Get GitHub token from environment or .env file."""
    # Check environment variable first
    token = os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN")
    if token:
        return token
    
    # Check .env file
    env_file = project_root / ".env"
    if env_file.exists():
        try:
            with open(env_file, "r") as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("GITHUB_TOKEN=") or line.startswith("GH_TOKEN="):
                        return line.split("=", 1)[1].strip().strip('"').strip("'")
        except Exception:
            pass
    
    return None


def check_github_rate_limit() -> Dict[str, Any]:
    """
    Check GitHub API rate limit status.
    
    Returns:
        Dictionary with rate limit information
    """
    try:
        result = subprocess.run(
            ["gh", "api", "rate_limit"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            import json
            data = json.loads(result.stdout)
            
            core = data.get("resources", {}).get("core", {})
            graphql = data.get("resources", {}).get("graphql", {})
            
            return {
                "core": {
                    "remaining": core.get("remaining", 0),
                    "limit": core.get("limit", 0),
                    "reset_time": core.get("reset", 0),
                },
                "graphql": {
                    "remaining": graphql.get("remaining", 0),
                    "limit": graphql.get("limit", 0),
                    "reset_time": graphql.get("reset", 0),
                },
                "status": "ok"
            }
        else:
            # If GitHub CLI fails, try API directly
            token = get_github_token()
            if token:
                import requests
                headers = {
                    "Authorization": f"token {token}",
                    "Accept": "application/vnd.github.v3+json"
                }
                response = requests.get(
                    "https://api.github.com/rate_limit",
                    headers=headers,
                    timeout=10
                )
                if response.status_code == 200:
                    data = response.json()
                    core = data.get("resources", {}).get("core", {})
                    return {
                        "core": {
                            "remaining": core.get("remaining", 0),
                            "limit": core.get("limit", 0),
                            "reset_time": core.get("reset", 0),
                        },
                        "graphql": {
                            "remaining": 0,
                            "limit": 0,
                            "reset_time": 0,
                        },
                        "status": "ok"
                    }
            
            return {
                "core": {"remaining": 0, "limit": 0, "reset_time": 0},
                "graphql": {"remaining": 0, "limit": 0, "reset_time": 0},
                "status": "error",
                "error": result.stderr
            }
    except Exception as e:
        return {
            "core": {"remaining": 0, "limit": 0, "reset_time": 0},
            "graphql": {"remaining": 0, "limit": 0, "reset_time": 0},
            "status": "error",
            "error": str(e)
        }


def check_rate_limit_before_operation(operation_name: str, min_remaining: int = 10) -> Tuple[bool, str]:
    """
    Check rate limit before operation.
    
    Args:
        operation_name: Name of the operation
        min_remaining: Minimum remaining requests required
    
    Returns:
        Tuple of (can_proceed, message)
    """
    rate_limit = check_github_rate_limit()
    
    if rate_limit["status"] != "ok":
        return True, "⚠️ Could not check rate limit, proceeding anyway"
    
    core = rate_limit["core"]
    graphql = rate_limit["graphql"]
    
    # Check GraphQL (more restrictive)
    if graphql["remaining"] == 0 and graphql["reset_time"] > 0:
        reset_time = graphql["reset_time"]
        wait_seconds = max(0, reset_time - time.time())
        wait_minutes = wait_seconds / 60
        return False, f"❌ GraphQL rate limit exceeded. Reset in {wait_minutes:.1f} minutes"
    
    # Check Core API
    if core["remaining"] == 0 and core["reset_time"] > 0:
        reset_time = core["reset_time"]
        wait_seconds = max(0, reset_time - time.time())
        wait_minutes = wait_seconds / 60
        return False, f"❌ Core API rate limit exceeded. Reset in {wait_minutes:.1f} minutes"
    
    # Warn if low
    if core["remaining"] < min_remaining:
        return True, f"⚠️ Low rate limit: {core['remaining']} remaining (min: {min_remaining})"
    
    if graphql["remaining"] < min_remaining:
        return True, f"⚠️ Low GraphQL rate limit: {graphql['remaining']} remaining"
    
    return True, f"✅ Rate limit OK (Core: {core['remaining']}, GraphQL: {graphql['remaining']})"


def execute_with_retry(
    operation: Callable,
    operation_name: str = "operation",
    max_retries: int = 3,
    base_delay: int = 60
) -> Any:
    """
    Execute operation with rate limit retry logic.
    
    Args:
        operation: Function to execute
        operation_name: Name of operation for logging
        max_retries: Maximum retry attempts
        base_delay: Base delay in seconds
    
    Returns:
        Result of operation
    
    Raises:
        Exception: If operation fails after max retries
    """
    for attempt in range(max_retries):
        try:
            # Check rate limit before operation
            can_proceed, message = check_rate_limit_before_operation(operation_name)
            if not can_proceed:
                if attempt == max_retries - 1:
                    raise Exception(f"Rate limit exceeded: {message}")
                
                # Extract wait time from message
                rate_limit = check_github_rate_limit()
                if rate_limit["status"] == "ok":
                    graphql = rate_limit["graphql"]
                    core = rate_limit["core"]
                    
                    # Use GraphQL reset time if available, else core
                    reset_time = graphql.get("reset_time", 0) or core.get("reset_time", 0)
                    if reset_time > 0:
                        wait_time = max(base_delay, reset_time - time.time())
                        wait_time = min(wait_time, 3600)  # Max 1 hour
                        
                        print(f"⏳ Rate limit exceeded. Waiting {wait_time:.0f}s before retry {attempt + 1}/{max_retries}")
                        time.sleep(wait_time)
                        continue
            
            # Execute operation
            result = operation()
            return result
            
        except subprocess.CalledProcessError as e:
            error_output = e.stderr or e.stdout or str(e)
            
            # Check if it's a rate limit error
            if "rate limit" in error_output.lower() or "429" in error_output:
                if attempt == max_retries - 1:
                    raise Exception(f"Rate limit error after {max_retries} attempts: {error_output}")
                
                # Calculate wait time
                rate_limit = check_github_rate_limit()
                if rate_limit["status"] == "ok":
                    graphql = rate_limit["graphql"]
                    core = rate_limit["core"]
                    
                    reset_time = graphql.get("reset_time", 0) or core.get("reset_time", 0)
                    if reset_time > 0:
                        wait_time = max(base_delay, reset_time - time.time())
                        wait_time = min(wait_time, 3600)
                        
                        print(f"⏳ Rate limit error detected. Waiting {wait_time:.0f}s before retry {attempt + 1}/{max_retries}")
                        time.sleep(wait_time)
                        continue
                else:
                    # Fallback delay
                    wait_time = base_delay * (2 ** attempt)
                    print(f"⏳ Rate limit error detected. Waiting {wait_time}s before retry {attempt + 1}/{max_retries}")
                    time.sleep(wait_time)
                    continue
            
            # Not a rate limit error, re-raise
            raise
            
        except Exception as e:
            error_str = str(e).lower()
            if "rate limit" in error_str or "429" in error_str:
                if attempt == max_retries - 1:
                    raise
                
                # Calculate wait time
                rate_limit = check_github_rate_limit()
                if rate_limit["status"] == "ok":
                    graphql = rate_limit["graphql"]
                    core = rate_limit["core"]
                    
                    reset_time = graphql.get("reset_time", 0) or core.get("reset_time", 0)
                    if reset_time > 0:
                        wait_time = max(base_delay, reset_time - time.time())
                        wait_time = min(wait_time, 3600)
                        
                        print(f"⏳ Rate limit error. Waiting {wait_time:.0f}s before retry {attempt + 1}/{max_retries}")
                        time.sleep(wait_time)
                        continue
                else:
                    wait_time = base_delay * (2 ** attempt)
                    print(f"⏳ Rate limit error. Waiting {wait_time}s before retry {attempt + 1}/{max_retries}")
                    time.sleep(wait_time)
                    continue
            
            # Not a rate limit error, re-raise
            raise
    
    raise Exception(f"Operation failed after {max_retries} attempts")


def generate_manual_instructions(operation_type: str, **kwargs) -> str:
    """
    Generate manual operation instructions when rate limited.
    
    Args:
        operation_type: Type of operation (pr_create, pr_merge, etc.)
        **kwargs: Operation-specific parameters
    
    Returns:
        Manual instructions string
    """
    if operation_type == "pr_merge":
        repo = kwargs.get("repo", "owner/repo")
        pr_number = kwargs.get("pr_number", "N")
        
        return f"""
⚠️ RATE LIMIT EXCEEDED - Manual Merge Required

PR: {repo}#{pr_number}

Manual Steps:
1. Navigate to: https://github.com/{repo}/pull/{pr_number}
2. Review PR changes
3. Click "Merge pull request" button
4. Select merge method (merge commit recommended)
5. Confirm merge
6. Delete source branch if prompted

Alternative: Wait for rate limit reset and retry automatically
"""
    
    elif operation_type == "pr_create":
        repo = kwargs.get("repo", "owner/repo")
        source = kwargs.get("source", "source-repo")
        target = kwargs.get("target", "target-repo")
        base = kwargs.get("base", "main")
        head = kwargs.get("head", "main")
        
        return f"""
⚠️ RATE LIMIT EXCEEDED - Manual PR Creation Required

Merge: {source} → {target}

Manual Steps:
1. Navigate to: https://github.com/{repo}/compare/{base}...{source}:{head}
2. Review changes
3. Click "Create pull request"
4. Title: "Merge {source} into {target}"
5. Description: Repository consolidation merge
6. Create pull request

Alternative: Wait for rate limit reset and retry automatically
"""
    
    return "⚠️ Rate limit exceeded. Please wait for reset or use GitHub UI."


if __name__ == "__main__":
    """Test rate limit checking."""
    print("🔍 Checking GitHub rate limit status...")
    rate_limit = check_github_rate_limit()
    
    if rate_limit["status"] == "ok":
        core = rate_limit["core"]
        graphql = rate_limit["graphql"]
        
        print(f"\n📊 Core API:")
        print(f"   Remaining: {core['remaining']}/{core['limit']}")
        if core['reset_time'] > 0:
            reset_seconds = max(0, core['reset_time'] - time.time())
            reset_minutes = reset_seconds / 60
            print(f"   Reset: {reset_minutes:.1f} minutes")
        
        print(f"\n📊 GraphQL API:")
        print(f"   Remaining: {graphql['remaining']}/{graphql['limit']}")
        if graphql['reset_time'] > 0:
            reset_seconds = max(0, graphql['reset_time'] - time.time())
            reset_minutes = reset_seconds / 60
            print(f"   Reset: {reset_minutes:.1f} minutes")
        
        # Test pre-flight check
        can_proceed, message = check_rate_limit_before_operation("test operation")
        print(f"\n✅ Pre-flight check: {message}")
    else:
        print(f"❌ Error checking rate limit: {rate_limit.get('error', 'Unknown error')}")

