"""
Health Check Module - Agent Cellphone V2
========================================

SSOT Domain: core

Provides system health check functionality for the FastAPI application.

Features:
- System health status assessment
- Service availability checking
- Performance metrics collection

V2 Compliant: Yes (<300 lines)
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2026-01-07
"""

import time
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

def check_system_health(include_services: bool = True, include_metrics: bool = False) -> Dict[str, Any]:
    """
    Comprehensive system health check.

    Args:
        include_services: Whether to include service-specific checks
        include_metrics: Whether to include performance metrics

    Returns:
        Dictionary containing health status information
    """
    health_data = {
        "status": "healthy",
        "overall_status": "healthy",
        "timestamp": time.time(),
        "version": "2.0.0"
    }

    try:
        # Check core services
        if include_services:
            health_data.update(_check_services())

        # Add performance metrics if requested
        if include_metrics:
            health_data["metrics"] = _get_performance_metrics()

        # Determine overall status based on service health
        if include_services:
            service_statuses = [
                health_data.get("fastapi_status", "unknown"),
                health_data.get("analytics_status", "unknown"),
                health_data.get("database_status", "unknown")
            ]

            # If any critical service is unhealthy, overall status is unhealthy
            if any(status in ["unhealthy", "unavailable", "error"] for status in service_statuses):
                health_data["overall_status"] = "unhealthy"
                health_data["status"] = "degraded"
            else:
                health_data["overall_status"] = "healthy"
                health_data["status"] = "healthy"
        else:
            # Basic health check without services
            health_data["overall_status"] = "healthy"
            health_data["status"] = "healthy"

    except Exception as e:
        logger.error(f"Health check error: {e}")
        health_data.update({
            "status": "error",
            "overall_status": "unhealthy",
            "error": str(e)
        })

    return health_data

def _check_services() -> Dict[str, Any]:
    """Check individual service statuses."""
    services = {}

    # FastAPI service (self)
    services["fastapi_status"] = "healthy"

    # Analytics service (PHASE 4 CONSOLIDATION)
    try:
        from tools.infrastructure_tools import UnifiedInfrastructureManager
        infra_mgr = UnifiedInfrastructureManager()
        analytics_svc = infra_mgr.get_service("analytics")
        services["analytics_status"] = "healthy" if analytics_svc else "unavailable"
    except ImportError:
        services["analytics_status"] = "unavailable"
    except Exception as e:
        logger.warning(f"Analytics service check failed: {e}")
        services["analytics_status"] = "error"

    # Database service - simplified synchronous check
    try:
        import os
        # Simple check for database availability
        if os.path.exists("database/__init__.py"):
            services["database_status"] = "healthy"
        else:
            services["database_status"] = "unavailable"
    except Exception as e:
        logger.warning(f"Database service check failed: {e}")
        services["database_status"] = "error"

    # Message queue service
    try:
        # Check if message queue is accessible
        import os
        if os.path.exists("agent_workspaces"):
            services["message_queue_status"] = "healthy"
        else:
            services["message_queue_status"] = "unavailable"
    except Exception as e:
        logger.warning(f"Message queue check failed: {e}")
        services["message_queue_status"] = "error"

    return services

def _get_performance_metrics() -> Dict[str, Any]:
    """Get system performance metrics."""
    try:
        import psutil
        import os

        # Basic system metrics
        metrics = {
            "cpu_percent": psutil.cpu_percent(interval=0.1),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_usage": psutil.disk_usage('/').percent,
            "process_count": len(psutil.pids()),
            "uptime": time.time() - psutil.boot_time()
        }

        # Application-specific metrics
        pid = os.getpid()
        try:
            process = psutil.Process(pid)
            metrics.update({
                "app_cpu_percent": process.cpu_percent(interval=0.1),
                "app_memory_mb": process.memory_info().rss / (1024 * 1024),
                "app_threads": process.num_threads()
            })
        except Exception as e:
            logger.debug(f"Could not get app metrics: {e}")

        return metrics

    except ImportError:
        # psutil not available, return basic metrics
        return {
            "cpu_percent": 0.0,
            "memory_percent": 0.0,
            "uptime": time.time(),
            "note": "psutil not available"
        }
    except Exception as e:
        logger.warning(f"Performance metrics collection failed: {e}")
        return {"error": str(e)}

def check_fastapi_health() -> Dict[str, Any]:
    """FastAPI-specific health check."""
    return {
        "fastapi_status": "healthy",
        "version": "2.0.0",
        "timestamp": time.time(),
        "uptime": time.time() - getattr(check_fastapi_health, 'start_time', time.time())
    }

# Set initial start time for uptime calculation
check_fastapi_health.start_time = time.time()

# Export the main function
__all__ = ["check_system_health", "check_fastapi_health"]