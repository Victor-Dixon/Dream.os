#!/usr/bin/env python3
"""
Operational Transformation Router - Phase 4 Sprint 4
==================================================

FastAPI router for operational transformation collaborative editing.

<!-- SSOT Domain: collaboration -->

Navigation References:
├── Related Files:
│   ├── OT Engine → src/services/operational_transformation_engine.py
│   ├── WebSocket → src/services/ai_context_websocket.py
│   ├── FastAPI App → src/web/fastapi_app.py
│   └── Frontend Integration → src/web/static/js/operational-transformation.js
├── Documentation:
│   ├── Phase 4 Roadmap → PHASE4_STRATEGIC_ROADMAP.md
│   ├── API Docs → docs/api/operational_transformation_api.md
│   └── Real-time Guide → docs/collaboration/realtime_editing_guide.md
└── Testing:
    └── Integration Tests → tests/integration/test_operational_transformation_api.py

Endpoints:
- POST /api/ot/sessions - Create collaborative session
- GET /api/ot/sessions/{session_id} - Get session info
- DELETE /api/ot/sessions/{session_id} - Delete session
- GET /api/ot/sessions/{session_id}/state - Get document state
- GET /api/ot/stats - Get performance statistics
- POST /api/ot/sessions/{session_id}/export - Export session data

Author: Agent-6 (Web Architecture Lead)
Date: 2026-01-08
Phase: Phase 4 Sprint 4 - Operational Transformation Engine
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
import json
import time
from datetime import datetime

from src.services.operational_transformation_engine import operational_transformation_engine

router = APIRouter(prefix="/api/ot", tags=["operational-transformation"])


# Pydantic Models
class CreateSessionRequest(BaseModel):
    """Request model for creating a collaborative session."""
    session_id: str = Field(..., description="Unique session identifier")
    initial_content: str = Field(default="", description="Initial document content")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Session metadata")


class SessionInfo(BaseModel):
    """Response model for session information."""
    session_id: str
    version: int
    active_clients: List[str]
    last_modified: float
    operation_count: int
    metadata: Dict[str, Any]


class DocumentState(BaseModel):
    """Response model for document state."""
    session_id: str
    content: str
    version: int
    checksum: str
    last_modified: float
    active_clients: List[str]


class PerformanceStats(BaseModel):
    """Response model for performance statistics."""
    total_operations: int
    conflicts_resolved: int
    average_transform_time: float
    sync_operations: int
    active_sessions: int
    total_clients: int
    queue_sizes: Dict[str, int]
    timestamp: float


@router.post("/sessions", response_model=SessionInfo)
async def create_session(request: CreateSessionRequest):
    """
    Create a new collaborative editing session.

    - **session_id**: Unique identifier for the session
    - **initial_content**: Starting content for the document
    - **metadata**: Additional session metadata
    """
    try:
        # Create the document session
        document = operational_transformation_engine.create_document_session(
            request.session_id,
            request.initial_content
        )

        # Add metadata
        document.metadata = request.metadata

        return SessionInfo(
            session_id=document.session_id,
            version=document.version,
            active_clients=list(document.active_clients),
            last_modified=document.last_modified,
            operation_count=len(document.operation_history),
            metadata=document.metadata
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create session: {str(e)}")


@router.get("/sessions/{session_id}", response_model=SessionInfo)
async def get_session_info(session_id: str):
    """
    Get information about a collaborative session.

    - **session_id**: Session identifier
    """
    document = operational_transformation_engine.get_document_state(session_id)
    if not document:
        raise HTTPException(status_code=404, detail=f"Session {session_id} not found")

    return SessionInfo(
        session_id=document.session_id,
        version=document.version,
        active_clients=list(document.active_clients),
        last_modified=document.last_modified,
        operation_count=len(document.operation_history),
        metadata=getattr(document, 'metadata', {})
    )


@router.delete("/sessions/{session_id}")
async def delete_session(session_id: str):
    """
    Delete a collaborative session.

    - **session_id**: Session identifier to delete
    """
    if session_id not in operational_transformation_engine.documents:
        raise HTTPException(status_code=404, detail=f"Session {session_id} not found")

    try:
        # Remove from all data structures
        if session_id in operational_transformation_engine.documents:
            del operational_transformation_engine.documents[session_id]
        if session_id in operational_transformation_engine.operation_queues:
            del operational_transformation_engine.operation_queues[session_id]
        if session_id in operational_transformation_engine.session_clients:
            # Remove all clients from this session
            clients = operational_transformation_engine.session_clients[session_id].copy()
            for client_id in clients:
                operational_transformation_engine.leave_session(session_id, client_id)
            del operational_transformation_engine.session_clients[session_id]

        return {"message": f"Session {session_id} deleted successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete session: {str(e)}")


@router.get("/sessions/{session_id}/state", response_model=DocumentState)
async def get_document_state(session_id: str):
    """
    Get the current state of a collaborative document.

    - **session_id**: Session identifier
    """
    document = operational_transformation_engine.get_document_state(session_id)
    if not document:
        raise HTTPException(status_code=404, detail=f"Session {session_id} not found")

    return DocumentState(
        session_id=document.session_id,
        content=document.content,
        version=document.version,
        checksum=document.get_content_checksum(),
        last_modified=document.last_modified,
        active_clients=list(document.active_clients)
    )


@router.get("/sessions", response_model=List[SessionInfo])
async def list_sessions():
    """
    List all active collaborative sessions.
    """
    sessions = []
    for session_id, document in operational_transformation_engine.documents.items():
        sessions.append(SessionInfo(
            session_id=document.session_id,
            version=document.version,
            active_clients=list(document.active_clients),
            last_modified=document.last_modified,
            operation_count=len(document.operation_history),
            metadata=getattr(document, 'metadata', {})
        ))

    return sessions


@router.get("/stats", response_model=PerformanceStats)
async def get_performance_stats():
    """
    Get operational transformation engine performance statistics.
    """
    stats = operational_transformation_engine.get_performance_stats()
    return PerformanceStats(**stats, timestamp=time.time())


@router.post("/sessions/{session_id}/export")
async def export_session_data(session_id: str, background_tasks: BackgroundTasks):
    """
    Export complete session data including operation history.

    - **session_id**: Session identifier to export
    """
    document = operational_transformation_engine.get_document_state(session_id)
    if not document:
        raise HTTPException(status_code=404, detail=f"Session {session_id} not found")

    try:
        export_data = {
            "session_id": document.session_id,
            "content": document.content,
            "version": document.version,
            "checksum": document.get_content_checksum(),
            "last_modified": document.last_modified,
            "active_clients": list(document.active_clients),
            "operation_history": [op.to_dict() for op in document.operation_history],
            "metadata": getattr(document, 'metadata', {}),
            "export_timestamp": time.time(),
            "export_version": "1.0"
        }

        # In a real implementation, you might save this to a file or database
        # For now, return as JSON response
        return JSONResponse(
            content=export_data,
            media_type="application/json",
            headers={"Content-Disposition": f"attachment; filename={session_id}_export.json"}
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to export session: {str(e)}")


@router.get("/health")
async def health_check():
    """
    Health check endpoint for operational transformation service.
    """
    try:
        stats = operational_transformation_engine.get_performance_stats()
        return {
            "status": "healthy",
            "engine_running": operational_transformation_engine.running,
            "active_sessions": stats["active_sessions"],
            "total_clients": stats["total_clients"],
            "timestamp": time.time()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": time.time()
        }


# WebSocket endpoint information for clients
@router.get("/ws-info")
async def websocket_info():
    """
    Get WebSocket endpoint information for clients.
    """
    return {
        "websocket_url": "ws://localhost:8766/ws/ai/collaboration",
        "supported_message_types": [
            "join_session",
            "operation",
            "sync_request",
            "leave_session",
            "ping"
        ],
        "operation_types": ["insert", "delete", "update", "replace"],
        "features": [
            "real_time_collaborative_editing",
            "operational_transformation",
            "conflict_resolution",
            "automatic_sync"
        ],
        "protocol_version": "1.0"
    }