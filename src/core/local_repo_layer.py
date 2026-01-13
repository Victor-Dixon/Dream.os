#!/usr/bin/env python3
"""
Local Repo Layer - GitHub Bypass System

<!-- SSOT Domain: infrastructure -->

========================================

Creates a local-first repository system where GitHub is optional.
Agents work on local repos, GitHub only mirrors the result.

V2 Compliance: SOLID principles, repository pattern
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2025-11-28
Priority: CRITICAL - Bottleneck Breaking
"""

import json
import logging
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple

from .config.timeout_constants import TimeoutConstants

logger = logging.getLogger(__name__)


class LocalRepoManager:
    """Manages local repository clones independent of GitHub."""
    
    def __init__(self, base_path: Optional[Path] = None):
        """
        Initialize local repo manager with self-healing capabilities.
        
        Args:
            base_path: Base directory for local repos (default: D:/Temp)
        """
        if base_path is None:
            # Default to D:/Temp directly (simplified per directive)
            base_path = Path("D:/Temp")
        
        self.base_path = Path(base_path)
        
        # Self-healing: Try to create directory, handle failures gracefully
        try:
            self.base_path.mkdir(parents=True, exist_ok=True)
        except PermissionError as e:
            logger.warning(f"⚠️ Permission denied creating {self.base_path}, using D:/Temp fallback")
            # Fallback to D:/Temp directly
            self.base_path = Path("D:/Temp")
            self.base_path.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            logger.error(f"❌ Failed to create base path: {e}, using D:/Temp fallback")
            # Fallback to D:/Temp directly
            self.base_path = Path("D:/Temp")
            self.base_path.mkdir(parents=True, exist_ok=True)
        
        # Metadata file for tracking repos
        self.metadata_file = self.base_path / ".local_repos.json"
        self.repos: Dict[str, Dict[str, Any]] = self._load_metadata()
        
        # If metadata was cleaned, save the cleaned version
        if not self.metadata_file.exists() and len(self.repos) == 0:
            # Create empty metadata file
            self._save_metadata()
        
        # Log only at debug level to prevent stalls in tests
        logger.debug(f"✅ Local Repo Manager initialized: {self.base_path}")
    
    def _load_metadata(self) -> Dict[str, Dict[str, Any]]:
        """
        Load repository metadata from JSON file with self-healing.
        
        Handles:
        - Malformed JSON (backs up and recreates)
        - Missing file (creates empty)
        - Permission errors (uses fallback)
        - Invalid structure (validates and repairs)
        """
        if not self.metadata_file.exists():
            # File doesn't exist - return empty, will be created on first save
            return {}
        
        try:
            with open(self.metadata_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Self-healing: Validate structure
            if not isinstance(data, dict):
                logger.warning(f"⚠️ Invalid metadata structure, resetting")
                self._backup_metadata()
                return {}
            
            # Validate each repo entry has required fields
            validated_data = {}
            for repo_name, repo_info in data.items():
                if isinstance(repo_info, dict) and "local_path" in repo_info:
                    # Verify path still exists, remove if not
                    local_path = Path(repo_info.get("local_path", ""))
                    if local_path.exists():
                        validated_data[repo_name] = repo_info
                    else:
                        logger.debug(f"⚠️ Removing stale repo entry: {repo_name} (path doesn't exist)")
                else:
                    logger.debug(f"⚠️ Invalid repo entry format: {repo_name}")
            
            # If we removed entries, save the cleaned version
            if len(validated_data) != len(data):
                logger.info(f"🧹 Cleaned metadata: {len(data)} → {len(validated_data)} repos")
                # Save will happen after self.repos is set in __init__
            
            return validated_data
            
        except json.JSONDecodeError as e:
            logger.warning(f"⚠️ Malformed JSON in metadata file: {e}")
            self._backup_metadata()
            return {}
        except PermissionError as e:
            logger.warning(f"⚠️ Permission denied reading metadata: {e}")
            return {}
        except Exception as e:
            logger.warning(f"⚠️ Failed to load metadata: {e}")
            self._backup_metadata()
            return {}
    
    def _backup_metadata(self):
        """Backup corrupted metadata file before resetting."""
        if self.metadata_file.exists():
            try:
                backup_file = self.metadata_file.with_suffix('.json.bak')
                import shutil
                shutil.copy2(self.metadata_file, backup_file)
                logger.debug(f"📦 Backed up metadata to {backup_file}")
            except Exception as e:
                logger.debug(f"Could not backup metadata: {e}")
    
    def _save_metadata(self):
        """
        Save repository metadata to JSON file with self-healing.
        
        Handles:
        - Permission errors (logs warning, continues)
        - Directory creation failures
        - Write failures (retries with backup)
        """
        try:
            # Ensure directory exists
            self.metadata_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Write to temporary file first, then rename (atomic write)
            temp_file = self.metadata_file.with_suffix('.json.tmp')
            with open(temp_file, 'w', encoding='utf-8') as f:
                json.dump(self.repos, f, indent=2, ensure_ascii=False)
            
            # Atomic rename
            if temp_file.exists():
                if self.metadata_file.exists():
                    self.metadata_file.unlink()
                temp_file.rename(self.metadata_file)
                
        except PermissionError as e:
            logger.warning(f"⚠️ Permission denied saving metadata: {e}")
        except Exception as e:
            logger.error(f"❌ Failed to save metadata: {e}")
            # Try to clean up temp file
            try:
                temp_file = self.metadata_file.with_suffix('.json.tmp')
                if temp_file.exists():
                    temp_file.unlink()
            except:
                pass
    
    def clone_from_github(
        self,
        repo_name: str,
        github_url: Optional[str] = None,
        github_user: str = "Dadudekc",
        branch: str = "main"
    ) -> Tuple[bool, Optional[Path]]:
        """
        Clone repository from GitHub to local storage.
        
        Args:
            repo_name: Name of repository
            github_url: Full GitHub URL (optional, will construct if None)
            github_user: GitHub username (default: Dadudekc)
            branch: Branch to checkout (default: main)
        
        Returns:
            Tuple of (success, repo_path)
        """
        repo_path = self.base_path / repo_name
        
        # Check if already cloned
        if repo_path.exists() and repo_name in self.repos:
            logger.info(f"📦 {repo_name}: Already cloned locally")
            return True, repo_path
        
        # Construct URL if not provided
        if github_url is None:
            github_url = f"https://github.com/{github_user}/{repo_name}.git"
        
        try:
            logger.info(f"📥 Cloning {repo_name} from GitHub...")
            result = subprocess.run(
                ["git", "clone", "--depth", "1", "-b", branch, github_url, str(repo_path)],
                capture_output=True,
                text=True,
                timeout=TimeoutConstants.HTTP_LONG
            )
            
            if result.returncode != 0:
                logger.error(f"❌ Clone failed: {result.stderr}")
                return False, None
            
            # Register in metadata
            self.repos[repo_name] = {
                "github_url": github_url,
                "github_user": github_user,
                "local_path": str(repo_path),
                "branch": branch,
                "cloned_at": datetime.now().isoformat(),
                "last_synced": datetime.now().isoformat(),
                "status": "active"
            }
            self._save_metadata()
            
            logger.info(f"✅ {repo_name}: Cloned to {repo_path}")
            return True, repo_path
            
        except subprocess.TimeoutExpired:
            logger.error(f"❌ Clone timeout for {repo_name}")
            return False, None
        except Exception as e:
            logger.error(f"❌ Clone error for {repo_name}: {e}")
            return False, None
    
    def clone_locally(
        self,
        repo_name: str,
        source_path: Path,
        branch: str = "main"
    ) -> Tuple[bool, Optional[Path]]:
        """
        Clone from another local repository.
        
        Args:
            repo_name: Name for new local clone
            source_path: Path to source repository
            branch: Branch to checkout
        
        Returns:
            Tuple of (success, repo_path)
        """
        repo_path = self.base_path / repo_name
        
        if repo_path.exists():
            logger.warning(f"⚠️ {repo_name}: Already exists, skipping")
            return True, repo_path
        
        try:
            logger.info(f"📦 Cloning {repo_name} from local source...")
            result = subprocess.run(
                ["git", "clone", str(source_path), str(repo_path)],
                capture_output=True,
                text=True,
                timeout=TimeoutConstants.HTTP_LONG
            )
            
            if result.returncode != 0:
                logger.error(f"❌ Local clone failed: {result.stderr}")
                return False, None
            
            # Checkout branch
            subprocess.run(
                ["git", "checkout", branch],
                cwd=repo_path,
                capture_output=True,
                text=True
            )
            
            # Register in metadata
            self.repos[repo_name] = {
                "source_path": str(source_path),
                "local_path": str(repo_path),
                "branch": branch,
                "cloned_at": datetime.now().isoformat(),
                "status": "local_only"
            }
            self._save_metadata()
            
            logger.info(f"✅ {repo_name}: Local clone created")
            return True, repo_path
            
        except Exception as e:
            logger.error(f"❌ Local clone error: {e}")
            return False, None
    
    def get_repo_path(self, repo_name: str) -> Optional[Path]:
        """Get local path for repository."""
        if repo_name in self.repos:
            path = Path(self.repos[repo_name]["local_path"])
            if path.exists():
                return path
        return None
    
    def create_branch(self, repo_name: str, branch_name: str) -> bool:
        """Create a new branch in local repository."""
        repo_path = self.get_repo_path(repo_name)
        if not repo_path:
            logger.error(f"❌ Repository {repo_name} not found")
            return False
        
        try:
            result = subprocess.run(
                ["git", "checkout", "-b", branch_name],
                cwd=repo_path,
                capture_output=True,
                text=True,
                timeout=TimeoutConstants.HTTP_DEFAULT
            )
            
            if result.returncode != 0:
                logger.error(f"❌ Branch creation failed: {result.stderr}")
                return False
            
            logger.info(f"✅ Branch {branch_name} created in {repo_name}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Branch creation error: {e}")
            return False
    
    def merge_branch(
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
        repo_path = self.get_repo_path(repo_name)
        if not repo_path:
            return False, "Repository not found"
        
        try:
            # Checkout target branch
            subprocess.run(
                ["git", "checkout", target_branch],
                cwd=repo_path,
                capture_output=True,
                text=True,
                timeout=TimeoutConstants.HTTP_DEFAULT
            )
            
            # Merge source branch
            result = subprocess.run(
                ["git", "merge", "--no-commit", "--no-ff", source_branch],
                cwd=repo_path,
                capture_output=True,
                text=True,
                timeout=TimeoutConstants.HTTP_MEDIUM
            )
            
            if result.returncode != 0:
                # Check for conflicts
                if "CONFLICT" in result.stdout or "CONFLICT" in result.stderr:
                    logger.warning(f"⚠️ Merge conflict detected: {source_branch} → {target_branch}")
                    return False, "Merge conflict detected"
                
                logger.error(f"❌ Merge failed: {result.stderr}")
                return False, result.stderr
            
            logger.info(f"✅ Merged {source_branch} → {target_branch} in {repo_name}")
            return True, None
            
        except Exception as e:
            logger.error(f"❌ Merge error: {e}")
            return False, str(e)
    
    def generate_patch(
        self,
        repo_name: str,
        branch: str,
        output_path: Optional[Path] = None
    ) -> Optional[Path]:
        """
        Generate patch file for branch.
        
        Args:
            repo_name: Name of repository
            branch: Branch to generate patch for
            output_path: Output path for patch file
        
        Returns:
            Path to patch file, or None if failed
        """
        repo_path = self.get_repo_path(repo_name)
        if not repo_path:
            return None
        
        if output_path is None:
            patch_dir = self.base_path.parent / "patches"
            patch_dir.mkdir(parents=True, exist_ok=True)
            timestamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
            output_path = patch_dir / f"{repo_name}-{branch}-{timestamp}.patch"
        
        try:
            # Get base branch (main or master)
            result = subprocess.run(
                ["git", "branch", "--show-current"],
                cwd=repo_path,
                capture_output=True,
                text=True
            )
            base_branch = result.stdout.strip() if result.returncode == 0 else "main"
            
            # Generate patch
            result = subprocess.run(
                ["git", "format-patch", "-1", branch, "--stdout"],
                cwd=repo_path,
                capture_output=True,
                text=True,
                timeout=TimeoutConstants.HTTP_DEFAULT
            )
            
            if result.returncode != 0:
                logger.error(f"❌ Patch generation failed: {result.stderr}")
                return None
            
            # Write patch file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(result.stdout)
            
            logger.info(f"✅ Patch generated: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"❌ Patch generation error: {e}")
            return None
    
    def list_repos(self) -> List[str]:
        """List all locally managed repositories."""
        return list(self.repos.keys())
    
    def get_repo_status(self, repo_name: str) -> Optional[Dict[str, Any]]:
        """Get status information for repository."""
        return self.repos.get(repo_name)
    
    def remove_repo(self, repo_name: str) -> bool:
        """Remove repository from local storage."""
        if repo_name not in self.repos:
            return False
        
        repo_path = self.get_repo_path(repo_name)
        if repo_path and repo_path.exists():
            try:
                shutil.rmtree(repo_path)
                logger.info(f"✅ Removed repository: {repo_name}")
            except Exception as e:
                logger.error(f"❌ Failed to remove repository: {e}")
                return False
        
        del self.repos[repo_name]
        self._save_metadata()
        return True


# Global instance
_local_repo_manager: Optional[LocalRepoManager] = None


def get_local_repo_manager(base_path: Optional[Path] = None) -> LocalRepoManager:
    """Get global LocalRepoManager instance."""
    global _local_repo_manager
    if _local_repo_manager is None:
        _local_repo_manager = LocalRepoManager(base_path)
    return _local_repo_manager

