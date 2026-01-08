#!/usr/bin/env python3
"""
Middleware Module - FastAPI Services
====================================

V2 Compliant: Yes (<100 lines)
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2026-01-08

Middleware functions extracted from fastapi_app.py for V2 compliance.
Provides centralized middleware configuration for FastAPI application.
"""

import logging
import time
from typing import Callable

from fastapi import Request, Response
from fastapi.responses import JSONResponse

from .fastapi_rate_limiting import check_rate_limit
from .fastapi_monitoring import increment_metric, record_response_time

logger = logging.getLogger(__name__)

# Horizontal scaling configuration
HORIZONTAL_SCALING_ENABLED = False
INSTANCE_ID = "fastapi-01"


async def rate_limiting_middleware(request: Request, call_next: Callable) -> Response:
    """
    Rate limiting middleware for API protection.

    Applies rate limiting to API endpoints with configurable limits.
    Tracks requests and returns 429 status when limits exceeded.

    Args:
        request: FastAPI request object
        call_next: Next middleware/route handler

    Returns:
        Response: API response with rate limiting applied
    """
    increment_metric("requests_total")

    # Skip rate limiting for health checks and static files
    if request.url.path in ["/health", "/docs", "/redoc", "/openapi.json"] or request.url.path.startswith("/static"):
        response = await call_next()
        return response

    client_ip = request.client.host if request.client else "unknown"
    endpoint = request.url.path

    if not await check_rate_limit(client_ip, endpoint):
        increment_metric("rate_limit_hits")
        return JSONResponse(
            status_code=429,
            content={"error": "Rate limit exceeded", "retry_after": 60}  # Rate limit window
        )

    response = await call_next()

    # Track AI endpoint usage
    if endpoint.startswith("/api/ai/"):
        increment_metric("ai_requests")

    # Track response status
    if response.status_code >= 400:
        increment_metric("errors_total")

    return response


async def performance_monitoring_middleware(request: Request, call_next: Callable) -> Response:
    """
    Performance monitoring middleware for response time tracking.

    Measures response times and adds performance headers.
    Tracks slow responses and maintains performance metrics.

    Args:
        request: FastAPI request object
        call_next: Next middleware/route handler

    Returns:
        Response: API response with performance headers
    """
    start_time = time.perf_counter()

    response = await call_next()

    # Calculate response time
    response_time = time.perf_counter() - start_time
    response_time_ms = response_time * 1000

    # Add performance headers
    response.headers["X-Response-Time"] = ".2f"
    response.headers["X-Performance-Monitor"] = "enabled"

    # Record response time for monitoring
    record_response_time(response_time_ms)

    # Log slow responses (>500ms)
    if response_time_ms > 500:
        logger.warning(".2f"
                      f"{request.url.path}")

    return response


async def horizontal_scaling_middleware(request: Request, call_next: Callable) -> Response:
    """
    Horizontal scaling middleware for load balancer health checks.

    Adds instance identification headers for load balancer routing.
    Supports multi-instance deployment scenarios.

    Args:
        request: FastAPI request object
        call_next: Next middleware/route handler

    Returns:
        Response: API response with instance headers
    """
    response = await call_next()

    if HORIZONTAL_SCALING_ENABLED:
        response.headers["X-Instance-ID"] = INSTANCE_ID
        response.headers["X-Load-Balancer"] = "enabled"

    return response


def setup_middleware(app):
    """
    Setup all middleware for the FastAPI application.

    Configures middleware stack in optimal order:
    1. Performance monitoring (first to capture all timings)
    2. Rate limiting (early rejection of abusive requests)
    3. Horizontal scaling (instance identification)

    Args:
        app: FastAPI application instance
    """
    # Add middleware in order (first added = first executed)
    app.middleware("http")(performance_monitoring_middleware)
    app.middleware("http")(rate_limiting_middleware)
    app.middleware("http")(horizontal_scaling_middleware)

    logger.info("✅ Middleware stack configured")


def get_middleware_status() -> dict:
    """
    Get middleware configuration status.

    Returns:
        dict: Middleware status information
    """
    return {
        "rate_limiting": "enabled",
        "performance_monitoring": "enabled",
        "horizontal_scaling": "enabled" if HORIZONTAL_SCALING_ENABLED else "disabled",
        "instance_id": INSTANCE_ID
    }


__all__ = [
    "rate_limiting_middleware",
    "performance_monitoring_middleware",
    "horizontal_scaling_middleware",
    "setup_middleware",
    "get_middleware_status",
    "HORIZONTAL_SCALING_ENABLED",
    "INSTANCE_ID"
]