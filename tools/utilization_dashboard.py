#!/usr/bin/env python3
"""
Enterprise Utilization Dashboard
Real-time monitoring and visualization of enterprise infrastructure utilization

Usage:
    python tools/utilization_dashboard.py --dashboard
    python tools/utilization_dashboard.py --alerts
    python tools/utilization_dashboard.py --report
"""

import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any
import subprocess


class EnterpriseUtilizationDashboard:
    """Real-time enterprise infrastructure utilization monitoring"""

    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.registry = self._load_registry()
        self.baseline_metrics = self._load_baseline()

    def _load_registry(self) -> Dict:
        """Load the enterprise capability registry"""
        registry_file = self.project_root / "tools" / "registry.json"
        if registry_file.exists():
            try:
                with open(registry_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Warning: Could not load registry: {e}")
        return {}

    def _load_baseline(self) -> Dict:
        """Load baseline utilization metrics"""
        return {
            "ai": 0.3,  # 30% baseline
            "coordination": 0.4,  # 40% baseline
            "task_management": 0.25,  # 25% baseline
            "orchestration": 0.6,  # 60% baseline
            "testing": 0.35,  # 35% baseline
            "enterprise_infrastructure": 0.0  # New category
        }

    def get_current_utilization(self) -> Dict[str, Any]:
        """Get current utilization metrics across all categories"""
        utilization = {
            "timestamp": datetime.now().isoformat(),
            "categories": {},
            "overall_metrics": {
                "total_capabilities": 0,
                "operational_capabilities": 0,
                "utilization_rate": 0.0,
                "improvement_potential": 0.0
            },
            "trends": {}
        }

        # Analyze registry data
        for name, tool in self.registry.items():
            category = tool.get("category", "unknown")
            status = tool.get("status", "unknown")

            if category not in utilization["categories"]:
                utilization["categories"][category] = {
                    "total": 0,
                    "operational": 0,
                    "utilization_rate": 0.0,
                    "baseline": self.baseline_metrics.get(category, 0.0),
                    "improvement": 0.0
                }

            utilization["categories"][category]["total"] += 1
            utilization["overall_metrics"]["total_capabilities"] += 1

            if status == "operational":
                utilization["categories"][category]["operational"] += 1
                utilization["overall_metrics"]["operational_capabilities"] += 1

        # Calculate utilization rates and improvements
        for category, data in utilization["categories"].items():
            if data["total"] > 0:
                data["utilization_rate"] = data["operational"] / data["total"]
                data["improvement"] = data["utilization_rate"] - data["baseline"]

        # Overall metrics
        if utilization["overall_metrics"]["total_capabilities"] > 0:
            utilization["overall_metrics"]["utilization_rate"] = (
                utilization["overall_metrics"]["operational_capabilities"] /
                utilization["overall_metrics"]["total_capabilities"]
            )
            utilization["overall_metrics"]["improvement_potential"] = (
                1.0 - utilization["overall_metrics"]["utilization_rate"]
            )

        return utilization

    def get_coordination_metrics(self) -> Dict[str, Any]:
        """Get A2A coordination effectiveness metrics"""
        metrics = {
            "timestamp": datetime.now().isoformat(),
            "coordination_health": "UNKNOWN",
            "active_coordinations": 0,
            "recent_activity": [],
            "effectiveness_score": 0.0
        }

        try:
            # Try to get coordination status
            result = subprocess.run([
                "python", "tools/a2a_coordination_status_checker.py", "--check"
            ], capture_output=True, text=True, cwd=str(self.project_root))

            if result.returncode == 0:
                metrics["coordination_health"] = "HEALTHY"
                metrics["active_coordinations"] = 1  # Simplified
            else:
                metrics["coordination_health"] = "ISSUES"

        except Exception as e:
            metrics["coordination_health"] = f"ERROR: {str(e)}"

        return metrics

    def get_ai_utilization_metrics(self) -> Dict[str, Any]:
        """Get AI infrastructure utilization metrics"""
        metrics = {
            "timestamp": datetime.now().isoformat(),
            "ai_services_status": "UNKNOWN",
            "available_services": 0,
            "operational_services": 0,
            "utilization_rate": 0.0
        }

        try:
            result = subprocess.run([
                "python", "tools/ai_integration_status_checker.py", "--check-all"
            ], capture_output=True, text=True, cwd=str(self.project_root))

            # Parse output for basic metrics
            output = result.stdout + result.stderr
            if "AI services ready" in output:
                metrics["ai_services_status"] = "READY"
            elif "import" in output.lower():
                metrics["ai_services_status"] = "IMPORT_ISSUES"
            else:
                metrics["ai_services_status"] = "CHECK_NEEDED"

        except Exception as e:
            metrics["ai_services_status"] = f"ERROR: {str(e)}"

        return metrics

    def generate_dashboard_report(self) -> str:
        """Generate comprehensive dashboard report"""
        utilization = self.get_current_utilization()
        coordination = self.get_coordination_metrics()
        ai_metrics = self.get_ai_utilization_metrics()

        report = "# 🏗️ Enterprise Utilization Dashboard\n\n"
        report += f"**Generated:** {utilization['timestamp']}\n\n"

        # Overall Status
        report += "## 📊 Overall Status\n\n"
        report += f"- **Total Capabilities:** {utilization['overall_metrics']['total_capabilities']}\n"
        report += f"- **Operational Rate:** {utilization['overall_metrics']['utilization_rate']:.1%}\n"
        report += f"- **Improvement Potential:** {utilization['overall_metrics']['improvement_potential']:.1%}\n"
        report += f"- **Coordination Health:** {coordination['coordination_health']}\n"
        report += f"- **AI Services Status:** {ai_metrics['ai_services_status']}\n\n"

        # Category Breakdown
        report += "## 📈 Category Utilization\n\n"
        report += "| Category | Operational | Total | Utilization | Baseline | Improvement |\n"
        report += "|----------|-------------|-------|-------------|----------|-------------|\n"

        for category, data in utilization["categories"].items():
            operational = data["operational"]
            total = data["total"]
            utilization_rate = data["utilization_rate"] * 100
            baseline = data["baseline"] * 100
            improvement = data["improvement"] * 100

            status_icon = "🟢" if utilization_rate >= 80 else "🟡" if utilization_rate >= 50 else "🔴"
            report += f"| {category} | {operational} | {total} | {status_icon} {utilization_rate:.1f}% | {baseline:.1f}% | {'↗️' if improvement > 0 else '➡️'} {improvement:+.1f}% |\n"

        report += "\n"

        # Priority Actions
        report += "## 🎯 Priority Actions\n\n"

        # Identify categories needing attention
        low_utilization = []
        for category, data in utilization["categories"].items():
            if data["utilization_rate"] < 0.5:  # Less than 50%
                low_utilization.append((category, data["utilization_rate"]))

        if low_utilization:
            report += "### 🚨 Low Utilization Categories\n"
            for category, rate in sorted(low_utilization, key=lambda x: x[1]):
                report += f"- **{category}**: {rate:.1%} utilization - High priority optimization\n"
            report += "\n"

        # Coordination status
        if coordination["coordination_health"] != "HEALTHY":
            report += "### 🤝 Coordination Optimization Needed\n"
            report += f"- Current status: {coordination['coordination_health']}\n"
            report += "- Recommendation: Review A2A coordination workflows\n\n"

        # AI status
        if ai_metrics["ai_services_status"] != "READY":
            report += "### 🤖 AI Infrastructure Optimization Needed\n"
            report += f"- Current status: {ai_metrics['ai_services_status']}\n"
            report += "- Recommendation: Complete import path resolution\n\n"

        # Success highlights
        high_utilization = []
        for category, data in utilization["categories"].items():
            if data["utilization_rate"] >= 0.8:  # 80% or higher
                high_utilization.append((category, data["utilization_rate"]))

        if high_utilization:
            report += "### ✅ High Utilization Success\n"
            for category, rate in high_utilization:
                report += f"- **{category}**: {rate:.1%} utilization - Excellent adoption\n"
            report += "\n"

        # Next Steps
        report += "## 🚀 Next Steps\n\n"
        report += "1. **Address Low Utilization**: Focus on categories below 50%\n"
        report += "2. **Optimize Coordination**: Enhance A2A effectiveness\n"
        report += "3. **Complete AI Integration**: Resolve import path issues\n"
        report += "4. **Monitor Progress**: Weekly utilization assessments\n"
        report += "5. **Scale Success**: Apply high-utilization patterns\n\n"

        # Footer
        report += "---\n"
        report += "*Dashboard Status: ACTIVE | Update Frequency: Real-time*\n"
        report += "*Optimization Target: 80%+ utilization across all categories*\n"

        return report

    def check_alerts(self) -> List[str]:
        """Check for utilization alerts and optimization opportunities"""
        alerts = []
        utilization = self.get_current_utilization()

        # Low utilization alerts
        for category, data in utilization["categories"].items():
            if data["utilization_rate"] < 0.3:  # Below 30%
                alerts.append(f"🚨 CRITICAL: {category} utilization at {data['utilization_rate']:.1f}% - Immediate optimization required")

        # Coordination alerts
        coordination = self.get_coordination_metrics()
        if coordination["coordination_health"] != "HEALTHY":
            alerts.append(f"⚠️ COORDINATION: Health status is {coordination['coordination_health']} - Review A2A workflows")

        # AI alerts
        ai_metrics = self.get_ai_utilization_metrics()
        if ai_metrics["ai_services_status"] != "READY":
            alerts.append(f"⚠️ AI INFRASTRUCTURE: Status is {ai_metrics['ai_services_status']} - Complete import path resolution")

        return alerts


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Enterprise Utilization Dashboard")
    parser.add_argument("--dashboard", action="store_true", help="Show full utilization dashboard")
    parser.add_argument("--alerts", action="store_true", help="Check for utilization alerts")
    parser.add_argument("--report", action="store_true", help="Generate comprehensive report")
    parser.add_argument("--json", action="store_true", help="Output JSON format")

    args = parser.parse_args()

    dashboard = EnterpriseUtilizationDashboard()

    if args.dashboard or args.report:
        report = dashboard.generate_dashboard_report()
        if args.json:
            # Convert to JSON structure
            utilization = dashboard.get_current_utilization()
            coordination = dashboard.get_coordination_metrics()
            ai_metrics = dashboard.get_ai_utilization_metrics()

            json_output = {
                "utilization": utilization,
                "coordination": coordination,
                "ai_metrics": ai_metrics,
                "alerts": dashboard.check_alerts()
            }
            print(json.dumps(json_output, indent=2))
        else:
            print(report)

    elif args.alerts:
        alerts = dashboard.check_alerts()
        if alerts:
            print("🚨 Utilization Alerts:\n")
            for alert in alerts:
                print(f"  {alert}")
        else:
            print("✅ No critical utilization alerts - all systems nominal")

    else:
        print("Use --dashboard, --alerts, or --report")
        print("\nQuick Stats:")
        utilization = dashboard.get_current_utilization()
        print(f"  Total Capabilities: {utilization['overall_metrics']['total_capabilities']}")
        print(f"  Operational Rate: {utilization['overall_metrics']['utilization_rate']:.1%}")
        print(f"  Coordination Health: {dashboard.get_coordination_metrics()['coordination_health']}")
        print(f"  AI Status: {dashboard.get_ai_utilization_metrics()['ai_services_status']}")


if __name__ == "__main__":
    main()