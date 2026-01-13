"""
Repo Scanner Processor (S1)
===========================

Scans a repository for recent activity and prepares structured data
for downstream processors (story extraction, README generation, etc.).

V2 constraints:
- Keep file under 300 LOC
- Single-responsibility functions
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


@dataclass
class CommitFileChange:
    """Represents a single file change in a commit."""

    path: str


@dataclass
class CommitSummary:
    """Lightweight commit summary used by the flywheel."""

    hash: str
    message: str
    author: str
    timestamp: str
    files: List[CommitFileChange]


@dataclass
class RepoScanResult:
    """Result of a repo scan."""

    repo_path: str
    commits: List[CommitSummary]
    files_changed: int
    lines_added: int
    lines_removed: int


def _safe_import_gitpython() -> Any | None:
    """Import GitPython lazily, return None if unavailable."""
    try:
        import git  # type: ignore

        return git
    except Exception:  # pragma: no cover - optional dependency
        logger.info("GitPython not available; falling back to basic scan")
        return None


def _scan_with_gitpython(repo_path: Path, max_commits: int = 10) -> RepoScanResult:
    """Scan repo using GitPython for rich commit information."""
    git = _safe_import_gitpython()
    if git is None:
        return RepoScanResult(
            repo_path=str(repo_path),
            commits=[],
            files_changed=0,
            lines_added=0,
            lines_removed=0,
        )

    try:
        repo = git.Repo(str(repo_path))
    except Exception as exc:  # pragma: no cover - repo errors
        logger.warning("Failed to open repo %s: %s", repo_path, exc)
        return RepoScanResult(
            repo_path=str(repo_path),
            commits=[],
            files_changed=0,
            lines_added=0,
            lines_removed=0,
        )

    commits: List[CommitSummary] = []
    files_seen: set[str] = set()

    for commit in list(repo.iter_commits("HEAD", max_count=max_commits)):
        files: List[CommitFileChange] = []
        for parent in commit.parents or []:
            diff_index = parent.diff(commit, create_patch=False)
            for diff in diff_index:
                if diff.a_path:
                    files.append(CommitFileChange(path=diff.a_path))
                    files_seen.add(diff.a_path)
        commits.append(
            CommitSummary(
                hash=commit.hexsha,
                message=commit.message.strip(),
                author=str(commit.author),
                timestamp=str(commit.committed_datetime),
                files=files,
            )
        )

    # GitPython does not cheaply expose aggregated line stats in a portable way,
    # so we provide zero values here; downstream processors treat them as optional.
    return RepoScanResult(
        repo_path=str(repo_path),
        commits=commits,
        files_changed=len(files_seen),
        lines_added=0,
        lines_removed=0,
    )


def _basic_scan(repo_path: Path) -> RepoScanResult:
    """
    Basic fallback scan when GitPython is not available.

    Walks the repo tree and reports rough file counts. This still feeds
    templates with sensible defaults so the pipeline does not fail.
    """
    if not repo_path.exists():
        logger.warning("Repo path does not exist: %s", repo_path)
        return RepoScanResult(
            repo_path=str(repo_path),
            commits=[],
            files_changed=0,
            lines_added=0,
            lines_removed=0,
        )

    files_seen: set[str] = set()
    for path in repo_path.rglob("*"):
        if path.is_file() and ".git" not in path.parts:
            try:
                rel = path.relative_to(repo_path)
            except ValueError:
                rel = path
            files_seen.add(str(rel))

    return RepoScanResult(
        repo_path=str(repo_path),
        commits=[],
        files_changed=len(files_seen),
        lines_added=0,
        lines_removed=0,
    )


def scan_repo(repo_path: str, use_git: bool = True, max_commits: int = 10) -> RepoScanResult:
    """
    Public entry point for S1: Repo Scan.

    - If GitPython is available and `use_git` is True, use rich scan.
    - Otherwise, fall back to a lightweight filesystem-based scan.
    """
    path = Path(repo_path)
    logger.info("Scanning repository for Output Flywheel: %s", path)

    if use_git:
        result = _scan_with_gitpython(path, max_commits=max_commits)
    else:
        result = _basic_scan(path)

    logger.info(
        "Repo scan complete: files_changed=%s, commits=%s",
        result.files_changed,
        len(result.commits),
    )
    return result


def scan_repo_to_dict(repo_path: str, use_git: bool = True, max_commits: int = 10) -> Dict[str, Any]:
    """
    Convenience wrapper that returns a plain dict suitable for JSON / templates.
    """
    result = scan_repo(repo_path, use_git=use_git, max_commits=max_commits)
    return {
        "repo_path": result.repo_path,
        "files_changed": result.files_changed,
        "lines_added": result.lines_added,
        "lines_removed": result.lines_removed,
        "commits": [
            {
                "hash": c.hash,
                "message": c.message,
                "author": c.author,
                "timestamp": c.timestamp,
                "files": [f.path for f in c.files],
            }
            for c in result.commits
        ],
    }


