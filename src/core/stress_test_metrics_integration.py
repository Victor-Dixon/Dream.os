#!/usr/bin/env python3
"""
<!-- SSOT Domain: core -->
Stress Test Metrics Integration
================================

Integration helpers for stress test metrics collection:
- Integration with message queue processor
- Integration with messaging infrastructure
- Helper functions for stress test runner

Author: Agent-5 (Business Intelligence Specialist)
Date: 2025-11-28
License: MIT
"""

import logging
import time
from typing import Any, Optional

from .stress_test_metrics import (
    StressTestMetricsCollector,
    StressTestAnalyzer,
)

logger = logging.getLogger(__name__)


class StressTestMetricsIntegration:
    """Integration layer for stress test metrics in messaging system."""
    
    def __init__(self, collector: Optional[StressTestMetricsCollector] = None):
        """Initialize metrics integration."""
        self.collector = collector or StressTestMetricsCollector()
        self.logger = logger
    
    def integrate_with_message_queue(self, message_queue) -> None:
        """
        Integrate metrics collection with message queue processor.
        
        This should be called to hook into message queue events.
        """
        # Example integration - would need to adapt to actual message queue implementation
        self.logger.info("Metrics integration with message queue initialized")
    
    def record_queue_event(
        self,
        event_type: str,
        queue_id: str,
        agent_id: Optional[str] = None,
        message_type: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        """Record a queue event for metrics collection."""
        if event_type == "message_queued":
            self.collector.record_message_sent(agent_id, message_type)
            # Record queue depth if available
            if "queue_depth" in kwargs:
                self.collector.record_queue_depth(kwargs["queue_depth"])
        
        elif event_type == "message_delivered":
            latency_ms = kwargs.get("latency_ms", 0)
            delivery_mode = kwargs.get("delivery_mode", "real")
            self.collector.record_message_delivered(
                latency_ms, agent_id, message_type, delivery_mode
            )
        
        elif event_type == "message_failed":
            reason = kwargs.get("reason", "unknown")
            self.collector.record_message_failed(agent_id, message_type, reason)
    
    def integrate_with_stress_test_runner(self, test_config: dict[str, Any]) -> StressTestMetricsCollector:
        """
        Initialize metrics collection for stress test run.
        
        Args:
            test_config: Configuration for the stress test
            
        Returns:
            Metrics collector instance
        """
        self.collector.start_test(test_config)
        self.logger.info("Stress test metrics collection started")
        return self.collector
    
    def finalize_stress_test(self, output_dir: Optional[str] = None) -> dict[str, Any]:
        """
        Finalize stress test and generate dashboard.
        
        Args:
            output_dir: Optional directory to save JSON dashboard
            
        Returns:
            Dashboard dictionary
        """
        self.collector.stop_test()
        
        from pathlib import Path
        output_path = Path(output_dir) if output_dir else Path("stress_test_results")
        output_path.mkdir(exist_ok=True)
        
        dashboard = self.collector.generate_dashboard_json(output_path)
        
        # Analyze results
        analyzer = StressTestAnalyzer()
        bottlenecks = analyzer.identify_bottlenecks(dashboard)
        failure_patterns = analyzer.analyze_failure_patterns(dashboard)
        
        # Add analysis to dashboard
        dashboard["analysis"] = {
            "bottlenecks": bottlenecks,
            "failure_patterns": failure_patterns,
        }
        
        # Save updated dashboard
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = output_path / f"stress_test_results_{timestamp}.json"
        
        import json
        with open(filename, "w") as f:
            json.dump(dashboard, f, indent=2)
        
        self.logger.info(f"Stress test finalized - dashboard saved to {filename}")
        
        return dashboard


def create_stress_test_integration(
    collector: Optional[StressTestMetricsCollector] = None
) -> StressTestMetricsIntegration:
    """Create stress test metrics integration."""
    return StressTestMetricsIntegration(collector)


__all__ = [
    "StressTestMetricsIntegration",
    "create_stress_test_integration",
]

