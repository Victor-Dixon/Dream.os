#!/usr/bin/env python3
"""
Synthetic GitHub Client Module
==============================

<!-- SSOT Domain: integration -->

Extracted from synthetic_github.py for V2 compliance.
Main GitHub client interface with local/remote routing logic.

V2 Compliance | Author: Agent-1 | Date: 2025-12-14
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional, Tuple

from ..local_repo_layer import get_local_repo_manager
from ..deferred_push_queue import get_deferred_push_queue
from .sandbox_manager import GitHubSandboxMode
from .local_router import LocalRouter
from .remote_router import RemoteRouter

logger = logging.getLogger(__name__)


class SyntheticGitHub:
    """
    Synthetic GitHub wrapper - routes calls to local storage or real GitHub.
    
    Strategy:
    - 70% of operations use local storage
    - 30% of operations hit real GitHub
    - All failures fall back to local mode
    """
    
    def __init__(self):
        """Initialize synthetic GitHub wrapper."""
        self.local_repo_manager = get_local_repo_manager()
        self.deferred_queue = get_deferred_push_queue()
        self.sandbox_mode = GitHubSandboxMode()
        
        # Initialize routers
        self.local_router = LocalRouter(
            self.local_repo_manager,
            self.sandbox_mode
        )
        self.remote_router = RemoteRouter(
            self.local_repo_manager,
            self.deferred_queue,
            self.sandbox_mode
        )
        
        logger.info("✅ Synthetic GitHub initialized")
    
    def get_repo(
        self,
        repo_name: str,
        github_user: str = "Dadudekc",
        branch: str = "main"
    ) -> Tuple[bool, Optional[Path], bool]:
        """
        Get repository (local-first, GitHub fallback).
        
        Args:
            repo_name: Name of repository
            github_user: GitHub username
            branch: Branch to checkout
        
        Returns:
            Tuple of (success, repo_path, was_local)
        """
        # Try local first
        local_path = self.local_repo_manager.get_repo_path(repo_name)
        if local_path:
            logger.debug(f"📦 Using local repo: {repo_name}")
            return True, local_path, True
        
        # Check sandbox mode
        if self.sandbox_mode.is_enabled():
            logger.warning(f"⚠️ Sandbox mode: Cannot fetch {repo_name} from GitHub")
            return False, None, False
        
        # Try GitHub clone
        try:
            success, repo_path = self.local_repo_manager.clone_from_github(
                repo_name, github_user=github_user, branch=branch
            )
            
            if success:
                logger.info(f"✅ Cloned from GitHub: {repo_name}")
                return True, repo_path, False
            else:
                logger.warning(f"⚠️ GitHub clone failed, enabling sandbox mode")
                self.sandbox_mode.enable("github_clone_failed")
                return False, None, False
                
        except Exception as e:
            logger.error(f"❌ Error cloning from GitHub: {e}")
            self.sandbox_mode.enable(f"error: {str(e)}")
            return False, None, False
    
    def create_branch(
        self,
        repo_name: str,
        branch_name: str,
        source_branch: str = "main"
    ) -> bool:
        """
        Create branch (local-only, GitHub sync deferred).
        
        Args:
            repo_name: Name of repository
            branch_name: Name of new branch
            source_branch: Source branch to branch from
        
        Returns:
            True if successful
        """
        # Get local repo first (if not exists, try to get from GitHub)
        repo_path = self.local_repo_manager.get_repo_path(repo_name)
        if not repo_path:
            success, repo_path, _ = self.get_repo(repo_name)
            if not success:
                return False
        
        return self.local_router.create_branch(repo_name, branch_name, source_branch)
    
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
        return self.remote_router.push_branch(repo_name, branch, force)
    
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
        return self.remote_router.create_pr(
            repo_name, branch, base_branch, title, body
        )
    
    def get_file(
        self,
        repo_name: str,
        file_path: str,
        branch: str = "main"
    ) -> Tuple[bool, Optional[str]]:
        """
        Get file content (local-first).
        
        Args:
            repo_name: Name of repository
            file_path: Path to file
            branch: Branch to read from
        
        Returns:
            Tuple of (success, file_content)
        """
        # Get local repo first (if not exists, try to get from GitHub)
        repo_path = self.local_repo_manager.get_repo_path(repo_name)
        if not repo_path:
            success, repo_path, _ = self.get_repo(repo_name, branch=branch)
            if not success:
                return False, None
        
        return self.local_router.get_file(repo_name, file_path, branch)
    
    def merge_branches(
        self,
        repo_name: str,
        source_branch: str,
        target_branch: str = "main"
    ) -> Tuple[bool, Optional[str]]:
        """
        Merge branches locally.
        
        Args:
            repo_name: Name of repository
            source_branch: Branch to merge from
            target_branch: Branch to merge into
        
        Returns:
            Tuple of (success, conflict_message)
        """
        return self.local_router.merge_branches(
            repo_name, source_branch, target_branch
        )
    
    def is_sandbox_mode(self) -> bool:
        """Check if sandbox mode is enabled."""
        return self.sandbox_mode.is_enabled()
