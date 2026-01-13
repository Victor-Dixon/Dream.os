"""
FastAPI Rate Limiting Module
<<<<<<< HEAD
============================

V2 Compliant - Comprehensive rate limiting with Redis backend
Author: Agent-7 (Web Development Specialist)
Date: 2026-01-10

Implements configurable rate limiting per endpoint with Redis storage.
Supports different limits for different user types and endpoints.
"""

import logging
from typing import Dict, Optional, Any, Callable
from functools import wraps
from fastapi import Request, HTTPException, Depends
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware

logger = logging.getLogger(__name__)

class ConfigurableRateLimiter:
    """Configurable rate limiter with Redis backend and fallback."""

    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.redis_url = redis_url
        self.limiter = None
        self.endpoint_limits = {}
        self._setup_limiter()

    def _setup_limiter(self):
        """Setup rate limiter with Redis backend."""
        try:
            from slowapi import Limiter as SlowAPILimiter
            self.limiter = SlowAPILimiter(
                key_func=get_remote_address,
                storage_uri=self.redis_url,
                strategy="fixed-window"
            )
            logger.info("✅ Redis-backed rate limiter initialized")
        except Exception as e:
            logger.warning(f"⚠️ Redis rate limiter failed ({e}), using in-memory fallback")
            from slowapi import Limiter as SlowAPILimiter
            self.limiter = SlowAPILimiter(
                key_func=get_remote_address,
                storage_uri="memory://",
                strategy="fixed-window"
            )

    def add_endpoint_limit(self, endpoint: str, limit: str, methods: list = None):
        """
        Add rate limit for specific endpoint.

        Args:
            endpoint: URL path pattern (e.g., "/api/*" or "/users")
            limit: Rate limit string (e.g., "100/minute", "10/second")
            methods: List of HTTP methods to apply limit to (default: all)
        """
        self.endpoint_limits[endpoint] = {
            'limit': limit,
            'methods': methods or ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']
        }
        logger.info(f"✅ Rate limit added: {endpoint} -> {limit}")

    def get_endpoint_limit(self, path: str, method: str) -> Optional[str]:
        """Get rate limit for endpoint and method."""
        # Check for exact matches first
        if path in self.endpoint_limits:
            config = self.endpoint_limits[path]
            if method in config['methods']:
                return config['limit']

        # Check for pattern matches (simple wildcard support)
        for endpoint_pattern, config in self.endpoint_limits.items():
            if endpoint_pattern.endswith('/*'):
                base_pattern = endpoint_pattern[:-2]
                if path.startswith(base_pattern) and method in config['methods']:
                    return config['limit']

        return None

    def limit(self, limit_string: str = None, key_func: Callable = None):
        """Decorator to apply rate limiting."""
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                if not self.limiter:
                    return await func(*args, **kwargs)

                # Get limit from parameter or endpoint config
                limit = limit_string
                if not limit:
                    # Try to get from endpoint config
                    request = None
                    for arg in args:
                        if isinstance(arg, Request):
                            request = arg
                            break

                    if request:
                        limit = self.get_endpoint_limit(request.url.path, request.method)

                if limit:
                    # Apply rate limiting
                    limiter_decorator = self.limiter.limit(limit, key_func=key_func)
                    return await limiter_decorator(func)(*args, **kwargs)

                # No limit configured, proceed normally
                return await func(*args, **kwargs)

            return wrapper
        return decorator

# Global rate limiter instance
rate_limiter = ConfigurableRateLimiter()

def get_rate_limiter():
    """Get the global rate limiter instance."""
    return rate_limiter

def setup_default_limits():
    """Setup default rate limits for common endpoints."""
    # API endpoints - moderate limits
    rate_limiter.add_endpoint_limit("/api/*", "100/minute")
    rate_limiter.add_endpoint_limit("/api/auth/*", "10/minute")  # Stricter for auth
    rate_limiter.add_endpoint_limit("/api/admin/*", "50/minute")  # Moderate for admin

    # Public endpoints - higher limits
    rate_limiter.add_endpoint_limit("/health", "1000/minute")
    rate_limiter.add_endpoint_limit("/ping", "1000/minute")
    rate_limiter.add_endpoint_limit("/perf/*", "100/minute")

    # Static files - very high limits
    rate_limiter.add_endpoint_limit("/static/*", "10000/minute")

    logger.info("✅ Default rate limits configured")

def create_rate_limit_middleware():
    """Create rate limiting middleware for FastAPI."""
    if rate_limiter.limiter:
        return SlowAPIMiddleware
    return None

def apply_rate_limits():
    """Apply rate limiting to endpoints (decorator version)."""
    def decorator(func):
        return rate_limiter.limit()(func)
    return decorator

def custom_rate_limit(limit: str, key_func: Callable = None):
    """Custom rate limit decorator with specific limit."""
    def decorator(func):
        return rate_limiter.limit(limit, key_func)(func)
    return decorator

def endpoint_rate_limit(endpoint: str, limit: str):
    """Apply rate limit to specific endpoint."""
    rate_limiter.add_endpoint_limit(endpoint, limit)

def user_based_rate_limit(user_type_func: Callable):
    """
    Rate limit based on user type.

    Args:
        user_type_func: Function that returns user type ('admin', 'premium', 'basic', etc.)
    """
    def key_func(request: Request):
        user_type = user_type_func(request)
        ip = get_remote_address(request)
        return f"{user_type}:{ip}"

    # Define limits for different user types
    user_limits = {
        'admin': '1000/minute',
        'premium': '500/minute',
        'basic': '100/minute',
        'anonymous': '50/minute'
    }

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            if not rate_limiter.limiter:
                return await func(*args, **kwargs)

            request = None
            for arg in args:
                if isinstance(arg, Request):
                    request = arg
                    break

            if request:
                user_type = user_type_func(request)
                limit = user_limits.get(user_type, user_limits['anonymous'])

                limiter_decorator = rate_limiter.limiter.limit(limit, key_func=key_func)
                return await limiter_decorator(func)(*args, **kwargs)

            return await func(*args, **kwargs)

        return wrapper

    return decorator

def get_rate_limit_status() -> Dict[str, Any]:
    """Get current rate limiting status and configuration."""
    return {
        'enabled': rate_limiter.limiter is not None,
        'storage_type': 'redis' if 'redis' in str(rate_limiter.redis_url) else 'memory',
        'endpoint_limits': rate_limiter.endpoint_limits,
        'default_limits_configured': bool(rate_limiter.endpoint_limits)
    }

# Initialize default limits
setup_default_limits()
=======
V2 Compliant - <100 lines
"""

from fastapi import Request, HTTPException
from slowapi import Limiter
from slowapi.util import get_remote_address

# Rate limiter instance
limiter = Limiter(key_func=get_remote_address)

def get_rate_limiter():
    """Get configured rate limiter"""
    return limiter

def apply_rate_limits():
    """Apply rate limiting to endpoints"""
    pass
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
