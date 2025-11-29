#!/usr/bin/env python3
"""
Swarm Consolidation Buffer
==========================

Holds diffs, branches, merge plans, and metadata locally
before attempting GitHub operations. Enables N-agents to work
in parallel without network bottlenecks.

V2 Compliance: SOLID principles, buffer pattern
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2025-11-28
Priority: CRITICAL - Bottleneck Breaking
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from enum import Enum
import hashlib

logger = logging.getLogger(__name__)


class ConsolidationStatus(Enum):
    """Status of consolidation operation."""
    PENDING = "pending"
    VALIDATED = "validated"
    MERGED = "merged"
    CONFLICT = "conflict"
    APPLIED = "applied"
    FAILED = "failed"


class MergePlan:
    """Represents a merge plan for consolidation."""
    
    def __init__(
        self,
        source_repo: str,
        target_repo: str,
        source_branch: str = "main",
        target_branch: str = "main",
        description: Optional[str] = None
    ):
        """Initialize merge plan."""
        self.source_repo = source_repo
        self.target_repo = target_repo
        self.source_branch = source_branch
        self.target_branch = target_branch
        self.description = description
        self.plan_id = self._generate_id()
        self.created_at = datetime.now().isoformat()
        self.status = ConsolidationStatus.PENDING
        self.diff_file: Optional[Path] = None
        self.conflicts: List[str] = []
        self.metadata: Dict[str, Any] = {}
    
    def _generate_id(self) -> str:
        """Generate unique plan ID."""
        data = f"{self.source_repo}-{self.target_repo}-{self.created_at}"
        return hashlib.md5(data.encode()).hexdigest()[:12]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "plan_id": self.plan_id,
            "source_repo": self.source_repo,
            "target_repo": self.target_repo,
            "source_branch": self.source_branch,
            "target_branch": self.target_branch,
            "description": self.description,
            "created_at": self.created_at,
            "status": self.status.value,
            "diff_file": str(self.diff_file) if self.diff_file else None,
            "conflicts": self.conflicts,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MergePlan':
        """Create from dictionary."""
        plan = cls(
            source_repo=data["source_repo"],
            target_repo=data["target_repo"],
            source_branch=data.get("source_branch", "main"),
            target_branch=data.get("target_branch", "main"),
            description=data.get("description")
        )
        plan.plan_id = data["plan_id"]
        plan.created_at = data["created_at"]
        plan.status = ConsolidationStatus(data["status"])
        plan.diff_file = Path(data["diff_file"]) if data.get("diff_file") else None
        plan.conflicts = data.get("conflicts", [])
        plan.metadata = data.get("metadata", {})
        return plan


class ConsolidationBuffer:
    """Manages consolidation buffer for swarm operations."""
    
    def __init__(self, buffer_dir: Optional[Path] = None):
        """
        Initialize consolidation buffer.
        
        Args:
            buffer_dir: Directory for buffer storage
        """
        if buffer_dir is None:
            project_root = Path(__file__).resolve().parent.parent.parent
            buffer_dir = project_root / "dream" / "consolidation_buffer"
        
        self.buffer_dir = Path(buffer_dir)
        self.buffer_dir.mkdir(parents=True, exist_ok=True)
        
        # Storage for merge plans
        self.plans_file = self.buffer_dir / "merge_plans.json"
        self.plans: Dict[str, MergePlan] = self._load_plans()
        
        # Storage for diffs
        self.diffs_dir = self.buffer_dir / "diffs"
        self.diffs_dir.mkdir(parents=True, exist_ok=True)
        
        # Storage for conflicts
        self.conflicts_dir = self.buffer_dir / "conflicts"
        self.conflicts_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"✅ Consolidation Buffer initialized: {self.buffer_dir}")
    
    def _load_plans(self) -> Dict[str, MergePlan]:
        """Load merge plans from storage."""
        if self.plans_file.exists():
            try:
                with open(self.plans_file, 'r') as f:
                    data = json.load(f)
                    return {
                        plan_id: MergePlan.from_dict(plan_data)
                        for plan_id, plan_data in data.items()
                    }
            except Exception as e:
                logger.warning(f"Failed to load plans: {e}")
                return {}
        return {}
    
    def _save_plans(self):
        """Save merge plans to storage."""
        try:
            data = {
                plan_id: plan.to_dict()
                for plan_id, plan in self.plans.items()
            }
            with open(self.plans_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save plans: {e}")
    
    def create_merge_plan(
        self,
        source_repo: str,
        target_repo: str,
        source_branch: str = "main",
        target_branch: str = "main",
        description: Optional[str] = None
    ) -> MergePlan:
        """
        Create a new merge plan.
        
        Args:
            source_repo: Source repository name
            target_repo: Target repository name
            source_branch: Source branch
            target_branch: Target branch
            description: Optional description
        
        Returns:
            MergePlan instance
        """
        plan = MergePlan(
            source_repo=source_repo,
            target_repo=target_repo,
            source_branch=source_branch,
            target_branch=target_branch,
            description=description
        )
        
        self.plans[plan.plan_id] = plan
        self._save_plans()
        
        logger.info(f"📋 Merge plan created: {plan.plan_id} ({source_repo} → {target_repo})")
        return plan
    
    def get_plan(self, plan_id: str) -> Optional[MergePlan]:
        """Get merge plan by ID."""
        return self.plans.get(plan_id)
    
    def get_pending_plans(self) -> List[MergePlan]:
        """Get all pending merge plans."""
        return [
            plan for plan in self.plans.values()
            if plan.status == ConsolidationStatus.PENDING
        ]
    
    def get_conflict_plans(self) -> List[MergePlan]:
        """Get all plans with conflicts."""
        return [
            plan for plan in self.plans.values()
            if plan.status == ConsolidationStatus.CONFLICT
        ]
    
    def store_diff(
        self,
        plan_id: str,
        diff_content: str
    ) -> Path:
        """
        Store diff content for merge plan.
        
        Args:
            plan_id: Merge plan ID
            diff_content: Diff content
        
        Returns:
            Path to diff file
        """
        plan = self.get_plan(plan_id)
        if not plan:
            raise ValueError(f"Plan not found: {plan_id}")
        
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        diff_file = self.diffs_dir / f"{plan_id}-{timestamp}.diff"
        
        diff_file.write_text(diff_content, encoding='utf-8')
        
        plan.diff_file = diff_file
        self._save_plans()
        
        logger.info(f"📝 Diff stored: {diff_file}")
        return diff_file
    
    def mark_validated(self, plan_id: str):
        """Mark plan as validated."""
        plan = self.get_plan(plan_id)
        if plan:
            plan.status = ConsolidationStatus.VALIDATED
            self._save_plans()
            logger.info(f"✅ Plan validated: {plan_id}")
    
    def mark_merged(self, plan_id: str):
        """Mark plan as merged locally."""
        plan = self.get_plan(plan_id)
        if plan:
            plan.status = ConsolidationStatus.MERGED
            self._save_plans()
            logger.info(f"✅ Plan merged: {plan_id}")
    
    def mark_conflict(
        self,
        plan_id: str,
        conflicts: List[str]
    ):
        """
        Mark plan as having conflicts.
        
        Args:
            plan_id: Merge plan ID
            conflicts: List of conflict file paths
        """
        plan = self.get_plan(plan_id)
        if plan:
            plan.status = ConsolidationStatus.CONFLICT
            plan.conflicts = conflicts
            
            # Store conflict details
            conflict_file = self.conflicts_dir / f"{plan_id}-conflicts.json"
            conflict_file.write_text(
                json.dumps({
                    "plan_id": plan_id,
                    "conflicts": conflicts,
                    "timestamp": datetime.now().isoformat()
                }, indent=2),
                encoding='utf-8'
            )
            
            self._save_plans()
            logger.warning(f"⚠️ Plan has conflicts: {plan_id} ({len(conflicts)} files)")
    
    def mark_applied(self, plan_id: str):
        """Mark plan as applied (pushed to GitHub)."""
        plan = self.get_plan(plan_id)
        if plan:
            plan.status = ConsolidationStatus.APPLIED
            self._save_plans()
            logger.info(f"✅ Plan applied: {plan_id}")
    
    def mark_failed(self, plan_id: str, error: str):
        """Mark plan as failed."""
        plan = self.get_plan(plan_id)
        if plan:
            plan.status = ConsolidationStatus.FAILED
            plan.metadata["error"] = error
            plan.metadata["failed_at"] = datetime.now().isoformat()
            self._save_plans()
            logger.error(f"❌ Plan failed: {plan_id} - {error}")
    
    def get_stats(self) -> Dict[str, int]:
        """Get buffer statistics."""
        stats = {
            "pending": 0,
            "validated": 0,
            "merged": 0,
            "conflict": 0,
            "applied": 0,
            "failed": 0,
            "total": len(self.plans)
        }
        
        for plan in self.plans.values():
            status = plan.status.value
            if status in stats:
                stats[status] += 1
        
        return stats
    
    def clear_completed(self, older_than_days: int = 7):
        """Clear completed/failed plans older than specified days."""
        from datetime import timedelta
        
        cutoff = datetime.now() - timedelta(days=older_than_days)
        
        initial_count = len(self.plans)
        
        self.plans = {
            plan_id: plan
            for plan_id, plan in self.plans.items()
            if plan.status not in [ConsolidationStatus.APPLIED, ConsolidationStatus.FAILED] or
            datetime.fromisoformat(plan.created_at) > cutoff
        }
        
        removed = initial_count - len(self.plans)
        if removed > 0:
            self._save_plans()
            logger.info(f"🧹 Cleared {removed} old completed plans")
        
        return removed


# Global instance
_consolidation_buffer: Optional[ConsolidationBuffer] = None


def get_consolidation_buffer(buffer_dir: Optional[Path] = None) -> ConsolidationBuffer:
    """Get global ConsolidationBuffer instance."""
    global _consolidation_buffer
    if _consolidation_buffer is None:
        _consolidation_buffer = ConsolidationBuffer(buffer_dir)
    return _consolidation_buffer

"""
Swarm Consolidation Buffer
==========================

Holds diffs, branches, merge plans, and metadata locally
before attempting GitHub operations. Enables N-agents to work
in parallel without network bottlenecks.

V2 Compliance: SOLID principles, buffer pattern
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2025-11-28
Priority: CRITICAL - Bottleneck Breaking
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from enum import Enum
import hashlib

logger = logging.getLogger(__name__)


class ConsolidationStatus(Enum):
    """Status of consolidation operation."""
    PENDING = "pending"
    VALIDATED = "validated"
    MERGED = "merged"
    CONFLICT = "conflict"
    APPLIED = "applied"
    FAILED = "failed"


class MergePlan:
    """Represents a merge plan for consolidation."""
    
    def __init__(
        self,
        source_repo: str,
        target_repo: str,
        source_branch: str = "main",
        target_branch: str = "main",
        description: Optional[str] = None
    ):
        """Initialize merge plan."""
        self.source_repo = source_repo
        self.target_repo = target_repo
        self.source_branch = source_branch
        self.target_branch = target_branch
        self.description = description
        self.plan_id = self._generate_id()
        self.created_at = datetime.now().isoformat()
        self.status = ConsolidationStatus.PENDING
        self.diff_file: Optional[Path] = None
        self.conflicts: List[str] = []
        self.metadata: Dict[str, Any] = {}
    
    def _generate_id(self) -> str:
        """Generate unique plan ID."""
        data = f"{self.source_repo}-{self.target_repo}-{self.created_at}"
        return hashlib.md5(data.encode()).hexdigest()[:12]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "plan_id": self.plan_id,
            "source_repo": self.source_repo,
            "target_repo": self.target_repo,
            "source_branch": self.source_branch,
            "target_branch": self.target_branch,
            "description": self.description,
            "created_at": self.created_at,
            "status": self.status.value,
            "diff_file": str(self.diff_file) if self.diff_file else None,
            "conflicts": self.conflicts,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MergePlan':
        """Create from dictionary."""
        plan = cls(
            source_repo=data["source_repo"],
            target_repo=data["target_repo"],
            source_branch=data.get("source_branch", "main"),
            target_branch=data.get("target_branch", "main"),
            description=data.get("description")
        )
        plan.plan_id = data["plan_id"]
        plan.created_at = data["created_at"]
        plan.status = ConsolidationStatus(data["status"])
        plan.diff_file = Path(data["diff_file"]) if data.get("diff_file") else None
        plan.conflicts = data.get("conflicts", [])
        plan.metadata = data.get("metadata", {})
        return plan


class ConsolidationBuffer:
    """Manages consolidation buffer for swarm operations."""
    
    def __init__(self, buffer_dir: Optional[Path] = None):
        """
        Initialize consolidation buffer.
        
        Args:
            buffer_dir: Directory for buffer storage
        """
        if buffer_dir is None:
            project_root = Path(__file__).resolve().parent.parent.parent
            buffer_dir = project_root / "dream" / "consolidation_buffer"
        
        self.buffer_dir = Path(buffer_dir)
        self.buffer_dir.mkdir(parents=True, exist_ok=True)
        
        # Storage for merge plans
        self.plans_file = self.buffer_dir / "merge_plans.json"
        self.plans: Dict[str, MergePlan] = self._load_plans()
        
        # Storage for diffs
        self.diffs_dir = self.buffer_dir / "diffs"
        self.diffs_dir.mkdir(parents=True, exist_ok=True)
        
        # Storage for conflicts
        self.conflicts_dir = self.buffer_dir / "conflicts"
        self.conflicts_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"✅ Consolidation Buffer initialized: {self.buffer_dir}")
    
    def _load_plans(self) -> Dict[str, MergePlan]:
        """Load merge plans from storage."""
        if self.plans_file.exists():
            try:
                with open(self.plans_file, 'r') as f:
                    data = json.load(f)
                    return {
                        plan_id: MergePlan.from_dict(plan_data)
                        for plan_id, plan_data in data.items()
                    }
            except Exception as e:
                logger.warning(f"Failed to load plans: {e}")
                return {}
        return {}
    
    def _save_plans(self):
        """Save merge plans to storage."""
        try:
            data = {
                plan_id: plan.to_dict()
                for plan_id, plan in self.plans.items()
            }
            with open(self.plans_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save plans: {e}")
    
    def create_merge_plan(
        self,
        source_repo: str,
        target_repo: str,
        source_branch: str = "main",
        target_branch: str = "main",
        description: Optional[str] = None
    ) -> MergePlan:
        """
        Create a new merge plan.
        
        Args:
            source_repo: Source repository name
            target_repo: Target repository name
            source_branch: Source branch
            target_branch: Target branch
            description: Optional description
        
        Returns:
            MergePlan instance
        """
        plan = MergePlan(
            source_repo=source_repo,
            target_repo=target_repo,
            source_branch=source_branch,
            target_branch=target_branch,
            description=description
        )
        
        self.plans[plan.plan_id] = plan
        self._save_plans()
        
        logger.info(f"📋 Merge plan created: {plan.plan_id} ({source_repo} → {target_repo})")
        return plan
    
    def get_plan(self, plan_id: str) -> Optional[MergePlan]:
        """Get merge plan by ID."""
        return self.plans.get(plan_id)
    
    def get_pending_plans(self) -> List[MergePlan]:
        """Get all pending merge plans."""
        return [
            plan for plan in self.plans.values()
            if plan.status == ConsolidationStatus.PENDING
        ]
    
    def get_conflict_plans(self) -> List[MergePlan]:
        """Get all plans with conflicts."""
        return [
            plan for plan in self.plans.values()
            if plan.status == ConsolidationStatus.CONFLICT
        ]
    
    def store_diff(
        self,
        plan_id: str,
        diff_content: str
    ) -> Path:
        """
        Store diff content for merge plan.
        
        Args:
            plan_id: Merge plan ID
            diff_content: Diff content
        
        Returns:
            Path to diff file
        """
        plan = self.get_plan(plan_id)
        if not plan:
            raise ValueError(f"Plan not found: {plan_id}")
        
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        diff_file = self.diffs_dir / f"{plan_id}-{timestamp}.diff"
        
        diff_file.write_text(diff_content, encoding='utf-8')
        
        plan.diff_file = diff_file
        self._save_plans()
        
        logger.info(f"📝 Diff stored: {diff_file}")
        return diff_file
    
    def mark_validated(self, plan_id: str):
        """Mark plan as validated."""
        plan = self.get_plan(plan_id)
        if plan:
            plan.status = ConsolidationStatus.VALIDATED
            self._save_plans()
            logger.info(f"✅ Plan validated: {plan_id}")
    
    def mark_merged(self, plan_id: str):
        """Mark plan as merged locally."""
        plan = self.get_plan(plan_id)
        if plan:
            plan.status = ConsolidationStatus.MERGED
            self._save_plans()
            logger.info(f"✅ Plan merged: {plan_id}")
    
    def mark_conflict(
        self,
        plan_id: str,
        conflicts: List[str]
    ):
        """
        Mark plan as having conflicts.
        
        Args:
            plan_id: Merge plan ID
            conflicts: List of conflict file paths
        """
        plan = self.get_plan(plan_id)
        if plan:
            plan.status = ConsolidationStatus.CONFLICT
            plan.conflicts = conflicts
            
            # Store conflict details
            conflict_file = self.conflicts_dir / f"{plan_id}-conflicts.json"
            conflict_file.write_text(
                json.dumps({
                    "plan_id": plan_id,
                    "conflicts": conflicts,
                    "timestamp": datetime.now().isoformat()
                }, indent=2),
                encoding='utf-8'
            )
            
            self._save_plans()
            logger.warning(f"⚠️ Plan has conflicts: {plan_id} ({len(conflicts)} files)")
    
    def mark_applied(self, plan_id: str):
        """Mark plan as applied (pushed to GitHub)."""
        plan = self.get_plan(plan_id)
        if plan:
            plan.status = ConsolidationStatus.APPLIED
            self._save_plans()
            logger.info(f"✅ Plan applied: {plan_id}")
    
    def mark_failed(self, plan_id: str, error: str):
        """Mark plan as failed."""
        plan = self.get_plan(plan_id)
        if plan:
            plan.status = ConsolidationStatus.FAILED
            plan.metadata["error"] = error
            plan.metadata["failed_at"] = datetime.now().isoformat()
            self._save_plans()
            logger.error(f"❌ Plan failed: {plan_id} - {error}")
    
    def get_stats(self) -> Dict[str, int]:
        """Get buffer statistics."""
        stats = {
            "pending": 0,
            "validated": 0,
            "merged": 0,
            "conflict": 0,
            "applied": 0,
            "failed": 0,
            "total": len(self.plans)
        }
        
        for plan in self.plans.values():
            status = plan.status.value
            if status in stats:
                stats[status] += 1
        
        return stats
    
    def clear_completed(self, older_than_days: int = 7):
        """Clear completed/failed plans older than specified days."""
        from datetime import timedelta
        
        cutoff = datetime.now() - timedelta(days=older_than_days)
        
        initial_count = len(self.plans)
        
        self.plans = {
            plan_id: plan
            for plan_id, plan in self.plans.items()
            if plan.status not in [ConsolidationStatus.APPLIED, ConsolidationStatus.FAILED] or
            datetime.fromisoformat(plan.created_at) > cutoff
        }
        
        removed = initial_count - len(self.plans)
        if removed > 0:
            self._save_plans()
            logger.info(f"🧹 Cleared {removed} old completed plans")
        
        return removed


# Global instance
_consolidation_buffer: Optional[ConsolidationBuffer] = None


def get_consolidation_buffer(buffer_dir: Optional[Path] = None) -> ConsolidationBuffer:
    """Get global ConsolidationBuffer instance."""
    global _consolidation_buffer
    if _consolidation_buffer is None:
        _consolidation_buffer = ConsolidationBuffer(buffer_dir)
    return _consolidation_buffer

