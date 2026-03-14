"""
@file
@summary Export AGI Phase 0 safety components for package consumers.
@registry docs/recovery/recovery_registry.yaml#safety-package-init
"""

from .safety_sandbox import (
    SafetySandbox as _SafetySandbox,
    SandboxConfig,
    SandboxMode,
    SandboxViolation,
)
from .kill_switch import KillSwitch, KillSwitchState, get_kill_switch
from .blast_radius import (
    BlastRadiusLimiter,
    BlastRadiusViolation,
    ResourceType,
    get_blast_radius_limiter,
)
from .audit_trail import AuditTrail, AuditEvent, EventType, get_audit_trail
from .state_snapshots import StateSnapshotManager, SnapshotConfig, get_snapshot_manager


class SafetySandbox(_SafetySandbox):
    """Compatibility wrapper that normalizes string-based mode overrides."""

    def __init__(self, config: SandboxConfig | None = None):
        if config is not None and isinstance(config.mode, str):
            config.mode = SandboxMode(config.mode.lower())
        super().__init__(config)


__all__ = [
    "SafetySandbox",
    "SandboxConfig",
    "SandboxMode",
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

__version__ = "1.0.1"
__phase__ = "AGI Phase 0"
