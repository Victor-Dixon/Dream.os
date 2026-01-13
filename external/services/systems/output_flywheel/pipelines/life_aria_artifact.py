"""
Life/Aria → Artifact Pipeline
=============================

Generates blog-style narrative and optional social post for
`session_type == "life_aria"` sessions.
"""

from __future__ import annotations

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Tuple

from systems.output_flywheel.processors.story_extractor import (
    extract_story_from_session,
    story_to_dict,
)
from systems.output_flywheel.processors.social_generator import generate_social_post
from systems.output_flywheel.manifest_system import (
    ManifestSystem,
    calculate_artifact_hash,
)

logger = logging.getLogger(__name__)

try:  # pragma: no cover - optional
    from jinja2 import Environment, FileSystemLoader, select_autoescape

    HAS_JINJA2 = True
except Exception:  # pragma: no cover
    HAS_JINJA2 = False
    Environment = None  # type: ignore


PROJECT_ROOT = Path(__file__).resolve().parents[3]
OUTPUT_ROOT = PROJECT_ROOT / "systems" / "output_flywheel" / "outputs"
TEMPLATE_ROOT = PROJECT_ROOT / "systems" / "output_flywheel" / "templates"


def _env() -> Any:
    if not HAS_JINJA2:
        raise RuntimeError("jinja2 is required for life_aria pipeline templates")
    return Environment(
        loader=FileSystemLoader(str(TEMPLATE_ROOT)),
        autoescape=select_autoescape(enabled_extensions=("j2",)),
        trim_blocks=True,
        lstrip_blocks=True,
    )


def run_life_aria_pipeline(session: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """Execute Life/Aria → Artifact pipeline for a single work session."""
    session_id = session.get("session_id", "unknown-session")
    logger.info("Running Life/Aria → Artifact pipeline for session %s", session_id)

    # Initialize manifest system and register session
    manifest = ManifestSystem()
    manifest.register_session(session_id, session)

    story_summary = extract_story_from_session(session)
    story_dict = story_to_dict(story_summary)

    env = _env()
    blog_template = env.get_template("blog_post.md.j2")

    artifacts_dir = OUTPUT_ROOT / "artifacts" / "life_aria"
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    # Blog post
    blog_path = artifacts_dir / f"blog_{session_id}.md"
    blog_context: Dict[str, Any] = {
        "title": story_dict.get("title") or "Aria Session Devlog",
        "date": datetime.utcnow().strftime("%Y-%m-%d"),
        "session_type": session.get("session_type", "life_aria"),
        "agent_id": session.get("agent_id", "Agent-?"),
        "overview": story_dict.get("overview"),
        "problem": story_dict.get("problem"),
        "solution": story_dict.get("solution"),
        "metrics": [],
        "stats": session.get("metadata") or {},
        "lessons": story_dict.get("lessons") or [],
        "code_snippets": [],
        "screenshots": [],
        "next_steps": story_dict.get("next_steps") or [],
        "related_work": [],
        "session_id": session_id,
    }
    blog_path.write_text(blog_template.render(**blog_context), encoding="utf-8")

    # Social post
    social_dir = artifacts_dir / "social"
    social_template = TEMPLATE_ROOT / "social_post.md.j2"
    social_path = generate_social_post(
        story=story_dict,
        output_dir=social_dir,
        template_path=social_template,
        session_id=session_id,
        hashtags=["dreamos", "buildinpublic"],
    )

    artifacts = session.get("artifacts") or {}
    artifacts.setdefault("blog_post", {})
    artifacts.setdefault("social_post", {})
    artifacts["blog_post"].update(
        {
            "generated": True,
            "path": str(blog_path.relative_to(PROJECT_ROOT)),
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

    pipeline_status = session.get("pipeline_status") or {}
    pipeline_status["life_aria_artifact"] = "complete"

    session["artifacts"] = artifacts
    session["pipeline_status"] = pipeline_status

    # Register artifacts in manifest system with hash for duplicate detection
    artifact_paths = {
        "blog_post": blog_path,
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
        "blog_path": str(blog_path),
        "social_path": str(social_path),
        "story": story_dict,
        "ssot_compliance": compliance,
    }
    return session, outputs


def run_life_aria_pipeline_from_file(session_path: Path) -> Dict[str, Any]:
    """Load session JSON, run life/aria pipeline, persist updated session."""
    data = json.loads(session_path.read_text(encoding="utf-8"))
    updated_session, outputs = run_life_aria_pipeline(data)

    sessions_dir = OUTPUT_ROOT / "sessions"
    sessions_dir.mkdir(parents=True, exist_ok=True)
    out_path = sessions_dir / f"{updated_session.get('session_id', 'session')}_life_aria.json"
    out_path.write_text(json.dumps(updated_session, indent=2), encoding="utf-8")

    logger.info("Updated life_aria session written to %s", out_path)
    outputs["session_output_path"] = str(out_path)
    return outputs


