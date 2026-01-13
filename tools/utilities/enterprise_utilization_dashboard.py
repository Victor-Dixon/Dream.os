#!/usr/bin/env python3
"""
Enterprise Utilization Dashboard
Real-time monitoring of swarm-wide enterprise capability utilization

Usage:
python tools/enterprise_utilization_dashboard.py --overview
python tools/enterprise_utilization_dashboard.py --detailed
python tools/enterprise_utilization_dashboard.py --export
"""

import sys
import json
import time
from pathlib import Path
from typing import Dict, List, Any, Optional
import argparse

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

class EnterpriseUtilizationDashboard:
    """Real-time enterprise capability utilization monitoring"""

    def __init__(self):
        self.repo_root = Path(__file__).parent.parent
        self.capabilities_file = self.repo_root / "SYSTEM_CAPABILITIES_ANALYSIS.md"

        # Enterprise capability categories
        self.capability_categories = {
            "ai_utilization": {
                "name": "AI Infrastructure",
                "target": 80,
                "current": 0,
                "capabilities": ["Advanced Reasoning", "Vector Database", "AI APIs"]
            },
            "a2a_coordination": {
                "name": "A2A Coordination",
                "target": 90,
                "current": 40,
                "capabilities": ["Unified Messaging", "Command Handlers", "Workflow Templates"]
            },
            "task_management": {
                "name": "Task Management",
                "target": 80,
                "current": 0,
                "capabilities": ["Contract System", "Agent Management", "Performance Monitoring"]
            },
            "service_orchestration": {
                "name": "Service Orchestration",
                "target": 99.9,
                "current": 0,
                "capabilities": ["Main.py Launcher", "Service Manager", "Health Monitoring"]
            },
            "development_tools": {
                "name": "Development Tools",
                "target": 90,
                "current": 0,
                "capabilities": ["Coordination Tools", "AI Integration", "Infrastructure Tools"]
            },
            "web_infrastructure": {
                "name": "Web Infrastructure",
                "target": 95,
                "current": 0,
                "capabilities": ["FastAPI Application", "API Routes", "Enterprise Features"]
            },
            "communication_systems": {
                "name": "Communication Systems",
                "target": 95,
                "current": 0,
                "capabilities": ["Discord Integration", "Twitch Integration", "WebSocket Support"]
            },
            "analytics_intelligence": {
                "name": "Analytics & Intelligence",
                "target": 90,
                "current": 0,
                "capabilities": ["Swarm Intelligence", "Performance Analyzers", "Recommendation Engines"]
            }
        }

    def assess_ai_utilization(self) -> Dict[str, Any]:
        """Assess current AI utilization across swarm"""
        try:
            # Try to get AI status from swarm automation tool
            sys.path.insert(0, str(self.repo_root / "tools"))
            from swarm_ai_adoption_automation import SwarmAIAdoptionAutomation
            automation = SwarmAIAdoptionAutomation()
            validation = automation.validate_swarm_ai_adoption()

            functional_rate = validation.get('fully_functional', 0) / validation.get('total_agents', 1)
            utilization_percent = functional_rate * 100

            return {
                "current": round(utilization_percent, 1),
                "target": 80,
                "status": "operational" if utilization_percent > 0 else "not_deployed",
                "details": f"{validation.get('fully_functional', 0)}/{validation.get('total_agents', 0)} agents functional"
            }
        except Exception as e:
            return {
                "current": 0,
                "target": 80,
                "status": "assessment_error",
                "details": f"Error assessing AI utilization: {str(e)}"
            }

    def assess_a2a_coordination(self) -> Dict[str, Any]:
        """Assess A2A coordination utilization"""
        try:
            # Check coordination infrastructure
            from a2a_coordination_implementation import A2ACoordinationImplementer
            implementer = A2ACoordinationImplementer()
            validation = implementer.validate_coordination_infrastructure()

            if validation.get("overall_status") == "partially_operational":
                current = 60  # Improved from baseline 40%
            elif validation.get("overall_status") == "fully_operational":
                current = 90
            else:
                current = 40

            return {
                "current": current,
                "target": 90,
                "status": validation.get("overall_status", "unknown"),
                "details": f"Templates: {validation.get('templates_available', False)}, Messaging: {validation.get('messaging_system', False)}"
            }
        except Exception as e:
            return {
                "current": 40,
                "target": 90,
                "status": "baseline_assessment",
                "details": "Using baseline 40% coordination utilization"
            }

    def assess_task_management(self) -> Dict[str, Any]:
        """Assess task management utilization"""
        # Check for contract system and agent management indicators
        contract_indicators = [
            self.repo_root / "src" / "services" / "contract_system",
            self.repo_root / "src" / "services" / "agent_management.py"
        ]

        operational_count = sum(1 for indicator in contract_indicators if indicator.exists())

        if operational_count >= 2:
            current = 60  # Partially operational
        elif operational_count >= 1:
            current = 30  # Basic implementation
        else:
            current = 0   # Not implemented

        return {
            "current": current,
            "target": 80,
            "status": "partially_operational" if current > 0 else "not_implemented",
            "details": f"{operational_count}/2 core components available"
        }

    def assess_service_orchestration(self) -> Dict[str, Any]:
        """Assess service orchestration utilization"""
        # Check for main.py and service manager
        orchestration_indicators = [
            self.repo_root / "main.py",
            self.repo_root / "src" / "services" / "service_manager.py"
        ]

        operational_count = sum(1 for indicator in orchestration_indicators if indicator.exists())

        if operational_count >= 2:
            current = 70  # Good operational status
        elif operational_count >= 1:
            current = 40  # Basic orchestration
        else:
            current = 0   # Not implemented

        return {
            "current": current,
            "target": 99.9,
            "status": "operational" if current >= 70 else "developing",
            "details": f"{operational_count}/2 orchestration components available"
        }

    def assess_development_tools(self) -> Dict[str, Any]:
        """Assess development tools utilization"""
        # Check for tool categories
        tool_categories = [
            "a2a_coordination_health_check.py",
            "ai_integration_status_checker.py",
            "infrastructure_health_check.py"
        ]

        available_tools = sum(1 for tool in tool_categories
                            if (self.repo_root / "tools" / tool).exists())

        utilization_rate = (available_tools / len(tool_categories)) * 100

        if utilization_rate >= 75:
            current = 80
        elif utilization_rate >= 50:
            current = 60
        else:
            current = utilization_rate

        return {
            "current": round(current, 1),
            "target": 90,
            "status": "well_utilized" if current >= 60 else "developing",
            "details": f"{available_tools}/{len(tool_categories)} tool categories available"
        }

    def assess_web_infrastructure(self) -> Dict[str, Any]:
        """Assess web infrastructure utilization"""
        # Check for FastAPI and API routes
        web_indicators = [
            self.repo_root / "src" / "web" / "fastapi_app.py",
            self.repo_root / "src" / "web" / "ai_routes.py",
            self.repo_root / "src" / "web" / "api_routes.py"
        ]

        operational_count = sum(1 for indicator in web_indicators if indicator.exists())

        if operational_count >= 3:
            current = 85  # Highly operational
        elif operational_count >= 2:
            current = 65  # Good operational status
        elif operational_count >= 1:
            current = 35  # Basic implementation
        else:
            current = 0   # Not implemented

        return {
            "current": current,
            "target": 95,
            "status": "highly_operational" if current >= 80 else "operational",
            "details": f"{operational_count}/3 web infrastructure components available"
        }

    def assess_communication_systems(self) -> Dict[str, Any]:
        """Assess communication systems utilization"""
        # Check for Discord, Twitch, WebSocket integrations
        comm_indicators = [
            "discord" in str(f) for f in self.repo_root.glob("**/*discord*.py")
        ].count(True) > 0

        twitch_indicators = [
            "twitch" in str(f) for f in self.repo_root.glob("**/*twitch*.py")
        ].count(True) > 0

        websocket_indicators = [
            "websocket" in str(f) for f in self.repo_root.glob("**/*websocket*.py")
        ].count(True) > 0

        operational_count = sum([comm_indicators, twitch_indicators, websocket_indicators])

        if operational_count >= 3:
            current = 90
        elif operational_count >= 2:
            current = 70
        elif operational_count >= 1:
            current = 40
        else:
            current = 0

        return {
            "current": current,
            "target": 95,
            "status": "well_integrated" if current >= 70 else "developing",
            "details": f"{operational_count}/3 communication systems integrated"
        }

    def assess_analytics_intelligence(self) -> Dict[str, Any]:
        """Assess analytics and intelligence utilization"""
        # Check for swarm intelligence and analytics components
        analytics_indicators = [
            self.repo_root / "src" / "services" / "swarm_intelligence_manager.py",
            self.repo_root / "src" / "services" / "performance_analyzer.py",
            self.repo_root / "src" / "services" / "learning_recommender.py"
        ]

        operational_count = sum(1 for indicator in analytics_indicators if indicator.exists())

        if operational_count >= 3:
            current = 75
        elif operational_count >= 2:
            current = 50
        elif operational_count >= 1:
            current = 25
        else:
            current = 0

        return {
            "current": current,
            "target": 90,
            "status": "operational" if current >= 50 else "developing",
            "details": f"{operational_count}/3 analytics components available"
        }

    def generate_overview_report(self) -> Dict[str, Any]:
        """Generate comprehensive utilization overview"""
        assessments = {
            "ai_utilization": self.assess_ai_utilization(),
            "a2a_coordination": self.assess_a2a_coordination(),
            "task_management": self.assess_task_management(),
            "service_orchestration": self.assess_service_orchestration(),
            "development_tools": self.assess_development_tools(),
            "web_infrastructure": self.assess_web_infrastructure(),
            "communication_systems": self.assess_communication_systems(),
            "analytics_intelligence": self.assess_analytics_intelligence()
        }

        # Calculate overall metrics
        total_current = sum(assessment["current"] for assessment in assessments.values())
        total_target = sum(assessment["target"] for assessment in assessments.values())
        overall_utilization = (total_current / total_target) * 100 if total_target > 0 else 0

        # Achievement levels
        achievements = sum(1 for assessment in assessments.values()
                         if assessment["current"] >= assessment["target"] * 0.8)

        return {
            "timestamp": time.time(),
            "overall_utilization": round(overall_utilization, 1),
            "target_achievement_rate": f"{achievements}/{len(assessments)}",
            "assessments": assessments,
            "recommendations": self.generate_recommendations(assessments)
        }

    def generate_detailed_report(self) -> Dict[str, Any]:
        """Generate detailed utilization analysis"""
        overview = self.generate_overview_report()

        # Add trend analysis and predictions
        overview["trends"] = {
            "immediate_focus": self.identify_immediate_priorities(overview["assessments"]),
            "quick_wins": self.identify_quick_wins(overview["assessments"]),
            "long_term_goals": self.identify_long_term_goals(overview["assessments"])
        }

        # Add capability maturity matrix
        overview["maturity_matrix"] = self.generate_maturity_matrix(overview["assessments"])

        return overview

    def generate_recommendations(self, assessments: Dict[str, Any]) -> List[str]:
        """Generate utilization improvement recommendations"""
        recommendations = []

        for category, assessment in assessments.items():
            gap = assessment["target"] - assessment["current"]
            category_name = self.capability_categories[category]["name"]

            if gap > 30:
                recommendations.append(f"URGENT: Accelerate {category_name} from {assessment['current']}% to {assessment['target']}% utilization")
            elif gap > 15:
                recommendations.append(f"PRIORITY: Improve {category_name} utilization (currently {assessment['current']}%, target {assessment['target']}%)")
            elif gap > 5:
                recommendations.append(f"OPTIMIZE: Fine-tune {category_name} for complete utilization")

        # Sort by urgency
        urgent = [r for r in recommendations if "URGENT" in r]
        priority = [r for r in recommendations if "PRIORITY" in r]
        optimize = [r for r in recommendations if "OPTIMIZE" in r]

        return urgent + priority + optimize

    def identify_immediate_priorities(self, assessments: Dict[str, Any]) -> List[str]:
        """Identify areas needing immediate attention"""
        priorities = []
        for category, assessment in assessments.items():
            if assessment["current"] < 50 and assessment["target"] >= 80:
                priorities.append(f"{assessment['name']}: {assessment['current']}% → {assessment['target']}%")
        return priorities

    def identify_quick_wins(self, assessments: Dict[str, Any]) -> List[str]:
        """Identify quick utilization improvements"""
        quick_wins = []
        for category, assessment in assessments.items():
            if assessment["current"] >= 60 and assessment["current"] < assessment["target"]:
                quick_wins.append(f"{assessment['name']}: {assessment['current']}% → {assessment['target']}%")
        return quick_wins

    def identify_long_term_goals(self, assessments: Dict[str, Any]) -> List[str]:
        """Identify long-term utilization goals"""
        goals = []
        for category, assessment in assessments.items():
            if assessment["target"] >= 90 and assessment["current"] < 80:
                goals.append(f"{assessment['name']}: Enterprise-grade {assessment['target']}% utilization")
        return goals

    def generate_maturity_matrix(self, assessments: Dict[str, Any]) -> Dict[str, List[str]]:
        """Generate capability maturity matrix"""
        matrix = {
            "enterprise_ready": [],
            "operational": [],
            "developing": [],
            "not_implemented": []
        }

        for category, assessment in assessments.items():
            utilization_rate = assessment["current"] / assessment["target"]

            if utilization_rate >= 0.9:
                matrix["enterprise_ready"].append(assessment["name"])
            elif utilization_rate >= 0.7:
                matrix["operational"].append(assessment["name"])
            elif utilization_rate >= 0.3:
                matrix["developing"].append(assessment["name"])
            else:
                matrix["not_implemented"].append(assessment["name"])

        return matrix

def main():
    parser = argparse.ArgumentParser(description="Enterprise Utilization Dashboard")
    parser.add_argument("--overview", action="store_true", help="Show utilization overview")
    parser.add_argument("--detailed", action="store_true", help="Show detailed utilization analysis")
    parser.add_argument("--export", action="store_true", help="Export utilization report to JSON")

    args = parser.parse_args()

    dashboard = EnterpriseUtilizationDashboard()

    if args.overview:
        report = dashboard.generate_overview_report()
        print("🏗️ ENTERPRISE UTILIZATION OVERVIEW")
        print("=" * 50)
        print(f"Overall Utilization: {report['overall_utilization']}%")
        print(f"Target Achievement: {report['target_achievement_rate']} categories")
        print(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(report['timestamp']))}")
        print()

        print("CAPABILITY UTILIZATION:")
        for category, assessment in report['assessments'].items():
            category_name = dashboard.capability_categories[category]["name"]
            status_emoji = "✅" if assessment['current'] >= assessment['target'] * 0.8 else "🔶" if assessment['current'] >= 50 else "❌"
            print(f"{status_emoji} {category_name}: {assessment['current']}% / {assessment['target']}% - {assessment['status']}")

        print()
        print("RECOMMENDATIONS:")
        for i, rec in enumerate(report['recommendations'][:5], 1):
            print(f"{i}. {rec}")

    elif args.detailed:
        report = dashboard.generate_detailed_report()
        print("📊 DETAILED ENTERPRISE UTILIZATION ANALYSIS")
        print("=" * 50)
        print(json.dumps(report, indent=2, default=str))

    elif args.export:
        report = dashboard.generate_detailed_report()
        export_file = f"enterprise_utilization_report_{int(time.time())}.json"
        with open(export_file, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        print(f"✅ Report exported to {export_file}")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()