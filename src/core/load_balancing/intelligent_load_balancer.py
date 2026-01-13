#!/usr/bin/env python3
"""
Intelligent Load Balancer - Optimal Multi-Agent Coordination
===========================================================

Advanced load balancing system that intelligently distributes tasks across agents
based on capacity, expertise, workload, and performance metrics.

FEATURES:
- Capacity-aware task distribution
- Expertise-based agent selection
- Workload balancing algorithms
- Performance prediction and optimization
- Dynamic scaling and adaptation
- Fairness and priority handling

Author: Agent-5 (Infrastructure Automation Specialist - Phase 2 Lead)
Date: 2026-01-13
Phase: Phase 2 - Scalability & Performance Optimization
"""

import asyncio
import logging
import random
import statistics
from collections import defaultdict, deque
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Any, Optional, Tuple, Set

from ..performance.performance_profiler import get_performance_profiler

logger = logging.getLogger(__name__)


class LoadBalancingStrategy(Enum):
    """Load balancing strategies."""
    ROUND_ROBIN = "round_robin"
    LEAST_LOADED = "least_loaded"
    WEIGHTED_RANDOM = "weighted_random"
    EXPERTISE_BASED = "expertise_based"
    PERFORMANCE_AWARE = "performance_aware"
    HYBRID_OPTIMAL = "hybrid_optimal"


@dataclass
class AgentCapacity:
    """Agent capacity and performance metrics."""
    agent_id: str
    max_concurrent_tasks: int = 5
    current_tasks: int = 0
    expertise_domains: Set[str] = field(default_factory=set)
    performance_score: float = 1.0  # 0.0 to 2.0, higher is better
    reliability_score: float = 1.0  # 0.0 to 1.0, higher is better
    specialization_bonus: float = 1.0  # Bonus for domain expertise
    last_assignment: Optional[float] = None
    total_assignments: int = 0
    successful_completions: int = 0

    @property
    def available_capacity(self) -> int:
        """Get available task slots."""
        return max(0, self.max_concurrent_tasks - self.current_tasks)

    @property
    def utilization_rate(self) -> float:
        """Get current utilization rate (0.0 to 1.0)."""
        return self.current_tasks / max(1, self.max_concurrent_tasks)

    @property
    def effective_score(self) -> float:
        """Get effective agent score combining all factors."""
        base_score = self.performance_score * self.reliability_score

        # Capacity factor (prefer less loaded agents)
        capacity_factor = 1.0 - (self.utilization_rate * 0.5)

        # Recency factor (prefer agents that haven't been assigned recently)
        recency_factor = 1.0
        if self.last_assignment:
            hours_since_assignment = (asyncio.get_event_loop().time() - self.last_assignment) / 3600
            recency_factor = min(1.0, hours_since_assignment / 2.0)  # Full bonus after 2 hours

        return base_score * capacity_factor * recency_factor * self.specialization_bonus


@dataclass
class TaskRequirements:
    """Task requirements and constraints."""
    task_id: str
    required_domains: Set[str] = field(default_factory=set)
    priority: int = 3  # 1-5, higher is more important
    estimated_complexity: float = 1.0  # 0.5 to 3.0
    max_completion_time: Optional[float] = None  # seconds
    dependencies: Set[str] = field(default_factory=set)  # Other task IDs
    preferred_agents: Set[str] = field(default_factory=set)
    excluded_agents: Set[str] = field(default_factory=set)


@dataclass
class LoadBalancingDecision:
    """Load balancing decision result."""
    task_id: str
    assigned_agent: str
    strategy_used: LoadBalancingStrategy
    confidence_score: float  # 0.0 to 1.0
    reasoning: str
    expected_completion_time: Optional[float] = None
    load_distribution_score: float = 0.0  # How well balanced the assignment is


class IntelligentLoadBalancer:
    """
    Intelligent load balancer for multi-agent coordination.

    Features:
    - Multiple balancing strategies
    - Real-time capacity monitoring
    - Expertise-based routing
    - Performance-aware decisions
    - Adaptive learning and optimization
    """

    def __init__(self, strategy: LoadBalancingStrategy = LoadBalancingStrategy.HYBRID_OPTIMAL):
        self.strategy = strategy
        self.agents: Dict[str, AgentCapacity] = {}
        self.task_history: deque = deque(maxlen=1000)  # Recent decisions for learning
        self.performance_profiler = get_performance_profiler()

        # Strategy-specific state
        self.round_robin_index = 0
        self.task_queue: asyncio.Queue = asyncio.Queue()

        # Learning and adaptation
        self.strategy_performance: Dict[LoadBalancingStrategy, List[float]] = defaultdict(list)
        self.agent_performance_history: Dict[str, deque] = defaultdict(lambda: deque(maxlen=50))

    def register_agent(self, agent_id: str, capacity: int = 5, expertise_domains: Optional[Set[str]] = None) -> bool:
        """Register an agent with the load balancer."""
        if agent_id in self.agents:
            logger.warning(f"Agent {agent_id} already registered")
            return False

        self.agents[agent_id] = AgentCapacity(
            agent_id=agent_id,
            max_concurrent_tasks=capacity,
            expertise_domains=expertise_domains or set()
        )

        logger.info(f"✅ Registered agent {agent_id} (capacity: {capacity}, domains: {expertise_domains})")
        return True

    def update_agent_capacity(self, agent_id: str, new_capacity: int) -> bool:
        """Update agent capacity dynamically."""
        if agent_id not in self.agents:
            return False

        self.agents[agent_id].max_concurrent_tasks = new_capacity
        logger.debug(f"📊 Updated agent {agent_id} capacity to {new_capacity}")
        return True

    def update_agent_performance(self, agent_id: str, performance_score: float, reliability_score: float) -> bool:
        """Update agent performance metrics."""
        if agent_id not in self.agents:
            return False

        agent = self.agents[agent_id]
        agent.performance_score = max(0.1, min(2.0, performance_score))
        agent.reliability_score = max(0.0, min(1.0, reliability_score))

        # Store in history for trend analysis
        self.agent_performance_history[agent_id].append({
            'timestamp': asyncio.get_event_loop().time(),
            'performance': performance_score,
            'reliability': reliability_score
        })

        return True

    async def assign_task(self, task: TaskRequirements) -> Optional[LoadBalancingDecision]:
        """
        Assign a task to the optimal agent using the configured strategy.

        Returns LoadBalancingDecision or None if no suitable agent found.
        """
        with self.performance_profiler.profile_operation("task_assignment", task_id=task.task_id):

            # Filter eligible agents
            eligible_agents = self._filter_eligible_agents(task)

            if not eligible_agents:
                logger.warning(f"❌ No eligible agents found for task {task.task_id}")
                return None

            # Select agent based on strategy
            selected_agent_id = await self._select_agent_by_strategy(task, eligible_agents)

            if not selected_agent_id:
                logger.warning(f"❌ No suitable agent selected for task {task.task_id}")
                return None

            # Update agent state
            await self._update_agent_assignment(selected_agent_id, task)

            # Calculate decision metrics
            confidence_score = self._calculate_assignment_confidence(task, selected_agent_id)
            expected_time = self._estimate_completion_time(task, selected_agent_id)
            load_balance_score = self._calculate_load_distribution_score()

            decision = LoadBalancingDecision(
                task_id=task.task_id,
                assigned_agent=selected_agent_id,
                strategy_used=self.strategy,
                confidence_score=confidence_score,
                reasoning=self._generate_assignment_reasoning(task, selected_agent_id),
                expected_completion_time=expected_time,
                load_distribution_score=load_balance_score
            )

            # Store decision for learning
            self.task_history.append(decision)

            logger.info(f"✅ Assigned task {task.task_id} to agent {selected_agent_id} "
                       f"(strategy: {self.strategy.value}, confidence: {confidence_score:.2f})")

            return decision

    def _filter_eligible_agents(self, task: TaskRequirements) -> List[str]:
        """Filter agents that meet task requirements."""
        eligible = []

        for agent_id, agent in self.agents.items():
            # Check capacity
            if agent.available_capacity <= 0:
                continue

            # Check exclusions
            if agent_id in task.excluded_agents:
                continue

            # Check preferences (preferred agents get priority)
            if task.preferred_agents and agent_id not in task.preferred_agents:
                continue

            # Check domain expertise (if required)
            if task.required_domains:
                agent_domains = agent.expertise_domains
                domain_match = len(task.required_domains.intersection(agent_domains))
                required_match = len(task.required_domains)

                # Require at least 50% domain match, or exact match for critical domains
                if domain_match < required_match * 0.5:
                    continue

            eligible.append(agent_id)

        return eligible

    async def _select_agent_by_strategy(self, task: TaskRequirements, eligible_agents: List[str]) -> Optional[str]:
        """Select agent using the configured load balancing strategy."""
        if not eligible_agents:
            return None

        if self.strategy == LoadBalancingStrategy.ROUND_ROBIN:
            return self._round_robin_selection(eligible_agents)

        elif self.strategy == LoadBalancingStrategy.LEAST_LOADED:
            return self._least_loaded_selection(eligible_agents)

        elif self.strategy == LoadBalancingStrategy.WEIGHTED_RANDOM:
            return self._weighted_random_selection(eligible_agents)

        elif self.strategy == LoadBalancingStrategy.EXPERTISE_BASED:
            return self._expertise_based_selection(task, eligible_agents)

        elif self.strategy == LoadBalancingStrategy.PERFORMANCE_AWARE:
            return self._performance_aware_selection(eligible_agents)

        elif self.strategy == LoadBalancingStrategy.HYBRID_OPTIMAL:
            return await self._hybrid_optimal_selection(task, eligible_agents)

        else:
            # Default to hybrid optimal
            return await self._hybrid_optimal_selection(task, eligible_agents)

    def _round_robin_selection(self, eligible_agents: List[str]) -> str:
        """Simple round-robin selection."""
        agent = eligible_agents[self.round_robin_index % len(eligible_agents)]
        self.round_robin_index += 1
        return agent

    def _least_loaded_selection(self, eligible_agents: List[str]) -> str:
        """Select least loaded agent."""
        return min(eligible_agents, key=lambda aid: self.agents[aid].utilization_rate)

    def _weighted_random_selection(self, eligible_agents: List[str]) -> str:
        """Weighted random selection based on effective scores."""
        weights = [self.agents[aid].effective_score for aid in eligible_agents]
        total_weight = sum(weights)

        if total_weight == 0:
            return random.choice(eligible_agents)

        # Normalize weights
        normalized_weights = [w / total_weight for w in weights]

        # Weighted selection
        r = random.random()
        cumulative = 0
        for i, weight in enumerate(normalized_weights):
            cumulative += weight
            if r <= cumulative:
                return eligible_agents[i]

        return eligible_agents[-1]  # Fallback

    def _expertise_based_selection(self, task: TaskRequirements, eligible_agents: List[str]) -> str:
        """Select agent with best domain expertise match."""
        best_agent = None
        best_score = 0

        for agent_id in eligible_agents:
            agent = self.agents[agent_id]
            domain_overlap = len(task.required_domains.intersection(agent.expertise_domains))

            # Calculate expertise score
            score = domain_overlap * agent.specialization_bonus

            if score > best_score:
                best_score = score
                best_agent = agent_id

        return best_agent or eligible_agents[0]

    def _performance_aware_selection(self, eligible_agents: List[str]) -> str:
        """Select agent with best performance metrics."""
        return max(eligible_agents, key=lambda aid: self.agents[aid].effective_score)

    async def _hybrid_optimal_selection(self, task: TaskRequirements, eligible_agents: List[str]) -> str:
        """Hybrid selection combining multiple factors."""
        # Calculate composite scores
        agent_scores = {}

        for agent_id in eligible_agents:
            agent = self.agents[agent_id]

            # Expertise score (40%)
            domain_overlap = len(task.required_domains.intersection(agent.expertise_domains))
            expertise_score = domain_overlap / max(1, len(task.required_domains))

            # Capacity score (30%) - prefer less loaded
            capacity_score = 1.0 - agent.utilization_rate

            # Performance score (20%)
            performance_score = agent.effective_score / 2.0  # Normalize to 0-1

            # Reliability score (10%)
            reliability_score = agent.reliability_score

            # Composite score
            total_score = (
                expertise_score * 0.4 +
                capacity_score * 0.3 +
                performance_score * 0.2 +
                reliability_score * 0.1
            )

            agent_scores[agent_id] = total_score

        # Select highest scoring agent
        return max(agent_scores.items(), key=lambda x: x[1])[0]

    async def _update_agent_assignment(self, agent_id: str, task: TaskRequirements):
        """Update agent state after assignment."""
        agent = self.agents[agent_id]
        agent.current_tasks += 1
        agent.last_assignment = asyncio.get_event_loop().time()
        agent.total_assignments += 1

        # Update specialization bonus based on domain match
        if task.required_domains and agent.expertise_domains:
            match_ratio = len(task.required_domains.intersection(agent.expertise_domains)) / len(task.required_domains)
            agent.specialization_bonus = 1.0 + (match_ratio * 0.5)  # Up to 50% bonus

    def _calculate_assignment_confidence(self, task: TaskRequirements, agent_id: str) -> float:
        """Calculate confidence score for the assignment."""
        agent = self.agents[agent_id]

        # Domain expertise confidence
        domain_confidence = 1.0
        if task.required_domains:
            overlap = len(task.required_domains.intersection(agent.expertise_domains))
            domain_confidence = overlap / len(task.required_domains)

        # Capacity confidence (lower utilization = higher confidence)
        capacity_confidence = 1.0 - (agent.utilization_rate * 0.5)

        # Performance confidence
        performance_confidence = min(1.0, agent.effective_score)

        # Composite confidence
        confidence = (
            domain_confidence * 0.5 +
            capacity_confidence * 0.3 +
            performance_confidence * 0.2
        )

        return min(1.0, max(0.0, confidence))

    def _estimate_completion_time(self, task: TaskRequirements, agent_id: str) -> Optional[float]:
        """Estimate task completion time."""
        agent = self.agents[agent_id]

        # Base time calculation
        base_time = task.estimated_complexity * 3600  # Complexity hours in seconds

        # Agent performance factor (better agents complete faster)
        performance_factor = 2.0 - agent.performance_score  # Invert (higher score = faster)

        # Capacity factor (more loaded = slower)
        capacity_factor = 1.0 + (agent.utilization_rate * 0.5)

        estimated_time = base_time * performance_factor * capacity_factor

        # Apply maximum time constraint if specified
        if task.max_completion_time:
            estimated_time = min(estimated_time, task.max_completion_time)

        return estimated_time

    def _calculate_load_distribution_score(self) -> float:
        """Calculate how well balanced the current load distribution is."""
        if not self.agents:
            return 0.0

        utilizations = [agent.utilization_rate for agent in self.agents.values()]

        # Calculate standard deviation (lower = more balanced)
        if len(utilizations) > 1:
            std_dev = statistics.stdev(utilizations)
            # Convert to score (0 = perfectly balanced, 1 = highly unbalanced)
            balance_score = min(1.0, std_dev * 2.0)
        else:
            balance_score = 0.0

        # Return balance score (higher = more balanced)
        return 1.0 - balance_score

    def _generate_assignment_reasoning(self, task: TaskRequirements, agent_id: str) -> str:
        """Generate human-readable reasoning for the assignment."""
        agent = self.agents[agent_id]
        reasons = []

        # Domain expertise
        if task.required_domains:
            overlap = task.required_domains.intersection(agent.expertise_domains)
            if overlap:
                reasons.append(f"expertise in {', '.join(overlap)}")

        # Capacity
        if agent.available_capacity > 2:
            reasons.append("good capacity availability")

        # Performance
        if agent.performance_score > 1.2:
            reasons.append("strong performance history")

        if not reasons:
            reasons.append("general availability")

        return f"Selected {agent_id} due to {', '.join(reasons)}"

    def complete_task(self, agent_id: str, task_id: str, success: bool = True):
        """Mark a task as completed and update agent metrics."""
        if agent_id not in self.agents:
            return

        agent = self.agents[agent_id]
        agent.current_tasks = max(0, agent.current_tasks - 1)

        if success:
            agent.successful_completions += 1

        # Update reliability score based on recent performance
        total_attempts = agent.total_assignments
        success_rate = agent.successful_completions / max(1, total_attempts)
        agent.reliability_score = success_rate

    def get_load_balancing_stats(self) -> Dict[str, Any]:
        """Get comprehensive load balancing statistics."""
        total_agents = len(self.agents)
        total_capacity = sum(agent.max_concurrent_tasks for agent in self.agents.values())
        used_capacity = sum(agent.current_tasks for agent in self.agents.values())

        agent_stats = []
        for agent_id, agent in self.agents.items():
            agent_stats.append({
                'agent_id': agent_id,
                'utilization': agent.utilization_rate,
                'available_capacity': agent.available_capacity,
                'performance_score': agent.performance_score,
                'reliability_score': agent.reliability_score,
                'total_assignments': agent.total_assignments,
                'success_rate': agent.successful_completions / max(1, agent.total_assignments)
            })

        return {
            'total_agents': total_agents,
            'total_capacity': total_capacity,
            'used_capacity': used_capacity,
            'overall_utilization': used_capacity / max(1, total_capacity),
            'strategy': self.strategy.value,
            'recent_decisions': len(self.task_history),
            'agent_stats': agent_stats
        }

    def optimize_strategy(self) -> LoadBalancingStrategy:
        """Analyze performance and suggest optimal strategy."""
        # Simple strategy optimization based on current metrics
        stats = self.get_load_balancing_stats()

        # If high utilization, prefer least loaded
        if stats['overall_utilization'] > 0.8:
            return LoadBalancingStrategy.LEAST_LOADED

        # If many agents with different expertise, use expertise-based
        agent_domains = [len(agent.expertise_domains) for agent in self.agents.values()]
        if statistics.mean(agent_domains) > 2:
            return LoadBalancingStrategy.EXPERTISE_BASED

        # Default to hybrid optimal
        return LoadBalancingStrategy.HYBRID_OPTIMAL


# Global load balancer instance
_load_balancer = None

def get_load_balancer(strategy: LoadBalancingStrategy = LoadBalancingStrategy.HYBRID_OPTIMAL) -> IntelligentLoadBalancer:
    """Get the global load balancer instance."""
    global _load_balancer
    if _load_balancer is None:
        _load_balancer = IntelligentLoadBalancer(strategy)
    return _load_balancer

def register_agents_with_balancer(agent_configs: List[Dict[str, Any]]):
    """Register multiple agents with the load balancer."""
    balancer = get_load_balancer()

    for config in agent_configs:
        balancer.register_agent(
            agent_id=config['id'],
            capacity=config.get('capacity', 5),
            expertise_domains=set(config.get('expertise', []))
        )