#!/usr/bin/env python3
"""
Memory Convenience Functions
===========================

Provides easy-to-use functions for common memory operations.
These functions handle API creation and cleanup automatically.
"""

import logging
from typing import List, Dict, Any, Optional

from .api import MemoryAPI
from dreamscape.core.config import MEMORY_DB_PATH

logger = logging.getLogger(__name__)

# Global API instance for convenience
_global_memory_api = None


def get_memory_api(db_path: str = str(MEMORY_DB_PATH)) -> MemoryAPI:
    """Get a MemoryAPI instance."""
    return MemoryAPI(db_path)


def close_memory_api():
    """Close the global memory API instance."""
    global _global_memory_api
    if _global_memory_api:
        _global_memory_api.close()
        _global_memory_api = None


def search_memory(query: str, limit: int = 5) -> List[Dict[str, Any]]:
    """Search memory for conversations."""
    api = get_memory_api()
    try:
        return api.search_conversations(query, limit)
    finally:
        api.close()


def advanced_search_memory(query: str, limit: int = 5) -> List[Dict[str, Any]]:
    """Advanced search in memory."""
    api = get_memory_api()
    try:
        return api.advanced_search_conversations(query, limit)
    finally:
        api.close()


def get_context_for_task(task: str, limit: int = 3) -> str:
    """Get context for a specific task."""
    api = get_memory_api()
    try:
        return api.get_agent_context(task, limit)
    finally:
        api.close()


def get_memory_stats() -> Dict[str, Any]:
    """Get memory statistics."""
    api = get_memory_api()
    try:
        return api.get_memory_stats()
    finally:
        api.close()


def search_prompts(query: str = None, category: str = None, prompt_type: str = None, limit: int = 20) -> List[Dict[str, Any]]:
    """Search prompts."""
    api = get_memory_api()
    try:
        return api.search_prompts(query, category, prompt_type, limit)
    finally:
        api.close()


def get_prompt_stats() -> Dict[str, Any]:
    """Get prompt statistics."""
    api = get_memory_api()
    try:
        return api.get_prompt_stats()
    finally:
        api.close()


def get_best_prompts(category: str = None, limit: int = 10) -> List[Dict[str, Any]]:
    """Get best performing prompts."""
    api = get_memory_api()
    try:
        return api.get_best_prompts(category, limit)
    finally:
        api.close() 