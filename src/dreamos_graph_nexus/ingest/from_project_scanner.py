"""Adapter for Project Scanner JSON into Graph Nexus nodes/edges."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Sequence

from ..models import GraphData, GraphEdge, GraphNode
from ..store.graph_repository import GraphRepository

NODE_TYPE_FILE = "file"
NODE_TYPE_SYMBOL = "symbol"
NODE_TYPE_MODULE = "module"
NODE_TYPE_ENTRYPOINT = "entrypoint"

EDGE_TYPE_CONTAINS = "contains"
EDGE_TYPE_BELONGS_TO = "belongs_to"
EDGE_TYPE_DECLARES = "declares"

FILE_METADATA_KEYS = {
    "language",
    "size",
    "hash",
    "sha256",
    "md5",
    "mtime",
    "line_count",
    "loc",
}


@dataclass(frozen=True)
class GraphIngestResult:
    """Summary of ingestion output."""

    node_count: int
    edge_count: int


class StableIdBuilder:
    """Deterministic ID builder for nodes and edges."""

    def build(self, namespace: str, parts: Iterable[str]) -> str:
        clean_parts = [namespace] + [part for part in parts if part]
        payload = "|".join(clean_parts)
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def load_scanner_json(scan_path: Path) -> Dict[str, Any]:
    """Load scanner JSON from disk."""
    with open(scan_path, "r", encoding="utf-8") as handle:
        return json.load(handle)


class ProjectScannerAdapter:
    """Convert Project Scanner data into Graph Nexus graph data."""

    def __init__(
        self,
        project_root: Path | None = None,
        id_builder: StableIdBuilder | None = None,
    ):
        self.project_root = Path(project_root).resolve() if project_root else None
        self.id_builder = id_builder or StableIdBuilder()

    def ingest(self, scan_path: Path, repository: GraphRepository) -> GraphIngestResult:
        """Load scan JSON, build graph data, and persist to repository."""
        raw_data = load_scanner_json(scan_path)
        graph_data = self.build_graph_data(raw_data)
        repository.initialize_schema()
        node_count = repository.upsert_nodes(graph_data.nodes)
        edge_count = repository.upsert_edges(graph_data.edges)
        return GraphIngestResult(node_count=node_count, edge_count=edge_count)

    def build_graph_data(self, raw_data: Dict[str, Any]) -> GraphData:
        """Build graph nodes and edges from scanner output."""
        scan_payload = self._extract_scan_payload(raw_data)
        entrypoints = self._collect_entrypoints(raw_data)

        nodes_by_id: Dict[str, GraphNode] = {}
        edges_by_id: Dict[str, GraphEdge] = {}

        for file_path, file_info in self._iter_file_entries(scan_payload):
            normalized_path = self._normalize_path(file_path)
            if not normalized_path:
                continue
            if isinstance(file_info, dict) and (
                file_info.get("is_entrypoint") or file_info.get("entrypoint")
            ):
                entrypoints.add(normalized_path)
            file_node = self._build_file_node(normalized_path, file_info)
            nodes_by_id[file_node.node_id] = file_node

            module_name = self._extract_module_name(file_info)
            if module_name:
                module_node = self._build_module_node(module_name, normalized_path)
                nodes_by_id[module_node.node_id] = module_node
                edge = self._build_edge(
                    EDGE_TYPE_BELONGS_TO, file_node.node_id, module_node.node_id
                )
                edges_by_id[edge.edge_id] = edge

            if normalized_path in entrypoints:
                entrypoint_node = self._build_entrypoint_node(normalized_path)
                nodes_by_id[entrypoint_node.node_id] = entrypoint_node
                edge = self._build_edge(
                    EDGE_TYPE_DECLARES, file_node.node_id, entrypoint_node.node_id
                )
                edges_by_id[edge.edge_id] = edge

            for symbol in self._extract_symbols(file_info):
                symbol_node = self._build_symbol_node(normalized_path, symbol)
                nodes_by_id[symbol_node.node_id] = symbol_node
                edge = self._build_edge(
                    EDGE_TYPE_CONTAINS, file_node.node_id, symbol_node.node_id
                )
                edges_by_id[edge.edge_id] = edge

        for entry_path in entrypoints:
            normalized_path = self._normalize_path(entry_path)
            if not normalized_path:
                continue
            entrypoint_node = self._build_entrypoint_node(normalized_path)
            nodes_by_id.setdefault(entrypoint_node.node_id, entrypoint_node)

        nodes = sorted(nodes_by_id.values(), key=lambda node: node.node_id)
        edges = sorted(edges_by_id.values(), key=lambda edge: edge.edge_id)
        return GraphData(nodes=nodes, edges=edges)

    def _extract_scan_payload(self, raw_data: Any) -> Any:
        if isinstance(raw_data, dict):
            if "scan_data" in raw_data:
                return raw_data["scan_data"]
            if "files" in raw_data:
                return raw_data["files"]
        return raw_data

    def _collect_entrypoints(self, raw_data: Dict[str, Any]) -> set[str]:
        entrypoints: set[str] = set()
        if not isinstance(raw_data, dict):
            return entrypoints
        for key in ("entrypoints", "entrypoint_files"):
            value = raw_data.get(key)
            if isinstance(value, list):
                entrypoints.update(str(item) for item in value if item)
        repo_metadata = raw_data.get("repo_metadata")
        if isinstance(repo_metadata, dict):
            value = repo_metadata.get("entrypoints")
            if isinstance(value, list):
                entrypoints.update(str(item) for item in value if item)
        normalized_paths = set()
        for path in entrypoints:
            normalized = self._normalize_path(path)
            if normalized:
                normalized_paths.add(normalized)
        return normalized_paths

    def _iter_file_entries(self, scan_payload: Any) -> Iterable[tuple[str | None, Any]]:
        if isinstance(scan_payload, dict):
            for key, value in scan_payload.items():
                if isinstance(value, dict):
                    path_value = value.get("path") or value.get("file_path") or key
                    yield str(path_value), value
                else:
                    yield str(key), {}
        elif isinstance(scan_payload, list):
            for item in scan_payload:
                if not isinstance(item, dict):
                    continue
                path_value = item.get("path") or item.get("file_path")
                if path_value:
                    yield str(path_value), item

    def _normalize_path(self, path_value: str | None) -> str | None:
        if not path_value:
            return None
        normalized = str(path_value).replace("\\", "/").strip()
        if normalized.startswith("./"):
            normalized = normalized[2:]
        if self.project_root:
            try:
                path = Path(normalized)
                if path.is_absolute():
                    normalized = str(path.relative_to(self.project_root))
            except ValueError:
                pass
        return normalized or None

    def _extract_module_name(self, file_info: Any) -> str | None:
        if not isinstance(file_info, dict):
            return None
        module_name = (
            file_info.get("module")
            or file_info.get("module_name")
            or file_info.get("module_path")
        )
        if module_name:
            return str(module_name)
        return None

    def _extract_symbols(self, file_info: Any) -> Sequence[Dict[str, Any]]:
        if not isinstance(file_info, dict):
            return []
        symbols: List[Dict[str, Any]] = []
        for key, kind in (
            ("functions", "function"),
            ("classes", "class"),
            ("symbols", "symbol"),
            ("entities", "symbol"),
        ):
            entries = file_info.get(key)
            if not isinstance(entries, list):
                continue
            for entry in entries:
                symbol = self._normalize_symbol_entry(entry, kind)
                if symbol:
                    symbols.append(symbol)
        return symbols

    def _normalize_symbol_entry(self, entry: Any, kind: str) -> Dict[str, Any] | None:
        if isinstance(entry, str):
            return {"name": entry, "kind": kind}
        if not isinstance(entry, dict):
            return None
        name = entry.get("name") or entry.get("function_name") or entry.get("class_name")
        if not name:
            return None
        signature = entry.get("signature") or entry.get("qualname") or entry.get("full_name")
        params = entry.get("parameters") or entry.get("params")
        if not signature and params:
            signature = f"{name}({', '.join(str(p) for p in params)})"
        symbol_data: Dict[str, Any] = {"name": str(name), "kind": kind}
        if signature:
            symbol_data["signature"] = str(signature)
        for key in ("line_start", "line_end", "line", "column"):
            if key in entry:
                symbol_data[key] = entry[key]
        location = entry.get("location")
        if isinstance(location, dict):
            symbol_data["location"] = location
        return symbol_data

    def _build_file_node(self, file_path: str, file_info: Any) -> GraphNode:
        node_id = self.id_builder.build(NODE_TYPE_FILE, [file_path])
        name = Path(file_path).name
        metadata = {}
        if isinstance(file_info, dict):
            metadata = {k: file_info[k] for k in FILE_METADATA_KEYS if k in file_info}
        return GraphNode(
            node_id=node_id,
            node_type=NODE_TYPE_FILE,
            name=name,
            path=file_path,
            metadata=metadata,
        )

    def _build_symbol_node(self, file_path: str, symbol: Dict[str, Any]) -> GraphNode:
        signature = symbol.get("signature") or symbol.get("name")
        node_id = self.id_builder.build(NODE_TYPE_SYMBOL, [file_path, str(signature)])
        metadata = {k: v for k, v in symbol.items() if k != "name" and k != "signature"}
        return GraphNode(
            node_id=node_id,
            node_type=NODE_TYPE_SYMBOL,
            name=str(symbol["name"]),
            path=file_path,
            signature=str(signature) if signature else None,
            metadata=metadata,
        )

    def _build_module_node(self, module_name: str, file_path: str) -> GraphNode:
        node_id = self.id_builder.build(NODE_TYPE_MODULE, [module_name])
        metadata = {"source_path": file_path}
        return GraphNode(
            node_id=node_id,
            node_type=NODE_TYPE_MODULE,
            name=module_name,
            path=file_path,
            signature=module_name,
            metadata=metadata,
        )

    def _build_entrypoint_node(self, entry_path: str) -> GraphNode:
        node_id = self.id_builder.build(NODE_TYPE_ENTRYPOINT, [entry_path])
        name = Path(entry_path).name
        metadata = {"entry_path": entry_path}
        return GraphNode(
            node_id=node_id,
            node_type=NODE_TYPE_ENTRYPOINT,
            name=name,
            path=entry_path,
            signature=entry_path,
            metadata=metadata,
        )

    def _build_edge(self, edge_type: str, source_id: str, target_id: str) -> GraphEdge:
        edge_id = self.id_builder.build(edge_type, [source_id, target_id])
        return GraphEdge(
            edge_id=edge_id,
            edge_type=edge_type,
            source_id=source_id,
            target_id=target_id,
            metadata={},
        )
