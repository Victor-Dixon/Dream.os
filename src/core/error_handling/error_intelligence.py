#!/usr/bin/env python3
"""
<!-- SSOT Domain: core -->

Error Intelligence & Predictive Models - Agent Cellphone V2
===========================================================

Intelligent error analysis, pattern detection, and predictive error handling.
Enables autonomous systems to learn from error history and predict failures.

Author: Agent-5 (Business Intelligence & Team Beta Leader)
License: MIT
"""

import logging
from collections import defaultdict, deque
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import Any
from dataclasses import dataclass, field


logger = logging.getLogger(__name__)


class ErrorTrend(Enum):
    """Error trend indicators."""

    INCREASING = "increasing"
    DECREASING = "decreasing"
    STABLE = "stable"
    SPIKE = "spike"


@dataclass
class ErrorPattern:
    """Detected error pattern."""

    error_type: str
    component: str
    frequency: int
    trend: ErrorTrend
    last_occurrence: datetime
    suggested_action: str


@dataclass
class ErrorMetrics:
    """Error metrics for a component."""

    total_errors: int = 0
    recoverable_errors: int = 0
    critical_errors: int = 0
    recovery_success_rate: float = 0.0
    average_recovery_time: float = 0.0
    health_score: float = 100.0


class ErrorIntelligenceEngine:
    """Intelligent error analysis and prediction system.

    Analyzes error patterns, predicts failures, and suggests recovery strategies
    based on historical data and learning.
    """

    def __init__(self, history_window: int = 1000, analysis_interval: int = 100):
        """Initialize error intelligence engine.

        Args:
            history_window: Number of error records to maintain
            analysis_interval: Number of errors before running pattern analysis
        """
        self.history_window = history_window
        self.analysis_interval = analysis_interval

        # Error tracking
        self.error_history: deque = deque(maxlen=history_window)
        self.component_errors: dict[str, list] = defaultdict(list)
        self.error_type_counts: dict[str, int] = defaultdict(int)

        # Pattern detection
        self.detected_patterns: list[ErrorPattern] = []
        self.component_metrics: dict[str, ErrorMetrics] = defaultdict(ErrorMetrics)

        # Learning data
        self.recovery_success: dict[str, list[bool]] = defaultdict(list)
        self.recovery_times: dict[str, list[float]] = defaultdict(list)

        logger.info("Error Intelligence Engine initialized")

    def record_error(
        self,
        error_type: str,
        component: str,
        severity: str = "medium",
        context: dict[str, Any] | None = None,
    ) -> None:
        """Record an error occurrence for analysis.

        Args:
            error_type: Type of error
            component: Component where error occurred
            severity: Error severity (low, medium, high, critical)
            context: Additional error context
        """
        error_record = self._create_error_record(error_type, component, severity, context)
        self._store_error_record(error_record, component)
        self._update_metrics(component, severity)
        self._trigger_pattern_analysis()

    def _create_error_record(
        self, error_type: str, component: str, severity: str, context: dict[str, Any] | None
    ) -> dict[str, Any]:
        """Create error record dictionary."""
        return {
            "type": error_type,
            "component": component,
            "severity": severity,
            "timestamp": datetime.now(),
            "context": context or {},
        }

    def _store_error_record(self, error_record: dict[str, Any], component: str) -> None:
        """Store error record in history and component tracking."""
        self.error_history.append(error_record)
        self.component_errors[component].append(error_record)
        if len(self.component_errors[component]) > self.history_window:
            self.component_errors[component] = self.component_errors[component][
                -self.history_window :
            ]
        self.error_type_counts[error_record["type"]] += 1

    def _update_metrics(self, component: str, severity: str) -> None:
        """Update component metrics based on error."""
        metrics = self.component_metrics[component]
        metrics.total_errors += 1
        if severity == "critical":
            metrics.critical_errors += 1
        else:
            metrics.recoverable_errors += 1

    def _trigger_pattern_analysis(self) -> None:
        """Trigger pattern analysis if threshold reached."""
        if len(self.error_history) % self.analysis_interval == 0:
            self._analyze_patterns()

    def record_recovery(self, component: str, success: bool, recovery_time: float) -> None:
        """Record recovery attempt outcome for learning.

        Args:
            component: Component being recovered
            success: Whether recovery succeeded
            recovery_time: Time taken for recovery attempt
        """
        self.recovery_success[component].append(success)
        self.recovery_times[component].append(recovery_time)

        # Memory leak fix: Limit recovery history to 100 entries (only last 100 used for metrics)
        if len(self.recovery_success[component]) > 100:
            self.recovery_success[component] = self.recovery_success[component][-100:]
        if len(self.recovery_times[component]) > 100:
            self.recovery_times[component] = self.recovery_times[component][-100:]

        # Update metrics
        metrics = self.component_metrics[component]
        success_list = self.recovery_success[component][-100:]  # Last 100 attempts
        metrics.recovery_success_rate = (
            sum(success_list) / len(success_list) if success_list else 0.0
        )

        time_list = self.recovery_times[component][-100:]
        metrics.average_recovery_time = sum(time_list) / len(time_list) if time_list else 0.0

        # Calculate health score
        metrics.health_score = self._calculate_health_score(component)

    def predict_failure_risk(self, component: str) -> tuple[float, str]:
        """Predict failure risk for a component.

        Args:
            component: Component to analyze

        Returns:
            Tuple of (risk_score, risk_level) where:
            - risk_score: 0.0-1.0 (0=low, 1=high)
            - risk_level: 'low', 'medium', 'high', 'critical'
        """
        if component not in self.component_errors:
            return 0.0, "low"

        risk_factors = self._calculate_risk_factors(component)
        risk_score = self._compute_weighted_risk(risk_factors)
        risk_level = self._classify_risk_level(risk_score)

        return risk_score, risk_level

    def _calculate_risk_factors(self, component: str) -> dict[str, float]:
        """Calculate risk factors for a component."""
        recent_errors = self._get_recent_errors(component, hours=1)
        error_rate = len(recent_errors) / 60.0  # Errors per minute
        metrics = self.component_metrics[component]

        return {
            "error_rate": min(error_rate / 10.0, 1.0),
            "critical_ratio": (metrics.critical_errors / max(metrics.total_errors, 1)),
            "recovery_failure": 1.0 - metrics.recovery_success_rate,
            "health_decline": 1.0 - (metrics.health_score / 100.0),
        }

    def _compute_weighted_risk(self, risk_factors: dict[str, float]) -> float:
        """Compute weighted risk score from factors."""
        return (
            risk_factors["error_rate"] * 0.3
            + risk_factors["critical_ratio"] * 0.3
            + risk_factors["recovery_failure"] * 0.2
            + risk_factors["health_decline"] * 0.2
        )

    def _classify_risk_level(self, risk_score: float) -> str:
        """Classify risk level from score."""
        if risk_score >= 0.75:
            return "critical"
        elif risk_score >= 0.5:
            return "high"
        elif risk_score >= 0.25:
            return "medium"
        else:
            return "low"

    def suggest_recovery_strategy(self, error_type: str, component: str) -> str:
        """Suggest optimal recovery strategy based on historical success.

        Args:
            error_type: Type of error
            component: Component affected

        Returns:
            Suggested recovery strategy name
        """
        # Analyze historical recovery success for this error type
        success_rate = self.component_metrics[component].recovery_success_rate

        if success_rate < 0.3:
            return "configuration_reset"  # Low success, try reset
        elif success_rate < 0.7:
            return "service_restart"  # Medium success, try restart
        else:
            return "retry_with_backoff"  # High success, retry is sufficient

    def get_component_health(self, component: str) -> dict[str, Any]:
        """Get comprehensive health report for a component.

        Args:
            component: Component to analyze

        Returns:
            Health report dictionary
        """
        metrics = self.component_metrics[component]
        risk_score, risk_level = self.predict_failure_risk(component)

        return {
            "component": component,
            "health_score": round(metrics.health_score, 2),
            "risk_level": risk_level,
            "risk_score": round(risk_score, 3),
            "total_errors": metrics.total_errors,
            "critical_errors": metrics.critical_errors,
            "recovery_success_rate": round(metrics.recovery_success_rate, 2),
            "average_recovery_time": round(metrics.average_recovery_time, 2),
            "trend": self._get_error_trend(component),
            "patterns": [p for p in self.detected_patterns if p.component == component],
        }

    def get_system_intelligence_report(self) -> dict[str, Any]:
        """Generate comprehensive intelligence report for entire system.

        Returns:
            System-wide intelligence report
        """
        summary = self._calculate_system_summary()
        high_risk_components = self._identify_high_risk_components()
        patterns_data = self._format_detected_patterns()
        component_health = self._get_all_component_health()

        return {
            "summary": summary,
            "high_risk_components": high_risk_components,
            "detected_patterns": patterns_data,
            "component_health": component_health,
        }

    def _calculate_system_summary(self) -> dict[str, Any]:
        """Calculate system-wide summary statistics."""
        total_errors = sum(m.total_errors for m in self.component_metrics.values())
        total_critical = sum(m.critical_errors for m in self.component_metrics.values())
        high_risk_count = len(self._identify_high_risk_components())

        return {
            "total_errors": total_errors,
            "critical_errors": total_critical,
            "components_tracked": len(self.component_metrics),
            "high_risk_components": high_risk_count,
            "patterns_detected": len(self.detected_patterns),
        }

    def _identify_high_risk_components(self) -> list[str]:
        """Identify components with high or critical risk."""
        return [
            comp
            for comp in self.component_metrics.keys()
            if self.predict_failure_risk(comp)[1] in ("high", "critical")
        ]

    def _format_detected_patterns(self) -> list[dict[str, Any]]:
        """Format detected patterns for report."""
        return [
            {
                "error_type": p.error_type,
                "component": p.component,
                "frequency": p.frequency,
                "trend": p.trend.value,
                "suggested_action": p.suggested_action,
            }
            for p in self.detected_patterns
        ]

    def _get_all_component_health(self) -> dict[str, Any]:
        """Get health status for all components."""
        return {
            comp: self.get_component_health(comp) for comp in self.component_metrics.keys()
        }

    def _analyze_patterns(self) -> None:
        """Analyze error history for patterns."""
        self.detected_patterns.clear()

        for component in self.component_errors.keys():
            recent_errors = self._get_recent_errors(component, hours=24)

            if not recent_errors:
                continue

            # Detect error type patterns
            error_types = defaultdict(int)
            for error in recent_errors:
                error_types[error["type"]] += 1

            for error_type, frequency in error_types.items():
                if frequency >= 5:  # Threshold for pattern
                    trend = self._get_error_trend(component)
                    suggested_action = self.suggest_recovery_strategy(error_type, component)

                    pattern = ErrorPattern(
                        error_type=error_type,
                        component=component,
                        frequency=frequency,
                        trend=trend,
                        last_occurrence=recent_errors[-1]["timestamp"],
                        suggested_action=suggested_action,
                    )
                    self.detected_patterns.append(pattern)

    def _get_recent_errors(self, component: str, hours: int = 1) -> list:
        """Get recent errors for a component within time window."""
        cutoff = datetime.now() - timedelta(hours=hours)
        return [e for e in self.component_errors.get(component, []) if e["timestamp"] > cutoff]

    def _get_error_trend(self, component: str) -> ErrorTrend:
        """Determine error trend for a component."""
        recent_1h = len(self._get_recent_errors(component, hours=1))
        recent_24h = len(self._get_recent_errors(component, hours=24))

        if recent_1h >= 20:
            return ErrorTrend.SPIKE
        elif recent_1h > recent_24h / 24 * 2:  # More than 2x hourly average
            return ErrorTrend.INCREASING
        elif recent_1h < recent_24h / 24 * 0.5:  # Less than half hourly average
            return ErrorTrend.DECREASING
        else:
            return ErrorTrend.STABLE

    def _calculate_health_score(self, component: str) -> float:
        """Calculate health score for a component (0-100)."""
        metrics = self.component_metrics[component]

        # Base score starts at 100
        score = 100.0

        # Deduct points for errors
        error_penalty = min(metrics.total_errors * 0.1, 30.0)
        score -= error_penalty

        # Deduct points for critical errors
        critical_penalty = min(metrics.critical_errors * 2.0, 30.0)
        score -= critical_penalty

        # Deduct points for low recovery success
        recovery_penalty = (1.0 - metrics.recovery_success_rate) * 20.0
        score -= recovery_penalty

        # Add bonus for high recovery success
        if metrics.recovery_success_rate > 0.9:
            score += 10.0

        return max(0.0, min(100.0, score))


# Global intelligence engine instance
intelligence_engine = ErrorIntelligenceEngine()
