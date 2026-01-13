"""
<!-- SSOT Domain: core -->

Intelligent Context Core - V2 Compliance Module
==============================================

Core intelligent context functionality.

V2 Compliance: < 300 lines, single responsibility, context core.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

from datetime import datetime
from typing import Any

from ..analysis_models import RiskAssessment, SuccessPrediction
from ..core_models import AgentCapability, MissionContext
from ..emergency_models import EmergencyContext, InterventionProtocol
from ..engines.agent_assignment_engine import AgentAssignmentEngine
from ..engines.risk_assessment_engine import RiskAssessmentEngine
from ..intelligent_context_emergency import IntelligentContextEmergency
from ..intelligent_context_engine import IntelligentContextEngine
from ..metrics_models import ContextMetrics
from ..search_models import ContextRetrievalResult
# Use SSOT SearchResult - supports all intelligent context fields
from src.services.models.vector_models import SearchResult


class ContextCore:
    """Core intelligent context functionality."""

    def __init__(self):
        """Initialize context core."""
        self.contexts = {}
        self.capabilities = {}
        self.protocols = []
        # Initialize engine for real implementations
        self.engine = IntelligentContextEngine()
        self.emergency_handler = IntelligentContextEmergency(self.engine)
        self.assignment_engine = AgentAssignmentEngine(self.engine)
        self.risk_engine = RiskAssessmentEngine(self.engine)

    def update_mission_context(self, context: MissionContext) -> bool:
        """Update mission context."""
        try:
            self.contexts[context.mission_id] = context
            return True
        except Exception:
            return False

    def get_mission_context(self, mission_id: str) -> MissionContext | None:
        """Get mission context."""
        return self.contexts.get(mission_id)

    def get_agent_capabilities(self, agent_id: str) -> list[AgentCapability]:
        """Get agent capabilities."""
        return self.capabilities.get(agent_id, [])

    def search_context(self, query: str) -> ContextRetrievalResult:
        """Search context."""
        try:
            # Simple search implementation
            results = []
            for context in self.contexts.values():
                if query.lower() in context.mission_type.lower():
                    results.append(
                        SearchResult(
                            result_id=f"search_{len(results)}",
                            content=context.mission_type,
                            relevance_score=0.8,
                            source_type="mission",
                            source_id=context.mission_id,
                        )
                    )

            return ContextRetrievalResult(
                success=True,
                search_results=results,
                execution_time_ms=0.1,
            )
        except Exception as e:
            return ContextRetrievalResult(
                success=False,
                search_results=[],
                execution_time_ms=0.0,
                error_message=str(e),
            )

    def get_emergency_context(self, emergency_id: str) -> EmergencyContext | None:
        """Get emergency context."""
        try:
            # Try to find mission by emergency_id (may be mission_id)
            mission = self.get_mission_context(emergency_id)
            if not mission:
                # Try to find in engine's active missions
                mission = self.engine.get_mission_context(emergency_id)
            
            if mission:
                # Use emergency handler to get emergency context
                return self.emergency_handler.get_emergency_context(mission)
            
            # If no mission found, create minimal emergency context
            return EmergencyContext(
                emergency_id=emergency_id,
                mission_id=emergency_id,
                emergency_type="unknown",
                severity_level="medium",
            )
        except Exception:
            return None

    def get_intervention_protocols(self) -> list[InterventionProtocol]:
        """Get intervention protocols."""
        return self.protocols

    def optimize_agent_assignment(self, mission_id: str) -> list[str]:
        """Optimize agent assignment."""
        try:
            # Get mission context
            mission = self.get_mission_context(mission_id)
            if not mission:
                mission = self.engine.get_mission_context(mission_id)
            
            if not mission:
                # Create minimal mission context for optimization
                mission = MissionContext(
                    mission_id=mission_id,
                    mission_type="unknown",
                    current_phase="planning",
                )
            
            # Use assignment engine to optimize
            result = self.assignment_engine.optimize_agent_assignment(mission)
            
            if result.success and result.data.get("recommendations"):
                # Extract agent IDs from recommendations
                recommendations = result.data["recommendations"]
                return [rec.agent_id for rec in recommendations]
            
            return []
        except Exception:
            return []

    def analyze_success_patterns(self) -> dict[str, Any]:
        """Analyze success patterns."""
        try:
            # Import SwarmCoordinationAnalyzer for pattern analysis
            from ...vector_strategic_oversight.unified_strategic_oversight.analyzers.swarm_analyzer import (
                SwarmCoordinationAnalyzer,
            )
            
            analyzer = SwarmCoordinationAnalyzer()
            
            # Convert contexts to agent data format
            agent_data = []
            for agent_id, capability in self.capabilities.items():
                agent_data.append({
                    "agent_id": agent_id,
                    "capability": capability.to_dict() if hasattr(capability, 'to_dict') else {},
                })
            
            # Convert missions to mission data format
            mission_data = []
            for mission_id, mission in self.contexts.items():
                mission_data.append(mission.to_dict() if hasattr(mission, 'to_dict') else {
                    "mission_id": mission_id,
                    "mission_type": getattr(mission, 'mission_type', 'unknown'),
                })
            
            # Analyze patterns (async method, but we'll call it synchronously)
            import asyncio
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            
            insights = loop.run_until_complete(
                analyzer.analyze_swarm_coordination(agent_data, mission_data)
            )
            
            # Convert insights to dict format
            return {
                "total_insights": len(insights),
                "insights": [
                    {
                        "insight_id": insight.insight_id,
                        "type": insight.insight_type.value if hasattr(insight.insight_type, 'value') else str(insight.insight_type),
                        "description": insight.description,
                        "confidence": insight.confidence_level.value if hasattr(insight.confidence_level, 'value') else str(insight.confidence_level),
                        "key_findings": insight.key_findings,
                    }
                    for insight in insights
                ],
                "patterns_identified": len([i for i in insights if "pattern" in i.description.lower()]),
            }
        except Exception as e:
            # Fallback to basic pattern analysis
            return {
                "total_insights": 0,
                "insights": [],
                "patterns_identified": 0,
                "error": str(e),
            }

    def assess_mission_risks(self, mission_id: str) -> RiskAssessment | None:
        """Assess mission risks."""
        try:
            # Get mission context
            mission = self.get_mission_context(mission_id)
            if not mission:
                mission = self.engine.get_mission_context(mission_id)
            
            if not mission:
                # Create minimal mission context for risk assessment
                mission = MissionContext(
                    mission_id=mission_id,
                    mission_type="unknown",
                    current_phase="planning",
                )
            
            # Use risk assessment engine
            return self.risk_engine.assess_mission_risks(mission)
        except Exception:
            return None

    def generate_success_predictions(self, task_id: str) -> SuccessPrediction | None:
        """Generate success predictions."""
        try:
            # Import PredictionAnalyzer
            from ...vector_strategic_oversight.unified_strategic_oversight.analyzers.prediction_analyzer import (
                PredictionAnalyzer,
            )
            
            analyzer = PredictionAnalyzer()
            
            # Get task data from mission context (task_id may be mission_id)
            mission = self.get_mission_context(task_id)
            if not mission:
                mission = self.engine.get_mission_context(task_id)
            
            # Convert mission to task data format
            task_data = {
                "task_id": task_id,
                "title": getattr(mission, 'mission_type', 'unknown') if mission else 'unknown',
                "description": f"Mission: {getattr(mission, 'mission_type', 'unknown')}" if mission else "Unknown task",
                "complexity": "high" if mission and len(getattr(mission, 'risk_factors', [])) > 3 else "medium",
                "priority": "high" if mission and len(getattr(mission, 'risk_factors', [])) > 5 else "normal",
            }
            
            # Generate prediction (async method, but we'll call it synchronously)
            import asyncio
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            
            prediction = loop.run_until_complete(
                analyzer.predict_task_success(task_data)
            )
            
            # Convert to SuccessPrediction format
            return SuccessPrediction(
                prediction_id=prediction.prediction_id,
                success_probability=prediction.success_probability,
                confidence_level=prediction.confidence_level.value if hasattr(prediction.confidence_level, 'value') else 0.5,
                key_factors=prediction.key_factors,
                potential_bottlenecks=prediction.risk_factors,
                recommended_actions=prediction.recommendations,
            )
        except Exception:
            return None

    def get_context_metrics(self) -> ContextMetrics:
        """Get context metrics."""
        return ContextMetrics(
            total_contexts=len(self.contexts),
            total_capabilities=sum(len(caps) for caps in self.capabilities.values()),
            total_protocols=len(self.protocols),
            last_updated=datetime.now(),
        )
