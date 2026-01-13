"""
<!-- SSOT Domain: core -->

Coordination Utilities - Shared V2 Compliant Utilities
Main coordination utilities module that aggregates focused utility modules
V2 Compliance: Under 300-line limit with modular architecture

@Author: Agent-6 - Gaming & Entertainment Specialist (Coordination & Communication V2 Compliance)
@Version: 2.0.0 - Modular DRY Violation Elimination
@License: MIT
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List

from .agent_matching import AgentMatchingUtils

# Performance Metrics Utilities - Lightweight implementation
class PerformanceMetricsUtils:
    """Lightweight performance metrics utilities.
    
    Provides basic metrics tracking without heavy dependencies.
    For advanced features, use StatsTracker or PerformanceMonitoringEngine.
    """
    _metrics_store: Dict[str, Any] = {}
    _history_store: List[Dict[str, Any]] = []
    _max_history_size: int = 1000

    @staticmethod
    def update_coordination_metrics(
        success: bool = True,
        coordination_time: float = 0.0,
        **kwargs
    ) -> None:
        """Update coordination metrics.
        
        Args:
            success: Whether coordination was successful
            coordination_time: Time taken for coordination
            **kwargs: Additional metric data
        """
        if "coordination" not in PerformanceMetricsUtils._metrics_store:
            PerformanceMetricsUtils._metrics_store["coordination"] = {
                "total": 0,
                "successful": 0,
                "failed": 0,
                "total_time": 0.0,
                "avg_time": 0.0,
            }
        
        metrics = PerformanceMetricsUtils._metrics_store["coordination"]
        metrics["total"] += 1
        
        if success:
            metrics["successful"] += 1
        else:
            metrics["failed"] += 1
        
        if coordination_time > 0:
            metrics["total_time"] += coordination_time
            metrics["avg_time"] = metrics["total_time"] / metrics["total"]

    @staticmethod
    def update_performance_metrics(
        task_id: str = None,
        execution_time: float = 0.0,
        success: bool = True,
        **kwargs
    ) -> None:
        """Update performance metrics.
        
        Args:
            task_id: Task identifier
            execution_time: Task execution time
            success: Whether task was successful
            **kwargs: Additional metric data
        """
        if "performance" not in PerformanceMetricsUtils._metrics_store:
            PerformanceMetricsUtils._metrics_store["performance"] = {
                "total_tasks": 0,
                "successful_tasks": 0,
                "failed_tasks": 0,
                "total_execution_time": 0.0,
                "avg_execution_time": 0.0,
            }
        
        metrics = PerformanceMetricsUtils._metrics_store["performance"]
        metrics["total_tasks"] += 1
        
        if success:
            metrics["successful_tasks"] += 1
        else:
            metrics["failed_tasks"] += 1
        
        if execution_time > 0:
            metrics["total_execution_time"] += execution_time
            metrics["avg_execution_time"] = (
                metrics["total_execution_time"] / metrics["total_tasks"]
            )

    @staticmethod
    def store_coordination_history(
        entry: Dict[str, Any] = None,
        **kwargs
    ) -> None:
        """Store coordination history entry.
        
        Args:
            entry: History entry dictionary
            **kwargs: Additional history data (merged into entry)
        """
        from datetime import datetime
        
        if entry is None:
            entry = {}
        
        # Merge kwargs into entry
        entry.update(kwargs)
        
        # Add timestamp if not present
        if "timestamp" not in entry:
            entry["timestamp"] = datetime.now().isoformat()
        
        PerformanceMetricsUtils._history_store.append(entry)
        
        # Limit history size
        if len(PerformanceMetricsUtils._history_store) > PerformanceMetricsUtils._max_history_size:
            PerformanceMetricsUtils._history_store = (
                PerformanceMetricsUtils._history_store[-PerformanceMetricsUtils._max_history_size:]
            )

    @staticmethod
    def get_performance_summary(metrics: Dict[str, Any] = None) -> Dict[str, Any]:
        """Get performance summary.
        
        Args:
            metrics: Optional metrics dictionary (uses stored if None)
        
        Returns:
            Performance summary dictionary
        """
        from datetime import datetime
        
        if metrics is None:
            metrics = PerformanceMetricsUtils._metrics_store.get("performance", {})
        
        return {
            "timestamp": datetime.now().isoformat(),
            "total_tasks": metrics.get("total_tasks", 0),
            "successful_tasks": metrics.get("successful_tasks", 0),
            "failed_tasks": metrics.get("failed_tasks", 0),
            "avg_execution_time": metrics.get("avg_execution_time", 0.0),
            "success_rate": (
                metrics.get("successful_tasks", 0) / metrics.get("total_tasks", 1)
                if metrics.get("total_tasks", 0) > 0
                else 0.0
            ),
        }

class VectorInsightsUtils:
    @staticmethod
    def enhance_data_with_vector_insights(*args, **kwargs): return {}
    @staticmethod
    def extract_recommendations_from_insights(*args, **kwargs): return []
    @staticmethod
    def generate_coordination_recommendations(*args, **kwargs): return []
    @staticmethod
    def create_enhanced_handler(*args, **kwargs): return None
    @staticmethod
    def save_coordination_insights(*args, **kwargs): pass
    @staticmethod
    def analyze_pattern_effectiveness(*args, **kwargs): return {}

class VectorDatabaseOperations:
    @staticmethod
    def load_coordination_patterns(*args, **kwargs): return []
    @staticmethod
    def load_agent_capabilities(*args, **kwargs): return {}
    @staticmethod
    def search_coordination_patterns(*args, **kwargs): return []
    @staticmethod
    def add_coordination_pattern(*args, **kwargs): pass
    @staticmethod
    def get_vector_database_status(*args, **kwargs): return {}

class CoordinationUtils:
    """Main coordination utilities class that aggregates focused utility modules.

    This class serves as a unified interface to all coordination utilities, providing
    backward compatibility while maintaining modular architecture.
    """

    # Agent Matching Methods - Direct delegation to avoid duplication
    calculate_agent_match_score = AgentMatchingUtils.calculate_agent_match_score
    get_agent_type_match_score = AgentMatchingUtils.get_agent_type_match_score

    # Performance Metrics Methods - Direct delegation to avoid duplication
    update_coordination_metrics = PerformanceMetricsUtils.update_coordination_metrics
    update_performance_metrics = PerformanceMetricsUtils.update_performance_metrics
    store_coordination_history = PerformanceMetricsUtils.store_coordination_history

    # Vector Insights Methods - Direct delegation to avoid duplication
    enhance_data_with_vector_insights = VectorInsightsUtils.enhance_data_with_vector_insights
    extract_recommendations_from_insights = (
        VectorInsightsUtils.extract_recommendations_from_insights
    )
    generate_coordination_recommendations = (
        VectorInsightsUtils.generate_coordination_recommendations
    )
    create_enhanced_handler = VectorInsightsUtils.create_enhanced_handler
    save_coordination_insights = VectorInsightsUtils.save_coordination_insights

    # Vector Database Operations - Direct delegation to avoid duplication
    load_coordination_patterns = VectorDatabaseOperations.load_coordination_patterns
    load_agent_capabilities = VectorDatabaseOperations.load_agent_capabilities
    search_coordination_patterns = VectorDatabaseOperations.search_coordination_patterns
    add_coordination_pattern = VectorDatabaseOperations.add_coordination_pattern
    get_vector_database_status = VectorDatabaseOperations.get_vector_database_status

    # Additional Utility Methods
    @staticmethod
    def get_coordination_summary(
        metrics: Dict[str, Any], coordination_history: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Get comprehensive coordination summary.

        Args:
            metrics: Performance metrics dictionary
            coordination_history: List of coordination history entries

        Returns:
            Comprehensive coordination summary
        """
        performance_summary = PerformanceMetricsUtils.get_performance_summary(metrics)
        pattern_analysis = VectorInsightsUtils.analyze_pattern_effectiveness(coordination_history)

        return {
            "performance_metrics": performance_summary,
            "pattern_analysis": pattern_analysis,
            "total_history_entries": len(coordination_history),
            "summary_timestamp": performance_summary.get("timestamp", "unknown"),
        }

    @staticmethod
    def validate_coordination_data(data: Dict[str, Any]) -> bool:
        """Validate coordination data structure.

        Args:
            data: Coordination data to validate

        Returns:
            True if data is valid, False otherwise
        """
        required_fields = ["agent_type", "task_requirements"]

        for field in required_fields:
            if field not in data:
                return False

        return True


# Export main interfaces
__all__ = [
    "CoordinationUtils",
    "AgentCapability",
    "CoordinationMetrics",
    "AgentMatchingUtils",
    "PerformanceMetricsUtils",
    "VectorInsightsUtils",
    "VectorDatabaseOperations",
]
