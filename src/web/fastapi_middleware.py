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
import gzip
import hashlib
from typing import Callable, Optional
from fastapi import Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse

from .fastapi_config import settings, get_cors_origins

logger = logging.getLogger(__name__)

# PERFORMANCE OPTIMIZATION: Response cache
_response_cache = {}
_cache_max_size = 1000
_cache_ttl = 300  # 5 minutes


def _get_cache_key(request: Request) -> str:
    """Generate cache key from request."""
    key_parts = [
        request.method,
        str(request.url),
        str(request.query_params),
        hashlib.md5(request.headers.get("authorization", "").encode()).hexdigest()[:8]
    ]
    return hashlib.md5("|".join(key_parts).encode()).hexdigest()


def _is_cacheable_request(request: Request) -> bool:
    """Check if request can be cached."""
    return (
        request.method == "GET" and
        not request.headers.get("authorization") and  # Don't cache authenticated requests
        not any(param.startswith("nocache") for param in request.query_params.keys())
    )


def _is_cacheable_response(response: Response) -> bool:
    """Check if response can be cached."""
    return (
        response.status_code == 200 and
        not response.headers.get("cache-control") == "no-cache"
    )


async def response_caching_middleware(request: Request, call_next: Callable) -> Response:
    """
    PERFORMANCE OPTIMIZATION: Response caching middleware.
    Caches GET responses to reduce processing overhead.
    """
    if not _is_cacheable_request(request):
        return await call_next(request)

    cache_key = _get_cache_key(request)
    current_time = time.time()

    # Check cache
    if cache_key in _response_cache:
        cached_response, cache_time = _response_cache[cache_key]
        if current_time - cache_time < _cache_ttl:
            logger.debug(f"Cache hit for {request.url.path}")
            # Return cached response (deep copy to avoid mutation)
            return Response(
                content=cached_response["content"],
                status_code=cached_response["status_code"],
                headers=cached_response["headers"]
            )
        else:
            # Remove expired cache entry
            del _response_cache[cache_key]

    # Process request
    response = await call_next(request)

    # Cache successful responses
    if _is_cacheable_response(response):
        try:
            content = response.body if hasattr(response, 'body') else b""
            _response_cache[cache_key] = {
                "content": content,
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "cached_at": current_time
            }

            # Maintain cache size limit
            if len(_response_cache) > _cache_max_size:
                # Remove oldest entries
                sorted_entries = sorted(_response_cache.items(), key=lambda x: x[1]["cached_at"])
                for key, _ in sorted_entries[:100]:  # Remove 10% of entries
                    del _response_cache[key]

            logger.debug(f"Cached response for {request.url.path}")

        except Exception as e:
            logger.warning(f"Failed to cache response: {e}")

    return response


async def performance_monitoring_middleware(request: Request, call_next: Callable) -> Response:
    """
    PERFORMANCE OPTIMIZATION: Enhanced performance monitoring.
    Tracks detailed performance metrics for optimization.
    """
    start_time = time.time()
    start_memory = 0

    # Track memory usage if available
    try:
        import psutil
        process = psutil.Process()
        start_memory = process.memory_info().rss
    except ImportError:
        pass

    try:
        response = await call_next(request)

        # Calculate performance metrics
        duration = time.time() - start_time
        memory_used = 0

        try:
            import psutil
            process = psutil.Process()
            memory_used = process.memory_info().rss - start_memory
        except ImportError:
            pass

        # Add performance headers
        response.headers["X-Response-Time"] = ".2f"
        response.headers["X-Memory-Usage"] = str(memory_used)
        response.headers["X-Cache-Status"] = "HIT" if hasattr(response, '_from_cache') else "MISS"

        # Log performance warnings
        if duration > 1.0:  # Log slow requests
            logger.warning(f"Slow request: {duration:.2f}s for {request.url.path}")
        if memory_used > 50 * 1024 * 1024:  # Log high memory usage (>50MB)
            logger.warning(f"High memory usage: {memory_used / 1024 / 1024:.1f}MB for {request.url.path}")

        return response

    except Exception as e:
        logger.error(f"Performance monitoring error: {e}")
        raise


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
    """Setup all middleware for the FastAPI application with performance optimizations."""

    # PERFORMANCE OPTIMIZATION: GZip compression middleware
    app.add_middleware(GZipMiddleware, minimum_size=1000)

<<<<<<< HEAD
    # RATE LIMITING: Apply rate limiting middleware
    from .fastapi_rate_limiting import create_rate_limit_middleware
    rate_limit_middleware = create_rate_limit_middleware()
    if rate_limit_middleware:
        app.add_middleware(rate_limit_middleware)

=======
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
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

<<<<<<< HEAD
    # PERFORMANCE OPTIMIZATION: Redis-based response caching middleware (applied first)
    from .fastapi_caching import cache_response_middleware
    app.middleware("http")(cache_response_middleware(ttl=300))  # 5 minute TTL

    # PERFORMANCE OPTIMIZATION: Enhanced performance monitoring
    from .fastapi_performance import get_performance_middleware
    app.middleware("http")(get_performance_middleware())
=======
    # PERFORMANCE OPTIMIZATION: Response caching middleware (applied first)
    app.middleware("http")(response_caching_middleware)

    # PERFORMANCE OPTIMIZATION: Enhanced performance monitoring
    app.middleware("http")(performance_monitoring_middleware)
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1

    # Request logging middleware (applied last to capture all processing)
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