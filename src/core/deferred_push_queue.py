#!/usr/bin/env python3
"""
Deferred Push Queue - GitHub Failure Handler

<!-- SSOT Domain: infrastructure -->

============================================

JSON-based queue for deferred GitHub pushes when rate-limited or unavailable.
Allows swarm to continue working even when GitHub is down.

V2 Compliance: SOLID principles, single responsibility
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2025-11-28
Priority: CRITICAL - Bottleneck Breaking
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
from enum import Enum

logger = logging.getLogger(__name__)


class PushStatus(Enum):
    """Status of push operation."""
    PENDING = "pending"
    RETRYING = "retrying"
    FAILED = "failed"
    COMPLETED = "completed"


class DeferredPushQueue:
    """Manages queue of deferred GitHub pushes."""
    
    def __init__(self, queue_file: Optional[Path] = None):
        """
        Initialize deferred push queue.
        
        Args:
            queue_file: Path to queue JSON file (default: deferred_push_queue.json)
        """
        if queue_file is None:
            project_root = Path(__file__).resolve().parent.parent.parent
            queue_file = project_root / "deferred_push_queue.json"
        
        self.queue_file = Path(queue_file)
        self.queue_file.parent.mkdir(parents=True, exist_ok=True)
        
        self.pending_pushes: List[Dict[str, Any]] = self._load_queue()
        logger.info(f"✅ Deferred Push Queue initialized: {len(self.pending_pushes)} pending")
    
    def _load_queue(self) -> List[Dict[str, Any]]:
        """Load queue from JSON file."""
        if self.queue_file.exists():
            try:
                with open(self.queue_file, 'r') as f:
                    data = json.load(f)
                    # Filter out completed entries older than 24 hours
                    pending = [
                        entry for entry in data.get("pending_pushes", [])
                        if entry.get("status") != PushStatus.COMPLETED.value or
                        self._is_recent(entry.get("timestamp"))
                    ]
                    return pending
            except Exception as e:
                logger.warning(f"Failed to load queue: {e}")
                return []
        return []
    
    def _is_recent(self, timestamp_str: Optional[str], hours: int = 24) -> bool:
        """Check if timestamp is within last N hours."""
        if not timestamp_str:
            return False
        
        try:
            timestamp = datetime.fromisoformat(timestamp_str)
            age = (datetime.now() - timestamp).total_seconds() / 3600
            return age < hours
        except Exception:
            return False
    
    def _save_queue(self):
        """Save queue to JSON file."""
        try:
            data = {
                "pending_pushes": self.pending_pushes,
                "last_updated": datetime.now().isoformat()
            }
            with open(self.queue_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save queue: {e}")
    
    def enqueue_push(
        self,
        repo: str,
        branch: str,
        patch_file: Optional[Path] = None,
        reason: str = "rate_limit",
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Add push operation to deferred queue.
        
        Args:
            repo: Repository name
            branch: Branch name
            patch_file: Path to patch file (optional)
            reason: Reason for deferral (rate_limit, network_error, etc.)
            metadata: Additional metadata
        
        Returns:
            Queue entry ID
        """
        import hashlib
        
        # Generate unique ID
        entry_id = hashlib.md5(
            f"{repo}-{branch}-{datetime.now().isoformat()}".encode()
        ).hexdigest()[:12]
        
        entry = {
            "id": entry_id,
            "repo": repo,
            "branch": branch,
            "patch_file": str(patch_file) if patch_file else None,
            "reason": reason,
            "status": PushStatus.PENDING.value,
            "timestamp": datetime.now().isoformat(),
            "retry_count": 0,
            "last_attempt": None,
            "metadata": metadata or {}
        }
        
        self.pending_pushes.append(entry)
        self._save_queue()
        
        logger.info(f"📥 Enqueued push: {repo}/{branch} (ID: {entry_id})")
        return entry_id
    
    def dequeue_push(self) -> Optional[Dict[str, Any]]:
        """Get next pending push operation."""
        pending = [
            entry for entry in self.pending_pushes
            if entry.get("status") == PushStatus.PENDING.value
        ]
        
        if not pending:
            return None
        
        # Return oldest pending entry
        pending.sort(key=lambda x: x.get("timestamp", ""))
        return pending[0]
    
    def mark_retrying(self, entry_id: str):
        """Mark entry as retrying."""
        for entry in self.pending_pushes:
            if entry.get("id") == entry_id:
                entry["status"] = PushStatus.RETRYING.value
                entry["retry_count"] = entry.get("retry_count", 0) + 1
                entry["last_attempt"] = datetime.now().isoformat()
                self._save_queue()
                return
    
    def mark_completed(self, entry_id: str):
        """Mark entry as completed."""
        for entry in self.pending_pushes:
            if entry.get("id") == entry_id:
                entry["status"] = PushStatus.COMPLETED.value
                entry["completed_at"] = datetime.now().isoformat()
                self._save_queue()
                logger.info(f"✅ Push completed: {entry.get('repo')}/{entry.get('branch')}")
                return
    
    def mark_failed(self, entry_id: str, error_message: str, max_retries: int = 5):
        """Mark entry as failed if retry limit exceeded."""
        for entry in self.pending_pushes:
            if entry.get("id") == entry_id:
                retry_count = entry.get("retry_count", 0)
                
                if retry_count >= max_retries:
                    entry["status"] = PushStatus.FAILED.value
                    entry["error"] = error_message
                    entry["failed_at"] = datetime.now().isoformat()
                    logger.warning(f"❌ Push failed permanently: {entry.get('repo')}/{entry.get('branch')}")
                else:
                    # Reset to pending for retry
                    entry["status"] = PushStatus.PENDING.value
                    entry["error"] = error_message
                
                self._save_queue()
                return
    
    def get_pending_count(self) -> int:
        """Get count of pending pushes."""
        return len([
            entry for entry in self.pending_pushes
            if entry.get("status") == PushStatus.PENDING.value
        ])
    
    def get_stats(self) -> Dict[str, int]:
        """Get queue statistics."""
        stats = {
            "pending": 0,
            "retrying": 0,
            "failed": 0,
            "completed": 0,
            "total": len(self.pending_pushes)
        }
        
        for entry in self.pending_pushes:
            status = entry.get("status", PushStatus.PENDING.value)
            if status == PushStatus.PENDING.value:
                stats["pending"] += 1
            elif status == PushStatus.RETRYING.value:
                stats["retrying"] += 1
            elif status == PushStatus.FAILED.value:
                stats["failed"] += 1
            elif status == PushStatus.COMPLETED.value:
                stats["completed"] += 1
        
        return stats
    
    def clear_completed(self, older_than_hours: int = 24):
        """Remove completed entries older than specified hours."""
        initial_count = len(self.pending_pushes)
        
        self.pending_pushes = [
            entry for entry in self.pending_pushes
            if entry.get("status") != PushStatus.COMPLETED.value or
            self._is_recent(entry.get("completed_at"), older_than_hours)
        ]
        
        removed = initial_count - len(self.pending_pushes)
        if removed > 0:
            self._save_queue()
            logger.info(f"🧹 Cleared {removed} old completed entries")
        
        return removed


# Global instance
_deferred_queue: Optional[DeferredPushQueue] = None


def get_deferred_push_queue(queue_file: Optional[Path] = None) -> DeferredPushQueue:
    """Get global DeferredPushQueue instance."""
    global _deferred_queue
    if _deferred_queue is None:
        _deferred_queue = DeferredPushQueue(queue_file)
    return _deferred_queue

