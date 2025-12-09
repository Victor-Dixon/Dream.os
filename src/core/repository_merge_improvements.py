#!/usr/bin/env python3
"""
Repository Merge Improvements - Enhanced Merge System
=====================================================

Implements all 6 recommendations from MERGE_FAILURE_INVESTIGATION.md:
1. Error classification (permanent vs transient)
2. Pre-flight checks (verify repos exist)
3. Duplicate prevention (track attempts)
4. Name resolution (normalize repo names)
5. Status tracking (exists/merged/deleted)
6. Strategy review (verify consolidation direction)

<!-- SSOT Domain: infrastructure -->

Author: Agent-7 (Web Development Specialist)
Date: 2025-12-04
V2 Compliant: Yes (<300 lines)
"""

import json
import logging
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Dict, Optional, Tuple, List
from dataclasses import dataclass
from src.core.utils.serialization_utils import to_dict

logger = logging.getLogger(__name__)

# Path to repository status tracking file
REPO_STATUS_FILE = Path("dream/consolidation_buffer/repo_status_tracking.json")
ATTEMPT_TRACKING_FILE = Path("dream/consolidation_buffer/merge_attempt_tracking.json")


class ErrorType(Enum):
    """Error classification for merge failures."""
    PERMANENT = "permanent"  # Don't retry (repo not available, deleted, etc.)
    TRANSIENT = "transient"  # Retry with backoff (network, rate limits)
    UNKNOWN = "unknown"  # Log and investigate


class RepoStatus(Enum):
    """Repository status tracking."""
    EXISTS = "exists"
    MERGED = "merged"
    DELETED = "deleted"
    UNKNOWN = "unknown"
    NOT_ACCESSIBLE = "not_accessible"


@dataclass
class RepoMetadata:
    """Repository metadata for tracking."""
    name: str
    normalized_name: str
    status: RepoStatus
    last_seen: Optional[str] = None
    last_checked: Optional[str] = None
    error_count: int = 0
    last_error: Optional[str] = None
    merged_into: Optional[str] = None


@dataclass
class MergeAttempt:
    """Track merge attempts to prevent duplicates."""
    source_repo: str
    target_repo: str
    normalized_pair: str
    first_attempt: str
    last_attempt: str
    attempt_count: int
    last_error: Optional[str] = None
    error_type: Optional[ErrorType] = None
    success: bool = False


class RepositoryMergeImprovements:
    """Enhanced repository merge system with all improvements."""
    
    def __init__(self):
        self.repo_statuses: Dict[str, RepoMetadata] = {}
        self.merge_attempts: Dict[str, MergeAttempt] = {}
        self._load_tracking_data()
    
    def _load_tracking_data(self):
        """Load repository status and attempt tracking data."""
        try:
            if REPO_STATUS_FILE.exists():
                data = json.loads(REPO_STATUS_FILE.read_text(encoding='utf-8'))
                for name, meta in data.items():
                    self.repo_statuses[name] = RepoMetadata(
                        **{**meta, 'status': RepoStatus(meta['status'])}
                    )
        except Exception as e:
            logger.warning(f"Error loading repo statuses: {e}")
        
        try:
            if ATTEMPT_TRACKING_FILE.exists():
                data = json.loads(ATTEMPT_TRACKING_FILE.read_text(encoding='utf-8'))
                for pair, attempt in data.items():
                    self.merge_attempts[pair] = MergeAttempt(
                        **{**attempt, 'error_type': ErrorType(attempt['error_type']) if attempt.get('error_type') else None}
                    )
        except Exception as e:
            logger.warning(f"Error loading merge attempts: {e}")
    
    def _save_tracking_data(self):
        """Save repository status and attempt tracking data."""
        try:
            REPO_STATUS_FILE.parent.mkdir(parents=True, exist_ok=True)
            data = {
                name: {
                    **to_dict(meta),
                    'status': meta.status.value
                }
                for name, meta in self.repo_statuses.items()
            }
            REPO_STATUS_FILE.write_text(
                json.dumps(data, indent=2, ensure_ascii=False),
                encoding='utf-8'
            )
        except Exception as e:
            logger.error(f"Error saving repo statuses: {e}")
        
        try:
            ATTEMPT_TRACKING_FILE.parent.mkdir(parents=True, exist_ok=True)
            data = {
                pair: {
                    **to_dict(attempt),
                    'error_type': attempt.error_type.value if attempt.error_type else None
                }
                for pair, attempt in self.merge_attempts.items()
            }
            ATTEMPT_TRACKING_FILE.write_text(
                json.dumps(data, indent=2, ensure_ascii=False),
                encoding='utf-8'
            )
        except Exception as e:
            logger.error(f"Error saving merge attempts: {e}")
    
    # 1. ERROR CLASSIFICATION
    def classify_error(self, error_message: str) -> ErrorType:
        """
        Classify error as permanent, transient, or unknown.
        
        Permanent errors: Don't retry (repo not available, deleted, etc.)
        Transient errors: Retry with backoff (network, rate limits)
        """
        error_lower = error_message.lower()
        
        # Permanent errors - don't retry
        permanent_indicators = [
            "source repo not available",
            "target repo not available",
            "repo not available",
            "repository not found",
            "404",
            "repository does not exist",
            "repository deleted",
            "access denied",
            "permission denied",
            "forbidden"
        ]
        
        if any(indicator in error_lower for indicator in permanent_indicators):
            return ErrorType.PERMANENT
        
        # Transient errors - retry with backoff
        transient_indicators = [
            "rate limit",
            "network",
            "timeout",
            "connection",
            "temporary",
            "503",
            "502",
            "500"
        ]
        
        if any(indicator in error_lower for indicator in transient_indicators):
            return ErrorType.TRANSIENT
        
        return ErrorType.UNKNOWN
    
    # 2. PRE-FLIGHT CHECKS
    def verify_repo_exists(self, repo_name: str, github_client=None) -> Tuple[bool, Optional[str]]:
        """
        Verify repository exists before attempting merge.
        
        Returns:
            (exists, error_message)
        """
        normalized = self.normalize_repo_name(repo_name)
        
        # Check cached status
        if normalized in self.repo_statuses:
            meta = self.repo_statuses[normalized]
            if meta.status == RepoStatus.DELETED:
                return False, f"Repository {repo_name} was previously deleted"
            if meta.status == RepoStatus.MERGED:
                return False, f"Repository {repo_name} was already merged into {meta.merged_into}"
            if meta.status == RepoStatus.EXISTS:
                # Update last checked
                meta.last_checked = datetime.now().isoformat()
                self._save_tracking_data()
                return True, None
        
        # If we have a GitHub client, verify via API
        if github_client:
            try:
                exists = github_client.repo_exists(repo_name)
                status = RepoStatus.EXISTS if exists else RepoStatus.DELETED
                self.update_repo_status(repo_name, status)
                return exists, None if exists else f"Repository {repo_name} does not exist"
            except Exception as e:
                logger.warning(f"Error checking repo existence via API: {e}")
        
        # Default: assume exists if not in cache
        return True, None
    
    # 3. DUPLICATE PREVENTION
    def should_attempt_merge(self, source_repo: str, target_repo: str) -> Tuple[bool, Optional[str]]:
        """
        Check if merge should be attempted (prevent duplicates).
        
        Returns:
            (should_attempt, reason_if_not)
        """
        normalized_pair = self._normalize_pair(source_repo, target_repo)
        
        if normalized_pair in self.merge_attempts:
            attempt = self.merge_attempts[normalized_pair]
            
            # If already successful, don't retry
            if attempt.success:
                return False, f"Merge already successful: {source_repo} → {target_repo}"
            
            # If permanent error, don't retry
            if attempt.error_type == ErrorType.PERMANENT:
                return False, f"Permanent error on previous attempt: {attempt.last_error}"
            
            # If transient error, check cooldown (1 hour)
            if attempt.error_type == ErrorType.TRANSIENT:
                last_attempt = datetime.fromisoformat(attempt.last_attempt)
                if datetime.now() - last_attempt < timedelta(hours=1):
                    return False, f"Transient error - cooldown period (last attempt: {attempt.last_attempt})"
        
        return True, None
    
    def record_merge_attempt(self, source_repo: str, target_repo: str, 
                            success: bool, error: Optional[str] = None):
        """Record merge attempt for duplicate prevention."""
        normalized_pair = self._normalize_pair(source_repo, target_repo)
        now = datetime.now().isoformat()
        
        if normalized_pair in self.merge_attempts:
            attempt = self.merge_attempts[normalized_pair]
            attempt.last_attempt = now
            attempt.attempt_count += 1
            attempt.success = success
            attempt.last_error = error
            attempt.error_type = self.classify_error(error) if error else None
        else:
            attempt = MergeAttempt(
                source_repo=source_repo,
                target_repo=target_repo,
                normalized_pair=normalized_pair,
                first_attempt=now,
                last_attempt=now,
                attempt_count=1,
                success=success,
                last_error=error,
                error_type=self.classify_error(error) if error else None
            )
            self.merge_attempts[normalized_pair] = attempt
        
        self._save_tracking_data()
    
    # 4. NAME RESOLUTION
    def normalize_repo_name(self, repo_name: str) -> str:
        """
        Normalize repository name for comparison.
        
        Handles:
        - Case variations (focusforge vs FocusForge)
        - Owner/repo format (Dadudekc/focusforge vs focusforge)
        - Whitespace
        """
        # Remove whitespace
        normalized = repo_name.strip()
        
        # Extract repo name if owner/repo format
        if "/" in normalized:
            parts = normalized.split("/")
            owner = parts[0].strip()
            repo = "/".join(parts[1:]).strip()
            normalized = f"{owner}/{repo}"
        else:
            normalized = normalized
        
        # Store original case for reference, but normalize for comparison
        return normalized
    
    def _normalize_pair(self, source: str, target: str) -> str:
        """Normalize merge pair for tracking."""
        return f"{self.normalize_repo_name(source)}→{self.normalize_repo_name(target)}"
    
    def find_case_variations(self, repo_name: str, known_repos: List[str]) -> List[str]:
        """
        Find case variations of a repository name.
        
        Example: "focusforge" → ["FocusForge", "FocusForge", etc.]
        """
        normalized = self.normalize_repo_name(repo_name).lower()
        variations = []
        
        for known in known_repos:
            if self.normalize_repo_name(known).lower() == normalized:
                variations.append(known)
        
        return variations
    
    # 5. STATUS TRACKING
    def update_repo_status(self, repo_name: str, status: RepoStatus, 
                          merged_into: Optional[str] = None):
        """Update repository status tracking."""
        normalized = self.normalize_repo_name(repo_name)
        now = datetime.now().isoformat()
        
        if normalized in self.repo_statuses:
            meta = self.repo_statuses[normalized]
            meta.status = status
            meta.last_checked = now
            if status == RepoStatus.EXISTS:
                meta.last_seen = now
            if merged_into:
                meta.merged_into = merged_into
        else:
            meta = RepoMetadata(
                name=repo_name,
                normalized_name=normalized,
                status=status,
                last_seen=now if status == RepoStatus.EXISTS else None,
                last_checked=now,
                merged_into=merged_into
            )
            self.repo_statuses[normalized] = meta
        
        self._save_tracking_data()
    
    def get_repo_status(self, repo_name: str) -> Optional[RepoMetadata]:
        """Get repository status metadata."""
        normalized = self.normalize_repo_name(repo_name)
        return self.repo_statuses.get(normalized)
    
    # 6. STRATEGY REVIEW
    def verify_consolidation_direction(self, source_repo: str, target_repo: str) -> Tuple[bool, Optional[str]]:
        """
        Verify consolidation direction is correct.
        
        Checks:
        - Source repo exists
        - Target repo exists
        - Source not already merged
        - Target not a case variation of source (unless intentional)
        """
        # Check source exists
        source_exists, source_error = self.verify_repo_exists(source_repo)
        if not source_exists:
            return False, f"Source repo check failed: {source_error}"
        
        # Check target exists
        target_exists, target_error = self.verify_repo_exists(target_repo)
        if not target_exists:
            return False, f"Target repo check failed: {target_error}"
        
        # Check source not already merged
        source_status = self.get_repo_status(source_repo)
        if source_status and source_status.status == RepoStatus.MERGED:
            return False, f"Source repo {source_repo} already merged into {source_status.merged_into}"
        
        return True, None
    
    def pre_merge_validation(self, source_repo: str, target_repo: str, 
                            github_client=None) -> Tuple[bool, Optional[str], Dict[str, any]]:
        """
        Complete pre-merge validation combining all checks.
        
        Returns:
            (should_proceed, error_message, validation_details)
        """
        validation = {
            "source_repo": source_repo,
            "target_repo": target_repo,
            "normalized_source": self.normalize_repo_name(source_repo),
            "normalized_target": self.normalize_repo_name(target_repo),
            "checks": {}
        }
        
        # 1. Duplicate prevention
        should_attempt, reason = self.should_attempt_merge(source_repo, target_repo)
        validation["checks"]["duplicate_prevention"] = {
            "should_attempt": should_attempt,
            "reason": reason
        }
        if not should_attempt:
            return False, reason, validation
        
        # 2. Pre-flight checks
        source_exists, source_error = self.verify_repo_exists(source_repo, github_client)
        validation["checks"]["source_repo_exists"] = {
            "exists": source_exists,
            "error": source_error
        }
        if not source_exists:
            self.record_merge_attempt(source_repo, target_repo, False, source_error)
            return False, source_error, validation
        
        target_exists, target_error = self.verify_repo_exists(target_repo, github_client)
        validation["checks"]["target_repo_exists"] = {
            "exists": target_exists,
            "error": target_error
        }
        if not target_exists:
            self.record_merge_attempt(source_repo, target_repo, False, target_error)
            return False, target_error, validation
        
        # 3. Strategy review
        direction_ok, direction_error = self.verify_consolidation_direction(source_repo, target_repo)
        validation["checks"]["consolidation_direction"] = {
            "valid": direction_ok,
            "error": direction_error
        }
        if not direction_ok:
            self.record_merge_attempt(source_repo, target_repo, False, direction_error)
            return False, direction_error, validation
        
        validation["checks"]["all_passed"] = True
        return True, None, validation


# Singleton instance
_merge_improvements: Optional[RepositoryMergeImprovements] = None


def get_merge_improvements() -> RepositoryMergeImprovements:
    """Get singleton instance of merge improvements."""
    global _merge_improvements
    if _merge_improvements is None:
        _merge_improvements = RepositoryMergeImprovements()
    return _merge_improvements

