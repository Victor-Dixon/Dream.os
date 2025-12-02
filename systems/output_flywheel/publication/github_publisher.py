"""
GitHub Publisher - Phase 3
==========================

Automates GitHub publication of artifacts.

Author: Agent-7 (Web Development Specialist)
V2 Compliant: <300 lines
"""

import os
import subprocess
from pathlib import Path
from typing import Optional, Dict, Any
import json


class GitHubPublisher:
    """Publishes artifacts to GitHub."""
    
    def __init__(
        self,
        repo_path: Optional[Path] = None,
        branch: str = "main",
        auto_commit: bool = False,
        auto_push: bool = False
    ):
        """Initialize GitHub publisher."""
        if repo_path is None:
            repo_path = Path.cwd()
        self.repo_path = Path(repo_path)
        self.branch = branch
        self.auto_commit = auto_commit
        self.auto_push = auto_push
    
    def _run_git_command(self, command: list, cwd: Optional[Path] = None) -> tuple[bool, str]:
        """Run git command."""
        if cwd is None:
            cwd = self.repo_path
        
        try:
            result = subprocess.run(
                ["git"] + command,
                cwd=cwd,
                capture_output=True,
                text=True,
                check=False
            )
            return result.returncode == 0, result.stdout + result.stderr
        except Exception as e:
            return False, str(e)
    
    def _is_git_repo(self) -> bool:
        """Check if path is a git repository."""
        git_dir = self.repo_path / ".git"
        return git_dir.exists()
    
    def update_readme(self, readme_path: str, commit_message: Optional[str] = None) -> Dict[str, Any]:
        """Update README.md in repository."""
        if not self._is_git_repo():
            return {
                "success": False,
                "error": "Not a git repository"
            }
        
        readme_file = self.repo_path / readme_path
        if not readme_file.exists():
            return {
                "success": False,
                "error": f"README file not found: {readme_path}"
            }
        
        if not self.auto_commit:
            return {
                "success": True,
                "status": "ready",
                "message": "README updated (commit disabled)"
            }
        
        # Stage file
        success, output = self._run_git_command(["add", str(readme_file)])
        if not success:
            return {
                "success": False,
                "error": f"Failed to stage file: {output}"
            }
        
        # Commit
        if commit_message is None:
            commit_message = "docs: Update README from Output Flywheel"
        
        success, output = self._run_git_command(
            ["commit", "-m", commit_message]
        )
        if not success:
            return {
                "success": False,
                "error": f"Failed to commit: {output}"
            }
        
        # Push if enabled
        if self.auto_push:
            success, output = self._run_git_command(["push", "origin", self.branch])
            if not success:
                return {
                    "success": False,
                    "error": f"Failed to push: {output}"
                }
        
        return {
            "success": True,
            "status": "published" if self.auto_push else "committed",
            "message": "README updated successfully"
        }
    
    def update_repo_description(
        self,
        description: str,
        commit_message: Optional[str] = None
    ) -> Dict[str, Any]:
        """Update repository description via GitHub API."""
        # Note: This requires GitHub API token
        # For now, return ready status
        return {
            "success": True,
            "status": "ready",
            "message": "Repository description update ready (API integration needed)"
        }
    
    def publish_artifact(
        self,
        artifact_type: str,
        artifact_path: str,
        target_path: Optional[str] = None,
        commit_message: Optional[str] = None
    ) -> Dict[str, Any]:
        """Publish artifact to GitHub."""
        if not self._is_git_repo():
            return {
                "success": False,
                "error": "Not a git repository"
            }
        
        source_file = Path(artifact_path)
        if not source_file.exists():
            return {
                "success": False,
                "error": f"Artifact file not found: {artifact_path}"
            }
        
        # Determine target path
        if target_path is None:
            if artifact_type == "readme":
                target_path = "README.md"
            elif artifact_type == "blog_post":
                target_path = f"docs/blog/{source_file.name}"
            elif artifact_type == "social_post":
                target_path = f"docs/social/{source_file.name}"
            else:
                target_path = f"docs/{source_file.name}"
        
        target_file = self.repo_path / target_path
        target_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Copy file
        import shutil
        shutil.copy2(source_file, target_file)
        
        if not self.auto_commit:
            return {
                "success": True,
                "status": "ready",
                "message": f"Artifact copied to {target_path} (commit disabled)"
            }
        
        # Stage file
        success, output = self._run_git_command(["add", str(target_file)])
        if not success:
            return {
                "success": False,
                "error": f"Failed to stage file: {output}"
            }
        
        # Commit
        if commit_message is None:
            commit_message = f"docs: Add {artifact_type} from Output Flywheel"
        
        success, output = self._run_git_command(
            ["commit", "-m", commit_message]
        )
        if not success:
            return {
                "success": False,
                "error": f"Failed to commit: {output}"
            }
        
        # Push if enabled
        if self.auto_push:
            success, output = self._run_git_command(["push", "origin", self.branch])
            if not success:
                return {
                    "success": False,
                    "error": f"Failed to push: {output}"
                }
        
        return {
            "success": True,
            "status": "published" if self.auto_push else "committed",
            "message": f"Artifact published to {target_path}",
            "target_path": target_path
        }

