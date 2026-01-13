#!/usr/bin/env python3
"""
System Adoption Tracker
=======================

Tracks agent system usage and calculates adoption scores.
Provides insights into system utilization and adoption progress.

Usage:
    python tools/metrics/system_adoption_tracker.py --agent Agent-1
    python tools/metrics/system_adoption_tracker.py --leaderboard
    python tools/metrics/system_adoption_tracker.py --report
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict, Counter
import argparse

class SystemAdoptionTracker:
    """Track and analyze system adoption across agents."""

    def __init__(self):
        self.usage_file = Path("data/system_usage.json")
        self.usage_file.parent.mkdir(exist_ok=True)
        self.systems = self._get_available_systems()

    def _get_available_systems(self):
        """Get list of available systems."""
        return {
            "scanner": {"category": "analysis", "weight": 1.0},
            "debate": {"category": "decision_making", "weight": 1.2},
            "planner": {"category": "planning", "weight": 0.8},
            "tasks": {"category": "coordination", "weight": 0.9},
            "database": {"category": "infrastructure", "weight": 0.7},
            "config": {"category": "configuration", "weight": 0.5},
            "health": {"category": "monitoring", "weight": 0.6},
            "portal": {"category": "documentation", "weight": 0.4}
        }

    def get_agent_usage(self, agent_id):
        """Get usage statistics for a specific agent."""
        try:
            if not self.usage_file.exists():
                return self._create_empty_usage_stats(agent_id)

            with open(self.usage_file, 'r') as f:
                all_usage = json.load(f)

            agent_usage = all_usage.get(agent_id, {})

            return self._calculate_usage_stats(agent_id, agent_usage)

        except Exception as e:
            print(f"❌ Error getting usage for {agent_id}: {e}")
            return self._create_empty_usage_stats(agent_id)

    def _calculate_usage_stats(self, agent_id, agent_usage):
        """Calculate comprehensive usage statistics."""
        stats = {
            "agent_id": agent_id,
            "last_updated": datetime.now().isoformat(),
            "systems_used": {},
            "total_actions": 0,
            "systems_count": len(agent_usage),
            "categories_used": set(),
            "scores": {}
        }

        # Calculate per-system stats
        for system_name, actions in agent_usage.items():
            system_stats = {
                "actions_count": len(actions),
                "first_used": min(a["timestamp"] for a in actions),
                "last_used": max(a["timestamp"] for a in actions),
                "days_since_last_use": (datetime.now() - datetime.fromisoformat(actions[-1]["timestamp"])).days
            }

            # Add system category
            if system_name in self.systems:
                system_stats["category"] = self.systems[system_name]["category"]
                stats["categories_used"].add(self.systems[system_name]["category"])

            stats["systems_used"][system_name] = system_stats
            stats["total_actions"] += len(actions)

        # Calculate adoption scores
        stats["scores"] = self._calculate_adoption_scores(stats)

        return stats

    def _calculate_adoption_scores(self, stats):
        """Calculate various adoption scores."""
        scores = {}

        # Basic adoption score (systems used / total systems)
        systems_used = len(stats["systems_used"])
        total_systems = len(self.systems)
        scores["basic_adoption"] = (systems_used / total_systems) * 100

        # Weighted adoption score (considering system complexity)
        weighted_score = 0
        total_weight = 0

        for system_name in stats["systems_used"]:
            if system_name in self.systems:
                weight = self.systems[system_name]["weight"]
                actions = stats["systems_used"][system_name]["actions_count"]
                # More usage = higher score, but diminishing returns
                usage_score = min(actions / 10, 1.0)  # Cap at 10 uses
                weighted_score += weight * usage_score
                total_weight += weight

        scores["weighted_adoption"] = (weighted_score / total_weight) * 100 if total_weight > 0 else 0

        # Recency score (recent usage is more valuable)
        recency_score = 0
        for system_name, system_stats in stats["systems_used"].items():
            days_old = system_stats["days_since_last_use"]
            # Exponential decay: newer usage worth more
            recency_value = max(0, 1 - (days_old / 30))  # 30-day half-life
            recency_score += recency_value

        scores["recency_score"] = (recency_score / len(stats["systems_used"])) * 100 if stats["systems_used"] else 0

        # Overall adoption score (weighted combination)
        scores["overall_adoption"] = (
            scores["basic_adoption"] * 0.4 +
            scores["weighted_adoption"] * 0.4 +
            scores["recency_score"] * 0.2
        )

        # Adoption level
        overall = scores["overall_adoption"]
        if overall >= 95:
            scores["adoption_level"] = "SYSTEM MASTER"
            scores["benefits"] = ["Advanced system features", "Priority resource allocation", "Leadership opportunities"]
        elif overall >= 90:
            scores["adoption_level"] = "EXPERT"
            scores["benefits"] = ["Advanced system features", "Priority resource allocation"]
        elif overall >= 80:
            scores["adoption_level"] = "ADVANCED"
            scores["benefits"] = ["Advanced system features"]
        elif overall >= 60:
            scores["adoption_level"] = "INTERMEDIATE"
            scores["benefits"] = ["Standard system access"]
        elif overall >= 30:
            scores["adoption_level"] = "BEGINNER"
            scores["benefits"] = ["Basic system access", "Training recommendations"]
        else:
            scores["adoption_level"] = "STARTER"
            scores["benefits"] = ["Mandatory training required", "Basic system access"]

        return scores

    def _create_empty_usage_stats(self, agent_id):
        """Create empty usage stats for new agents."""
        return {
            "agent_id": agent_id,
            "last_updated": datetime.now().isoformat(),
            "systems_used": {},
            "total_actions": 0,
            "systems_count": 0,
            "categories_used": set(),
            "scores": {
                "basic_adoption": 0,
                "weighted_adoption": 0,
                "recency_score": 0,
                "overall_adoption": 0,
                "adoption_level": "STARTER",
                "benefits": ["Mandatory training required", "Basic system access"]
            }
        }

    def get_leaderboard(self, top_n=10):
        """Get adoption leaderboard."""
        try:
            if not self.usage_file.exists():
                return []

            with open(self.usage_file, 'r') as f:
                all_usage = json.load(f)

            leaderboard = []
            for agent_id, usage_data in all_usage.items():
                stats = self._calculate_usage_stats(agent_id, usage_data)
                leaderboard.append({
                    "agent_id": agent_id,
                    "overall_score": stats["scores"]["overall_adoption"],
                    "systems_used": stats["systems_count"],
                    "total_actions": stats["total_actions"],
                    "adoption_level": stats["scores"]["adoption_level"]
                })

            # Sort by overall score
            leaderboard.sort(key=lambda x: x["overall_score"], reverse=True)

            return leaderboard[:top_n]

        except Exception as e:
            print(f"❌ Error generating leaderboard: {e}")
            return []

    def generate_adoption_report(self):
        """Generate comprehensive adoption report."""
        try:
            if not self.usage_file.exists():
                return self._create_empty_report()

            with open(self.usage_file, 'r') as f:
                all_usage = json.load(f)

            report = {
                "generated_at": datetime.now().isoformat(),
                "total_agents": len(all_usage),
                "system_usage_summary": {},
                "category_usage_summary": {},
                "adoption_levels": Counter(),
                "recommendations": []
            }

            # Analyze system usage
            system_usage = defaultdict(int)
            category_usage = defaultdict(int)
            all_scores = []

            for agent_id, usage_data in all_usage.items():
                stats = self._calculate_usage_stats(agent_id, usage_data)
                all_scores.append(stats["scores"]["overall_adoption"])

                # Count system usage
                for system_name in usage_data.keys():
                    system_usage[system_name] += 1
                    if system_name in self.systems:
                        category_usage[self.systems[system_name]["category"]] += 1

                # Count adoption levels
                report["adoption_levels"][stats["scores"]["adoption_level"]] += 1

            report["system_usage_summary"] = dict(system_usage)
            report["category_usage_summary"] = dict(category_usage)

            # Calculate averages
            if all_scores:
                report["average_adoption_score"] = sum(all_scores) / len(all_scores)
                report["highest_adoption_score"] = max(all_scores)
                report["lowest_adoption_score"] = min(all_scores)

            # Generate recommendations
            report["recommendations"] = self._generate_recommendations(report)

            return report

        except Exception as e:
            print(f"❌ Error generating report: {e}")
            return self._create_empty_report()

    def _generate_recommendations(self, report):
        """Generate recommendations based on report data."""
        recommendations = []

        # Check system usage distribution
        total_agents = report["total_agents"]
        if total_agents > 0:
            for system_name, usage_count in report["system_usage_summary"].items():
                adoption_rate = (usage_count / total_agents) * 100
                if adoption_rate < 50:
                    recommendations.append(f"Improve {system_name} adoption (currently {adoption_rate:.1f}%)")
                elif adoption_rate > 80:
                    recommendations.append(f"🎉 Excellent {system_name} adoption ({adoption_rate:.1f}%)")

        # Check category balance
        categories = report["category_usage_summary"]
        if categories:
            max_usage = max(categories.values())
            min_usage = min(categories.values())

            if max_usage / min_usage > 2:
                recommendations.append("Balance system category usage - some categories underutilized")

        # Check overall adoption
        avg_score = report.get("average_adoption_score", 0)
        if avg_score < 60:
            recommendations.append("Accelerate training program - average adoption below 60%")
        elif avg_score > 80:
            recommendations.append("🎉 Strong adoption culture - maintain momentum")

        return recommendations

    def _create_empty_report(self):
        """Create empty report structure."""
        return {
            "generated_at": datetime.now().isoformat(),
            "total_agents": 0,
            "system_usage_summary": {},
            "category_usage_summary": {},
            "adoption_levels": {},
            "average_adoption_score": 0,
            "recommendations": ["Start using systems to generate adoption data"]
        }

    def display_agent_stats(self, agent_id):
        """Display formatted agent statistics."""
        stats = self.get_agent_usage(agent_id)

        print(f"\n🏆 SYSTEM ADOPTION STATS - {agent_id}")
        print("=" * 50)
        print(f"📊 Overall Adoption Score: {stats['scores']['overall_adoption']:.1f}%")
        print(f"🏅 Adoption Level: {stats['scores']['adoption_level']}")
        print(f"🔧 Systems Used: {stats['systems_count']}/{len(self.systems)}")
        print(f"⚡ Total Actions: {stats['total_actions']}")

        print("
📈 Score Breakdown:"        print(f"  Basic Adoption: {stats['scores']['basic_adoption']:.1f}%")
        print(f"  Weighted Adoption: {stats['scores']['weighted_adoption']:.1f}%")
        print(f"  Recency Score: {stats['scores']['recency_score']:.1f}%")

        if stats["systems_used"]:
            print("
🛠️ System Usage Details:"            for system_name, system_stats in stats["systems_used"].items():
                days_old = system_stats["days_since_last_use"]
                recency_indicator = "🟢" if days_old <= 7 else "🟡" if days_old <= 30 else "🔴"
                print(f"  {recency_indicator} {system_name}: {system_stats['actions_count']} uses ({days_old}d ago)")

        print("
🎁 Your Benefits:"        for benefit in stats["scores"]["benefits"]:
            print(f"  ✅ {benefit}")

        if stats["scores"]["overall_adoption"] < 80:
            print("
📚 Training Recommendations:"            unused_systems = set(self.systems.keys()) - set(stats["systems_used"].keys())
            if unused_systems:
                print(f"  Try these systems: {', '.join(list(unused_systems)[:3])}")
            print("  Run: python scripts/system_training.py --day 1"
    def display_leaderboard(self, top_n=10):
        """Display adoption leaderboard."""
        leaderboard = self.get_leaderboard(top_n)

        print(f"\n🏆 SYSTEM ADOPTION LEADERBOARD - Top {top_n}")
        print("=" * 60)
        print("<10"        print("-" * 60)

        for i, agent in enumerate(leaderboard, 1):
            medal = {1: "🥇", 2: "🥈", 3: "🥉"}.get(i, "📊")
            print("<10")

    def display_report(self):
        """Display comprehensive adoption report."""
        report = self.generate_adoption_report()

        print("
📊 SYSTEM ADOPTION REPORT"        print("=" * 50)
        print(f"Generated: {report['generated_at']}")
        print(f"Total Agents: {report['total_agents']}")

        if report["total_agents"] > 0:
            print("
📈 Adoption Metrics:"            print(f"  Average Score: {report.get('average_adoption_score', 0):.1f}%")
            print(f"  Highest Score: {report.get('highest_adoption_score', 0):.1f}%")
            print(f"  Lowest Score: {report.get('lowest_adoption_score', 0):.1f}%")

            print("
🏅 Adoption Levels:"            for level, count in report["adoption_levels"].items():
                percentage = (count / report["total_agents"]) * 100
                print(f"  {level}: {count} agents ({percentage:.1f}%)")

        if report["recommendations"]:
            print("
💡 Recommendations:"            for rec in report["recommendations"]:
                print(f"  • {rec}")


def main():
    """Main function for system adoption tracking."""
    parser = argparse.ArgumentParser(
        description="System Adoption Tracker - Monitor agent system usage and adoption",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python tools/metrics/system_adoption_tracker.py --agent Agent-1
  python tools/metrics/system_adoption_tracker.py --leaderboard
  python tools/metrics/system_adoption_tracker.py --report
        """
    )

    parser.add_argument("--agent", "-a", help="Show stats for specific agent")
    parser.add_argument("--leaderboard", "-l", action="store_true", help="Show adoption leaderboard")
    parser.add_argument("--report", "-r", action="store_true", help="Generate comprehensive report")

    args = parser.parse_args()

    tracker = SystemAdoptionTracker()

    if args.agent:
        tracker.display_agent_stats(args.agent)
    elif args.leaderboard:
        tracker.display_leaderboard()
    elif args.report:
        tracker.display_report()
    else:
        print("🤖 System Adoption Tracker")
        print("Usage:")
        print("  --agent Agent-X    : View agent stats")
        print("  --leaderboard      : View adoption leaderboard")
        print("  --report          : View comprehensive report")
        print("\nExample: python tools/metrics/system_adoption_tracker.py --agent Agent-1")


if __name__ == "__main__":
    main()