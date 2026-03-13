"""Data models for Graph Nexus nodes and edges."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Sequence


@dataclass(frozen=True)
class GraphNode:
    """Graph node representation."""

    node_id: str
    node_type: str
    name: str
    path: str | None = None
    signature: str | None = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class GraphEdge:
    """Graph edge representation."""

    edge_id: str
    edge_type: str
    source_id: str
    target_id: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class GraphData:
    """Container for graph nodes and edges."""

    nodes: Sequence[GraphNode]
    edges: Sequence[GraphEdge]
