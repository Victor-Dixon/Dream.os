"""Shared utilities for Graph Nexus ingestion."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable


@dataclass(frozen=True)
class GraphIngestResult:
    """Summary of ingestion output."""

    node_count: int
    edge_count: int


class GraphIngestError(RuntimeError):
    """Error raised when ingestion fails."""


class StableIdBuilder:
    """Deterministic ID builder for nodes and edges."""

    def build(self, namespace: str, parts: Iterable[str]) -> str:
        clean_parts = [namespace] + [part for part in parts if part]
        payload = "|".join(clean_parts)
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def load_scanner_json(scan_path: Path) -> Dict[str, Any]:
    """Load scanner JSON from disk."""
    try:
        with open(scan_path, "r", encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        raise GraphIngestError(f"Failed to load scanner JSON: {scan_path}") from exc


def stable_string(value: Any) -> str:
    """Canonical string for deterministic hashing."""
    if value is None:
        return ""
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(value, sort_keys=True, separators=(",", ":"))
    return str(value)


def build_symbol_identity(symbol: Dict[str, Any]) -> str:
    """Build canonical identity payload for a symbol."""
    name = stable_string(symbol.get("name"))
    kind = stable_string(symbol.get("kind") or "symbol")
    scope = symbol.get("scope") or symbol.get("qualname") or symbol.get("full_name")
    signature = symbol.get("signature")
    identity: Dict[str, Any] = {"name": name, "kind": kind}
    if scope:
        identity["scope"] = stable_string(scope)
    elif signature:
        identity["signature"] = stable_string(signature)
    return json.dumps(identity, sort_keys=True, separators=(",", ":"))
