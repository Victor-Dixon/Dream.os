"""Simple knowledge graph backend for skills and dependencies."""

from __future__ import annotations

from dataclasses import asdict
from typing import Any, Dict, List, Tuple

from ..models import KnowledgeNode


class KnowledgeGraphBackend:
    """In-memory knowledge graph for skill relationships."""

    def __init__(self) -> None:
        self.nodes: Dict[str, KnowledgeNode] = {}
        self.edges: List[Tuple[str, str, str]] = []  # (src, dst, type)

    # ------------------------------------------------------------------
    # Node/Edge management
    # ------------------------------------------------------------------
    def add_node(self, node: KnowledgeNode) -> None:
        """Add or update a knowledge node."""
        self.nodes[node.topic] = node

    def add_dependency(self, source: str, target: str) -> None:
        self.edges.append((source, target, "dependency"))

    def add_unlock(self, source: str, target: str) -> None:
        self.edges.append((source, target, "unlock"))

    # ------------------------------------------------------------------
    # Retrieval helpers
    # ------------------------------------------------------------------
    def get_graph(self) -> Dict[str, Any]:
        """Return graph in node/edge format."""
        nodes = [asdict(node) for node in self.nodes.values()]
        edges = [
            {"source": s, "target": t, "type": typ}
            for s, t, typ in self.edges
        ]
        return {"nodes": nodes, "edges": edges}
