"""
Trade → Artifact Pipeline
=========================

Implements T1–T5 for trade sessions:
T1: Normalize trades        → trade_processor.prepare_trade_journal_context
T2: Summarize performance   → trade_processor.build_social_trade_summary
T3: Extract lessons         → from session / derived defaults
T4: Generate journal        → trade_journal template
T5: Generate social thread  → social_post template
"""

from __future__ import annotations

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Tuple

from systems.output_flywheel.processors.trade_processor import (
    build_social_trade_summary,
    prepare_trade_journal_context,
)
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
        raise RuntimeError("jinja2 is required for trade pipeline templates")
    return Environment(
        loader=FileSystemLoader(str(TEMPLATE_ROOT)),
        autoescape=select_autoescape(enabled_extensions=("j2",)),
        trim_blocks=True,
        lstrip_blocks=True,
    )


def run_trade_pipeline(session: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """Execute Trade → Artifact pipeline for a single work session."""
    session_id = session.get("session_id", "unknown-session")
    logger.info("Running Trade → Artifact pipeline for session %s", session_id)

    # Initialize manifest system and register session
    manifest = ManifestSystem()
    manifest.register_session(session_id, session)

    ctx = prepare_trade_journal_context(session)

    env = _env()
    journal_tmpl = env.get_template("trade_journal.md.j2")
    social_tmpl = env.get_template("social_post.md.j2")

    artifacts_dir = OUTPUT_ROOT / "artifacts" / "trade"
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    # Trade journal
    journal_path = artifacts_dir / f"trade_journal_{session_id}.md"
    journal_path.write_text(journal_tmpl.render(**ctx), encoding="utf-8")

    # Social summary
    social_summary = build_social_trade_summary(ctx)
    social_context = {
        "title": f"Trading Session - {ctx['date']}",
        "platform": "twitter",
        "post_type": "Single",
        "date": ctx["date"],
        "main_post": social_summary,
        "thread_posts": [],
        "hashtags": ["tradingjournal", "buildinpublic"],
        "mentions": [],
        "character_count": len(social_summary),
        "session_id": session_id,
    }
    social_path = artifacts_dir / f"trade_social_{session_id}.md"
    social_path.write_text(social_tmpl.render(**social_context), encoding="utf-8")

    artifacts = session.get("artifacts") or {}
    artifacts.setdefault("trade_journal", {})
    artifacts.setdefault("social_post", {})
    artifacts["trade_journal"].update(
        {
            "generated": True,
            "path": str(journal_path.relative_to(PROJECT_ROOT)),
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
    pipeline_status["trade_artifact"] = "complete"

    session["artifacts"] = artifacts
    session["pipeline_status"] = pipeline_status

    # Register artifacts in manifest system with hash for duplicate detection
    artifact_paths = {
        "trade_journal": journal_path,
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
        "journal_path": str(journal_path),
        "social_path": str(social_path),
        "trade_context": ctx,
        "ssot_compliance": compliance,
    }
    return session, outputs


def run_trade_pipeline_from_file(session_path: Path) -> Dict[str, Any]:
    """Load session JSON, run trade pipeline, persist updated session."""
    data = json.loads(session_path.read_text(encoding="utf-8"))
    updated_session, outputs = run_trade_pipeline(data)

    sessions_dir = OUTPUT_ROOT / "sessions"
    sessions_dir.mkdir(parents=True, exist_ok=True)
    out_path = sessions_dir / f"{updated_session.get('session_id', 'session')}_trade.json"
    out_path.write_text(json.dumps(updated_session, indent=2), encoding="utf-8")

    logger.info("Updated trade session written to %s", out_path)
    outputs["session_output_path"] = str(out_path)
    return outputs


