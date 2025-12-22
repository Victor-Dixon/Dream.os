#!/usr/bin/env python3
"""
Configure Git Authentication with GitHub Token
==============================================

Configures git remote URL to use GitHub token from .env file for authentication.
Uses FG_PROFESSIONAL_DEVELOPMENT_ACCOUNT_GITHUB_TOKEN or GITHUB_TOKEN from .env.

<!-- SSOT Domain: core -->

Author: Agent-2 (Architecture & Design Specialist)
Date: 2025-12-22
V2 Compliant: Yes (<300 lines)
"""

import subprocess
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.core.utils.github_utils import get_github_token


def configure_git_remote_with_token(remote_name: str = "origin") -> bool:
    """
    Configure git remote URL to include GitHub token for authentication.

    Args:
        remote_name: Name of the remote (default: "origin")

    Returns:
        True if successful, False otherwise
    """
    # Get GitHub token
    token = get_github_token()
    if not token:
        print("❌ ERROR: GitHub token not found in .env file")
        print("   Expected: FG_PROFESSIONAL_DEVELOPMENT_ACCOUNT_GITHUB_TOKEN or GITHUB_TOKEN")
        return False

    # Get current remote URL
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", remote_name],
            capture_output=True,
            text=True,
            check=True,
        )
        current_url = result.stdout.strip()
    except subprocess.CalledProcessError:
        print(f"❌ ERROR: Remote '{remote_name}' not found")
        return False

    # Parse current URL to extract owner/repo
    repo_path = None
    
    if current_url.startswith("https://"):
        # Handle https://github.com/owner/repo.git or https://token@github.com/owner/repo.git
        if "github.com" in current_url:
            # Remove protocol and any existing token
            parts = current_url.replace("https://", "").split("@")
            if len(parts) > 1:
                # Has token, use the part after @
                repo_part = parts[-1]
            else:
                # No token, use the whole thing
                repo_part = parts[0]
            
            # Extract owner/repo
            if repo_part.startswith("github.com/"):
                repo_path = repo_part.replace("github.com/", "").replace(".git", "")
            else:
                print(f"❌ ERROR: Could not parse repo path from: {current_url}")
                return False
        else:
            print(f"❌ ERROR: Unsupported remote URL format: {current_url}")
            return False
    elif current_url.startswith("git@github.com:"):
        # SSH URL - convert to HTTPS with token
        repo_path = current_url.replace("git@github.com:", "").replace(".git", "")
    else:
        print(f"❌ ERROR: Unsupported remote URL format: {current_url}")
        return False
    
    if not repo_path:
        print(f"❌ ERROR: Could not extract repo path from: {current_url}")
        return False
    
    # Construct new URL with token
    new_url = f"https://{token}@github.com/{repo_path}.git"

    # Update remote URL
    try:
        subprocess.run(
            ["git", "remote", "set-url", remote_name, new_url],
            check=True,
        )
        print(f"✅ Successfully configured '{remote_name}' remote with token authentication")
        print(f"   URL: https://***@github.com/{repo_path}.git")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ ERROR: Failed to update remote URL: {e}")
        return False


def main():
    """Main execution function."""
    remote_name = sys.argv[1] if len(sys.argv) > 1 else "origin"

    print(f"🔧 Configuring git authentication for remote '{remote_name}'...")
    success = configure_git_remote_with_token(remote_name)

    if success:
        print("\n✅ Git authentication configured successfully!")
        print("   You can now push to the remote repository.")
        return 0
    else:
        print("\n❌ Failed to configure git authentication")
        return 1


if __name__ == "__main__":
    sys.exit(main())

