"""CLI entrypoint for Graph Nexus."""

from __future__ import annotations

import argparse
import logging
from pathlib import Path
from typing import Sequence

from .ingest.from_project_scanner import ProjectScannerAdapter
from .store.graph_repository import GraphRepository

DEFAULT_SCANNER_OUTPUT = "artifacts/scanner/scan.json"
DEFAULT_DB_PATH = "graph.sqlite"

logger = logging.getLogger(__name__)


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser."""
    parser = argparse.ArgumentParser(description="Graph Nexus CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    index_parser = subparsers.add_parser(
        "index", help="Ingest scanner output and store graph"
    )
    index_parser.add_argument("project_path", nargs="?", default=".")
    index_parser.add_argument("--scanner-output", default=DEFAULT_SCANNER_OUTPUT)
    index_parser.add_argument("--db-path", default=DEFAULT_DB_PATH)
    index_parser.add_argument("--incremental", action="store_true")

    scanner_group = index_parser.add_mutually_exclusive_group()
    scanner_group.add_argument("--use-project-scanner", action="store_true")
    scanner_group.add_argument("--no-project-scanner", action="store_false")
    index_parser.set_defaults(use_project_scanner=True)

    return parser


def run_index(args: argparse.Namespace) -> int:
    """Run the index pipeline."""
    if not args.use_project_scanner:
        logger.warning("Project scanner disabled; no ingest performed.")
        return 0

    scan_path = Path(args.scanner_output)
    if not scan_path.exists():
        logger.error("Scanner output not found: %s", scan_path)
        return 1

    project_root = Path(args.project_path).resolve()
    repository = GraphRepository(Path(args.db_path))
    adapter = ProjectScannerAdapter(project_root=project_root)
    result = adapter.ingest(scan_path, repository)

    logger.info("Ingested %s nodes and %s edges.", result.node_count, result.edge_count)
    if args.incremental:
        logger.info("Incremental mode requested; no incremental logic implemented yet.")
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    """CLI entrypoint."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "index":
        return run_index(args)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
