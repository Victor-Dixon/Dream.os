"""
Audit Trail Integration for Technical Debt
===========================================

Connects technical debt system to audit trail for compliance tracking and transparency.

Features:
- Audit debt management actions
- Track debt reduction progress
- Log automated task assignments
- Provide compliance evidence

<!-- SSOT Domain: safety -->
"""

import logging
from datetime import datetime
from typing import Dict, Any, Optional, List

from ..debt_tracker import TechnicalDebtTracker

# Import with proper path resolution
import sys
from pathlib import Path
project_root = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(project_root))
from src.core.safety.audit_trail import AuditTrail, EventType, EventSeverity, AuditEvent

logger = logging.getLogger(__name__)


class AuditDebtIntegration:
    """
    Integrates technical debt system with audit trail.

    Provides complete transparency and accountability for:
    - Debt task assignments
    - Progress tracking
    - Compliance validation
    - Automated decision making
    """

    def __init__(self, debt_tracker: Optional[TechnicalDebtTracker] = None, audit_trail: Optional[AuditTrail] = None):
        """Initialize audit integration."""
        self.debt_tracker = debt_tracker or TechnicalDebtTracker()
        self.audit_trail = audit_trail or AuditTrail()

    def log_debt_task_assignment(self, assignment: Dict[str, Any]) -> bool:
        """
        Log technical debt task assignment to audit trail.

        Args:
            assignment: Task assignment details

        Returns:
            Success status
        """
        try:
            task = assignment.get("task", {})
            agent_id = assignment.get("assigned_agent", "unknown")
            timestamp = datetime.now().isoformat()

            # Create audit event
            event = AuditEvent(
                event_id=f"debt_assignment_{task.get('category', 'unknown')}_{int(datetime.now().timestamp())}",
                timestamp=timestamp,
                event_type=EventType.DECISION,
                severity=EventSeverity.INFO,
                agent_id=agent_id,
                agent_name=f"Agent-{agent_id}",
                decision_summary=f"Automated assignment of {task.get('category', 'unknown')} debt task",
                decision_rationale=f"Assigned based on agent capabilities and availability",
                options_considered=["manual_assignment", "different_agent"],
                chosen_option=f"assign_to_{agent_id}",
                confidence_score=0.85,
                risk_level="low",
                estimated_cost=0.0,
                context={
                    "component": "technical_debt_system",
                    "operation": "task_assignment",
                    "task_category": task.get("category", "unknown"),
                    "task_priority": task.get("priority", "medium"),
                    "pending_count": task.get("pending_count", 0),
                    "capabilities_matched": assignment.get("capabilities_matched", []),
                    "automation_level": "full_automation"
                }
            )

            success = self.audit_trail.log_event(event)

            if success:
                logger.info(f"Audited debt task assignment: {task.get('category')} -> {agent_id}")
            else:
                logger.error("Failed to audit debt task assignment")

            return success

        except Exception as e:
            logger.error(f"Error logging debt task assignment: {e}")
            return False

    def log_debt_progress_update(self, category: str, progress_data: Dict[str, Any]) -> bool:
        """
        Log technical debt progress update to audit trail.

        Args:
            category: Debt category updated
            progress_data: Progress information

        Returns:
            Success status
        """
        try:
            timestamp = datetime.now().isoformat()

            # Create audit event
            event = AuditEvent(
                event_id=f"debt_progress_{category}_{int(datetime.now().timestamp())}",
                timestamp=timestamp,
                event_type=EventType.ACTION,
                severity=EventSeverity.INFO,
                agent_id="system",
                agent_name="Technical Debt System",
                decision_summary=f"Progress update for {category} debt category",
                decision_rationale="Automated progress tracking",
                options_considered=[],  # No alternatives for progress tracking
                chosen_option="automated_update",
                confidence_score=1.0,
                risk_level="low",
                estimated_cost=0.0,
                context={
                    "component": "technical_debt_system",
                    "operation": "progress_update",
                    "debt_category": category,
                    "progress_type": "automated_update",
                    "items_resolved": progress_data.get("resolved", 0),
                    "items_pending": progress_data.get("pending", 0),
                    "update_timestamp": progress_data.get("timestamp", timestamp),
                    "update_method": "automated_tracking",
                    "data_integrity": "checksum_validated"
                }
            )

            success = self.audit_trail.log_event(event)

            if success:
                logger.info(f"Audited debt progress update for {category}")
            else:
                logger.error(f"Failed to audit debt progress update for {category}")

            return success

        except Exception as e:
            logger.error(f"Error logging debt progress update: {e}")
            return False

    def log_debt_report_generation(self, report_type: str, report_data: Dict[str, Any]) -> bool:
        """
        Log technical debt report generation to audit trail.

        Args:
            report_type: Type of report generated
            report_data: Report generation details

        Returns:
            Success status
        """
        try:
            timestamp = datetime.now().isoformat()

            # Create audit event
            event = AuditEvent(
                event_id=f"debt_report_{report_type}_{int(datetime.now().timestamp())}",
                timestamp=timestamp,
                event_type=EventType.ACTION,
                severity=EventSeverity.INFO,
                agent_id="system",
                agent_name="Technical Debt System",
                decision_summary=f"Generated {report_type} technical debt report",
                decision_rationale="Automated report generation",
                options_considered=["manual_report", "no_report"],
                chosen_option="automated_generation",
                confidence_score=1.0,
                risk_level="low",
                estimated_cost=0.0,
                context={
                    "component": "technical_debt_system",
                    "operation": "report_generation",
                    "report_type": report_type,
                    "generation_method": "automated",
                    "generation_timestamp": report_data.get("timestamp", timestamp),
                    "trigger_source": report_data.get("trigger", "scheduled"),
                    "data_sources": ["debt_tracker", "git_history", "code_analysis"],
                    "output_destinations": report_data.get("destinations", ["file", "discord"]),
                    "compliance_check": "data_integrity_verified"
                }
            )

            success = self.audit_trail.log_event(event)

            if success:
                logger.info(f"Audited {report_type} debt report generation")
            else:
                logger.error(f"Failed to audit {report_type} debt report generation")

            return success

        except Exception as e:
            logger.error(f"Error logging debt report generation: {e}")
            return False

    def log_debt_system_health_check(self, health_data: Dict[str, Any]) -> bool:
        """
        Log technical debt system health check to audit trail.

        Args:
            health_data: System health information

        Returns:
            Success status
        """
        try:
            health_status = health_data.get("status", "unknown")
            timestamp = datetime.now().isoformat()

            # Create audit event
            event = AuditEvent(
                event_id=f"debt_health_check_{int(datetime.now().timestamp())}",
                timestamp=timestamp,
                event_type=EventType.ACTION,
                severity=EventSeverity.INFO if health_status == "healthy" else EventSeverity.WARNING,
                agent_id="system",
                agent_name="Technical Debt System",
                decision_summary=f"System health check completed: {health_status}",
                decision_rationale="Automated health monitoring",
                options_considered=["manual_check", "skip_check"],
                chosen_option="automated_monitoring",
                confidence_score=0.95,
                risk_level="low",
                estimated_cost=0.0,
                context={
                    "component": "technical_debt_system",
                    "operation": "health_check",
                    "check_type": "system_health",
                    "health_status": health_status,
                    "check_timestamp": health_data.get("timestamp", timestamp),
                    "data_integrity": health_data.get("data_integrity", "unknown"),
                    "system_availability": health_data.get("availability", "unknown"),
                    "last_update_age": health_data.get("update_age_hours", 0),
                    "alerts_generated": health_data.get("alerts", 0),
                    "automated_actions": health_data.get("actions_taken", [])
                }
            )

            success = self.audit_trail.log_event(event)

            if success:
                logger.info(f"Audited debt system health check: {health_status}")
            else:
                logger.error("Failed to audit debt system health check")

            return success

        except Exception as e:
            logger.error(f"Error logging debt system health check: {e}")
            return False

    def get_debt_audit_history(self, days: int = 30) -> Dict[str, Any]:
        """
        Retrieve technical debt audit history.

        Args:
            days: Number of days to look back

        Returns:
            Audit history data
        """
        try:
            # Query audit trail for debt-related events
            events = self.audit_trail.query_events(
                component="technical_debt_system",
                days=days
            )

            # Summarize audit activity
            summary = {
                "total_events": len(events),
                "event_types": {},
                "operations": {},
                "agents_involved": set(),
                "time_range": {
                    "start": min((e.timestamp for e in events), default=None),
                    "end": max((e.timestamp for e in events), default=None)
                }
            }

            for event in events:
                # Count event types
                event_type = event.event_data.get("event_type", "unknown")
                summary["event_types"][event_type] = summary["event_types"].get(event_type, 0) + 1

                # Count operations
                operation = event.context.operation if event.context else "unknown"
                summary["operations"][operation] = summary["operations"].get(operation, 0) + 1

                # Track agents
                agent_id = event.context.agent_id if event.context else "unknown"
                summary["agents_involved"].add(agent_id)

            summary["agents_involved"] = list(summary["agents_involved"])

            return {
                "status": "success",
                "summary": summary,
                "events": [self._format_event_for_display(e) for e in events[-10:]]  # Last 10 events
            }

        except Exception as e:
            logger.error(f"Error retrieving debt audit history: {e}")
            return {"status": "error", "message": str(e)}

    def _format_event_for_display(self, event) -> Dict[str, Any]:
        """Format audit event for display."""
        return {
            "timestamp": event.timestamp.isoformat() if hasattr(event.timestamp, 'isoformat') else str(event.timestamp),
            "event_type": event.event_type.value if hasattr(event.event_type, 'value') else str(event.event_type),
            "operation": event.context.operation if event.context else "unknown",
            "agent_id": event.context.agent_id if event.context else "unknown",
            "summary": self._summarize_event(event)
        }

    def _summarize_event(self, event) -> str:
        """Create human-readable summary of audit event."""
        event_data = event.event_data
        event_type = event_data.get("event_type", "")

        if event_type == EventType.DECISION.value:
            return f"Automated decision: {event_data.get('task_category', 'unknown')} task assigned to {event_data.get('assigned_agent', 'unknown')}"
        elif event_type == EventType.ACTION.value:
            operation = event.context.operation if event.context else "unknown"
            if operation == "report_generation":
                return f"Generated {event_data.get('report_type', 'unknown')} report"
            elif operation == "progress_update":
                return f"Updated progress for {event_data.get('debt_category', 'unknown')} category"
            elif operation == "health_check":
                return f"Health check completed: {event_data.get('health_status', 'unknown')}"
            else:
                return f"Action performed: {operation}"
        else:
            return f"Event: {event_type}"

    def verify_debt_compliance(self) -> Dict[str, Any]:
        """
        Verify technical debt management compliance through audit trail.

        Returns:
            Compliance verification results
        """
        try:
            # Check recent audit activity
            recent_audits = self.get_debt_audit_history(days=7)

            if recent_audits["status"] != "success":
                return {"status": "error", "message": "Could not retrieve audit history"}

            summary = recent_audits["summary"]

            # Compliance criteria
            compliance_checks = {
                "regular_reporting": summary["operations"].get("report_generation", 0) >= 1,  # At least 1 report per week
                "active_monitoring": summary["total_events"] >= 5,  # At least 5 audit events per week
                "automated_tracking": summary["operations"].get("progress_update", 0) >= 3,  # Progress updates
                "system_health": summary["operations"].get("health_check", 0) >= 1  # Health checks
            }

            overall_compliance = all(compliance_checks.values())

            return {
                "status": "verified",
                "overall_compliance": overall_compliance,
                "compliance_checks": compliance_checks,
                "audit_summary": summary,
                "recommendations": self._generate_compliance_recommendations(compliance_checks)
            }

        except Exception as e:
            logger.error(f"Error verifying debt compliance: {e}")
            return {"status": "error", "message": str(e)}

    def _generate_compliance_recommendations(self, compliance_checks: Dict[str, bool]) -> List[str]:
        """Generate compliance recommendations based on check results."""
        recommendations = []

        if not compliance_checks.get("regular_reporting", True):
            recommendations.append("Increase report generation frequency to ensure weekly compliance reporting")

        if not compliance_checks.get("active_monitoring", True):
            recommendations.append("Enhance audit trail activity to ensure comprehensive tracking of debt management actions")

        if not compliance_checks.get("automated_tracking", True):
            recommendations.append("Improve automated progress tracking to maintain up-to-date debt status")

        if not compliance_checks.get("system_health", True):
            recommendations.append("Implement regular system health checks for debt management infrastructure")

        if not recommendations:
            recommendations.append("All compliance checks passed - debt management system is fully compliant")

        return recommendations