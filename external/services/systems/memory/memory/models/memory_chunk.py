#!/usr/bin/env python3
"""
Memory Chunk Model
=================

Represents a searchable memory chunk for the memory system.
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class MemoryChunk:
    """Represents a searchable memory chunk."""
    id: str
    conversation_id: str
    content: str
    role: str  # 'user', 'assistant', 'system'
    timestamp: str
    embedding: Optional[Any] = None
    metadata: Optional[Dict[str, Any]] = None 