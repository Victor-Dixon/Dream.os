#!/usr/bin/env python3
"""
Git Token Push Tool
===================

Handles git push operations using GitHub token authentication.
Uses FG_PROFESSIONAL_DEVELOPMENT_ACCOUNT_GITHUB_TOKEN from environment.

Usage:
    python tools/git_token_push.py                    # Push current branch
    python tools/git_token_push.py --commit "msg"     # Add, commit, push
    python tools/git_token_push.py --force            # Force push

Author: Agent-7 (Git Authentication Specialist)
V2 Compliant: <200 lines
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path
from typing import Optional, Tuple

# Import token utility
try:
    sys.path.append(str(Path(__file__).parent.parent))
    from src.core.utils.github_utils import get_github_token
    GITHUB_UTILS_AVAILABLE = True
except ImportError:
    GITHUB_UTILS_AVAILABLE = False


def get_repo_info() -> Tuple[str, str]:
    """Get repository owner and name from git remote."""
    try:
        result = subprocess.run(
            ['git', 'remote', 'get-url', 'origin'],
            capture_output=True,
            text=True,
            check=True
        )
        url = result.stdout.strip()

        # Handle different URL formats
        if 'github.com/' in url:
            if url.startswith('https://'):
                # https://github.com/owner/repo.git
                parts = url.split('github.com/')[1].split('/')
            elif url.startswith('git@'):
                # git@github.com:owner/repo.git
                parts = url.split('github.com:')[1].split('/')
            else:
                raise ValueError(f"Unsupported URL format: {url}")

            owner = parts[0]
            repo = parts[1].replace('.git', '')
            return owner, repo

    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to get repository info: {e}")
        sys.exit(1)

    raise ValueError(f"Could not parse repository URL: {url}")


def setup_git_credentials(owner: str, token: str) -> None:
    """Configure git to use token for authentication."""
    # Set up credential helper with token
    credential_url = f"https://{owner}:{token}@github.com"

    try:
        # Configure credential helper for this session
        subprocess.run([
            'git', 'config', '--local',
            'credential.helper', 'store'
        ], check=True)

        # Store credentials (this creates/overwrites .git/credentials)
        credential_line = f"{credential_url}\n"
        git_dir = Path('.git')
        if git_dir.exists():
            cred_file = git_dir / 'credentials'
            with open(cred_file, 'w') as f:
                f.write(credential_line)
            print(f"✅ Git credentials configured for {owner}")

    except subprocess.CalledProcessError as e:
        print(f"⚠️ Failed to configure git credentials: {e}")
        print("   You may need to authenticate manually for this push")


def run_git_command(command: list, description: str) -> bool:
    """Run git command and return success status."""
    try:
        print(f"🔄 {description}...")
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"✅ {description} successful")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stdout:
            print(f"   stdout: {e.stdout}")
        if e.stderr:
            print(f"   stderr: {e.stderr}")
        return False


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Git push with token authentication")
    parser.add_argument('--commit', '-c', help='Commit message (will add and commit all changes)')
    parser.add_argument('--force', '-f', action='store_true', help='Force push')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be done without executing')

    args = parser.parse_args()

    # Get GitHub token
    if not GITHUB_UTILS_AVAILABLE:
        print("❌ GitHub utils not available")
        sys.exit(1)

    token = get_github_token()
    if not token:
        print("❌ No GitHub token found in environment or .env file")
        print("   Set FG_PROFESSIONAL_DEVELOPMENT_ACCOUNT_GITHUB_TOKEN")
        sys.exit(1)

    print("🔑 GitHub token found, configuring authentication...")

    # Get repository info
    try:
        owner, repo = get_repo_info()
        print(f"📦 Repository: {owner}/{repo}")
    except ValueError as e:
        print(f"❌ {e}")
        sys.exit(1)

    # Setup git credentials
    setup_git_credentials(owner, token)

    success = True

    # Handle commit if requested
    if args.commit:
        if not run_git_command(['git', 'add', '-A'], "Staging all changes"):
            success = False

        if success and not run_git_command(
            ['git', 'commit', '-m', args.commit],
            f"Committing with message: {args.commit}"
        ):
            success = False

    # Push
    if success:
        push_cmd = ['git', 'push']
        if args.force:
            push_cmd.append('--force')

        description = "Force pushing" if args.force else "Pushing"
        if not run_git_command(push_cmd, description):
            success = False

    if success:
        print("🎉 Git operations completed successfully!")
        sys.exit(0)
    else:
        print("❌ Some git operations failed")
        sys.exit(1)


if __name__ == "__main__":
    main()