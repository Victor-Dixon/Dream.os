# <!-- SSOT Domain: trading_robot -->
"""CLI entrypoints for TSLA morning report workflow."""
from __future__ import annotations

import argparse
import json
import uuid
from datetime import datetime, timezone, timedelta
from typing import Any

from ..ledger.db import Ledger
from ..ledger.scoring import score_recommendations
from ..publisher.discord import post_to_discord
from ..reports.renderer import render_report
from ..reporting import archive_artifacts, build_snapshot, get_market_provider, snapshot_hash


def run_morning_report(args: argparse.Namespace) -> int:
    provider = get_market_provider()
    snapshot, _ = build_snapshot(args.symbol, provider)
    for rec in snapshot["recommendations"]:
        rec["rec_id"] = str(uuid.uuid4())
        rec["ticker"] = snapshot["ticker"]
    report = render_report(snapshot)
    archive_artifacts(snapshot, report.markdown, report.payload)
    ledger = Ledger()
    snap_hash = snapshot_hash(snapshot)
    for rec in snapshot["recommendations"]:
        rec["snapshot_hash"] = snap_hash
    ledger.save_snapshot(snap_hash, snapshot)
    ledger.save_recommendations(snapshot["recommendations"], snapshot["regime"], snap_hash)
    publish_result = post_to_discord(report.payload, dry_run=args.dry_run)
    if args.dry_run:
        print(publish_result.response_text)
    elif not publish_result.posted:
        print(f"Discord publish failed: {publish_result.response_text}")
    return 0


def run_score_recommendations(args: argparse.Namespace) -> int:
    ledger = Ledger()
    provider = get_market_provider()
    date_prefix = args.date or datetime.now(timezone.utc).date().isoformat()
    recs = ledger.fetch_recommendations_by_date(date_prefix)
    scored = score_recommendations(provider, recs, slippage=args.slippage)
    for score in scored:
        ledger.save_score(score.__dict__)
    print(json.dumps([score.__dict__ for score in scored], indent=2))
    return 0


def run_weekly_summary(args: argparse.Namespace) -> int:
    ledger = Ledger()
    since_date = (datetime.now(timezone.utc) - timedelta(days=7)).date().isoformat()
    rows = ledger.fetch_weekly_summary(since_date)
    summary = [
        {
            "setup_type": row[0],
            "count": row[1],
            "avg_r": round(row[2] or 0, 2),
            "wins": row[3],
        }
        for row in rows
    ]
    print(json.dumps(summary, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="TSLA report CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    report = subparsers.add_parser("morning_report")
    report.add_argument("--symbol", default="TSLA")
    report.add_argument("--dry-run", action="store_true")
    report.set_defaults(func=run_morning_report)

    score = subparsers.add_parser("score_recommendations")
    score.add_argument("--date", help="YYYY-MM-DD")
    score.add_argument("--slippage", type=float, default=0.02)
    score.set_defaults(func=run_score_recommendations)

    weekly = subparsers.add_parser("weekly_summary")
    weekly.set_defaults(func=run_weekly_summary)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
