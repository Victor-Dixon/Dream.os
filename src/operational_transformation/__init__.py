"""
Operational Transformation Engine - Phase 5 Foundation
======================================================

Conflict-free Replicated Data Types (CRDT) and Operational Transformation (OT)
for real-time collaborative editing and synchronization.

This module provides the foundation for Phase 5 Operational Transformation,
enabling conflict-free collaboration across the swarm intelligence system.

Key Components:
- CRDT Core: Base CRDT implementations (G-Counter, PN-Counter, G-Set, etc.)
- OT Engine: Operational transformation algorithms for concurrent operations
- Sync Protocol: Real-time synchronization and conflict resolution
- Collaborative Framework: Integration with swarm coordination

Author: Agent-8 (SSOT & System Integration Specialist)
Date: 2026-01-11
"""

from .crdt_core import CRDTBase, GCounter, PNCounter, GSet, TwoPSet
from .ot_engine import OTEngine, Operation, OperationType
from .sync_protocol import SyncProtocol, SyncMessage

__all__ = [
    'CRDTBase', 'GCounter', 'PNCounter', 'GSet', 'TwoPSet',
    'OTEngine', 'Operation', 'OperationType',
    'SyncProtocol', 'SyncMessage'
]

__version__ = "0.1.0"
__phase__ = "Phase 5 - Operational Transformation Foundation"