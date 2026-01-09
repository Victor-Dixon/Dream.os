"""
Build → Artifact Pipeline
=========================

Implements S1–S6 for build sessions:
S1: Repo Scan          → repo_scanner.scan_repo_to_dict
S2: Story Extraction   → story_extractor.extract_story_from_session
S3: README Generation  → readme_generator.generate_readme
S4: Build-log          → build_log_generator.generate_build_log
S5: Social Post        → social_generator.generate_social_post
S6: Mark Ready         → update session pipeline_status + artifacts
"""

from __future__ import annotations

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Tuple

from systems.output_flywheel.processors.repo_scanner import scan_repo_to_dict
from systems.output_flywheel.processors.story_extractor import (
    extract_story_from_session,
    story_to_dict,
)
from systems.output_flywheel.processors.readme_generator import (
    ReadmeConfig,
    generate_readme,
)
from systems.output_flywheel.processors.build_log_generator import generate_build_log
from systems.output_flywheel.processors.social_generator import generate_social_post
from systems.output_flywheel.manifest_system import (
    ManifestSystem,
    calculate_artifact_hash,
)

logger = logging.getLogger(__name__)


# File is at systems/output_flywheel/pipelines/build_artifact.py
# parents[0] = pipelines, [1] = output_flywheel, [2] = systems, [3] = repo root
PROJECT_ROOT = Path(__file__).resolve().parents[3]
OUTPUT_ROOT = PROJECT_ROOT / "systems" / "output_flywheel" / "outputs"
TEMPLATE_ROOT = PROJECT_ROOT / "systems" / "output_flywheel" / "templates"


def _resolve_repo_path(session: Dict[str, Any]) -> str:
    source_data = session.get("source_data") or {}
    repo_path = source_data.get("repo_path")
    if isinstance(repo_path, str) and repo_path:
        return repo_path
    # Fallback to project root
    return str(PROJECT_ROOT)


def run_build_pipeline(session: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """
    Execute the Build → Artifact pipeline for a single work session.

    Returns:
        (updated_session, pipeline_outputs)
    """
    session_id = session.get("session_id", "unknown-session")
    logger.info("Running Build → Artifact pipeline for session %s", session_id)

    # Initialize manifest system and register session
    manifest = ManifestSystem()
    manifest.register_session(session_id, session)

    repo_path = _resolve_repo_path(session)
    repo_stats = scan_repo_to_dict(repo_path)

    story_summary = extract_story_from_session(session)
    story_dict = story_to_dict(story_summary)

    artifacts_dir = OUTPUT_ROOT / "artifacts"
    build_dir = artifacts_dir / "build"
    build_dir.mkdir(parents=True, exist_ok=True)

    # README
    repo_name = Path(repo_path).name or "repository"
    readme_cfg = ReadmeConfig(
        repo_name=repo_name,
        repo_url=None,
        template_path=TEMPLATE_ROOT / "README.md.j2",
        output_path=build_dir / repo_name / "README.generated.md",
    )
    readme_path = generate_readme(
        config=readme_cfg,
        story=story_dict,
        repo_stats=repo_stats,
        extra={
            "session_id": session_id,
            "generation_date": datetime.utcnow().strftime("%Y-%m-%d"),
        },
    )

    # Build-log
    build_log_dir = build_dir / repo_name
    build_log_path = generate_build_log(session, repo_stats, build_log_dir)

    # Social post
    social_dir = build_dir / repo_name / "social"
    social_template = TEMPLATE_ROOT / "social_post.md.j2"
    social_path = generate_social_post(
        story=story_dict,
        output_dir=social_dir,
        template_path=social_template,
        session_id=session_id,
    )

    # Update session dict with artifact + status info
    artifacts = session.get("artifacts") or {}
    artifacts.setdefault("readme", {})
    artifacts.setdefault("blog_post", {})
    artifacts.setdefault("social_post", {})

    artifacts["readme"].update(
        {
            "generated": True,
            "path": str(readme_path.relative_to(PROJECT_ROOT)),
            "status": "ready",
        }
    )
    artifacts["social_post"].update(
        {
            "generated": True,
            "path": str(social_path.relative_to(PROJECT_ROOT)),
            "status": "ready",
        }
    )
    artifacts.setdefault("build_log", {})
    artifacts["build_log"].update(
        {
            "generated": True,
            "path": str(build_log_path.relative_to(PROJECT_ROOT)),
            "status": "ready",
        }
    )

    pipeline_status = session.get("pipeline_status") or {}
    pipeline_status["build_artifact"] = "complete"

    session["artifacts"] = artifacts
    session["pipeline_status"] = pipeline_status

    # Register artifacts in manifest system with hash for duplicate detection
    artifact_paths = {
        "readme": readme_path,
        "build_log": build_log_path,
        "social_post": social_path,
    }
    for artifact_type, artifact_path in artifact_paths.items():
        if artifact_path and artifact_path.exists():
            artifact_hash = calculate_artifact_hash(artifact_path)
            manifest.register_artifact(
                session_id,
                artifact_type,
                str(artifact_path.relative_to(PROJECT_ROOT)),
                artifact_hash,
            )

    # Verify SSOT compliance
    compliance = manifest.verify_ssot_compliance()
    if not compliance["compliant"]:
        logger.warning(f"SSOT violations detected: {compliance['violations']}")
    if compliance["warnings"]:
        logger.info(f"SSOT warnings: {compliance['warnings']}")

    outputs: Dict[str, Any] = {
        "readme_path": str(readme_path),
        "build_log_path": str(build_log_path),
        "social_path": str(social_path),
        "repo_stats": repo_stats,
        "story": story_dict,
        "ssot_compliance": compliance,
    }

    return session, outputs


def run_build_pipeline_from_file(session_path: Path) -> Dict[str, Any]:
    """Helper to load a session JSON, run the pipeline, and persist results."""
    data = json.loads(session_path.read_text(encoding="utf-8"))
    updated_session, outputs = run_build_pipeline(data)

    # Persist updated session under outputs/sessions
    sessions_dir = OUTPUT_ROOT / "sessions"
    sessions_dir.mkdir(parents=True, exist_ok=True)
    out_path = sessions_dir / f"{updated_session.get('session_id', 'session')}_build.json"
    out_path.write_text(json.dumps(updated_session, indent=2), encoding="utf-8")

    logger.info("Updated build session written to %s", out_path)
    outputs["session_output_path"] = str(out_path)
    return outputs


