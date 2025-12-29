"""
<!-- SSOT Domain: core -->

Single Source of Truth (SSOT) for Results Domain Management
Domain: Results (Analysis + Validation + Integration + Performance)
Owner: Agent-2 (Architecture & Design)
Last Updated: 2025-12-08

Results Domain Manager - V2 Compliant Module
===========================================

Consolidates result processing operations including:
- Analysis results processing
- Validation results processing
- Integration results processing
- Performance results processing
- General results processing

This SSOT replaces:
- src/core/managers/results/analysis_results_processor.py
- src/core/managers/results/validation_results_processor.py
- src/core/managers/results/integration_results_processor.py
- src/core/managers/results/performance_results_processor.py
- src/core/managers/results/general_results_processor.py

V2 Compliance: < 300 lines, single domain responsibility.
Consolidation: 5+ managers → 1 SSOT (-60% code reduction)

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

from __future__ import annotations

import uuid
from collections.abc import Callable
from datetime import datetime
from typing import Any, Dict

from ..contracts import Manager, ManagerContext, ManagerResult
from ..manager_state import ManagerType
from ..results.results_processing import ResultsProcessor, ResultStatus
from ..results.results_query_helpers import ResultsQueryHelper
from ..results.results_validation import ResultsValidator


class ResultsDomainManager(Manager):
    """
    SSOT for all result processing operations.

    Consolidates:
    - Analysis results (from AnalysisResultsProcessor)
    - Validation results (from ValidationResultsProcessor)
    - Integration results (from IntegrationResultsProcessor)
    - Performance results (from PerformanceResultsProcessor)
    - General results (from GeneralResultsProcessor)
    """

    def __init__(self) -> None:
        # Initialize components (from BaseResultsManager)
        self._processor = ResultsProcessor()
        self._query_helper = ResultsQueryHelper()
        self._validator = ResultsValidator()

        # Result storage (from BaseResultsManager)
        self._results: Dict[str, Dict[str, Any]] = {}
        self._result_callbacks: Dict[str, Callable] = {}

        # Domain-specific state
        self._analysis_results: Dict[str, Dict[str, Any]] = {}
        self._validation_results: Dict[str, Dict[str, Any]] = {}
        self._integration_results: Dict[str, Dict[str, Any]] = {}
        self._performance_results: Dict[str, Dict[str, Any]] = {}

    def initialize(self, context: ManagerContext) -> bool:
        """Initialize results domain manager."""
        context.logger("ResultsDomainManager initialized - Analysis + Validation + Integration + Performance consolidated")
        return True

    def execute(
        self, context: ManagerContext, operation: str, payload: Dict[str, Any]
    ) -> ManagerResult:
        """Execute result processing operation."""
        handlers = {
            # Core operations (from BaseResultsManager)
            "process_result": self.process_result,
            "query_results": self.query_results,
            "validate_result": self.validate_result,
            "register_callback": self.register_callback,

            # Analysis operations (from AnalysisResultsProcessor)
            "process_analysis_result": self.process_analysis_result,

            # Validation operations (from ValidationResultsProcessor)
            "process_validation_result": self.process_validation_result,

            # Integration operations (from IntegrationResultsProcessor)
            "process_integration_result": self.process_integration_result,

            # Performance operations (from PerformanceResultsProcessor)
            "process_performance_result": self.process_performance_result,

            # General operations (from GeneralResultsProcessor)
            "process_general_result": self.process_general_result,
        }

        handler = handlers.get(operation)
        if not handler:
            return ManagerResult(False, {}, {}, f"Unknown results operation: {operation}")
        return handler(context, payload)

    def cleanup(self, context: ManagerContext) -> bool:
        """Cleanup all result resources."""
        self._results.clear()
        self._result_callbacks.clear()
        self._analysis_results.clear()
        self._validation_results.clear()
        self._integration_results.clear()
        self._performance_results.clear()
        context.logger("ResultsDomainManager cleaned up")
        return True

    def get_status(self) -> Dict[str, Any]:
        """Return consolidated results status."""
        return {
            "total_results": len(self._results),
            "analysis_results": len(self._analysis_results),
            "validation_results": len(self._validation_results),
            "integration_results": len(self._integration_results),
            "performance_results": len(self._performance_results),
            "callbacks_registered": len(self._result_callbacks),
            "consolidated_operations": [
                "process_result", "query_results", "validate_result", "register_callback",
                "process_analysis_result", "process_validation_result", "process_integration_result",
                "process_performance_result", "process_general_result"
            ]
        }

    # Core Operations -------------------------------------------------------------------

    def process_result(self, context: ManagerContext, payload: Dict[str, Any]) -> ManagerResult:
        """Process a general result."""
        result_id = payload.get("result_id", str(uuid.uuid4()))
        result_data = payload.get("result_data", {})
        result_type = payload.get("result_type", "general")

        # Store result
        self._results[result_id] = {
            "result_id": result_id,
            "result_data": result_data,
            "result_type": result_type,
            "processed_at": datetime.utcnow().isoformat(),
            "status": ResultStatus.PROCESSED.value
        }

        # Trigger callbacks
        self._trigger_callbacks(context, result_id, result_data)

        context.logger(f"Result processed: {result_id} ({result_type})")
        return ManagerResult(True, {"result_id": result_id}, {})

    def query_results(self, context: ManagerContext, payload: Dict[str, Any]) -> ManagerResult:
        """Query results using helper."""
        query_params = payload.get("query", {})
        results = self._query_helper.query(self._results, query_params)
        return ManagerResult(True, {"results": results}, {})

    def validate_result(self, context: ManagerContext, payload: Dict[str, Any]) -> ManagerResult:
        """Validate a result."""
        result_data = payload.get("result_data", {})
        is_valid, errors = self._validator.validate(result_data)
        return ManagerResult(is_valid, {"valid": is_valid, "errors": errors}, {})

    def register_callback(self, context: ManagerContext, payload: Dict[str, Any]) -> ManagerResult:
        """Register a result callback."""
        callback_id = payload.get("callback_id", str(uuid.uuid4()))
        callback = payload.get("callback")

        if not callable(callback):
            return ManagerResult(False, {}, {}, "Callback must be callable")

        self._result_callbacks[callback_id] = callback
        context.logger(f"Callback registered: {callback_id}")
        return ManagerResult(True, {"callback_id": callback_id}, {})

    # Domain-Specific Operations -------------------------------------------------------

    def process_analysis_result(self, context: ManagerContext, payload: Dict[str, Any]) -> ManagerResult:
        """Process analysis-specific result."""
        result_id = str(uuid.uuid4())
        result_data = payload.get("result_data", {})

        self._analysis_results[result_id] = {
            "result_id": result_id,
            "analysis_type": payload.get("analysis_type", "general"),
            "metrics": result_data.get("metrics", {}),
            "insights": result_data.get("insights", []),
            "processed_at": datetime.utcnow().isoformat()
        }

        context.logger(f"Analysis result processed: {result_id}")
        return ManagerResult(True, {"result_id": result_id}, {})

    def process_validation_result(self, context: ManagerContext, payload: Dict[str, Any]) -> ManagerResult:
        """Process validation-specific result."""
        result_id = str(uuid.uuid4())
        result_data = payload.get("result_data", {})

        self._validation_results[result_id] = {
            "result_id": result_id,
            "validation_type": payload.get("validation_type", "general"),
            "passed": result_data.get("passed", False),
            "errors": result_data.get("errors", []),
            "warnings": result_data.get("warnings", []),
            "processed_at": datetime.utcnow().isoformat()
        }

        context.logger(f"Validation result processed: {result_id}")
        return ManagerResult(True, {"result_id": result_id}, {})

    def process_integration_result(self, context: ManagerContext, payload: Dict[str, Any]) -> ManagerResult:
        """Process integration-specific result."""
        result_id = str(uuid.uuid4())
        result_data = payload.get("result_data", {})

        self._integration_results[result_id] = {
            "result_id": result_id,
            "integration_type": payload.get("integration_type", "general"),
            "components": result_data.get("components", []),
            "status": result_data.get("status", "unknown"),
            "logs": result_data.get("logs", []),
            "processed_at": datetime.utcnow().isoformat()
        }

        context.logger(f"Integration result processed: {result_id}")
        return ManagerResult(True, {"result_id": result_id}, {})

    def process_performance_result(self, context: ManagerContext, payload: Dict[str, Any]) -> ManagerResult:
        """Process performance-specific result."""
        result_id = str(uuid.uuid4())
        result_data = payload.get("result_data", {})

        self._performance_results[result_id] = {
            "result_id": result_id,
            "performance_type": payload.get("performance_type", "general"),
            "metrics": result_data.get("metrics", {}),
            "benchmarks": result_data.get("benchmarks", {}),
            "bottlenecks": result_data.get("bottlenecks", []),
            "processed_at": datetime.utcnow().isoformat()
        }

        context.logger(f"Performance result processed: {result_id}")
        return ManagerResult(True, {"result_id": result_id}, {})

    def process_general_result(self, context: ManagerContext, payload: Dict[str, Any]) -> ManagerResult:
        """Process general result (fallback)."""
        result_id = str(uuid.uuid4())
        result_data = payload.get("result_data", {})

        result = {
            "result_id": result_id,
            "result_type": payload.get("result_type", "general"),
            "data": result_data,
            "processed_at": datetime.utcnow().isoformat()
        }

        self._results[result_id] = result
        context.logger(f"General result processed: {result_id}")
        return ManagerResult(True, {"result_id": result_id}, {})

    # Helper Methods -------------------------------------------------------------------

    def _trigger_callbacks(self, context: ManagerContext, result_id: str, result_data: Dict[str, Any]) -> None:
        """Trigger registered callbacks."""
        for callback_id, callback in self._result_callbacks.items():
            try:
                callback(context, result_id, result_data)
            except Exception as e:
                context.logger(f"Callback {callback_id} failed: {e}")
