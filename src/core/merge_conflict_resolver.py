#!/usr/bin/env python3
"""
Local Merge Conflict Resolver

<!-- SSOT Domain: infrastructure -->

==

Deterministic merge conflict resolution for multi-agent consolidation.
Resolves conflicts locally before attempting GitHub operations.

V2 Compliance: SOLID principles, strategy pattern
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2025-11-28
Priority: CRITICAL - Bottleneck Breaking
"""

import logging
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
import re

from src.core.config.timeout_constants import TimeoutConstants

logger = logging.getLogger(__name__)


class MergeConflictResolver:
    """Resolves merge conflicts in local repositories."""
    
    def __init__(self):
        """Initialize conflict resolver."""
        logger.info("✅ Merge Conflict Resolver initialized")
    
    def detect_conflicts(
        self,
        repo_path: Path,
        source_branch: str,
        target_branch: str = "main"
    ) -> Tuple[bool, List[str]]:
        """
        Detect merge conflicts before attempting merge.
        
        Args:
            repo_path: Path to repository
            source_branch: Source branch
            target_branch: Target branch
        
        Returns:
            Tuple of (has_conflicts, conflict_files)
        """
        try:
            # Checkout target branch
            subprocess.run(
                ["git", "checkout", target_branch],
                cwd=repo_path,
                capture_output=True,
                text=True,
                timeout=TimeoutConstants.HTTP_DEFAULT
            )
            
            # Try merge (dry run)
            result = subprocess.run(
                ["git", "merge", "--no-commit", "--no-ff", source_branch],
                cwd=repo_path,
                capture_output=True,
                text=True,
                timeout=TimeoutConstants.HTTP_MEDIUM
            )
            
            # Check for conflict markers
            conflict_files = []
            if result.returncode != 0:
                # Parse conflict output
                conflict_pattern = re.compile(r"CONFLICT \(.*?\): Merge conflict in (.+)")
                matches = conflict_pattern.findall(result.stdout + result.stderr)
                conflict_files = list(set(matches))
            
            # Abort merge
            subprocess.run(
                ["git", "merge", "--abort"],
                cwd=repo_path,
                capture_output=True,
                text=True,
                timeout=TimeoutConstants.HTTP_DEFAULT
            )
            
            has_conflicts = len(conflict_files) > 0
            return has_conflicts, conflict_files
            
        except Exception as e:
            logger.error(f"❌ Conflict detection error: {e}")
            return True, []  # Assume conflicts if detection fails
    
    def resolve_conflicts_auto(
        self,
        repo_path: Path,
        conflict_files: List[str],
        strategy: str = "theirs"
    ) -> bool:
        """
        Automatically resolve conflicts using strategy.
        
        Args:
            repo_path: Path to repository
            conflict_files: List of conflicted files
            strategy: Resolution strategy (ours, theirs, union)
        
        Returns:
            True if resolution successful
        """
        try:
            if strategy == "theirs":
                # Use source branch version (theirs)
                for file_path in conflict_files:
                    result = subprocess.run(
                        ["git", "checkout", "--theirs", file_path],
                        cwd=repo_path,
                        capture_output=True,
                        text=True,
                        timeout=TimeoutConstants.HTTP_DEFAULT
                    )
                    if result.returncode != 0:
                        logger.error(f"❌ Failed to resolve {file_path}")
                        return False
                
                # Stage resolved files
                for file_path in conflict_files:
                    subprocess.run(
                        ["git", "add", file_path],
                        cwd=repo_path,
                        capture_output=True,
                        text=True
                    )
                
                logger.info(f"✅ Auto-resolved {len(conflict_files)} conflicts using '{strategy}' strategy")
                return True
            
            elif strategy == "ours":
                # Use target branch version (ours)
                for file_path in conflict_files:
                    result = subprocess.run(
                        ["git", "checkout", "--ours", file_path],
                        cwd=repo_path,
                        capture_output=True,
                        text=True,
                        timeout=TimeoutConstants.HTTP_DEFAULT
                    )
                    if result.returncode != 0:
                        logger.error(f"❌ Failed to resolve {file_path}")
                        return False
                
                # Stage resolved files
                for file_path in conflict_files:
                    subprocess.run(
                        ["git", "add", file_path],
                        cwd=repo_path,
                        capture_output=True,
                        text=True
                    )
                
                logger.info(f"✅ Auto-resolved {len(conflict_files)} conflicts using '{strategy}' strategy")
                return True
            
            else:
                logger.error(f"❌ Unknown resolution strategy: {strategy}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Auto-resolution error: {e}")
            return False
    
    def generate_conflict_report(
        self,
        repo_path: Path,
        conflict_files: List[str]
    ) -> Dict[str, Any]:
        """
        Generate detailed conflict report.
        
        Args:
            repo_path: Path to repository
            conflict_files: List of conflicted files
        
        Returns:
            Conflict report dictionary
        """
        report = {
            "conflict_count": len(conflict_files),
            "conflict_files": conflict_files,
            "conflict_details": []
        }
        
        for file_path in conflict_files:
            file_full_path = repo_path / file_path
            if file_full_path.exists():
                content = file_full_path.read_text(encoding='utf-8')
                
                # Count conflict markers
                ours_markers = content.count("<<<<<<<")
                theirs_markers = content.count("")
                end_markers = content.count(">>>>>>>")
                
                report["conflict_details"].append({
                    "file": file_path,
                    "ours_markers": ours_markers,
                    "theirs_markers": theirs_markers,
                    "end_markers": end_markers,
                    "total_conflicts": min(ours_markers, theirs_markers, end_markers)
                })
        
        return report
    
    def merge_with_conflict_resolution(
        self,
        repo_path: Path,
        source_branch: str,
        target_branch: str = "main",
        resolution_strategy: str = "theirs"
    ) -> Tuple[bool, Optional[List[str]], Optional[str]]:
        """
        Perform merge with automatic conflict resolution.
        
        Args:
            repo_path: Path to repository
            source_branch: Source branch
            target_branch: Target branch
            resolution_strategy: Conflict resolution strategy
        
        Returns:
            Tuple of (success, conflict_files, error_message)
        """
        try:
            # Checkout target branch
            subprocess.run(
                ["git", "checkout", target_branch],
                cwd=repo_path,
                capture_output=True,
                text=True,
                timeout=TimeoutConstants.HTTP_DEFAULT
            )
            
            # Detect conflicts first
            has_conflicts, conflict_files = self.detect_conflicts(
                repo_path, source_branch, target_branch
            )
            
            # Perform merge
            result = subprocess.run(
                ["git", "merge", "--no-commit", "--no-ff", source_branch],
                cwd=repo_path,
                capture_output=True,
                text=True,
                timeout=TimeoutConstants.HTTP_MEDIUM
            )
            
            # Resolve conflicts if any
            if has_conflicts and conflict_files:
                logger.warning(f"⚠️ Conflicts detected: {len(conflict_files)} files")
                
                # Auto-resolve
                resolution_success = self.resolve_conflicts_auto(
                    repo_path, conflict_files, resolution_strategy
                )
                
                if not resolution_success:
                    return False, conflict_files, "Conflict resolution failed"
                
                # Generate conflict report
                report = self.generate_conflict_report(repo_path, conflict_files)
                logger.info(f"📋 Conflict report: {report['conflict_count']} files resolved")
                
                return True, conflict_files, None
            
            elif result.returncode == 0:
                logger.info(f"✅ Merge successful: {source_branch} → {target_branch}")
                return True, None, None
            else:
                error_msg = result.stderr or result.stdout
                logger.error(f"❌ Merge failed: {error_msg}")
                return False, None, error_msg
                
        except Exception as e:
            logger.error(f"❌ Merge with resolution error: {e}")
            return False, None, str(e)


# Global instance
_conflict_resolver: Optional[MergeConflictResolver] = None


def get_conflict_resolver() -> MergeConflictResolver:
    """Get global MergeConflictResolver instance."""
    global _conflict_resolver
    if _conflict_resolver is None:
        _conflict_resolver = MergeConflictResolver()
    return _conflict_resolver

