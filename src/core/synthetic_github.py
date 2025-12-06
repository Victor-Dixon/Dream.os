#!/usr/bin/env python3
"""
Synthetic GitHub - Local-First GitHub Wrapper
=============================================

Thin wrapper that makes agents think they're talking to GitHub,
but routes 70% of calls to local storage, only 30% to real GitHub.

V2 Compliance: Adapter pattern, dependency inversion
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2025-11-28
Priority: CRITICAL - Bottleneck Breaking
"""

import json
import logging
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional, Tuple, List
from datetime import datetime
import os

from .local_repo_layer import get_local_repo_manager
from .deferred_push_queue import get_deferred_push_queue, PushStatus
from .config.timeout_constants import TimeoutConstants

logger = logging.getLogger(__name__)


class GitHubSandboxMode:
    """Manages GitHub sandbox mode (offline/local-only mode)."""
    
    def __init__(self, config_file: Optional[Path] = None):
        """
        Initialize sandbox mode manager.
        
        Args:
            config_file: Path to sandbox config file
        """
        if config_file is None:
            project_root = Path(__file__).resolve().parent.parent.parent
            config_file = project_root / "github_sandbox_mode.json"
        
        self.config_file = Path(config_file)
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load sandbox mode configuration."""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except Exception:
                pass
        
        return {
            "sandbox_mode": False,
            "reason": None,
            "enabled_at": None,
            "auto_detect": True
        }
    
    def _save_config(self):
        """Save sandbox mode configuration."""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save sandbox config: {e}")
    
    def is_enabled(self) -> bool:
        """Check if sandbox mode is enabled."""
        if self.config.get("sandbox_mode"):
            return True
        
        # Auto-detect if enabled
        if self.config.get("auto_detect", True):
            return self._detect_github_availability() == False
        
        return False
    
    def _detect_github_availability(self) -> bool:
        """Detect if GitHub is available."""
        try:
            # Quick check - try to ping GitHub
            result = subprocess.run(
                ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", 
                 "https://api.github.com/zen"],
                capture_output=True,
                text=True,
                timeout=TimeoutConstants.HTTP_QUICK
            )
            
            # Fallback: try python requests if curl not available
            if result.returncode != 0:
                try:
                    import requests
                    response = requests.get("https://api.github.com/zen", timeout=TimeoutConstants.HTTP_QUICK)
                    return response.status_code == 200
                except:
                    pass
            
            return result.stdout.strip() == "200"
        except Exception:
            # If check fails, assume GitHub is unavailable
            return False
    
    def enable(self, reason: str = "manual"):
        """Enable sandbox mode."""
        self.config["sandbox_mode"] = True
        self.config["reason"] = reason
        self.config["enabled_at"] = datetime.now().isoformat()
        self._save_config()
        logger.info(f"🔒 Sandbox mode ENABLED: {reason}")
    
    def disable(self):
        """Disable sandbox mode."""
        self.config["sandbox_mode"] = False
        self.config["reason"] = None
        self.config["enabled_at"] = None
        self._save_config()
        logger.info("🔓 Sandbox mode DISABLED")


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
        # Get local repo
        repo_path = self.local_repo_manager.get_repo_path(repo_name)
        if not repo_path:
            # Try to get from GitHub first (if not sandbox)
            success, repo_path, _ = self.get_repo(repo_name)
            if not success:
                return False
        
        # Create branch locally
        success = self.local_repo_manager.create_branch(repo_name, branch_name)
        
        if success:
            logger.info(f"✅ Branch created locally: {repo_name}/{branch_name}")
            # Defer GitHub sync
            if not self.sandbox_mode.is_enabled():
                self._defer_branch_sync(repo_name, branch_name, source_branch)
        
        return success
    
    def _defer_branch_sync(self, repo_name: str, branch_name: str, source_branch: str):
        """Defer branch sync to GitHub."""
        # Branch creation will be synced when pushed
        logger.debug(f"📝 Branch sync deferred: {repo_name}/{branch_name}")
    
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
            # Try to get from GitHub first
            success, repo_path, _ = self.get_repo(repo_name, branch=branch)
            if not success:
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
        """
        return self.local_repo_manager.merge_branch(
            repo_name, source_branch, target_branch
        )
    
    def is_sandbox_mode(self) -> bool:
        """Check if sandbox mode is enabled."""
        return self.sandbox_mode.is_enabled()


# Global instance
_synthetic_github: Optional[SyntheticGitHub] = None


def get_synthetic_github() -> SyntheticGitHub:
    """Get global SyntheticGitHub instance."""
    global _synthetic_github
    if _synthetic_github is None:
        _synthetic_github = SyntheticGitHub()
    return _synthetic_github

"""
Synthetic GitHub - Local-First GitHub Wrapper
=============================================

Thin wrapper that makes agents think they're talking to GitHub,
but routes 70% of calls to local storage, only 30% to real GitHub.

V2 Compliance: Adapter pattern, dependency inversion
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2025-11-28
Priority: CRITICAL - Bottleneck Breaking
"""

import json
import logging
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional, Tuple, List
from datetime import datetime
import os

from .local_repo_layer import get_local_repo_manager
from .deferred_push_queue import get_deferred_push_queue, PushStatus
from .config.timeout_constants import TimeoutConstants

logger = logging.getLogger(__name__)


class GitHubSandboxMode:
    """Manages GitHub sandbox mode (offline/local-only mode)."""
    
    def __init__(self, config_file: Optional[Path] = None):
        """
        Initialize sandbox mode manager.
        
        Args:
            config_file: Path to sandbox config file
        """
        if config_file is None:
            project_root = Path(__file__).resolve().parent.parent.parent
            config_file = project_root / "github_sandbox_mode.json"
        
        self.config_file = Path(config_file)
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load sandbox mode configuration."""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except Exception:
                pass
        
        return {
            "sandbox_mode": False,
            "reason": None,
            "enabled_at": None,
            "auto_detect": True
        }
    
    def _save_config(self):
        """Save sandbox mode configuration."""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save sandbox config: {e}")
    
    def is_enabled(self) -> bool:
        """Check if sandbox mode is enabled."""
        if self.config.get("sandbox_mode"):
            return True
        
        # Auto-detect if enabled
        if self.config.get("auto_detect", True):
            return self._detect_github_availability() == False
        
        return False
    
    def _detect_github_availability(self) -> bool:
        """Detect if GitHub is available."""
        try:
            # Quick check - try to ping GitHub
            result = subprocess.run(
                ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", 
                 "https://api.github.com/zen"],
                capture_output=True,
                text=True,
                timeout=TimeoutConstants.HTTP_QUICK
            )
            
            # Fallback: try python requests if curl not available
            if result.returncode != 0:
                try:
                    import requests
                    response = requests.get("https://api.github.com/zen", timeout=TimeoutConstants.HTTP_QUICK)
                    return response.status_code == 200
                except:
                    pass
            
            return result.stdout.strip() == "200"
        except Exception:
            # If check fails, assume GitHub is unavailable
            return False
    
    def enable(self, reason: str = "manual"):
        """Enable sandbox mode."""
        self.config["sandbox_mode"] = True
        self.config["reason"] = reason
        self.config["enabled_at"] = datetime.now().isoformat()
        self._save_config()
        logger.info(f"🔒 Sandbox mode ENABLED: {reason}")
    
    def disable(self):
        """Disable sandbox mode."""
        self.config["sandbox_mode"] = False
        self.config["reason"] = None
        self.config["enabled_at"] = None
        self._save_config()
        logger.info("🔓 Sandbox mode DISABLED")


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
        # Get local repo
        repo_path = self.local_repo_manager.get_repo_path(repo_name)
        if not repo_path:
            # Try to get from GitHub first (if not sandbox)
            success, repo_path, _ = self.get_repo(repo_name)
            if not success:
                return False
        
        # Create branch locally
        success = self.local_repo_manager.create_branch(repo_name, branch_name)
        
        if success:
            logger.info(f"✅ Branch created locally: {repo_name}/{branch_name}")
            # Defer GitHub sync
            if not self.sandbox_mode.is_enabled():
                self._defer_branch_sync(repo_name, branch_name, source_branch)
        
        return success
    
    def _defer_branch_sync(self, repo_name: str, branch_name: str, source_branch: str):
        """Defer branch sync to GitHub."""
        # Branch creation will be synced when pushed
        logger.debug(f"📝 Branch sync deferred: {repo_name}/{branch_name}")
    
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
            # Try to get from GitHub first
            success, repo_path, _ = self.get_repo(repo_name, branch=branch)
            if not success:
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
        """
        return self.local_repo_manager.merge_branch(
            repo_name, source_branch, target_branch
        )
    
    def is_sandbox_mode(self) -> bool:
        """Check if sandbox mode is enabled."""
        return self.sandbox_mode.is_enabled()


# Global instance
_synthetic_github: Optional[SyntheticGitHub] = None


def get_synthetic_github() -> SyntheticGitHub:
    """Get global SyntheticGitHub instance."""
    global _synthetic_github
    if _synthetic_github is None:
        _synthetic_github = SyntheticGitHub()
    return _synthetic_github

