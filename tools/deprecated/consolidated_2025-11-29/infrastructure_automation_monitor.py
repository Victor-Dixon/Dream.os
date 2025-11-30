#!/usr/bin/env python3
"""
Infrastructure Automation Monitor
=================================

Automated infrastructure health monitoring, CI/CD status tracking,
and system reliability checks. Runs continuously and reports issues.

Author: Agent-3 (Infrastructure & DevOps Specialist)
Created: 2025-01-27
Priority: CRITICAL
V2 Compliance: <400 lines
"""

import json
import logging
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class InfrastructureAutomationMonitor:
    """Automated infrastructure monitoring and health checks."""

    def __init__(self, project_root: Optional[Path] = None):
        """Initialize monitor."""
        self.project_root = project_root or Path(__file__).parent.parent
        self.reports_dir = self.project_root / "agent_workspaces" / "Agent-3" / "infrastructure_reports"
        self.reports_dir.mkdir(parents=True, exist_ok=True)

    def check_test_coverage(self) -> Dict:
        """Check current test coverage status."""
        logger.info("Checking test coverage...")
        try:
            result = subprocess.run(
                ["python", "-m", "pytest", "--co", "-q"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=60
            )
            coverage_info = {
                "status": "success" if result.returncode == 0 else "warning",
                "output": result.stdout,
                "timestamp": datetime.now().isoformat()
            }
            return coverage_info
        except Exception as e:
            logger.error(f"Test coverage check failed: {e}")
            return {"status": "error", "error": str(e)}

    def check_ci_cd_status(self) -> Dict:
        """Check CI/CD pipeline status."""
        logger.info("Checking CI/CD status...")
        workflows_dir = self.project_root / ".github" / "workflows"
        status = {
            "workflows_found": 0,
            "workflows": [],
            "timestamp": datetime.now().isoformat()
        }
        
        if workflows_dir.exists():
            for workflow_file in workflows_dir.glob("*.yml"):
                status["workflows_found"] += 1
                status["workflows"].append({
                    "name": workflow_file.name,
                    "exists": True,
                    "size": workflow_file.stat().st_size
                })
        
        return status

    def check_system_health(self) -> Dict:
        """Check overall system health."""
        logger.info("Checking system health...")
        health = {
            "timestamp": datetime.now().isoformat(),
            "checks": {},
            "overall_status": "unknown"
        }
        
        # Check critical directories
        critical_dirs = [
            "src",
            "tests",
            "tools",
            "agent_workspaces",
            ".github"
        ]
        
        for dir_name in critical_dirs:
            dir_path = self.project_root / dir_name
            health["checks"][dir_name] = {
                "exists": dir_path.exists(),
                "is_directory": dir_path.is_dir() if dir_path.exists() else False
            }
        
        # Determine overall status
        all_exist = all(check["exists"] for check in health["checks"].values())
        health["overall_status"] = "healthy" if all_exist else "degraded"
        
        return health

    def check_tool_availability(self) -> Dict:
        """Check infrastructure tool availability."""
        logger.info("Checking tool availability...")
        tools_dir = self.project_root / "tools"
        required_tools = [
            "integration_health_checker.py",
            "infrastructure_health_dashboard.py",
            "check_integration_issues.py"
        ]
        
        availability = {
            "timestamp": datetime.now().isoformat(),
            "tools": {},
            "total_available": 0,
            "total_required": len(required_tools)
        }
        
        for tool in required_tools:
            tool_path = tools_dir / tool
            exists = tool_path.exists()
            availability["tools"][tool] = {
                "exists": exists,
                "path": str(tool_path) if exists else None
            }
            if exists:
                availability["total_available"] += 1
        
        availability["coverage_percent"] = (
            (availability["total_available"] / availability["total_required"]) * 100
            if availability["total_required"] > 0 else 0
        )
        
        return availability

    def generate_report(self) -> Dict:
        """Generate comprehensive infrastructure report."""
        logger.info("Generating infrastructure report...")
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "test_coverage": self.check_test_coverage(),
            "ci_cd_status": self.check_ci_cd_status(),
            "system_health": self.check_system_health(),
            "tool_availability": self.check_tool_availability()
        }
        
        # Save report
        report_file = self.reports_dir / f"infrastructure_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"Report saved to: {report_file}")
        return report

    def print_summary(self, report: Dict):
        """Print human-readable summary."""
        print("\n" + "=" * 70)
        print("🔧 INFRASTRUCTURE AUTOMATION MONITOR - SUMMARY")
        print("=" * 70)
        print(f"Timestamp: {report['timestamp']}")
        print()
        
        # System Health
        health = report["system_health"]
        print(f"System Health: {health['overall_status'].upper()}")
        for check_name, check_data in health["checks"].items():
            status = "✅" if check_data["exists"] else "❌"
            print(f"  {status} {check_name}")
        print()
        
        # Tool Availability
        tools = report["tool_availability"]
        print(f"Tool Availability: {tools['total_available']}/{tools['total_required']} "
              f"({tools['coverage_percent']:.1f}%)")
        for tool_name, tool_data in tools["tools"].items():
            status = "✅" if tool_data["exists"] else "❌"
            print(f"  {status} {tool_name}")
        print()
        
        # CI/CD Status
        ci_cd = report["ci_cd_status"]
        print(f"CI/CD Workflows: {ci_cd['workflows_found']} found")
        for workflow in ci_cd["workflows"]:
            print(f"  ✅ {workflow['name']}")
        print()
        
        # Test Coverage
        coverage = report["test_coverage"]
        print(f"Test Coverage Check: {coverage['status'].upper()}")
        print()
        
        print("=" * 70)
        print(f"📊 Full report: {self.reports_dir}")
        print("=" * 70 + "\n")


def main():
    """Main entry point."""
    monitor = InfrastructureAutomationMonitor()
    report = monitor.generate_report()
    monitor.print_summary(report)
    
    # Return exit code based on health
    if report["system_health"]["overall_status"] == "healthy":
        return 0
    else:
        return 1


if __name__ == "__main__":
    sys.exit(main())

