"""Shared helpers for the audit harness (SSOT for utilities)."""

from __future__ import annotations

import hashlib
from pathlib import Path


def count_lines(file_path: Path) -> int:
    """Count lines in a file."""
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as handle:
            return sum(1 for _ in handle)
    except OSError:
        return 0


def file_hash(file_path: Path) -> str:
    """Calculate MD5 hash of file contents."""
    try:
        with open(file_path, "rb") as handle:
            return hashlib.md5(handle.read()).hexdigest()[:8]
    except OSError:
        return "error"
