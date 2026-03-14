"""Standalone validation audit server stub for tests."""

from __future__ import annotations


def check_php_syntax(site_key: str, file_path: str) -> dict[str, str]:
    return {
        "site": site_key,
        "file": file_path,
        "status": "ok",
        "detail": "syntax check skipped in test environment",
    }
