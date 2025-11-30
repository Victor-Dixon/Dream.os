#!/usr/bin/env python3
"""
Passdown Validator - Session Transition Quality Assurance
==========================================================

Validates passdown.json completeness and quality before session handoff.
Ensures all required fields are present and properly formatted.

Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2025-01-27
V2 Compliant: <400 lines
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple


class PassdownValidator:
    """Validates passdown.json files for completeness."""

    REQUIRED_SECTIONS = [
        "agent_id",
        "agent_name",
        "session_date",
        "session_status",
        "last_updated",
        "deliverables",
        "next_actions",
        "gas_pipeline",
        "blockers",
        "coordination_status",
        "technical_state",
        "session_metrics",
        "handoff_notes",
    ]

    REQUIRED_DELIVERABLES = ["completed", "in_progress", "blocked"]
    REQUIRED_NEXT_ACTIONS = ["immediate", "short_term", "coordination"]
    REQUIRED_BLOCKERS = ["current", "resolved", "potential"]
    REQUIRED_GAS_PIPELINE = ["status", "current_level"]
    REQUIRED_HANDOFF_NOTES = ["key_achievements", "important_context", "warnings", "next_session_priorities"]

    def __init__(self, passdown_path: Path):
        """Initialize validator."""
        self.passdown_path = passdown_path
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.data: Dict = {}

    def validate(self) -> Tuple[bool, List[str], List[str]]:
        """Validate passdown.json file."""
        # Load file
        if not self.passdown_path.exists():
            return False, [f"❌ Passdown file not found: {self.passdown_path}"], []

        try:
            self.data = json.loads(self.passdown_path.read_text())
        except json.JSONDecodeError as e:
            return False, [f"❌ Invalid JSON: {e}"], []

        # Validate required sections
        self._validate_sections()
        self._validate_deliverables()
        self._validate_next_actions()
        self._validate_blockers()
        self._validate_gas_pipeline()
        self._validate_handoff_notes()
        self._validate_content_quality()

        is_valid = len(self.errors) == 0
        return is_valid, self.errors, self.warnings

    def _validate_sections(self):
        """Validate all required sections exist."""
        for section in self.REQUIRED_SECTIONS:
            if section not in self.data:
                self.errors.append(f"❌ Missing required section: {section}")

    def _validate_deliverables(self):
        """Validate deliverables structure."""
        if "deliverables" not in self.data:
            return

        deliverables = self.data["deliverables"]
        for field in self.REQUIRED_DELIVERABLES:
            if field not in deliverables:
                self.errors.append(f"❌ Missing deliverables.{field}")

        # Check for empty lists (warnings)
        if deliverables.get("completed") == []:
            self.warnings.append("⚠️ No completed deliverables listed")
        if deliverables.get("in_progress") == [] and deliverables.get("blocked") == []:
            self.warnings.append("⚠️ No in-progress or blocked items (may indicate incomplete session)")

    def _validate_next_actions(self):
        """Validate next_actions structure."""
        if "next_actions" not in self.data:
            return

        next_actions = self.data["next_actions"]
        for field in self.REQUIRED_NEXT_ACTIONS:
            if field not in next_actions:
                self.errors.append(f"❌ Missing next_actions.{field}")

        # Check for empty lists
        if next_actions.get("immediate") == []:
            self.warnings.append("⚠️ No immediate next actions listed")

    def _validate_blockers(self):
        """Validate blockers structure."""
        if "blockers" not in self.data:
            return

        blockers = self.data["blockers"]
        for field in self.REQUIRED_BLOCKERS:
            if field not in blockers:
                self.errors.append(f"❌ Missing blockers.{field}")

    def _validate_gas_pipeline(self):
        """Validate gas_pipeline structure."""
        if "gas_pipeline" not in self.data:
            return

        gas = self.data["gas_pipeline"]
        for field in self.REQUIRED_GAS_PIPELINE:
            if field not in gas:
                self.errors.append(f"❌ Missing gas_pipeline.{field}")

        # Validate status values
        valid_statuses = ["FULL", "FLOWING", "LOW", "EMPTY", "BLOCKED"]
        if gas.get("status") not in valid_statuses:
            self.warnings.append(f"⚠️ Unusual gas_pipeline.status: {gas.get('status')}")

    def _validate_handoff_notes(self):
        """Validate handoff_notes structure."""
        if "handoff_notes" not in self.data:
            return

        notes = self.data["handoff_notes"]
        for field in self.REQUIRED_HANDOFF_NOTES:
            if field not in notes:
                self.warnings.append(f"⚠️ Missing handoff_notes.{field} (recommended)")

    def _validate_content_quality(self):
        """Validate content quality and completeness."""
        # Check for meaningful content
        if "deliverables" in self.data:
            completed = self.data["deliverables"].get("completed", [])
            if len(completed) == 0:
                self.warnings.append("⚠️ No completed deliverables (session may be incomplete)")

        # Check session status
        status = self.data.get("session_status", "")
        if status not in ["COMPLETE", "IN_PROGRESS", "BLOCKED"]:
            self.warnings.append(f"⚠️ Unusual session_status: {status}")

        # Check for agent_id consistency
        agent_id = self.data.get("agent_id", "")
        if not agent_id.startswith("Agent-"):
            self.warnings.append(f"⚠️ Unusual agent_id format: {agent_id}")

    def generate_report(self) -> str:
        """Generate validation report."""
        is_valid, errors, warnings = self.validate()

        report = []
        report.append("=" * 70)
        report.append("📋 PASSDOWN VALIDATION REPORT")
        report.append("=" * 70)
        report.append(f"\n📁 File: {self.passdown_path}")
        report.append(f"✅ Status: {'VALID' if is_valid else 'INVALID'}")
        report.append(f"❌ Errors: {len(errors)}")
        report.append(f"⚠️ Warnings: {len(warnings)}")
        report.append("")

        if errors:
            report.append("❌ ERRORS (Must Fix):")
            report.append("-" * 70)
            for error in errors:
                report.append(f"  {error}")
            report.append("")

        if warnings:
            report.append("⚠️ WARNINGS (Recommended Fixes):")
            report.append("-" * 70)
            for warning in warnings:
                report.append(f"  {warning}")
            report.append("")

        if is_valid and not warnings:
            report.append("✅ All checks passed! Passdown is complete and ready for handoff.")
        elif is_valid:
            report.append("✅ Passdown is valid but has some warnings to consider.")
        else:
            report.append("❌ Passdown has errors that must be fixed before handoff.")

        report.append("=" * 70)

        return "\n".join(report)


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Validate passdown.json file")
    parser.add_argument(
        "passdown_file",
        nargs="?",
        type=Path,
        help="Path to passdown.json file (default: agent_workspaces/Agent-1/passdown.json)",
    )
    parser.add_argument("--agent", type=str, help="Agent ID (e.g., Agent-1)")

    args = parser.parse_args()

    # Determine passdown path
    if args.passdown_file:
        passdown_path = args.passdown_file
    elif args.agent:
        passdown_path = Path(f"agent_workspaces/{args.agent}/passdown.json")
    else:
        # Default to Agent-1
        passdown_path = Path("agent_workspaces/Agent-1/passdown.json")

    # Validate
    validator = PassdownValidator(passdown_path)
    report = validator.generate_report()
    print(report)

    # Exit code
    is_valid, errors, _ = validator.validate()
    return 0 if is_valid else 1


if __name__ == "__main__":
    sys.exit(main())

