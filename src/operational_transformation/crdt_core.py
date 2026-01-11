#!/usr/bin/env python3
"""
CRDT Core - Conflict-free Replicated Data Types Foundation
==========================================================

Base CRDT implementations for Phase 5 Operational Transformation.
Provides the mathematical foundation for conflict-free collaboration.

CRDT Types Implemented:
- G-Counter: Grow-only counter (increment only)
- PN-Counter: Positive-negative counter (increment/decrement)
- G-Set: Grow-only set (add only)
- 2P-Set: Two-phase set (add/remove with tombstones)

These form the mathematical basis for operational transformation
and real-time collaborative editing.

Author: Agent-8 (SSOT & System Integration Specialist)
Date: 2026-01-11
"""

import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, Set, List, Optional, Union
from dataclasses import dataclass, field
from datetime import datetime

logger = logging.getLogger(__name__)


class CRDTBase(ABC):
    """
    Abstract base class for all CRDT implementations.

    Provides common interface and merge functionality that all CRDTs must support.
    """

    def __init__(self, replica_id: str):
        """
        Initialize CRDT with replica identifier.

        Args:
            replica_id: Unique identifier for this replica/instance
        """
        self.replica_id = replica_id
        self.metadata = {
            'created_at': datetime.now().isoformat(),
            'replica_id': replica_id,
            'version': 0
        }

    @abstractmethod
    def merge(self, other: 'CRDTBase') -> None:
        """
        Merge another CRDT instance into this one.

        This is the core CRDT operation that ensures convergence across replicas.
        Must be commutative, associative, and idempotent.

        Args:
            other: Another CRDT instance to merge
        """
        pass

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize CRDT state to dictionary for transmission/sync.

        Returns:
            Dictionary representation of CRDT state
        """
        pass

    @classmethod
    @abstractmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CRDTBase':
        """
        Deserialize CRDT state from dictionary.

        Args:
            data: Dictionary representation of CRDT state

        Returns:
            Reconstructed CRDT instance
        """
        pass

    def get_version(self) -> int:
        """Get current version number."""
        return self.metadata['version']

    def increment_version(self) -> None:
        """Increment version number."""
        self.metadata['version'] += 1


class GCounter(CRDTBase):
    """
    Grow-only Counter CRDT.

    Only supports increment operations. Values can only increase.
    Mathematically sound for counting events that never decrease.
    """

    def __init__(self, replica_id: str):
        super().__init__(replica_id)
        self.counters: Dict[str, int] = {}  # replica_id -> count

    def increment(self, amount: int = 1) -> None:
        """
        Increment the counter by the specified amount.

        Args:
            amount: Amount to increment (must be positive)
        """
        if amount <= 0:
            raise ValueError("GCounter can only increment by positive amounts")

        current = self.counters.get(self.replica_id, 0)
        self.counters[self.replica_id] = current + amount
        self.increment_version()
        logger.debug(f"GCounter {self.replica_id} incremented by {amount}, total: {self.value()}")

    def value(self) -> int:
        """
        Get the current counter value.

        Returns:
            Sum of all replica counters
        """
        return sum(self.counters.values())

    def merge(self, other: 'GCounter') -> None:
        """
        Merge another GCounter by taking maximum values for each replica.

        Args:
            other: GCounter to merge
        """
        for replica_id, count in other.counters.items():
            current = self.counters.get(replica_id, 0)
            if count > current:
                self.counters[replica_id] = count

        self.increment_version()
        logger.debug(f"GCounter {self.replica_id} merged with {other.replica_id}")

    def to_dict(self) -> Dict[str, Any]:
        """Serialize GCounter state."""
        return {
            'type': 'GCounter',
            'replica_id': self.replica_id,
            'counters': self.counters.copy(),
            'metadata': self.metadata.copy()
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'GCounter':
        """Deserialize GCounter state."""
        counter = cls(data['replica_id'])
        counter.counters = data['counters'].copy()
        counter.metadata = data.get('metadata', counter.metadata)
        return counter


class PNCounter(CRDTBase):
    """
    Positive-Negative Counter CRDT.

    Supports both increment and decrement operations.
    Uses two G-Counters: one for positive operations, one for negative.
    """

    def __init__(self, replica_id: str):
        super().__init__(replica_id)
        self.positive = GCounter(f"{replica_id}_pos")
        self.negative = GCounter(f"{replica_id}_neg")

    def increment(self, amount: int = 1) -> None:
        """
        Increment the counter.

        Args:
            amount: Amount to increment (can be negative for decrement)
        """
        if amount > 0:
            self.positive.increment(amount)
        elif amount < 0:
            self.negative.increment(-amount)

        self.increment_version()

    def decrement(self, amount: int = 1) -> None:
        """
        Decrement the counter.

        Args:
            amount: Amount to decrement
        """
        if amount > 0:
            self.negative.increment(amount)
            self.increment_version()

    def value(self) -> int:
        """
        Get the current counter value.

        Returns:
            Positive counter minus negative counter
        """
        return self.positive.value() - self.negative.value()

    def merge(self, other: 'PNCounter') -> None:
        """
        Merge another PNCounter by merging both internal counters.

        Args:
            other: PNCounter to merge
        """
        self.positive.merge(other.positive)
        self.negative.merge(other.negative)
        self.increment_version()

    def to_dict(self) -> Dict[str, Any]:
        """Serialize PNCounter state."""
        return {
            'type': 'PNCounter',
            'replica_id': self.replica_id,
            'positive': self.positive.to_dict(),
            'negative': self.negative.to_dict(),
            'metadata': self.metadata.copy()
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PNCounter':
        """Deserialize PNCounter state."""
        counter = cls(data['replica_id'])
        counter.positive = GCounter.from_dict(data['positive'])
        counter.negative = GCounter.from_dict(data['negative'])
        counter.metadata = data.get('metadata', counter.metadata)
        return counter


class GSet(CRDTBase):
    """
    Grow-only Set CRDT.

    Only supports add operations. Elements can only be added, never removed.
    Useful for tracking events, logs, or immutable collections.
    """

    def __init__(self, replica_id: str):
        super().__init__(replica_id)
        self.elements: Set[Any] = set()

    def add(self, element: Any) -> None:
        """
        Add an element to the set.

        Args:
            element: Element to add
        """
        if element not in self.elements:
            self.elements.add(element)
            self.increment_version()
            logger.debug(f"GSet {self.replica_id} added element: {element}")

    def contains(self, element: Any) -> bool:
        """
        Check if element is in the set.

        Args:
            element: Element to check

        Returns:
            True if element is in set
        """
        return element in self.elements

    def size(self) -> int:
        """
        Get the size of the set.

        Returns:
            Number of elements in set
        """
        return len(self.elements)

    def merge(self, other: 'GSet') -> None:
        """
        Merge another GSet by union of elements.

        Args:
            other: GSet to merge
        """
        old_size = len(self.elements)
        self.elements.update(other.elements)

        if len(self.elements) > old_size:
            self.increment_version()
            logger.debug(f"GSet {self.replica_id} merged {len(other.elements)} elements")

    def to_dict(self) -> Dict[str, Any]:
        """Serialize GSet state."""
        return {
            'type': 'GSet',
            'replica_id': self.replica_id,
            'elements': list(self.elements),
            'metadata': self.metadata.copy()
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'GSet':
        """Deserialize GSet state."""
        gset = cls(data['replica_id'])
        gset.elements = set(data['elements'])
        gset.metadata = data.get('metadata', gset.metadata)
        return gset


class TwoPSet(CRDTBase):
    """
    Two-Phase Set CRDT.

    Supports add and remove operations using tombstones.
    Elements can be added and removed, but removals are permanent.
    Uses two G-Sets: one for additions, one for removals (tombstones).
    """

    def __init__(self, replica_id: str):
        super().__init__(replica_id)
        self.additions = GSet(f"{replica_id}_add")
        self.removals = GSet(f"{replica_id}_rem")

    def add(self, element: Any) -> None:
        """
        Add an element to the set.

        Args:
            element: Element to add
        """
        self.additions.add(element)
        self.increment_version()

    def remove(self, element: Any) -> None:
        """
        Remove an element from the set (permanent).

        Args:
            element: Element to remove
        """
        self.removals.add(element)
        self.increment_version()

    def contains(self, element: Any) -> bool:
        """
        Check if element is in the set.

        An element is in the set if it was added and not removed.

        Args:
            element: Element to check

        Returns:
            True if element is in set
        """
        return self.additions.contains(element) and not self.removals.contains(element)

    def elements(self) -> Set[Any]:
        """
        Get all current elements in the set.

        Returns:
            Set of elements currently in the set
        """
        return {elem for elem in self.additions.elements if not self.removals.contains(elem)}

    def size(self) -> int:
        """
        Get the current size of the set.

        Returns:
            Number of elements currently in set
        """
        return len(self.elements())

    def merge(self, other: 'TwoPSet') -> None:
        """
        Merge another TwoPSet by merging both internal sets.

        Args:
            other: TwoPSet to merge
        """
        old_elements = self.elements()
        self.additions.merge(other.additions)
        self.removals.merge(other.removals)

        if self.elements() != old_elements:
            self.increment_version()

    def to_dict(self) -> Dict[str, Any]:
        """Serialize TwoPSet state."""
        return {
            'type': 'TwoPSet',
            'replica_id': self.replica_id,
            'additions': self.additions.to_dict(),
            'removals': self.removals.to_dict(),
            'metadata': self.metadata.copy()
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TwoPSet':
        """Deserialize TwoPSet state."""
        twopset = cls(data['replica_id'])
        twopset.additions = GSet.from_dict(data['additions'])
        twopset.removals = GSet.from_dict(data['removals'])
        twopset.metadata = data.get('metadata', twopset.metadata)
        return twopset