"""
FastAPI Caching Module
V2 Compliant - <100 lines
"""

from fastapi import Request, Response
from cachetools import TTLCache

# Cache instance
cache = TTLCache(maxsize=100, ttl=300)

def get_cache():
    """Get caching instance"""
    return cache

def cache_response():
    """Cache response decorator"""
    pass