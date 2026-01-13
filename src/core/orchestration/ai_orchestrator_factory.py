"""
AI Orchestrator Factory - Intelligent Orchestrator Selection
==========================================================

<!-- SSOT Domain: ai_integration -->

Factory for creating AI-enhanced orchestrators with intelligent selection
based on coordination context and requirements.

FEATURES:
- Automatic orchestrator selection based on task complexity
- AI capability detection and fallback handling
- Performance monitoring and optimization
- Configuration-driven orchestrator selection

Author: Agent-5 (Infrastructure Automation Specialist)
Date: 2026-01-13
"""

import logging
from typing import Dict, Any, Optional, Type
from enum import Enum

from .core_orchestrator import CoreOrchestrator
from .ai_enhanced_orchestrator import AIEnhancedOrchestrator
from .registry import StepRegistry
from .contracts import Orchestrator

logger = logging.getLogger(__name__)


class OrchestratorType(Enum):
    """Available orchestrator types."""
    STANDARD = "standard"      # Basic CoreOrchestrator
    AI_ENHANCED = "ai_enhanced"  # AI-powered coordination


class AIOrchestratorFactory:
    """
    Factory for creating intelligent orchestrators based on context.

    Automatically selects the most appropriate orchestrator type based on:
    - Task complexity and count
    - Agent availability and capabilities
    - AI system availability
    - Performance requirements
    """

    def __init__(self):
        self.ai_available = self._check_ai_availability()
        self.performance_metrics = {}

    def _check_ai_availability(self) -> bool:
        """Check if AI components are available."""
        try:
            from src.ai_training.dreamvault.advanced_reasoning import AdvancedReasoningEngine
            from src.services.ai_context_engine.ai_context_engine import AIContextEngine
            return True
        except ImportError:
            logger.info("AI components not available - using standard orchestration")
            return False

    def select_orchestrator_type(self, context: Dict[str, Any]) -> OrchestratorType:
        """
        Intelligently select the best orchestrator type for the given context.

        Args:
            context: Coordination context including tasks, agents, requirements

        Returns:
            Recommended orchestrator type
        """
        if not self.ai_available:
            return OrchestratorType.STANDARD

        # Analyze context for AI enhancement suitability
        tasks = context.get('tasks', [])
        agents = context.get('agents', [])
        requirements = context.get('requirements', {})

        # Criteria for AI enhancement
        task_complexity = self._assess_task_complexity(tasks)
        agent_diversity = len(set(a.get('specialties', []) for a in agents if a.get('specialties')))
        time_pressure = self._assess_time_pressure(tasks)
        coordination_complexity = len(tasks) * len(agents)

        # Decision logic
        ai_score = (
            task_complexity * 0.3 +
            (agent_diversity / max(1, len(agents))) * 0.2 +
            time_pressure * 0.2 +
            min(1.0, coordination_complexity / 20.0) * 0.3
        )

        # AI enhancement threshold
        if ai_score > 0.6:
            logger.info(".2f"            return OrchestratorType.AI_ENHANCED
        else:
            logger.info(".2f"            return OrchestratorType.STANDARD

    def _assess_task_complexity(self, tasks: list) -> float:
        """Assess average task complexity (0.0 to 1.0)."""
        if not tasks:
            return 0.0

        complexities = []
        for task in tasks:
            complexity = 0.0

            # Priority-based complexity
            priority = task.get('priority', 3)
            complexity += min(1.0, priority / 5.0) * 0.4

            # Dependency-based complexity
            dependencies = task.get('dependencies', [])
            complexity += min(1.0, len(dependencies) / 3.0) * 0.3

            # Skill requirements
            required_skills = task.get('required_skills', [])
            complexity += min(1.0, len(required_skills) / 5.0) * 0.3

            complexities.append(min(1.0, complexity))

        return sum(complexities) / len(complexities) if complexities else 0.0

    def _assess_time_pressure(self, tasks: list) -> float:
        """Assess time pressure across tasks (0.0 to 1.0)."""
        if not tasks:
            return 0.0

        pressure_indicators = 0
        total_tasks = len(tasks)

        for task in tasks:
            # Deadline pressure
            if task.get('deadline') and task.get('priority', 1) >= 3:
                pressure_indicators += 1

            # High priority tasks
            if task.get('priority', 1) >= 4:
                pressure_indicators += 0.5

            # Blocked or dependent tasks
            if task.get('blocked') or task.get('dependencies'):
                pressure_indicators += 0.3

        return min(1.0, pressure_indicators / total_tasks)

    def create_orchestrator(
        self,
        registry: StepRegistry,
        pipeline: list,
        context: Optional[Dict[str, Any]] = None
    ) -> Orchestrator:
        """
        Create the most appropriate orchestrator for the given context.

        Args:
            registry: Step registry
            pipeline: Pipeline steps
            context: Coordination context (optional)

        Returns:
            Configured orchestrator instance
        """
        context = context or {}
        orchestrator_type = self.select_orchestrator_type(context)

        if orchestrator_type == OrchestratorType.AI_ENHANCED:
            try:
                return AIEnhancedOrchestrator(registry, pipeline)
            except Exception as e:
                logger.warning(f"Failed to create AI orchestrator: {e}")
                logger.info("Falling back to standard orchestrator")
                return CoreOrchestrator(registry, pipeline)
        else:
            return CoreOrchestrator(registry, pipeline)

    def get_orchestrator_info(self, orchestrator: Orchestrator) -> Dict[str, Any]:
        """Get information about the given orchestrator."""
        info = {
            'type': orchestrator.__class__.__name__,
            'ai_enhanced': isinstance(orchestrator, AIEnhancedOrchestrator),
            'ai_available': self.ai_available
        }

        if isinstance(orchestrator, AIEnhancedOrchestrator):
            info.update({
                'reasoning_engine_available': orchestrator.reasoning_engine is not None,
                'context_engine_available': orchestrator.context_engine is not None,
                'decision_history_count': len(orchestrator.decision_history),
                'metrics_tracked': len(orchestrator.metrics.coordination_patterns)
            })

        return info


# Global factory instance
_orchestrator_factory = None

def get_orchestrator_factory() -> AIOrchestratorFactory:
    """Get the global orchestrator factory instance."""
    global _orchestrator_factory
    if _orchestrator_factory is None:
        _orchestrator_factory = AIOrchestratorFactory()
    return _orchestrator_factory

def create_smart_orchestrator(
    registry: StepRegistry,
    pipeline: list,
    context: Optional[Dict[str, Any]] = None
) -> Orchestrator:
    """
    Create a smart orchestrator that automatically selects the best type.

    Args:
        registry: Step registry
        pipeline: Pipeline steps
        context: Coordination context

    Returns:
        Best orchestrator for the context
    """
    factory = get_orchestrator_factory()
    return factory.create_orchestrator(registry, pipeline, context)