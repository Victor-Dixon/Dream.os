#!/usr/bin/env python3
"""
Monthly Money Map Reviewer
===========================

Reviews monthly money map to check if spending followed the map and
identify adjustments needed.

Usage:
    python review_money_map.py monthly_map_2025-12.yaml
    python review_money_map.py monthly_map_2025-12.yaml --weekly-check
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

import yaml


class MoneyMapReviewer:
    """Reviews monthly money map for compliance and adjustments."""

    def __init__(self, map_path: Path):
        """Initialize reviewer with money map file."""
        self.map_path = map_path
        self.money_map: Dict[str, Any] = {}

    def load_map(self):
        """Load money map YAML file."""
        try:
            with open(self.map_path, "r", encoding="utf-8") as f:
                self.money_map = yaml.safe_load(f) or {}
        except Exception as e:
            print(f"❌ Error loading money map: {e}", file=sys.stderr)
            sys.exit(1)

    def calculate_totals(self):
        """Calculate totals for income and expenses."""
        # Calculate total income
        trading_income = self.money_map.get("income_streams", {}).get("trading", {}).get("actual", 0)
        other_income = sum(
            stream.get("actual", 0)
            for stream in self.money_map.get("income_streams", {}).get("other", [])
        )
        total_income = trading_income + other_income

        # Calculate total fixed costs
        fixed_costs = self.money_map.get("fixed_costs", {})
        total_fixed = sum(
            cost.get("amount", 0) if isinstance(cost, dict) else 0
            for cost in fixed_costs.values()
            if isinstance(cost, (int, float))
        )
        total_fixed += sum(
            item.get("amount", 0)
            for item in fixed_costs.get("obligations", [])
        )

        # Calculate total variable costs
        variable_costs = self.money_map.get("variable_costs", {})
        total_variable_budget = sum(
            cost.get("budget", 0) if isinstance(cost, dict) else 0
            for cost in variable_costs.values()
            if isinstance(cost, dict)
        )
        total_variable_actual = sum(
            cost.get("actual", 0) if isinstance(cost, dict) else 0
            for cost in variable_costs.values()
            if isinstance(cost, dict)
        )
        total_variable_actual += sum(
            item.get("actual", 0)
            for item in variable_costs.get("other", [])
        )

        # Calculate break-even
        break_even = total_fixed + total_variable_budget

        # Calculate net and surplus
        total_expenses = total_fixed + total_variable_actual
        net_income = total_income - total_expenses

        # Update money map
        if "monthly_summary" not in self.money_map:
            self.money_map["monthly_summary"] = {}

        self.money_map["monthly_summary"].update({
            "total_income": total_income,
            "total_expenses": total_expenses,
            "net_income": net_income,
            "surplus_deficit": net_income,
        })

        # Check targets
        targets = self.money_map.get("targets", {})
        break_even_target = targets.get("break_even", break_even)
        surplus_target = targets.get("surplus_target", 0)

        self.money_map["monthly_summary"]["on_track"] = net_income >= break_even_target

        return {
            "total_income": total_income,
            "total_fixed": total_fixed,
            "total_variable_budget": total_variable_budget,
            "total_variable_actual": total_variable_actual,
            "break_even": break_even_target,
            "net_income": net_income,
            "surplus_target": surplus_target,
        }

    def check_spending_vs_budget(self) -> Dict[str, Any]:
        """Check if spending followed the map."""
        variable_costs = self.money_map.get("variable_costs", {})
        over_budget = []

        for category, data in variable_costs.items():
            if isinstance(data, dict):
                budget = data.get("budget", 0)
                actual = data.get("actual", 0)

                if actual > budget:
                    over_budget.append({
                        "category": category,
                        "budget": budget,
                        "actual": actual,
                        "over_by": actual - budget,
                        "over_percent": ((actual - budget) / budget * 100) if budget > 0 else 0,
                    })

        return {
            "over_budget_categories": over_budget,
            "count": len(over_budget),
        }

    def generate_review_report(self, weekly_check: bool = False) -> Dict[str, Any]:
        """Generate review report."""
        totals = self.calculate_totals()
        spending_check = self.check_spending_vs_budget()

        report = {
            "review_type": "weekly_check" if weekly_check else "monthly_review",
            "month": self.money_map.get("month"),
            "review_timestamp": datetime.now().isoformat(),
            "totals": totals,
            "spending_analysis": spending_check,
            "recommendations": [],
        }

        # Generate recommendations
        if totals["net_income"] < totals["break_even"]:
            report["recommendations"].append({
                "priority": "HIGH",
                "message": f"⚠️ Net income (${totals['net_income']:.2f}) below break-even (${totals['break_even']:.2f})",
                "action": "Review spending and income streams immediately",
            })

        if spending_check["count"] > 0:
            report["recommendations"].append({
                "priority": "MEDIUM",
                "message": f"⚠️ {spending_check['count']} category/categories over budget",
                "action": "Review variable costs and adjust spending",
                "categories": spending_check["over_budget_categories"],
            })

        if totals["net_income"] < totals["surplus_target"]:
            report["recommendations"].append({
                "priority": "MEDIUM",
                "message": f"⚠️ Surplus (${totals['net_income']:.2f}) below target (${totals['surplus_target']:.2f})",
                "action": "Review ways to increase income or reduce expenses",
            })

        if len(report["recommendations"]) == 0:
            report["recommendations"].append({
                "priority": "INFO",
                "message": "✅ Spending on track with money map",
                "action": "Continue following the plan",
            })

        return report

    def print_report(self, report: Dict[str, Any]):
        """Print formatted report."""
        review_type = "WEEKLY CHECK" if report["review_type"] == "weekly_check" else "MONTHLY REVIEW"
        print("\n" + "=" * 70)
        print(f"💰 MONTHLY MONEY MAP {review_type}")
        print("=" * 70 + "\n")

        print(f"Month: {report['month']}")
        print(f"Review Time: {report['review_timestamp']}\n")

        totals = report["totals"]
        print("📊 FINANCIAL TOTALS:")
        print("-" * 70)
        print(f"  Total Income: ${totals['total_income']:.2f}")
        print(f"  Total Fixed Costs: ${totals['total_fixed']:.2f}")
        print(f"  Variable Costs Budget: ${totals['total_variable_budget']:.2f}")
        print(f"  Variable Costs Actual: ${totals['total_variable_actual']:.2f}")
        print(f"  Break-Even Target: ${totals['break_even']:.2f}")
        print(f"  Net Income: ${totals['net_income']:.2f}")
        print(f"  Surplus Target: ${totals['surplus_target']:.2f}\n")

        spending = report["spending_analysis"]
        if spending["count"] > 0:
            print("⚠️  OVER BUDGET CATEGORIES:")
            print("-" * 70)
            for category in spending["over_budget_categories"]:
                print(f"  {category['category']}:")
                print(f"    Budget: ${category['budget']:.2f}")
                print(f"    Actual: ${category['actual']:.2f}")
                print(f"    Over by: ${category['over_by']:.2f} ({category['over_percent']:.1f}%)")
            print()
        else:
            print("✅ All variable costs within budget\n")

        print("💡 RECOMMENDATIONS:")
        print("-" * 70)
        for rec in report["recommendations"]:
            priority = rec.get("priority", "INFO")
            message = rec.get("message", "")
            action = rec.get("action", "")
            print(f"  [{priority}] {message}")
            if action:
                print(f"      → {action}")
        print()

        print("=" * 70 + "\n")


def main():
    """Main execution."""
    parser = argparse.ArgumentParser(
        description="Review monthly money map"
    )
    parser.add_argument(
        "map_file",
        type=str,
        help="Path to monthly money map YAML file"
    )
    parser.add_argument(
        "--weekly-check",
        action="store_true",
        help="Perform weekly check instead of full monthly review"
    )

    args = parser.parse_args()

    # Resolve path
    map_path = Path(args.map_file)
    if not map_path.is_absolute():
        map_path = Path(__file__).parent.parent / map_path

    if not map_path.exists():
        print(f"❌ Money map file not found: {map_path}", file=sys.stderr)
        sys.exit(1)

    # Run review
    reviewer = MoneyMapReviewer(map_path)
    reviewer.load_map()
    report = reviewer.generate_review_report(weekly_check=args.weekly_check)

    # Print report
    reviewer.print_report(report)


if __name__ == "__main__":
    main()




