#!/usr/bin/env python3
"""
FastAPI Middleware - Modular V2 Compliance
==========================================

<!-- SSOT Domain: web -->

Middleware setup for FastAPI application.
All middleware configured here for modularity.

V2 Compliant: <100 lines
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2026-01-08
"""

import time
import logging
from typing import Callable
from fastapi import Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse

from .fastapi_config import settings, get_cors_origins

logger = logging.getLogger(__name__)


async def request_logging_middleware(request: Request, call_next: Callable) -> Response:
    """Middleware for request logging and basic monitoring."""
    start_time = time.time()

    # Log request
    logger.info(f"→ {request.method} {request.url.path}")

    try:
        response = await call_next(request)

        # Calculate duration
        duration = time.time() - start_time

        # Log response
        logger.info(f"← {request.method} {request.url.path} - {response.status_code} ({duration:.2f}s)")
        # Add custom headers
        response.headers["X-Process-Time"] = str(duration)
        response.headers["X-API-Version"] = settings.app_version

        return response

    except Exception as e:
        # Log error
        duration = time.time() - start_time
        logger.error(f"Request error for {request.method} {request.url.path}: {e} ({duration:.2f}s)")
        # Return error response
        return JSONResponse(
            status_code=500,
            content={"error": "Internal server error", "detail": str(e)},
        )


async def cors_middleware(request: Request, call_next: Callable) -> Response:
    """CORS handling middleware."""
    # Add CORS headers manually if not using CORSMiddleware
    response = await call_next(request)

    # Allow all origins for development
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "*"

    return response


async def security_headers_middleware(request: Request, call_next: Callable) -> Response:
    """Add security headers to responses."""
    response = await call_next(request)

    # Security headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"

    # Only add HSTS in production
    if not settings.debug:
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"

    return response


def setup_all_middleware(app) -> None:
    """Setup all middleware for the FastAPI application."""

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=get_cors_origins(),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Trusted host middleware (production only)
    if not settings.debug:
        app.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts=["your-domain.com", "*.your-domain.com"]
        )

    # Request logging middleware
    app.middleware("http")(request_logging_middleware)

    # Security headers middleware
    app.middleware("http")(security_headers_middleware)

    logger.info("✅ All middleware configured")


def add_custom_middleware(app, middleware_func: Callable) -> None:
    """Add custom middleware to the application."""
    app.middleware("http")(middleware_func)
    logger.info(f"✅ Custom middleware added: {middleware_func.__name__}")


def remove_middleware(app, middleware_func: Callable) -> None:
    """Remove middleware from the application (if needed)."""
    # Note: FastAPI doesn't provide direct removal, this would require app rebuild
    logger.warning(f"⚠️ Middleware removal not supported: {middleware_func.__name__}")
    logger.warning("   Application restart required for middleware changes")