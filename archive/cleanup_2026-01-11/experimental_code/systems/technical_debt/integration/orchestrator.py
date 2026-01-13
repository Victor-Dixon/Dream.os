"""
Technical Debt Integration Orchestrator
========================================

Unified interface for all technical debt system integrations.

Features:
- Single entry point for all debt operations
- Automated task assignment and tracking
- Master task log synchronization
- Audit trail compliance
- Discord command integration

<!-- SSOT Domain: integration -->
"""

import logging
from datetime import datetime
from typing import Dict, Any, List, Optional

from ..debt_tracker import TechnicalDebtTracker
from .agent_status_integration import AgentStatusDebtIntegration
from .master_task_integration import MasterTaskDebtIntegration
from .audit_integration import AuditDebtIntegration

logger = logging.getLogger(__name__)


class TechnicalDebtIntegrationOrchestrator:
    """
    Orchestrates all technical debt system integrations.

    Provides a unified interface for:
    - Agent status monitor integration
    - Master task log synchronization
    - Audit trail compliance
    - Automated task management
    """

    def __init__(self, debt_tracker: Optional[TechnicalDebtTracker] = None):
        """Initialize orchestrator with all integration components."""
        self.debt_tracker = debt_tracker or TechnicalDebtTracker()

        # Initialize integration components
        self.agent_integration = AgentStatusDebtIntegration(self.debt_tracker)
        self.task_integration = MasterTaskDebtIntegration(self.debt_tracker)
        self.audit_integration = AuditDebtIntegration(self.debt_tracker)

        logger.info("✅ Technical Debt Integration Orchestrator initialized")

    def run_full_integration_cycle(self) -> Dict[str, Any]:
        """
        Run complete integration cycle:
        1. Sync tasks to master log
        2. Assign tasks to available agents
        3. Update audit trail
        4. Generate reports

        Returns:
            Complete cycle results
        """
        logger.info("🚀 Starting full technical debt integration cycle")

        results = {
            "cycle_start": datetime.now().isoformat(),
            "steps": {},
            "overall_status": "in_progress"
        }

        try:
            # Step 1: Sync debt tasks to master task log
            logger.info("📋 Step 1: Syncing debt tasks to master task log")
            task_sync_result = self.task_integration.sync_debt_tasks_to_master_log()
            results["steps"]["task_sync"] = task_sync_result

            # Step 2: Assign debt tasks to agents
            logger.info("🤖 Step 2: Assigning debt tasks to agents")
            assignment_result = self.agent_integration.assign_debt_tasks()
            results["steps"]["task_assignment"] = assignment_result

            # Step 3: Audit task assignments
            logger.info("📊 Step 3: Auditing task assignments")
            audit_results = []
            if assignment_result.get("status") == "completed":
                assignments = assignment_result.get("assignments", [])
                for assignment in assignments:
                    audit_success = self.audit_integration.log_debt_task_assignment(assignment)
                    audit_results.append({
                        "assignment": assignment,
                        "audit_logged": audit_success
                    })
            results["steps"]["audit_logging"] = {
                "assignments_audited": len(audit_results),
                "audit_success_rate": len([r for r in audit_results if r["audit_logged"]]) / len(audit_results) if audit_results else 1.0
            }

            # Step 4: Generate progress report
            logger.info("📈 Step 4: Generating progress report")
            progress_data = self.task_integration.get_debt_task_summary()
            report_audit = self.audit_integration.log_debt_report_generation("integration_cycle", {
                "timestamp": datetime.now().isoformat(),
                "trigger": "automated_cycle",
                "format": "integrated",
                "destinations": ["master_log", "audit_trail"]
            })
            results["steps"]["progress_report"] = {
                "data": progress_data,
                "audit_logged": report_audit
            }

            # Step 5: Health check
            logger.info("🏥 Step 5: Performing system health check")
            health_data = self._perform_health_check()
            health_audit = self.audit_integration.log_debt_system_health_check(health_data)
            results["steps"]["health_check"] = {
                "data": health_data,
                "audit_logged": health_audit
            }

            results["overall_status"] = "completed"
            results["cycle_end"] = datetime.now().isoformat()

            logger.info("✅ Full technical debt integration cycle completed")
            return results

        except Exception as e:
            logger.error(f"❌ Technical debt integration cycle failed: {e}")
            results["overall_status"] = "failed"
            results["error"] = str(e)
            results["cycle_end"] = datetime.now().isoformat()
            return results

    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive status of the integrated debt system."""
        try:
            # Get debt summary
            debt_summary = self.task_integration.get_debt_task_summary()

            # Get agent availability
            agent_status = self.agent_integration.get_available_agents()

            # Get audit compliance
            audit_compliance = self.audit_integration.verify_debt_compliance()

            # Get assignment recommendations
            recommendations = self.agent_integration.get_assignment_recommendations()

            return {
                "status": "operational",
                "debt_summary": debt_summary,
                "agent_availability": {
                    "total_available": len(agent_status),
                    "agents": list(agent_status.keys())
                },
                "audit_compliance": audit_compliance,
                "assignment_recommendations": recommendations,
                "last_updated": datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"Failed to get system status: {e}")
            return {
                "status": "error",
                "error": str(e),
                "last_updated": datetime.now().isoformat()
            }

    def assign_specific_debt_task(self, category: str, agent_id: str) -> Dict[str, Any]:
        """
        Manually assign a specific debt task category to an agent.

        Args:
            category: Debt category to assign
            agent_id: Agent to assign to

        Returns:
            Assignment result
        """
        try:
            # Check if agent is available
            available_agents = self.agent_integration.get_available_agents()
            if agent_id not in available_agents:
                return {
                    "status": "agent_unavailable",
                    "message": f"Agent {agent_id} is not available for task assignment"
                }

            # Create manual assignment
            assignment = {
                "task": {
                    "category": category,
                    "priority": self.agent_integration._get_category_priority(category),
                    "pending_count": len(self.debt_tracker.debt_data.get("categories", {}).get(category, {}).get("pending", []))
                },
                "assigned_agent": agent_id,
                "timestamp": datetime.now().isoformat(),
                "capabilities_matched": self.agent_integration._get_category_capabilities(category)
            }

            # Log to audit trail
            audit_success = self.audit_integration.log_debt_task_assignment(assignment)

            return {
                "status": "assigned",
                "assignment": assignment,
                "audit_logged": audit_success
            }

        except Exception as e:
            logger.error(f"Failed to assign specific debt task: {e}")
            return {"status": "error", "message": str(e)}

    def generate_integrated_report(self, report_type: str = "comprehensive") -> Dict[str, Any]:
        """
        Generate a comprehensive report integrating all system data.

        Args:
            report_type: Type of report to generate

        Returns:
            Report data and metadata
        """
        try:
            # Collect data from all integrations
            system_status = self.get_system_status()
            audit_history = self.audit_integration.get_debt_audit_history(days=30)

            report = {
                "report_type": report_type,
                "generated_at": datetime.now().isoformat(),
                "system_status": system_status,
                "audit_history": audit_history,
                "sections": {}
            }

            # Executive Summary
            report["sections"]["executive_summary"] = {
                "total_debt_items": system_status.get("debt_summary", {}).get("total_pending_tasks", 0),
                "resolved_items": system_status.get("debt_summary", {}).get("total_resolved_tasks", 0),
                "available_agents": system_status.get("agent_availability", {}).get("total_available", 0),
                "audit_compliance": system_status.get("audit_compliance", {}).get("overall_compliance", False),
                "assignment_recommendations": system_status.get("assignment_recommendations", {}).get("recommended_count", 0)
            }

            # Detailed breakdown by category
            report["sections"]["debt_categories"] = system_status.get("debt_summary", {}).get("categories", {})

            # Agent workload analysis
            report["sections"]["agent_workload"] = {
                agent_id: agent_data
                for agent_id, agent_data in system_status.get("agent_availability", {}).get("agents", {}).items()
            }

            # Audit compliance details
            report["sections"]["audit_compliance"] = system_status.get("audit_compliance", {})

            # Recent audit events
            report["sections"]["recent_audits"] = audit_history.get("events", [])

            # Log report generation
            audit_success = self.audit_integration.log_debt_report_generation(report_type, {
                "timestamp": report["generated_at"],
                "trigger": "manual_request",
                "format": "integrated_json",
                "sections": list(report["sections"].keys())
            })

            report["audit_logged"] = audit_success

            return report

        except Exception as e:
            logger.error(f"Failed to generate integrated report: {e}")
            return {
                "report_type": report_type,
                "status": "error",
                "error": str(e),
                "generated_at": datetime.now().isoformat()
            }

    def _perform_health_check(self) -> Dict[str, Any]:
        """Perform comprehensive health check of debt system."""
        try:
            health_data = {
                "timestamp": datetime.now().isoformat(),
                "status": "healthy",
                "checks": {}
            }

            # Check debt tracker
            try:
                debt_data = self.debt_tracker.debt_data
                health_data["checks"]["debt_tracker"] = {
                    "status": "operational",
                    "last_updated": debt_data.get("last_updated", "unknown"),
                    "categories_count": len(debt_data.get("categories", {}))
                }
            except Exception as e:
                health_data["checks"]["debt_tracker"] = {"status": "error", "error": str(e)}

            # Check integrations
            try:
                agent_status = self.agent_integration.get_available_agents()
                health_data["checks"]["agent_integration"] = {
                    "status": "operational",
                    "agents_available": len(agent_status)
                }
            except Exception as e:
                health_data["checks"]["agent_integration"] = {"status": "error", "error": str(e)}

            try:
                task_summary = self.task_integration.get_debt_task_summary()
                health_data["checks"]["task_integration"] = {
                    "status": "operational",
                    "pending_tasks": task_summary.get("total_pending_tasks", 0)
                }
            except Exception as e:
                health_data["checks"]["task_integration"] = {"status": "error", "error": str(e)}

            try:
                audit_compliance = self.audit_integration.verify_debt_compliance()
                health_data["checks"]["audit_integration"] = {
                    "status": "operational",
                    "compliance": audit_compliance.get("overall_compliance", False)
                }
            except Exception as e:
                health_data["checks"]["audit_integration"] = {"status": "error", "error": str(e)}

            # Overall health assessment
            failed_checks = [check for check in health_data["checks"].values() if check.get("status") == "error"]
            if failed_checks:
                health_data["status"] = "degraded"
                health_data["issues"] = len(failed_checks)
            else:
                health_data["status"] = "healthy"

            return health_data

        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return {
                "timestamp": datetime.now().isoformat(),
                "status": "critical_error",
                "error": str(e)
            }

    def emergency_sync(self) -> Dict[str, Any]:
        """
        Emergency synchronization of all debt data.
        Use when systems are out of sync.

        Returns:
            Emergency sync results
        """
        logger.warning("🚨 Performing emergency debt system synchronization")

        try:
            # Force sync all integrations
            task_sync = self.task_integration.sync_debt_tasks_to_master_log()
            assignment_check = self.agent_integration.get_assignment_recommendations()
            audit_check = self.audit_integration.verify_debt_compliance()

            return {
                "status": "emergency_sync_completed",
                "task_sync": task_sync,
                "assignments": assignment_check,
                "audit_status": audit_check,
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"Emergency sync failed: {e}")
            return {
                "status": "emergency_sync_failed",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }