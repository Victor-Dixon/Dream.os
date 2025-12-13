#!/usr/bin/env python3
"""
Local Router Module - Synthetic GitHub
======================================

<!-- SSOT Domain: integration -->

Extracted from synthetic_github.py for V2 compliance.
Handles local storage routing and local-first strategy implementation.

V2 Compliance | Author: Agent-1 | Date: 2025-12-14
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional, Tuple

from ..local_repo_layer import get_local_repo_manager
from .sandbox_manager import GitHubSandboxMode

logger = logging.getLogger(__name__)


class LocalRouter:
    """Handles local storage routing for synthetic GitHub operations."""
    
    def __init__(
        self,
        local_repo_manager,
        sandbox_mode: GitHubSandboxMode
    ):
        """
        Initialize local router.
        
        Args:
            local_repo_manager: Local repository manager instance
            sandbox_mode: Sandbox mode manager instance
        """
        self.local_repo_manager = local_repo_manager
        self.sandbox_mode = sandbox_mode
    
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
            source_branch: Source branch to branch from (accepted for API consistency,
                         but underlying local_repo_manager.create_branch() doesn't use it)
        
        Returns:
            True if successful
        """
        # Get local repo
        repo_path = self.local_repo_manager.get_repo_path(repo_name)
        if not repo_path:
            return False
        
        # Create branch locally
        # Note: local_repo_manager.create_branch() only accepts repo_name and branch_name
        # source_branch parameter is accepted for API consistency but not used here
        success = self.local_repo_manager.create_branch(repo_name, branch_name)
        
        if success:
            logger.info(f"✅ Branch created locally: {repo_name}/{branch_name}")
            # Defer GitHub sync if not in sandbox mode
            if not self.sandbox_mode.is_enabled():
                self._defer_branch_sync(repo_name, branch_name, source_branch)
        
        return success
    
    def _defer_branch_sync(self, repo_name: str, branch_name: str, source_branch: str):
        """Defer branch sync to GitHub."""
        # Branch creation will be synced when pushed
        logger.debug(f"📝 Branch sync deferred: {repo_name}/{branch_name}")
    
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
        repo_path = self.local_repo_manager.get_repo_path(repo_name)
        if not repo_path:
            return False, None
        
        file_full_path = repo_path / file_path
        if file_full_path.exists():
            try:
                content = file_full_path.read_text(encoding='utf-8')
                return True, content
            except Exception as e:
                logger.error(f"❌ Failed to read file: {e}")
                return False, None
        
        return False, None
    
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
        
        Note: Method name is plural (merge_branches) for API consistency,
        but delegates to local_repo_manager.merge_branch() (singular).
        """
        return self.local_repo_manager.merge_branch(
            repo_name, source_branch, target_branch
        )

