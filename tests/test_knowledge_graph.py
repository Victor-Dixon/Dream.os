"""Tests for snapshot knowledge graph tooling."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import importlib.util


def _load_module(module_path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


ROOT = Path(__file__).resolve().parents[1]
SNAPSHOTS_DIR = ROOT / "tests" / "snapshots"
REGISTRY_PATH = ROOT / "docs" / "recovery" / "recovery_registry.yaml"
BUILD_MODULE = _load_module(ROOT / "scripts" / "build_knowledge_graph.py", "build_knowledge_graph")
DIFF_MODULE = _load_module(ROOT / "scripts" / "snapshot_diff_summary.py", "snapshot_diff_summary")


def test_build_graph_contains_known_modules_and_registry_ids() -> None:
    graph = BUILD_MODULE.build_graph_from_snapshots(SNAPSHOTS_DIR, REGISTRY_PATH)

    error_handling = graph["modules"]["src/core/error_handling.py"]
    validation_engine = graph["modules"]["src/core/engines/validation_core_engine.py"]
    gas_pipeline_init = graph["modules"]["src/core/gas_pipeline/core/__init__.py"]

    assert error_handling["has_syntax_error"] is False
    assert validation_engine["has_syntax_error"] is False
    assert gas_pipeline_init["has_syntax_error"] is False

    assert error_handling["registry_id"] == "core-error-handling-logger-shim"
    assert validation_engine["registry_id"] == "core-validation-core-engine"
    assert gas_pipeline_init["registry_id"] == "core-gas-pipeline-core-package"


def test_build_script_is_idempotent(tmp_path: Path) -> None:
    out1 = tmp_path / "graph1.json"
    out2 = tmp_path / "graph2.json"

    cmd = [
        sys.executable,
        str(ROOT / "scripts" / "build_knowledge_graph.py"),
        "--snapshots-dir",
        str(SNAPSHOTS_DIR),
        "--registry",
        str(REGISTRY_PATH),
        "--output",
    ]
    subprocess.run(cmd + [str(out1)], check=True)
    subprocess.run(cmd + [str(out2)], check=True)

    assert out1.read_text(encoding="utf-8") == out2.read_text(encoding="utf-8")


def test_diff_summary_detects_expected_syntax_fix_and_no_unexpected_changes() -> None:
    old_graph = {
        "modules": {
            "src/core/error_handling.py": {
                "has_syntax_error": True,
                "functions": [],
                "classes": [],
                "in_registry": False,
                "registry_id": None,
            },
            "src/core/unchanged.py": {
                "has_syntax_error": False,
                "functions": [],
                "classes": [],
                "in_registry": True,
                "registry_id": "unchanged-id",
            },
        },
        "registry_entries": {"unchanged-id": "src/core/unchanged.py"},
    }
    new_graph = {
        "modules": {
            "src/core/error_handling.py": {
                "has_syntax_error": False,
                "functions": [{"name": "log_error", "signature": "(args=1, kwonly=0, defaults=0)"}],
                "classes": [{"name": "ErrorHandler", "methods": []}],
                "in_registry": True,
                "registry_id": "core-error-handling-logger-shim",
            },
            "src/core/unchanged.py": {
                "has_syntax_error": False,
                "functions": [],
                "classes": [],
                "in_registry": True,
                "registry_id": "unchanged-id",
            },
        },
        "registry_entries": {
            "unchanged-id": "src/core/unchanged.py",
            "core-error-handling-logger-shim": "src/core/error_handling.py",
        },
    }

    summary, has_unexpected = DIFF_MODULE.summarize_diff(
        old_graph,
        new_graph,
        expected_prefixes=["src/core/"],
    )

    assert "Fixed (error → valid)" in summary
    assert "`src/core/error_handling.py`" in summary
    assert "Registry IDs added" in summary
    assert has_unexpected is False


def test_latest_graph_file_parses() -> None:
    path = ROOT / "knowledge_graph" / "latest.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    assert "modules" in data
    assert "registry_entries" in data
