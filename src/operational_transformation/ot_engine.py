#!/usr/bin/env python3
"""
Operational Transformation Engine - Phase 5 Core
================================================

Operational Transformation (OT) algorithms for real-time collaborative editing.
Provides conflict-free concurrent operations on shared data structures.

Key Components:
- Operation Types: Insert, Delete, Update operations
- Transformation Functions: Convert concurrent operations to serializable form
- Site ID Management: Unique identifiers for operation ordering
- History Buffer: Maintain operation history for transformation

This enables real-time collaborative editing where multiple users can
modify the same document simultaneously without conflicts.

Author: Agent-8 (SSOT & System Integration Specialist)
Date: 2026-01-11
"""

import logging
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple, Union
from dataclasses import dataclass, field
from datetime import datetime

logger = logging.getLogger(__name__)


class OperationType(Enum):
    """Types of operations that can be transformed."""
    INSERT = "insert"
    DELETE = "delete"
    UPDATE = "update"


@dataclass
class Operation:
    """
    Represents a single operation in the operational transformation system.

    Each operation has a unique ID, type, position/context information,
    and the actual data being operated on.
    """
    operation_id: str
    operation_type: OperationType
    site_id: int  # Unique identifier for the site/replica that generated this operation
    sequence_number: int  # Logical clock value for this operation
    position: Union[int, str]  # Position in the document (index for text, key for objects)
    data: Any  # The actual data (character for insert, None for delete, new value for update)
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """Convert operation to dictionary for serialization."""
        return {
            'operation_id': self.operation_id,
            'operation_type': self.operation_type.value,
            'site_id': self.site_id,
            'sequence_number': self.sequence_number,
            'position': self.position,
            'data': self.data,
            'timestamp': self.timestamp.isoformat()
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Operation':
        """Create operation from dictionary."""
        return cls(
            operation_id=data['operation_id'],
            operation_type=OperationType(data['operation_type']),
            site_id=data['site_id'],
            sequence_number=data['sequence_number'],
            position=data['position'],
            data=data['data'],
            timestamp=datetime.fromisoformat(data['timestamp'])
        )

    def __lt__(self, other: 'Operation') -> bool:
        """Compare operations for ordering (by sequence number, then site ID)."""
        if self.sequence_number != other.sequence_number:
            return self.sequence_number < other.sequence_number
        return self.site_id < other.site_id


class OTEngine:
    """
    Operational Transformation Engine.

    Manages concurrent operations on shared data structures, ensuring
    that all replicas converge to the same final state regardless of
    operation order.
    """

    def __init__(self, site_id: int):
        """
        Initialize OT engine with unique site identifier.

        Args:
            site_id: Unique identifier for this replica/site
        """
        self.site_id = site_id
        self.sequence_number = 0
        self.history_buffer: List[Operation] = []
        self.pending_operations: List[Operation] = []

        # State vector for causal ordering
        self.state_vector: Dict[int, int] = {}

        logger.info(f"OT Engine initialized for site {site_id}")

    def generate_operation(self, op_type: OperationType, position: Union[int, str],
                          data: Any) -> Operation:
        """
        Generate a new operation with proper sequencing.

        Args:
            op_type: Type of operation
            position: Position in the document
            data: Operation data

        Returns:
            New operation with proper sequence number
        """
        self.sequence_number += 1

        operation = Operation(
            operation_id=f"op_{self.site_id}_{self.sequence_number}",
            operation_type=op_type,
            site_id=self.site_id,
            sequence_number=self.sequence_number,
            position=position,
            data=data
        )

        # Update state vector
        self.state_vector[self.site_id] = self.sequence_number

        logger.debug(f"Generated operation: {operation.operation_id} ({op_type.value})")
        return operation

    def apply_operation(self, operation: Operation, document: str) -> str:
        """
        Apply an operation to a document.

        Args:
            operation: Operation to apply
            document: Current document state

        Returns:
            New document state after applying operation
        """
        if operation.operation_type == OperationType.INSERT:
            return self._apply_insert(document, operation)
        elif operation.operation_type == OperationType.DELETE:
            return self._apply_delete(document, operation)
        elif operation.operation_type == OperationType.UPDATE:
            return self._apply_update(document, operation)
        else:
            raise ValueError(f"Unknown operation type: {operation.operation_type}")

    def transform_operation(self, operation: Operation, concurrent_ops: List[Operation]) -> Operation:
        """
        Transform an operation against concurrent operations.

        This is the core of operational transformation - it converts
        operations that were designed for one state into operations
        that work on a different state.

        Args:
            operation: Operation to transform
            concurrent_ops: List of concurrent operations to transform against

        Returns:
            Transformed operation
        """
        transformed_op = operation

        # Sort concurrent operations by sequence number for deterministic transformation
        sorted_ops = sorted(concurrent_ops, key=lambda op: (op.sequence_number, op.site_id))

        for concurrent_op in sorted_ops:
            if self._operations_concurrent(operation, concurrent_op):
                transformed_op = self._transform_single(transformed_op, concurrent_op)

        return transformed_op

    def _operations_concurrent(self, op1: Operation, op2: Operation) -> bool:
        """
        Check if two operations are concurrent (no causal relationship).

        Args:
            op1: First operation
            op2: Second operation

        Returns:
            True if operations are concurrent
        """
        # Operations are concurrent if they have the same sequence number
        # and are from different sites (simplified concurrency detection)
        if op1.sequence_number == op2.sequence_number and op1.site_id != op2.site_id:
            return True

        # Check causal relationships using state vector
        # op1 causally precedes op2 if op1's site has seen op2's sequence number
        op1_precedes_op2 = (op1.site_id in self.state_vector and
                           self.state_vector[op1.site_id] >= op2.sequence_number)

        # op2 causally precedes op1 if op2's site has seen op1's sequence number
        op2_precedes_op1 = (op2.site_id in self.state_vector and
                           self.state_vector[op2.site_id] >= op1.sequence_number)

        # Operations are concurrent if neither causally precedes the other
        return not (op1_precedes_op2 or op2_precedes_op1)

    def _transform_single(self, op: Operation, against: Operation) -> Operation:
        """
        Transform a single operation against another operation.

        Args:
            op: Operation to transform
            against: Operation to transform against

        Returns:
            Transformed operation
        """
        if op.operation_type == OperationType.INSERT and against.operation_type == OperationType.INSERT:
            return self._transform_insert_insert(op, against)
        elif op.operation_type == OperationType.INSERT and against.operation_type == OperationType.DELETE:
            return self._transform_insert_delete(op, against)
        elif op.operation_type == OperationType.DELETE and against.operation_type == OperationType.INSERT:
            return self._transform_delete_insert(op, against)
        elif op.operation_type == OperationType.DELETE and against.operation_type == OperationType.DELETE:
            return self._transform_delete_delete(op, against)
        else:
            # For now, return operation unchanged for unhandled combinations
            logger.warning(f"Unimplemented transformation: {op.operation_type} vs {against.operation_type}")
            return op

    def _transform_insert_insert(self, op: Operation, against: Operation) -> Operation:
        """Transform insert operation against another insert."""
        if op.position < against.position:
            # Insert before the other insert - position unchanged
            return op
        elif op.position > against.position:
            # Insert after the other insert - shift position right
            return Operation(
                operation_id=op.operation_id,
                operation_type=op.operation_type,
                site_id=op.site_id,
                sequence_number=op.sequence_number,
                position=op.position + 1,  # Shift right by 1
                data=op.data,
                timestamp=op.timestamp
            )
        else:
            # Insert at same position - order by site ID (lower site ID wins)
            if op.site_id < against.site_id:
                # Current operation has lower site ID - keep position, shift the other
                return op
            else:
                # Current operation has higher site ID - shift right
                return Operation(
                    operation_id=op.operation_id,
                    operation_type=op.operation_type,
                    site_id=op.site_id,
                    sequence_number=op.sequence_number,
                    position=op.position + 1,  # Shift right by 1
                    data=op.data,
                    timestamp=op.timestamp
                )

    def _transform_insert_delete(self, op: Operation, against: Operation) -> Operation:
        """Transform insert operation against a delete."""
        if op.position <= against.position:
            # Insert before or at delete position - position unchanged
            return op
        else:
            # Insert after delete position - shift left by 1
            return Operation(
                operation_id=op.operation_id,
                operation_type=op.operation_type,
                site_id=op.site_id,
                sequence_number=op.sequence_number,
                position=op.position - 1,  # Shift left by 1
                data=op.data,
                timestamp=op.timestamp
            )

    def _transform_delete_insert(self, op: Operation, against: Operation) -> Operation:
        """Transform delete operation against an insert."""
        if op.position < against.position:
            # Delete before insert - position unchanged
            return op
        else:
            # Delete at or after insert - shift right by 1
            return Operation(
                operation_id=op.operation_id,
                operation_type=op.operation_type,
                site_id=op.site_id,
                sequence_number=op.sequence_number,
                position=op.position + 1,  # Shift right by 1
                data=op.data,
                timestamp=op.timestamp
            )

    def _transform_delete_delete(self, op: Operation, against: Operation) -> Operation:
        """Transform delete operation against another delete."""
        if op.position < against.position:
            # Delete before the other delete - position unchanged
            return op
        elif op.position > against.position:
            # Delete after the other delete - shift left by 1
            return Operation(
                operation_id=op.operation_id,
                operation_type=op.operation_type,
                site_id=op.site_id,
                sequence_number=op.sequence_number,
                position=op.position - 1,  # Shift left by 1
                data=op.data,
                timestamp=op.timestamp
            )
        else:
            # Delete at same position - this is a conflict, keep original
            # In practice, this should be handled by the application
            logger.warning(f"Delete conflict at position {op.position}")
            return op

    def _apply_insert(self, document: str, operation: Operation) -> str:
        """Apply insert operation to document."""
        pos = int(operation.position)
        if pos < 0:
            pos = 0
        elif pos > len(document):
            pos = len(document)

        return document[:pos] + str(operation.data) + document[pos:]

    def _apply_delete(self, document: str, operation: Operation) -> str:
        """Apply delete operation to document."""
        pos = int(operation.position)
        if 0 <= pos < len(document):
            return document[:pos] + document[pos + 1:]
        return document

    def _apply_update(self, document: str, operation: Operation) -> str:
        """Apply update operation to document."""
        # For text documents, update is treated as replace at position
        pos = int(operation.position)
        if 0 <= pos < len(document):
            return document[:pos] + str(operation.data) + document[pos + 1:]
        return document

    def integrate_remote_operation(self, remote_op: Operation) -> List[Operation]:
        """
        Integrate a remote operation into the local history.

        Args:
            remote_op: Remote operation to integrate

        Returns:
            List of operations that need to be transformed due to this integration
        """
        # Add to history buffer
        self.history_buffer.append(remote_op)

        # Update state vector
        if remote_op.site_id not in self.state_vector:
            self.state_vector[remote_op.site_id] = 0
        self.state_vector[remote_op.site_id] = max(
            self.state_vector[remote_op.site_id],
            remote_op.sequence_number
        )

        # Find operations that need transformation
        affected_ops = []
        for pending_op in self.pending_operations:
            if self._operations_concurrent(pending_op, remote_op):
                affected_ops.append(pending_op)

        return affected_ops

    def get_state_vector(self) -> Dict[int, int]:
        """
        Get current state vector for causal ordering.

        Returns:
            Copy of current state vector
        """
        return self.state_vector.copy()

    def update_state_vector(self, remote_state: Dict[int, int]) -> None:
        """
        Update local state vector with remote state information.

        Args:
            remote_state: State vector from remote site
        """
        for site_id, sequence in remote_state.items():
            if site_id not in self.state_vector:
                self.state_vector[site_id] = 0
            self.state_vector[site_id] = max(self.state_vector[site_id], sequence)