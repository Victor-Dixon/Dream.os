"""Lock-in tests for batches 001-003 module contracts."""

from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
BATCH_FILES = [
    ROOT / "batches/batch_001_paths.txt",
    ROOT / "batches/batch_002_paths.txt",
    ROOT / "batches/batch_003_paths.txt",
]
CONTRACT_SNAPSHOT_PATH = ROOT / "tests/snapshots/batch_001_003_module_contracts.json"
REGISTRY_SNAPSHOT_PATH = ROOT / "tests/snapshots/batch_001_003_registry_coverage.json"
RECOVERY_REGISTRY = ROOT / "docs/recovery/recovery_registry.yaml"


def _load_batch_paths() -> list[str]:
    paths: list[str] = []
    for path_file in BATCH_FILES:
        for line in path_file.read_text(encoding="utf-8").splitlines():
            if line.strip():
                paths.append(line.strip())
    return sorted(set(paths))


def _public_assignments(node: ast.Assign) -> list[str]:
    names: list[str] = []
    for target in node.targets:
        if isinstance(target, ast.Name) and not target.id.startswith("_"):
            names.append(target.id)
    return names


def _function_contract(node: ast.AST) -> dict[str, Any]:
    assert isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    return {
        "name": node.name,
        "async": isinstance(node, ast.AsyncFunctionDef),
        "lineno": node.lineno,
        "args": len(node.args.args),
        "kwonly_args": len(node.args.kwonlyargs),
        "defaults": len(node.args.defaults),
        "decorators": [ast.unparse(d) for d in node.decorator_list],
    }


def _class_contract(node: ast.ClassDef) -> dict[str, Any]:
    methods = [
        _function_contract(child)
        for child in node.body
        if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef))
    ]
    return {
        "name": node.name,
        "lineno": node.lineno,
        "bases": [ast.unparse(base) for base in node.bases],
        "decorators": [ast.unparse(d) for d in node.decorator_list],
        "methods": methods,
    }


def _module_contract(rel_path: str) -> dict[str, Any]:
    file_path = ROOT / rel_path
    source = file_path.read_text(encoding="utf-8")
    source_hash = hashlib.sha256(source.encode("utf-8")).hexdigest()

    try:
        parsed = ast.parse(source)
    except SyntaxError as exc:
        return {
            "file": rel_path,
            "sha256": source_hash,
            "syntax_error": {
                "lineno": exc.lineno,
                "offset": exc.offset,
                "msg": exc.msg,
            },
        }

    functions: list[dict[str, Any]] = []
    classes: list[dict[str, Any]] = []
    top_level: list[dict[str, Any]] = []

    for node in parsed.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            functions.append(_function_contract(node))
        elif isinstance(node, ast.ClassDef):
            classes.append(_class_contract(node))
        elif isinstance(node, ast.Assign):
            names = _public_assignments(node)
            if names:
                top_level.append({"type": "Assign", "names": names, "lineno": node.lineno})
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            if not node.target.id.startswith("_"):
                top_level.append(
                    {"type": "AnnAssign", "name": node.target.id, "lineno": node.lineno}
                )
        elif not isinstance(node, ast.Expr):
            top_level.append({"type": type(node).__name__, "lineno": node.lineno})

    return {
        "file": rel_path,
        "sha256": source_hash,
        "docstring": bool(ast.get_docstring(parsed)),
        "imports": len([n for n in parsed.body if isinstance(n, (ast.Import, ast.ImportFrom))]),
        "functions": functions,
        "classes": classes,
        "top_level": top_level,
    }


def _recovery_registry_files() -> set[str]:
    files: set[str] = set()
    for line in RECOVERY_REGISTRY.read_text(encoding="utf-8").splitlines():
        normalized = line.strip()
        if normalized.startswith("file:"):
            files.add(normalized.split("file:", maxsplit=1)[1].strip())
    return files


def test_batch_001_003_contract_snapshot() -> None:
    # Invariant: module-level contracts (including syntax-error state) stay stable across refactors.
    paths = _load_batch_paths()
    contracts = [_module_contract(path) for path in paths]
    expected = json.loads(CONTRACT_SNAPSHOT_PATH.read_text(encoding="utf-8"))
    assert contracts == expected


def test_batch_001_003_registry_coverage_snapshot() -> None:
    # Invariant: SSOT registry coverage for these batches cannot silently drift.
    paths = _load_batch_paths()
    registry_files = _recovery_registry_files()
    coverage = {
        "total_files": len(paths),
        "in_registry": [path for path in paths if path in registry_files],
        "missing_from_registry": [path for path in paths if path not in registry_files],
        "missing_from_disk": [path for path in paths if not (ROOT / path).exists()],
    }
    expected = json.loads(REGISTRY_SNAPSHOT_PATH.read_text(encoding="utf-8"))
    assert coverage == expected
