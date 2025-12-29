#!/usr/bin/env python3
"""
<!-- SSOT Domain: core -->

Swarm Coordination Analyzer - V2 Compliance Module

Author: Agent-6 (Coordination & Communication Specialist)
Mission: V2 Compliance - Modular Architecture
Status: REFACTORED - Clean separation of concerns
"""

from datetime import datetime
from typing import Any

from ..data_models import SwarmCoordinationInsight
from ..enums import ConfidenceLevel, ImpactLevel, InsightType


class SwarmCoordinationAnalyzer:
    """Analyzes swarm coordination patterns and agent collaboration."""

    def __init__(self):
        """Initialize swarm coordination analyzer."""
        self.analysis_history: list[dict[str, Any]] = []

    async def analyze_swarm_coordination(
        self,
        agent_data: list[dict[str, Any]],
        mission_data: list[dict[str, Any]],
        time_window_hours: int = 24,
    ) -> list[SwarmCoordinationInsight]:
        """Analyze swarm coordination patterns."""
        try:
            insights = []

            # Analyze agent collaboration patterns
            collaboration_insights = await self._analyze_collaboration_patterns(agent_data)
            insights.extend(collaboration_insights)

            # Analyze mission coordination
            mission_insights = await self._analyze_mission_coordination(mission_data)
            insights.extend(mission_insights)

            # Analyze performance trends
            performance_insights = await self._analyze_performance_trends(
                agent_data, time_window_hours
            )
            insights.extend(performance_insights)

            # Store analysis history
            self.analysis_history.append(
                {
                    "timestamp": datetime.now(),
                    "agent_count": len(agent_data),
                    "mission_count": len(mission_data),
                    "insights_generated": len(insights),
                }
            )

            return insights

        except Exception:
            # Return empty insights on error
            return []

    async def _analyze_collaboration_patterns(
        self, agent_data: list[dict[str, Any]]
    ) -> list[SwarmCoordinationInsight]:
        """Analyze agent collaboration patterns using real message history data."""
        insights = []
        
        try:
            from src.repositories.message_repository import MessageRepository
            
            message_repo = MessageRepository()
            
            # Get message history for collaboration analysis
            message_history = message_repo.get_message_history(limit=1000)
            
            if not message_history:
                # No message data - return minimal insight
                if len(agent_data) > 2:
                    insights.append(
                        SwarmCoordinationInsight(
                            insight_id=f"collab_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                            insight_type=InsightType.COLLABORATION,
                            description="Limited collaboration data available",
                            confidence_level=ConfidenceLevel.LOW,
                            impact_level=ImpactLevel.LOW,
                            key_findings=["Insufficient message history for analysis"],
                            recommendations=["Collect more message data for accurate analysis"],
                            generated_at=datetime.now(),
                        )
                    )
                return insights
            
            # Analyze agent-to-agent communication patterns
            agent_ids = [agent.get("agent_id") or agent.get("id", "") for agent in agent_data]
            agent_ids = [aid for aid in agent_ids if aid]
            
            if not agent_ids:
                return insights
            
            # Count messages between agents
            collaboration_matrix = {}
            total_messages = 0
            agent_message_counts = {}
            
            for message in message_history:
                sender = message.get("from") or message.get("sender", "")
                recipient = message.get("to") or message.get("recipient", "")
                
                # Only count messages between known agents
                if sender in agent_ids and recipient in agent_ids:
                    # Count bidirectional collaboration
                    pair_key = tuple(sorted([sender, recipient]))
                    collaboration_matrix[pair_key] = collaboration_matrix.get(pair_key, 0) + 1
                    total_messages += 1
                    
                    # Count per-agent messages
                    agent_message_counts[sender] = agent_message_counts.get(sender, 0) + 1
                    agent_message_counts[recipient] = agent_message_counts.get(recipient, 0) + 1
            
            if total_messages == 0:
                return insights
            
            # Calculate collaboration metrics
            active_pairs = len(collaboration_matrix)
            avg_messages_per_pair = total_messages / max(1, active_pairs)
            most_active_pair = max(collaboration_matrix.items(), key=lambda x: x[1]) if collaboration_matrix else None
            avg_agent_messages = sum(agent_message_counts.values()) / max(1, len(agent_message_counts))
            
            # Determine collaboration strength
            collaboration_strength = "strong" if avg_messages_per_pair > 10 else "moderate" if avg_messages_per_pair > 5 else "weak"
            confidence = ConfidenceLevel.HIGH if total_messages > 50 else ConfidenceLevel.MEDIUM if total_messages > 20 else ConfidenceLevel.LOW
            
            # Generate findings
            findings = [
                f"Total inter-agent messages: {total_messages}",
                f"Active collaboration pairs: {active_pairs}",
                f"Average messages per pair: {avg_messages_per_pair:.1f}",
                f"Average messages per agent: {avg_agent_messages:.1f}",
            ]
            
            if most_active_pair:
                findings.append(f"Most active pair: {most_active_pair[0][0]} ↔ {most_active_pair[0][1]} ({most_active_pair[1]} messages)")
            
            # Generate recommendations
            recommendations = []
            if collaboration_strength == "weak":
                recommendations.extend([
                    "Increase inter-agent communication",
                    "Establish more collaboration channels",
                ])
            elif collaboration_strength == "strong":
                recommendations.extend([
                    "Maintain current collaboration patterns",
                    "Consider expanding successful collaboration pairs",
                ])
            else:
                recommendations.extend([
                    "Monitor collaboration trends",
                    "Encourage more active agent pairs",
                ])
            
            insights.append(
                SwarmCoordinationInsight(
                    insight_id=f"collab_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    insight_type=InsightType.COLLABORATION,
                    description=f"{collaboration_strength.capitalize()} agent collaboration patterns detected",
                    confidence_level=confidence,
                    impact_level=ImpactLevel.MEDIUM if collaboration_strength == "strong" else ImpactLevel.LOW,
                    key_findings=findings,
                    recommendations=recommendations,
                    generated_at=datetime.now(),
                )
            )
            
        except (ImportError, Exception) as e:
            # Fallback to minimal insight on error
            if len(agent_data) > 2:
                insights.append(
                    SwarmCoordinationInsight(
                        insight_id=f"collab_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                        insight_type=InsightType.COLLABORATION,
                        description="Collaboration analysis unavailable",
                        confidence_level=ConfidenceLevel.LOW,
                        impact_level=ImpactLevel.LOW,
                        key_findings=[f"Analysis error: {str(e)}"],
                        recommendations=["Check message repository availability"],
                        generated_at=datetime.now(),
                    )
                )
        
        return insights

    async def _analyze_mission_coordination(
        self, mission_data: list[dict[str, Any]]
    ) -> list[SwarmCoordinationInsight]:
        """Analyze mission coordination patterns using real mission data."""
        insights = []
        
        if not mission_data:
            return insights
        
        try:
            from src.infrastructure.persistence.task_repository import TaskRepository
            from src.infrastructure.persistence.database_connection import DatabaseConnection
            
            db = DatabaseConnection()
            task_repo = TaskRepository(db)
            
            # Get all tasks for mission analysis
            all_tasks = list(task_repo.list_all(limit=1000))
            
            if not all_tasks:
                # No task data - analyze mission_data directly
                return self._analyze_mission_data_directly(mission_data)
            
            # Calculate mission coordination metrics
            completed_missions = sum(1 for mission in mission_data if mission.get("status") == "completed" or mission.get("completed_at"))
            total_missions = len(mission_data)
            completion_rate = completed_missions / max(1, total_missions)
            
            # Calculate average completion time from tasks
            completed_tasks = [t for t in all_tasks if t.completed_at and t.assigned_at]
            completion_times = []
            for task in completed_tasks:
                if task.assigned_at and task.completed_at:
                    duration = (task.completed_at - task.assigned_at).total_seconds() / 3600  # hours
                    completion_times.append(duration)
            
            avg_completion_time = sum(completion_times) / max(1, len(completion_times)) if completion_times else 0
            
            # Analyze mission assignment patterns
            mission_agents = {}
            for mission in mission_data:
                agent_id = mission.get("assigned_agent_id") or mission.get("agent_id")
                if agent_id:
                    mission_agents[agent_id] = mission_agents.get(agent_id, 0) + 1
            
            # Calculate coordination efficiency
            coordination_efficiency = "high" if completion_rate > 0.8 else "medium" if completion_rate > 0.6 else "low"
            confidence = ConfidenceLevel.HIGH if total_missions > 10 else ConfidenceLevel.MEDIUM if total_missions > 5 else ConfidenceLevel.LOW
            
            # Generate findings
            findings = [
                f"Mission completion rate: {completion_rate * 100:.1f}%",
                f"Total missions analyzed: {total_missions}",
                f"Completed missions: {completed_missions}",
            ]
            
            if avg_completion_time > 0:
                findings.append(f"Average completion time: {avg_completion_time:.1f} hours")
            
            if mission_agents:
                findings.append(f"Agents involved: {len(mission_agents)}")
                most_active_agent = max(mission_agents.items(), key=lambda x: x[1])
                findings.append(f"Most active agent: {most_active_agent[0]} ({most_active_agent[1]} missions)")
            
            # Generate recommendations
            recommendations = []
            if coordination_efficiency == "low":
                recommendations.extend([
                    "Improve mission assignment algorithms",
                    "Increase mission completion monitoring",
                    "Provide additional resources for struggling missions",
                ])
            elif coordination_efficiency == "high":
                recommendations.extend([
                    "Maintain current coordination efficiency",
                    "Scale successful coordination patterns",
                ])
            else:
                recommendations.extend([
                    "Optimize mission assignment algorithms",
                    "Improve resource allocation",
                    "Monitor mission progress more closely",
                ])
            
            insights.append(
                SwarmCoordinationInsight(
                    insight_id=f"mission_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    insight_type=InsightType.MISSION_COORDINATION,
                    description=f"{coordination_efficiency.capitalize()} mission coordination efficiency observed",
                    confidence_level=confidence,
                    impact_level=ImpactLevel.HIGH if coordination_efficiency == "high" else ImpactLevel.MEDIUM,
                    key_findings=findings,
                    recommendations=recommendations,
                    generated_at=datetime.now(),
                )
            )
            
        except (ImportError, Exception) as e:
            # Fallback to direct mission data analysis
            return self._analyze_mission_data_directly(mission_data)
        
        return insights
    
    def _analyze_mission_data_directly(self, mission_data: list[dict[str, Any]]) -> list[SwarmCoordinationInsight]:
        """Fallback: Analyze mission data directly without task repository."""
        insights = []
        
        if not mission_data:
            return insights
        
        completed = sum(1 for m in mission_data if m.get("status") == "completed" or m.get("completed_at"))
        total = len(mission_data)
        completion_rate = completed / max(1, total)
        
        insights.append(
            SwarmCoordinationInsight(
                insight_id=f"mission_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                insight_type=InsightType.MISSION_COORDINATION,
                description="Mission coordination analysis (limited data)",
                confidence_level=ConfidenceLevel.MEDIUM,
                impact_level=ImpactLevel.MEDIUM,
                key_findings=[
                    f"Mission completion rate: {completion_rate * 100:.1f}%",
                    f"Total missions: {total}",
                ],
                recommendations=[
                    "Collect more mission data for detailed analysis",
                    "Monitor mission progress closely",
                ],
                generated_at=datetime.now(),
            )
        )
        
        return insights

    async def _analyze_performance_trends(
        self, agent_data: list[dict[str, Any]], time_window_hours: int
    ) -> list[SwarmCoordinationInsight]:
        """Analyze performance trends using real historical performance data."""
        insights = []
        
        if not agent_data or len(agent_data) < 2:
            return insights
        
        try:
            from src.repositories.metrics_repository import MetricsRepository
            from datetime import timedelta
            
            metrics_repo = MetricsRepository()
            
            # Get metrics history for the time window
            cutoff_time = datetime.now() - timedelta(hours=time_window_hours)
            
            # Get recent metrics snapshots
            recent_snapshots = metrics_repo.get_metrics_history(limit=100)
            
            if not recent_snapshots:
                # No metrics data - analyze agent status data
                return self._analyze_agent_performance_directly(agent_data, time_window_hours)
            
            # Filter snapshots by time window
            window_snapshots = []
            for snapshot in recent_snapshots:
                snapshot_time_str = snapshot.get("timestamp", "")
                try:
                    snapshot_time = datetime.fromisoformat(snapshot_time_str.replace('Z', '+00:00'))
                    if snapshot_time >= cutoff_time:
                        window_snapshots.append(snapshot)
                except (ValueError, AttributeError):
                    continue
            
            if len(window_snapshots) < 2:
                # Not enough data points for trend analysis
                return self._analyze_agent_performance_directly(agent_data, time_window_hours)
            
            # Analyze performance trends from metrics
            # Get key performance metrics
            performance_metrics = [
                "queue.processing",
                "queue.depth",
                "messages.total",
                "tasks.completed",
            ]
            
            trends = {}
            for metric_name in performance_metrics:
                trend_data = metrics_repo.get_metrics_trend(metric_name, limit=50)
                if len(trend_data) >= 2:
                    # Calculate trend (positive = improving, negative = declining)
                    recent_avg = sum(trend_data[:len(trend_data)//2]) / max(1, len(trend_data)//2)
                    older_avg = sum(trend_data[len(trend_data)//2:]) / max(1, len(trend_data) - len(trend_data)//2)
                    
                    if older_avg > 0:
                        change_pct = ((recent_avg - older_avg) / older_avg) * 100
                        trends[metric_name] = change_pct
            
            # Determine overall trend
            if not trends:
                return self._analyze_agent_performance_directly(agent_data, time_window_hours)
            
            avg_trend = sum(trends.values()) / len(trends)
            trend_direction = "improving" if avg_trend > 5 else "declining" if avg_trend < -5 else "stable"
            
            # Calculate confidence based on data points
            confidence = ConfidenceLevel.HIGH if len(window_snapshots) > 20 else ConfidenceLevel.MEDIUM if len(window_snapshots) > 10 else ConfidenceLevel.LOW
            
            # Generate findings
            findings = [
                f"Performance trend: {trend_direction}",
                f"Average change: {avg_trend:+.1f}%",
                f"Metrics analyzed: {len(trends)}",
                f"Data points: {len(window_snapshots)}",
            ]
            
            # Add specific metric trends
            for metric, change in sorted(trends.items(), key=lambda x: abs(x[1]), reverse=True)[:3]:
                findings.append(f"{metric}: {change:+.1f}%")
            
            # Generate recommendations
            recommendations = []
            if trend_direction == "improving":
                recommendations.extend([
                    "Continue current optimization strategies",
                    "Monitor for performance plateaus",
                    "Scale successful performance improvements",
                ])
            elif trend_direction == "declining":
                recommendations.extend([
                    "Investigate performance degradation causes",
                    "Review recent system changes",
                    "Implement performance recovery measures",
                ])
            else:
                recommendations.extend([
                    "Maintain current performance levels",
                    "Identify optimization opportunities",
                    "Monitor for performance changes",
                ])
            
            insights.append(
                SwarmCoordinationInsight(
                    insight_id=f"perf_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    insight_type=InsightType.PERFORMANCE,
                    description=f"{trend_direction.capitalize()} performance trends detected",
                    confidence_level=confidence,
                    impact_level=ImpactLevel.HIGH if abs(avg_trend) > 10 else ImpactLevel.MEDIUM,
                    key_findings=findings,
                    recommendations=recommendations,
                    generated_at=datetime.now(),
                )
            )
            
        except (ImportError, Exception) as e:
            # Fallback to direct agent performance analysis
            return self._analyze_agent_performance_directly(agent_data, time_window_hours)
        
        return insights
    
    def _analyze_agent_performance_directly(
        self, agent_data: list[dict[str, Any]], time_window_hours: int
    ) -> list[SwarmCoordinationInsight]:
        """Fallback: Analyze agent performance directly from agent data."""
        insights = []
        
        if not agent_data:
            return insights
        
        # Analyze agent status data
        active_agents = sum(1 for agent in agent_data if agent.get("status") == "ACTIVE_AGENT_MODE")
        total_agents = len(agent_data)
        activity_rate = active_agents / max(1, total_agents)
        
        insights.append(
            SwarmCoordinationInsight(
                insight_id=f"perf_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                insight_type=InsightType.PERFORMANCE,
                description="Performance trend analysis (limited data)",
                confidence_level=ConfidenceLevel.MEDIUM,
                impact_level=ImpactLevel.MEDIUM,
                key_findings=[
                    f"Active agents: {active_agents}/{total_agents}",
                    f"Activity rate: {activity_rate * 100:.1f}%",
                ],
                recommendations=[
                    "Collect more performance metrics for detailed analysis",
                    "Monitor agent activity patterns",
                ],
                generated_at=datetime.now(),
            )
        )
        
        return insights
