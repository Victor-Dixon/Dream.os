#!/usr/bin/env python3
"""
Synchronization Protocol - Real-time OT Communication
=====================================================

Real-time synchronization protocol for operational transformation.
Handles communication between replicas for conflict-free collaboration.

Key Components:
- SyncMessage: Structured messages for OT operations
- SyncProtocol: Protocol for exchanging operations and state
- Connection Management: Peer-to-peer and centralized sync
- Conflict Resolution: Automatic conflict detection and resolution

Enables real-time collaborative editing across distributed replicas.

Author: Agent-8 (SSOT & System Integration Specialist)
Date: 2026-01-11
"""

import asyncio
import logging
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Callable
from dataclasses import dataclass, field
from datetime import datetime
import json

from .ot_engine import Operation, OperationType
from .crdt_core import CRDTBase

logger = logging.getLogger(__name__)


class SyncMessageType(Enum):
    """Types of synchronization messages."""
    OPERATION = "operation"           # Individual operation broadcast
    STATE_VECTOR = "state_vector"     # State vector exchange
    CRDT_UPDATE = "crdt_update"       # CRDT state synchronization
    ACKNOWLEDGMENT = "acknowledgment" # Operation acknowledgment
    REQUEST_OPERATIONS = "request_ops" # Request missing operations
    BULK_OPERATIONS = "bulk_ops"      # Bulk operation transfer


@dataclass
class SyncMessage:
    """
    Structured message for operational transformation synchronization.

    Contains operation data, metadata, and routing information for
    real-time collaborative editing.
    """
    message_id: str
    message_type: SyncMessageType
    sender_site_id: int
    recipient_site_id: Optional[int]  # None for broadcast
    timestamp: datetime = field(default_factory=datetime.now)

    # Message payload
    operation: Optional[Operation] = None
    state_vector: Optional[Dict[int, int]] = None
    crdt_data: Optional[Dict[str, Any]] = None
    requested_operations: Optional[List[str]] = None
    bulk_operations: Optional[List[Operation]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary for transmission."""
        data = {
            'message_id': self.message_id,
            'message_type': self.message_type.value,
            'sender_site_id': self.sender_site_id,
            'recipient_site_id': self.recipient_site_id,
            'timestamp': self.timestamp.isoformat()
        }

        if self.operation:
            data['operation'] = self.operation.to_dict()
        if self.state_vector:
            data['state_vector'] = self.state_vector
        if self.crdt_data:
            data['crdt_data'] = self.crdt_data
        if self.requested_operations:
            data['requested_operations'] = self.requested_operations
        if self.bulk_operations:
            data['bulk_operations'] = [op.to_dict() for op in self.bulk_operations]

        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SyncMessage':
        """Create message from dictionary."""
        message = cls(
            message_id=data['message_id'],
            message_type=SyncMessageType(data['message_type']),
            sender_site_id=data['sender_site_id'],
            recipient_site_id=data['recipient_site_id'],
            timestamp=datetime.fromisoformat(data['timestamp'])
        )

        if 'operation' in data:
            message.operation = Operation.from_dict(data['operation'])
        if 'state_vector' in data:
            message.state_vector = data['state_vector']
        if 'crdt_data' in data:
            message.crdt_data = data['crdt_data']
        if 'requested_operations' in data:
            message.requested_operations = data['requested_operations']
        if 'bulk_operations' in data:
            message.bulk_operations = [Operation.from_dict(op) for op in data['bulk_operations']]

        return message


class SyncProtocol:
    """
    Operational Transformation Synchronization Protocol.

    Manages real-time communication between replicas for collaborative editing.
    Handles operation exchange, conflict resolution, and state synchronization.
    """

    def __init__(self, site_id: int, ot_engine: Any):
        """
        Initialize sync protocol.

        Args:
            site_id: Unique identifier for this site
            ot_engine: Operational transformation engine instance
        """
        self.site_id = site_id
        self.ot_engine = ot_engine

        # Connected peers (site_id -> connection_info)
        self.peers: Dict[int, Dict[str, Any]] = {}

        # Message handlers
        self.message_handlers: Dict[SyncMessageType, Callable] = {
            SyncMessageType.OPERATION: self._handle_operation_message,
            SyncMessageType.STATE_VECTOR: self._handle_state_vector_message,
            SyncMessageType.CRDT_UPDATE: self._handle_crdt_update_message,
            SyncMessageType.ACKNOWLEDGMENT: self._handle_acknowledgment_message,
            SyncMessageType.REQUEST_OPERATIONS: self._handle_request_operations_message,
            SyncMessageType.BULK_OPERATIONS: self._handle_bulk_operations_message,
        }

        # Operation queue for outgoing messages
        self.outgoing_queue: asyncio.Queue = asyncio.Queue()

        # Synchronization state
        self.is_running = False
        self.sync_task: Optional[asyncio.Task] = None

        logger.info(f"SyncProtocol initialized for site {site_id}")

    async def start(self) -> None:
        """Start the synchronization protocol."""
        if self.is_running:
            return

        self.is_running = True
        self.sync_task = asyncio.create_task(self._sync_loop())
        logger.info(f"Synchronization protocol started for site {self.site_id}")

    async def stop(self) -> None:
        """Stop the synchronization protocol."""
        self.is_running = False
        if self.sync_task:
            self.sync_task.cancel()
            try:
                await self.sync_task
            except asyncio.CancelledError:
                pass
        logger.info(f"Synchronization protocol stopped for site {self.site_id}")

    async def _sync_loop(self) -> None:
        """Main synchronization loop."""
        while self.is_running:
            try:
                # Process outgoing messages
                await self._process_outgoing_messages()

                # Check for peer synchronization
                await self._sync_with_peers()

                # Small delay to prevent busy waiting
                await asyncio.sleep(0.1)

            except Exception as e:
                logger.error(f"Error in sync loop: {e}")
                await asyncio.sleep(1.0)

    async def _process_outgoing_messages(self) -> None:
        """Process and send outgoing synchronization messages."""
        try:
            while not self.outgoing_queue.empty():
                message = self.outgoing_queue.get_nowait()
                await self._send_message(message)
        except Exception as e:
            logger.error(f"Error processing outgoing messages: {e}")

    async def _sync_with_peers(self) -> None:
        """Synchronize state with connected peers."""
        for peer_id, peer_info in self.peers.items():
            try:
                # Send state vector for causal ordering
                await self._send_state_vector(peer_id)

                # Check for missing operations
                await self._request_missing_operations(peer_id)

            except Exception as e:
                logger.error(f"Error syncing with peer {peer_id}: {e}")

    async def broadcast_operation(self, operation: Operation) -> None:
        """
        Broadcast an operation to all connected peers.

        Args:
            operation: Operation to broadcast
        """
        message = SyncMessage(
            message_id=f"op_broadcast_{operation.operation_id}",
            message_type=SyncMessageType.OPERATION,
            sender_site_id=self.site_id,
            recipient_site_id=None,  # Broadcast
            operation=operation
        )

        await self.outgoing_queue.put(message)
        logger.debug(f"Broadcasting operation: {operation.operation_id}")

    async def send_operation(self, operation: Operation, target_site: int) -> None:
        """
        Send an operation to a specific site.

        Args:
            operation: Operation to send
            target_site: Target site ID
        """
        message = SyncMessage(
            message_id=f"op_direct_{operation.operation_id}",
            message_type=SyncMessageType.OPERATION,
            sender_site_id=self.site_id,
            recipient_site_id=target_site,
            operation=operation
        )

        await self.outgoing_queue.put(message)

    async def receive_message(self, message: SyncMessage) -> None:
        """
        Receive and process an incoming synchronization message.

        Args:
            message: Incoming sync message
        """
        try:
            handler = self.message_handlers.get(message.message_type)
            if handler:
                await handler(message)
            else:
                logger.warning(f"No handler for message type: {message.message_type}")
        except Exception as e:
            logger.error(f"Error processing message {message.message_id}: {e}")

    async def _handle_operation_message(self, message: SyncMessage) -> None:
        """Handle incoming operation message."""
        if not message.operation:
            return

        logger.debug(f"Received operation: {message.operation.operation_id}")

        # Integrate remote operation
        affected_ops = self.ot_engine.integrate_remote_operation(message.operation)

        # Transform affected pending operations
        for affected_op in affected_ops:
            transformed_op = self.ot_engine.transform_operation(affected_op, [message.operation])
            # Update the pending operation with transformed version
            # (In practice, this would update the operation in the pending queue)

        # Send acknowledgment
        await self._send_acknowledgment(message.message_id, message.sender_site_id)

    async def _handle_state_vector_message(self, message: SyncMessage) -> None:
        """Handle incoming state vector message."""
        if not message.state_vector:
            return

        logger.debug(f"Received state vector from site {message.sender_site_id}")

        # Update local state vector
        self.ot_engine.update_state_vector(message.state_vector)

    async def _handle_crdt_update_message(self, message: SyncMessage) -> None:
        """Handle incoming CRDT update message."""
        if not message.crdt_data:
            return

        logger.debug(f"Received CRDT update from site {message.sender_site_id}")

        # CRDT merging would happen here
        # (Implementation depends on specific CRDT types being used)

    async def _handle_acknowledgment_message(self, message: SyncMessage) -> None:
        """Handle operation acknowledgment."""
        logger.debug(f"Received acknowledgment for message: {message.message_id}")

        # Mark operation as acknowledged
        # (In practice, this would update delivery tracking)

    async def _handle_request_operations_message(self, message: SyncMessage) -> None:
        """Handle request for missing operations."""
        if not message.requested_operations:
            return

        logger.debug(f"Received request for {len(message.requested_operations)} operations")

        # Find and send requested operations
        operations_to_send = []
        for op_id in message.requested_operations:
            # Look up operation in history (implementation depends on storage)
            # operations_to_send.append(found_operation)
            pass

        if operations_to_send:
            bulk_message = SyncMessage(
                message_id=f"bulk_ops_{message.message_id}",
                message_type=SyncMessageType.BULK_OPERATIONS,
                sender_site_id=self.site_id,
                recipient_site_id=message.sender_site_id,
                bulk_operations=operations_to_send
            )
            await self.outgoing_queue.put(bulk_message)

    async def _handle_bulk_operations_message(self, message: SyncMessage) -> None:
        """Handle bulk operations message."""
        if not message.bulk_operations:
            return

        logger.debug(f"Received {len(message.bulk_operations)} bulk operations")

        # Process each operation
        for operation in message.bulk_operations:
            await self.receive_message(SyncMessage(
                message_id=f"bulk_op_{operation.operation_id}",
                message_type=SyncMessageType.OPERATION,
                sender_site_id=message.sender_site_id,
                recipient_site_id=self.site_id,
                operation=operation
            ))

    async def _send_state_vector(self, target_site: int) -> None:
        """Send current state vector to target site."""
        state_vector = self.ot_engine.get_state_vector()

        message = SyncMessage(
            message_id=f"state_vector_{self.site_id}_{target_site}",
            message_type=SyncMessageType.STATE_VECTOR,
            sender_site_id=self.site_id,
            recipient_site_id=target_site,
            state_vector=state_vector
        )

        await self.outgoing_queue.put(message)

    async def _request_missing_operations(self, target_site: int) -> None:
        """Request missing operations from target site."""
        # Compare state vectors to find missing operations
        local_state = self.ot_engine.get_state_vector()

        # This would compare with known remote state vectors
        # For now, this is a placeholder for the logic

        missing_ops = []  # Would be calculated based on state vector comparison

        if missing_ops:
            message = SyncMessage(
                message_id=f"request_ops_{self.site_id}_{target_site}",
                message_type=SyncMessageType.REQUEST_OPERATIONS,
                sender_site_id=self.site_id,
                recipient_site_id=target_site,
                requested_operations=missing_ops
            )
            await self.outgoing_queue.put(message)

    async def _send_acknowledgment(self, original_message_id: str, target_site: int) -> None:
        """Send acknowledgment for received message."""
        message = SyncMessage(
            message_id=f"ack_{original_message_id}",
            message_type=SyncMessageType.ACKNOWLEDGMENT,
            sender_site_id=self.site_id,
            recipient_site_id=target_site
        )

        await self.outgoing_queue.put(message)

    async def _send_message(self, message: SyncMessage) -> None:
        """
        Send message to appropriate destination.

        Args:
            message: Message to send
        """
        # This would implement the actual network transport
        # For now, it's a placeholder that logs the message

        logger.info(f"Sending {message.message_type.value} message to site {message.recipient_site_id}")
        logger.debug(f"Message content: {message.to_dict()}")

        # In a real implementation, this would:
        # - Serialize the message
        # - Send via network transport (WebSocket, HTTP, etc.)
        # - Handle delivery confirmations

    def add_peer(self, site_id: int, connection_info: Dict[str, Any]) -> None:
        """
        Add a peer site for synchronization.

        Args:
            site_id: Site ID of the peer
            connection_info: Connection information for the peer
        """
        self.peers[site_id] = connection_info
        logger.info(f"Added peer site {site_id} for synchronization")

    def remove_peer(self, site_id: int) -> None:
        """
        Remove a peer site from synchronization.

        Args:
            site_id: Site ID to remove
        """
        if site_id in self.peers:
            del self.peers[site_id]
            logger.info(f"Removed peer site {site_id} from synchronization")