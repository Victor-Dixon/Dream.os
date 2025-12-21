#!/usr/bin/env python3
"""
Remote Router Module - Synthetic GitHub
=======================================

<!-- SSOT Domain: integration -->

Extracted from synthetic_github.py for V2 compliance.
Handles remote GitHub API calls with rate limiting and error handling.

V2 Compliance | Author: Agent-1 | Date: 2025-12-14
"""

from __future__ import annotations

import logging
import subprocess
from pathlib import Path
from typing import Optional, Tuple, Dict, Any

from ..local_repo_layer import get_local_repo_manager
from ..deferred_push_queue import get_deferred_push_queue
from ..config.timeout_constants import TimeoutConstants
from .sandbox_manager import GitHubSandboxMode

logger = logging.getLogger(__name__)


class RemoteRouter:
    """Handles remote GitHub API calls for synthetic GitHub operations."""
    
    def __init__(
        self,
        local_repo_manager,
        deferred_queue,
        sandbox_mode: GitHubSandboxMode
    ):
        """
        Initialize remote router.
        
        Args:
            local_repo_manager: Local repository manager instance
            deferred_queue: Deferred push queue instance
            sandbox_mode: Sandbox mode manager instance
        """
        self.local_repo_manager = local_repo_manager
        self.deferred_queue = deferred_queue
        self.sandbox_mode = sandbox_mode
    
    def push_branch(
        self,
        repo_name: str,
        branch: str,
        force: bool = False
    ) -> Tuple[bool, Optional[str]]:
        """
        Push branch to GitHub (with deferred queue fallback).
        
        Args:
            repo_name: Name of repository
            branch: Branch to push
            force: Force push
        
        Returns:
            Tuple of (success, error_message)
        """
        # Check sandbox mode
        if self.sandbox_mode.is_enabled():
            logger.info(f"🔒 Sandbox mode: Deferring push {repo_name}/{branch}")
            self.deferred_queue.enqueue_push(
                repo=repo_name,
                branch=branch,
                reason="sandbox_mode"
            )
            return False, "Sandbox mode enabled"
        
        # Try to push to GitHub
        repo_path = self.local_repo_manager.get_repo_path(repo_name)
        if not repo_path:
            return False, "Repository not found locally"
        
        try:
            # Get GitHub URL
            repo_info = self.local_repo_manager.get_repo_status(repo_name)
            if not repo_info or "github_url" not in repo_info:
                return False, "No GitHub URL configured"
            
            github_url = repo_info["github_url"]
            
            # Push command
            cmd = ["git", "push"]
            if force:
                cmd.append("--force")
            cmd.extend([github_url.replace(".git", ""), branch])
            
            result = subprocess.run(
                cmd,
                cwd=repo_path,
                capture_output=True,
                text=True,
                timeout=TimeoutConstants.HTTP_MEDIUM
            )
            
            if result.returncode == 0:
                logger.info(f"✅ Pushed to GitHub: {repo_name}/{branch}")
                return True, None
            else:
                error_msg = result.stderr or result.stdout
                
                # Check for rate limit
                if "rate limit" in error_msg.lower() or "429" in error_msg:
                    logger.warning(f"⚠️ Rate limit: Deferring push {repo_name}/{branch}")
                    self.deferred_queue.enqueue_push(
                        repo=repo_name,
                        branch=branch,
                        reason="rate_limit"
                    )
                    self.sandbox_mode.enable("rate_limit")
                    return False, "Rate limit - deferred"
                
                # Other errors - defer anyway
                logger.warning(f"⚠️ Push failed: Deferring {repo_name}/{branch}")
                self.deferred_queue.enqueue_push(
                    repo=repo_name,
                    branch=branch,
                    reason="push_failed"
                )
                return False, error_msg
                
        except subprocess.TimeoutExpired:
            logger.error(f"❌ Push timeout: {repo_name}/{branch}")
            self.deferred_queue.enqueue_push(
                repo=repo_name,
                branch=branch,
                reason="timeout"
            )
            return False, "Timeout"
        except Exception as e:
            logger.error(f"❌ Push error: {e}")
            self.deferred_queue.enqueue_push(
                repo=repo_name,
                branch=branch,
                reason=f"error: {str(e)}"
            )
            return False, str(e)
    
    def create_pr(
        self,
        repo_name: str,
        branch: str,
        base_branch: str = "main",
        title: Optional[str] = None,
        body: Optional[str] = None
    ) -> Tuple[bool, Optional[str]]:
        """
        Create pull request (with deferred queue fallback).
        
        Args:
            repo_name: Name of repository
            branch: Branch for PR
            base_branch: Base branch
            title: PR title
            body: PR body
        
        Returns:
            Tuple of (success, pr_url_or_error)
        """
        # Check sandbox mode
        if self.sandbox_mode.is_enabled():
            logger.info(f"🔒 Sandbox mode: Deferring PR creation {repo_name}/{branch}")
            self.deferred_queue.enqueue_push(
                repo=repo_name,
                branch=branch,
                reason="sandbox_mode_pr",
                metadata={
                    "pr_title": title,
                    "pr_body": body,
                    "base_branch": base_branch,
                    "action": "create_pr"
                }
            )
            return False, "Sandbox mode enabled"
        
        # Try to create PR via GitHub CLI
        try:
            repo_info = self.local_repo_manager.get_repo_status(repo_name)
            if not repo_info:
                return False, "Repository not found"
            
            github_user = repo_info.get("github_user", "Dadudekc")
            repo_full = f"{github_user}/{repo_name}"
            
            # Generate PR title if not provided
            if not title:
                title = f"Merge {branch} into {base_branch}"
            
            # Create PR via gh CLI
            cmd = [
                "gh", "pr", "create",
                "--repo", repo_full,
                "--head", branch,
                "--base", base_branch,
                "--title", title
            ]
            
            if body:
                cmd.extend(["--body", body])
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=TimeoutConstants.HTTP_DEFAULT
            )
            
            if result.returncode == 0:
                pr_url = result.stdout.strip()
                logger.info(f"✅ PR created: {pr_url}")
                return True, pr_url
            else:
                error_msg = result.stderr or result.stdout
                
                # Check for rate limit
                if "rate limit" in error_msg.lower() or "429" in error_msg:
                    logger.warning(f"⚠️ Rate limit: Deferring PR creation {repo_name}/{branch}")
                    self.deferred_queue.enqueue_push(
                        repo=repo_name,
                        branch=branch,
                        reason="rate_limit_pr",
                        metadata={
                            "pr_title": title,
                            "pr_body": body,
                            "base_branch": base_branch,
                            "action": "create_pr"
                        }
                    )
                    self.sandbox_mode.enable("rate_limit")
                    return False, "Rate limit - deferred"
                
                # Defer on any error
                logger.warning(f"⚠️ PR creation failed: Deferring {repo_name}/{branch}")
                self.deferred_queue.enqueue_push(
                    repo=repo_name,
                    branch=branch,
                    reason="pr_failed",
                    metadata={
                        "pr_title": title,
                        "pr_body": body,
                        "base_branch": base_branch,
                        "action": "create_pr"
                    }
                )
                return False, error_msg
                
        except Exception as e:
            logger.error(f"❌ PR creation error: {e}")
            self.deferred_queue.enqueue_push(
                repo=repo_name,
                branch=branch,
                reason=f"error: {str(e)}",
                metadata={
                    "pr_title": title,
                    "pr_body": body,
                    "base_branch": base_branch,
                    "action": "create_pr"
                }
            )
            return False, str(e)



