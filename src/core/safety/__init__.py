"""
Safety Foundation Module - AGI Phase 0
======================================

Core safety infrastructure for autonomous operations.
Provides isolation, auditing, rollback, and blast radius limiting.

Components:
- safety_sandbox.py: Isolated execution environment (AGI-17)
- kill_switch.py: Emergency stop mechanism (AGI-18)
- blast_radius.py: Damage control limits (AGI-19)
- audit_trail.py: Decision logging (AGI-20)
- state_snapshots.py: Rollback capability (AGI-26)

Author: Agent-4 (Captain) with Cloud Agent
License: MIT
"""

from .safety_sandbox import SafetySandbox, SandboxConfig, SandboxViolation
from .kill_switch import KillSwitch, KillSwitchState
from .blast_radius import BlastRadiusLimiter, BlastRadiusViolation
from .audit_trail import AuditTrail, AuditEvent
from .state_snapshots import StateSnapshotManager, SnapshotConfig

__all__ = [
    "SafetySandbox",
    "SandboxConfig",
    "SandboxViolation",
    "KillSwitch",
    "KillSwitchState",
    "BlastRadiusLimiter",
    "BlastRadiusViolation",
    "AuditTrail",
    "AuditEvent",
    "StateSnapshotManager",
    "SnapshotConfig",
]

__version__ = "1.0.0"
__phase__ = "AGI Phase 0"
