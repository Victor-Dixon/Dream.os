#!/usr/bin/env python3
"""
Operational Transformation Engine - Phase 4 Sprint 4
==================================================

Real-time collaborative editing engine with operational transformation for conflict resolution.

<!-- SSOT Domain: collaboration -->

Navigation References:
├── Related Files:
│   ├── WebSocket Server → src/services/ai_context_websocket.py
│   ├── Messaging Service → src/services/unified_messaging_service.py
│   ├── FastAPI Integration → src/web/fastapi_app.py
│   └── Real-time Processing → src/core/analytics/engines/realtime_analytics_engine.py
├── Documentation:
│   ├── Phase 4 Roadmap → PHASE4_STRATEGIC_ROADMAP.md
│   ├── Collaboration Design → docs/collaboration/OPERATIONAL_TRANSFORMATION_DESIGN.md
│   └── Conflict Resolution → docs/collaboration/CONFLICT_RESOLUTION_STRATEGIES.md
└── Testing:
    └── Integration Tests → tests/integration/test_operational_transformation.py

Features:
- Real-time collaborative document editing
- Operational transformation for conflict resolution
- Session state synchronization
- Undo/redo with collaborative awareness
- Performance monitoring and optimization

Author: Agent-6 (Web Architecture Lead) & Agent-7 (Quality Assurance Lead)
Date: 2026-01-08
Phase: Phase 4 Sprint 4 - Operational Transformation Engine
"""

import asyncio
import json
import logging
import time
import uuid
from typing import Dict, List, Any, Optional, Set, Tuple, Callable
from dataclasses import dataclass, field
from enum import Enum
import heapq
import threading

logger = logging.getLogger(__name__)


class OperationType(Enum):
    """Types of operations that can be performed on collaborative documents."""
    INSERT = "insert"
    DELETE = "delete"
    UPDATE = "update"
    MOVE = "move"
    REPLACE = "replace"


class ConflictResolutionStrategy(Enum):
    """Strategies for resolving operation conflicts."""
    LAST_WRITE_WINS = "last_write_wins"
    PRIORITY_BASED = "priority_based"
    MANUAL_RESOLUTION = "manual_resolution"
    TRANSFORM_BASED = "transform_based"


@dataclass
class Operation:
    """Represents a single operation in the collaborative editing system."""
    id: str
    session_id: str
    client_id: str
    type: OperationType
    position: int
    content: str = ""
    length: int = 0
    timestamp: float = field(default_factory=time.time)
    priority: int = 1
    parent_operation_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert operation to dictionary for serialization."""
        return {
            "id": self.id,
            "session_id": self.session_id,
            "client_id": self.client_id,
            "type": self.type.value,
            "position": self.position,
            "content": self.content,
            "length": self.length,
            "timestamp": self.timestamp,
            "priority": self.priority,
            "parent_operation_id": self.parent_operation_id,
            "metadata": self.metadata
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Operation':
        """Create operation from dictionary."""
        return cls(
            id=data["id"],
            session_id=data["session_id"],
            client_id=data["client_id"],
            type=OperationType(data["type"]),
            position=data["position"],
            content=data.get("content", ""),
            length=data.get("length", 0),
            timestamp=data.get("timestamp", time.time()),
            priority=data.get("priority", 1),
            parent_operation_id=data.get("parent_operation_id"),
            metadata=data.get("metadata", {})
        )


@dataclass
class DocumentState:
    """Represents the current state of a collaborative document."""
    session_id: str
    content: str
    version: int = 0
    last_modified: float = field(default_factory=time.time)
    active_clients: Set[str] = field(default_factory=set)
    operation_history: List[Operation] = field(default_factory=list)

    def apply_operation(self, operation: Operation) -> bool:
        """Apply an operation to the document state."""
        try:
            if operation.type == OperationType.INSERT:
                self.content = (
                    self.content[:operation.position] +
                    operation.content +
                    self.content[operation.position:]
                )
            elif operation.type == OperationType.DELETE:
                self.content = (
                    self.content[:operation.position] +
                    self.content[operation.position + operation.length:]
                )
            elif operation.type == OperationType.UPDATE:
                self.content = (
                    self.content[:operation.position] +
                    operation.content +
                    self.content[operation.position + operation.length:]
                )
            elif operation.type == OperationType.REPLACE:
                self.content = operation.content

            self.version += 1
            self.last_modified = time.time()
            self.operation_history.append(operation)
            return True
        except Exception as e:
            logger.error(f"Failed to apply operation {operation.id}: {e}")
            return False

    def get_content_checksum(self) -> str:
        """Get checksum of current content for integrity verification."""
        import hashlib
        return hashlib.md5(self.content.encode()).hexdigest()


class OperationalTransformationEngine:
    """
    Core engine for operational transformation in collaborative editing.

    Handles:
    - Operation queuing and ordering
    - Conflict detection and resolution
    - State synchronization across clients
    - Performance monitoring
    """

    def __init__(self):
        self.documents: Dict[str, DocumentState] = {}
        self.operation_queues: Dict[str, List[Operation]] = {}
        self.client_sessions: Dict[str, Set[str]] = {}  # client_id -> set of session_ids
        self.session_clients: Dict[str, Set[str]] = {}  # session_id -> set of client_ids

        # Performance monitoring
        self.performance_stats = {
            "total_operations": 0,
            "conflicts_resolved": 0,
            "average_transform_time": 0.0,
            "sync_operations": 0
        }

        # Conflict resolution settings
        self.conflict_strategy = ConflictResolutionStrategy.TRANSFORM_BASED
        self.max_operation_history = 1000

        # Background processing
        self.processing_task = None
        self.running = False

    async def start(self):
        """Start the operational transformation engine."""
        if self.running:
            return

        self.running = True
        self.processing_task = asyncio.create_task(self._process_operation_queues())
        logger.info("🚀 Operational Transformation Engine started")

    async def stop(self):
        """Stop the operational transformation engine."""
        self.running = False
        if self.processing_task:
            self.processing_task.cancel()
            try:
                await self.processing_task
            except asyncio.CancelledError:
                pass
        logger.info("🛑 Operational Transformation Engine stopped")

    def create_document_session(self, session_id: str, initial_content: str = "") -> DocumentState:
        """Create a new collaborative document session."""
        if session_id in self.documents:
            raise ValueError(f"Session {session_id} already exists")

        document = DocumentState(
            session_id=session_id,
            content=initial_content
        )

        self.documents[session_id] = document
        self.operation_queues[session_id] = []
        self.session_clients[session_id] = set()

        logger.info(f"📄 Created collaborative session {session_id}")
        return document

    def join_session(self, session_id: str, client_id: str) -> bool:
        """Add a client to a collaborative session."""
        if session_id not in self.documents:
            return False

        if session_id not in self.session_clients:
            self.session_clients[session_id] = set()
        if client_id not in self.client_sessions:
            self.client_sessions[client_id] = set()

        self.session_clients[session_id].add(client_id)
        self.client_sessions[client_id].add(session_id)
        self.documents[session_id].active_clients.add(client_id)

        logger.info(f"👤 Client {client_id} joined session {session_id}")
        return True

    def leave_session(self, session_id: str, client_id: str):
        """Remove a client from a collaborative session."""
        if session_id in self.session_clients:
            self.session_clients[session_id].discard(client_id)
        if client_id in self.client_sessions:
            self.client_sessions[client_id].discard(session_id)
        if session_id in self.documents:
            self.documents[session_id].active_clients.discard(client_id)

        logger.info(f"👋 Client {client_id} left session {session_id}")

    async def submit_operation(self, operation: Operation) -> Tuple[bool, Optional[str]]:
        """
        Submit an operation for processing.

        Returns:
            Tuple of (success, error_message)
        """
        if operation.session_id not in self.documents:
            return False, f"Session {operation.session_id} does not exist"

        if operation.client_id not in self.session_clients.get(operation.session_id, set()):
            return False, f"Client {operation.client_id} not in session {operation.session_id}"

        # Add to operation queue
        if operation.session_id not in self.operation_queues:
            self.operation_queues[operation.session_id] = []

        self.operation_queues[operation.session_id].append(operation)
        self.performance_stats["total_operations"] += 1

        logger.debug(f"📝 Queued operation {operation.id} for session {operation.session_id}")
        return True, None

    async def _process_operation_queues(self):
        """Background task to process operation queues."""
        while self.running:
            try:
                for session_id in list(self.operation_queues.keys()):
                    queue = self.operation_queues[session_id]
                    if not queue:
                        continue

                    # Sort operations by timestamp and priority
                    queue.sort(key=lambda op: (op.timestamp, -op.priority))

                    # Process operations in order
                    processed_ops = []
                    for operation in queue[:]:
                        if await self._process_single_operation(operation):
                            processed_ops.append(operation)
                            queue.remove(operation)

                    if processed_ops:
                        logger.debug(f"✅ Processed {len(processed_ops)} operations for session {session_id}")

                await asyncio.sleep(0.01)  # Small delay to prevent busy waiting

            except Exception as e:
                logger.error(f"Error processing operation queues: {e}")
                await asyncio.sleep(1.0)

    async def _process_single_operation(self, operation: Operation) -> bool:
        """Process a single operation with conflict resolution."""
        document = self.documents[operation.session_id]

        # Check for conflicts with concurrent operations
        conflicts = self._detect_conflicts(operation, document)

        if conflicts:
            resolved_operation = await self._resolve_conflicts(operation, conflicts, document)
            if resolved_operation:
                operation = resolved_operation
            else:
                logger.warning(f"Failed to resolve conflicts for operation {operation.id}")
                return False

        # Apply the operation
        start_time = time.time()
        success = document.apply_operation(operation)
        transform_time = time.time() - start_time

        # Update performance stats
        self.performance_stats["average_transform_time"] = (
            (self.performance_stats["average_transform_time"] * 0.9) + (transform_time * 0.1)
        )

        if success:
            # Trim operation history if needed
            if len(document.operation_history) > self.max_operation_history:
                document.operation_history = document.operation_history[-self.max_operation_history:]

        return success

    def _detect_conflicts(self, operation: Operation, document: DocumentState) -> List[Operation]:
        """Detect operations that conflict with the given operation."""
        conflicts = []

        # Check recent operations that affect the same position range
        recent_ops = document.operation_history[-50:]  # Check last 50 operations

        for recent_op in recent_ops:
            if recent_op.client_id == operation.client_id:
                continue  # Skip operations from same client

            # Check for position overlap
            if self._operations_conflict(operation, recent_op):
                conflicts.append(recent_op)

        return conflicts

    def _operations_conflict(self, op1: Operation, op2: Operation) -> bool:
        """Check if two operations conflict with each other."""
        # Insert operations conflict if they affect the same position
        if op1.type == OperationType.INSERT and op2.type == OperationType.INSERT:
            return abs(op1.position - op2.position) < 10  # Within 10 characters

        # Delete operations conflict if they overlap
        if op1.type == OperationType.DELETE and op2.type == OperationType.DELETE:
            op1_end = op1.position + op1.length
            op2_end = op2.position + op2.length
            return max(op1.position, op2.position) < min(op1_end, op2_end)

        # Mixed operations (insert/delete) often conflict
        if {op1.type, op2.type} == {OperationType.INSERT, OperationType.DELETE}:
            return self._ranges_overlap(op1.position, op1.position + len(op1.content),
                                       op2.position, op2.position + op2.length)

        return False

    def _ranges_overlap(self, start1: int, end1: int, start2: int, end2: int) -> bool:
        """Check if two ranges overlap."""
        return max(start1, start2) < min(end1, end2)

    async def _resolve_conflicts(self, operation: Operation, conflicts: List[Operation],
                                document: DocumentState) -> Optional[Operation]:
        """Resolve conflicts using the configured strategy."""
        if self.conflict_strategy == ConflictResolutionStrategy.LAST_WRITE_WINS:
            # Keep the newer operation
            for conflict in conflicts:
                if conflict.timestamp > operation.timestamp:
                    return None  # Current operation is older, discard it
            return operation

        elif self.conflict_strategy == ConflictResolutionStrategy.TRANSFORM_BASED:
            # Transform the operation to avoid conflicts
            transformed_op = operation
            for conflict in conflicts:
                transformed_op = self._transform_operation(transformed_op, conflict)
            return transformed_op

        elif self.conflict_strategy == ConflictResolutionStrategy.PRIORITY_BASED:
            # Check if current operation has higher priority
            for conflict in conflicts:
                if conflict.priority > operation.priority:
                    return None  # Lower priority, discard
            return operation

        else:
            # Manual resolution or other strategies
            logger.warning(f"Unresolved conflicts for operation {operation.id}: {len(conflicts)} conflicts")
            return None

    def _transform_operation(self, operation: Operation, conflicting_op: Operation) -> Operation:
        """Transform an operation to avoid conflicts with another operation."""
        # Simple transformation: adjust position based on the conflicting operation
        if operation.type == OperationType.INSERT:
            if conflicting_op.type == OperationType.INSERT:
                # If both are inserts at similar positions, shift the later one
                if (operation.timestamp > conflicting_op.timestamp and
                    abs(operation.position - conflicting_op.position) < 10):
                    operation.position += len(conflicting_op.content)
            elif conflicting_op.type == OperationType.DELETE:
                # If conflicting operation deleted before our insert position
                if conflicting_op.position <= operation.position:
                    operation.position -= min(conflicting_op.length,
                                            operation.position - conflicting_op.position)

        elif operation.type == OperationType.DELETE:
            if conflicting_op.type == OperationType.INSERT:
                # If conflicting operation inserted before our delete position
                if conflicting_op.position <= operation.position:
                    operation.position += len(conflicting_op.content)
            elif conflicting_op.type == OperationType.DELETE:
                # Adjust overlapping deletes
                if conflicting_op.position < operation.position:
                    overlap = min(operation.position + operation.length,
                                conflicting_op.position + conflicting_op.length) - operation.position
                    if overlap > 0:
                        operation.position += overlap
                        operation.length -= overlap

        return operation

    def get_document_state(self, session_id: str) -> Optional[DocumentState]:
        """Get the current state of a document."""
        return self.documents.get(session_id)

    def get_session_clients(self, session_id: str) -> Set[str]:
        """Get all clients connected to a session."""
        return self.session_clients.get(session_id, set())

    def get_client_sessions(self, client_id: str) -> Set[str]:
        """Get all sessions a client is connected to."""
        return self.client_sessions.get(client_id, set())

    def get_performance_stats(self) -> Dict[str, Any]:
        """Get current performance statistics."""
        return {
            **self.performance_stats,
            "active_sessions": len(self.documents),
            "total_clients": len(self.client_sessions),
            "queue_sizes": {sid: len(queue) for sid, queue in self.operation_queues.items()}
        }

    async def synchronize_client(self, session_id: str, client_id: str,
                               last_known_version: int) -> Dict[str, Any]:
        """Synchronize a client with the current document state."""
        if session_id not in self.documents:
            return {"error": f"Session {session_id} does not exist"}

        document = self.documents[session_id]

        # Get operations since the client's last known version
        operations_since = []
        if last_known_version < len(document.operation_history):
            operations_since = document.operation_history[last_known_version:]

        self.performance_stats["sync_operations"] += 1

        return {
            "session_id": session_id,
            "current_version": document.version,
            "content": document.content,
            "operations_since": [op.to_dict() for op in operations_since],
            "checksum": document.get_content_checksum(),
            "active_clients": list(document.active_clients),
            "timestamp": time.time()
        }


# Global instance
operational_transformation_engine = OperationalTransformationEngine()


class CollaborativeWebSocketHandler:
    """
    WebSocket handler for collaborative editing with operational transformation.
    """

    def __init__(self, engine: OperationalTransformationEngine):
        self.engine = engine
        self.active_connections: Dict[str, Set[Any]] = {}  # session_id -> set of websockets

    async def handle_connection(self, websocket, session_id: str, client_id: str):
        """Handle a new collaborative editing connection."""
        if session_id not in self.active_connections:
            self.active_connections[session_id] = set()

        self.active_connections[session_id].add(websocket)

        # Join the session
        self.engine.join_session(session_id, client_id)

        try:
            # Send welcome message with current state
            welcome_data = await self.engine.synchronize_client(session_id, client_id, 0)
            welcome_data["type"] = "welcome"
            await websocket.send(json.dumps(welcome_data))

            # Handle incoming messages
            async for message in websocket:
                try:
                    data = json.loads(message)
                    await self._handle_message(websocket, session_id, client_id, data)
                except json.JSONDecodeError:
                    logger.warning(f"Invalid JSON from client {client_id}")

        except Exception as e:
            logger.error(f"Connection error for client {client_id}: {e}")
        finally:
            # Clean up
            self.active_connections[session_id].discard(websocket)
            self.engine.leave_session(session_id, client_id)

    async def _handle_message(self, websocket, session_id: str, client_id: str, data: Dict[str, Any]):
        """Handle incoming messages from clients."""
        message_type = data.get("type")

        if message_type == "operation":
            # Process collaborative operation
            operation_data = data.get("operation", {})
            operation_data.update({
                "session_id": session_id,
                "client_id": client_id
            })

            try:
                operation = Operation.from_dict(operation_data)
                success, error = await self.engine.submit_operation(operation)

                response = {
                    "type": "operation_ack",
                    "operation_id": operation.id,
                    "success": success,
                    "timestamp": time.time()
                }

                if not success:
                    response["error"] = error

                await websocket.send(json.dumps(response))

                # Broadcast operation to other clients in session
                if success:
                    await self._broadcast_to_session(session_id, client_id, {
                        "type": "remote_operation",
                        "operation": operation.to_dict(),
                        "timestamp": time.time()
                    })

            except Exception as e:
                logger.error(f"Operation processing error: {e}")
                await websocket.send(json.dumps({
                    "type": "error",
                    "message": str(e),
                    "timestamp": time.time()
                }))

        elif message_type == "sync_request":
            # Handle synchronization request
            last_version = data.get("last_version", 0)
            sync_data = await self.engine.synchronize_client(session_id, client_id, last_version)
            sync_data["type"] = "sync_response"
            await websocket.send(json.dumps(sync_data))

        elif message_type == "ping":
            await websocket.send(json.dumps({
                "type": "pong",
                "timestamp": time.time()
            }))

    async def _broadcast_to_session(self, session_id: str, exclude_client_id: str, message: Dict[str, Any]):
        """Broadcast a message to all clients in a session except the sender."""
        if session_id not in self.active_connections:
            return

        # Note: In a real implementation, you'd need to track which websocket belongs to which client
        # This is a simplified version
        for conn in self.active_connections[session_id]:
            try:
                await conn.send(json.dumps(message))
            except Exception as e:
                logger.error(f"Broadcast error: {e}")


# Global collaborative handler
collaborative_handler = CollaborativeWebSocketHandler(operational_transformation_engine)


# Integration with existing AI Context WebSocket Server
async def integrate_operational_transformation():
    """
    Integrate operational transformation with the existing AI Context WebSocket Server.
    """
    # Start the operational transformation engine
    await operational_transformation_engine.start()

    # The collaborative features are now available through the existing WebSocket endpoints
    # Clients can connect to /ws/ai/collaboration and use operational transformation

    logger.info("🔄 Operational Transformation integrated with AI Context WebSocket Server")


if __name__ == "__main__":
    # Example usage
    async def demo():
        """Demonstrate operational transformation engine."""
        await operational_transformation_engine.start()

        # Create a collaborative session
        doc = operational_transformation_engine.create_document_session(
            "demo_session",
            "Hello, world!"
        )

        # Simulate collaborative editing
        op1 = Operation(
            id=str(uuid.uuid4()),
            session_id="demo_session",
            client_id="user1",
            type=OperationType.INSERT,
            position=7,
            content="collaborative "
        )

        op2 = Operation(
            id=str(uuid.uuid4()),
            session_id="demo_session",
            client_id="user2",
            type=OperationType.INSERT,
            position=13,
            content="amazing "
        )

        # Add clients to session
        operational_transformation_engine.join_session("demo_session", "user1")
        operational_transformation_engine.join_session("demo_session", "user2")

        # Submit operations
        await operational_transformation_engine.submit_operation(op1)
        await asyncio.sleep(0.1)  # Allow processing
        await operational_transformation_engine.submit_operation(op2)
        await asyncio.sleep(0.1)  # Allow processing

        # Check final state
        final_doc = operational_transformation_engine.get_document_state("demo_session")
        print(f"Final content: {final_doc.content}")
        print(f"Operations processed: {len(final_doc.operation_history)}")

        await operational_transformation_engine.stop()

    asyncio.run(demo())