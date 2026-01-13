"""
README Generator Processor (S3)
===============================

Renders a README.md artifact from:
- repo scan data (files_changed, commits)
- story summary (overview, features, etc.)
- configuration preferences

Uses the Jinja2 template at `systems/output_flywheel/templates/README.md.j2`.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

try:  # pragma: no cover - optional dependency
    from jinja2 import Environment, FileSystemLoader, select_autoescape

    HAS_JINJA2 = True
except Exception:  # pragma: no cover - library may not be installed
    HAS_JINJA2 = False
    Environment = None  # type: ignore


@dataclass
class ReadmeConfig:
    repo_name: str
    repo_url: Optional[str]
    template_path: Path
    output_path: Path


def _build_env(template_dir: Path) -> Any:
    if not HAS_JINJA2:
        raise RuntimeError("jinja2 is required to render README templates")
    return Environment(
        loader=FileSystemLoader(str(template_dir)),
        autoescape=select_autoescape(enabled_extensions=("j2",)),
        trim_blocks=True,
        lstrip_blocks=True,
    )


def generate_readme(
    config: ReadmeConfig,
    story: Dict[str, Any],
    repo_stats: Dict[str, Any],
    extra: Optional[Dict[str, Any]] = None,
) -> Path:
    """
    Generate README.md using the configured template and data.

    Args:
        config: ReadmeConfig with template/output locations.
        story: Story dict from story_extractor.story_to_dict.
        repo_stats: Repo dict from repo_scanner.scan_repo_to_dict.
        extra: Optional additional context (architecture, docs, etc.).

    Returns:
        Path to generated README file.
    """
    template_file = config.template_path
    template_dir = template_file.parent
    env = _build_env(template_dir)
    template = env.get_template(template_file.name)

    commits: List[Dict[str, Any]] = repo_stats.get("commits") or []
    stats = {
        "files_changed": repo_stats.get("files_changed", 0),
        "commits": len(commits),
        "lines_added": repo_stats.get("lines_added", 0),
        "lines_removed": repo_stats.get("lines_removed", 0),
    }

    context: Dict[str, Any] = {
        "repo_name": config.repo_name,
        "repo_url": config.repo_url,
        "description": story.get("overview"),
        "overview": story.get("overview"),
        "features": (extra or {}).get("features", []),
        "prerequisites": (extra or {}).get("prerequisites", []),
        "install_commands": (extra or {}).get("install_commands", []),
        "usage_examples": (extra or {}).get("usage_examples", []),
        "recent_commits": commits,
        "stats": stats,
        "architecture": (extra or {}).get("architecture"),
        "documentation": (extra or {}).get("documentation", []),
        "contributing": (extra or {}).get("contributing"),
        "license": (extra or {}).get("license"),
        "links": (extra or {}).get("links", []),
        "badges": (extra or {}).get("badges", []),
        "session_id": (extra or {}).get("session_id"),
        "generation_date": (extra or {}).get("generation_date"),
    }

    output_path = config.output_path
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_text = template.render(**context)
    output_path.write_text(output_text, encoding="utf-8")

    logger.info("README generated at %s", output_path)
    return output_path


