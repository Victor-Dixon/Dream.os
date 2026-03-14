"""
@file
@summary Export AGI Phase 0 safety components for package consumers.
@registry docs/recovery/recovery_registry.yaml#safety-package-init
"""

from .safety_sandbox import SafetySandbox, SandboxConfig, SandboxViolation
from .kill_switch import KillSwitch, KillSwitchState, get_kill_switch
from .blast_radius import (
    BlastRadiusLimiter,
    BlastRadiusViolation,
    ResourceType,
    get_blast_radius_limiter,
)
from .audit_trail import AuditTrail, AuditEvent, EventType, get_audit_trail
from .state_snapshots import StateSnapshotManager, SnapshotConfig, get_snapshot_manager

__all__ = [
    "SafetySandbox",
    "SandboxConfig",
    "SandboxViolation",
    "KillSwitch",
    "KillSwitchState",
    "get_kill_switch",
    "BlastRadiusLimiter",
    "BlastRadiusViolation",
    "ResourceType",
    "get_blast_radius_limiter",
    "AuditTrail",
    "AuditEvent",
    "EventType",
    "get_audit_trail",
    "StateSnapshotManager",
    "SnapshotConfig",
    "get_snapshot_manager",
]

__version__ = "1.0.0"
__phase__ = "AGI Phase 0"
