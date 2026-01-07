#!/usr/bin/env python3
"""
Analytics Operations Center
===========================

Unified command center for comprehensive analytics deployment and operations management.
Integrates all analytics tools into a single enterprise operations interface.

Features:
- Unified analytics ecosystem dashboard
- Multi-tool orchestration and coordination
- Real-time deployment status monitoring
- Automated compliance and health reporting
- Enterprise analytics operations management
- Command-line interface for all analytics operations

Author: Agent-3 (Infrastructure & DevOps Specialist)
Created: 2026-01-07
Purpose: Provide unified enterprise analytics operations management center
"""

import asyncio
import json
import time
import subprocess
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class AnalyticsOperationsCenter:
    """Unified analytics operations center."""
    center_id: str
    initialized: str
    tools_available: Dict[str, bool]
    ecosystem_status: Dict[str, Any]
    last_operations: List[Dict[str, Any]]

class AnalyticsOperationsCommand:
    """Command interface for analytics operations."""

    def __init__(self):
        self.operations_center = AnalyticsOperationsCenter(
            center_id=f"aoc_{int(time.time())}",
            initialized=datetime.now().isoformat(),
            tools_available={},
            ecosystem_status={},
            last_operations=[]
        )
        self._scan_available_tools()

    def _scan_available_tools(self):
        """Scan for available analytics tools."""
        tools_to_check = {
            "website_health_monitor": "tools/website_health_monitor.py",
            "analytics_deployment_monitor": "src/infrastructure/analytics_deployment_monitor.py",
            "compliance_validator": "tools/enterprise_analytics_compliance_validator.py",
            "deployment_dashboard": "tools/analytics_deployment_dashboard.py",
            "deployment_orchestrator": "tools/analytics_deployment_orchestrator.py",
            "deployment_automation": "tools/analytics_deployment_automation.py",
            "config_validator": "tools/deploy_ga4_pixel_analytics.py",
            "live_verifier": "tools/analytics_live_verification.py"
        }

        for tool_name, tool_path in tools_to_check.items():
            self.operations_center.tools_available[tool_name] = Path(tool_path).exists()

    async def get_ecosystem_status(self) -> Dict[str, Any]:
        """Get comprehensive ecosystem status."""
        status = {
            "operations_center_id": self.operations_center.center_id,
            "timestamp": datetime.now().isoformat(),
            "tools_status": {},
            "ecosystem_health": {},
            "recent_operations": self.operations_center.last_operations[-5:],
            "system_summary": {}
        }

        # Check tool availability
        status["tools_status"] = self.operations_center.tools_available.copy()

        # Get deployment dashboard status
        if status["tools_status"].get("deployment_dashboard"):
            try:
                dashboard_result = await self._run_tool_command(
                    "python", "tools/analytics_deployment_dashboard.py", "--json"
                )
                if dashboard_result["returncode"] == 0:
                    status["ecosystem_health"] = json.loads(dashboard_result["stdout"])
            except Exception as e:
                logger.debug(f"Dashboard status check failed: {e}")

        # Generate system summary
        tools_available = sum(status["tools_status"].values())
        total_tools = len(status["tools_status"])

        status["system_summary"] = {
            "tools_available": tools_available,
            "tools_total": total_tools,
            "ecosystem_completeness": ".1f",
            "last_operation": self.operations_center.last_operations[-1] if self.operations_center.last_operations else None
        }

        return status

    async def execute_operation(self, operation: str, **kwargs) -> Dict[str, Any]:
        """Execute a specific analytics operation."""
        operation_id = f"op_{int(time.time())}"
        operation_record = {
            "operation_id": operation_id,
            "operation": operation,
            "timestamp": datetime.now().isoformat(),
            "parameters": kwargs,
            "status": "executing",
            "result": None,
            "duration": None
        }

        start_time = time.time()

        try:
            if operation == "health_check":
                result = await self._execute_health_check(kwargs)
            elif operation == "compliance_audit":
                result = await self._execute_compliance_audit(kwargs)
            elif operation == "deployment_status":
                result = await self._execute_deployment_status(kwargs)
            elif operation == "live_verification":
                result = await self._execute_live_verification(kwargs)
            elif operation == "automated_deployment":
                result = await self._execute_automated_deployment(kwargs)
            elif operation == "orchestrated_deployment":
                result = await self._execute_orchestrated_deployment(kwargs)
            else:
                raise ValueError(f"Unknown operation: {operation}")

            operation_record["status"] = "completed"
            operation_record["result"] = result

        except Exception as e:
            operation_record["status"] = "failed"
            operation_record["result"] = {"error": str(e)}
            logger.error(f"Operation {operation} failed: {e}")

        operation_record["duration"] = time.time() - start_time
        self.operations_center.last_operations.append(operation_record)

        return operation_record

    async def _execute_health_check(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute comprehensive health check."""
        sites = params.get("sites", ["freerideinvestor.com", "tradingrobotplug.com", "dadudekc.com", "crosbyultimateevents.com"])

        results = {}
        for site in sites:
            try:
                result = await self._run_tool_command(
                    "python", "tools/website_health_monitor.py",
                    "--site", site
                )
                results[site] = {
                    "success": result["returncode"] == 0,
                    "output": result["stdout"],
                    "timestamp": datetime.now().isoformat()
                }
            except Exception as e:
                results[site] = {"success": False, "error": str(e)}

        return {
            "operation": "health_check",
            "sites_checked": len(sites),
            "results": results,
            "summary": f"Health check completed for {len(sites)} sites"
        }

    async def _execute_compliance_audit(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute enterprise compliance audit."""
        sites = params.get("sites", ["freerideinvestor.com", "tradingrobotplug.com"])

        results = {}
        for site in sites:
            try:
                result = await self._run_tool_command(
                    "python", "tools/enterprise_analytics_compliance_validator.py",
                    "--site", site
                )
                results[site] = {
                    "success": result["returncode"] == 0,
                    "output": result["stdout"],
                    "timestamp": datetime.now().isoformat()
                }
            except Exception as e:
                results[site] = {"success": False, "error": str(e)}

        return {
            "operation": "compliance_audit",
            "sites_audited": len(sites),
            "results": results,
            "summary": f"Compliance audit completed for {len(sites)} sites"
        }

    async def _execute_deployment_status(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute deployment status check."""
        try:
            result = await self._run_tool_command(
                "python", "tools/analytics_deployment_dashboard.py", "--json"
            )

            if result["returncode"] == 0:
                dashboard_data = json.loads(result["stdout"])
                return {
                    "operation": "deployment_status",
                    "status": "success",
                    "dashboard_data": dashboard_data,
                    "summary": f"Deployment dashboard generated with {dashboard_data.get('summary', {}).get('sites_audited', 0)} sites monitored"
                }
            else:
                return {
                    "operation": "deployment_status",
                    "status": "failed",
                    "error": result["stderr"],
                    "summary": "Deployment status check failed"
                }

        except Exception as e:
            return {
                "operation": "deployment_status",
                "status": "error",
                "error": str(e),
                "summary": "Deployment status check encountered an error"
            }

    async def _execute_live_verification(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute live verification check."""
        sites = params.get("sites", ["freerideinvestor.com", "tradingrobotplug.com"])

        results = {}
        for site in sites:
            try:
                result = await self._run_tool_command(
                    "python", "tools/analytics_live_verification.py",
                    "--site", site
                )
                results[site] = {
                    "success": result["returncode"] == 0,
                    "output": result["stdout"],
                    "timestamp": datetime.now().isoformat()
                }
            except Exception as e:
                results[site] = {"success": False, "error": str(e)}

        return {
            "operation": "live_verification",
            "sites_verified": len(sites),
            "results": results,
            "summary": f"Live verification completed for {len(sites)} sites"
        }

    async def _execute_automated_deployment(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute automated deployment."""
        try:
            result = await self._run_tool_command(
                "python", "tools/analytics_deployment_automation.py", "--execute"
            )

            return {
                "operation": "automated_deployment",
                "status": "completed" if result["returncode"] == 0 else "failed",
                "output": result["stdout"],
                "summary": "Automated deployment execution completed"
            }

        except Exception as e:
            return {
                "operation": "automated_deployment",
                "status": "error",
                "error": str(e),
                "summary": "Automated deployment encountered an error"
            }

    async def _execute_orchestrated_deployment(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute orchestrated deployment."""
        try:
            result = await self._run_tool_command(
                "python", "tools/analytics_deployment_orchestrator.py",
                "--p0-sites", "--execute"
            )

            return {
                "operation": "orchestrated_deployment",
                "status": "completed" if result["returncode"] == 0 else "failed",
                "output": result["stdout"],
                "summary": "Orchestrated deployment execution completed"
            }

        except Exception as e:
            return {
                "operation": "orchestrated_deployment",
                "status": "error",
                "error": str(e),
                "summary": "Orchestrated deployment encountered an error"
            }

    async def _run_tool_command(self, *args) -> Dict[str, Any]:
        """Run a tool command and return results."""
        try:
            process = await asyncio.create_subprocess_exec(
                *args,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()

            return {
                "returncode": process.returncode,
                "stdout": stdout.decode(),
                "stderr": stderr.decode()
            }
        except Exception as e:
            return {
                "returncode": -1,
                "stdout": "",
                "stderr": str(e)
            }

    def print_operations_center_status(self):
        """Print comprehensive operations center status."""
        print("🎯 Analytics Operations Center")
        print("=" * 40)
        print(f"Center ID: {self.operations_center.center_id}")
        print(f"Initialized: {self.operations_center.initialized}")
        print()

        # Tools availability
        tools_available = sum(self.operations_center.tools_available.values())
        tools_total = len(self.operations_center.tools_available)

        print("🛠️  Tools Status")
        print("-" * 14)
        print(f"Available: {tools_available}/{tools_total}")
        print(".1f")

        for tool, available in self.operations_center.tools_available.items():
            status = "✅ Available" if available else "❌ Missing"
            print(f"   {tool}: {status}")
        print()

        # Recent operations
        if self.operations_center.last_operations:
            print("📋 Recent Operations")
            print("-" * 19)
            for op in self.operations_center.last_operations[-3:]:
                status_icon = "✅" if op["status"] == "completed" else "❌" if op["status"] == "failed" else "⏳"
                duration = ".2f" if op.get("duration") else "N/A"
                print(f"   {status_icon} {op['operation']} ({duration}s)")
        else:
            print("📋 Recent Operations")
            print("-" * 19)
            print("   No operations executed yet")
        print()

        # Available operations
        print("🚀 Available Operations")
        print("-" * 22)
        operations = [
            "health_check - Comprehensive website health monitoring",
            "compliance_audit - Enterprise GDPR compliance validation",
            "deployment_status - Real-time deployment ecosystem status",
            "live_verification - Live analytics functionality testing",
            "automated_deployment - Execute automated deployment pipeline",
            "orchestrated_deployment - Run orchestrated deployment workflow"
        ]

        for op in operations:
            print(f"   • {op}")
        print()

# CLI interface
async def main():
    """Main CLI interface for Analytics Operations Center."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Analytics Operations Center - Unified enterprise analytics management",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python tools/analytics_operations_center.py --status
  python tools/analytics_operations_center.py --operation health_check
  python tools/analytics_operations_center.py --operation compliance_audit --sites freerideinvestor.com
  python tools/analytics_operations_center.py --operation automated_deployment
        """
    )

    parser.add_argument('--status', action='store_true', help='Show operations center status')
    parser.add_argument('--operation', help='Execute specific operation')
    parser.add_argument('--sites', help='Comma-separated list of sites for operation')
    parser.add_argument('--json', action='store_true', help='Output results as JSON')

    args = parser.parse_args()

    operations_center = AnalyticsOperationsCommand()

    try:
        if args.status:
            if args.json:
                status = await operations_center.get_ecosystem_status()
                print(json.dumps(status, indent=2))
            else:
                operations_center.print_operations_center_status()

        elif args.operation:
            # Parse sites parameter
            sites = args.sites.split(',') if args.sites else None

            # Execute operation
            result = await operations_center.execute_operation(
                args.operation,
                sites=sites
            )

            if args.json:
                print(json.dumps(result, indent=2))
            else:
                print(f"🎯 Operation Result: {args.operation.upper()}")
                print("=" * 40)
                print(f"Status: {result['status'].upper()}")
                if result.get('duration'):
                    print(".2f")
                if result.get('result') and 'summary' in result['result']:
                    print(f"Summary: {result['result']['summary']}")

                # Print key results
                if args.operation == "health_check":
                    results = result.get('result', {}).get('results', {})
                    for site, site_result in results.items():
                        status = "✅ SUCCESS" if site_result.get('success') else "❌ FAILED"
                        print(f"   {status}: {site}")

                elif args.operation == "compliance_audit":
                    results = result.get('result', {}).get('results', {})
                    for site, site_result in results.items():
                        status = "✅ SUCCESS" if site_result.get('success') else "❌ FAILED"
                        print(f"   {status}: {site}")

                elif args.operation == "deployment_status":
                    if result['status'] == 'success':
                        dashboard = result.get('result', {}).get('dashboard_data', {})
                        summary = dashboard.get('summary', {})
                        print(f"   Sites Audited: {summary.get('sites_audited', 0)}")
                        print(".1f")
                        print(f"   Sites Verified: {summary.get('sites_fully_verified', 0)}")
                    else:
                        print(f"   Error: {result.get('result', {}).get('error', 'Unknown error')}")

        else:
            parser.print_help()

    except KeyboardInterrupt:
        print("\n⚠️  Operations interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())