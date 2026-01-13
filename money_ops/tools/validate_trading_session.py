#!/usr/bin/env python3
"""
Trading Rules Engine Validator
===============================

Validates trading session logs against trading_rules.yaml to generate
rule-compliance reports.

Usage:
    python validate_trading_session.py trading_session_2025-12-01.yaml
    python validate_trading_session.py trading_session_2025-12-01.yaml --rules trading_rules.yaml
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

import yaml


class TradingSessionValidator:
    """Validates trading sessions against trading rules."""

    def __init__(self, rules_path: Path, session_path: Path):
        """Initialize validator with rules and session files."""
        self.rules_path = rules_path
        self.session_path = session_path
        self.rules: Dict[str, Any] = {}
        self.session: Dict[str, Any] = {}
        self.violations: List[Dict[str, Any]] = []
        self.compliance_score: float = 1.0

    def load_files(self):
        """Load YAML files."""
        try:
            with open(self.rules_path, "r", encoding="utf-8") as f:
                self.rules = yaml.safe_load(f) or {}
        except Exception as e:
            print(f"❌ Error loading rules file: {e}", file=sys.stderr)
            sys.exit(1)

        try:
            with open(self.session_path, "r", encoding="utf-8") as f:
                self.session = yaml.safe_load(f) or {}
        except Exception as e:
            print(f"❌ Error loading session file: {e}", file=sys.stderr)
            sys.exit(1)

    def validate_setup_is_vetted(self) -> bool:
        """Check all trades use vetted setups."""
        allowed_setups = {
            setup.get("name")
            for setup in self.rules.get("only_trade_setups", [])
        }
        allowed_setups.update(
            self.session.get("allowed_setups", [])
        )

        trades = self.session.get("trades", [])
        violation = False

        for trade in trades:
            setup_type = trade.get("setup_type")
            if setup_type not in allowed_setups:
                self.violations.append({
                    "rule": "only_trade_setups",
                    "severity": "HIGH",
                    "trade": trade.get("trade_number"),
                    "message": f"Trade used non-vetted setup: {setup_type}",
                })
                violation = True

        return not violation

    def validate_daily_trade_count(self) -> bool:
        """Check daily trade count doesn't exceed limit."""
        max_trades = self.rules.get("max_trades_per_day", 3)
        trades = self.session.get("trades", [])
        trade_count = len(trades)

        if trade_count > max_trades:
            self.violations.append({
                "rule": "max_trades_per_day",
                "severity": "HIGH",
                "message": f"Exceeded daily trade limit: {trade_count} > {max_trades}",
                "actual": trade_count,
                "limit": max_trades,
            })
            return False

        return True

    def validate_daily_loss_limit(self) -> bool:
        """Check daily loss doesn't exceed limit."""
        max_loss_percent = self.rules.get("max_daily_loss_percent", 2)
        starting_balance = self.session.get("starting_balance", 0)

        if starting_balance == 0:
            return True  # Skip if no starting balance provided

        session_summary = self.session.get("session_summary", {})
        total_pnl = session_summary.get("total_pnl", 0)

        # Calculate daily loss percent
        daily_loss_percent = abs(total_pnl) / starting_balance * 100 if total_pnl < 0 else 0

        if daily_loss_percent > max_loss_percent:
            self.violations.append({
                "rule": "max_daily_loss_percent",
                "severity": "CRITICAL",
                "message": f"Exceeded daily loss limit: {daily_loss_percent:.2f}% > {max_loss_percent}%",
                "actual_percent": daily_loss_percent,
                "limit_percent": max_loss_percent,
                "actual_loss": abs(total_pnl),
            })
            return False

        return True

    def validate_position_size(self) -> bool:
        """Check position sizes follow rules."""
        position_rule = self.rules.get("position_size_rule", {})
        method = position_rule.get("method", "fixed_fraction")
        fixed_fraction = position_rule.get("fixed_fraction", 0.05)

        starting_balance = self.session.get("starting_balance", 0)
        trades = self.session.get("trades", [])

        for trade in trades:
            position_size_dollars = trade.get("position_size_dollars", 0)
            position_size_percent = trade.get("position_size_percent", 0)

            if starting_balance > 0:
                calculated_percent = position_size_dollars / starting_balance

                if method == "fixed_fraction":
                    if abs(calculated_percent - fixed_fraction) > 0.01:  # 1% tolerance
                        self.violations.append({
                            "rule": "position_size_rule",
                            "severity": "MEDIUM",
                            "trade": trade.get("trade_number"),
                            "message": f"Position size {calculated_percent:.2%} doesn't match fixed fraction {fixed_fraction:.2%}",
                            "actual_percent": calculated_percent,
                            "expected_percent": fixed_fraction,
                        })

        return len([v for v in self.violations if v.get("rule") == "position_size_rule"]) == 0

    def validate_journal_required(self) -> bool:
        """Check all trades have journal entries."""
        trades = self.session.get("trades", [])

        for trade in trades:
            journal_entry = trade.get("journal_entry")
            if not journal_entry:
                self.violations.append({
                    "rule": "journal_required",
                    "severity": "MEDIUM",
                    "trade": trade.get("trade_number"),
                    "message": "Missing journal entry for trade",
                })

        return len([v for v in self.violations if v.get("rule") == "journal_required"]) == 0

    def validate_all(self):
        """Run all validations."""
        validation_rules = self.rules.get("validation_rules", {})

        if validation_rules.get("check_setup_is_vetted", True):
            self.validate_setup_is_vetted()

        if validation_rules.get("check_daily_trade_count", True):
            self.validate_daily_trade_count()

        if validation_rules.get("check_daily_loss_limit", True):
            self.validate_daily_loss_limit()

        if validation_rules.get("check_position_size", True):
            self.validate_position_size()

        if validation_rules.get("check_journal_completed", True):
            self.validate_journal_required()

        # Calculate compliance score (1.0 = perfect, decreases with violations)
        total_checks = len([v for v in validation_rules.values() if v])
        violation_count = len(self.violations)
        self.compliance_score = max(0.0, 1.0 - (violation_count / max(1, total_checks * 2)))

    def generate_report(self) -> Dict[str, Any]:
        """Generate compliance report."""
        session_summary = self.session.get("session_summary", {})
        trades = self.session.get("trades", [])

        report = {
            "session_date": self.session.get("session_date"),
            "validation_timestamp": datetime.now().isoformat(),
            "rules_respected": len(self.violations) == 0,
            "rules_broken": len(self.violations),
            "compliance_score": self.compliance_score,
            "violations": self.violations,
            "session_summary": {
                "total_trades": len(trades),
                "total_pnl": session_summary.get("total_pnl", 0),
                "daily_loss_percent": session_summary.get("daily_loss_percent", 0),
            },
            "notes_for_review": self._generate_notes(),
        }

        return report

    def _generate_notes(self) -> List[str]:
        """Generate notes for review."""
        notes = []

        if len(self.violations) == 0:
            notes.append("✅ All rules respected - excellent discipline!")
        else:
            notes.append(f"⚠️ {len(self.violations)} rule violation(s) found")
            high_severity = [v for v in self.violations if v.get("severity") == "HIGH" or v.get("severity") == "CRITICAL"]
            if high_severity:
                notes.append(f"🚨 {len(high_severity)} high-severity violation(s) require immediate attention")

        return notes

    def print_report(self, report: Dict[str, Any]):
        """Print formatted report."""
        print("\n" + "=" * 70)
        print("📊 TRADING SESSION VALIDATION REPORT")
        print("=" * 70 + "\n")

        print(f"Session Date: {report['session_date']}")
        print(f"Validation Time: {report['validation_timestamp']}\n")

        print(f"Rules Respected: {'✅ YES' if report['rules_respected'] else '❌ NO'}")
        print(f"Rules Broken: {report['rules_broken']}")
        print(f"Compliance Score: {report['compliance_score']:.2%}\n")

        if report['violations']:
            print("🚨 RULE VIOLATIONS:")
            print("-" * 70)
            for violation in report['violations']:
                severity = violation.get('severity', 'UNKNOWN')
                trade = violation.get('trade', 'N/A')
                message = violation.get('message', 'No message')
                print(f"  [{severity}] Trade #{trade}: {message}")
            print()

        print("📋 SESSION SUMMARY:")
        print("-" * 70)
        summary = report['session_summary']
        print(f"  Total Trades: {summary['total_trades']}")
        print(f"  Total P&L: ${summary['total_pnl']:.2f}")
        print(f"  Daily Loss %: {summary['daily_loss_percent']:.2f}%\n")

        print("📝 NOTES FOR REVIEW:")
        print("-" * 70)
        for note in report['notes_for_review']:
            print(f"  {note}")

        print("\n" + "=" * 70 + "\n")


def main():
    """Main execution."""
    parser = argparse.ArgumentParser(
        description="Validate trading session against trading rules"
    )
    parser.add_argument(
        "session_file",
        type=str,
        help="Path to trading session YAML file"
    )
    parser.add_argument(
        "--rules",
        type=str,
        default="trading_rules.yaml",
        help="Path to trading rules YAML file (default: trading_rules.yaml)"
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Output JSON report file (optional)"
    )

    args = parser.parse_args()

    # Resolve paths
    session_path = Path(args.session_file)
    if not session_path.is_absolute():
        session_path = Path(__file__).parent.parent / session_path

    rules_path = Path(args.rules)
    if not rules_path.is_absolute():
        rules_path = Path(__file__).parent.parent / rules_path

    # Validate files exist
    if not session_path.exists():
        print(f"❌ Session file not found: {session_path}", file=sys.stderr)
        sys.exit(1)

    if not rules_path.exists():
        print(f"❌ Rules file not found: {rules_path}", file=sys.stderr)
        sys.exit(1)

    # Run validation
    validator = TradingSessionValidator(rules_path, session_path)
    validator.load_files()
    validator.validate_all()
    report = validator.generate_report()

    # Print report
    validator.print_report(report)

    # Save report if requested
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
        print(f"✅ Report saved to: {output_path}\n")

    # Exit with error code if violations found
    if not report['rules_respected']:
        sys.exit(1)


if __name__ == "__main__":
    main()




