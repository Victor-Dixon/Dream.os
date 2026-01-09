#!/usr/bin/env python3
"""
Repository Monitor Router - Phase 4 Continuous Scanning
======================================================

FastAPI router for repository monitoring and analytics.

<!-- SSOT Domain: monitoring -->

Navigation References:
├── Related Files:
│   ├── Monitor Service → src/services/repository_monitor.py
│   ├── FastAPI App → src/web/fastapi_app.py
│   ├── Dashboard Integration → src/web/static/js/repository-monitor.js
│   └── Analytics Engine → src/core/analytics/engines/realtime_analytics_engine.py
├── Documentation:
│   ├── Phase 4 Roadmap → PHASE4_STRATEGIC_ROADMAP.md
│   ├── Monitor Guide → docs/monitoring/repository_monitoring.md
│   └── Analytics Spec → PHASE_5_2_ADVANCED_ANALYTICS_SPEC.md
└── Testing:
    └── Integration Tests → tests/integration/test_repository_monitor_api.py

Endpoints:
- GET /monitor/stats - Get current repository statistics
- GET /monitor/trends/{hours} - Get trend analysis for time window
- GET /monitor/snapshots - List available snapshots
- GET /monitor/snapshots/{index} - Get specific snapshot
- POST /monitor/scan - Trigger manual scan
- GET /monitor/export - Export monitoring data
- GET /monitor/health - Monitor health check

Author: Agent-5 (Business Intelligence Specialist)
Date: 2026-01-08
Phase: Phase 4 Sprint 4 - Operational Transformation Engine
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse, StreamingResponse
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
import json
import io
from datetime import datetime

from src.services.repository_monitor import repository_monitor

router = APIRouter(prefix="/repository", tags=["repository-monitor"])


# Pydantic Models
class RepositoryStats(BaseModel):
    """Response model for repository statistics."""
    total_files: int
    total_size_mb: float
    file_types: Dict[str, int]
    directories: int
    largest_files: List[Dict[str, Any]]
    snapshots_count: int
    monitoring_active: bool
    last_scan: float


class TrendAnalysis(BaseModel):
    """Response model for trend analysis."""
    time_window_hours: int
    growth_rate_files_per_hour: float
    growth_rate_size_per_hour: float
    most_changed_files: List[Dict[str, Any]]
    anomaly_score: float
    recommendations: List[str]


class SnapshotInfo(BaseModel):
    """Response model for snapshot information."""
    index: int
    timestamp: float
    total_files: int
    total_size_bytes: int
    file_type_distribution: Dict[str, int]
    directory_count: int
    recent_changes_count: int
    checksum: str


@router.get("/stats", response_model=RepositoryStats)
async def get_repository_stats():
    """
    Get current repository statistics.

    Returns comprehensive statistics about the repository including file counts,
    sizes, types, and monitoring status.
    """
    try:
        stats = repository_monitor.get_current_stats()
        if stats.get("error"):
            raise HTTPException(status_code=500, detail=stats["error"])

        return RepositoryStats(**stats)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get repository stats: {str(e)}")


@router.get("/trends/{hours}", response_model=TrendAnalysis)
async def get_trend_analysis(hours: int):
    """
    Get trend analysis for a specific time window.

    - **hours**: Time window in hours (1, 6, 24, 168 supported)
    """
    try:
        trend = repository_monitor.get_trends(hours)
        if not trend:
            raise HTTPException(
                status_code=404,
                detail=f"No trend data available for {hours} hour window"
            )

        return TrendAnalysis(**trend.__dict__)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get trend analysis: {str(e)}")


@router.get("/snapshots", response_model=List[SnapshotInfo])
async def list_snapshots():
    """
    List all available repository snapshots.
    """
    try:
        snapshots = []
        for i, snapshot in enumerate(repository_monitor.snapshots):
            snapshots.append(SnapshotInfo(
                index=i,
                timestamp=snapshot.timestamp,
                total_files=snapshot.total_files,
                total_size_bytes=snapshot.total_size_bytes,
                file_type_distribution=snapshot.file_type_distribution,
                directory_count=snapshot.directory_count,
                recent_changes_count=len(snapshot.recent_changes),
                checksum=snapshot.checksum
            ))

        return snapshots

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list snapshots: {str(e)}")


@router.get("/snapshots/{index}")
async def get_snapshot(index: int):
    """
    Get detailed information about a specific snapshot.

    - **index**: Snapshot index (0 = oldest, -1 = newest)
    """
    try:
        if index < 0:
            index = len(repository_monitor.snapshots) + index

        if index < 0 or index >= len(repository_monitor.snapshots):
            raise HTTPException(
                status_code=404,
                detail=f"Snapshot index {index} out of range"
            )

        snapshot = repository_monitor.snapshots[index]

        return {
            "index": index,
            "timestamp": snapshot.timestamp,
            "datetime": datetime.fromtimestamp(snapshot.timestamp).isoformat(),
            "total_files": snapshot.total_files,
            "total_size_bytes": snapshot.total_size_bytes,
            "total_size_mb": snapshot.total_size_bytes / 1024 / 1024,
            "file_type_distribution": snapshot.file_type_distribution,
            "directory_count": snapshot.directory_count,
            "largest_files": snapshot.largest_files,
            "recent_changes": snapshot.recent_changes,
            "checksum": snapshot.checksum,
            "metadata": snapshot.metadata
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get snapshot: {str(e)}")


@router.post("/scan")
async def trigger_scan(background_tasks: BackgroundTasks):
    """
    Trigger a manual repository scan.

    This will perform an immediate scan regardless of the regular schedule.
    """
    try:
        # Run scan in background
        background_tasks.add_task(repository_monitor._perform_scan)

        return {
            "message": "Repository scan triggered",
            "status": "running",
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to trigger scan: {str(e)}")


@router.get("/export")
async def export_monitoring_data():
    """
    Export complete monitoring data for analysis.

    Returns a JSON file containing all snapshots, trends, and configuration.
    """
    try:
        export_data = repository_monitor.export_data()

        # Create in-memory file
        json_data = json.dumps(export_data, indent=2, default=str)
        file_obj = io.BytesIO(json_data.encode('utf-8'))

        return StreamingResponse(
            file_obj,
            media_type="application/json",
            headers={
                "Content-Disposition": f"attachment; filename=repository_monitor_export_{int(datetime.now().timestamp())}.json"
            }
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to export data: {str(e)}")


@router.get("/health")
async def monitor_health():
    """
    Health check for the repository monitoring system.
    """
    try:
        stats = repository_monitor.get_performance_stats()

        health_status = {
            "status": "healthy" if repository_monitor.is_monitoring else "stopped",
            "monitoring_active": repository_monitor.is_monitoring,
            "snapshots_count": len(repository_monitor.snapshots),
            "last_scan_timestamp": repository_monitor.last_scan_time,
            "performance_stats": stats,
            "timestamp": datetime.now().isoformat()
        }

        # Check if monitoring is working
        if not repository_monitor.is_monitoring:
            health_status["issues"] = ["Repository monitoring is not active"]

        if len(repository_monitor.snapshots) == 0:
            health_status["issues"] = health_status.get("issues", []) + ["No snapshots available"]

        return health_status

    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }


@router.get("/alerts")
async def get_recent_alerts(limit: int = 10):
    """
    Get recent monitoring alerts.

    - **limit**: Maximum number of alerts to return (default: 10)
    """
    # Note: In a full implementation, you'd store alerts in a database
    # For now, return a placeholder
    return {
        "alerts": [],
        "message": "Alert system not yet implemented - check logs for alerts",
        "timestamp": datetime.now().isoformat()
    }


@router.get("/config")
async def get_monitor_config():
    """
    Get current monitoring configuration.
    """
    try:
        return {
            "config": repository_monitor.config,
            "alert_thresholds": repository_monitor.alert_thresholds,
            "is_monitoring": repository_monitor.is_monitoring,
            "snapshots_retention": repository_monitor.max_snapshots,
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get config: {str(e)}")


# WebSocket endpoint information
@router.get("/ws-info")
async def monitor_websocket_info():
    """
    Get WebSocket endpoint information for real-time monitoring updates.
    """
    return {
        "websocket_url": "ws://localhost:8766/ws/ai/monitoring",
        "supported_events": [
            "scan_complete",
            "alert_triggered",
            "trend_updated",
            "anomaly_detected"
        ],
        "message_format": {
            "type": "event_type",
            "data": {},
            "timestamp": "ISO format"
        },
        "protocol_version": "1.0"
    }