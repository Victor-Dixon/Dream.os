"""
Output Flywheel CLI - Phase 2 Pipelines
=======================================

Runs Output Flywheel pipelines (Phase 2) to generate artifacts from
`work_session.json` style inputs.

Usage examples:

    python tools/run_output_flywheel.py --session-file path/to/session.json
    python tools/run_output_flywheel.py --session-file path/to/session.json --pipeline build
    python tools/run_output_flywheel.py --session-file path/to/trade_session.json --pipeline trade

This is distinct from `run_publication.py`, which handles Phase 3
publication of already-generated artifacts.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

# Ensure project root on path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from systems.output_flywheel.pipelines.build_artifact import (  # type: ignore
    run_build_pipeline_from_file,
)
from systems.output_flywheel.pipelines.trade_artifact import (  # type: ignore
    run_trade_pipeline_from_file,
)
from systems.output_flywheel.pipelines.life_aria_artifact import (  # type: ignore
    run_life_aria_pipeline_from_file,
)


def _load_session(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Session file not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def _detect_pipeline(session: Dict[str, Any]) -> str:
    """Infer pipeline from session_type."""
    session_type = session.get("session_type", "build")
    if session_type == "trade":
        return "trade"
    if session_type == "life_aria":
        return "life_aria"
    return "build"


def run_pipeline(session_file: Path, pipeline: str | None = None) -> Tuple[str, Dict[str, Any]]:
    """
    Run the appropriate pipeline for a session file.

    Returns:
        (pipeline_name, outputs_dict)
    """
    session = _load_session(session_file)
    pipeline_to_run = pipeline or _detect_pipeline(session)

    if pipeline_to_run == "build":
        outputs = run_build_pipeline_from_file(session_file)
    elif pipeline_to_run == "trade":
        outputs = run_trade_pipeline_from_file(session_file)
    elif pipeline_to_run == "life_aria":
        outputs = run_life_aria_pipeline_from_file(session_file)
    else:
        raise ValueError(f"Unknown pipeline: {pipeline_to_run}")

    return pipeline_to_run, outputs


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Output Flywheel CLI - Run Phase 2 pipelines to generate artifacts"
    )

    parser.add_argument(
        "--session-file",
        type=str,
        required=True,
        help="Path to work_session.json-like file",
    )
    parser.add_argument(
        "--pipeline",
        type=str,
        choices=["build", "trade", "life_aria"],
        help="Pipeline to run (defaults based on session_type)",
    )

    args = parser.parse_args(argv)
    session_path = Path(args.session_file)

    try:
        pipeline_name, outputs = run_pipeline(session_path, args.pipeline)
    except Exception as exc:
        print(f"❌ Pipeline failed: {exc}")
        return 1

    print(f"✅ Pipeline '{pipeline_name}' completed successfully")
    session_out = outputs.get("session_output_path")
    if session_out:
        print(f"   Updated session written to: {session_out}")
    for key, value in outputs.items():
        if key.endswith("_path") and isinstance(value, str):
            print(f"   {key}: {value}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())


