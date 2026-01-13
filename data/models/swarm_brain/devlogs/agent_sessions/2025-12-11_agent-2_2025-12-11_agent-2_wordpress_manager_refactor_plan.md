# Agent-2 Stall Recovery Slice — WordPress Manager Refactor Plan (2025-12-11)

## Task
- Produce a concrete refactor plan for `tools/wordpress_manager.py` to meet V2 LOC and modularity standards.

## Findings
- File size ~1062 lines; header claims "<400" — noncompliant with V2 LOC target.
- Responsibilities bundled: connection mgmt, deployment, content ops, DB/menu/WP-CLI helpers, env handling.
- Paramiko optional; no structured dry-run/smoke harness for safe changes.

## Plan (Sliceable)
- Phase 1 (safety shell): add `--dry-run` flag and logging redaction audit; create small smoke harness using mocks for SFTP/WP-CLI calls.
- Phase 2 (modularization): split into modules (`wordpress/connection.py`, `wordpress/deploy.py`, `wordpress/wp_cli.py`, `wordpress/content.py`, `wordpress/menu.py`) with a thin orchestrator.
- Phase 3 (tests): add unit tests for dry-run + arg parsing; add contract tests for connection retries/backoff and env loading.
- Phase 4 (ops): publish quick operator guide and dependency check (`paramiko`, `python-dotenv`) with install hints.

## Immediate Next Slice
- Implement `--dry-run` flag around deploy/CLI operations with no remote side effects and add minimal smoke test harness.

## Status
- ✅ Artifact produced (refactor plan). No code changes yet; ready to execute next slice.

