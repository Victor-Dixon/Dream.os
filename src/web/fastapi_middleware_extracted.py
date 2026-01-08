"""
FastAPI Middleware Stack
V2 Compliant - <100 lines
"""

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

class CustomMiddleware(BaseHTTPMiddleware):
    """Custom middleware for FastAPI"""
    pass