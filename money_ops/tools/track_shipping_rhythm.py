#!/usr/bin/env python3
"""
Shipping Rhythm Tracker
========================

Tracks weekly shipping artifacts and verifies minimum shipping targets are met.
Integrates with output_flywheel logs when available.

Usage:
    python track_shipping_rhythm.py
    python track_shipping_rhythm.py --week 2025-12-01
    python track_shipping_rhythm.py --add-artifact "Repo README Update" --type repo
"""

import argparse
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List

import yaml


class ShippingRhythmTracker:
    """Tracks weekly shipping rhythm and artifacts."""

    def __init__(self, rhythm_path: Path):
        """Initialize tracker with shipping rhythm file."""
        self.rhythm_path = rhythm_path
        self.rhythm: Dict[str, Any] = {}

    def load_rhythm(self):
        """Load shipping rhythm YAML file."""
        try:
            if self.rhythm_path.exists():
                with open(self.rhythm_path, "r", encoding="utf-8") as f:
                    self.rhythm = yaml.safe_load(f) or {}
            else:
                # Initialize default structure
                self.rhythm = {
                    "version": "1.0",
                    "last_updated": datetime.now().isoformat(),
                    "baseline_rhythm": {
                        "weekly_targets": {
                            "repo_artifacts": 1,
                            "narrative_artifacts": 1,
                            "total_minimum": 2,
                        },
                    },
                    "weeks": [],
                    "current_week": {},
                }
        except Exception as e:
            print(f"❌ Error loading shipping rhythm: {e}", file=sys.stderr)
            sys.exit(1)

    def save_rhythm(self):
        """Save shipping rhythm YAML file."""
        self.rhythm["last_updated"] = datetime.now().isoformat()
        try:
            self.rhythm_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.rhythm_path, "w", encoding="utf-8") as f:
                yaml.dump(self.rhythm, f, default_flow_style=False, sort_keys=False)
        except Exception as e:
            print(f"❌ Error saving shipping rhythm: {e}", file=sys.stderr)
            sys.exit(1)

    def get_current_week_range(self, date: datetime = None) -> tuple:
        """Get current week start and end dates."""
        if date is None:
            date = datetime.now()

        # Get Monday of current week
        days_since_monday = date.weekday()
        week_start = date - timedelta(days=days_since_monday)
        week_end = week_start + timedelta(days=6)

        return week_start.date(), week_end.date()

    def get_or_create_current_week(self, date: datetime = None) -> Dict[str, Any]:
        """Get or create current week entry."""
        week_start, week_end = self.get_current_week_range(date)
        week_start_str = week_start.isoformat()
        week_end_str = week_end.isoformat()

        # Check if current week exists
        current_week_data = self.rhythm.get("current_week", {})
        if current_week_data.get("week_start") == week_start_str:
            return current_week_data

        # Close previous week if exists
        if current_week_data:
            self._close_week(current_week_data)

        # Create new week
        baseline = self.rhythm.get("baseline_rhythm", {}).get("weekly_targets", {})
        new_week = {
            "week_start": week_start_str,
            "week_end": week_end_str,
            "repo_artifacts": [],
            "narrative_artifacts": [],
            "bonus_artifacts": [],
            "total_shipped": 0,
            "target_met": False,
        }

        self.rhythm["current_week"] = new_week
        return new_week

    def _close_week(self, week_data: Dict[str, Any]):
        """Close a week and move to weeks log."""
        if "weeks" not in self.rhythm:
            self.rhythm["weeks"] = []

        baseline = self.rhythm.get("baseline_rhythm", {}).get("weekly_targets", {})
        total_minimum = baseline.get("total_minimum", 2)

        repo_count = len(week_data.get("repo_artifacts", []))
        narrative_count = len(week_data.get("narrative_artifacts", []))
        total_shipped = repo_count + narrative_count

        week_data["total_shipped"] = total_shipped
        week_data["target_met"] = total_shipped >= total_minimum

        # If target not met, add to missed weeks
        if not week_data["target_met"]:
            if "missed_weeks" not in self.rhythm:
                self.rhythm["missed_weeks"] = []

            self.rhythm["missed_weeks"].append({
                "week_start": week_data["week_start"],
                "reason": "Less than 2 artifacts shipped",
                "catch_up_plan": "Schedule explicit make-up work",
                "catch_up_completed": False,
            })

        self.rhythm["weeks"].append(week_data)

    def add_artifact(
        self,
        title: str,
        artifact_type: str,
        date: str = None,
        url: str = None,
        output_flywheel_reference: str = None,
    ):
        """Add an artifact to current week."""
        if date is None:
            date = datetime.now().isoformat()[:10]

        current_week = self.get_or_create_current_week()

        artifact = {
            "date": date,
            "title": title,
            "type": artifact_type,
        }

        if url:
            artifact["url"] = url
        if output_flywheel_reference:
            artifact["output_flywheel_reference"] = output_flywheel_reference

        # Categorize artifact
        baseline = self.rhythm.get("baseline_rhythm", {}).get("weekly_targets", {})
        repo_types = ["repo", "readme", "demo", "docs", "upgrade"]
        narrative_types = ["devlog", "trading_breakdown", "system_doc", "narrative"]

        artifact_type_lower = artifact_type.lower()

        if any(rt in artifact_type_lower for rt in repo_types):
            current_week["repo_artifacts"].append(artifact)
        elif any(nt in artifact_type_lower for nt in narrative_types):
            current_week["narrative_artifacts"].append(artifact)
        else:
            current_week["bonus_artifacts"].append(artifact)

        # Update totals
        repo_count = len(current_week.get("repo_artifacts", []))
        narrative_count = len(current_week.get("narrative_artifacts", []))
        total_minimum = baseline.get("total_minimum", 2)
        current_week["total_shipped"] = repo_count + narrative_count
        current_week["target_met"] = current_week["total_shipped"] >= total_minimum

        self.rhythm["current_week"] = current_week
        self.save_rhythm()

        print(f"✅ Added artifact: {title} ({artifact_type})")
        print(f"   Week total: {current_week['total_shipped']}/{total_minimum} artifacts\n")

    def get_week_status(self, week_start: str = None) -> Dict[str, Any]:
        """Get status for a specific week."""
        if week_start is None:
            current_week = self.get_or_create_current_week()
            week_start = current_week["week_start"]

        # Check current week
        current_week_data = self.rhythm.get("current_week", {})
        if current_week_data.get("week_start") == week_start:
            return current_week_data

        # Check archived weeks
        for week in self.rhythm.get("weeks", []):
            if week.get("week_start") == week_start:
                return week

        return {}

    def print_status(self, week_start: str = None):
        """Print current week status."""
        status = self.get_week_status(week_start)

        if not status:
            print("❌ Week not found")
            return

        baseline = self.rhythm.get("baseline_rhythm", {}).get("weekly_targets", {})
        total_minimum = baseline.get("total_minimum", 2)

        print("\n" + "=" * 70)
        print("📦 SHIPPING RHYTHM STATUS")
        print("=" * 70 + "\n")

        print(f"Week: {status.get('week_start')} to {status.get('week_end')}")
        print(f"Target: {total_minimum} artifacts (1 repo + 1 narrative)\n")

        repo_count = len(status.get("repo_artifacts", []))
        narrative_count = len(status.get("narrative_artifacts", []))
        total_shipped = status.get("total_shipped", 0)

        print(f"Repo Artifacts: {repo_count}/1")
        if status.get("repo_artifacts"):
            for artifact in status["repo_artifacts"]:
                print(f"  • {artifact.get('title')} ({artifact.get('date')})")

        print(f"\nNarrative Artifacts: {narrative_count}/1")
        if status.get("narrative_artifacts"):
            for artifact in status["narrative_artifacts"]:
                print(f"  • {artifact.get('title')} ({artifact.get('date')})")

        print(f"\nTotal Shipped: {total_shipped}/{total_minimum}")
        print(f"Target Met: {'✅ YES' if status.get('target_met') else '❌ NO'}")

        if not status.get("target_met"):
            needed = total_minimum - total_shipped
            print(f"\n⚠️  Need {needed} more artifact(s) to meet weekly target")

        print("\n" + "=" * 70 + "\n")


def main():
    """Main execution."""
    parser = argparse.ArgumentParser(
        description="Track weekly shipping rhythm"
    )
    parser.add_argument(
        "--week",
        type=str,
        help="Week start date (YYYY-MM-DD) to check status"
    )
    parser.add_argument(
        "--add-artifact",
        type=str,
        help="Add an artifact to current week"
    )
    parser.add_argument(
        "--type",
        type=str,
        choices=["repo", "narrative", "bonus"],
        help="Artifact type (repo, narrative, bonus)"
    )
    parser.add_argument(
        "--url",
        type=str,
        help="URL for the artifact"
    )
    parser.add_argument(
        "--rhythm-file",
        type=str,
        default="shipping_rhythm.yaml",
        help="Path to shipping rhythm YAML file"
    )

    args = parser.parse_args()

    # Resolve path
    rhythm_path = Path(args.rhythm_file)
    if not rhythm_path.is_absolute():
        rhythm_path = Path(__file__).parent.parent / rhythm_path

    # Initialize tracker
    tracker = ShippingRhythmTracker(rhythm_path)
    tracker.load_rhythm()

    # Add artifact
    if args.add_artifact:
        if not args.type:
            print("❌ --type required when adding artifact", file=sys.stderr)
            sys.exit(1)
        tracker.add_artifact(
            title=args.add_artifact,
            artifact_type=args.type,
            url=args.url,
        )
        tracker.save_rhythm()
        return

    # Print status
    tracker.print_status(week_start=args.week)


if __name__ == "__main__":
    main()




