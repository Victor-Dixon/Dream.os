from __future__ import annotations

import json
import subprocess
from pathlib import Path

import yaml


def _write_protocol(tmp_path: Path) -> Path:
    protocol = {
        "version": "1.3.0",
        "mode": "audit_only",
        "scope_globs": ["fixtures/**"],
        "exclude_globs": [],
        "supported_file_types": {
            ".py": {"line_prefix": "#"},
            ".js": {"line_prefix": "//"},
            ".ts": {"line_prefix": "//"},
        },
        "required_header_fields": {
            "full": ["Header-Variant", "Owner", "Purpose", "SSOT"],
            "utility": ["Header-Variant", "Owner", "Purpose"],
        },
        "utility_constraints": {"max_non_comment_non_blank_lines": 40},
        "placeholder_blocklist": ["TBD", "TODO", "FIXME", "???"],
        "license_detection": {"required_keywords": ["copyright", "license", "spdx"], "min_lines": 2},
        "exceptions": {
            "file": "exceptions.yaml",
            "valid_suppressed_checks": ["HDR001", "HDR002", "HDR003", "HDR004", "HDR005", "HDR006", "HDR007", "HDRW001"],
        },
        "baseline": {"file": "baseline.json"},
        "reports": {"json": "report.json", "markdown": "report.md"},
    }
    protocol_path = tmp_path / "protocol.yaml"
    protocol_path.write_text(yaml.safe_dump(protocol), encoding="utf-8")
    return protocol_path


def _run_case(tmp_path: Path, fixture_rel: str) -> dict:
    repo = tmp_path
    fixture_root = Path("tests/fixtures/file_header_protocol")
    target = repo / "fixtures"
    target.mkdir()
    src = fixture_root / fixture_rel
    for file in src.rglob("*"):
        if file.is_file():
            out = target / file.relative_to(src)
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(file.read_text(encoding="utf-8"), encoding="utf-8")
    _write_protocol(repo)
    (repo / "exceptions.yaml").write_text("exceptions: []\n", encoding="utf-8")
    script = Path.cwd() / "tools/file_header_validator.py"
    cmd = ["python", str(script), "validate", "--protocol", "protocol.yaml"]
    proc = subprocess.run(cmd, cwd=repo, check=True, capture_output=True, text=True)
    assert proc.returncode == 0
    return json.loads((repo / "report.json").read_text(encoding="utf-8"))


def test_valid_full_headers(tmp_path: Path) -> None:
    report = _run_case(tmp_path, "valid_full")
    assert not report["violations"]


def test_valid_utility_headers(tmp_path: Path) -> None:
    report = _run_case(tmp_path, "valid_utility")
    assert not report["violations"]


def test_missing_header(tmp_path: Path) -> None:
    report = _run_case(tmp_path, "missing")
    assert any(v["rule_id"] == "HDR001" for v in report["violations"])


def test_partial_header(tmp_path: Path) -> None:
    report = _run_case(tmp_path, "partial")
    assert any(v["rule_id"] == "HDR002" for v in report["violations"])


def test_invalid_placeholder_values(tmp_path: Path) -> None:
    report = _run_case(tmp_path, "invalid_placeholder")
    assert any(v["rule_id"] == "HDR003" for v in report["violations"])


def test_invalid_preheader_constructs(tmp_path: Path) -> None:
    report = _run_case(tmp_path, "invalid_preheader")
    assert any(v["rule_id"] == "HDR004" for v in report["violations"])


def test_comment_style_mismatch(tmp_path: Path) -> None:
    report = _run_case(tmp_path, "comment_mismatch")
    assert any(v["rule_id"] in {"HDR005", "HDR001"} for v in report["violations"])


def test_rename_parsing_destination_only(tmp_path: Path, monkeypatch) -> None:
    import importlib.util

    module_path = Path.cwd() / "tools/file_header_validator.py"
    spec = importlib.util.spec_from_file_location("fhv", module_path)
    import sys
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    sys.modules["fhv"] = mod
    spec.loader.exec_module(mod)

    protocol_path = _write_protocol(tmp_path)
    validator = mod.HeaderValidator(tmp_path, protocol_path, "touched_file_enforcement", True)

    class Proc:
        stdout = "R100\told.py\tfixtures/new_name.py\n"

    monkeypatch.setattr(subprocess, "run", lambda *args, **kwargs: Proc())
    changed = validator.changed_paths()
    assert "fixtures/new_name.py" in changed
    assert "old.py" not in changed


def test_expired_exception_detection(tmp_path: Path) -> None:
    repo = tmp_path
    target = repo / "fixtures"
    target.mkdir()
    src = Path("tests/fixtures/file_header_protocol/exceptions/expired.py")
    (target / "expired.py").write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
    _write_protocol(repo)
    (repo / "exceptions.yaml").write_text(
        """exceptions:
  - path: fixtures/expired.py
    owner: qa
    reason: expired fixture
    expires_on: 2000-01-01
    suppressed_checks: [HDR001]
""",
        encoding="utf-8",
    )
    script = Path.cwd() / "tools/file_header_validator.py"
    cmd = ["python", str(script), "validate", "--protocol", "protocol.yaml"]
    subprocess.run(cmd, cwd=repo, check=True)
    report = json.loads((repo / "report.json").read_text(encoding="utf-8"))
    assert any(v["rule_id"] == "HDR007" for v in report["violations"])
