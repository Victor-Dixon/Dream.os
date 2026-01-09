#!/usr/bin/env python3
"""
Weaponization Configuration
==========================

Configuration for memory weaponization pipeline.
"""

from dataclasses import dataclass
from dreamscape.core.config import MEMORY_DB_PATH


@dataclass
class WeaponizationConfig:
    """Configuration for memory weaponization."""
    corpus_path: str = str(MEMORY_DB_PATH)
    output_dir: str = "outputs/weaponization"
    chunk_size: int = 512
    overlap: int = 50
    max_chunks_per_conversation: int = 100
    min_chunk_length: int = 50
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    faiss_index_type: str = "IVFFlat"
    nlist: int = 100
    nprobe: int = 10 