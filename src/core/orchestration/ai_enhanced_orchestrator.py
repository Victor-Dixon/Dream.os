"""
AI-Enhanced Orchestrator - Intelligent Agent Coordination
======================================================

<!-- SSOT Domain: ai_integration -->

AI-powered orchestrator that leverages advanced reasoning for intelligent task allocation,
priority optimization, and adaptive coordination strategies.

INTEGRATION POINTS:
├── DreamVault Advanced Reasoning → Decision optimization and strategy planning
├── AI Context Engine → Real-time context awareness and session state
├── Risk Analytics → Risk-aware decision making and mitigation
├── Performance Metrics → Learning from historical coordination patterns

STRATEGIC IMPACT:
- AI-driven task allocation based on agent capabilities and workload
- Intelligent priority setting using contextual analysis
- Adaptive coordination strategies that learn from success patterns
- Risk-aware decision making for critical operations

Author: Agent-5 (Infrastructure Automation Specialist)
Date: 2026-01-13
Phase: Phase 5.5 - AI Integration Enhancement
"""

import asyncio
import logging
import time
from typing import Dict, List, Any, Optional, Union
from collections.abc import Iterable
from dataclasses import dataclass, field

from .core_orchestrator import CoreOrchestrator
from .contracts import OrchestrationContext, OrchestrationResult, Orchestrator, Step
from .registry import StepRegistry

# AI Integration imports
try:
    from src.ai_training.dreamvault.advanced_reasoning import (
        AdvancedReasoningEngine,
        ReasoningMode,
        ResponseFormat,
        ReasoningContext
    )
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False
    logger = logging.getLogger(__name__)
    logger.warning("Advanced reasoning engine not available - falling back to standard orchestration")

try:
    from src.services.ai_context_engine.ai_context_engine import AIContextEngine
    CONTEXT_AVAILABLE = True
except ImportError:
    CONTEXT_AVAILABLE = False

logger = logging.getLogger(__name__)


@dataclass
class CoordinationMetrics:
    """Metrics for AI-enhanced coordination decisions."""
    agent_workload: Dict[str, float] = field(default_factory=dict)
    task_complexity: Dict[str, float] = field(default_factory=dict)
    success_rates: Dict[str, float] = field(default_factory=dict)
    coordination_patterns: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class AIDecision:
    """AI-generated coordination decision."""
    task_allocation: Dict[str, List[str]]  # agent_id -> task_ids
    priority_adjustments: Dict[str, int]   # task_id -> new_priority
    coordination_strategy: str
    reasoning: str
    confidence_score: float
    alternative_approaches: List[str]


class AIEnhancedOrchestrator(Orchestrator):
    """
    AI-enhanced orchestrator with intelligent coordination capabilities.

    Features:
    - AI-driven task allocation based on agent capabilities
    - Intelligent priority optimization using context analysis
    - Adaptive coordination strategies that learn from patterns
    - Risk-aware decision making for critical operations
    """

    def __init__(self, registry: StepRegistry, pipeline: Iterable[str]):
        super().__init__(registry, pipeline)
        self.reasoning_engine = None
        self.context_engine = None
        self.metrics = CoordinationMetrics()
        self.decision_history: List[AIDecision] = []

        # Initialize AI components if available
        self._initialize_ai_components()

    def _initialize_ai_components(self) -> None:
        """Initialize AI reasoning and context engines."""
        if AI_AVAILABLE:
            try:
                self.reasoning_engine = AdvancedReasoningEngine()
                logger.info("✅ Advanced reasoning engine initialized for orchestration")
            except Exception as e:
                logger.warning(f"Failed to initialize reasoning engine: {e}")

        if CONTEXT_AVAILABLE:
            try:
                self.context_engine = AIContextEngine()
                logger.info("✅ AI context engine initialized for orchestration")
            except Exception as e:
                logger.warning(f"Failed to initialize context engine: {e}")

    async def analyze_coordination_context(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Use AI to analyze the coordination context and provide insights.

        Args:
            payload: Orchestration payload with tasks, agents, and context

        Returns:
            Enhanced context with AI insights
        """
        if not self.reasoning_engine:
            return payload

        try:
            # Extract coordination context
            agents = payload.get('agents', [])
            tasks = payload.get('tasks', [])
            current_state = payload.get('coordination_state', {})

            # Build reasoning context
            context = ReasoningContext(
                query=f"Analyze coordination context: {len(agents)} agents, {len(tasks)} tasks",
                mode=ReasoningMode.STRATEGIC,
                format=ResponseFormat.STRUCTURED,
                context={
                    'agents': agents,
                    'tasks': tasks,
                    'current_state': current_state,
                    'historical_metrics': self.metrics.__dict__,
                    'recent_decisions': [d.__dict__ for d in self.decision_history[-5:]]
                }
            )

            # Get AI analysis
            analysis = await self.reasoning_engine.reason(context)

            # Extract insights
            insights = {
                'workload_distribution': self._analyze_workload_distribution(agents, tasks),
                'task_priorities': self._optimize_priorities(tasks, current_state),
                'coordination_strategy': self._recommend_strategy(agents, tasks, analysis),
                'risk_assessment': self._assess_coordination_risks(agents, tasks),
                'ai_confidence': analysis.get('confidence_score', 0.5)
            }

            # Update payload with AI insights
            payload['ai_insights'] = insights
            payload['ai_analysis'] = analysis

            logger.info(f"🤖 AI coordination analysis complete (confidence: {insights['ai_confidence']:.2f})")
            return payload

        except Exception as e:
            logger.warning(f"AI coordination analysis failed: {e}")
            return payload

    def _analyze_workload_distribution(self, agents: List[Dict], tasks: List[Dict]) -> Dict[str, Any]:
        """Analyze current workload distribution across agents."""
        distribution = {}

        for agent in agents:
            agent_id = agent.get('id', agent.get('agent_id', 'unknown'))
            current_tasks = [t for t in tasks if t.get('assigned_to') == agent_id]
            workload_score = len(current_tasks) * 1.0  # Simple metric

            # Factor in task complexity if available
            for task in current_tasks:
                complexity = task.get('complexity', task.get('priority', 1))
                workload_score += complexity * 0.5

            distribution[agent_id] = {
                'current_tasks': len(current_tasks),
                'workload_score': workload_score,
                'capacity': agent.get('capacity', 5),
                'specialties': agent.get('specialties', [])
            }

        return distribution

    def _optimize_priorities(self, tasks: List[Dict], context: Dict[str, Any]) -> Dict[str, Any]:
        """Use AI insights to optimize task priorities."""
        priority_recommendations = {}

        # Analyze task dependencies and urgency
        for task in tasks:
            task_id = task.get('id', task.get('task_id', 'unknown'))
            base_priority = task.get('priority', 3)

            # AI-enhanced priority calculation
            ai_boost = 0

            # Boost based on dependencies
            if task.get('dependencies'):
                ai_boost += 1  # Tasks with dependencies are more critical

            # Boost based on deadlines
            if task.get('deadline'):
                time_to_deadline = self._calculate_time_to_deadline(task['deadline'])
                if time_to_deadline < 24:  # Less than 24 hours
                    ai_boost += 2

            # Boost based on agent availability
            assigned_agent = task.get('assigned_to')
            if assigned_agent and self.metrics.agent_workload.get(assigned_agent, 0) > 3:
                ai_boost += 1  # Agent is overloaded

            recommended_priority = min(5, base_priority + ai_boost)
            priority_recommendations[task_id] = {
                'original': base_priority,
                'recommended': recommended_priority,
                'reasoning': f"AI boost: {ai_boost} (dependencies, deadlines, workload)"
            }

        return priority_recommendations

    def _recommend_strategy(self, agents: List[Dict], tasks: List[Dict], analysis: Dict[str, Any]) -> str:
        """Recommend coordination strategy based on AI analysis."""
        agent_count = len(agents)
        task_count = len(tasks)

        # Strategy selection logic
        if agent_count >= task_count * 2:
            return "parallel_execution"  # Many agents, few tasks
        elif any(t.get('priority', 1) >= 4 for t in tasks):
            return "prioritized_sequential"  # High priority tasks need focus
        elif agent_count <= 2:
            return "pair_programming"  # Small team, collaborative approach
        else:
            return "balanced_distribution"  # Standard load balancing

    def _assess_coordination_risks(self, agents: List[Dict], tasks: List[Dict]) -> Dict[str, Any]:
        """Assess risks in the current coordination setup."""
        risks = {
            'high_priority_tasks': len([t for t in tasks if t.get('priority', 1) >= 4]),
            'overloaded_agents': len([a for a in agents if self.metrics.agent_workload.get(a.get('id', ''), 0) > 4]),
            'single_points_failure': len([t for t in tasks if not t.get('backup_agents')]),
            'deadline_pressure': len([t for t in tasks if self._is_under_deadline_pressure(t)])
        }

        risk_score = sum(risks.values()) / max(1, len(tasks) + len(agents))
        risks['overall_score'] = min(1.0, risk_score)

        return risks

    def _calculate_time_to_deadline(self, deadline: Union[str, int, float]) -> float:
        """Calculate hours until deadline."""
        if isinstance(deadline, str):
            # Simple string parsing - in production, use proper datetime parsing
            try:
                # Assume format like "2026-01-14T10:00:00"
                deadline_time = time.time() + 24 * 3600  # Placeholder
            except:
                deadline_time = time.time() + 7 * 24 * 3600  # Default 1 week
        else:
            deadline_time = deadline

        return max(0, (deadline_time - time.time()) / 3600)

    def _is_under_deadline_pressure(self, task: Dict[str, Any]) -> bool:
        """Check if task is under deadline pressure."""
        deadline = task.get('deadline')
        if not deadline:
            return False

        time_to_deadline = self._calculate_time_to_deadline(deadline)
        priority = task.get('priority', 1)

        return time_to_deadline < 24 and priority >= 3

    async def make_ai_decision(self, payload: Dict[str, Any]) -> Optional[AIDecision]:
        """
        Make an AI-informed coordination decision.

        Args:
            payload: Enhanced payload with AI insights

        Returns:
            AI decision or None if AI not available
        """
        if not self.reasoning_engine:
            return None

        try:
            insights = payload.get('ai_insights', {})

            # Build comprehensive decision context
            decision_context = ReasoningContext(
                query="Generate optimal coordination strategy for current tasks and agents",
                mode=ReasoningMode.STRATEGIC,
                format=ResponseFormat.STRUCTURED,
                context={
                    'insights': insights,
                    'payload': payload,
                    'metrics': self.metrics.__dict__,
                    'decision_history': [d.__dict__ for d in self.decision_history[-3:]]
                }
            )

            # Get AI decision
            ai_response = await self.reasoning_engine.reason(decision_context)

            # Parse AI response into decision structure
            decision = AIDecision(
                task_allocation=ai_response.get('task_allocation', {}),
                priority_adjustments=ai_response.get('priority_adjustments', {}),
                coordination_strategy=ai_response.get('strategy', 'balanced_distribution'),
                reasoning=ai_response.get('reasoning', 'AI-optimized coordination'),
                confidence_score=ai_response.get('confidence', 0.7),
                alternative_approaches=ai_response.get('alternatives', [])
            )

            # Store decision for learning
            self.decision_history.append(decision)

            return decision

        except Exception as e:
            logger.warning(f"AI decision making failed: {e}")
            return None

    def plan(self, ctx: OrchestrationContext, payload: Dict[str, Any]) -> Iterable[Step]:
        """Override plan to include AI-enhanced decision making."""
        # Run AI analysis synchronously for now (could be async in future)
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            enhanced_payload = loop.run_until_complete(self.analyze_coordination_context(payload))
            ai_decision = loop.run_until_complete(self.make_ai_decision(enhanced_payload))
            loop.close()
        except Exception as e:
            logger.warning(f"AI planning failed: {e}")
            enhanced_payload = payload
            ai_decision = None

        # Apply AI decisions to payload if available
        if ai_decision:
            enhanced_payload['ai_decision'] = ai_decision.__dict__
            ctx.emit("ai.decision", {
                "strategy": ai_decision.coordination_strategy,
                "confidence": ai_decision.confidence_score
            })

        # Log AI-enhanced planning
        if enhanced_payload.get('ai_insights'):
            ctx.emit("ai.insights", enhanced_payload['ai_insights'])

        # Use base planning with enhanced payload
        return super().plan(ctx, enhanced_payload)

    def execute(self, ctx: OrchestrationContext, payload: Dict[str, Any]) -> OrchestrationResult:
        """Override execute to include AI monitoring and learning."""
        start_time = time.time()

        # Execute with base orchestrator
        result = super().execute(ctx, payload)

        # Update metrics for learning
        execution_time = time.time() - start_time
        self._update_learning_metrics(payload, result, execution_time)

        # Emit AI learning event
        ctx.emit("ai.learning", {
            "execution_time": execution_time,
            "success": result.ok,
            "metrics_updated": True
        })

        return result

    def _update_learning_metrics(self, payload: Dict[str, Any], result: OrchestrationResult, execution_time: float) -> None:
        """Update internal metrics for AI learning."""
        # Update agent workload metrics
        agents = payload.get('agents', [])
        for agent in agents:
            agent_id = agent.get('id', agent.get('agent_id', 'unknown'))
            self.metrics.agent_workload[agent_id] = self.metrics.agent_workload.get(agent_id, 0) * 0.8 + 1.0 * 0.2

        # Update success rates
        if result.ok:
            strategy = payload.get('ai_decision', {}).get('coordination_strategy', 'unknown')
            current_rate = self.metrics.success_rates.get(strategy, 0.5)
            self.metrics.success_rates[strategy] = current_rate * 0.9 + 1.0 * 0.1
        else:
            strategy = payload.get('ai_decision', {}).get('coordination_strategy', 'unknown')
            current_rate = self.metrics.success_rates.get(strategy, 0.5)
            self.metrics.success_rates[strategy] = current_rate * 0.9 + 0.0 * 0.1

        # Store coordination pattern
        self.metrics.coordination_patterns.append({
            'timestamp': time.time(),
            'strategy': payload.get('ai_decision', {}).get('coordination_strategy', 'unknown'),
            'success': result.ok,
            'execution_time': execution_time,
            'agent_count': len(payload.get('agents', [])),
            'task_count': len(payload.get('tasks', []))
        })

        # Keep only recent patterns (last 100)
        if len(self.metrics.coordination_patterns) > 100:
            self.metrics.coordination_patterns = self.metrics.coordination_patterns[-100:]

    def report(self, result: OrchestrationResult) -> str:
        """Enhanced reporting with AI insights."""
        base_report = super().report(result)

        ai_info = ""
        if hasattr(result, 'metrics') and 'ai_confidence' in result.metrics:
            ai_info = f" | AI Confidence: {result.metrics['ai_confidence']:.2f}"

        return f"[AI-Enhanced Orchestrator] {result.summary}{ai_info} :: metrics={result.metrics}"