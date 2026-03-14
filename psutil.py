"""Minimal psutil stub for test environment."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class _MemoryInfo:
    rss: int = 0


class Process:
    def __init__(self, pid: int | None = None) -> None:
        self.pid = pid

    def memory_info(self) -> _MemoryInfo:
        return _MemoryInfo(rss=0)


def cpu_percent(interval: float | None = None) -> float:
    return 0.0
